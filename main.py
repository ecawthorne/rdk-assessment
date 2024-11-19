import argparse
import configparser
import os
import random
from typing import List

from controller import Controller
from favorites_model import FavoritesModel
from view import View

"""
Simple MVC architecture. 

Unit tests for the model and controller could be added fairly easily, the model's database could be replaced with an 
RDBMS or something similar, view could be replaced by another front end such as a webpage.

Important static data is kept in a config file, other options could be added there as needed. 

API key is assumed to be stored in an environment variable called <OPENWEATHER_API_KEY>.  

Input validation, JSON validation, response and error handling would be the first things I would improve if the 
development of this app was continued.

Python 3.10+ required to run as the main module uses the match case functionality.
"""


def run_api_client():
    config = configparser.ConfigParser()
    config.read("config.ini")
    repo = FavoritesModel()
    view = View()
    controller = Controller(config, view, repo)

    while True:
        choice = controller.display_main_menu()
        match choice:
            case "1":
                controller.display_location_details()
            case "2":
                controller.add_location()
            case "3":
                controller.remove_location()
            case "4":
                controller.update_location()
            case "5":
                controller.display_favorites()
            case "6":
                break


# Sort one partition of the unsorted list
def partition(array: List[int], low: int, high: int) -> int:
    pivot = array[high]
    i = low
    for j in range(low, high):
        if array[j] <= pivot:
            # Swap element if less than pivot point
            array[j], array[i] = array[i], array[j]
            i = i + 1

    # The pivot point is now the largest element in the array so swap with last element
    array[high], array[i] = array[i], array[high]

    return i


def quicksort(array: List[int], low: int, high: int):
    if low >= high or low < 0:
        return

    pivot = partition(array, low, high)

    quicksort(array, low, pivot - 1)
    quicksort(array, pivot + 1, high)


# Assuming sort should be in-place instead of return a new list
def sort(numbers: List[int]):
    quicksort(numbers, 0, len(numbers) - 1)


# Assuming that <numbers> is a list of integers.
def sort_and_find_median(numbers: List[int]) -> int:
    sort(numbers)

    return (
        (numbers[(len(numbers) // 2) - 1] + numbers[(len(numbers) // 2)]) / 2
        if len(numbers) % 2 == 0
        else numbers[(len(numbers) // 2)]
    )


def run_sort_example(example: List[int]):
    print(f"Example list: {example}")
    sort(example)
    print(f"Sorted list: {example}")
    print(f"Median: {sort_and_find_median(example)}{os.linesep}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("rdk-assessment")
    parser.add_argument("--run-client", action="store_true")
    parser.add_argument("--sort", action="store_true")
    args = parser.parse_args()

    if args.run_client:
        run_api_client()
    elif args.sort:
        run_sort_example([1, 5, 3, 6, 7, 2, 4, 8])

        run_sort_example(random.sample(range(0, 100), 9))
    else:
        parser.print_help()
