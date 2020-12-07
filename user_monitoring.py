

import discord
from discord.ext import tasks

import keys

# https://discordpy.readthedocs.io/en/latest/api.html#event-reference


class Monitor:
    channel = None
    self_mute = None
    self_deaf = None


def voice_status(mute, deaf):
    str_status = "{}{}".format("🔇\t" if mute else "🔈\t\t",
                               "❌" if deaf else "🎧")
    return str_status


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.my_monitor = Monitor()
        self.printer.start()

    async def on_ready(self):
        print('Logged in as {} with id {}'.format(self.user.name, self.user.id))

        for guild in client.guilds:
            print("-{}".format(guild.name))
            channel_list = []
            for channel in guild.channels:
                if isinstance(channel, discord.VoiceChannel):
                    channel_list.append(channel.name)

            print("--{}".format(channel_list))

    async def on_voice_state_update(self, member, before, after):

        if member == self.user:
            name = "you"
        else:
            name = member.name

        if member == self.user and self.my_monitor.channel != after.channel:
            self.my_monitor.channel = after.channel
            self.user_status()

        if before.channel is not after.channel:
            if after.channel is self.my_monitor.channel:
                print("INTRUDER")

            print("{} just enter in {} of {} guild".format(name, after.channel.name, after.channel.guild.name))

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
        print("You are on channel: {} with\t{}".format(self.my_monitor.channel.name,
                                                       voice_status(self.my_monitor.self_mute,
                                                                    self.my_monitor.self_deaf)))


client = MyClient()
key = keys.Mykeys().perso
client.run(key[0], bot=key[1])
