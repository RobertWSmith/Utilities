# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 14:46:15 2014

@author: robert.w.smith08@gmail.com
"""

import abc
import csv

class StreamWriter(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, dialect = 'excel-tab', encoding = 'utf-8'):
        self.dialect = dialect
        self.encoding = encoding
        self.newline = ''
        if isinstance(dialect, str):
            self.dialect = dialect
        if isinstance(encoding, str):
            self.encoding = encoding

    def write(self, stream, filename):
        with open(filename, mode = 'w', encoding = self.encoding, newline = self.newline) as output_file:
            my_writer = csv.writer(output_file, dialect = self.dialect)
            my_writer.writerows(stream)







############################## BEGIN TESTS ####################################

#import unittest
#
#
#class Test_User(unittest.TestCase):
#
#    my_dsn = "LCLPSQL"
#    my_uid = "rob"
#    my_pwd = "1234Abc"
#    my_database = "rob"
#
#    def test_connection_kwargs(self):
#        test_user = User(dsn = self.my_dsn, uid = self.my_uid, pwd = self.my_pwd, database = self.my_database)
#        expected_result = {'dsn': self.my_dsn, 'uid': self.my_uid, 'pwd': self.my_pwd, 'database': self.my_database}
#        self.assertEqual(test_user.connection_kwargs, expected_result)
#
#    def test_connection_string(self):
#        test_user = User(dsn = self.my_dsn, uid = self.my_uid, pwd = self.my_pwd, database = self.my_database)
#        expected_result = "DSN={0};UID={1};PWD={2};".format(self.my_dsn, self.my_uid, self.my_pwd)
#        self.assertEqual(test_user.connection_string, expected_result)
#
#
#class Test_Connection(unittest.TestCase):
#
#    postgres_db = {'dsn': 'LCLPSQL', 'uid': 'rob', 'pwd':'4344', 'database': 'rob'}
#    teradata_db = {'dsn': 'EDWTDDEV', 'uid': 'A421356', 'pwd': 'Middle12'}
#
#    def test_connection(self):
#        my_conn = Connection(**self.postgres_db)
#        expected_result = (1, )
#
#        my_output = [val for val in my_conn.execute('SELECT 1;')]
#        my_result = tuple(my_output[0])
#        self.assertEqual(my_result, expected_result)



############################## END TESTS ######################################


#if __name__ == "__main__":
#    unittest.main()










