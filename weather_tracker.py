# =================================================================
# Project 18 - Live Weather Tracker & Global Forecast Engine
# Description: Fetches real-time weather metrics using Geocoding 
#              and dynamic REST API orchestration.
# =================================================================

import requests

class WeatherTracker:
    def __init__(self):
        """Initializes API endpoints for geocoding and current weather forecasts."""
        self.geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.weather_url = "https://api.open-meteo.com/v1/forecast"

    def get_coordinates(self, city_name):
        """
        Translates a human-readable city name into GPS coordinates (Lat/Lon).
        Returns a tuple of (lat, lon, standard_name, country) or None if not found.
        """
        params = {
            "name": city_name,
            "count": "1",
            "format": "json"
        }
        try:
            response = requests.get(self.geo_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "results" in data and len(data["results"]) > 0:
                    result = data["results"][0]
                    return (
                        result["latitude"], 
                        result["longitude"], 
                        result["name"], 
                        result.get("country", "Unknown")
                    )
            return None
        except Exception:
            return None

    def fetch_live_weather(self, city_name):
        """Resolves location details and streams dynamic weather analytics from the API."""
        print(f"\n🔍 Resolving location coordinates for '{city_name}'...")
        
        # Step 1: Dynamic Location Resolution via Geocoding
        location_data = self.get_coordinates(city_name)
        
        if not location_data:
            print("❌ Error: Location not found! Please check the spelling and try again.")
            return

        lat, lon, clean_name, country = location_data
        print(f"📍 Location matched: {clean_name}, {country} ({lat}°, {lon}°)")

        # Step 2: Extracting real-time weather analytics
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true"
        }

        try:
            print(f"🔄 Streaming live weather matrices...")
            response = requests.get(self.weather_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                current = data["current_weather"]
                
                # Render Clean Analytical Tabular Output
                print(f"\n🌤️  --- LIVE WEATHER METRICS: {clean_name.upper()} --- 🌤️")
                print(f"🌍 Country          : {country}")
                print(f"🌡️  Temperature      : {current['temperature']}°C")
                print(f"💨  Wind Velocity    : {current['windspeed']} km/h")
                print(f"🧭  Wind Direction   : {current['winddirection']}°")
                print(f"⏰  Data Timestamp   : {current['time']}")
                print("-" * 50)
            else:
                print("❌ API Server Error: Unable to fetch live metrics at this moment.")
                
        except requests.exceptions.ConnectionError:
            print("❌ Network Connection Error: Please verify your internet link.")
        except Exception as e:
            print(f"❌ Execution Failure: An unexpected error occurred: {e}")

    def run_interface(self):
        """Launches the interactive shell control room for the application."""
        while True:
            print("\n" + "="*40)
            print("🌍 GLOBAL WEATHER TRACKER ENGINE")
            print("="*40)
            print("1. Query Live Weather (Any Global City)")
            print("2. Exit System")
            print("="*40)
            
            choice = input("Select a system operation (1-2): ").strip()
            
            if choice == "1":
                city = input("Enter target city name (e.g., Tokyo, London, Delhi): ").strip()
                if city:
                    self.fetch_live_weather(city)
                else:
                    print("❌ Input Error: City name cannot be empty.")
            elif choice == "2":
                print("\n👋 Deactivating engine. Thank you for using WeatherTracker!")
                break
            else:
                print("❌ Input Error: Invalid operation index. Select 1 or 2.")

if __name__ == "__main__":
    # Standard entry point to instantiate and boot the application
    tracker = WeatherTracker()
    tracker.run_interface()