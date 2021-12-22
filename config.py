from dotenv import load_dotenv

load_dotenv()

import os

# vrchat
username = os.getenv("username")
password = os.getenv("password")
totp = os.getenv("totp")

# discord
token = os.getenv("token")

# google calender
calender_url = os.getenv("calender_url")
