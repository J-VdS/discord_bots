# discord_bots (PYTHON)
#### Python version 3.6 and higher

## used lib
  * discord.py (not the rewrite)
    https://github.com/Rapptz/discord.py

### Bots I made and some explanation
  * indielm_bot.py:
    * If somebody wrote a message containing 'router' or 'splitter' the bot reacts with a 'router' emoji.
    * The server owner can use the !clean command to delete some messages in a channel.
      These feature will only work if the second line of your token.txt file contains your discord id.
      You could get this using the !my_id command.
    * The bot will automaticly ping mindustry servers every 5 min. This will only work if your third line of
      the token.txt contains the name of a server. In this server the bot will send server messages. (online or offline)
  * connect4 - bot:
    * This bot makes it possible to play connect4 in python.
    * commands: join, move <num>
    * The use this bot, you need to download the PIL python library on your computer. 
      
       
##### Ps: You will need to add token.txt in the same directory as your bot. The firs line needs to contain your TOKEN
   
   
