"""Internal module to help with normalizing cloud args.

This module (and all function/classes within this module) should be
considered internal, and *not* a public API.
"""
from abc import abstractmethod, ABCMeta


def make_cloud_args_creator(name, credentials, endpoint=None):
    """Factory function for :class:`CloudArgsCreator` objects.

    Parameters
    ----------
    name : str
        Args creator name.

    credentials : client.credentials.Credentials
        Client credentials object.

    endpoint : client.endpoint.Endpoint
        Endpoint object.

    Returns
    -------
    cloud_args_creator : CloudArgsCreator
    """
    args_creators = {
        'minio': MinioArgsCreator,
        'S3FileSystem': S3FilesystemArgsCreator
    }
    return args_creators[name](credentials, endpoint)


class CloudArgsCreator(metaclass=ABCMeta):
    """Base abstract class for cloud args creator.

    Derived classes are not meant to be constructed
    directly. Instead, instances of derived classes are constructed and
    returned from :meth:`make_args_creator`.
    """

    def __init__(self, credentials, endpoint=None):
        self._credentials = credentials
        self._endpoint = endpoint

    @abstractmethod
    def create_args(self):
        pass

    def _split_host(self):
        protocol, endpoint = self._endpoint.host.split('://')
        return protocol, endpoint

    def _is_secure(self):
        protocol, _ = self._split_host()
        if protocol == 'https':
            return True
        elif protocol == 'http':
            return False
        else:
            raise ValueError(f'Invalid protocol: {protocol}')


class MinioArgsCreator(CloudArgsCreator):
    def __init__(self, credentials, endpoint=None):
        super().__init__(credentials, endpoint)

    def create_args(self):
        if hasattr(self._credentials, 's3_endpoint'):
            endpoint = self._credentials.s3_endpoint
        else:
            _, endpoint = self._split_host()
        return {
            "endpoint": endpoint,
            "access_key": self._credentials.access_key,
            "secret_key": self._credentials.secret_key,
            "secure": self._is_secure()
        }


class S3FilesystemArgsCreator(CloudArgsCreator):
    def __init__(self, credentials, endpoint=None):
        super().__init__(credentials, endpoint)

    def create_args(self):
        return {
            "endpoint_url": self._endpoint.host,
            "aws_access_key_id": self._credentials.access_key,
            "aws_secret_access_key": self._credentials.secret_key,
            "verify": False
        }
