from location import Location


class FavoritesModel:
    def __init__(self):
        self.repo = list()

    def get_all(self):
        return self.repo

    def add_favorite(self, location: Location):
        self.repo.append(location)

    def remove_favorite(self, index: int):
        self.repo.pop(index)

    def update_favorite(self, index: int, updated_location: Location):
        self.repo.insert(index, updated_location)
        self.repo.pop(index)
