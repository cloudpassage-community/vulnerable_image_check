import os
import sys
import imp
import unittest

# import modules
here_dir = os.path.dirname(os.path.abspath(__file__))

module_name = 'config_helper'
module_path = os.path.join(here_dir, '../../vulnerable_image_check/')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
config_helper = imp.load_module(module_name, fp, pathname, description)


class TestConfigHelper(unittest.TestCase):
    '''
           Test the configuration
    '''

    def setUp(self):
        pass

    def test_config(self):
        '''
            Test if the config is as expected
        '''

        config = None
        EXIT_CODE = "0"

        # get config
        config = config_helper.ConfigHelper()

        # these are set in the .travis.yml
        self.assertNotEqual(config.halo_key, None)
        self.assertNotEqual(config.halo_secret, None)

        # registry_name can be unset
        self.assertEqual(config.registry_name, None)

        # repository_name can be unset
        self.assertEqual(config.repository_name, None)

        # image tag can be unset
        self.assertEqual(config.image_tag, None)

        # ensure default is correct
        self.assertEqual(config.exit_code, EXIT_CODE)

        # check defaults
        self.assertEqual(config.output_format, None)
        self.assertEqual(config.octo_box, False)

if __name__ == '__main__':
    unittest.main()
