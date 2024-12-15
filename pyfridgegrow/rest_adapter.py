import requests
import logging
from typing import Dict, List
from json import JSONDecodeError
from pyfridgegrow.exceptions import FridgegrowApiException
from pyfridgegrow.models import Result


class RestAdapter:
    def __init__(self, hostname: str = 'api.plantalytix-app.com', username: str = '', password: str = '', ssl_verify: bool = True, logger: logging.Logger = None):
        """
        Constructor for RestAdapter
        :param hostname: Normally, api.plantalytix-app.com
        :param username: username
        :param password: password
        :param ssl_verify: Normally set to True, but if having SSL/TLS cert validation issues, can turn off with False
        :param logger: (optional) If your app has a logger, pass it in here.
        """
        self._logger = logger or logging.getLogger(__name__)
        self.url = f"https://{hostname}"
        self.username = username
        self.password = password
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def _do(self, http_method: str, endpoint: str, headers: Dict = None, ep_params: Dict = None, data: Dict = None) -> Result:
        """
        Private method for get(), post(), delete(), etc. methods
        :param http_method: GET, POST, DELETE, etc.
        :param endpoint: URL Endpoint as a string
        :param headers: Headers
        :param ep_params: Dictionary of Endpoint parameters (Optional)
        :param data: Dictionary of data to pass to TheCatApi (Optional)
        :return: a Result object
        """
        full_url = self.url + endpoint
        log_line_pre = f"method={http_method}, url={full_url}, params={ep_params}"
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, message={}"))

        # Log HTTP params and perform an HTTP request, catching and re-raising any exceptions
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(method=http_method, url=full_url, verify=self._ssl_verify,
                                        headers=headers, params=ep_params, json=data)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise FridgegrowApiException("Request failed") from e

        # Deserialize JSON output to Python object, or return failed Result on exception
        try:
            data_out = response.json()
        except (ValueError, TypeError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise FridgegrowApiException("Bad JSON in response") from e

        # If status_code in 200-299 range, return success Result with data, otherwise raise exception
        is_success = 299 >= response.status_code >= 200     # 200 to 299 is OK
        log_line = log_line_post.format(is_success, response.status_code, response.reason)
        if is_success:
            self._logger.debug(msg=log_line)
            return Result(response.status_code, headers=response.headers, message=response.reason, data=data_out)
        self._logger.error(msg=log_line)
        raise FridgegrowApiException(f"{response.status_code}: {response.reason}")

    def get(self, endpoint: str, headers: Dict = None, ep_params: Dict = None) -> Result:
        return self._do(http_method='GET', endpoint=endpoint, headers=headers, ep_params=ep_params)

    def post(self, endpoint: str, headers: Dict = None, ep_params: Dict = None, data: Dict = None) -> Result:
        return self._do(http_method='POST', endpoint=endpoint, headers=headers, ep_params=ep_params, data=data)

    def delete(self, endpoint: str, headers: Dict = None, ep_params: Dict = None, data: Dict = None) -> Result:
        return self._do(http_method='DELETE', endpoint=endpoint, headers=headers, ep_params=ep_params, data=data)


    def fetch_data(self, url: str) -> bytes:
        # GET URL; catching, logging, and re-raising any exceptions
        http_method = 'GET'
        try:
            log_line = f"method={http_method}, url={url}"
            self._logger.debug(msg=log_line)
            response = requests.request(method=http_method, url=url, verify=self._ssl_verify)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise FridgegrowApiException(str(e)) from e

        # If status_code in 200-299 range, return byte stream, otherwise raise exception
        is_success = 299 >= response.status_code >= 200
        log_line = f"success={is_success}, status_code={response.status_code}, message={response.reason}"
        self._logger.debug(msg=log_line)
        if not is_success:
            raise FridgegrowApiException(response.reason)
        return response.content