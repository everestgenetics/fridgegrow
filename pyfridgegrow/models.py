    #import os
from typing import List, Dict, TypeVar#, Union
from requests.structures import CaseInsensitiveDict
from enum import Enum
#from pyfridgegrow.exceptions import FridgegrowApiException

Model = TypeVar('Model', covariant=True)


class Result:
    def __init__(self, status_code: int, headers: CaseInsensitiveDict, message: str = '', data: List[Dict] = None):
        """
        Result returned from low-level RestAdapter
        :param status_code: Standard HTTP Status code
        :param message: Human readable result
        :param data: Python List of Dictionaries (or maybe just a single Dictionary on error)
        """
        self.status_code = int(status_code)
        self.headers = headers
        self.message = str(message)
        self.data = data if data else []

class User:
    def __init__(self, username: str, user_id: str, is_admin: str):
        self.username = username
        self.user_id = user_id
        self.is_admin = is_admin

class UserToken:
    def __init__(self, expiresIn: str, token: str):
        self.expiresIn = expiresIn
        self.token = token

class RefreshToken:
    def __init__(self, expiresIn: str, token: str):
        self.expiresIn = expiresIn
        self.token = token

class Login:
    def __init__(self, user: User, userToken: UserToken, refreshToken: RefreshToken):
        self.user = user
        self.user_token = userToken
        self.refresh_token = refreshToken

class Device:
    def __init__(self, _id: str, device_id: str, device_type: str, configuration: Dict):
        self.id = _id
        self.device_id = device_id
        self.device_type = device_type
        self.configuration = configuration

class Co2:
    def __init__(self, value: float):
        self.value = value

class Temperature:
    def __init__(self, value: float):
        self.value = value

class Humidity:
    def __init__(self, value: float):
        self.value = value

class DataType(Enum):
    TEMPERATURE = 1
    CO2 = 2
    HUMIDITY = 3

class DataSeriesItem:
    def __init__(self, result: str, table: int, _start: str, _stop: str, _time: str, _value: float, _field: str, _measurement: str, device_id: str, user_id: str):
        self.result = result
        self.table = table
        self._start = _start
        self._stop = _stop
        self._time = _time
        self._value = _value
        self._field = _field
        self._measurement = _measurement
        self.device_id = device_id
        self.user_id = user_id
'''
class Fact:
    def __init__(self, id: str, text: str, language_code: str, breed_id: str):
        self.id = id
        self.text = text
        self.language_code = language_code
        self.breed_id = breed_id


class Weight:
    def __init__(self, imperial: str, metric: str):
        self.imperial = imperial
        self.metric = metric


class Category:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Breed:
    def __init__(self, weight: Union[Weight, dict], id: str, name: str, country_codes: str, country_code: str,
                 description: str, temperament: str = '', origin: str = '', life_span: str = '', alt_names: str = '',
                 wikipedia_url: str = '', **kwargs) -> None:
        self.weight = Weight(**weight) if isinstance(weight, dict) else weight
        self.id = id
        self.name = name
        self.origin = origin
        self.country_codes = country_codes
        self.country_code = country_code
        self.description = description
        self.temperament = temperament
        self.life_span = life_span
        self.alt_names = alt_names
        self.wikipedia_url = wikipedia_url
        self.__dict__.update(kwargs)


class ImageShort:
    def __init__(self, id: int, url: str, categories: List[Category] = None, breeds: List[Breed] = None, data: bytes = bytes(), **kwargs):
        self.id = id
        self.url = url
        self.categories = [] if not categories else [Category(**c) for c in categories]
        self.breeds = [] if not breeds else [Breed(**b) for b in breeds]
        self.data = data
        self.__dict__.update(kwargs)

    def save_to(self, path: str = './', file_name: str = ''):
        if not self.data:
            raise FridgegrowApiException("No data to save")
        try:
            save_file_name = file_name if file_name else self.url.split('/')[-1]
            save_path = os.path.join(path, save_file_name)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(self.data)
        except Exception as e:
            raise FridgegrowApiException(str(e)) from e


class ImageFull(ImageShort):
    def __init__(self, id: int, url: str, sub_id: int = 0, created_at: str = '', original_filename: str = '',
                 categories: List[Category] = None, breeds: List[Breed] = None, **kwargs):
        super().__init__(id, url, categories, breeds, **kwargs)
        self.sub_id = sub_id
        self.created_at = created_at
        self.original_filename = original_filename
        self.__dict__.update(kwargs)
'''