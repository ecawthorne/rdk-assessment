import os

from location import Location
from weather_details import WeatherDetails


class View:

    def print_message(self, msg: str):
        print(msg)

    def get_user_input(self, prompt: str) -> str:
        # More robust input validation could be done here.
        return input(prompt)

    def display_favorites(self, favorites: list):
        if not favorites:
            self.print_message("No favorites added.")

        for i, e in enumerate(favorites):
            self.print_message(f"{i + 1}: {e}")

    def display_location(self, location: Location, weather: WeatherDetails):
        self.print_message(str(location))
        if weather:
            self.print_message(str(weather))

    def display_main_menu(self):
        self.print_message(f"{os.linesep}==============================")
        self.print_message("Main Menu")
        self.print_message("1. Find City")
        self.print_message("2. Add City to Favorites")
        self.print_message("3. Remove Favorited City")
        self.print_message("4. Update Favorited City")
        self.print_message("5. Display Favorited Cities")
        self.print_message("6. Quit")

    def prompt_for_location(self):
        return self.get_user_input(
            "Enter a location as <city,state,country> e.g. New York City, New York, US: "
        )

    def choose_favorite(self, param):
        for i, e in enumerate(param):
            self.print_message(f"{i + 1}: {e}")
        choice = self.get_user_input("Select favorite by index: ")
        return choice
