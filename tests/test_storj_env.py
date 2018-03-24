import sys, subprocess, yaml, re, unittest, time
from os import path
from datetime import datetime
from lib.storj_env import StorjEnv
from lib.ext import python_libstorj as pystorj
sys.path.append('..')
import ipdb


class UtilityTestCase(unittest.TestCase):
    BAD_HOST_ERROR = Exception("Couldn't resolve host name")
    STATUS_CODE_7000 = Exception("Unable to decode hex string: status code 7000")

    def assertExceptionEqual(self, error1, error2):
        self.assertEqual(type(error1), type(error2))
        self.assertEqual(error1.message, error2.message)

    def assertBadHostError(self, error):
        self.assertExceptionEqual(error, self.BAD_HOST_ERROR)

    def assertStatus7000Error(self, error):
        self.assertExceptionEqual(error, self.STATUS_CODE_7000)

    def assertRaisesWithMessage(self, msg, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as error:
            return self.assertEqual(error.message, msg)

        self.fail('Function call did not raise an exception!')

    def assertRaisesWithBadHost(self, func, *args, **kwargs):
        message = self.BAD_HOST_ERROR.message
        self.assertRaisesWithMessage(message, func, *args, **kwargs)

    def assertRaisesWithStatus7000(self, func, *args, **kwargs):
        message = self.STATUS_CODE_7000.message
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

    def get_file_iterator_match(self, bucket_id, file_name):
        files = self.env.list_files(bucket_id)
        return (file for file in files if re.search(r'%s$' % file_name, file['filename']) is not None)

    def get_file_id(self, bucket_id, file_name):
        return next(file['id'] for file in self.get_file_iterator_match(bucket_id, file_name))

    @staticmethod
    def upload_test_data(bucket_id):
        file_path = path.join(path.dirname(path.realpath(__file__)), 'upload.data')
        upload_file_command = 'storj upload-file %s %s' % (bucket_id, file_path)
        # NB: `stdout=subprocess.PIPE` prevents subprocess
        #     stdout from printing during unittest
        subprocess.call(upload_file_command.split(), stdout=subprocess.PIPE)


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


class TestCreateDeleteBucketSuccess(TestStorjEnv):
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
        # NB: asserts no bucket with name: `bucket_name` exists
        bucket_iterator = (b for b in self.env.list_buckets() if b['name'] == bucket_name)
        self.assertRaises(StopIteration, next, bucket_iterator)

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


class TestGetBucketIdSuccess(TestStorjEnv):
    def setUp(self):
        super(TestGetBucketIdSuccess, self).setUp()
        self.bucket_name = 'python_libstorj-test3'
        self.bucket = self.env.create_bucket(self.bucket_name)

    def tearDown(self):
        self.env.delete_bucket(self.bucket['id'])
        super(TestGetBucketIdSuccess, self).tearDown()

    def test_get_bucket_id_without_callback(self):
        bucket = self.env.get_bucket_id(self.bucket_name)
        self.assertEqual(bucket['id'], self.bucket['id'])

    def test_get_bucket_id_with_callback(self):
        results = {}

        def callback(error, bucket):
            results['error'] = error
            results['bucket'] = bucket

        self.env.get_bucket_id(self.bucket_name, callback)
        bucket, error = [results[key] for key in ('bucket', 'error')]
        self.assertEqual(error, None)
        self.assertEqual(bucket['id'], self.bucket['id'])


class TestGetBucketIdFailure(TestStorjEnvBadHost):
    def test_get_bucket_id_without_callback_failure(self):
        bucket_name = 'python_libstorj-test2'
        self.assertRaisesWithBadHost(self.env.get_bucket_id, bucket_name)

    def test_get_bucket_id_with_callback_failure(self):
        bucket_name = 'python_libstorj-test'
        results = {}

        def callback(error, bucket):
            results['error'] = error
            results['bucket'] = bucket

        self.assertRaisesWithBadHost(self.env.get_bucket_id, bucket_name, callback)
        try:
            error = results['error']

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


# class TestDeleteFileSuccess(TestStorjEnv):
#     def setUp(self):
#         super(TestDeleteFileSuccess, self).setUp()
#         bucket_name = 'python_libstorj-test_bucket7'
#         # self.file_name = 'test.data'
#         self.file_name = 'upload.data'
#         self.bucket = self.env.create_bucket(bucket_name)
#         self.upload_test_data(self.bucket['id'])
#         self.file_id = self.get_file_id(self.bucket['id'], 'upload.data')
#
#     def tearDown(self):
#         self.env.delete_bucket(self.bucket['id'])
#         super(TestDeleteFileSuccess, self).tearDown()
#
#     def test_delete_file_without_callback_success(self):
#         self.env.delete_file(self.bucket['id'], self.file_id)
#         # NB: asserts no file with name: `bucket_name` exists
#         file_iterator = self.get_file_iterator_match(self.bucket['id'], self.file_name)
#         self.assertRaises(StopIteration, next, file_iterator)
#
#     def test_delete_file_with_callback_success(self):
#         results = []
#
#         def callback(error):
#             results.append(error)
#
#         self.env.delete_file(self.bucket['id'], self.file_id, callback)
#         try:
#             error = results[0]
#             self.assertIsNone(error)
#
#             # NB: asserts no bucket with name: `bucket_name` exists
#             # file_iterator = (f for f in self.env.list_files(self.bucket['id']) if re.search(r'%s' % self.file_name, f['filename']) is not None)
#             file_iterator = self.get_file_iterator_match(self.bucket['id'], self.file_name)
#             self.assertRaises(StopIteration, next, file_iterator)
#         except IndexError:
#             self.fail('Callback not called!')


class TestDeleteFileFailure(TestStorjEnvBadHost):
    def test_delete_file_without_callback_failure(self):
        bucket_name = 'python_libstorj-test_bucket2'
        file_name = 'python_libstorj-test_file2'
        self.assertRaisesWithBadHost(self.env.delete_file, bucket_name, file_name)

    def test_delete_file_with_callback_failure(self):
        bucket_name = 'python_libstorj-test_bucket'
        file_name = 'python_libstorj-test_file'
        results = []

        def callback(error):
            results.append(error)

        self.assertRaisesWithBadHost(self.env.delete_file, bucket_name, file_name, callback)
        try:
            error = results[0]

            self.assertBadHostError(error)
        except KeyError:
            self.fail('Callback not called!')


class TestListFilesSuccess(TestStorjEnv):
    def setUp(self):
        super(TestListFilesSuccess, self).setUp()
        self.file_name = 'test.data'
        self.bucket = self.env.create_bucket('python_libstorj-test4')
        file_path = path.join(path.dirname(path.realpath(__file__)), 'upload.data')
        upload_options = {
            'file_name': self.file_name
        }
        self.file = self.env.store_file(self.bucket['id'], file_path, options=upload_options)

    def tearDown(self):
        self.env.delete_file(self.bucket['id'], self.file['id'])
        self.env.delete_bucket(self.bucket['id'])
        super(TestListFilesSuccess, self).tearDown()

    def test_list_files_without_callback_success(self):
        files = self.env.list_files(self.bucket['id'])
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0]['filename'], self.file_name)

    def test_list_files_with_callback_success(self):
        results = {}

        def callback(error, files):
            results['error'] = error
            results['files'] = files

        self.env.list_files(self.bucket['id'], callback)
        try:
            error, files = [results[k] for k in ('error', 'files')]
            self.assertEqual(error, None)
            self.assertEqual(len(files), 1)
            self.assertEqual(files[0]['filename'], self.file_name)
        except KeyError:
            self.fail('Callback not called!')


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


class TestStoreFileSuccess(TestStorjEnv):
    def setUp(self):
        super(TestStoreFileSuccess, self).setUp()
        self.file_id_regex = re.compile('\w+', re.I)
        self.file_name = 'test.data'
        self.file_path = path.join(path.dirname(path.realpath(__file__)), 'upload.data')
        self.upload_options = {
            'file_name': self.file_name
        }
        self.bucket = self.env.create_bucket('python_libstorj-test5')

    def tearDown(self):
       self.env.delete_bucket(self.bucket['id'])
       super(TestStoreFileSuccess, self).tearDown()

    def test_store_file_without_callback_success(self):
        file_ = self.env.store_file(self.bucket['id'],
                                    self.file_path,
                                    options=self.upload_options)
        self.assertNotEqual(file_, None)
        self.assertRegexpMatches(file_['filename'], self.file_name)
        self.assertRegexpMatches(file_['id'], self.file_id_regex)

    def test_store_file_with_callback_success(self):
        results = {}

        # TODO: ensure progress_callback is called as well
        def callback(error, file_):
            results['error'] = error
            results['file'] = file_

        self.env.store_file(self.bucket['id'],
                            self.file_path,
                            options=self.upload_options,
                            finished_callback=callback)

        try:
            error, file_ = [results[k] for k in ('error', 'file')]
            self.assertEqual(error, None)
            self.assertNotEqual(file_, None)
            self.assertEqual(file_['filename'], self.file_name)
            self.assertRegexpMatches(file_['id'], self.file_id_regex)
        except(KeyError):
            self.fail('Callback not called!')


class TestStoreFileFailure(TestStorjEnvBadHost):
    def setUp(self):
        super(TestStoreFileFailure, self).setUp()
        self.file_name = 'test.data'
        self.file_path = path.join(path.dirname(path.realpath(__file__)), 'upload.data')
        self.upload_options = {
            'file_name': self.file_name
        }
        self.bucket = {'id': 'python_libstorj-test-4_id'}

    def test_store_file_without_callback_failure(self):
        self.assertRaisesWithStatus7000(self.env.store_file,
                                     self.bucket['id'],
                                     self.file_path,
                                     options=self.upload_options)

    def test_store_file_with_callback_failure(self):
        results = {
            'error': None,
            'file': None
        }

        def callback(error, file_):
            results['error'] = error
            results['file'] = file_

        self.assertRaisesWithStatus7000(self.env.store_file,
                                     self.bucket['id'],
                                     self.file_path,
                                     options=self.upload_options,
                                     finished_callback=callback)
        try:
            error, file_ = [results[k] for k in ('error', 'file')]
            self.assertStatus7000Error(error)
            self.assertEqual(file_, None)
        except KeyError:
            self.fail('Callback not called!')
