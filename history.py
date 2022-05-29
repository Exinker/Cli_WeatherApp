from datetime import datetime
from typing import NamedTuple

from exceptions import SaveWeatherError
from printer import format_weather
from weather_service import Weather


class HistoryRecord(NamedTuple):
    datetime: str
    weather: str


class Storage:
    '''Interface for any storage'''
    def save(self, record: HistoryRecord) -> None:
        raise NotImplementedError


class PlainTextStorage(Storage):
    def __init__(self, filename: str) -> None:
        self._filename = filename

    def save(self, record: HistoryRecord) -> None:
        message = f'{record.datetime}: {record.weather}\n\n'

        try:
            with open(self._filename, mode='a') as file:
                file.write(message)
        except Exception:
            raise SaveWeatherError


def save_history(weather: Weather, storage: Storage) -> None:
    '''Save weather to storage'''
    
    record = HistoryRecord(
        datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        weather=format_weather(weather),
    )

    storage.save(record)


if __name__ == '__main__':
    from location_service import get_location, WhereAmILocationService
    from weather_service import get_weather, OpenWeatherMapWeatherService
    
    location = get_location(
        service=WhereAmILocationService()
    )

    weather = get_weather(
        location=location,
        service=OpenWeatherMapWeatherService(),
    )
    print(weather)

    save_history(
        weather=weather,
        storage=PlainTextStorage(filename='history.txt')
    )
