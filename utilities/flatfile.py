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



