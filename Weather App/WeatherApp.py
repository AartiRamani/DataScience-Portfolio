# Author: Aarti Ramani
# Created Date: 11/11/2022
# Purpose: Program to connect to a Webservice to get current weather
# ********************************************************************************************
# Change(s) Made: Version 1.0
# Date of Change: 11/11/2022
# Author: Aarti Ramani
# Change Approved by: N/A
# Date Moved to Production: N/A
# ********************************************************************************************
import requests
import us as geo_us
# import os.path


class GeoCode:
    def __init__(self):
        self.err = 0
        # Commenting below code since I am no longer able to access GitHub. Hardcoding the API Key
        self.apikey = 'dfec42ccbede0b2d309fcf16e4d54cf2'
        # file_path = "API-Key.txt"
        # if not os.path.exists(file_path):
        #     print("Input file unavailable.")
        # else:
        #     try:
        #         with open(file_path, 'r') as file_data:  # using with to handle file closing
        #             # Read every line from file to get the API key
        #             for line in file_data:
        #                 self.apikey = str(line)
        #     except FileNotFoundError as file:
        #         print('Could not locate the API-key file')
        #     except RuntimeError as err:
        #         print('There was an error in getting the API Key')

    # Function to lookup latitude and longitude by zipcode
    def get_geo_data_by_zip(self, zipcode):
        try:
            # URL to lookup by zip code
            geocode_request_url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zipcode}&appid={self.apikey}"
            if self.err == 0:
                response = requests.get(geocode_request_url)
                if response.status_code == 200:  # success response
                    self.err = 0
                    if len(response.json()) > 0:
                        return response.json()
                    else:
                        print('The GEO location API could not retrieve the location. Please retry.')
                elif response.status_code == 404:  # not found
                    self.err = 1
                    print('Not a valid U.S. Zip Code. Please enter a valid zip code.')
                else:
                    self.err = 1
                    print('Unable to retrieve GEO location using entered zip code. The service returned a'
                          ' : ', response.status_code)
        except ConnectionError as connect:
            print('Unable to connect to the GEO API : ', connect)
        except requests.HTTPError as error:
            print('Unable to retrieve GEO location using entered zip code : ', error)
        except requests.exceptions.RequestException as req:
            print('There seems to be a problem with the connection. Connection Error : ', req)
        except RuntimeError as err:
            print('There was an error in getting the geo location data : ', err)

    # Function to lookup latitude and longitude by city and state
    def get_geo_data_by_city(self, user_input_city, user_input_state):
        try:
            # URL to lookup by city and state in USA country
            geocode_request_url = f"http://api.openweathermap.org/geo/1.0/direct?q={user_input_city},{user_input_state},USA&limit={1}&appid={self.apikey}"
            # print(geocode_request_url)
            if self.err == 0:
                response = requests.get(geocode_request_url)
                if response.status_code == 200:  # success response
                    self.err = 0
                    if len(response.json()) > 0:
                        return response.json()
                    else:
                        self.err = 1
                        print('Not a Valid City/State.')
                elif response.status_code == 404:  # not found
                    self.err = 1
                    print('Not a Valid City/State :', response.status_code)
                else:
                    self.err = 1
                    print('Unable to retrieve GEO location using entered City/State name : ', response.status_code)
        except ConnectionError as connect:
            print('Unable to connect to the GEO API : ', connect)
        except requests.HTTPError as error:
            print('Unable to retrieve GEO location using entered City/State name : ', error)
        except requests.exceptions.RequestException as req:
            print('There seems to be a problem with the connection. Connection Error : ', req)
        except RuntimeError as err:
            print('There was an error in getting the geo location data : ', err)

    # Function to lookup weather information from openweathermap
    def open_weather(self, lat, lon, unit):
        try:
            if lat != '' and lon != '':
                # URL to lookup weather information based on lat, lon and unit.
                request_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units={unit}&appid={self.apikey}"
                # print(request_url)
                if self.err == 0:
                    response = requests.get(request_url)
                    if response.status_code == 200:  # success response
                        self.err = 0
                        if len(response.json()) > 0:
                            return response.json()
                        else:
                            print('API was unable to retrieve weather data. Please retry.')
                    elif response.status_code == 404:  # not found
                        self.err = 1
                        print('Weather data not found.')
                    else:
                        self.err = 1
                        print('Unable to retrieve weather information : ', response.status_code)
        except ConnectionError as connect:
            print('Unable to connect to the Open Weather API : ', connect)
        except requests.HTTPError as error:
            print('Unable to retrieve weather information : ', error)
        except requests.exceptions.RequestException as req:
            print('There seems to be a problem with the connection. Connection Error : ', req)
        except RuntimeError as err:
            print('There was an error in getting the weather information : ', err)


# Function to get a US state code based on user input
def get_us_state_cd(state, geo_code):
    try:
        res = geo_us.states.lookup(state.upper())
        if res is None:
            geo_code.err = 1
            print('Not a valid US state. Please enter a valid U.S. state.')
        else:
            return res
    except RuntimeError as err:
        geo_code.err = 1
        print('Error in getting a valid U.S. state code : ', err)


# Get weather data based in user preferred unit
def get_weather_data(geo_code, lat, lon, place):
    weather = {}
    units = 'F'
    try:
        # Accept user input for units
        unit = input("Temperature will be printed in 'F - Fahrenheit' by default. "
                     "\nEnter 1 to continue with the default unit. If you wish to change unit, "
                     "enter 'C' for Celsius, 'K' for Kelvin. "
                     ": ")
        match str(unit).upper():
            case '1':
                units = 'imperial'
                unit = 'F'
            case 'C':
                units = 'metric'
            case 'K':
                units = 'standard'
            case _:  # Default to Fahrenheit
                units = 'imperial'
                unit = 'F'

        # Call the weather api to get the latest weather
        weather = geo_code.open_weather(lat, lon, units.upper())
    except RuntimeError as err:
        print('There was an error in getting weather data. Please retry.')
    else:
        try:
            # Print the weather in Fahrenheit
            if geo_code.err == 0 and weather is not None and len(weather) > 0:
                print_temperature(weather, unit.upper(), place)
        except RuntimeError as err:
            print('Unable to print the weather report. Please retry.')


# Call zipcode API when a zip is entered by user
def process_zip(geo_code, user_input):
    location = {}
    lat = ''
    lon = ''
    place = ''
    try:
        # Get the location details by zipcode from geolocation getter
        location = geo_code.get_geo_data_by_zip(user_input)
        if location is not None and len(location) > 0 and geo_code.err == 0:
            lat = location['lat']
            lon = location['lon']
            place = str(location['name']) + ' ' + str(location['zip'])
    except RuntimeError as err:
        print('Unable to get the location information for zip code :', err)
    return lat, lon, place


# Accept state name from user when a city name is entered and call API for location details
def process_state(geo_code, user_input):
    location = {}
    lat = ''
    lon = ''
    place = ''
    # Accept user input for state code
    user_input_state = input('Please enter the state name : ')
    try:
        # Make sure a valid string is entered for state code
        user_input_state = int(user_input_state)
    except ValueError as val:
        state_cd = get_us_state_cd(user_input_state.upper(), geo_code)  # Validate state code
        if geo_code.err != 1 and state_cd != '':
            location = geo_code.get_geo_data_by_city(user_input.upper(), state_cd)  # Get lat and lon based on city and state
            if location is not None and len(location) > 0 and geo_code.err == 0:
                lat = location[0]['lat']
                lon = location[0]['lon']
                place = str(location[0]['name']) + ' ' + str(location[0]['state'])
    else:
        print('Numeric entry found for state code. Please enter a valid U.S. state.')
    return lat, lon, place


# Print weather information
def print_temperature(weather, unit, place):
    try:
        weather_main = weather['list'][0]['main']
        weather_desc = weather['list'][0]['weather'][0]['description'].upper()
        visibility = weather['list'][0]['visibility']
        wind = weather['list'][0]['wind']['speed']
        clouds = weather['list'][0]['clouds']['all']
        current_temp = weather_main['temp']
        high_temp = weather_main['temp_max']
        low_temp = weather_main['temp_min']
        pressure = weather_main['pressure']
        humidity = weather_main['humidity']
        feels_like = weather_main['feels_like']
        print(
            '\n\n=============================================================================================================================================================')
        print('Weather information for : ', place.upper())
        print('\n\033[1m' + '{:20}''{:28}''{:25}''{:18}''{:16}''{:18}''{:12}''{:15}'.format('Weather',
                                                                                            'Current Temp/Feels Like',
                                                                                            'Max/Min Temperature',
                                                                                            'Pressure(hPa)',
                                                                                            'Humidity %',
                                                                                            'Visibility(mt)',
                                                                                            'Clouds %',
                                                                                            'Wind(mt/sec)') + '\033[0m')
        print('{:20}''{:28}''{:25}''{:18}''{:16}''{:18}''{:12}''{:15}'.format('---------------',
                                                                              '------------------------',
                                                                              '-------------------',
                                                                              '------------',
                                                                              '-----------',
                                                                              '--------------',
                                                                              '---------', '------------'))
        max_min_temp = "".join([str(high_temp), chr(176), unit, ' / ', str(low_temp), chr(176), unit])
        # pressure = "".join([str(pressure), ' hPa'])
        # humidity = "".join([str(humidity), '%'])
        # clouds = "".join([str(clouds), '%'])
        temp_feels_like = "".join([str(current_temp), chr(176), unit, ' / ', str(feels_like), chr(176), unit])
        print('{:20}''{:28}''{:25}''{:18}''{:16}''{:18}''{:12}''{:15}'.format(str(weather_desc),
                                                                              temp_feels_like,
                                                                              max_min_temp,
                                                                              str(pressure) + ' hPa',
                                                                              str(humidity) + '%',
                                                                              str(visibility) + ' mt',
                                                                              str(clouds) + '%', str(wind) + ' mt/sec'))
        print(
            '\n=============================================================================================================================================================')
    except RuntimeError as err:
        print('Unable to print weather. Please retry.')


def main():
    counter = 0
    lat = ''
    lon = ''
    place = ''
    try:
        print('\033[1m' + '         WELCOME TO THE U.S. WEATHER APP      ' + '\033[0m')
        # Accept user input for zip code or city
        user_input = input(
            "Enter the U.S. zip code or city name for which you wish to see the weather information OR Enter '!' to stop : ")
        geo_code = GeoCode()  # Create an instance of the class GeoCode
        while user_input != '!':
            if user_input != '!':
                if counter > 0:
                    geo_code.err = 0
                    user_input = input("\nLookup weather information for another location? "
                                       "Enter a U.S. zip code or U.S. city name or '!' to stop : ")
                try:
                    user_input = int(user_input)  # validate for zip(int) vs city name(string)
                    lat, lon, place = process_zip(geo_code, user_input)
                except ValueError as val:
                    lat, lon, place = process_state(geo_code, user_input)
                except RuntimeError as err:
                    print('There was an error processing user input. Please retry.')
                if lat != '' and lon != '' and geo_code.err == 0:
                    get_weather_data(geo_code, lat, lon, place)
            elif user_input == '!':
                break
            counter += 1
    except RuntimeError as err:
        print('There was an error: ', err, '\nPlease start over.')


if __name__ == '__main__':
    main()
