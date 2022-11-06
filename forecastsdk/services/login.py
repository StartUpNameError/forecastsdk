from .base import BaseService


class LoginService(BaseService):
    def __init__(self, endpoint, loader, access_token, credentials):
        super().__init__(endpoint, loader, access_token, credentials)

    def login(self):
        credentials = self.get_credentials()
        api_params = {
            'username': credentials.access_key,
            'password': credentials.secret_key,
        }

        # Notice ``annon`` param is set to True.
        return self._make_api_call(data=api_params, annon=True)
