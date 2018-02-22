import base64
import csv
import io
from utility import Utility


class Report(object):
    """
    We use this class to generate text reports.
    Class based on awilson@cloudpassage.com's Report.py class and modified
    for this purpose
    """
    @classmethod
    def create_csv_report(cls, vulnerable_image_check_data):
        """
        Expect a dictionary object, produce text in CSV format.

        Args:
             - cls - reference to the current instance of hte class
             - vulnerable_image_check_data (dict) - dictionary of vulnerability
             data

        Return:
            - result (str) - base64 encoded vulnerability report
        """

        # initialize the list as we will have a list of dicts
        rows = []

        # let's build the output for all sets in the dataset
        # dataset is vulnerability info for all images in request
        for set in vulnerable_image_check_data["image_issues"]:
            # format the data for a cvs report
            row = cls.format_vulnerable_image_data_csv(set)
            # append each returned data set to the whole
            rows.append(row)

        # the fieldnames for the csv - DictWriter will order by these
        fieldnames = \
            ["registry", "repository", "tag",
             "package", "version", "image_digest"]

        # get a stream io object
        ephemeral_obj = io.BytesIO()

        # write the csv data
        csv_writer = csv.DictWriter(ephemeral_obj, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(rows)

        # encode to base64
        result = base64.b64encode(ephemeral_obj.getvalue())

        # clean up
        ephemeral_obj.close()

        # return report data
        return result

    @classmethod
    def create_stdout_report(cls, vulnerable_image_check_data):
        """
        Expect a dictionary object, produce text appropriate for stdout.

        Args:
            - cls - reference to the current instance of the class
            - vulnerable_image_check_data (dict) - dictionary of vulnerability
             data

        Return:
            - result (str) - base64 encoded vulnerability report

            Format of encoded data:

            Registry: DPR
              Repository: bkumar89/centos
                Tag: 7.1.1503
                  Vulnerabilities:
                    Package: binutils Package Version: 2.23.52.0.1-30.el7 | CVE List: cve-2014-8484 cve-2014-8485 # NOQA
        """

        result = ""

        # for each data set in all the data
        for set in vulnerable_image_check_data["image_issues"]:
            # format data as noted above
            pieces = cls.format_vulnerable_image_data(set)
            pieces = pieces.split('\n')
            pieces = "\n".join(pieces)

            # build full dataset
            result += pieces

        # encode data
        result = base64.b64encode(result)

        # return report data
        return result

    @classmethod
    def create_slack_reports(cls, channel_reference, default_channel,
                             routing_rules, instances):
        """Create a plaintext report for Slack.
        Args:
            channel_reference(dict): Keys are channel names, values are channel
                IDs.
            default_channel(str): Name of default Slack channel.
            routing_rules(dict): Rules for routing messages to different Slack
                channels.  Formatted like
                {"metadata_field_name":
                    {"metadata_field_value_to_match": "slack_channel_name"}}
            instances(dict): Instance metadata.
        Returns:
            dict: {"channel": "report"} where "channel" is the Slack channel
                ID and "report" is the text of the report.
        """
        organized = {}
        # Group by target Slack channel.
        for instance in instances:
            channel = Utility.get_channel_for_message(channel_reference,
                                                      instance, routing_rules,
                                                      default_channel)
            if channel not in organized:
                organized[channel] = []
            organized[channel].append(instance)
        # Build report per channel, each sorted by instance ID.
        report = {}
        for target, content in organized.items():
            x_content = {c.keys()[0]: c.values()[0] for c in content}
            report[target] = cls.create_stdout_report(x_content)
        return report

    @classmethod
    def format_vulnerable_image_data(cls, vic_data):
        """Format vulnerability data for reporting.
        Args:
            - cls - reference to the current instance of the class
            - vic_data (dict): Formatted like this:

            Registry: DPR
              Repository: bkumar89/centos
                Tag: 7.1.1503
                  Vulnerabilities:
                    Package: binutils Package Version: 2.23.52.0.1-30.el7 | CVE List: cve-2014-8484 cve-2014-8485 # NOQA
        """

        registry = \
            "\n\nRegistry: {registry}" \
            "".format(registry=vic_data["image"]["registry"]["name"])

        repository = \
            "  Repository: {repository}" \
            "".format(repository=vic_data["image"]["repository"]["name"])

        tag = \
            "    Tag: {tag}" \
            "".format(tag=vic_data["image"]["tag"])

        vulnerabilities = "      Vulnerabilities:"  # NOQA

        package = "        Package: {package}".format(package=vic_data["name"])

        # build package, package version and cve's into one line
        package_version = \
            "  Package Version: {package_version}" \
            "".format(package_version=vic_data["version"])
        package += package_version

        cves = ""
        for cve in vic_data["cves"]:
            cves += cve["name"]
            cves += " "

        cve_list = " | CVE List: {cve_list}".format(cve_list=cves)

        package += cve_list

        # order the fields and separate them by a newline
        ordered_fields = [registry, repository, tag, vulnerabilities, package]

        # return formatted report data
        return "\n".join(ordered_fields)

    @classmethod
    def format_vulnerable_image_data_csv(cls, vic_data):
        """
        Format vulnerability data for reporting in CSV format.
        Args:
            vic_data (dict) - vulnerability data

        Returns:
            result - (dict) - vulnerability report data
        """

        result = {"registry": vic_data["image"]["registry"]["name"],
                  "repository": vic_data["image"]["repository"]["name"],
                  "tag": vic_data["image"]["tag"],
                  "package": vic_data["name"],
                  "image_digest": vic_data["image"]["image_sha"],
                  "version": vic_data["version"]}

        return result
