from fastmcp import FastMCP
from lithops import Storage
from typing import Optional

mcp = FastMCP("lithops-storage")
storage = None
cloud_objects = []


@mcp.tool()
def lithops_storage(args: dict):
    """
    Name --> lithops_storage
    Description -->
        An Storage object is used by partitioner and other components to access underlying
        storage backend without exposing the implementation details.
    Parameters -->
        config
        backend
        storage_config
    Example -->
        {
            "config":{
                "lithops":{
                    "storage": "redis,
                },
                "redis":{
                    "host" : "localhost",
                    "port":6379
                }
            },
            "backend":"redis"
        }
    """
    global storage
    storage = Storage(**args)


@mcp.tool()
def lithops_create_bucket(args: dict):
    """
    Name --> lithops_create_bucket
    Description --> Creates a bucket if not exists.
    Parameters --> bucket(str) - Name of the bucket
    Example -->
        args = {
            bucket="pyrun-mcp-testing"
        }
    """
    storage.create_bucket(**args)


@mcp.tool()
def lithops_delete_cloudobject(index: int):
    """
    Name --> lithops_delete_cloudobject
    Description --> Delete a CloudObject from storage.
    Parameters -->
        cloudobject (CloudObject) - CloudObject instance (Index of the list cloud_objects you want to delete)
        This deletes form the list too
    Example -->
        index=0
    """
    storage.delete_cloudobject(cloud_objects.pop(index))


@mcp.tool()
def lithops_delete_cloudobjects(start: int, end: int):
    """
    Name --> lithops_delete_cloudobjects
    Description --> Delete multiple CloudObjects from storage.
    Parameters -->
        cloudobjects (List[CloudObject]) - List of CloudObject instances (Indexes of the list cloud_objects[start:end])
        This deletes form the list too
    Example -->
        start=0,end=2
    """
    storage.delete_cloudobjects(cloud_objects[start:end])
    del cloud_objects[start:end]


@mcp.tool()
def lithops_delete_object(args: dict):
    """
    Name --> lithops_delete_object
    Description --> Removes object from the storage backend.
    Parameters -->
        bucket (str) - Name of the bucket
        key (str) - Key of the object
    Example -->
        args={
            "bucket":"pyrun-mcp-testing",
            "key":"test.txt"
        }
    """
    storage.delete_object(**args)


@mcp.tool()
def lithops_delete_objects(args: dict):
    """
    Name --> lithops_delete_objects
    Description --> This operation enables you to delete multiple objects from a bucket using a single HTTP request.
    If you know the object keys that you want to delete, then this operation provides a suitable alternative to sending individual delete requests, reducing per-request overhead.
    Parameters -->
        bucket (str) - Name of the bucket
        key_list (List[str]) - List of object keys
    Example -->
        arg={
            "bucket":"pyrun-mcp-testing",
            "key_list" :["test.txt", "test2.txt"]
        }
    """
    storage.delete_objects(**args)


# @mcp.tool()
# def lithops_get_client():
#     """
#         Name --> lithops_get_client
#         Description --> Retrieves the underlying storage client.
#         Returns --> Storage backend client
#         Return Type --> object
#     """
#     return storage.get_client()


@mcp.tool()
def lithops_get_cloudobject(index: int, stream: bool):
    """
    Name --> lithops_get_cloudobject
    Description --> Get a CloudObject's content from storage.
    Parameters -->
        cloudobject (CloudObject) - CloudObject instance (Index of the cloudObject which is saved in the list cloud_objects)
        stream (bool | None) - Get the object data or a file-like object
    Returns --> Cloud object content
    Return Type --> str | bytes | TextIO | BinaryIO
    Example -->
        index=0,stream=false
    """
    return storage.get_cloudobject(cloud_objects[index], stream=stream)


@mcp.tool()
def lithops_get_object(args: dict):
    """
    Name --> lithops_get_object
    Description --> Retrieves objects from the storage backend.
    Parameters -->
        bucket (str) - Name of the bucket
        key (str) - Key of the object
        stream (bool | None) - Get the object data or a file-like object
        extra_get_args (Dict | None) - Extra get arguments to be passed to the underlying backend implementation (dict). For example, to specify the byte-range to read: extra_get_args={'Range': 'bytes=0-100'}.
    Returns --> Object, as a binary array or as a file-like stream if parameter stream is enabled
    Return Type --> str | bytes | TextIO | BinaryIO
    Example -->
        args={
            "bucket":"pyrun-mcp-testing",
            "key":"test.txt"
        }
    """
    return storage.get_object(**args)


@mcp.tool()
def lithops_get_storage_config():
    """
    Name --> lithops_get_storage_config
    Description --> Retrieves the configuration of this storage handler.
    Returns --> Storage configuration
    Return Type --> Dict
    """
    return storage.get_storage_config()


@mcp.tool()
def lithops_head_bucket(args: dict):
    """
    Name --> lithops_head_bucket
    Description -->
        This operation is useful to determine if a bucket exists and you have permission to access it.
        The operation returns a 200 OK if the bucket exists and you have permission to access it.
        Otherwise, the operation might return responses such as 404 Not Found and 403 Forbidden.
    Parameters --> bucket (str) - Name of the bucket
    Returns --> Request response
    Return Type --> Dict
    Example -->
        args={
            bucket="pyrun-mcp-testing"
        }
    """
    return storage.head_bucket(**args)


@mcp.tool()
def lithops_head_object(args: dict):
    """
    Name -->
    Description -->
        The HEAD operation retrieves metadata from an object without returning the object itself.
        This operation is useful if you're only interested in an object's metadata.
    Parameters -->
        bucket (str) - Name of the bucket
        key (str) - Key of the object
    Returns --> Object metadata
    Return Type --> Dict
    Example -->
        args={
            bucket="pyrun-mcp-testing",
            key="test.txt"
        }
    """
    return storage.head_object(**args)


@mcp.tool()
def lithops_list_keys(args):
    """
    Name --> lithops_list_keys
    Description -->
        Similar to list_objects(), it returns all of the object keys in a bucket.
        For each object, the list contains only the names of the objects (keys).
    Parameters -->
        bucket - Name of the bucket
        prefix - Key prefix for filtering
    Returns --> List of object keys
    Return Type --> List[str]
    Example -->
        args={
            "bucket":"pyrun-mcp-testing",
            "prefix":"alpha"
        }
    """
    return storage.list_keys(**args)


@mcp.tool()
def lithops_list_objects(args: dict):
    """
    Name --> lithops_list_objects
    Description -->
        Returns all of the object keys in a bucket.
        For each object, the list contains the name of the object (key) and the size.
    Parameters -->
        bucket (str) - Name of the bucket
        prefix (str | None) - Key prefix for filtering
        match_pattern (str | None) -
    Returns --> List of tuples containing the object key and size in bytes
    Return Type --> List[Tuple[str, int]]
    Example -->
        args={
            "bucket":"pyrun-mcp-testing",
            "prefix":"alpha"
        }
    """
    return storage.list_objects(**args)


@mcp.tool()
def lithops_put_cloudobject(args: dict, aux: dict):
    """
    Name --> lithops_put_cloudobject
    Description --> Put a CloudObject into storage.
    Parameters -->
        args --> {
            bucket (str) - Name of the bucket (Must be always)
            key (str) - Key of the object (Must be always)
            bucket (str | bytes) - Only if aux['file'] = false
        }

        aux --> {
            file (Bool) --> If you want to upload a file (Must be always)
            text_io (Bool) --> If you want to upload a file with text_io else is BinaryIO (Must be only if file  = true)
            path_to_file (str) --> Absolut path to the file (Must be only if file  = true)
        }
    Returns -->
        CloudObject instance which will be saved in a gloabal list in the last position
    Return Type --> CloudObject
    Example -->
        args ={
            "bucket":"pyrun-mcp-testing",
            "key":"test3.txt",
            "body":"Hello World"
        }
        aux={
            "file":false
        }
        ------------
        args ={
            "bucket":"pyrun-mcp-testing",
            "key":"hello2.csv"
        }
        aux={
            "file":true,
            "text_io":false,
            "path_to_file":"hello2.csv"
        }
    """
    if aux["file"]:
        if aux["text_io"]:
            with open(aux["path_to_file"], "r", encoding="utf-8") as fl:
                args["body"] = fl.read()
                val = storage.put_cloudobject(**args)
        else:
            with open(aux["path_to_file"], "rb") as fl:
                args["body"] = fl.read()
                val = storage.put_cloudobject(**args)
    else:
        val = storage.put_cloudobject(**args)

    cloud_objects.append(val)
    return val


@mcp.tool()
def lithops_put_object(args: dict, aux: dict):
    """
    Name --> lithops_put_object
    Description --> Adds an object to a bucket of the storage backend.
    Parameters -->
        args --> {
            bucket (str) - Name of the bucket (Must be always)
            key (str) - Key of the object (Must be always)
            body (str | bytes) - Only if aux['file'] = false
        }

        aux --> {
            file (Bool) --> If you want to upload a file (Must be always)
            text_io (Bool) --> If you want to upload a file with text_io else is BinaryIO (Must be only if file  = true)
            path_to_file (str) --> Absolut path to the file (Must be only if file  = true)
        }
    Example -->
        args ={
            "bucket":"pyrun-mcp-testing",
            "key":"test4.txt",
            "body":"Hello World"
        }
        aux={
            "file":false
        }
        ----------------------
        args ={
            "bucket":"pyrun-mcp-testing",
            "key":"hello3.csv"
        }
        aux={
            "file":true,
            "text_io":false,
            "path_to_file":"hello3.csv"
        }
    """

    if aux["file"]:
        if aux["text_io"]:
            with open(aux["path_to_file"], "r", encoding="utf-8") as fl:
                args["body"] = fl.read()
                storage.put_object(**args)
        else:
            with open(aux["path_to_file"], "rb") as fl:
                args["body"] = fl.read()
                storage.put_object(**args)
    else:
        storage.put_object(**args)


@mcp.tool()
def lithops_upload_file(args: dict):
    """
    Name --> lithops_upload_file
    Description --> Upload a file to a bucket of the storage backend. (Multipart upload)
    Parameters -->
        file_name (str) - Name of the file to upload
        bucket (str) - Name of the bucket
        key (str | None) - Key of the object
        extra_args (Dict | None) - Extra get arguments to be passed to the underlying backend implementation (dict).
        config (Any | None) - The transfer configuration to be used when performing the transfer (boto3.s3.transfer.TransferConfig).
    Return Type --> str | bytes | TextIO | BinaryIO
    """
    return storage.upload_file(**args)


@mcp.tool()
def lithops_download_file(args: dict):
    """
    Name --> lithops_download_file
    Description --> Download a file from the storage backend. (Multipart download)
    Parameters -->
        bucket (str) - Name of the bucket
        key (str) - Key of the object
        file_name (str | None) - Name of the file to save the object data
        extra_args (Dict | None) - Extra get arguments to be passed to the underlying backend implementation (dict).
        config (Any | None) - The transfer configuration to be used when performing the transfer (boto3.s3.transfer.TransferConfig).
    Returns --> Object, as a binary array or as a file-like stream if parameter stream is enabled
    Return Type --> str | bytes | TextIO | BinaryIO
    """
    return storage.download_file(**args)


if __name__ == "__main__":
    mcp.run(transport="stdio")
