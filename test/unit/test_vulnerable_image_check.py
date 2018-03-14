import os
import sys
import imp
import unittest
import cloudpassage


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


class Test_Vulnerable_Image_Check(unittest.TestCase):
    '''
           Test the scan examples
    '''

    def setUp(self):
        # get a config and halo object
        self.config = config_helper.ConfigHelper()

    def test_vulnerable_image_check(self):
        '''
            Test sva scan examples
        '''

        # save key
        self.temp = self.config.halo_key

        # invalidate key
        self.config.halo_key = None

        # init class object
        vic = vulnerable_image_check.VulnerableImageCheck(self.config)

        print "Testing with invalid credentials.\n"

        # test with invalid credentials
        self.test_invalid_credentials(vic)

        # restore key
        self.config.halo_key = self.temp

        # clean up misconfigured object
        del vic

        # init class object again
        vic = vulnerable_image_check.VulnerableImageCheck(self.config)

        print "Testing with default configuration.\n"
        # test with a default config
        self.test_default_config(vic)

        image_issues_endpoint = \
            "/v1/image_issues?critical=true&status=active"

        print "Testing endpoint URL with defaults\n"

        # pass in registry name, repository name, and image tag as None
        # (default values)
        formatted_image_issues_endpoint = \
            self.test_paramaterize_images_issues_endpoint(
                image_issues_endpoint, vic)

        self.assertEqual(image_issues_endpoint,
                         formatted_image_issues_endpoint)

        print "Testing endpoint URL with empty strings\n"

        # pass in registry name, repository name, and image tag as ""
        self.config.registry_name = ""
        self.config.repository_name = ""
        self.config.image_tag = ""

        formatted_image_issues_endpoint = \
            self.test_paramaterize_images_issues_endpoint(
                image_issues_endpoint, vic)

        self.assertEqual(image_issues_endpoint,
                         formatted_image_issues_endpoint)

        print "Testing endpoint URL with custom values\n"
        # pass in registry name, repository name, and image tag as ""
        self.config.registry_name = "registry_name"
        self.config.repository_name = "repo_name"
        self.config.image_tag = "image_tag"

        formatted_image_issues_endpoint = \
            self.test_paramaterize_images_issues_endpoint(
                image_issues_endpoint, vic)

        customized_image_issues_endpoint = \
            "/v1/image_issues?critical=true&status=active&registry_name=" \
            "registry_name&repository_name=repo_name&image_tag=image_tag"

        self.assertEqual(customized_image_issues_endpoint,
                         formatted_image_issues_endpoint)

    def test_default_config(self, vic):
        """
        Test with a default configuration
        """

        image_issues = vic.vulnerable_image_check()

        # confirm the result is a dictionary
        dict_object = False

        if isinstance(image_issues, dict):
            dict_object = True

        self.assertTrue(dict_object)

    def test_invalid_credentials(self, vic):
        """
        Test with invalid credential
        """

        # expect to get a cloudpassage.CloudPassageAuthentication error
        self.assertRaises(cloudpassage.CloudPassageAuthentication,
                          lambda: vic.vulnerable_image_check())

    def test_paramaterize_images_issues_endpoint(self, image_issues_endpoint,
                                                 vic):
        formatted_image_issues_endpoint = \
            vic.paramaterize_images_issues_endpoint(image_issues_endpoint)

        return formatted_image_issues_endpoint


if __name__ == "__main__":
    unittest.main()