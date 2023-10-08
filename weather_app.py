import argparse
import os
import requests
from datetime import datetime

WEATHER_API_KEY = "1d47f5bb5b77486a92b131318230310"  
FAVORITE_CITIES_FILE = "favorite_cities.txt"
def get_weather_data(api_key, location):
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "q": location,
        "key": api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
def display_weather_info(data):
    if data is None:
        return

    try:
        location = data["location"]["name"]
        temp_c = data["current"]["temp_c"]
        weather_desc = data["current"]["condition"]["text"]
        humidity = data["current"]["humidity"]
        wind_kph = data["current"]["wind_kph"]
        date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")

        print(f"Weather Stats for - {location} || {date_time}")
        print(f"Current temperature is: {temp_c:.2f} deg C")
        print(f"Current weather desc  : {weather_desc}")
        print(f"Current Humidity      : {humidity}%")
        print(f"Current wind speed    : {wind_kph} km/h")

    except KeyError:
        print("Data format from the API is not as expected.")
def add_favorite_city(city):
    with open(FAVORITE_CITIES_FILE, "a") as f:
        f.write(city + "\n")
def remove_favorite_city(city):
    try:
        with open(FAVORITE_CITIES_FILE, "r") as f:
            lines = f.readlines()
        with open(FAVORITE_CITIES_FILE, "w") as f:
            for line in lines:
                if line.strip() != city:
                    f.write(line)
        print(f"{city} removed from favorites.")
    except FileNotFoundError:
        print(f"{FAVORITE_CITIES_FILE} not found. No cities removed.")
def list_favorite_cities():
    try:
        with open(FAVORITE_CITIES_FILE, "r") as f:
            cities = f.readlines()
        if cities:
            print("Favorite Cities:")
            for index, city in enumerate(cities, start=1):
                print(f"{index}. {city.strip()}")
        else:
            print("No favorite cities added.")
    except FileNotFoundError:
        print(f"{FAVORITE_CITIES_FILE} not found. No favorite cities added.")
def check_weather_for_favorites():
    try:
        with open(FAVORITE_CITIES_FILE, "r") as f:
            cities = f.readlines()
        if cities:
            for city in cities:
                city = city.strip()
                print(f"\nChecking weather for {city}...")
                weather_data = get_weather_data(WEATHER_API_KEY, city)
                display_weather_info(weather_data)
        else:
            print("No favorite cities added.")
    except FileNotFoundError:
        print(f"{FAVORITE_CITIES_FILE} not found. No favorite cities added.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weather App")
    parser.add_argument("--city", help="City name to get weather data")
    parser.add_argument("--add-favorite", help="Add a city to favorites")
    parser.add_argument("--list-favorites", action="store_true", help="List favorite cities")
    parser.add_argument("--remove-favorite", help="Remove a city from favorites")
    parser.add_argument("--check-favorites", action="store_true", help="Check weather for all favorite cities")

    args = parser.parse_args()

    if args.add_favorite:
        add_favorite_city(args.add_favorite)
        print(f"{args.add_favorite} added to favorites.")

    if args.remove_favorite:
        remove_favorite_city(args.remove_favorite)

    if args.list_favorites:
        list_favorite_cities()

    if args.check_favorites:
        check_weather_for_favorites()

    if args.city:
        weather_data = get_weather_data(WEATHER_API_KEY, args.city)
        display_weather_info(weather_data)
