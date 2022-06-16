import os
import random
import re

import discord
import csv
from discord.ext import commands

from settings import bot


# Random discord configurations honestly idk what this does
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=":", intents=intents)


@client.event
async def on_ready():
    """
    This function is triggered when the bot is online
    """
    print("BOT ONLINE")


@client.event
async def on_message(message):
    """
    This function is called when a message is sent in a discord the bot is a member of

    :param discord.Message message: The message that was sent
    :return: None
    """
    bot.log_message(message)

    msg_txt = str(message.content).lower()
    author = str(message.author)
    author_is_admin = bot.is_admin(author)

    if msg_txt.startswith("!"):

        # Command for adding an admin (ADMINS ONLY)
        match = re.match(r"!addadmin +(?P<username>[\w#]+)", msg_txt)
        if match and author_is_admin:
            username = match.groupdict()["username"]
            bot.add_admin(username)
            await message.channel.send(username + " has been added as an admin")

        # Command for removing an admin (ADMINS ONLY)
        match = re.match(r"!removeadmin +(?P<username>[\w#]+)", msg_txt)
        if match and author_is_admin:
            username = match.groupdict()["username"]
            bot.remove_admin(username)
            await message.channel.send(username + " has been removed as an admin")

        # Command to log all messages in a channel (ADMINS ONLY)
        match = re.match(r"!logchannel ?(?P<keyword>\w+)?", msg_txt)
        if match:
            message_data = []
            keyword = match.groupdict()["keyword"]
            if keyword:
                print(f"WE HAVE THE KEYWORD {keyword}")
            await message.channel.send(f"Logging channel, this may take a sec...")
            async for msg in message.channel.history(limit=100000):
                if keyword:
                    if keyword in str(msg.content).lower():
                        message_data.append(
                            [
                                msg.author.name,
                                msg.content,
                                msg.created_at,
                                message.channel,
                                msg.guild,
                            ]
                        )
                else:
                    message_data.append(
                        [
                            msg.author.name,
                            msg.content,
                            msg.created_at,
                            message.channel,
                            msg.guild,
                        ]
                    )

            # Send a message to the channel letting them know how many matches we found
            if message_data:
                if keyword:
                    await message.channel.send(
                        f"The word {keyword} appeared in {len(message_data)} messages in this channel"
                    )
                else:
                    await message.channel.send(
                        f"There are {len(message_data)} messages in this channel"
                    )
                # If the user is an admin, send them the CSV
                if author_is_admin:
                    csv_name = f"{message.guild.name}_{message.channel}_log.csv"
                    bot.create_log_csv(csv_name, message_data)
                    file = discord.File(csv_name)
                    await message.author.send(file=file)
                    print("Logged channel file sent to admin")
                    del message_data
                    os.remove(csv_name)

                print("channel logged")

        # Command to clean the channel of any banned words (ADMINS ONLY)
        match = re.match(r"!cleanchannel", msg_txt)
        if match:
            """
            Cleans the discord channel of any banned words. If there is a local file titled banned_words.json, we loop through all the messages
            in the channel and any that return a match are removed. The banned_words.json file is a list of strings, each strings contains regex
            to words or phrases we are trying to remove
            """
            if author_is_admin:
                banned_words = bot.get_banned_words()
                if banned_words:
                    await message.channel.send(
                        "Cleaning discord channel, this may take a bit..."
                    )

                    banned_words_re = "|".join(banned_words)
                    messages_removed = []

                    async for msg in message.channel.history(limit=100000):
                        match = re.search(
                            banned_words_re, str(msg.content), re.IGNORECASE
                        )
                        if match:
                            messages_removed.append(
                                [
                                    msg.author.name,
                                    msg.content,
                                    msg.created_at,
                                    message.channel,
                                    msg.guild,
                                ]
                            )
                            await msg.delete()

                    if messages_removed:
                        csv_name = f"removed_messages_{message.guild.name}_{message.channel}_log.csv"
                        bot.create_log_csv(csv_name, messages_removed)
                        file = discord.File(csv_name)
                        await message.author.send(file=file)

                        await message.channel.send(
                            f"{len(messages_removed)} messages have been removed... Jesus..."
                        )
                        del messages_removed
                        os.remove(csv_name)

                    else:
                        await message.channel.send(
                            "No messages were matched, so none were removed"
                        )
                else:
                    await message.channel.send("No banned word file exists")
            else:
                await message.channel.send("NOPE! You're not an admin, sorry sweetie")

        # --------------------
        # END OF ADMIN ONLY COMMANDS
        # --------------------

        # Command for list all admins
        match = re.match(r"!listadmins", msg_txt)
        if match:
            admin_list_message = "-- ADMINS --\n" + "".join(
                "      " + str(admin) + "\n" for admin in bot.admins
            )
            await message.channel.send(admin_list_message)

        # Command that sends a random message from a list of "rude" messages stored in a local json file
        match = re.match(r"!rude", msg_txt)
        if match:
            rude_phrases = bot.get_rude_phrases()
            if rude_phrases:
                await message.author.send(random.choice(rude_phrases))

        # Command to list all the available commands
        match = re.match(r"!help", msg_txt)
        if match:
            admin_command_list = ["!addadmin <user>", "!removeadmin <user>", "!logchannel <optional keyword>", "!cleanchannel"]
            regular_command_list = ["!listadmins", "!rude", "!help"]
            command_list = "-- COMMANDS --\n" + "".join("" + command + "\n" for command in regular_command_list)
            if author_is_admin:
                command_list += "\n-- ADMIN COMMANDS --\n" + "".join("" + command + "\n" for command in admin_command_list)
            await message.channel.send(command_list)


"""
Creates our bot profile for managing our data
Creates our bot class instance to execute commands
"""
bot = bot()

# Start the bot
client.run(bot.get_api_token())
print("Bot Finished")
