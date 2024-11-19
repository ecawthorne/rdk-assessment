import os


# Ideally I would use a library for validating and deserializing json such as pydantic if expanding on this type of
# class.
class WeatherDetails:
    def __init__(self, weather_json: dict):
        self.temp = weather_json.get("temp")
        self.pressure = weather_json.get("pressure")
        self.humidity = weather_json.get("humidity")

    def __str__(self):
        return (
            f"Temperature: {self.temp}{os.linesep}"
            f"Pressure: {self.pressure}{os.linesep}"
            f"Humidity: {self.humidity}"
        )
