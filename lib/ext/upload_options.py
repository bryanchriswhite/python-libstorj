from os import path
import python_libstorj as pystorj


class UploadOptions(pystorj.storj_upload_opts_t):

    def __init__(self, bucket_id=None, file_path=None, options=None):
        super(UploadOptions, self).__init__()

        if options is not None:
            bucket_id_, \
            file_path_, \
            file_name, \
            index = [options.get(k, None) for k in ('bucket_id',
                                                    'file_path',
                                                    'file_name',
                                                    'index')]
        else:
            bucket_id_, file_path_, file_name, index = None, None, None, None

        # NB: default to options
        bucket_id = bucket_id_ or bucket_id
        file_path = file_path_ or file_path

        if file_path is None or not path.isfile(file_path):
            raise IOError('Path "%s" is not a file.' % file_path)

        if file_name is None:
            file_name = path.dirname(file_path)

        self.prepare_frame_limit = 1
        self.push_frame_limit = 64
        self.push_shard_limit = 64
        self.rs = True
        self.index = index if (type(index) is str and len(index) == 64) else None
        self.bucket_id = bucket_id
        self.file_name = file_name
        self.fd = pystorj.fopen(file_path, 'r')
