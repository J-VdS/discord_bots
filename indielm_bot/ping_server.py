import socket
import discord
import asyncio


def ping(host, port, timeout=5):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(timeout) #after 5 sec raise time out message
    data = "failed"
    try:
        s.sendto(b'\xFE\x01', (host, port)) #send -2,1
        data, server = s.recvfrom(1024)
        #print(data)
    finally:
        s.close()
        return (data != "failed")

async def delete(client, msg):
    if msg:
        await client.delete_message(msg)

async def check(channel, client, servers, INTERVAL=300):
    #init offline_msg's
    msg = {SERVER:None for SERVER, _, _ in servers} #make empty directory
    count = {SERVER:1 for SERVER, _, _ in servers}  #make empty counter
    interval = INTERVAL
    print('-- Ping sequence started --\n\n')
    while 1:
        for SERVER, OWNER, SERVERN in servers:
            ping
            if ping(socket.gethostbyname(SERVER), 6567): 
                if count[SERVER] != 0:
                    count[SERVER] = 0 #reset offline counter
                    if count.values == len(count)*[0]:
                        #if all the servers are online change inteval
                        interval= INTERVAL
                    await delete(client, msg[SERVER]) #deletes a msg if available
                    msg[SERVER] = await client.send_message(channel, SERVERN +' went online')
            else:
                #server offline -> ping every 30 seconds, 4 times in row
                count[SERVER] += 1
                interval = 30 if (count[SERVER]<5) else INTERVAL 
                if count[SERVER] == 4: #after 4 failed pings send offline message
                    await delete(client, msg[SERVER])
                    msg[SERVER] = await client.send_message(channel,
                       '%s offline, <@%s>' %(SERVERN, OWNER.strip()))
        await asyncio.sleep(interval) #interval in seconds!
    
