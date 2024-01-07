import requests

API_ENDPOINT = "http://localhost:3001/vehicle_in_out_post"
plate = "99H72345"

plate_json = {'license_plate':plate}

r = requests.post(url=API_ENDPOINT, json=plate_json)