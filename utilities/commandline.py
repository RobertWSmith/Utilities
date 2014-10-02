# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 19:19:41 2014

@author: robert.w.smith08@gmail.com
"""

import abc
import os
#import subprocess
import urllib.parse
import itertools


class CommandArg(metaclass=abc.ABCMeta):
    """
    Builds command line arg text for subprocess.call() on Windows
    """

    def __init__(self, exec_file, *args):
        self.exec_file = os.path.normpath(str(exec_file))
        self.exec_dir = os.path.dirname(self.exec_file)
        self.exec_basename = os.path.basename(self.exec_file)
        self.run_args = list([arg for arg in args])

    @property
    def args(self):
        return list(itertools.chain([CommandArg.double_quote(self.exec_file),  ], self.run_args))

    def instance_args(self, *args):
        return list(itertools.chain(self.args, [arg for arg in args]))

    @staticmethod
    def double_quote(string):
        return ''.join(['"', str(string), '"'])

    @staticmethod
    def arg_concat(arg, filepath, sep = ''):
        return sep.join([arg, CommandArg.double_quote(filepath)])

    @staticmethod
    def test_filepath(filepath):
        return os.path.isfile(filepath) or os.path.isdir(filepath)



class SapQuery(CommandArg):
    """
    Builds command line arg string for Winshuttle Query.
    """

    def __init__(self, alf):
        my_exec_file = os.path.normpath("C:/Program Files (x86)/Winshuttle/QUERY/querySHUTTLEcom.exe")
        my_alf_arg = '-alf'
        my_alf_file = CommandArg.double_quote(os.path.normpath(str(alf)))
        supress_prod_warning = '-spw'

        super().__init__(my_exec_file, *[my_alf_arg, my_alf_file, supress_prod_warning])

        self.central_site = urllib.parse.urlparse("http://corp-lite.goodyear.com/sites/WinshuttleCentral/QueryFiles/")

        self.my_result_arg = '-rfn'
        self.my_result_file = None

        self.my_run_arg = '-run'
        self.my_run_file = None

    @property
    def args(self):
        return list(itertools.chain(super().args, [self.my_run_arg, CommandArg.double_quote(urllib.parse.urljoin(self.central_site.geturl(), self.my_run_file)), self.my_result_arg, self.my_result_file]))

    def instance_args(self, result_file, run_file):
        self.my_result_file = os.path.normpath(str(result_file))
        self.my_run_file = str(run_file)
        return self.args



############################## BEGIN TESTS ####################################

import unittest


class Test_CommandArg(unittest.TestCase):

    my_exec_files = (os.path.normpath('C:/Abc/123.exe'), )
    my_run_args = ('-a', '--help')

    def test_exec_args(self):
        sp = CommandArg(self.my_exec_files[0], self.my_run_args)
        self.assertEqual(sp.args[0], CommandArg.double_quote(self.my_exec_files[0]))
        self.assertEqual(sp.args[1], self.my_run_args)


class Test_SapQuery(unittest.TestCase):

    my_run_files = ('tlb_master.qsq', )
    my_result_files = ('C:/output.txt', )
    my_alf_file = ('C:/Users/A421356/Winshuttle/Alf/AP0010.alf', )

    def test_args(self):
        expected_result = ['"C:\\Program Files (x86)\\Winshuttle\\QUERY\\querySHUTTLEcom.exe"', '-run', '"http://corp-lite.goodyear.com/sites/WinshuttleCentral/QueryFiles/tlb_master.qsq"', '-rfn', '"C:\\output.txt"',  '-alf', '"C:\\Users\\A421356\\Winshuttle\\Alf\\AP0010.alf"', '-spw']
        my_alf = os.path.normpath('C:/Users/A421356/Winshuttle/Alf/AP0010.alf')
        my_result_file = CommandArg.double_quote(os.path.normpath('C:/output.txt'))
        my_run_file = 'tlb_master.qsq'
        sp = SapQuery(alf = my_alf)
        my_result = sp.instance_args(result_file = my_result_file, run_file = my_run_file)
        print(my_result)
        # final test
        self.assertSetEqual(set(my_result), set(expected_result))



############################## END TESTS ######################################


if __name__ == "__main__":
    unittest.main()



