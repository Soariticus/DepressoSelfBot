import asyncio
import discord
from discord.ext import commands
import json

try:
    with open("config.json", "r") as file:
        pass
except FileNotFoundError:
    x = {
      "USER_TOKEN1": "YOUR TOKEN HERE",
      "USER_TOKEN2": "OPTIONAL SECOND TOKEN",
      "SAFE_MODE": False,
      "PREFIX": "dep.",
      "UNUSED3": None,
      "UNUSED4": None,
      "UNUSED5": None
    }

    with open("config.json", "w") as file:
        json.dump(x, file, indent=4)



#with open("config.json", "r") as configFile:
#    configData = json.load(configFile)
#    token = configData["USER_TOKENS"]


but = discord.Client()
started = False
global prefix, invite
prefix = "dep."
invite = "https://discord.gg/wCfUgSK"

tokens = ["NjM4NDk0ODUwODYxMzY3Mjk2.XqcWrQ.J0IAzqU_lyClCrdW1282JyO4bRo",
          "Njc2MjI1MDcyMjgwNzY0NDUw.Xqyzaw.0wcaHbmdy7emnOE2t4z6OyxGt2I"]

class SelfBot(commands.Cog):
    def __init__(self, client):
        global afk, soar, annoyUsers, but, started

        annoyUsers = []
        but = client
        self.client = client
        if not started:
            print("|||||||||||||||||||||||||||||||||||||||||||||||||||||")
            print("")
            print("         DepressoSelfBot by Soariticus#0666          ")
            print("")
            print("|||||||||||||||||||||||||||||||||||||||||||||||||||||")
            started = True

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

loop = asyncio.get_event_loop()

for i in range(len(tokens)):
    client = commands.Bot(command_prefix="dep.", help_command=None, self_bot=True)
    client.add_cog(SelfBot(client))

    loop.create_task(client.start(tokens[i], bot=False))

loop.run_forever()







