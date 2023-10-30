import requests, nextcord
from nextcord.ext import commands
from bot_commands import botCommands

bot = commands.Bot()
bot.add_cog(botCommands(bot))


headers = {
    'application': 'json',
    'query': 'gravestone'
}
r = requests.get('https://api.modrinth.com/v2/search', headers = headers)
modrinthData = r.json()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    
bot.run('TOKEN-HERE')
