from unittest import TestCase
from unittest.mock import MagicMock
from pyfridgegrow.fridgegrow_api import FridgegrowApi
from pyfridgegrow.models import Login, Result


class TestTheCatApi(TestCase):
    def setUp(self) -> None:
        self.fgapi = FridgegrowApi()
        self.fgapi._rest_adapter = MagicMock()

    def test_login_returns_one_login_obj(self):
        self.fgapi._rest_adapter.post.return_value = Result(200, headers={}, data={
            "user": {
                "username": "everestgenetics@gmail.com",
                "user_id": "1232",
                "is_admin": "false"
            },
            "userToken": {
                "expiresIn": 60,
                "token": "uToken"
            },
            "refreshToken": {
                "expiresIn": 300,
                "token": "rToken"
            }
        })
        login = self.fgapi.login()
        self.assertIsInstance(login, Login)
      
'''
    def test_get_clowder_of_kitties_returns_list_of_image_short(self):
        kitty_amt = 2
        self.catapi._rest_adapter.get.return_value = Result(200, headers={}, data=[{'id': 1, 'url': "someurl.com"},
                                                                                   {'id': 2, 'url': "someurl.com"},
                                                                                   {'id': 3, 'url': "someurl.com"}])
        kitty_list = self.catapi.get_clowder_of_kitties(amt=kitty_amt)
        self.assertIsInstance(kitty_list, list)
        self.assertTrue(len(kitty_list), kitty_amt)
        self.assertIsInstance(kitty_list[0], ImageShort)

    def test_get_kitties_paged_returns_iterator_of_image_short(self):
        self.catapi._rest_adapter.get.side_effect = [Result(200, headers={"pagination-count": 1, "pagination-page": 0},
                                                                 data=[{'id': 1, 'url': "someurl.com"},
                                                                       {'id': 2, 'url': "someurl.com"},
                                                                       {'id': 3, 'url': "someurl.com"}]),
                                                     Result(200, headers={"pagination-count": 1, "pagination-page": 1},
                                                                 data=[])
                                                     ]
        kitty_iterator = self.catapi.get_kitties_paged()
        kitty1 = next(kitty_iterator)
        kitty2 = next(kitty_iterator)
        kitty3 = next(kitty_iterator)
        self.assertIsInstance(kitty3, ImageShort)
        with self.assertRaises(StopIteration):
            kitty4 = next(kitty_iterator)
'''

