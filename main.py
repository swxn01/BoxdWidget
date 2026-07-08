import os
import json
import time
import requests

from datetime import datetime

from dotenv import load_dotenv
from letterboxdpy.user import User
from letterboxdpy.movie import Movie


# Load .env
load_dotenv()

LETTERBOXD_USERNAME = os.getenv("LETTERBOXD_USERNAME")

DISCORD_APPLICATION_ID = os.getenv("DISCORD_APPLICATION_ID")
DISCORD_USER_ID = os.getenv("DISCORD_USER_ID")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


DISCORD_URL = (
    f"https://discord.com/api/v9/applications/"
    f"{DISCORD_APPLICATION_ID}/users/"
    f"{DISCORD_USER_ID}/identities/0/profile"
)


CACHE_FILE = "cache.json"
REFRESH_TIME = 1800  #in seconds


def load_cache():

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    return {}


def save_cache(data):

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def update_profile():

    cache = load_cache()

    print(
        f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking Letterboxd..."
    )


    # Get latest user data
    user = User(LETTERBOXD_USERNAME)

    username = user.username

    avatar = None

    if user.avatar and "url" in user.avatar:
        avatar = user.avatar["url"]


    favorites = list(user.favorites.values())[:4]

    favorite_slugs = [
        movie["slug"]
        for movie in favorites
    ]


    user_changed = (
        cache.get("username") != username
    )

    favorites_changed = (
        cache.get("favorites") != favorite_slugs
    )


    # Check for change against cached data
    if user_changed or favorites_changed:

        print("Favorites changed, updating movie data")

        movies_cache = {}


        for movie_data in favorites:

            slug = movie_data["slug"]


            if slug in cache.get("movies", {}):

                movies_cache[slug] = cache["movies"][slug]

                continue


            movie = Movie(slug)


            director = "n/a"

            if (
                "director" in movie.crew
                and movie.crew["director"]
            ):
                director = movie.crew["director"][0]["name"]


            movies_cache[slug] = {
                "name": movie.title,
                "poster": movie.poster,
                "info": f"{movie.year} • {director}"
            }


        cache = {
            "username": username,
            "favorites": favorite_slugs,
            "avatar": avatar,
            "movies": movies_cache
        }


        save_cache(cache)

        print("Movie cache updated")

    else:

        print("No changes detected, using cached movies")



    # Build Discord widget data
    dynamic_data = [
        {
            "type": 3,
            "name": "avatar",
            "value": {
                "url": cache["avatar"]
            }
        }
    ]


    for index, slug in enumerate(favorite_slugs, start=1):

        movie = cache["movies"][slug]


        dynamic_data.extend(
            [
                {
                    "type": 1,
                    "name": f"moviename{index}",
                    "value": movie["name"]
                },
                {
                    "type": 1,
                    "name": f"movieinfo{index}",
                    "value": movie["info"]
                },
                {
                    "type": 3,
                    "name": f"movieposter{index}",
                    "value": {
                        "url": movie["poster"]
                    }
                }
            ]
        )


    payload = {
        "username": username,
        "data": {
            "dynamic": dynamic_data
        }
    }


    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bot {DISCORD_TOKEN}",
        "User-Agent": "DiscordBot (https://github.com/discord/discord-api-docs, 1.0.0)"
    }


    response = requests.patch(
        DISCORD_URL,
        headers=headers,
        json=payload
    )


    if response.status_code == 204:

        print("Discord profile updated")

    else:

        print(
            f"Discord update failed: {response.status_code}"
        )




print("letterboxd Discord updater started")

while True:

    try:

        update_profile()

    except Exception as e:

        print(
            f"Error during update: {e}"
        )


    print(
        "Waiting 30 minutes for next refresh"
    )

    time.sleep(REFRESH_TIME)