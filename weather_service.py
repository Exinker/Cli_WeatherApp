import json
import ssl
from urllib.request import urlopen
from urllib.error import URLError
from datetime import datetime
from http.client import HTTPResponse
from typing import NamedTuple

from exceptions import GetWeatherError
from location_service import Location
from settings import OPENWEATHERMAP_API_KEY


class Weather(NamedTuple):
    temperature: float
    description: str  # FIXME: change to Enum
    sunrise: str
    sunset: str
    city: str

    def __repr__(self) -> str:
        return f'{self.city}, temperature: {self.temperature:.2f}°C'


class WeatherService:
    'Interface for any weather service'

    def get(self, longitude: float, latitude:float) -> Weather:
        raise NotImplementedError


class OpenWeatherMapWeatherService(WeatherService):

    def get(self, longitude: float, latitude:float) -> Weather:
        units = 'metric'
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units={units}&appid={OPENWEATHERMAP_API_KEY}'
        context = ssl._create_unverified_context()

        try:
            response = urlopen(url, context=context)
        except URLError:
            raise GetWeatherError
        if response.status != 200:
            raise GetWeatherError

        try:
            weather = self._parse_response(response)
        except Exception:
            raise GetWeatherError

        return weather

    def _parse_response(self, response: HTTPResponse) -> Weather:
        data = json.loads(response.read().decode('utf-8'))

        weather = Weather(
            temperature=data['main']['temp'],
            description=data['weather'][0]['description'],
            sunrise=self._parse_time(data['sys']['sunrise']),
            sunset=self._parse_time(data['sys']['sunset']),
            city=data['name'],
        )

        return weather

    def _parse_time(self, time: int) -> str:
        return datetime.fromtimestamp(time).strftime('%H:%M:%S')


def get_weather(location: Location, service: WeatherService) -> Weather:
    '''Return current weather at location.'''

    weather = service.get(
        longitude=location.longitude,
        latitude=location.latitude,
    )

    return weather


if __name__ == '__main__':
    from location_service import get_location, WhereAmILocationService
    
    location = get_location(
        service=WhereAmILocationService()
    )
    print(location)

    weather = get_weather(
        location=location,
        service=OpenWeatherMapWeatherService(),
    )
    print(weather)
