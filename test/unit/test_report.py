import csv
import base64
import imp
import os
import re
import sys
import unittest

# import modules
here_dir = os.path.dirname(os.path.abspath(__file__))

module_name = 'config_helper'
module_path = os.path.join(here_dir, '../../vulnerable_image_check/')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
config_helper = imp.load_module(module_name, fp, pathname, description)

module_name = 'vulnerable_image_check'
module_path = os.path.join(here_dir, '../../vulnerable_image_check/')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
vulnerable_image_check = \
    imp.load_module(module_name, fp, pathname, description)

module_name = 'report'
module_path = os.path.join(here_dir, '../../vulnerable_image_check/lib/')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
report = \
    imp.load_module(module_name, fp, pathname, description)

class Test_Report(unittest.TestCase):
    '''
           Test the output format
    '''

    def setUp(self):
        # get a config and halo object
        self.config = config_helper.ConfigHelper()

        # init class object
        self.vic = vulnerable_image_check.VulnerableImageCheck(self.config)

        # run the scan
        self.vic_output = self.vic.vulnerable_image_check()

        # init class object
        self.r = report.Report()

    def test_report(self):
        '''
            Test the report output
        '''
        exit_value = 0
        SUCCESS = 0
        FAIL = 1
        file_path = "/tmp/"
        file_name = "csv_report.csv"
        file = "%s%s" % (file_path, file_name)
        corrupt = False

        # test valid csv data
        exit_value = self.test_csv_output(exit_value, file)

        # test return value is successful
        self.assertEqual(exit_value, SUCCESS)

        #corrupt data
        self.corrupt_data(file)

        # test invalid csv data
        exit_value = self.test_csv_output(exit_value, file)

        # remove file
        os.remove(file)

        # test return value is failure
        self.assertEqual(exit_value, FAIL)

        # reset exit value default
        exit_value = SUCCESS

        # test with good data
        exit_value = self.test_formatted_output(exit_value, corrupt)

        self.assertEqual(exit_value, SUCCESS)

        # test with corrupt data
        corrupt = True
        exit_value = self.test_formatted_output(exit_value, corrupt)

        self.assertEqual(exit_value, FAIL)

    def test_csv_output(self, exit_value, file):
        """
        Validates the format of the csv data

        :param exit_value: int
        file: str
        :return: exit_value: int
        """

        READ = "r"
        WRITE = "w"
        FAIL = 1
        COMMA = ","
        fields = ""
        CORRECT_NUM_FIELDS = 6

        # run the report
        csv_report = self.r.create_csv_report(self.vic_output)

        # decode the output
        csv_report = base64.b64decode(csv_report)

        # write the data to a file if it does not exist
        if os.path.exists(file) is False:
            fh = open(file, WRITE)
            fh.write(csv_report)
            fh.close()

        # open for reading
        fh = open(file, READ)

        # get a csv reader object
        csv_reader = csv.reader(fh, delimiter=COMMA)

        # read each row and validate it
        for row in csv_reader:

            # now have a string rather than a list
            row = COMMA.join(row)

            # split the comma delimited data and confirm number of fields
            fields = row.split(COMMA)
            num_fields = len(fields)

            # if not correct then set exit value and break loop
            if num_fields != CORRECT_NUM_FIELDS:
                exit_value = FAIL
                break

        # close handle and remove the file
        fh.close()

        # if it is a failure then write the message
        if exit_value == FAIL:
            ERROR_MESSAGE = \
                "Not all data is in csv format... error in row \'%s\'\n" % row
            print ERROR_MESSAGE

        return exit_value

    def corrupt_data(self, file):
        """
        Add a non-csv line

        :param file: (str) fully qualified path to file
        """
        APPEND = "a"
        data = "This is not csv data ha ha ha ha (in a low evil voice)"

        with open(file, APPEND) as data_file:
            data_file.write(data)
            data_file.close()

    def test_formatted_output(self, exit_value, corrupt):
        """
        Test the formatted output

        :param exit_value: int
        :param corrupt: bool
        :return: int
        """
        FIRST_ELEMENT = 0
        FAIL = 1
        bad_data = "This data will not work"

        # run the report
        text_report = self.r.create_stdout_report(self.vic_output)

        # decode the output
        text_report = base64.b64decode(text_report)

        # strip the characters to make it easier to validate an to make
        # regex much easier
        text_report = re.sub('[\n]', '', text_report)
        text_report = re.sub('[-]', '', text_report)
        text_report = re.sub('[.]', '', text_report)
        text_report = re.sub('[:]', '', text_report)
        text_report = re.sub('[/]', '', text_report)
        text_report = re.sub('[+]', '', text_report)
        text_report = re.sub('[~]', '', text_report)

        # split into a list of strings
        text_report = text_report.split("Registry")

        # get rid of invalid row
        del text_report[FIRST_ELEMENT]

        # if we will test bad data
        if corrupt is True:
            text_report.append(bad_data)

        # regex pattern
        pattern = \
            re.compile('\s\w+\s\sRepository\s\w+\s\s\s\sTag' \
                       '\s\w+\s\s\s\s\s\sVulnerabilities\s\s\s\s\s\s\s\s' \
                       'Package\s\w+\s\sPackage\sVersion\s\w+\s\|' \
                       '\sCVE\sList\s\w+')

        # check each row
        for row in text_report:
            match = pattern.search(row)

            if not match:
                exit_value = FAIL
                break

        return exit_value

if __name__ == "__main__":
    exit_value = unittest.main()
