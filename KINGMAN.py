import discord
import json
from discord.ext import commands
###########
#Replit   #
###########
from flask import Flask
from threading import Thread

app=Flask("")

@app.route("/")
def index():
    return "<h1>KINGMAN4HACK</h1>"

Thread(target=app.run,args=("0.0.0.0",8080)).start()
###########
#KeepAlive#
###########
client = commands.Bot(command_prefix=".",intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f"KINGMAN REACTION Loggin in {client.user}")

#####################
#  Reaction Event   #
#####################
#RoleAdd
@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:
        with open('reaction.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)


#RoleRemove
@client.event
async def on_raw_reaction_remove(payload):

    with open('reaction.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.name:
                role = discord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])


                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)


@client.command()
async def hello(ctx):
    await ctx.channel.send(f"Hellow! {ctx.author.mention}")



@client.command()
@commands.has_permissions(administrator=True, manage_roles=True)
async def kmrole(ctx, emoji, role: discord.Role, *, message):
    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reaction.json') as json_file:
        data = json.load(json_file)
        new_react_role = {'role_name': role.name,
        'role_id': role.id,
        'emoji': emoji,
        'message_id': msg.id}
        data.append(new_react_role)
    with open('reaction.json', 'w') as f:
        json.dump(data, f, indent=4)

client.run("")
