import logging
from typing import Dict, List #, Callable
from pyfridgegrow.rest_adapter import RestAdapter
#from pyfridgegrow.exceptions import FridgegrowApiException
from pyfridgegrow.models import Login, Device


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
        result = self._rest_adapter.get(endpoint=f'/device',headers=headers)
        device_list= [Device(**device) for device in result.data]
        return device_list
        
    
        
        
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