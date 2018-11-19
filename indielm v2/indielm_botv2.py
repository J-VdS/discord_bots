import discord
from discord.ext import commands

import asyncio
import time

import ping_serverv2

#read data from file:
with open('info.txt', 'r') as infile:
    data = [i.strip() for i in infile.readlines()]
    TOKEN = data[0]
    OWNERID = data[1]
    SERVERID = data[2] #first number in url

#read data from server file:
with open('servers.txt', 'r') as infile:
    #first line of txt --> channel name
    #backup ip,hostip(visible)
    SERVERDATA = [i.strip().split(',') for i in infile.readlines()]
    print(SERVERDATA)
    
#---------------------------------------------------------    

client = commands.Bot(command_prefix = '!')

#server info getting from on_ready
si = {}

#backgroundtask
async def auto_ping():
    '''check if server online'''    
    await client.wait_until_ready()
    await asyncio.sleep(10) #run after on_ready function is done

    
    #init msg dictionarry:
    msg = {i[2]:[None,0] for i in SERVERDATA[1:]}
    botchannel = si['CHANNELS'][SERVERDATA[0][0]]
    async for i in client.logs_from(botchannel):
        for key in msg:
            if msg[key][0] != None:
                continue #skip
            elif key in i.content.split(' '):
                msg[key][0] = i
    while not client.is_closed:
        try:
            for server in SERVERDATA[1:]:
                #check if server online
                if ':' in server[2]:
                    port = int(server[2].split(':')[1])
                    online = ping_serverv2.check_online(server[0], port)
                    del port
                else:
                    online = ping_serverv2.check_online(server[0])

                #processing
                if not online and msg[server[2]][1]<5 :
                    #counter
                    msg[server[2]][1] += 1
                elif not online and msg[server[2]][1] == 5:
                    msg[server[2]][1] = 6 
                    #send/modify last message after 5/6 failed pings
                    text = f'{server[2]} went offline, <@{server[1]}>'
                    if msg[server[2]][0]:
                        msg[server[2]][0] = await client.edit_message(
                            msg[server[2]][0], text)
                    else:
                        msg[server[2]][0] = await client.send_message(
                            botchannel, text)
                    print(f'{time.asctime()}//{server[2]} is offline')
                elif online and msg[server[2]][1] != -1:
                    msg[server[2]][1] = -1
                    text = f'{server[2]} is online'
                    if msg[server[2]][0]:
                        msg[server[2]][0] = await client.edit_message(
                            msg[server[2]][0], text)
                    else:
                        msg[server[2]][0] = await client.send_message(
                            botchannel, text)
                    print(f'{time.asctime()}//{server[2]} is online') 
                
                    
        except:
            print('restarting or an error appeared')
        finally:
            await asyncio.sleep(5)

            
#--------------------------------------------------       


@client.event
async def on_ready():
    #server id
    print('\ngetting server info:')
    si['SERVER'] = client.get_server(SERVERID)

    #router emoji
    si['ROUTER'] = discord.utils.get(client.get_all_emojis(), name='router')
    si['CHANNELS'] = {x.name:x for x in client.get_all_channels()}

    print(si)
    print('bot is ready\n')
    

@client.event
async def on_message(msg):
    content = msg.content.lower().strip(' ')
    if 'rout' in content or 'splitter' in content:
        await client.add_reaction(msg, si['ROUTER'])
            
    await client.process_commands(msg) #exec commands


@client.command(pass_context=True,
                description='''[host] checks if server is online\n
                Use f.e. !ping mindustry.indielm.com:9001 for custom port setup''')
async def ping(ctx, host='mindustry.indielm.com'):
    if ':' in host:
        nhost, port = host.split(':')
    else:
        nhost, port = host, '6567'
    response = ping_serverv2.ping(nhost, int(port))
    embed = ping_serverv2.make_msg(host, response)
    await client.send_message(ctx.message.channel, embed=embed)

    '''
    msg = 'online' if ping_serverv2.check_online(host) else 'offline/failed'
    await client.say(f'{host} {msg}')
    '''

client.loop.create_task(auto_ping())
client.run(TOKEN)
