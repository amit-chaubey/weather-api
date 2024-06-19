import datetime
import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

API_KEY = open('apikey.txt', 'r').read().strip()  # Ensure API key is read properly
CITY = "LIVERPOOL"

def kel_to_cel_fah(kelvin):
    """
    Convert temperature from Kelvin to Celsius and Fahrenheit.
    """
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return celsius, fahrenheit

def fetch_weather_data(api_key, city):
    """
    Fetch weather data from the OpenWeather API.
    """
    url = f"{BASE_URL}appid={api_key}&q={city}"
    response = requests.get(url)
    return response.json()

def extract_weather_info(response):
    """
    Extract relevant weather information from the API response.
    """
    temp_kel = response['main']['temp']
    temp_cel, temp_fah = kel_to_cel_fah(temp_kel)
    feels_like_kelvin = response['main']['feels_like']
    feels_like_cel, feels_like_fah = kel_to_cel_fah(feels_like_kelvin)
    humidity = response['main']['humidity']
    description = response['weather'][0]['description']
    timezone_offset = response['timezone']
    sunrise_time = datetime.datetime.fromtimestamp(response['sys']['sunrise'] + timezone_offset)
    sunset_time = datetime.datetime.fromtimestamp(response['sys']['sunset'] + timezone_offset)
    
    return {
        'temp_celsius': temp_cel,
        'temp_fahrenheit': temp_fah,
        'feels_like_celsius': feels_like_cel,
        'feels_like_fahrenheit': feels_like_fah,
        'humidity': humidity,
        'description': description,
        'sunrise': sunrise_time,
        'sunset': sunset_time
    }

def display_weather_info(weather_info, city):
    """
    Display the weather information in a readable format.
    """
    print(f'Temperature in {city}: {weather_info["temp_celsius"]:.2f}°C / {weather_info["temp_fahrenheit"]:.2f}°F')
    print(f'Temperature in {city} feels like: {weather_info["feels_like_celsius"]:.2f}°C / {weather_info["feels_like_fahrenheit"]:.2f}°F')
    print(f'Humidity in {city}: {weather_info["humidity"]}%')
    print(f'Weather description: {weather_info["description"]}')
    print(f'Sunrise time in {city}: {weather_info["sunrise"].strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'Sunset time in {city}: {weather_info["sunset"].strftime("%Y-%m-%d %H:%M:%S")}')

def main():
    response = fetch_weather_data(API_KEY, CITY)
    weather_info = extract_weather_info(response)
    display_weather_info(weather_info, CITY)

if __name__ == '__main__':
    main()
