from unittest import TestCase
from unittest.mock import MagicMock
from pyfridgegrow.fridgegrow_api import FridgegrowApi
from pyfridgegrow.models import *


class TestFridgegrowApi(TestCase):
    def setUp(self) -> None:
        self.fgapi = FridgegrowApi()
        
        self.fgapi._login = Login("x","y","z")
        self.fgapi._login.user_token = UserToken("a","b")
        self.fgapi._rest_adapter = MagicMock()

    def _login_and_device_mocks(self):
        self.fgapi.login = MagicMock(return_value=Login("x","y","z"))
        self.fgapi._login.user_token = MagicMock(UserToken("a","b"))
        self.fgapi.get_device_list  = MagicMock(return_value=[Device("k","g","b",{})])
    
    def test_login_returns_one_login_obj(self):
        # Arrange
        self.fgapi._rest_adapter.post.return_value = Result(200, headers={}, data={
            "user": {
                "username": "everest@criminalz.de",
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

        # Act
        login = self.fgapi.login()

        # Assert
        self.assertIsInstance(login, Login)

    def test_get_device_list_returns_device_list(self):
        # Arrange
        self.fgapi._rest_adapter.get.return_value = Result(200, headers={}, data=[
            {
                "_id": "123",
                "device_id": "456",
                "device_type": "fridge",
                "configuration": "config"
            }
        ])

        # Act
        device_list = self.fgapi.get_device_list()

        # Assert
        self.assertIsInstance(device_list, list)
        self.assertIsInstance(device_list[0], Device)
    
    def test_get_temperature(self):
        # Arrange
        self._login_and_device_mocks()
        self.fgapi._rest_adapter.get.return_value = Result(200, headers={}, data={
                "value": 123.5
            })

        # Act
        temperature = self.fgapi.get_temperature()

        # Assert
        self.assertIsInstance(temperature, Temperature)
    
    def test_get_co2(self):
        # Arrange
        self._login_and_device_mocks()
        self.fgapi._rest_adapter.get.return_value = Result(200, headers={}, data={
                "value": 123.5
            })

        # Act
        co2 = self.fgapi.get_co2()
        
        # Assert
        self.assertIsInstance(co2, Co2)
    
    def test_get_humidity(self):
        # Arrange
        self._login_and_device_mocks()
        self.fgapi._rest_adapter.get.return_value = Result(200, headers={}, data={
                "value": 123.5
            })

        # Act
        humidity = self.fgapi.get_humidity()       
        
        # Assert
        self.assertIsInstance(humidity, Humidity)
    
    def test_get_data_latest(self):
        # Arrange
        self._login_and_device_mocks()
        self.fgapi._rest_adapter.get.return_value = Result(200, headers={}, data={
                "value": 123.5
            })

        # Act
        humidity = self.fgapi.get_data_latest(DataType.HUMIDITY)       
        co2 = self.fgapi.get_data_latest(DataType.CO2) 
        temperature = self.fgapi.get_data_latest(DataType.TEMPERATURE) 

        # Assert
        self.assertIsInstance(humidity, Humidity)
        self.assertIsInstance(co2, Co2)
        self.assertIsInstance(temperature, Temperature)
    
    def test_get_data_latest(self):
        # Arrange
        self._login_and_device_mocks()
        self.fgapi._rest_adapter.get.return_value = Result(200, headers={}, data=[{
                "result": "mean",
                "table": 0,
                "_start": "2024-12-14T22:14:29.609608177Z",
                "_stop": "2024-12-15T22:14:29.609608177Z",
                "_time": "2024-12-14T22:14:40Z",
                "_value": 117.3,
                "_field": "co2",
                "_measurement": "status",
                "device_id": "x",
                "user_id": "y"
            }])

        # Act
        humidity_dsi = self.fgapi.get_data_series(data_type=DataType.HUMIDITY)       
        co2_dsi = self.fgapi.get_data_series(data_type=DataType.CO2) 
        temperature_dsi = self.fgapi.get_data_series(data_type=DataType.TEMPERATURE) 

        # Assert
        self.assertIsInstance(humidity_dsi, list)
        self.assertIsInstance(humidity_dsi[0], DataSeriesItem)
        self.assertIsInstance(co2_dsi, list)
        self.assertIsInstance(co2_dsi[0], DataSeriesItem)
        self.assertIsInstance(temperature_dsi, list)
        self.assertIsInstance(temperature_dsi[0], DataSeriesItem)

    
