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
        results = []

        def callback(error, _info):
            results.append(error)
            results.append(_info)

        env.get_info(callback)
        error, info = results
        self.assertEqual(error, None)
        self.assertEqual(info['host'], self.options['bridge_options']['host'])
        self.assertEqual(info['info']['title'], 'Storj Bridge')

    def test_create_bucket(self):
        bucket_name = "python_libstorj-test"
        env = StorjEnv(**self.options)
        results = []

        def callback(error, _bucket):
            results.append(error)
            results.append(_bucket)

        env.create_bucket(bucket_name, callback)
        error, bucket = results
        self.assertEqual(error, None)
        self.assertEqual(bucket['name'], bucket_name)

    def test_list_buckets(self):
        bucket_name = "python_libstorj-test"
        env = StorjEnv(**self.options)
        results = {
            'buckets': [],
            'error': ''
        }

        def callback(error, _buckets):
            results['error'] = error
            for i, bucket in enumerate(_buckets):
                results['buckets'].append(bucket)

        env.list_buckets(callback)
        buckets, error = [results[key] for key in ('buckets', 'error')]
        self.assertEqual(error, None)
        self.assertEqual(len(buckets), 1)
        self.assertEqual(buckets[0]['name'], bucket_name)
