from db_utils import get_or_add_player_id


class User:

    def __init__(self, name):
        self.name = name

    def get_or_create(self):
        """creates the user in the database and returns his id"""
        user_id = get_or_add_player_id(self.name)
        return user_id
