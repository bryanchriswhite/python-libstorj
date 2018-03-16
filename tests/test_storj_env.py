import sys, subprocess, yaml, re, unittest
from os import path
from datetime import datetime
from lib.storj_env import StorjEnv
sys.path.append('..')


class UtilityTestCase(unittest.TestCase):
    BAD_HOST_ERROR = Exception("Couldn't resolve host name")

    def assertExceptionEqual(self, error1, error2):
        self.assertEqual(type(error1), type(error2))
        self.assertEqual(error1.message, error2.message)

    def assertBadHostError(self, error):
        self.assertExceptionEqual(error, self.BAD_HOST_ERROR)

    def assertRaisesWithMessage(self, msg, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as error:
            return self.assertEqual(error.message, msg)

        self.fail('Function call did not raise an exception!')

    def assertRaisesWithBadHost(self, func, *args, **kwargs):
        message = self.BAD_HOST_ERROR.message
        self.assertRaisesWithMessage(message, func, *args, **kwargs)


class TestStorjEnv(UtilityTestCase):
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


class TestStorjEnvBadHost(UtilityTestCase):
    def setUp(self):
        options_path = path.join(path.dirname(path.realpath(__file__)), 'options.yml')
        with open(options_path, 'r') as options_file:
            self.options = yaml.load(options_file.read())
            self.options['bridge_options']['host'] = 'nonexistant.example'

        self.env = StorjEnv(**self.options)

    def tearDown(self):
        self.env.destroy()


class TestGetInfoSuccess(TestStorjEnv):
    def test_get_info_without_callback_success(self):
        info = self.env.get_info()
        self.assertIsInstance(info, dict)
        self.assertEqual(info['info']['title'], 'Storj Bridge')

    def test_get_info_with_callback_success(self):
        results = []

        def callback(error, info):
            results.append(error)
            results.append(info)

        self.env.get_info(callback)
        error, info = results
        self.assertEqual(error, None)
        self.assertIsInstance(info, dict)
        self.assertEqual(info['info']['title'], 'Storj Bridge')


class TestGetInfoFailure(TestStorjEnvBadHost):
    def test_get_info_without_callback_failure(self):
        self.assertRaisesWithBadHost(self.env.get_info)

    def test_get_info_with_callback_failure(self):
        def callback():
            return None

        self.assertRaisesWithBadHost(self.env.get_info, callback)


class TestCreateDeleteSuccess(TestStorjEnv):
    def test_create_bucket_without_callback_success(self):
        bucket_name = 'python_libstorj-test2'

        bucket = self.env.create_bucket(bucket_name)
        self.assertEqual(bucket['name'], bucket_name)

    def test_create_bucket_with_callback_success(self):
        bucket_name = 'python_libstorj-test'
        results = []

        def callback(error_, bucket_):
            results.append(error_)
            results.append(bucket_)

        self.env.create_bucket(bucket_name, callback)
        error, bucket = results
        self.assertEqual(error, None)
        self.assertEqual(bucket['name'], bucket_name)

    def test_delete_bucket_without_callback_success(self):
        bucket_name = self.get_bucket_id('python_libstorj-test2')

        self.env.delete_bucket(bucket_name)

    def test_delete_bucket_with_callback_success(self):
        bucket_name = self.get_bucket_id('python_libstorj-test')
        results = []

        def callback(error):
            results.append(error)

        self.env.delete_bucket(bucket_name, callback)
        try:
            error = results[0]
            self.assertIsNone(error)

            # NB: asserts no bucket with name: `bucket_name` exists
            bucket_iterator = (b for b in self.env.list_buckets() if b['name'] == bucket_name)
            self.assertRaises(StopIteration, next, bucket_iterator)
        except IndexError:
            self.fail('Callback not called!')


class TestCreateBucketFailure(TestStorjEnvBadHost):
    def test_create_bucket_without_callback_failure(self):
        bucket_name = 'python_libstorj-test2'
        self.assertRaisesWithBadHost(self.env.create_bucket, bucket_name)

    def test_create_bucket_with_callback_failure(self):
        bucket_name = 'python_libstorj-test'
        results = {}

        def callback(error, bucket):
            results['bucket'] = bucket
            results['error'] = error

        self.assertRaisesWithBadHost(self.env.create_bucket, bucket_name, callback)
        try:
            error, bucket = [results[k] for k in ('error', 'bucket')]

            self.assertIsNone(bucket)
            self.assertBadHostError(error)
        except KeyError:
            self.fail('Callback not called!')


class TestDeleteBucketFailure(TestStorjEnvBadHost):
    def test_delete_bucket_without_callback_failure(self):
        bucket_name = 'python_libstorj-test2'
        self.assertRaisesWithBadHost(self.env.delete_bucket, bucket_name)

    def test_delete_bucket_with_callback_failure(self):
        bucket_name = 'python_libstorj-test'
        results = []

        def callback(error):
            results.append(error)

        self.assertRaisesWithBadHost(self.env.delete_bucket, bucket_name, callback)
        try:
            error = results[0]

            self.assertBadHostError(error)
        except KeyError:
            self.fail('Callback not called!')


class TestListBucketsSuccess(TestStorjEnv):
    def setUp(self):
        super(TestListBucketsSuccess, self).setUp()
        self.bucket = self.env.create_bucket('python_libstorj-test3')

    def tearDown(self):
        self.env.delete_bucket(self.bucket['id'])
        super(TestListBucketsSuccess, self).tearDown()

    def test_list_buckets_without_callback(self):
        bucket_name = 'python_libstorj-test3'

        buckets = self.env.list_buckets()
        self.assertEqual(len(buckets), 1)
        self.assertIsInstance(buckets[0]['created'], datetime)
        self.assertEqual(buckets[0]['name'], bucket_name)

    def test_list_buckets_with_callback(self):
        bucket_name = 'python_libstorj-test3'
        results = {
            'buckets': [],
            'error': ''
        }

        def callback(error_, buckets_):
            results['error'] = error_
            for i, bucket in enumerate(buckets_):
                results['buckets'].append(bucket)

        self.env.list_buckets(callback)
        buckets, error = [results[key] for key in ('buckets', 'error')]
        self.assertEqual(error, None)
        self.assertEqual(len(buckets), 1)
        self.assertIsInstance(buckets[0]['created'], datetime)
        self.assertEqual(buckets[0]['name'], bucket_name)


class TestListBucketsFailure(TestStorjEnvBadHost):
    def test_list_buckets_without_callback_failure(self):
        self.assertRaisesWithBadHost(self.env.list_buckets)

    def test_list_buckets_with_callback_failure(self):
        results = {}

        def callback(error, buckets):
            results['error'] = error
            results['buckets'] = buckets

        self.assertRaisesWithBadHost(self.env.list_buckets, callback)
        try:
            buckets, error = [results[key] for key in ('buckets', 'error')]
            self.assertEqual(buckets, [])
            self.assertBadHostError(error)
        except KeyError:
            self.fail('Callback not called!')


class TestListFilesSuccess(TestStorjEnv):
    def setUp(self):
        self.file_name = 'test.data'
        super(TestListFilesSuccess, self).setUp()
        file_path = path.join(path.dirname(path.realpath(__file__)), 'upload.data')
        self.bucket = self.env.create_bucket('python_libstorj-test4')
        upload_file_command = 'storj upload-file %s %s' % (self.bucket['id'], file_path)
        # NB: `stdout=subprocess.PIPE` prevents subprocess
        #     stdout from printing during unittest
        subprocess.call(upload_file_command.split(), stdout=subprocess.PIPE)

    def tearDown(self):
        # TODO: remove file as soon as it's implemented
        self.env.delete_bucket(self.bucket['id'])
        super(TestListFilesSuccess, self).tearDown()

    def test_list_files_without_callback_success(self):
        files = self.env.list_files(self.bucket['id'])
        self.assertEqual(len(files), 1)
        # TODO: uncomment when file naming works
        # self.assertEqual(files[0]['filename'], self.file_name)

    def test_list_files_with_callback_success(self):
        results = []

        def callback(error_, files_):
            results.append(error_)
            results.append(files_)

        self.env.list_files(self.bucket['id'], callback)
        error, files = results
        self.assertEqual(error, None)
        self.assertEqual(len(files), 1)
        # TODO: uncomment when file naming works
        # self.assertEqual(files[0]['filename'], self.file_name)


class TestListFilesFailure(TestStorjEnvBadHost):
    def setUp(self):
        super(TestListFilesFailure, self).setUp()
        self.bucket = {'id': 'python_libstorj-test-4_id'}

    def test_list_files_without_callback_failure(self):
        self.assertRaisesWithBadHost(self.env.list_files, self.bucket['id'])

    def test_list_files_with_callback_failure(self):
        results = {}

        def callback(error, files):
            results['error'] = error
            results['files'] = files

        self.assertRaisesWithBadHost(self.env.list_files, self.bucket['id'], callback)
        try:
            error, files = [results[k] for k in ('error', 'files')]
            self.assertBadHostError(error)
            self.assertEqual(files, [])
        except KeyError:
            self.fail('Callback not called!')


# class TestStoreFile(TestStorjEnv):
#     def setUp(self):
#         super(TestStoreFile, self).setUp()
#         # buckets = self.env.list_buckets()
#         # self.bucket = buckets[0]
#         self.bucket = self.env.create_bucket('python_libstorj-test5')
#
#     def tearDown(self):
#        self.bucket = self.env.delete_bucket(self.bucket['id'])
#        super(TestStoreFile, self).tearDown()
#
#     def test_store_file_without_callback(self):
#         # self.assertEqual(True, False)
#         # return self.skipTest('wip')
#         file_name = 'test.data'
#         file_path = path.join(path.dirname(path.realpath(__file__)), 'upload.data')
#         upload_options = {
#             'file_name': file_name
#         }
#
#         # file_ = self.env.store_file('6bb4051cac924f0264aca224',
#         upload_state = self.env.store_file(self.bucket['id'],
#                                     file_path,
#                                     options=upload_options)
#         # file_id_regex = re.compile('\w+', re.I)
#         print(upload_state)
#         self.assertNotEqual(upload_state, None)
#         # self.assertNotEqual(file_, None)
#         # self.assertRegexpMatches(file_['id'], file_id_regex)
