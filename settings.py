from pathlib import Path

import json


class bot_settings:
    """
    This class is used to read/write to data stored for the bot
    It manages our credentials along with an admin list as well as any other data we might need
    """

    def __init__(self):
        """
        Sets up a few base variables, like the admin list
        """
        self.read_admin_file()

    def is_admin(self, author):
        """
        Determins if a user is an admin

        :param str author: The author of the message
        :return: If the user is an admin
        :rtype: bool
        """
        if self.admins:
            return author in self.admins
        else:
            return False

    def add_admin(self, user):
        """
        Adds a user to the admin list

        :param str user: User to be added to admin list
        :return: None
        """
        self.admins.append(user)
        with open("admins.json", "w+") as admin_file:
                admin_file.write(json.dumps(self.admins))

    def remove_admin(self, user_to_remove):
        """
        Adds a user to the admin list

        :param str user: User to be removed from admin list
        :return: None
        """
        self.admins = [user for user in self.admins if user != user_to_remove]
        self.write_admin_file()

    def read_admin_file(self):
        """
        Reads the admin file and sets the values to a class variable
        """
        if Path("admins.json").is_file():
            with open("admins.json") as admin_file:
                self.admins = json.load(admin_file)
        else:
            self.admins = None

    def write_admin_file(self):
        """
        Writes the admin list into a json file
        """
        with open("admins.json", "w+") as admin_file:
                admin_file.write(json.dumps(self.admins))

    def get_api_token(self):
        if Path("based.json").is_file():
            with open("based.json", "r") as api_file:
                return json.load(api_file)
        else:
            raise ValueError("No api credentials were found")

    def get_banned_words(self):
        """
        If a json containing banned words exists, read it and return it
        This file will contain regex entries of words we want to remove from a discord channel
        """
        if Path("banned_words.json").is_file():
            with open("banned_words.json", "r") as words_file:
                return json.load(words_file)
        else:
            return None