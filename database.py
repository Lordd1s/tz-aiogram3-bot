class Database:
    def __init__(self):
        self.users = [883371538]

    def get_all_users(self):
        return self.users

    def add_user(self, user_id):
        self.users.append(user_id)
