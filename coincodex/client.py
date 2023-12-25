from sys import exception
from requests import Request, Session
import json

from exceptions import (
    CoincodexAPIBadRequestException,
    CoincodexAPIException,
    CoincodexAPIForbiddenException,
    CoincodexAPIInternalServerErrorException,
    CoincodexAPINotFoundException,
    CoincodexAPIPaymentRequiredException,
    CoincodexAPITooManyRequestsException,
    CoincodexRequestException,
)


class Client():
    """CoinCodex client"""
    _API_FREE_URL = "https://coincodex.com/api"
    _API_PRO_URL = None
    _HEADERS: dict = {"Accept": "application/json", "User-Agent": "coincodex/python"}

    def __init__(self, requests_params=None, api_key=None):
        self.session = self._init_session(api_key=api_key)
        self._base_url = self._get_base_url(api_key=api_key)
        self._requests_params = requests_params

    def _init_session(self, api_key=None):
        session = Session()
        session.headers.update(
            {**self._HEADERS, "Authorization": api_key} if api_key else self._HEADERS
        )
        return session

    def _get_base_url(self, api_key=None):
        return self._API_PRO_URL if api_key else self._API_FREE_URL

    def _request(self, method, uri, force_params=False, **kwargs):
        kwargs["timeout"] = 10

        data = kwargs.get("data", None)
        if data and isinstance(data, dict):
            kwargs["data"] = data

        # if get request assign data array to params value for requests lib
        if data and (method == "get" or force_params):
            kwargs["params"] = kwargs["data"]
            del kwargs["data"]

        response = getattr(self.session, method)(uri, **kwargs)

        return self._handle_response(response)

    def _create_api_uri(self, path):
        return f"{self._base_url}/{path}"

    def _request_api(self, method, path, **kwargs):
        uri = self._create_api_uri(path)
        return self._request(method, uri, **kwargs)

    def _handle_response(self, response):
        if response.status_code == 400:
            raise CoincodexAPIBadRequestException(response)
        if response.status_code == 402:
            raise CoincodexAPIPaymentRequiredException(response)
        if response.status_code == 403:
            raise CoincodexAPIForbiddenException(response)
        if response.status_code == 404:
            raise CoincodexAPINotFoundException(response)
        if response.status_code == 429:
            raise CoincodexAPITooManyRequestsException(response)
        if response.status_code == 500:
            raise CoincodexAPIInternalServerErrorException(response)
        if not str(response.status_code).startswith("2"):
            raise CoincodexAPIException(response)
        try:
            return response.json()
        except ValueError:
            raise CoincodexRequestException(
                f"Invalid Response: {response.text}"
                )

    def _get(self, path, **kwargs):
        return self._request_api("get", path, **kwargs)

    def get_coin_history(self, symbol, start_date, end_date, samples):
        """Returns historic price data for a single coin.

        Parameters:
            symbol: our unique internal id for the coin,
            start_date: YYYY-MM-DD format of start date in range,
            end_date: YYYY-MM-DD format of end date in range
            samples: how many samples (approximately) must be returned for each coin

        Returns:
            Object: [our unique internal id for the coin]: Array:
        Array:
            0: timestamp
            1: coin price in usd
            2: 24hr volume in usd
        """

        return self._get(f"coincodex/get_coin_history/{symbol}/{start_date}/{end_date}/{samples}")

    def get_coin(self, symbol):
        """Returns all properties for the coin needet to display the coin details page

        Args:
            symbol (_type_): our unique internal id for the coin

        Returns:
            description:       html short description
            ico_price:         coin start price in usd
            price_high_24_usd: highest price in the last 24 hours in usd
            price_low_24_usd:  lowest price in the last 24 hours in usd
            release_date:      YYYY-MM-DD or null of the coins release date
            social: Object:
                [key]: url
            today_open:        today's open price in usd
            website:           url
            whitepaper:        url
        """
        return self._get(f"coincodex/get_coin/{symbol}")
