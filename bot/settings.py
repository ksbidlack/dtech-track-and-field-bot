import dotenv
import os

HOME = os.environ["HOME"]

# load the environment variables
dotenv.load_dotenv(HOME + "/env_settings/.env")

# private tokens for apis etc.
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
DISCORD_GUILD = os.environ["DISCORD_GUILD"]
PATH_TO_TOKEN = os.environ["PATH_TO_TOKEN"]

# other variables
SCHEDULE_CHANNEL_ID = int(os.environ["SCHEDULE_CHANNEL_ID"])