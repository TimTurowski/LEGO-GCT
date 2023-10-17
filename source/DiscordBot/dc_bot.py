import discord

class DiscordBot(discord.Client) :


    async def on_ready(self):
        print("DiscordBot gestartet")

    async def on_message(self, message):

        if message.author == self.user:
            return
        print(message.content)

        if message.content.startswith("!anzahlSets"):
            await message.channel.send("Tja, das wüsstest du wohl gerne")

        if message.content.startswith("!test"):
            await self.sende_nachricht("message")


    async def sende_nachricht(self, message):
        print("sende_nachricht aufgerufen")
        channel = self.get_channel(1145617125734617132)
        await channel.send(message)

