import discord
from discord.ext import commands
import requests
from requests.auth import HTTPBasicAuth
import json

TOKEN="insert token"

client= commands.Bot(command_prefix="^")
#############################
@client.event
async def on_ready():
    print('Logged on as plane bot')
###############################
@client.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandNotFound):
        error=discord.Embed(
            title="Invalid Command",
            description=("[ ^ref ] if you need reference"),
            colour=discord.Colour.red()
        )
        await ctx.send(embed=error)
############################
@client.command()
async def ref(ctx):
    helper=discord.Embed(
        title="Help",
        description="Use prefix [ ^ ]",
        colour=discord.Colour.green()
    )
    helper.add_field(name="fly",value="Usage : ^fly [Departure ICAO / Airport] [Destination ICAO / Airport]",inline=False)
    helper.add_field(name="flyno",value="Usage : ^fly [Flight Number]",inline=False)
    await ctx.send(embed=helper)
#######################
@client.command()
async def invite(ctx):
    inviter=discord.Embed(
        title="Invite Plane Bot To Your Server",
        description='[Click Here](https://discord.com/oauth2/authorize?client_id=778247615481118720&permissions=8&scope=bot "This link send you to the your browser to invite the Plane Bot") To Invite Plane Bot To Your Server',
        colour=discord.Colour.green()
    )
    await ctx.send(embed=inviter)
######################
@client.command()
async def fly(ctx,icao1,icao2):
    formed="null"
    errorindatapull=0
    if (len(icao1)>1) and (len(icao2)>1):
        response=requests.get("https://api.flightplandatabase.com/search/plans?from={0}&to={1}&limit=1".format(icao1.upper(),icao2.upper()),auth=HTTPBasicAuth('vtV4WsrwNR6mN9Whep7vsjvvUBOwWvBw5Jl8gvKZ', ''))
        formed=json.dumps(response.json(), sort_keys=True, indent=1)
    else:
        error=discord.Embed(
            title="Invalid Usage Of Command",
            description=("^fly [Departure ICAO / Airport] [Destination ICAO / Airport]"),
            colour=discord.Colour.red()
        )
        await ctx.send(embed=error)
    if formed!="null":
        for line in formed.split("\n"):
            line=line.split(":")
            if line[0]=="[]":
                errorindatapull=1
            elif "fromICAO" in line[0]:
                start=line[1]
                start=start.replace(",","")
                start=start.replace('"',"")
            elif "fromName" in line[0]:
                startn=line[1]
                startn=startn.replace(",","")
                startn=startn.replace('"',"")
            elif "toICAO" in line[0]:
                end=line[1]
                end=end.replace(",","")
                end=end.replace('"',"")
            elif "toName" in line[0]:
                endn=line[1]
                endn=endn.replace(",","")
                endn=endn.replace('"',"")
            elif "distance" in line[0]:
                distance=line[1]
                distance=distance.replace(",","")
                distance=distance.replace(" ","")
                distance=round(int(float(distance)))
            elif "maxAltitude" in line[0]:
                maxalt=line[1]
                maxalt=maxalt.replace(",","")
                if int(maxalt)==0:
                    maxalt="N/A"
            elif "waypoints" in line[0]:
                waypoint=line[1]
                waypoint=waypoint.replace(",","")
            elif "flightNumber" in line[0]:
                flightno=line[1]
                flightno=flightno.replace(",","")
                flightno=flightno.replace('"',"")
                if "null" in flightno:
                    flightno="N/A"
            elif "id" in line[0]:
                iden=line[1]
                iden=iden.replace(",","")
                iden=iden.replace(" ","")
    if errorindatapull==1:
        baddata=discord.Embed(
            title="Invalid ICAO / Address has been sent!",
            description="Error with getting data on this plan",
            colour=discord.Colour.red()
        )
        await ctx.send(embed=baddata)
    final = discord.Embed(
        title=str(start)+" To "+str(end),
        description=str(startn)+" To "+str(endn),
        colour=discord.Colour.blue()
    )
    final.set_footer(text="Source : https://flightplandatabase.com")
    final.set_author(name=str(startn)+" To "+str(endn))
    final.add_field(name="Distance",value=str(distance)+" Nautical miles",inline=False)
    final.add_field(name="Suggested Max Altitude",value=str(maxalt)+" Feet",inline=False)
    final.add_field(name="Waypoints",value=str(waypoint),inline=False)
    final.add_field(name="Flight Number",value=str(flightno),inline=False)
    pdf=("https://flightplandatabase.com/plan/"+str(iden)+"/download/pdf")
    final.add_field(name="Route",value=str(pdf),inline=False)
    await ctx.send(embed=final)
###################################
@client.command()
async def flyno(ctx,flightno):
    formed="null"
    errorindatapull=0
    if len(flightno)>1:
        response=requests.get("https://api.flightplandatabase.com/search/plans?flightNumber={0}&limit=1".format(flightno.lower()),auth=HTTPBasicAuth('vtV4WsrwNR6mN9Whep7vsjvvUBOwWvBw5Jl8gvKZ', ''))
        formed=json.dumps(response.json(), sort_keys=True, indent=1)
    else:
        error=discord.Embed(
            title="Invalid Usage Of Command",
            description=("^fly [Flight Number]"),
            colour=discord.Colour.red()
        )
        await ctx.send(embed=error)
    if formed!="null":
        for line in formed.split("\n"):
            line=line.split(":")
            if line[0]=="[]":
                errorindatapull=1
            elif "fromICAO" in line[0]:
                start=line[1]
                start=start.replace(",","")
                start=start.replace('"',"")
            elif "fromName" in line[0]:
                startn=line[1]
                startn=startn.replace(",","")
                startn=startn.replace('"',"")
            elif "toICAO" in line[0]:
                end=line[1]
                end=end.replace(",","")
                end=end.replace('"',"")
            elif "toName" in line[0]:
                endn=line[1]
                endn=endn.replace(",","")
                endn=endn.replace('"',"")
            elif "distance" in line[0]:
                distance=line[1]
                distance=distance.replace(",","")
                distance=distance.replace(" ","")
                distance=round(int(float(distance)))
            elif "maxAltitude" in line[0]:
                maxalt=line[1]
                maxalt=maxalt.replace(",","")
                if int(maxalt)==0:
                    maxalt="N/A"
            elif "waypoints" in line[0]:
                waypoint=line[1]
                waypoint=waypoint.replace(",","")
            elif "flightNumber" in line[0]:
                flightno=line[1]
                flightno=flightno.replace(",","")
                flightno=flightno.replace('"',"")
                if "null" in flightno:
                    flightno="N/A"
            elif "id" in line[0]:
                iden=line[1]
                iden=iden.replace(",","")
                iden=iden.replace(" ","")
    if errorindatapull==1:
        baddata=discord.Embed(
            title="Invalid Flight Number has been sent!",
            description="Error with getting data on this plan",
            colour=discord.Colour.red()
        )
        await ctx.send(embed=baddata)
    final = discord.Embed(
        title=str(start)+" To "+str(end),
        description=str(startn)+" To "+str(endn),
        colour=discord.Colour.blue()
    )
    final.set_footer(text="Source : https://flightplandatabase.com")
    final.set_author(name=str(startn)+" To "+str(endn))
    final.add_field(name="Distance",value=str(distance)+" Nautical miles",inline=False)
    final.add_field(name="Suggested Max Altitude",value=str(maxalt)+" Feet",inline=False)
    final.add_field(name="Waypoints",value=str(waypoint),inline=False)
    final.add_field(name="Flight Number",value=str(flightno),inline=False)
    pdf=str("https://flightplandatabase.com/plan/"+str(iden)+"/download/pdf")
    final.add_field(name="Route",value=pdf,inline=False)
    await ctx.send(embed=final)
#####################################
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
#######################
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

client.run(TOKEN)
