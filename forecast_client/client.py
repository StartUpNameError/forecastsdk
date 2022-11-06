from .endpoint import ClientEndpointBridge, EndpointCreator
from .exceptions import UnknownServiceError
from .services import (
    TrainService,
    LoginService,
    WriterService,
    PredictService
)

SERVICES = {
    'writer': WriterService,
    'train': TrainService,
    'predict': PredictService,
    'login': LoginService
}


class ClientCreator:
    """Service client creator.

    Parameters
    ----------
    endpoint_resolver : botocore.session.EndpointResolver
        Resolver for endpoint data.
    """

    def __init__(self, loader, endpoint_resolver):
        self._loader = loader
        self._endpoint_resolver = endpoint_resolver

    def create_client(self, service_name, endpoint_name, is_secure=True,
                      endpoint_url=None, access_token=None, credentials=None):
        endpoint_bridge = ClientEndpointBridge(self._endpoint_resolver)
        cls = self._get_client_class(service_name)
        client_args = self._get_client_args(
            service_name, endpoint_name, endpoint_bridge, is_secure,
            endpoint_url, access_token, credentials
        )
        service_client = cls(**client_args)
        return service_client

    def _get_client_class(self, service_name):
        if service_name not in SERVICES:
            raise UnknownServiceError(name=service_name)
        return SERVICES[service_name]

    def _get_client_args(self, service_name, endpoint_name, endpoint_bridge,
                         is_secure, endpoint_url, access_token, credentials):
        args_creator = ClientArgsCreator(self._loader)
        return args_creator.get_client_args(
            service_name, endpoint_name, endpoint_bridge, is_secure,
            endpoint_url, access_token, credentials)


class ClientArgsCreator:
    """Service client args creator.

    Since services share a common interface, a consistent procedure for
    obtaining their constructor arguments can be achieved.
    """

    def __init__(self, loader):
        self._loader = loader

    def get_client_args(self, service_name, endpoint_name, endpoint_bridge,
                        is_secure, endpoint_url, access_token, credentials):
        """Obtains client args.

        Parameters
        ----------
        service_name : str
            Name of the service. To list available services call method
            :meth:`get_available_services`.

        endpoint_name : str
            Endpoint for the passed service.

        endpoint_bridge : botocore.client.EndpointBridge
            EndpointBridge object for resolving the endpoint.

        is_secure : bool
            Whether or not to use SSL.  By default, SSL is used.
            Note that not all services support non-ssl connections.

        endpoint_url : str
            The complete URL to use for the constructed
            client.

        access_token : str
            Access token for authenticating.

        Returns
        -------
        args : dict
        """
        # Resolve endpoint data.
        resolved = self._resolve_endpoint(
            service_name, endpoint_name, endpoint_url, is_secure,
            endpoint_bridge)

        # Create endpoint object.
        endpoint = self._get_endpoint(resolved)

        return {
            'endpoint': endpoint,
            'loader': self._loader,
            'access_token': access_token,
            'credentials': credentials
        }

    def _get_endpoint(self, endpoint_config):
        endpoint_creator = EndpointCreator()
        service_name = endpoint_config['service_name']
        endpoint = endpoint_creator.create_endpoint(
            service_name,
            endpoint_url=endpoint_config['endpoint_url']
        )
        return endpoint

    def _resolve_endpoint(self, service_name, endpoint_name, endpoint_url,
                          is_secure, endpoint_bridge):
        return endpoint_bridge.resolve(
            service_name=service_name,
            endpoint_name=endpoint_name,
            endpoint_url=endpoint_url,
            is_secure=is_secure)
