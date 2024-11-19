import configparser
import os
import urllib.parse
from typing import Optional

import requests

from favorites_model import FavoritesModel
from location import Location
from view import View
from weather_details import WeatherDetails


class Controller:
    def __init__(
        self, config: configparser.ConfigParser, view: View, model: FavoritesModel
    ):
        self.config = config
        self.view = view
        self.model = model

    @staticmethod
    def make_request(req_string: str) -> requests.Response:
        return requests.get(
            req_string + f"&appid={os.environ.get('OPENWEATHER_API_KEY')}"
        )

    # The API requires latitude and longitude in order to get the weather details. I'm making the assumption that the
    # user should not be expected to know the exact coordinates of a location, so we need to get the geocoded location
    # before requesting those details.
    def request_geocoded_location(self, location_name: str) -> Optional[Location]:
        response = self.make_request(
            self.config.get("URL", "geocoding_url")
            + urllib.parse.quote_plus(location_name)
        )

        try:
            # The response is a list of locations, I'm only using the first returned result for this assessment. If I
            # were planning to expand on this I would use something like pydantic along with schemas to validate and
            # deserialize the returned data in a more robust way. I would also add an additional
            # menu to allow the user to choose the closest match from a list.
            if response.json()[0]:
                return Location(response.json()[0])
        except (requests.JSONDecodeError, KeyError, IndexError):
            pass

        return None

    def request_weather_details(self, location: Location) -> Optional[WeatherDetails]:
        response = self.make_request(
            self.config.get("URL", "weather_data_url")
            + f"lat={location.lat}&lon={location.lon}&units=imperial)"
        )

        try:
            # Only using one section of returned json for sake of simplicity
            weather_json = response.json().get("main")
            if weather_json:
                return WeatherDetails(response.json().get("main"))
        except requests.JSONDecodeError:
            pass

        return None

    def display_location_details(self):
        location_name = self.view.prompt_for_location()
        location = self.request_geocoded_location(location_name)
        location_details = None

        if location:
            location_details = self.request_weather_details(location)

        if location_details:
            self.view.display_location(location, self.request_weather_details(location))
        else:
            self.view.print_message(
                f'No weather data found for "{location_name}". Check API key.'
            )

    def add_location(self):
        favorites = self.model.get_all()
        if len(favorites) >= 3:
            self.view.print_message(
                f"You can only have up to three cities favorited at a time, remove a city and try "
                f"again."
            )
            return

        location_name = self.view.prompt_for_location()
        location = self.request_geocoded_location(location_name)

        if location:
            self.model.add_favorite(location)
            self.view.print_message(f"SUCCESS: Added {location}")
        else:
            self.view.print_message("Location not found. Try again.")

    def remove_location(self):
        favorites = self.model.get_all()
        if len(favorites) == 0:
            self.view.print_message(
                f"No cities favorited, add a city before trying to remove cities."
            )
            return

        self.view.print_message(f"Favorite to remove: ")
        location_index = self.choose_favorite()
        if 0 <= location_index < len(self.model.get_all()):
            self.model.remove_favorite(location_index)
            self.view.print_message(f"SUCCESS: Removed location {location_index + 1}")
            return
        self.view.print_message("Invalid choice. Try again.")

    def update_location(self):
        if not self.model.get_all():
            self.view.print_message(
                f"No cities favorited, add a city before trying to update cities."
            )
            return

        self.view.print_message("Choose location to update: ")
        location_index = self.choose_favorite()
        if location_index < 0 or location_index > len(self.model.get_all()):
            self.view.print_message("No location selected.")
            return

        new_location = self.request_geocoded_location(self.view.prompt_for_location())

        if new_location:
            self.model.update_favorite(location_index, new_location)
            self.view.print_message(
                f"SUCCESS: Updated {location_index} to {new_location}"
            )
        else:
            self.view.print_message(f"Location not found. Try again.")

    def choose_favorite(self):
        try:
            return int(self.view.choose_favorite(self.model.get_all())) - 1
        except ValueError:
            return -1

    def display_favorites(self):
        self.view.display_favorites(self.model.get_all())

    def display_main_menu(self):
        self.view.display_main_menu()
        return self.view.get_user_input("Enter Selection: ")
