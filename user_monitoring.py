

import discord
from discord.ext import tasks
import requests

import keys

# https://discordpy.readthedocs.io/en/latest/api.html#event-reference


class Monitor:
    channel = None
    self_mute = None
    self_deaf = None


def voice_status(mute, deaf):
    str_status = "{}{}".format("🔇" if mute else "🔈 ",
                               "❌" if deaf else "🎧")
    return str_status


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.my_monitor = Monitor()
        self.printer.start()

    async def on_ready(self):
        print('Logged in as "{}" with id "{}"'.format(self.user.name, self.user.id))

        for guild in client.guilds:
            print("-{}[{}]".format(guild.name, guild.id))
            channel_list = []
            for channel in guild.channels:
                if isinstance(channel, discord.VoiceChannel):
                    channel_list.append(channel.name)

            print("--{}".format(channel_list))

    async def on_voice_state_update(self, member, before, after):

        if after.channel is None:
            if before.channel.guild.id not in keys.MyDiscords.target_guild:
                return
        else:
            if after.channel.guild.id not in keys.MyDiscords.target_guild:
                return

        if member == self.user:
            name = "You"
        else:
            name = member.name

        avatar_url = str(member.avatar_url).replace("1024", "128")
        avatar_id = "avatars/{}.jpg".format(member.avatar)

        r = requests.get(avatar_url, allow_redirects=True)
        open(avatar_id, 'wb').write(r.content)

        if member == self.user and self.my_monitor.channel != after.channel:
            self.my_monitor.channel = after.channel
            self.user_status()

        if before.channel is not after.channel:
            if after.channel is self.my_monitor.channel:
                if member.id in keys.MyDiscords.intruders:
                    print("MAJOR INTRUDER")
                else:
                    print("Intruder")
            if after.channel is None:
                print('{} just quit "{}" of "{}" guild'.format(name, before.channel.name, before.channel.guild.name))
            else:
                print('{} just enter in "{}" of "{}" guild'.format(name, after.channel.name, after.channel.guild.name))

        if (before.self_deaf is not after.self_deaf) or (before.self_mute is not after.self_mute):
            if member == self.user:
                self.my_monitor.self_deaf = after.self_deaf
                self.my_monitor.self_mute = after.self_mute

            print("{} - {}".format(name, voice_status(after.self_mute, after.self_deaf)))

    @tasks.loop(seconds=10.0)
    async def printer(self):

        # Wait to be connected
        if self.user and self.my_monitor.channel:
            self.user_status()

    def user_status(self):

        if self.my_monitor.channel is None:
            print('You are not in a voice channel anymore')
        else:
            print("You are on channel: {} with\t{}".format(self.my_monitor.channel.name,
                                                           voice_status(self.my_monitor.self_mute,
                                                                        self.my_monitor.self_deaf)))


client = MyClient()
key = keys.Mykeys().perso
client.run(key[0], bot=key[1])
