Python wrapper for the Fridgegrow 2.0 API, ses [https://www.plantalytix.com/] for more details on the product.

# Usage
`
from pyfridgegrow import FridgegrowApi

api = FridgegrowApi(username='your_username',password='your_password')
login = api.login() # get Login object containing user_id and user_token
device_list = api.get_device_list() # get list of devices
`
