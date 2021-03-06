import re

import aiohttp
import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu

old_invite = None


class KaoTools(commands.Cog):
    """Random tools for kaogurai that fit nowhere else."""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())
        # command remove logic - https://github.com/maxbooiii/maxcogs/blob/master/ping/ping.py#L28
        global old_invite
        if old_invite:
            try:
                self.bot.remove_command("invite")
            except:
                pass
            self.bot.add_command(old_invite)

    async def search_youtube(self, query):
        """Make a Get call to FAKE youtube data api (HEHE)."""
        params = {"identifier": "ytsearch:" + query}
        headers = {"Authorization": "youshallnotpass", "Accept": "application/json"}
        async with self.session.get(
            "http://localhost:2333/loadtracks", params=params, headers=headers
        ) as request:
            if request.status == 200:
                response = await request.json()
                try:
                    return response["tracks"]
                except:
                    return
            else:
                return

    @commands.Cog.listener()
    async def on_message_without_command(self, message: discord.Message):
        if message.author.bot:
            return
        if not message.guild:
            return
        if not message.channel.permissions_for(message.guild.me).send_messages:
            return
        if await self.bot.allowed_by_whitelist_blacklist(who=message.author) is False:
            return
        if not re.compile(rf"^<@!?{self.bot.user.id}>$").match(message.content):
            return
        prefixes = await self.bot.get_prefix(message.channel)
        prefixes.remove(f"<@!{self.bot.user.id}> ")
        sorted_prefixes = sorted(prefixes, key=len)
        if len(sorted_prefixes) > 500:
            return
        embed = discord.Embed(
            colour=await self.bot.get_embed_colour(message.channel),
            description=f"""
        **Hey there!** <a:bounce:778449468717531166>
        My prefixes in this server are {humanize_list(prefixes)}
        You can type `{sorted_prefixes[0]}help` to view all commands!
        Need some help? Join my [support server!](https://discord.gg/p6ehU9qhg8)
        Looking to invite me? [Click here!](https://discord.com/oauth2/authorize?client_id={message.guild.me.id}&permissions=6441922047&scope=bot+applications.commands)
        """,
        )
        await message.channel.send(embed=embed)

    @commands.command()
    async def debugerror(self, ctx, error_code: str):
        """Fetches error code information from hastebin."""
        async with self.session.get(
            f"https://haste.kaogurai.xyz/raw/{error_code}"
        ) as request:
            embed = discord.Embed(color=await ctx.embed_color())
            embed.description = f"```yaml\n{await request.text()}```"
            embed.set_footer(text=f"Error Code: {error_code}")
            await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def asia(self, ctx):
        """Emo kids lover"""
        await ctx.send(
            "asia is the best person on this earth and loves videos of emo kids dancing"
        )
        await ctx.send(
            "https://cdn.discordapp.com/attachments/768663090337677315/795133511673053225/emokidsyummy.mp4"
        )

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(hidden=True)
    async def maddie(self, ctx):
        """Cool Cat :)"""
        embed = discord.Embed(
            description="maddie is a cool cat + is emotionally attached to this cat’s birthday party :revolving_hearts::revolving_hearts::revolving_hearts::revolving_hearts:",
            color=11985904,
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/768663090337677315/796118254128332820/image0.jpg"
        )
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def oofchair(self, ctx):
        """Cool bot dev"""
        await ctx.send(
            "oof is p cool :) he's also a bot developer! check out his bot here: http://pwnbot.xyz/"
        )

    @commands.command(aliases=["yt"])
    async def youtube(self, ctx, *, video: str):
        """
        Search for a youtube video.
        Inspired by Aikaterna's YouTube cog
        """
        videos = await self.search_youtube(video)
        if videos:
            await ctx.send(videos[0]["info"]["uri"])
        else:
            await ctx.send("Nothing found.")

    @commands.command(aliases=["yts", "ytsearch"])
    async def youtubesearch(self, ctx, *, video: str):
        """
        Search for a youtube video with a menu of results.
        Inspired by Aikaterna's YouTube cog
        """
        results = await self.search_youtube(video)
        if results:
            videos = []
            for obj in results:
                videos.append(obj["info"]["uri"])
            await menu(ctx, videos, DEFAULT_CONTROLS, timeout=60)
        else:
            await ctx.send("Nothing found.")

    @commands.command()
    async def poll(self, ctx, *, question: str):
        """Create a simple poll."""
        if len(question) > 2000:
            return
        if (
            not ctx.channel.permissions_for(ctx.me).add_reactions
            and not ctx.channel.permissions_for(ctx.me).use_external_emojis
        ):
            await ctx.send(
                "Please give me permissions to react, and react with external emojis."
            )
            return
        message = await ctx.send(f"**{ctx.author} asks:** " + question)
        await message.add_reaction("👍")
        await message.add_reaction("<:idk:838887174345588796")
        await message.add_reaction("👎")

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(aliases=["support", "inv"])
    async def invite(self, ctx, bot: discord.User = None):
        """Invite me or another bot!"""
        if bot is None:
            embed = discord.Embed(
                title="Thanks for using me!",
                color=await ctx.embed_color(),
                url="https://kaogurai.xyz",
            )
            embed.set_thumbnail(url=ctx.me.avatar_url)
            embed.add_field(
                name="Bot Invite",
                value=(
                    f"[Click Here](https://discord.com/oauth2/authorize?client_id={ctx.me.id}&permissions=6441922047&scope=bot+applications.commands)"
                ),
                inline=True,
            )
            embed.add_field(
                name="Support Server",
                value="[Click Here](https://discord.gg/p6ehU9qhg8)",
                inline=True,
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Click here to invite that bot!",
                color=await ctx.embed_color(),
                url=f"https://discord.com/oauth2/authorize?client_id={bot.id}&permissions=6441922047&scope=bot+applications.commands",
            )
            await ctx.send(embed=embed)


def setup(bot):
    kaotools = KaoTools(bot)
    global old_invite
    old_invite = bot.get_command("invite")
    if old_invite:
        bot.remove_command(old_invite.name)
    bot.add_cog(kaotools)
