import os
from dotenv import load_dotenv
from discord import Client, Intents, User
import discord
from datetime import datetime
import aiohttp
import tempfile
# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # Discord bot token, from the .env file
USERID = os.getenv('USERID') # UserID of the user to track
CHANNELID = os.getenv('CHANNELID') # ID of the channel where updates will be posted
# Class for the discord bot
class DiscordBot(Client):
    def __init__(self, intents):
        super().__init__(intents=intents)
        self.last_avatar_url = None # Stores the last know avatar URL for comparison
    async def get_user(self):
        try:
            user = await self.fetch_user(int(USERID)) # Fetch user info using their ID
            return user
        except Exception as e:
            print(f"Error fetching user: {e}") # Error if user couldn't be fetches
            return None

    async def on_ready(self):
        # print some info to check if everything is working properly
        print("Bot is ready")
        user = await self.get_user()
        if user:
            print(f"User avatar: {user.avatar.url}") # Print the user avatar url
            print(f"User name: {user.name}") # Print the discord name of the user
            print(f"Channel name: {self.get_channel(int(CHANNELID))}") # Print the channel name
            print(f"Server name: {self.get_channel(int(CHANNELID)).guild.name}") # Print the server name
    async def on_user_update(self, before: User, after: User):
        if before.id == int(USERID) and before.avatar != after.avatar: # Check if the user id didn't change and if the avatar changed
            timestamp = discord.utils.utcnow().timestamp() # Discord time 
            formatted_timestamp = f"<t:{int(timestamp)}:F>"
            channel = self.get_channel(int(CHANNELID)) # store the channel inside a "channel" var
            # If the channel is found, send a message to the channel with the timestamp and the avatar URL
            if channel:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(after.avatar.url) as resp:
                            if resp.status == 200:
                                # Make a temp file 
                                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                                    temp_file.write(await resp.read())
                                    temp_filename = temp_file.name  # Save the path

                    await channel.send(
                    f"**[{formatted_timestamp}]** - User({after.name}) profile picture changed!\n",)
                    await channel.send(file=discord.File(temp_filename))
                    os.unlink(temp_filename)
                except Exception as e:
                    print(f"Error while uploading : {e}")
            else:
                print("Channel not found") # If the channel couldn't be found
            self.last_avatar_url = after.avatar.url # Store the last know avatar URL for comparison
def main():
    # Create intents
    intents = Intents.default()
    intents.members = True
    bot = DiscordBot(intents=intents)
    # run the bot
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
