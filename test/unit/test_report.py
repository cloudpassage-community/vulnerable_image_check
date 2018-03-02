import csv
import base64
import os
import sys
import imp
import unittest

# import modules
here_dir = os.path.dirname(os.path.abspath(__file__))

module_name = 'config_helper'
module_path = os.path.join(here_dir, '../../app/vulnerable_image_check/')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
config_helper = imp.load_module(module_name, fp, pathname, description)

module_name = 'vulnerable_image_check'
module_path = os.path.join(here_dir, '../../app/vulnerable_image_check/')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
vulnerable_image_check = \
    imp.load_module(module_name, fp, pathname, description)

module_name = 'report'
module_path = os.path.join(here_dir, '../../app/lib/')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
report = \
    imp.load_module(module_name, fp, pathname, description)

class Test_Report(unittest.TestCase):
    '''
           Test the output format
    '''

    def setUp(self):
        pass

    def test_report(self):
        '''
            Test the report output
        '''
        exit_value = 0
        SUCCESS = 0

        exit_value = self.test_csv_output(exit_value)

        if exit_value != SUCCESS:
            sys.exit(exit_value)
        else:
            return exit_value

    def test_csv_output(self, exit_value):
        """
        Validates the format of the csv data

        :param exit_value: int
        :return: exit_value: int
        """

        READ = "r"
        WRITE = "w"
        FAIL = 1
        COMMA = ","
        file_path = "/tmp/"
        file_name = "csv_report.csv"
        fields = ""
        CORRECT_NUM_FIELDS = 6

        # get a config and halo object
        config = config_helper.ConfigHelper()

        # init class object
        vic = vulnerable_image_check.VulnerableImageCheck(config)

        # run the scan
        vic_output = vic.vulnerable_image_check()

        # init class object
        r = report.Report()

        # run the report
        config.output_format = "csv"
        csv_report = r.create_csv_report(vic_output)

        # decode the output
        csv_report = base64.b64decode(csv_report)

        # write the data to a file
        file = "%s%s" % (file_path, file_name)

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
        os.remove(file)

        # if it is a failure then write the message
        if exit_value == FAIL:
            ERROR_MESSAGE = \
                "Not all data is in csv format... error in row \'%s\'\n" % row
            print ERROR_MESSAGE

        return exit_value

if __name__ == "__main__":
    exit_value = unittest.main()
