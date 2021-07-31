import re
import discord
from bot import Bot
from hidden import Hidden

bot = Bot(Hidden().token())
client = bot.connect()

class User_information:

    def __init__(self, ctx, user_reference) -> None:
        self.ctx = ctx
        self._user_reference = user_reference


    def avatar(self, user) -> discord.Embed:

        avatar = user.avatar_url

        emb_avatar = discord.Embed(
            title='Avatar URL',
            url=avatar,
            color=0x690FC3
        )

        user_url = f'https://discord.com/users/{user.id}'

        emb_avatar.set_author(name=user.display_name, url=user_url,icon_url=avatar)
        emb_avatar.set_image(url=avatar)

        return emb_avatar


    @property
    def user_id(self) -> str:
        user_id = ''

        if not self._user_reference.isnumeric():
            
            if self._user_reference.startswith('<@!'):
                user_id = re.findall('[0-9]*',self._user_reference)
                for item in user_id:
                    if item != '':
                        user_id = item

            else:
                for member in self.ctx.guild.members:
                    if self._user_reference.lower() == member.name.lower():
                        user_id = member.id
                        break

        if user_id != '':
            return user_id
        else: 
            return self._user_reference