import sys, os, yaml, json, unittest
from datetime import datetime
sys.path.append('..')

from lib.storj_env import StorjEnv
class TestStorjEnv(unittest.TestCase):
    def setUp(self):
        options_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'options.yml')
        with open(options_path, 'r') as options_file:
            self.options = yaml.load(options_file.read())

        self.env = StorjEnv(**self.options)

    def tearDown(self):
        self.env.destroy()

    def get_bucket_id(self, name):
        buckets = self.env.list_buckets()
        return next(bucket['id'] for bucket in buckets if bucket['name'] == name)

    def test_get_info(self):
        results = []

        def callback(error, _info):
            results.append(error)
            results.append(_info)

        self.env.get_info(callback)
        error, info = results
        self.assertEqual(error, None)
        self.assertEqual(info['host'], self.options['bridge_options']['host'])
        self.assertEqual(info['info']['title'], 'Storj Bridge')

class TestCreateDestroy(TestStorjEnv):
    def test_create_bucket_with_callback(self):
        bucket_name = 'python_libstorj-test'
        results = []

        def callback(error, _bucket):
            results.append(error)
            results.append(_bucket)

        self.env.create_bucket(bucket_name, callback)
        error, bucket = results
        self.assertEqual(error, None)
        self.assertEqual(bucket['name'], bucket_name)

    def test_create_bucket_without_callback(self):
        bucket_name = 'python_libstorj-test2'

        bucket = self.env.create_bucket(bucket_name)
        self.assertEqual(bucket['name'], bucket_name)

    def test_delete_bucket_with_callback(self):
        bucket_name = self.get_bucket_id('python_libstorj-test')
        results = []

        def callback(error):
            results.append(error)

        self.env.delete_bucket(bucket_name, callback)
        error = results[0]
        self.assertEqual(error, None)

    def test_delete_bucket_without_callback(self):
        bucket_name = self.get_bucket_id('python_libstorj-test2')

        self.env.delete_bucket(bucket_name)


class TestListBuckets(TestStorjEnv):
    def setUp(self):
        super(TestListBuckets, self).setUp()
        self.env.create_bucket('python_libstorj-test3')

    def tearDown(self):
        bucket_id = self.get_bucket_id('python_libstorj-test3')
        self.env.delete_bucket(bucket_id)
        super(TestListBuckets, self).tearDown()

    def test_list_buckets_with_callback(self):
        bucket_name = 'python_libstorj-test3'
        results = {
            'buckets': [],
            'error': ''
        }

        def callback(error, _buckets):
            results['error'] = error
            for i, bucket in enumerate(_buckets):
                results['buckets'].append(bucket)

        self.env.list_buckets(callback)
        buckets, error = [results[key] for key in ('buckets', 'error')]
        self.assertEqual(error, None)
        self.assertEqual(len(buckets), 1)
        self.assertIsInstance(buckets[0]['created'], datetime)
        self.assertEqual(buckets[0]['name'], bucket_name)

    def test_list_buckets_without_callback(self):
        bucket_name = 'python_libstorj-test3'

        buckets = self.env.list_buckets()
        self.assertEqual(len(buckets), 1)
        self.assertIsInstance(buckets[0]['created'], datetime)
        self.assertEqual(buckets[0]['name'], bucket_name)

