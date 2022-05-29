from weather_service import Weather


def format_weather(weather: Weather) -> str:
        return '\n'.join([
        f'{weather.city}, temperature: {weather.temperature:.2f}°C, description: {weather.description}',
        f'sunrise: {weather.sunrise}',
        f'sunset: {weather.sunset}',
    ])


def print_weather(weather: Weather) -> None:
    print(format_weather(weather))
