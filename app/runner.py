import base64
import os
import sys

# libraries used by runner
from lib.report import Report
# the program configuration
from vulnerable_image_check.config_helper import ConfigHelper # NOQA
# primary class
from vulnerable_image_check.vulnerable_image_check import VulnerableImageCheck # NOQA

DEFAULT_FORMAT = "csv"
NEWLINE = "\n"

# get the configuration
config = ConfigHelper()

# instantiate the vic object
vic = VulnerableImageCheck(config)

# run the scan
vic_output = vic.vulnerable_image_check()

# output defaults to base64
report = base64.b64encode("\nNo vulnerabilies found in scan...\n")

# if there is not vulnerability data from the scan skip this section
if vic_output != {}:
    # default format is csv otherwise formatted text
    if config.output_format == DEFAULT_FORMAT:
        report = Report.create_csv_report(vic_output)
    else:
        report = Report.create_stdout_report(vic_output)

print NEWLINE

# if ! running in octobox then decode the output
if config.octo_box is True:
    print report
else:
    print base64.b64decode(report)

# get exit value which is 1 if there are vulnerabilities.  This also causes
# a Jenkins job to fail
exit_value = os.getenv("FAIL_ON_CRITICAL")
exit_value = int(exit_value)

# exit with value
sys.exit(exit_value)
