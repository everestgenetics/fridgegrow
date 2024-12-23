import logging
from typing import Dict, List #, Callable
from pyfridgegrow.rest_adapter import RestAdapter
from pyfridgegrow.exceptions import FridgegrowApiException
from pyfridgegrow.models import *
from enum import Enum

class FridgegrowApi:
    def __init__(self, hostname: str = 'api.plantalytix-app.com', username: str = '', password: str = '', ssl_verify: bool = True,
                 logger: logging.Logger = None):
        self._rest_adapter = RestAdapter(hostname, username, password, ssl_verify, logger)

    def _get_auth_header(self) -> Dict:
        return {"Authorization":f"Bearer {self._login.user_token.token}"} 
    
    def login(self) -> Login:
        data = {"username":self._rest_adapter.username, "password":self._rest_adapter.password}
        result = self._rest_adapter.post(endpoint='/login',data=data)
        self._login =  Login(**result.data) 
        return self._login
    
    def get_device_list(self) -> List[Device]:
        headers = self._get_auth_header()
        result = self._rest_adapter.get(endpoint='/device',headers=headers)
        device_list= [Device(**device) for device in result.data]
        return device_list

    def _get_data_latest_path(self, device_num: int=0) -> str:
        device_list = self.get_device_list(device_num)
        device_id = device_list[device_num].device_id
        return f'data/latest/{device_id}'
    
    def _get_data_series_path(self, device_num: int=0) -> str:
        device_list = self.get_device_list(device_num)
        device_id = device_list[device_num].device_id
        return f'data/series/{device_id}'
    
    def get_temperature(self, device_num: int=0) -> Temperature:
        data_latest_path = self._get_data_latest_path(device_num)
        headers = self._get_auth_header()
        result = self._rest_adapter.get(endpoint=f'{data_latest_path}/temperature',headers=headers)
        temperature = Temperature(**result.data)
        return temperature
    
    def get_co2(self, device_num: int=0) -> Co2:
        data_latest_path = self._get_data_latest_path(device_num)
        headers = self._get_auth_header()
        result = self._rest_adapter.get(endpoint=f'{data_latest_path}/co2',headers=headers)
        co2 = Co2(**result.data)
        return co2
    
    def get_humidity(self, device_num: int=0) -> Humidity:
        data_latest_path = self._get_data_latest_path(device_num)
        headers = self._get_auth_header()
        result = self._rest_adapter.get(endpoint=f'{data_latest_path}/humidity',headers=headers)
        humidity = Humidity(**result.data)
        return humidity
    
    def get_data_latest(self, data_type:Enum, device_num: int=0) -> Temperature:
        if not data_type:
            raise FridgegrowApiException (f'Not data_type provided to get latest data')
        data_latest_path = self._get_data_latest_path(device_num)
        headers = self._get_auth_header()
        result = self._rest_adapter.get(endpoint=f'{data_latest_path}/{data_type.name.lower()}',headers=headers)
        match data_type:
            case DataType.TEMPERATURE: 
                return Temperature(**result.data)
            case DataType.CO2: 
                return Co2(**result.data)
            case DataType.HUMIDITY: 
                return Humidity(**result.data)

    def get_data_series(self, from_param: str='-1d', to_param:str ='now()', interval_param:str ='20s', data_type:Enum='', device_num: int=0):
        data_series_path = self._get_data_series_path(device_num)
        headers = self._get_auth_header()
        ep_params = {"from":from_param, "to":to_param, "interval":interval_param}
        result = self._rest_adapter.get(endpoint=f'{data_series_path}/{data_type.name.lower()}',headers=headers,ep_params=ep_params)
        data_series= [DataSeriesItem(**dsi) for dsi in result.data]
        return data_series

        
        
'''
    def get_kitty(self) -> ImageShort:
        return self.get_clowder_of_kitties(amt=1)[0]

    def get_clowder_of_kitties(self, amt: int = 1) -> List[ImageShort]:
        result = self._rest_adapter.get(endpoint=f'/images/search?limit={amt}')
        kitty_img_list = [ImageShort(**datum) for datum in result.data]
        return kitty_img_list

    def fetch_image_data(self, image: ImageShort):
        image.data = self._rest_adapter.fetch_data(url=image.url)

    def _page(self, endpoint: str, model: Callable[..., Model], max_amt: int = 100) -> Iterator[Model]:
        amt_yielded = 0
        curr_page = last_page = 0
        ep_params = {'limit': self._page_size, 'order': 'Desc'}
        while curr_page <= last_page:
            ep_params['page'] = curr_page
            result = self._rest_adapter.get(endpoint=endpoint, ep_params=ep_params)
            last_page = int(result.headers.get('pagination-count', 0))
            curr_page = int(result.headers.get('pagination-page')) + 1
            for datum in result.data:
                yield model(**datum)
                amt_yielded += 1
                if amt_yielded >= max_amt:
                    last_page = 0
                    break

    def get_kitties_paged(self, max_amt: int = 100) -> Iterator[ImageShort]:
        return self._page(endpoint='/images/search', model=ImageShort, max_amt=max_amt)
'''