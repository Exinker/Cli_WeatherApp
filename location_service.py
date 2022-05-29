import json
import os
import urllib.request
from http.client import HTTPResponse
import subprocess
from typing import NamedTuple

from exceptions import GetLocationError


class Location(NamedTuple):
    longitude: float
    latitude: float

    def __repr__(self) -> str:
        return f'longitude: {self.longitude:.2f}, latitude: {self.latitude:.2f}'


class LocationService:
    '''Interface for any location service'''

    def get(self) -> Location:
        raise NotImplementedError


class WhereAmILocationService(LocationService):
    '''get current location using whereami utility'''

    def get(self) -> Location:

        filedir = os.path.split(__file__)[0]
        filepath = os.path.join(filedir, 'utils', 'whereami')
        response = subprocess.run(
            filepath,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',
        )
        if response.returncode != 0:
            raise GetLocationError()

        location = self._parse_response(response)

        return location

    def _parse_response(self, response: subprocess.CompletedProcess) -> Location:

        longitude, latitude = None, None
        for spam in response.stdout.strip().split('\n'):
            key, value = spam.split(': ')

            try:
                if key == 'Longitude':
                    longitude = float(value)
                if key == 'Latitude':
                    latitude = float(value)
            except ValueError:
                raise GetLocationError

        if latitude is None or longitude is None:
            raise GetLocationError

        return Location(longitude, latitude)


class IpInfoLocationService(LocationService):
    '''get current location using ipinfo.io website'''

    def get(self) -> Location:

        response = urllib.request.urlopen('http://ipinfo.io/')
        if response.status != 200:
            raise GetLocationError

        location = self._parse_response(response)

        return location

    def _parse_response(self, response: HTTPResponse) -> Location:

        data = json.loads(response.read())

        try:
            latitude, longitude = map(float, data['loc'].split(','))
        except Exception:
            raise GetLocationError

        return Location(longitude, latitude)


def get_location(service: LocationService) -> Location:
    '''Return current location.'''

    location = service.get()

    return location


if __name__ == '__main__':
    location = get_location(
        IpInfoLocationService()
    )
    print(location)
