import sys, os, yaml, json, unittest
sys.path.append('..')
# from functools import partial
from lib.storj_env import StorjEnv

class TestStorjEnv(unittest.TestCase):
    def setUp(self):
        options_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'options.yml')
        with open(options_path, 'r') as options_file:
            self.options = yaml.load(options_file.read())

    def test_get_info(self):
        env = StorjEnv(**self.options)
        env.get_info(self.assert_get_info)

    def assert_get_info(self, error, info_json):
        # NB: WIP this doesn't work...
        info = json.loads(info_json)
        print(info['host'])
        print(info['info']['title'])
        self.assertTrue(False)
        self.assertEqual(info['host'], self.options['bridge_options']['host'])
        self.assertEqual(info['info']['title'], 'ballz')
