import re

import discord
from discord.ext import commands

from settings import bot_settings


# Random discord configurations honestly idk what this does
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=':', intents=intents)


class bot():
    """
    This class processes messages and executes commands
    """

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
        admin_status = str(bot_profile.is_admin(author))

        print(f'NEW MESSAGE "{msg_text}" (USER: "{author}" Server: "{server}" Channel: "{channel}" ADMIN: {admin_status})')

    def process_messages(self, message):
        """
        Determines which command is being called and calls the appropriate function to complete the task

        :param discord.Message message: The message that was sent
        :return: None
        """
        msg_txt = str(message.content).lower()
        author = str(message.author)
        author_is_admin = bot_profile.is_admin(author)
        if msg_txt.startswith("!"):

            # Command for adding an admin (ADMINS ONLY)
            match = re.match(r"!addadmin +(?P<username>[\w#]+)", msg_txt)
            if match and author_is_admin:
                username = match.groupdict()["username"]
                bot_profile.add_admin(username)

            # Command for removing an admin (ADMINS ONLY)
            match = re.match(r"!removeadmin +(?P<username>[\w#]+)", msg_txt)
            if match and author_is_admin:
                username = match.groupdict()["username"]
                bot_profile.remove_admin(username)

             # Command for list all admins
            match = re.match(r"!listadmins", msg_txt)
            if match:
                print(bot_profile.admins)

        else:
            print("NOT A COMMAND")


@client.event
async def on_ready():
    """
    This function is triggered when the bot is online
    """
    print('BOT ONLINE')


@client.event
async def on_message(message):
    """
    This function is called when a message is sent in a discord the bot is a member of

    :param discord.Message message: The message that was sent
    :return: None
    """
    bot.log_message(message)
    bot.process_messages(message)


"""
Creates our bot profile for managing our data
Creates our bot class instance to execute commands
"""
bot_profile = bot_settings()
bot = bot()


# Start the bot
client.run(bot_profile.get_api_token())
print("Bot Finished")