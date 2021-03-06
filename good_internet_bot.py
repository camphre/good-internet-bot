import datetime
import json
import sys

import discord
import requests
from discord.commands.commands import Option
from logzero import logger

import config
import vrchatapi as vrc

vrc.verify_2FA_code()
vrc.login_and_get_current_user()

bot = discord.Bot()

try:
    with open("guild_ids.json") as f:
        c = json.load(f)
    guild_ids = list(map(int, c["guild_ids"]))
    logger.info(f"guild_ids is {guild_ids}")
except FileNotFoundError as e:
    guild_ids = None
    logger.info("guild_ids is not specified. It takes about an hour to start the bot.")


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.slash_command(guild_ids=guild_ids)
async def jumbo(ctx, name: str = None):
    logger.info(f"jumbo {name}!")

    name = name or ctx.author.name
    await ctx.respond(f"Jumbo {name}!")


@bot.slash_command(
    guild_ids=guild_ids,
    description="入力されたusernameを持つユーザーがオンラインかどうかを返します．",
)
async def get_status_of(ctx, username: Option(str, "username of VRChat")):
    logger.info(f"get_status_of {username}")

    r = vrc.get_user_by_username(username)
    await ctx.defer()

    logger.info(r)

    if r["worldId"] == "offline":
        title = f"{r['displayName']} is offline"
    else:
        title = f"{r['displayName']} is online"

    keys = ["displayName", "username", "worldId"]
    message = "\n".join([f"{key} = {r[key]}" for key in keys])

    embed = discord.Embed(title=title)
    embed.add_field(name="---", value=f"```{message}```")
    embed.set_thumbnail(url=r["currentAvatarThumbnailImageUrl"])

    await ctx.respond(embed=embed)


@bot.slash_command(guild_ids=guild_ids, description="VRChatで今日開催される音楽イベントを通知します．")
async def get_todays_vrc_music_events(ctx):
    logger.info("get_todays_vrc_music_events")

    response = requests.get(config.calender_url)
    await ctx.defer()

    data = json.loads(response.text)
    logger.info(data)

    event_title = "\n".join([event["title"] for event in data.values()])
    event_date = "\n".join([event["startTime"] for event in data.values()])

    embed = discord.Embed(title="Today's VRC Music Events")

    if data == {}:
        embed.description = (
            f"VRCクラブイベントカレンダー上で今日({datetime.date.today()})開催されるイベントはありません．"
        )
    else:
        embed.description = (f"今日({datetime.date.today()}), VRChatで開催されるクラブイベント",)
        embed.add_field(name="イベント名", value=event_title)
        embed.add_field(name="時間", value=event_date)

    await ctx.respond(embed=embed)


bot.run(config.token)
