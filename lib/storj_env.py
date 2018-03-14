import json
from datetime import datetime
from ext import python_libstorj as pystorj
from ext.upload_options import UploadOptions


class StorjEnv():
    def __init__(self,
                 bridge_options,
                 encrypt_options,
                 http_options,
                 log_options):

        options_list = (
            (bridge_options, pystorj.BridgeOptions()),
            (encrypt_options, pystorj.EncryptOptions()),
            (http_options, pystorj.HttpOptions()),
            (log_options, pystorj.LogOptions())
        )

        for option_pair in options_list:
            (options, option_struct) = option_pair
            for key, value in options.viewitems():
                if key == 'pass':
                    # NB: `pass` is a reserved attribute name; swig
                    #     knows this and has changed `pass` to `_pass`
                    key = '_pass'
                setattr(option_struct, key, value)

        options = zip(*options_list)[1]
        self.env = pystorj.init_env(*options)
        self.env.loop = pystorj.set_loop(self.env)

    @staticmethod
    def _error_check(results):
        error, data = None, None

        try:
            if type(results) is list:
                data = results[0]
            elif type(results) is dict:

                try:
                    error = results['error']
                    if error is not None:
                        data = error
                except KeyError:
                    data = results['data']
            else:
                raise Exception('Unknown results structure')

            if type(data) is Exception:
                raise data
            return data
        except IndexError:
            return None

    def destroy(self):
        pystorj.destroy_env(self.env)

    def get_info(self, callback=None):
        results = []

        def handle(error, result):
            # NB: method executes in a separate C thread!
            info = None
            try:
                info = json.loads(result)
                results.append(info)
            finally:
                if error is not None:
                    error = Exception(error)
                    results.append(error)

                if callback is not None:
                    callback(error, info)

        pystorj.get_info(self.env, handle)
        pystorj.run(self.env.loop)
        return self._error_check(results)

    def list_buckets(self, callback=None):
        results = {}

        def handle(error, buckets):
            if buckets is not None:
                for i, bucket in enumerate(buckets):
                    iso8601_format = '%Y-%m-%dT%H:%M:%S.%fZ'
                    created_date = datetime.strptime(bucket['created'], iso8601_format)
                    buckets[i]['created'] = created_date
                results['data'] = buckets

            if error is not None:
                error = Exception(error)
                results['error'] = error

            if callback is not None:
                callback(error, buckets)

        pystorj.list_buckets(self.env, handle)
        pystorj.run(self.env.loop)
        return self._error_check(results)

    def create_bucket(self, name, callback=None):
        results = []

        def handle(error, bucket):
            if bucket is not None:
                results.append(bucket)

            if error is not None:
                error = Exception(error)
                results.append(error)

            if callback is not None:
                callback(error, bucket)

        pystorj.create_bucket(self.env, name, handle)
        pystorj.run(self.env.loop)
        return self._error_check(results)

    def delete_bucket(self, bucket_id, callback=None):
        results = []

        def handle(error):
            if error is not None:
                error = Exception(error)
                results.append(error)

            if callback is not None:
                callback(error)

        pystorj.delete_bucket(self.env, bucket_id, handle)
        pystorj.run(self.env.loop)
        return self._error_check(results)

    def get_bucket_id(self, bucket_name, callback=None):
        results = {}

        def handle(error, bucket):
            if bucket is not None:
                results['data'] = bucket

            if error is not None:
                error = Exception(error)
                results['error'] = error

            if callback is not None:
                callback(error, bucket)

        pystorj.get_bucket_id(self.env, bucket_name, handle)
        pystorj.run(self.env.loop)
        return self._error_check(results)

    def delete_file(self, bucket_id, file_id, callback=None):
        results = []

        def handle(error):
            if error is not None:
                error = Exception(error)
                results.append(error)

            if callback is not None:
                callback(error)

        pystorj.delete_file(self.env, bucket_id, file_id, handle)
        pystorj.run(self.env.loop)
        return self._error_check(results)

    def list_files(self, bucket_id, callback=None):
        results = {}

        def handle(error, files):
            if files is not None:
                for i, file_ in enumerate(files):
                    iso8601_format = '%Y-%m-%dT%H:%M:%S.%fZ'
                    created_date = datetime.strptime(file_['created'], iso8601_format)
                    files[i]['created'] = created_date
                results['data'] = files

            if error is not None:
                error = Exception(error)
                results['error'] = error

            if callback is not None:
                callback(error, files)

        pystorj.list_files(self.env, bucket_id, handle)
        pystorj.run(self.env.loop)
        return self._error_check(results)

    def store_file(self,
                   bucket_id,
                   file_path,
                   options=None,
                   progress_callback=None,
                   finished_callback=None):
        results = []

        def progress_callback_(progress, bytes, total_bytes):
            if progress_callback is not None:
                progress_callback(progress, bytes, total_bytes)

        def finished_callback_(status, file_id):
            # TODO: error handling based on `status`
            results.append(file_id)

            if finished_callback is not None:
                finished_callback(status, file_id)

            # if error is not None:
            #     raise Exception(error)

        upload_options = UploadOptions(bucket_id, file_path, options)
        pystorj.store_file(self.env,
                           upload_options,
                           progress_callback_,
                           finished_callback_)
