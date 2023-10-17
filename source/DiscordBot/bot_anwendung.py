import multiprocessing
from multiprocessing import Process

import discord

from DiscordBot.dc_bot import DiscordBot


def run_bot(conn2):
    intents = discord.Intents.all()
    dcBot = DiscordBot(intents=intents)
    conn2.send(1)
    dcBot.run("MTE0NTYxODMzNjQzNzI0MzkxNA.GvB5Bt.RdqcBQzEuuUEf879PjFIg7iEqFwzWaecZ6ndfA")




if __name__ == "__main__":
    conn1, conn2 = multiprocessing.Pipe()
    p = Process(target=run_bot, args=(conn2,))
    p.start()
    x = conn1.recv()
    #dcBot.sende_nachricht("BAUM")
