import os


class ConfigHelper():
    """Manage all configuration information for the application"""
    def __init__(self):
        self.halo_key = None
        self.halo_secret = None
        self.registry_name = None
        self.repository_name = None
        self.image_tag = None
        self.output_format = None
        self.octo_box = None

        self.halo_key = os.getenv("HALO_API_KEY")
        self.halo_secret = os.getenv("HALO_API_SECRET_KEY")
        self.registry_name = os.getenv("REGISTRY_NAME")
        self.repository_name = os.getenv("REPO_NAME")
        self.image_tag = os.getenv("IMAGE_TAG")
        self.exit_code = os.environ["FAIL_ON_CRITICAL"] = "0"

        # valid value is csv - anything other than that will output formatted
        # text
        self.output_format = os.getenv("OUTPUT_FORMAT")

        # if the variable is not explicitly set the program will not run in
        # octo-box mode and will dump output as decoded base64
        self.octo_box = os.getenv("OCTO_BOX")

        if self.octo_box != "True":
            self.octo_box = False
        else:
            self.octo_box = True
