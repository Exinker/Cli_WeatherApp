import os
import sys

# ENV
try:
    filedir = os.path.split(__file__)[0]
    filepath = os.path.join(filedir, '.env')
    with open(file=filepath, mode='r') as file:
        for line in file.readlines():
            key, value = line.split('=')

            os.environ[key] = value
except FileNotFoundError:
    print('Failed to open .env file')
    sys.exit(1)

# APP
DEBUG = False

APPLICATIONNAME = 'CLI Weather App'
APPLICATIONVERSION = '0.0.01 (beta)'

# OPENWEATHERMAP
OPENWEATHERMAP_API_KEY = os.environ['OPENWEATHERMAP_API_KEY']
