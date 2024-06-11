import requests

class RequestUtil:
    def __init__(self, base_url='http://127.0.0.1:5000'):
        self.base_url = base_url

    def add_vehicle(self, license_plate):
        data = {
            'license_plate': license_plate
        }
        url = f'{self.base_url}/vehicles'
        response = requests.post(url, json=data)
        return response.json()

    def add_entry_exit(self, license_plate, entry_exit):
        data = {
            'license_plate': license_plate,
            'entry_exit': entry_exit
        }
        url = f'{self.base_url}/entries'
        response = requests.post(url, json=data)
        return response.json()

    def get_vehicles_inside(self):
        url = f'{self.base_url}/vehicles/inside'
        response = requests.get(url)
        return response.json()

    def get_vehicles_outside(self):
        url = f'{self.base_url}/vehicles/outside'
        response = requests.get(url)
        return response.json()

    def get_vehicle_activity(self, license_plate):
        url = f'{self.base_url}/vehicles/activity/{license_plate}'
        response = requests.get(url)
        return response.json()

# Example usage
if __name__ == '__main__':
    request_util = RequestUtil()

    # Add a new vehicle
    print(request_util.add_vehicle('XYZ456'))

    # Add an entry or exit event
    print(request_util.add_entry_exit('XYZ456', 'entry'))

    # Fetch all vehicles inside and outside
    print(request_util.get_vehicles_inside())
    print(request_util.get_vehicles_outside())

    # Fetch activity for a specific vehicle
    print(request_util.get_vehicle_activity('XYZ456'))
