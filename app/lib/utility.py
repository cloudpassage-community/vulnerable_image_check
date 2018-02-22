import os


class Utility(object):
    """This class contains functionality that make use of data from multiple
    external services.
    """
    @classmethod
    def build_routing_rules(cls):
        """Returns a dictionary which represents the message routing rules.
        Example:
        ``{"vpc_id": {"onetwo": "channel_one", "threefour": "channel_two"},
           "key_name": {"keyone": "channel_three"}}``
        """
        rule_structure = {}
        env_rules = os.getenv("SLACK_ROUTING")
        for rule in env_rules.split(";"):
            rule_parts = rule.split(",")
            if rule_parts[0] not in rule_structure:
                rule_structure[rule_parts[0]] = {rule_parts[1]: rule_parts[2]}
            else:
                rule_structure[rule_parts[0]][rule_parts[1]] = rule_parts[2]
        return rule_structure

    @classmethod
    def get_aws_config(cls):
        """Return a dict with AWS configuration information.
        If either the AWS_ACCOUNT_NUMBERS or AWS_ROLE_NAME environment
        variables are missing, only ``api_key`` and ``api_secret`` will be
        included in the returned dictionary.  Otherwise, the returned
        dictionary will also contain ``accounts``, which is a list of AWS
        accounts to scan for EC2 instance inventory, and ``role_name``, which
        is used in composing the role to assume in other accounts for creating
        an inventory of EC2 instances.
        """
        account_env = os.getenv("AWS_ACCOUNT_NUMBERS")
        role_name = os.getenv("AWS_ROLE_NAME")
        config = {"api_key": os.getenv("AWS_ACCESS_KEY_ID"),
                  "api_secret": os.getenv("AWS_SECRET_ACCESS_KEY")}
        if None not in [account_env, role_name]:
            config["accounts"] = account_env.split(";")
            config["role_name"] = role_name
        return config

    @classmethod
    def get_halo_config(cls):
        """Return a dict with Halo configuration information."""
        config = {"api_key": os.getenv("HALO_API_KEY"),
                  "api_secret": os.getenv("HALO_API_SECRET_KEY")}
        if os.getenv("HALO_API_HOST"):
            config["api_host"] = os.getenv("HALO_API_HOST")
        return config

    @classmethod
    def get_slack_config(cls):
        """Return a dict with Slack configuration information."""
        config = {"api_token": os.getenv("SLACK_API_TOKEN"),
                  "default_channel_name": os.getenv("SLACK_CHANNEL", "halo")}
        if os.getenv("SLACK_ROUTING"):
            config["routing_rules"] = cls.build_routing_rules()
        return config

    @classmethod
    def get_channel_for_message(cls, channel_reference, instance_metadata,
                                routing_rules, default_channel_name):
        """Return channel ID for messages pertaining to instance.
        Args:
            channel_reference(dict): Channel name is key, value is channel ID.
            instance_metadata(dict):
            routing_rules(dict): Rules for routing messages.  Formatted like
                this: {"ROUTING_KEY": {"ROUTING_KEY_VALUE": "CHANNEL_NAME",
                                       "ROUTING_KEY_VALUE": "CHANNEL_NAME"}}
            default_channel_name(str): Name of default channel for alerts
        """

        priorities = ["key_name", "vpc_id", "aws_region", "aws_account"]
        target_channel = channel_reference[default_channel_name]
        for priority in priorities:
            try:
                instance_meta_match = instance_metadata.items()[0][1][priority]
                routing_matchers = routing_rules[priority]
                target_channel = channel_reference[routing_matchers[instance_meta_match]]  # NOQA
                break
            except KeyError:
                pass
        return target_channel
