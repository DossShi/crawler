# Import MinIO library.
import time
import datetime
from minio import Minio
from minio.error import ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists
from minio import Minio, CopyConditions

# Initialize minioClient with an endpoint and access/secret keys.
minioClient = Minio('47.101.168.84:9000',
                    access_key='minioadmin',
                    secret_key='minioadmin',
                    secure=False)


# Make a bucket with the make_bucket API call.
# try:
#        minioClient.make_bucket("test2")
# except BucketAlreadyOwnedByYou as err:
#        pass
# except BucketAlreadyExists as err:
#        pass
# except ResponseError as err:
#        raise


# List all buckets
# buckets = minioClient.list_buckets()
# for bucket in buckets:
#     print(bucket.name, '\t', bucket.creation_date)


# Put an object 'test1.jpg' with contents from '32412191465.jpg'.
try:
       minioClient.fput_object('test', 'testdir/dirSon/2.txt'.encode('utf-8'), '/tmp/app.log')
except ResponseError as err:
       print(err)


# List all object paths in bucket that begin with my-prefixname.
# objects = minioClient.list_objects('test', prefix='',
#                               recursive=True)
# for obj in objects:
#     print(obj.bucket_name, obj.object_name, obj.last_modified,
#           obj.etag, obj.size, obj.content_type)


# List all object paths in bucket that begin with my-prefixname using
# V2 listing API.
# objects = minioClient.list_objects_v2('test', prefix='',
#                               recursive=True)
# for obj in objects:
#     print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
#           obj.etag, obj.size, obj.content_type)


# Remove a bucket
# This operation will only work if your bucket is empty.
# try:
#     minioClient.remove_bucket('test2')
# except ResponseError as err:
#     print(err)


# List all object paths in bucket that begin with my-prefixname.
# uploads = minioClient.list_incomplete_uploads('test',
#                                          prefix='图片',
#                                          recursive=True)
# for obj in uploads:
#     print(obj.bucket_name, obj.object_name, obj.upload_id, obj.size)


# Get a full object
# try:
#     minioClient.fget_object('test', '图片.jpg', '/tmp/1.jpg')
# except ResponseError as err:
#     print(err)


# Fetch stats on your object.
# try:
#     print(minioClient.stat_object('test', '图片.jpg'))
# except ResponseError as err:
#     print(err)


# # client.trace_on(sys.stderr)
# copy_conditions = CopyConditions()
# # Set modified condition, copy object modified since 2014 April.
# t = (2020, 3, 25, 0, 0, 0, 0, 0, 0)
# mod_since = datetime.utcfromtimestamp(time.mktime(t))
# copy_conditions.set_modified_since(mod_since)
#
# # Set unmodified condition, copy object unmodified since 2014 April.
# # copy_conditions.set_unmodified_since(mod_since)
#
# # Set matching ETag condition, copy object which matches the following ETag.
# # copy_conditions.set_match_etag("31624deb84149d2f8ef9c385918b653a")
#
# # Set matching ETag except condition, copy object which does not match the
# # following ETag.
# # copy_conditions.set_match_etag_except("31624deb84149d2f8ef9c385918b653a")
#
# try:
#     copy_result = minioClient.copy_object("test", "a.txt",
#                                      "/test2/a.txt",
#                                      copy_conditions)
#     print(copy_result)
# except ResponseError as err:
#     print(err)


# # presigned get object URL for object name, expires in 7 days.
# try:
#     print(minioClient.presigned_get_object('test', '2.txt'))
# # Response error is still possible since internally presigned does get
# # bucket location.
# except ResponseError as err:
#     print(err)


# presigned Put object URL for an object name, expires in 3 days.
try:
    print(minioClient.presigned_put_object('test',
                                      '2.txt',
                                      datetime.timedelta(days=3)))
# Response error is still possible since internally presigned does get
# bucket location.
except ResponseError as err:
    print(err)