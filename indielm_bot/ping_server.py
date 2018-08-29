import socket
import discord
import asyncio


def ping(host, port, timeout=10):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(timeout)
    data = "failed"
    try:
        s.sendto(b'\xFE\x01', (host, port))
        data, server = s.recvfrom(1024)
    finally:
        s.close()
        return (data != "failed")

async def check(channel, client, servers, interval=300):
    #init offline_msg's
    offline_msg = {}
    for SERVER, _ in servers:
        offline_msg[SERVER] = None
    while 1:
        for SERVER, OWNER in servers:
            if offline_msg[SERVER]:
                await client.delete_message(offline_msg)
            if ping(socket.gethostbyname(SERVER), 6567):
                offline_msg[SERVER] = await client.send_message(channel,SERVER +' online')
            else:
                offline_msg[SERVER] = await client.send_message(channel,
                           '%s offline, <@%s>' %(SERVER, OWNER.strip()))
        await asyncio.sleep(interval) #interval in seconds!
    
