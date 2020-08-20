import asyncio
import discord
from discord.ext import commands
import json
import time
from currency_converter import CurrencyConverter
import requests
import ssl
import functions
import random

ssl._create_default_https_context = ssl._create_unverified_context

##################################### Everything within only happens if the config.json doesn't exist

try:
    with open("config.json", "r") as file:
        pass
except FileNotFoundError:
    print("Config file not found, creating new one...")

    x = {
      "USER_TOKENS": ["YOUR TOKEN HERE"],
      "SAFE_MODE": False,
      "PREFIX": "dep.",
      "INVITE": "https://discord.gg/wCfUgSK",
      "SPOOF_TOKEN": False,
      "ANTI_BAN": False,
      "UNUSED0": None,
      "UNUSED1": None,
      "UNUSED2": None,
      "UNUSED3": None,
      "UNUSED4": None,
      "UNUSED5": None,
      "UNUSED6": None,
      "UNUSED7": None,
    }

    with open("config.json", "w") as file:
        json.dump(x, file, indent=4)
        print("Config file created, please fill in your tokens and restart the bot.")
        exit()
try:
    length = 0
    with open("macro.json", 'r') as mac:
        macros = []
        for x in mac:
            macros.append(x)
            length += 1
        macros = macros[2:(length - 2)]


except FileNotFoundError:
    x = {
      "MACROS":
          [
              "rs", "https://recoverysaints.net",
              "soar", "https://soaritic.us",
              "empty example", "when adding more, dont forget to put a comma here >"
          ]
    }

    with open("macro.json", "w") as mac:
        json.dump(x, mac, indent=4)

#####################################

# Reading config file and assigning all required variables
try:
    with open("config.json", "r") as configFile:
        global prefix, invite, safeMode, heightUnit, weightUnit
        configData = json.load(configFile)
        tokens = configData["USER_TOKENS"]
        prefix = configData["PREFIX"]
        safeMode = configData["SAFE_MODE"]
        invite = configData["INVITE"]
except:
    print("Something is wrong with your config.json file, we suggest deleting it and having "
          "the bot create the file anew.")
    exit()

shownIntro = False

class SelfBot(commands.Cog):
    def __init__(self, client):
        global shownIntro
        self.client = client
        if not shownIntro:
            print("|||||||||||||||||||||||||||||||||||||||||||||||||||||")
            print("")
            print("    DepressoSelfBot by Soariticus / 0x0000ff#5455      ")
            if safeMode:
                print("                 SafeMode Enabled                  ")
            else:
                print("")
            print("")
            print("|||||||||||||||||||||||||||||||||||||||||||||||||||||")
            shownIntro = True

    @commands.command()
    async def ping(self, ctx):
        print(f"Ping command used. ({prefix}ping [user] [amount of times])")
        con = ctx.message.content.split()  # Make it so we can read the arguments
        amt = 0
        toPing = None
        try:
            # Gotta make sure the dumbass user doesn't fuck up and use the wrong syntax.
            toPing = con[1]  # Whilst this isn't required, makes it more readable
            amt = int(con[2])  # Amount of pings, has to be int or it'll just shit itself.
        except ValueError:  # Caused when "con[2]" can't be converted to int (when its something other than just numbers)
            await ctx.send("Retard, use proper syntax. `dep.ping [user] [amount]`. It's not that hard.")
        except IndexError:  # Caused when con[1] or con[2] can't be reached
            await ctx.send("Jesus christ, you gotta fill in all the arguments, retard. `dep.ping [user] [amount]`")
        for x in range(amt):
            await ctx.send(toPing)

    @commands.command()
    async def gping(self, ctx):
        await ctx.message.delete()
        print(f"Gping command used. ({prefix}gping [user] [amount of times])")
        con = ctx.message.content.split()  # Make it so we can read the arguments
        amt = 0
        toPing = None
        try:
            # Gotta make sure the dumbass user doesn't fuck up and use the wrong syntax.
            toPing = con[1]  # Whilst this isn't required, makes it more readable
            amt = int(con[2])  # Amount of pings, has to be int or it'll just shit itself.
        except ValueError:  # Caused when "con[2]" can't be converted to int (when its something other than just numbers)
            await ctx.send("Retard, use proper syntax. `dep.ping [user] [amount]`. It's not that hard.")
        except IndexError:  # Caused when con[1] or con[2] can't be reached
            await ctx.send("Jesus christ, you gotta fill in all the arguments, retard. `dep.ping [user] [amount]`")
        for x in range(amt):
            await ctx.send(toPing, delete_after=0)

    @commands.command()
    async def remind(self, ctx):
        print(f"Remind command used. ({prefix}remind [user] [time in minutes])")
        try:  # Wanna see if the user has mentioned anyone
            user = ctx.message.mentions[0] # Setting the person that we need to remind to the user mentioned
            i = 2  # In this case, we have to start at the 3rd spot in the message.
        except IndexError:  # If ctx.message.mentions[0] doesn't exist (no mentions), do this instead.
            user = ctx.message.author  # If no mention, remind the user themselves
            i = 1  # In that case, we start on the second spot in the message
        reason = []   # Defining the variable reason as an array, otherwise py shits itself
        time = 15  # Setting the default time to 15 seconds (later converted to 15 minutes)
        args = ctx.message.content.split()  # Splitting the message content
        for x in range(len(args)):  # Loop through the entire message
            if i < len(args):
                try:
                    time = int(args[i])  # Trying to see if the current part of the message is an int
                    i += 1
                except ValueError:  # Caused if we cannot convert it to int (it's something other than numbers)
                    reason.append(args[i])  # Add it to the reason array
                    i += 1
        reason = " ".join(reason)  # Turn the array into a big string
        await ctx.send(f"Reminding {user} of `{reason}` in {time} minute(s).")  # Not pinging user, already got pinged
        await asyncio.sleep(time * 60)  # Turn the number given into minutes on a different threat so more can run
        # consecutively
        await ctx.send(f"{user.mention} reminding you of `{reason}`.")  # Reminder

    @commands.command()
    async def invite(self, ctx):
        try:
            user = ctx.message.mentions[0]
            await user.send(invite)
        except IndexError:
            await ctx.send(invite)

    @commands.command()
    async def annoy(self, ctx):
       global annoyUsers
       annoyUsers.append(ctx.message.mentions[0])
       await ctx.send(f"added {ctx.message.mentions[0]} to annoylist")
       await ctx.send(f"full list = {annoyUsers}")

    @commands.command()
    async def credits(self, ctx):
        await ctx.message.delete()
        if safeMode:
            await ctx.send("**DepressoSelfBot by Soariticus#0666 | https://discord.gg/wCfUgSK | https://soaritic.us |**")
        if not safeMode:
            embed = discord.Embed(color=random.randint(0, 16777215))
            embed.add_field(name="Depresso SelfBot", value="By Soariticus / 0x0000ff#5455", inline=False)
            embed.add_field(name="Discord", value="https://discord.gg/wCfUgSK", inline=True)
            embed.add_field(name="Website", value="https://soaritic.us", inline=True)
            await ctx.send(embed=embed)

    @commands.command()
    async def mac(self, ctx):
        args = ctx.message.content.split()
        await ctx.message.delete()
        yes = stop = False
        msg = args[1]
        i = 0
        for x in macros:
            if yes:
                if not stop:
                    new = x.replace("\"", "")
                    await ctx.send(new.replace(",", ""))
                    yes = False
                    stop = True
            if msg in x:
                if (i % 2) != 0:
                    pass
                else:
                    yes = True
            i += 1

    @commands.command()
    async def latency(self, ctx):
        await ctx.message.delete()
        before = time.monotonic()
        message = await ctx.send("Calculating...")
        ping = (time.monotonic() - before) * 100
        if safeMode:
            await message.edit(content=f"Latency: `{int(ping)}ms`")
        if not safeMode:
            embed = discord.Embed()
            embed.add_field(name="Latency", value=f"{int(ping)}ms")
            await message.edit(embed=embed, content="")

    @commands.command()
    async def poll(self, ctx):
        await ctx.message.delete()
        cont = ctx.message.content.split()
        if not safeMode:
            embed = discord.Embed()
            embed.add_field(name="Poll:", value=" ".join(cont[1:]))
            newMessage = await ctx.send(embed=embed)
        if safeMode:
            newMessage = await ctx.send(" ".join(cont[1:]))
        reactions = ['✅', '❌', '🤷']
        for emoji in reactions:
            await newMessage.add_reaction(emoji)

    @commands.command()
    async def btcworth(self, ctx):
        await ctx.message.delete()
        url = "https://www.bitstamp.net/api/ticker/"
        try:
            r = requests.get(url)
            priceFloat = float(json.loads(r.text)["last"])
            if not safeMode:
                embed = discord.Embed()
                embed.add_field(name="BTC Current Value:", value=f"${str(priceFloat)}/BTC")
                await ctx.send(embed=embed)
            if safeMode:
                await ctx.send(f"BTC Current Value: **${str(priceFloat)}**/BTC.")
        except requests.ConnectionError:
            print("Something went wrong fetching BTC value, try again.")

    @commands.command()
    async def curcon(self, ctx):
        await ctx.message.delete()
        args = ctx.message.content.split()
        try:
            value = float(args[1])
            startCur = args[2].upper()
            endCur = args[3].upper()
        except ValueError:
            print(f"Your message || {ctx.message.content} || was not in the proper format.")

        c = CurrencyConverter('http://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip')
        result = c.convert(value, startCur, endCur)
        if not safeMode:
            embed = discord.Embed()
            embed.add_field(name="Currency Converter", value=f"{startCur} to {endCur} convertion", inline=False)
            embed.add_field(name=f"Value in {startCur}", value=f"{value}", inline=False)
            embed.add_field(name=f"Value in {endCur}", value=f"{result}", inline=False)
            await ctx.send(embed=embed)
        if safeMode:
            await ctx.send(f"Conversion of {startCur} to {endCur}; {value} {startCur} is **{result}{endCur}**")


loop = asyncio.get_event_loop()
try:
    for i in range(len(tokens)):
        client = commands.Bot(command_prefix=prefix, help_command=None, self_bot=True)
        client.add_cog(SelfBot(client))

        loop.create_task(client.start(tokens[i], bot=False))
except TypeError:
    print("No token found, please open config.json and fill in at least USER_TOKEN1")

loop.run_forever()
