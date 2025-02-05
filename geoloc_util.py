import re
import requests
import argparse
import json

API_KEY = "f897a99d971b5eef57be6fafa0d83239"
COUNTRY_CODE = "US"
BASE_URL = "http://api.openweathermap.org/geo/1.0"

def is_zip_code(location):
    return re.fullmatch(r"\d{5}", location.strip()) is not None

def verify_response_and_get_data(location, response):
    if response.status_code != 200:
        raise Exception(f"Error fetching data for location '{location}': {response.text}")
    
    data = response.json()
    if not data:
        raise Exception(f"No results found for '{location}'") 
    return data

def get_location_information_by_zip(location):
    url = f"{BASE_URL}/zip"
    parameters = {
        "zip": f"{location},{COUNTRY_CODE}",
        "appid": API_KEY
    }
    data = verify_response_and_get_data(location, requests.get(url, params=parameters))
    result = {
        location: {
            "name": data.get("name"),
            "lat": data.get("lat"),
            "lon": data.get("lon"),
            "zip": data.get("zip"),
            "country": data.get("country")
        }
    }
    return result

def get_location_information_city(location):
    url = f"{BASE_URL}/direct"
    parameters = {
        "q": f"{location}, {COUNTRY_CODE}",
        "limit": 1,
        "appid": API_KEY
    }
    data = verify_response_and_get_data(location, requests.get(url, params=parameters))
    result_data = data[0]
    result = {
        location: {
            "name": result_data.get("name"),
            "lat": result_data.get("lat"),
            "lon": result_data.get("lon"),
            "country": result_data.get("country"),
            "state": result_data.get("state")
        }
    }
    return result

def main():
    parser = argparse.ArgumentParser(
        description="Fetch geographical information for US locations using the OpenWeather Geocoding API."
    )
    parser.add_argument(
        "locations",
        nargs="+",
        help="List of locations (e.g., 'Madison, WI' or '12345')."
    )
    args = parser.parse_args()

    results = []
    for location in args.locations:
        try:
            if is_zip_code(location):
                result = get_location_information_by_zip(location)
            else:
                result = get_location_information_city(location)
            results.append(result)
        except Exception as e:
            results.append({location: {"error": str(e)}})

    print(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()
