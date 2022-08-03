import asyncio

import marshmallow
from aiohttp import TCPConnector, BasicAuth
from abstract_client import AbstractInteractionClient
from params_schema import ParamsSchema


class Client(AbstractInteractionClient):
    CONNECTOR = TCPConnector(ssl=False)  # dev config
    REQUEST_TIMEOUT = float(5 * 60)
    CONNECT_TIMEOUT = float(30)

    SERVICE = 'CloudPayments'
    BASE_URL = 'https://api.cloudpayments.ru/'
    REQUEST_RETRY_TIMEOUTS = (0.1, 0.2, 0.4)

    _session = None

    def __init__(self, public_id, secret_key):
        self.public_id = public_id
        self.secret_key = secret_key
        self._headers = {'Content-Type': 'application/json'}
        super().__init__()

    def _get_auth(self):
        auth = BasicAuth(login=self.public_id, password=self.secret_key)
        return auth

    async def _payment_request_handler(self, endpoint, params, method='POST'):
        auth = self._get_auth()
        url = self.endpoint_url(endpoint)
        if method == 'POST':
            response = await self.post('', url=url, headers=self._headers, json=params, auth=auth)
            return response

    @staticmethod
    def _is_valid_data(schema: marshmallow.Schema, params: dict):
        return False if schema.validate(params) else True

    @staticmethod
    def _load_params(schema: marshmallow.Schema, params: dict):
        return schema.load(params)

    async def _make_cryptogram_payment(self, **kwargs):
        endpoint = 'payments/cards/charge'
        params_schema = ParamsSchema()
        if self._is_valid_data(params_schema, kwargs):
            params = self._load_params(params_schema, kwargs)
            await self._payment_request_handler(endpoint, params)

    def make_cryptogram_payment(self, **kwargs):
        loop = asyncio.get_event_loop()
        task = asyncio.Task(self._make_cryptogram_payment(**kwargs))
        loop.run_until_complete(task)


foo = Client('123', '123')
foo.make_cryptogram_payment(
    amount=1.0,
    ip_address='127.0.0.1',
    card_cryptogram_packet='666',
    json_data='json_data4',
    culture_name='culture!'
)

