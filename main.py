from nextcord.ext import commands
from bot_commands import botCommands

bot = commands.Bot()
bot.add_cog(botCommands(bot))

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    
bot.run('TOKEN-HERE')
