import sys, subprocess, yaml, json, unittest
from os import path
from datetime import datetime
from lib.storj_env import StorjEnv
sys.path.append('..')


class TestStorjEnv(unittest.TestCase):
    def setUp(self):
        options_path = path.join(path.dirname(path.realpath(__file__)), 'options.yml')
        with open(options_path, 'r') as options_file:
            self.options = yaml.load(options_file.read())

        self.env = StorjEnv(**self.options)

    def tearDown(self):
        self.env.destroy()

    def get_bucket_id(self, name):
        buckets = self.env.list_buckets()
        return next(bucket['id'] for bucket in buckets if bucket['name'] == name)


class TestGetInfo(TestStorjEnv):
    def test_get_info(self):
        results = []

        def callback(error_, info_):
            results.append(error_)
            results.append(info_)

        self.env.get_info(callback)
        error, info = results
        self.assertEqual(error, None)
        self.assertEqual(info['host'], self.options['bridge_options']['host'])
        self.assertEqual(info['info']['title'], 'Storj Bridge')


class TestCreateDestroy(TestStorjEnv):
    def test_create_bucket_with_callback(self):
        bucket_name = 'python_libstorj-test'
        results = []

        def callback(error_, bucket_):
            results.append(error_)
            results.append(bucket_)

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

        def callback(error_):
            results.append(error_)

        self.env.delete_bucket(bucket_name, callback)
        error = results[0]
        self.assertEqual(error, None)

    def test_delete_bucket_without_callback(self):
        bucket_name = self.get_bucket_id('python_libstorj-test2')

        self.env.delete_bucket(bucket_name)


class TestListBuckets(TestStorjEnv):
    def setUp(self):
        super(TestListBuckets, self).setUp()
        self.bucket = self.env.create_bucket('python_libstorj-test3')

    def tearDown(self):
        self.env.delete_bucket(self.bucket['id'])
        super(TestListBuckets, self).tearDown()

    def test_list_buckets_with_callback(self):
        bucket_name = 'python_libstorj-test3'
        results = {
            'buckets': [],
            'error': ''
        }

        def callback(error, buckets_):
            results['error'] = error
            for i, bucket in enumerate(buckets_):
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


class TestListFiles(TestStorjEnv):
    def setUp(self):
        super(TestListFiles, self).setUp()
        file_path = path.join(path.dirname(path.realpath(__file__)), 'test.data')
        self.bucket = self.env.create_bucket('python_libstorj-test4')
        upload_file_command = 'storj upload-file %s %s' % (self.bucket['id'], file_path)
        # NB: `stdout=subprocess.PIPE` prevents subprocess
        #     stdout from printing during unittest
        subprocess.call(upload_file_command.split(), stdout=subprocess.PIPE)

    def tearDown(self):
        # TODO: remove file as soon as it's implemented
        self.env.delete_bucket(self.bucket['id'])
        super(TestListFiles, self).tearDown()

    def test_list_files_without_callback(self):
        files = self.env.list_files(self.bucket['id'])
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0]['filename'], 'test.data')
