import sys, os, yaml, json, unittest
sys.path.append('..')

from lib.storj_env import StorjEnv

class TestStorjEnv(unittest.TestCase):
    def setUp(self):
        options_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'options.yml')
        with open(options_path, 'r') as options_file:
            self.options = yaml.load(options_file.read())

    def test_get_info(self):
        env = StorjEnv(**self.options)
        info = [None]

        def callback(error, _info):
            info[0] = _info

        env.get_info(callback)
        info = info[0]
        self.assertEqual(info['host'], self.options['bridge_options']['host'])
        self.assertEqual(info['info']['title'], 'Storj Bridge')

    def test_list_buckets(self):
        env = StorjEnv(**self.options)
        buckets = []

        def callback(error, _buckets):
            for i, bucket in enumerate(_buckets):
                buckets.append(bucket)

        env.list_buckets(callback)
        self.assertEqual(len(buckets), 1)
        self.assertEqual(buckets[0]['name'], 'test')
