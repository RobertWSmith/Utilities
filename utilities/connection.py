# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 09:01:18 2014

@author: robert.w.smith08@gmail.com
"""

import abc
import pyodbc
import sys
import datetime


class User(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        self.driver = None
        self.dsn = None
        self.host = None
        self.uid = None
        self.pwd = None
        self.autocommit = None
        for key in self.__dict__.keys():
            self.__dict__[key] = kwargs.get(key)
        if not isinstance(self.autocommit, bool):
            self.autocommit = True

    def __del__(self):
        del self.driver
        del self.dsn
        del self.uid
        del self.pwd
        del self.autocommit

    def __getitem__(self, name):
        return self.__dict__[name]

    def __setitem__(self, name, value):
        set_val = None
        if name in self.__dict__.keys():
            if name == "autocommit" and isinstance(value, bool):
                set_val = True
            elif isinstance(value, str):
                set_val = True
            else:
                outval = None
                if name == "autocommit":
                    outval = bool
                else:
                    outval = str
                raise ValueError("field {0) must be type {1}".format(name, repr(outval)))
        else:
            raise AttributeError("field {0} not found in {1}".format(name, self.__class__.__name__))
        if set_val:
            self.__dict__[name] = value

    @property
    def connection_kwargs(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}

class Connection(User):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._conn = None
        self._conn_ts = None

    def __del__(self):
        self.close()
        del self._conn
        del self._conn_ts
        super().__del__()

    @property
    def connection(self):
        if self.is_alive:
            return self._conn
        else:
            self._conn = pyodbc.connect(**self.connection_kwargs)
            self._conn_ts = datetime.datetime.now()
            return self._conn

    def cursor(self):
        return self.connection.cursor()

    def close(self):
        if isinstance(self._conn, pyodbc.Connection):
            self._conn.close()
        self._conn = None
        self._conn_ts = None

    def execute(self, query, header = False):
        my_cursor = None
        if not isinstance(query, str):
            raise TypeError("query must be {0}".format(repr(str)))
        if not isinstance(header, bool):
            raise TypeError("header must be {0}".format(repr(bool)))
        try:
            my_cursor = self.cursor()
            my_cursor.execute(query)
            if header:
                yield tuple(val[0] for val in my_cursor.description)
            for row in my_cursor:
                yield row
        except pyodbc.DatabaseError as err:
            error, = err.args()
            sys.stderr(error)
            self.close()
            raise err
        finally:
            del my_cursor

    @property
    def is_alive(self):
        output_bool = None
        if not isinstance(self._conn_ts, datetime.datetime):
            output_bool = False
        elif not isinstance(self.conn, pyodbc.Connection):
            output_bool = False
        elif datetime.datetime.now() > self._conn_ts + datetime.timedelta(minutes=10) and isinstance(self.conn, pyodbc.Connection):
            output_bool = False
        else:
            my_cursor = self.cursor()
            if not isinstance(my_cursor, pyodbc.Cursor):
                output_bool = False
            try:
                res = my_cursor.execute('SELECT 1;').fetchall()
                if res == (1,):
                    self._conn_ts = datetime.datetime.now()
                    output_bool = True
            except pyodbc.DatabaseError as err:
                output_bool = False
                error, = err.args()
                sys.stderr(error)
        return output_bool

    def __connect(self):
            try:
                if not self.is_alive:
                    self._conn = None
                    self._conn = pyodbc.connect(**self.connection_kwargs)
            except pyodbc.DatabaseError as err:
                error, = err.args()
                sys.stderr(error)
                raise err
            finally:
                return self._conn


if __name__ == "__main__":
    conn = Connection(dsn = 'LCLPSQL', uid = 'rob', pwd = '4344')
    query = """
    select
        current_date
    """
    for row in conn.execute(query):
        print(row)
    del conn


