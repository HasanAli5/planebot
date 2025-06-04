import discord
from discord.ext import commands
import requests
from requests.auth import HTTPBasicAuth
import folium
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")

intents = discord.Intents.default()
intents.message_content = True

custom_prefix = "^"

bot = commands.Bot(command_prefix=custom_prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')
    
@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandNotFound):
        error=discord.Embed(
            title="Invalid Command",
            description=(f"```{custom_prefix}help``` if you need reference"),
            colour=discord.Colour.red()
        )
        await ctx.send(embed=error)

@bot.hybrid_command()
async def invite(ctx):
    inviter=discord.Embed(
        title="Invite Plane Bot To Your Server",
        description='[Click Here](https://discord.com/oauth2/authorize?client_id=778247615481118720 "This link send you to the your browser to invite the Plane Bot") To Invite Plane Bot To Your Server',
        colour=discord.Colour.green()
    )
    await ctx.send(embed=inviter)

@bot.hybrid_command()
async def fly(ctx,icao1,icao2):
    code = None
    data = None
    if (len(icao1)>0) and (len(icao2)>0):
        response=requests.get("https://api.flightplandatabase.com/search/plans?from={0}&to={1}&limit=1".format(icao1.upper(),icao2.upper()),auth=HTTPBasicAuth(API_KEY, ''))
        data = response.json()[0]
        code = response.status_code
    else:
        error=discord.Embed(
            title="Invalid Usage Of Command",
            description=(f"```{custom_prefix}fly``` ```[Departure ICAO / Airport]``` ```[Destination ICAO / Airport]```"),
            colour=discord.Colour.red()
        )
        await ctx.send(embed=error)

    if code==404:
        baddata=discord.Embed(
            title="Invalid ICAO / Address has been sent!",
            description="Error with getting data on this plan",
            colour=discord.Colour.red()
        )
        await ctx.send(embed=baddata)
    
    final = discord.Embed(
        title=f"{data["fromName"]} To {data["toName"]}",
        description=f"{data["fromICAO"]} To {data["toICAO"]}",
        colour=discord.Colour.blue()
    )
    final.set_footer(text="Source : https://flightplandatabase.com")
    final.set_author(name=f"{data["flightNumber"]}")
    final.add_field(name=f"Distance",value= f"{data["distance"]} Nautical miles",inline=False)
    final.add_field(name=f"Suggested Max Altitude",value= f"{data["maxAltitude"]} Feet",inline=False)
    final.add_field(name=f"Waypoints",value=f"{data["waypoints"]}",inline=False)
    pdf=f"https://flightplandatabase.com/plan/{data["id"]}/download/pdf"
    final.add_field(name="Route",value=pdf,inline=False)
    await ctx.send(embed=final)

@bot.hybrid_command()
async def flyno(ctx,flightno):
    code = None
    data = None
    if len(flightno)>0:
        response=requests.get("https://api.flightplandatabase.com/search/plans?flightNumber={0}&limit=1".format(flightno.lower()),auth=HTTPBasicAuth(API_KEY, ''))
        data = response.json()[0]
        code = response.status_code
    else:
        error=discord.Embed(
            title="Invalid Usage Of Command",
            description=(f"```{custom_prefix}flyno``` ```[Flight Number]```"),
            colour=discord.Colour.red()
        )
        await ctx.send(embed=error)

    if code==404:
        baddata=discord.Embed(
            title="Invalid Flight Number has been sent!",
            description="Error with getting data on this plan",
            colour=discord.Colour.red()
        )
        await ctx.send(embed=baddata)
    
    final = discord.Embed(
        title=f"{data["fromName"]} To {data["toName"]}",
        description=f"{data["fromICAO"]} To {data["toICAO"]}",
        colour=discord.Colour.blue()
    )
    final.set_footer(text="Source : https://flightplandatabase.com")
    final.set_author(name=f"{data["flightNumber"]}")
    final.add_field(name=f"Distance",value= f"{data["distance"]} Nautical miles",inline=False)
    final.add_field(name=f"Suggested Max Altitude",value= f"{data["maxAltitude"]} Feet",inline=False)
    final.add_field(name=f"Waypoints",value=f"{data["waypoints"]}",inline=False)
    pdf=f"https://flightplandatabase.com/plan/{data["id"]}/download/pdf"
    final.add_field(name="Route",value=pdf,inline=False)
    await ctx.send(embed=final)

@fly.error
async def fly_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        error=discord.Embed(
            title="Invalid Usage Of Command",
            description=("^fly [Departure ICAO / Airport] [Destination ICAO / Airport]"),
            colour=discord.Colour.red()
        )
        await ctx.send(embed=error)
    else:
        print("other error with fly fucntion")

@flyno.error
async def flyno_error(ctx,error):
    if isinstance(error,commands.MissingRequiredArgument):
        error=discord.Embed(
            title="Invalid Usage Of Command",
            description=("^fly [Flight Number]"),
            colour=discord.Colour.red()
        )
        await ctx.send(embed=error)
    else:
        print("other error with flyno fuction")

bot.run(TOKEN)
