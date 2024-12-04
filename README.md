# DiscordAvatarTracker
A Discord bot that tracks avatar changes and sends a message when the user changes their avatar.

This bot is a personal project I did to learn discord.py. The main goal was to build a bot that monitors changes to my 
avatar and stores the updated avatar in a channel. This way, if I lose the original image or want to revert to a 
previous one, I can easily retrieve it.
## Key Features:
- Tracks changes to your Discord avatar for a specific user.
- Sends a message to a designated channel with the new avatar whenever it changes.
- Stores the avatar URL inside a channel for future reference in case you want to revert to it later.
- Logs the timestamp of each change (in European format).
## Setup Instructions:
1. Clone the repository.
2. Create a `.env` file with the following variables:
    - `DISCORD_TOKEN`: Your Discord bot token.
    - `USERID`: The ID of the user to track (your user ID).
    - `CHANNELID`: The ID of the channel where updates will be posted.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run the bot and it will track avatar changes.
### OR
Build the Dockerfile
