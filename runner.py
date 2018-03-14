import base64
import os
import sys

exit_value = 0

# try to import the module which will be local or from a pip install
try:
    # import and instantiate the objects
    import vulnerable_image_check

    # get the config
    from vulnerable_image_check import config_helper
    config = config_helper.ConfigHelper()

    from vulnerable_image_check import vulnerable_image_check
    vic = vulnerable_image_check.VulnerableImageCheck(config)

    from vulnerable_image_check import lib
except ImportError as e:
    # module not found
    print "Import error: %s" % e
    sys.exit(exit_value)

DEFAULT_FORMAT = "csv"
NEWLINE = "\n"

# run the scan
vic_output = vic.vulnerable_image_check()

# output defaults to base64
report = base64.b64encode("\nNo vulnerabilies found in scan...\n")

# if there is not vulnerability data from the scan skip this section
if vic_output != {}:
    # default format is csv otherwise formatted text
    if config.output_format == DEFAULT_FORMAT:
        report = \
            lib.Report.create_csv_report(vic_output)
    else:
        report = \
            lib.Report.create_stdout_report(vic_output)

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
