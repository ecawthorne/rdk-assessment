# Ideally I would use a library for validating and deserializing json such as pydantic if expanding on this type of
# class.
class Location:
    def __init__(self, location_data: dict):
        self.city = location_data.get("name")
        self.state = location_data.get("state")
        self.country = location_data.get("country")
        self.lat = location_data.get("lat")
        self.lon = location_data.get("lon")

    def __str__(self):
        return f"{self.city}, {self.state}, {self.country} | Lat: {self.lat}, Lon: {self.lon}"
