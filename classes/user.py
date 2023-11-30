from db_utils import get_or_add_player_id


class User:

    def __init__(self, name):
        self.name = name

    def get_or_create(self):
        user_id = get_or_add_player_id(self.name)
        return user_id
