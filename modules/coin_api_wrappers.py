"""Module implementing api wrappers to fetch the cryptocurrencies data."""

import os

from abc import ABC, abstractmethod

import requests

_REQUEST_DEFAULT_TIMEOUT = 20
_BINANCE_BASE_URL = "https://api.binance.com"


class ApiWrapper(ABC):
    """Abstract base class for api wrappers."""

    def __init__(self, base_url: str):
        self._base_url = base_url

    @abstractmethod
    def test_connection(self) -> bool:
        """Verify connection."""
        pass

    @abstractmethod
    def get_symbol_kline_price(self) -> float:
        """Get price of a coin."""
        pass


class BinanceWrapper(ApiWrapper):
    """Class implementing Binance REST API wrapper.
    Documentation: https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md#exchange-information
    """

    _PATH_PING = "/api/v3/ping"
    _PATH_KLINES = "/api/v3/klines"

    def __init__(self, base_url: str, api_key: str = os.getenv("BINANCE_API_KEY", "")):
        super().__init__(base_url)
        self.__api_header = {"X-MBX-APIKEY": api_key}

    def test_connection(self, path: str = _PATH_PING) -> bool:
        """Tests connection to API under provided path.

        Args:
            path: url suffix to use for testing the connectivity.

        Returns:
            True if connection established, False otherwise.
        """
        try:
            response = requests.get(
                self._base_url + path, headers=self.__api_header, params={}, timeout=_REQUEST_DEFAULT_TIMEOUT
            )
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the '{response.request}' request: {e}")
        
        return response.status_code == 200

    def get_symbol_kline_price(
        self, symbol: str, params: dict[str, str] = {"interval": "1s"}, path: str = _PATH_KLINES
    ) -> float:
        """Fetches the Kline/Candlestick data for provided symbol.

        Args:
            symbol: pair to check.
            params: additional parameters of the api call such as interval.
            path:   url suffix to get the data.

        Returns:
            Closing price of selected symbol.
        """
        # Append symbol to call parameters
        params = {"symbol": symbol} | params

        try:
            response = requests.get(
                self._base_url + path, headers=self.__api_header, params=params, timeout=_REQUEST_DEFAULT_TIMEOUT
            )
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the '{response.request}' request: {e}")

        # Take value from first kline, closing price is a 5th element
        return response.json()[0][4]

    def get_change(self, symbol: str, interval: str, duration: int, path: str = _PATH_KLINES) -> float:
        """Calculates the selected % in price of selected symbol based on the Kline/Candlestick data.

        Args:
            symbol:     pair to check.
            interval:   Which interval of Candlestick to use. Should be reasonably connnected with limit.
                        Only Binance Api supported values can be used.
            duration:   How many candlesticks within sepcified interval use to calculate the change.
                        1min interval with duration=5 will result in 5 minutes % change.

        Returns:
            % Change within specified values.
        """
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": duration,
        }
        try:
            response = requests.get(
                self._base_url + path, headers=self.__api_header, params=params, timeout=_REQUEST_DEFAULT_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()

            # Extract closing prices (5th element of kline)
            close_prices = [float(kline[4]) for kline in data]

            # Get the latest and first within the limit prices
            latest_price = close_prices[-1]
            first_price = close_prices[0]

        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the '{response.request}' request: {e}")

        # Calculate percentage change
        return ((latest_price - first_price) / first_price) * 100


wrapper = BinanceWrapper(_BINANCE_BASE_URL)

print(wrapper.test_connection())
print(wrapper.get_symbol_kline_price("BTCUSDT"))
print(wrapper.get_change("BTCUSDT", "1h", 24))
