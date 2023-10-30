import nextcord, requests, json, xmltodict
from nextcord.ext import commands, menus
from color_convert import color

class nextPages(menus.ButtonMenu):
    def __init__(self, query, offset):
        super().__init__(disable_buttons_after=True)
        self.query = query
        self.offset = offset

    @nextcord.ui.button(emoji="\N{BLACK LEFT-POINTING DOUBLE TRIANGLE}")
    async def on_thumbs_up(self, button, interaction):
        headers = {'application': 'json'}
        self.offset = 0
        r = requests.get(f'https://api.modrinth.com/v2/search?query={self.query}&offset={self.offset}', headers = headers)
        modrinthData = r.json()
        try:
            color = modrinthData['hits'][0]['color']
        except IndexError:
            pass
        embed = nextcord.Embed(title=f"{modrinthData['total_hits']} search results for {self.query} on Modrinth:", color=color)
        for hit in modrinthData['hits']:
            title = hit['title']
            description = hit['description']
            project_id = hit['project_id']
            downloads = hit['downloads']
            project_type = hit['project_type']
            embed.add_field(name=f'{title} | Downloads: {downloads}', value=f'{description}\n [More Info](https://modrinth.com/project/{project_id}) | {project_type.title()}', inline=False)
        await interaction.response.edit_message(embed=embed)

    @nextcord.ui.button(emoji="\N{BLACK LEFT-POINTING TRIANGLE}")
    async def on_thumbs_down(self, button, interaction):
        headers = {'application': 'json'}
        self.offset -= 10
        if self.offset < 0:
            pass
        else:
            r = requests.get(f'https://api.modrinth.com/v2/search?query={self.query}&offset={self.offset}', headers = headers)
            modrinthData = r.json()
            try:
                color = modrinthData['hits'][0]['color']
            except IndexError:
                pass
            embed = nextcord.Embed(title=f"{modrinthData['total_hits']} search results for {self.query} on Modrinth:", color=color)
            for hit in modrinthData['hits']:
                title = hit['title']
                description = hit['description']
                project_id = hit['project_id']
                downloads = hit['downloads']
                project_type = hit['project_type']
                embed.add_field(name=f'{title} | Downloads: {downloads}', value=f'{description}\n [More Info](https://modrinth.com/project/{project_id}) | {project_type.title()}', inline=False)
            await interaction.response.edit_message(embed=embed)
        
    @nextcord.ui.button(emoji="\N{BLACK RIGHT-POINTING TRIANGLE}")
    async def on_fast_forward(self, button, interaction):
        headers = {'application': 'json'}
        self.offset += 10
        r = requests.get(f'https://api.modrinth.com/v2/search?query={self.query}&offset={self.offset}', headers = headers)
        modrinthData = r.json()
        try:
            color = modrinthData['hits'][0]['color']
        except IndexError:
            pass
        if self.offset > modrinthData['total_hits']:
            await interaction.response.edit_message()
        else:
            embed = nextcord.Embed(title=f"{modrinthData['total_hits']} search results for {self.query} on Modrinth:", color=color)
            for hit in modrinthData['hits']:
                title = hit['title']
                description = hit['description']
                project_id = hit['project_id']
                downloads = hit['downloads']
                project_type = hit['project_type']
                embed.add_field(name=f'{title} | Downloads: {downloads}', value=f'{description}\n [More Info](https://modrinth.com/project/{project_id}) | {project_type.title()}', inline=False)
            await interaction.response.edit_message(embed=embed)

    @nextcord.ui.button(emoji="\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE}")
    async def on_stop(self, button, interaction):
        headers = {'application': 'json'}
        r = requests.get(f'https://api.modrinth.com/v2/search?query={self.query}&offset={self.offset}', headers = headers)
        modrinthData = r.json()
        try:
            color = modrinthData['hits'][0]['color']
        except IndexError:
            pass
        self.offset = modrinthData['total_hits'] - 10
        if self.offset > modrinthData['total_hits']:
            await interaction.response.edit_message()
        else:
            embed = nextcord.Embed(title=f"{modrinthData['total_hits']} search results for {self.query} on Modrinth:", color=color)
            for hit in modrinthData['hits']:
                title = hit['title']
                description = hit['description']
                project_id = hit['project_id']
                downloads = hit['downloads']
                project_type = hit['project_type']
                embed.add_field(name=f'{title} | Downloads: {downloads}', value=f'{description}\n [More Info](https://modrinth.com/project/{project_id}) | {project_type.title()}', inline=False)
            await interaction.response.edit_message(embed=embed)

class botCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command()
    async def ping(self, interaction: nextcord.Interaction):
        latency = round(self.bot.latency * 1000, 0)
        embed = nextcord.Embed(title=f"**Latency:** {latency}MS")
        embed.set_footer(text=f"Contact @bluemethyst for issues or support")
        await interaction.response.send_message(embed=embed)
        
    @nextcord.slash_command(description="Search for a project on Modrinth")
    async def search_modrinth(self, interaction: nextcord.Interaction, query: str):
        headers = {'application': 'json'}
        offset = 0
        r = requests.get(f'https://api.modrinth.com/v2/search?query={query}', headers = headers)
        modrinthData = r.json()
        color = modrinthData['hits'][0]['color']
        embed = nextcord.Embed(title=f"{modrinthData['total_hits']} search results for {query} on Modrinth:", color=color)
        for hit in modrinthData['hits']:
            title = hit['title']
            description = hit['description']
            project_id = hit['project_id']
            downloads = hit['downloads']
            project_type = hit['project_type']
            embed.add_field(name=f'{title} | Downloads: {downloads}', value=f'{description}\n [More Info](https://modrinth.com/project/{project_id}) | {project_type.title()}', inline=False)
        view = nextPages(query=query, offset=offset)
        await interaction.response.send_message(embed=embed, view=view)
        
    @nextcord.slash_command(description="Get information about a project on Modrinth")
    async def mod_info(self, interaction: nextcord.Interaction, mod_id_or_name: str):
        r = requests.get(f'https://api.modrinth.com/v2/project/{mod_id_or_name}')
        modrinthData = r.json()
        title = modrinthData['title']
        description = modrinthData['description']
        project_type = modrinthData['project_type']
        icon = modrinthData['icon_url']
        game_versions = modrinthData['game_versions']
        loaders = modrinthData['loaders']
        loaders_text = ', '. join(loaders)
            
        
        embed = nextcord.Embed(title=f"**{title}**", color=modrinthData['color'], url=f"https://modrinth.com/project/{modrinthData['id']}")
        embed.add_field(name="Description", value=f"{title} is a {project_type} avalible for {game_versions[0]} to {game_versions[-1]} for {loaders_text}.\n{description}")
        embed.set_thumbnail(icon)
        await interaction.response.send_message(embed=embed)
        
    @nextcord.slash_command(description="Get a random project on Modrinth")
    async def random_project(self, interaction: nextcord.Interaction):
        r = requests.get(f'https://api.modrinth.com/v2/projects_random?count=1')
        modrinthData = r.json()
        for modrinthData in modrinthData:
            title = modrinthData['title']
            description = modrinthData['description']
            project_type = modrinthData['project_type']
            icon = modrinthData['icon_url']
            game_versions = modrinthData['game_versions']
            loaders = modrinthData['loaders']
            loaders_text = ', '. join(loaders)
                
            
            embed = nextcord.Embed(title=f"**{title}**", color=modrinthData['color'], url=f"https://modrinth.com/project/{modrinthData['id']}")
            embed.add_field(name="Description", value=f"{title} is a {project_type} avalible for {game_versions[0]} to {game_versions[-1]} for {loaders_text}.\n{description}")
            embed.set_thumbnail(icon)
        await interaction.response.send_message(embed=embed)
    
    
    @nextcord.slash_command(description="Get information on the latest Minecraft version")
    async def mc_version(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title="Latest Minecraft Version", color=3966246)
        r = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest_v2.json")
        mc = r.json()
        mc_release = mc['latest']['release']
        mc_release = mc_release.replace('.', '-')
        mc_snapshot = mc['latest']['snapshot']
        embed.add_field(name=f"Latest Release: {mc['latest']['release']}", value=f"More information [here](https://www.minecraft.net/en-us/article/minecraft-java-edition-{mc_release})")
        embed.add_field(name=f"Latest Snapshot: {mc['latest']['snapshot']}", value=f"More information [here](https://www.minecraft.net/en-us/article/minecraft-snapshot-{mc_snapshot})")
        embed.set_thumbnail(url="https://raw.githubusercontent.com/Bluemethyst/ModrinthDiscordBot/main/assets/mclogo.png")
        await interaction.response.send_message(embed=embed)
        
    @nextcord.slash_command(description="Get information on the latest FabricMC version")
    async def fabric_version(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title="Latest FabricMC Version", color=14405812)
        r = requests.get("https://meta.fabricmc.net/v2/versions/loader")
        fabric = r.json()
        embed.set_thumbnail(url="https://raw.githubusercontent.com/Bluemethyst/ModrinthDiscordBot/main/assets/fabriclogo.png")
        embed.add_field(name=f"{fabric[0]['version']}", value="Download [here](https://fabricmc.net/use/installer/)")
        await interaction.response.send_message(embed=embed)
        
    @nextcord.slash_command(description="Get information on the latest NeoForge version")
    async def neoforge_version(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title="Latest NeoForge Version", color=14119983)
        r = requests.get("https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml")
        xml_data = r.text
        data_dict = xmltodict.parse(xml_data)
        neoforge_json = json.dumps(data_dict, indent=4)
        neoforge_data = json.loads(neoforge_json)
        embed.set_thumbnail(url="https://raw.githubusercontent.com/Bluemethyst/ModrinthDiscordBot/main/assets/neoforgelogo.png")
        embed.add_field(name=f"{neoforge_data['metadata']['versioning']['latest']}", value=f"Download [here](https://neoforged.net/)")
        await interaction.response.send_message(embed=embed)