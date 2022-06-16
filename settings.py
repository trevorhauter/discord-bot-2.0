from pathlib import Path

import json


class bot:
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

    def get_rude_phrases(self):
        """
        If a json containing rude phrases exists, read it and return iti
        """
        if Path("rude_phrases.json").is_file():
            with open("rude_phrases.json", "r") as rude_phrases:
                return json.load(rude_phrases)
        else:
            return None


    def log_message(self, message):
        """
        Prints the message and it's relevant data in the console

        :param discord.Message message: The message that was sent
        :return: None
        """
        msg_text = str(message.content)
        author = str(message.author)
        server = str(message.guild)
        channel = str(message.channel)
        admin_status = str(self.is_admin(author))

        print(
            f'NEW MESSAGE "{msg_text}" (USER: "{author}" Server: "{server}" Channel: "{channel}" ADMIN: {admin_status})'
        )

    def create_log_csv(self, name, data, headers=None):
        """
        Creates a CSV with message data
        :param str name: Name of the file
        :param list headers: The headers of the csv file
        :param list data: The messages we want to log
        :return: None
        """
        if not headers:
            headers = ["User", "Message", "Date", "Channel", "Server"]

        with open(name, "w+") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for row in data:
                writer.writerow(row)