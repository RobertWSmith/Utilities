# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 14:36:14 2014

@author: A421356
"""

import abc
import pyodbc
import sys
import datetime


class User(object):
    """
    Internal class to hold connection details and generate the connection keyword
    arguments and / or  connection strings as properties
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        self.driver = kwargs.get('driver')
        # dsn, uid and pwd must be provided.
        self.dsn = kwargs.get('dsn') or ''
        self.uid = kwargs.get('uid') or ''
        self.pwd = kwargs.get('pwd') or ''
        self.database = kwargs.get('database')
        self.autocommit = kwargs.get('autocommit')
        self.ansi = kwargs.get('ansi')
        self.unicode_results = kwargs.get('unicode_results')
        # freeze the instance against type changes to existing variables or
        # additional fields
        self._is_frozen = True

    @property
    def connection_kwargs(self):
        """
        Property returns dict of keys and values relevant to pyodbc.connection
        """
        return {key: value for key, value in self.__dict__.items() if not key.startswith('_') and value is not None}

    @property
    def connection_string(self):
        """
        Minimal connection string
        """
        return 'DSN={0};UID={1};PWD={2};'.format(self.dsn, self.uid, self.pwd)


class Connection(User):
    """
    Connection object holds connection, and properly closes when it goes out of
    scope.
    Allows user to avoid reconnecting to run multiple queries, speeding up results.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._conn = None



    def __del__(self):
        """
        Attempts to properly close the connection
        """
        self.close()
        self._conn = None

    @property
    def connection(self):
        """
        Returns stored connection object -- if external connection is closed, object's
        connection may be closed as well.
        Object attempts to pool and preserve a connection.
        """
        if isinstance(self._conn, pyodbc.Connection):
            return self._conn
        else:
            return self.__connect()

    def __connect(self):
        """
        Internal connection logic.
        Only connection property should call this method.
        """
        if isinstance(self._conn, pyodbc.Connection):
            self._conn.close()
        self._conn = None
        try:
            self._conn = pyodbc.connect(**self.connection_kwargs)
            return self._conn
        except pyodbc.DatabaseError as err:
            error, = err.args()
            sys.stderr(error)
            self.close()
            raise err

    @property
    def cursor(self):
        """
        Cursor property creates a cursor from the connection property.
        Connection property confirms connection status, so cursor just needs to
        be concerned with if a cursor can or can not be created.
        """
        return self.connection.cursor()

    def close(self):
        """
        Close method calls the pyodbc Connection's close function (if self._conn
        is a Connection).
        Variables are returned to 'None' / Inital state
        """
        if isinstance(self._conn, pyodbc.Connection):
            self._conn.close()
        self._conn = None
        self._conn_ts = None

    def execute(self, query, header = False):
        """
        Executes query and acts as a iterable list over the result set.
        """
        if not isinstance(query, str):
            raise TypeError("query must be {0}".format(repr(str)))
        if not isinstance(header, bool):
            raise TypeError("header must be {0}".format(repr(bool)))
        with self.cursor.execute(query) as query_res:
            if header:
                yield tuple(val[0] for val in query_res.description)
            for row in query_res:
                yield row
            # update the connection timestamp to the time of the last successful
            # query completion
            self._conn_ts = datetime.datetime.now()
            query_res.commit()


############################## BEGIN TESTS ####################################

import unittest


class Test_User(unittest.TestCase):

    my_dsn = "LCLPSQL"
    my_uid = "rob"
    my_pwd = "1234Abc"
    my_database = "rob"

    def test_connection_kwargs(self):
        test_user = User(dsn = self.my_dsn, uid = self.my_uid, pwd = self.my_pwd, database = self.my_database)
        expected_result = {'dsn': self.my_dsn, 'uid': self.my_uid, 'pwd': self.my_pwd, 'database': self.my_database}
        self.assertEqual(test_user.connection_kwargs, expected_result)

    def test_connection_string(self):
        test_user = User(dsn = self.my_dsn, uid = self.my_uid, pwd = self.my_pwd, database = self.my_database)
        expected_result = "DSN={0};UID={1};PWD={2};".format(self.my_dsn, self.my_uid, self.my_pwd)
        self.assertEqual(test_user.connection_string, expected_result)


class Test_Connection(unittest.TestCase):

    postgres_db = {'dsn': 'LCLPSQL', 'uid': 'rob', 'pwd':'4344', 'database': 'rob'}
    teradata_db = {'dsn': 'EDWTDDEV', 'uid': 'A421356', 'pwd': 'Middle12'}

    def test_connection(self):
        my_conn = Connection(**self.postgres_db)
        expected_result = (1, )

        my_output = [val for val in my_conn.execute('SELECT 1;')]
        my_result = tuple(my_output[0])
        self.assertEqual(my_result, expected_result)



############################## END TESTS ######################################


if __name__ == "__main__":
    unittest.main()
