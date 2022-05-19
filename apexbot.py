from os import link
from turtle import title
import discord
import random
import requests

TOKEN = 'OTI5NzQ4NDkzMTM5MDcxMDI2.Ydr1wg.-eF7-FLyO1ly5wVf3mRX5qXtUpQ'

client = discord.Client()

#global library (UNUSED)
#response_global_apex_data = requests.get("https://api.mozambiquehe.re/bridge?version=5&platform=PC&player=HeyImLifeline&auth="
                #"{YOURAPIKEY}".format(YOURAPIKEY="rvkMv29kAQy5dpVw5Nrb"))
#global_apex_data = response_global_apex_data.json()

#Client event to signify the bot being online (displays in terminal)
@client.event 
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#Speech Commands
@client.event
async def on_message(message):

    username = str(message.author).split('#')[0] #Discord username of the person sending the message
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return
        
    #crafting library
    crafting_response = requests.get("https://api.mozambiquehe.re/crafting?&auth={YOURAPIKEY}".format(YOURAPIKEY="rvkMv29kAQy5dpVw5Nrb"))
    global_crafting_data = crafting_response.json()
    #Daily rotation is in index 0
    crafting_today = global_crafting_data[0]["bundleContent"]
    #Weekly rotation in in index 1
    crafting_weekly = global_crafting_data[1]["bundleContent"]

    #map library 
    map_response = requests.get("https://api.mozambiquehe.re/maprotation?version=5&auth={YOURAPIKEY}".format(YOURAPIKEY="rvkMv29kAQy5dpVw5Nrb",))
    global_map_data = map_response.json()

    #battle royale maps
    current_map = global_map_data["battle_royale"]["current"]["map"]
    current_map_timer = global_map_data["battle_royale"]["current"]["remainingTimer"]

    #arena maps
    current_map_arena = global_map_data["arenas"]["current"]["map"]
    current_map_timer_arena = global_map_data["arenas"]["current"]["remainingTimer"]

    #news and events
    news_response = requests.get("https://api.mozambiquehe.re/news?lang=en-us&auth={YOURAPIKEY}".format(YOURAPIKEY="rvkMv29kAQy5dpVw5Nrb"))
    news_data = news_response.json()
    news_count = 0 #int variable to cycle news posts up to the 3rd latest post 

    #if message.channel.name == 'generally-home' or 'bot-home': ---> this was to specify certain channels, probably not needed

    if user_message.lower() == '!playapex': #Question asking to play apex or not
        number = random.randrange(1, 100)
        if number <= 50:
            await message.channel.send('You should not play Apex.')
            return
        if number > 50:
            await message.channel.send('You should play Apex')
            return


    if user_message.lower() == '!craftingdaily': #Displays daily crafting materials
        #names of assets, item types and the rarity
        #daily_item_one_asset = crafting_today[0]["itemType"]["asset"]
        #daily_item_two_asset = crafting_today[1]["itemType"]["asset"]

        daily_item_one_name = crafting_today[0]["itemType"]["name"]
        daily_item_two_name = crafting_today[1]["itemType"]["name"]

        daily_item_one_rarity = crafting_today[0]["itemType"]["rarity"]
        daily_item_two_rarity = crafting_today[1]["itemType"]["rarity"]

        daily_item_one_price = crafting_today[0]["cost"]
        daily_item_two_price = crafting_today[1]["cost"]

        #name conversion for item names
        daily_craft = daily_item_one_name.replace("_", " ") #replace with helper function
        daily_craft2 = daily_item_two_name.replace("_", " ")
        d_1 = daily_item_one_rarity + " " + daily_craft.title()
        d_2 = daily_item_two_rarity + " " + daily_craft2.title()


        await message.channel.send("The current crafting rotation today consists of:\n - {d1} worth {c1} replicator points\n - {d2} worth {c2} replicator points".format(
                                        d1 = d_1, d2 = d_2, c1 = daily_item_one_price, c2 = daily_item_two_price))
        return


    if user_message.lower() == '!craftingweekly': #Displays weekly crafting materials 

        #weekly_item_one_asset = crafting_weekly[0]["itemType"]["asset"]
        #weekly_item_two_asset = crafting_weekly[1]["itemType"]["asset"]

        weekly_item_one_name = crafting_weekly[0]["itemType"]["name"]
        weekly_item_two_name = crafting_weekly[1]["itemType"]["name"]

        weekly_item_one_rarity = crafting_weekly[0]["itemType"]["rarity"]
        weekly_item_two_rarity = crafting_weekly[1]["itemType"]["rarity"]

        weekly_item_one_price = crafting_weekly[0]["cost"]
        weekly_item_two_price = crafting_weekly[1]["cost"]

        #name conversion for item names
        weekly_craft = weekly_item_one_name.replace("_", " ") #replace with helper function
        weekly_craft2 = weekly_item_two_name.replace("_", " ")
        w_1 = weekly_item_one_rarity + " " + weekly_craft.title()
        w_2 = weekly_item_two_rarity + " " + weekly_craft2.title()

        await message.channel.send("The current crafting rotation for the week consists of:\n - {w1} worth {c1} replicator points\n - {w2} worth {c2} replicator points".format(
                                        w1 = w_1, w2 = w_2, c1 = weekly_item_one_price, c2 = weekly_item_two_price))
        return
    

    if user_message.lower() == "!brmap": #displays the current map in batte royale
        await message.channel.send("The current map is {map} with {time} left.".format(map = current_map, time = current_map_timer))
        return 
        

    if user_message.lower() == "!arenamap": #displays the current map in arenas
        await message.channel.send("The current map is {map} with {time} left.".format(map = current_map_arena, time = current_map_timer_arena))
        return 

    if user_message.lower() == "!news": #links to a news site for apex legends
        if news_count == 3:
            news_count = 0
        current_news = news_data[news_count]
        await message.channel.send("{link}".format(link = current_news["link"]))
        news_count += 1
        return

    if user_message.lower() == "!help": #test comment

        await message.channel.send("The list of commands are:\n - !playapex\n - !craftingdaily\n - !craftingweekly\n - !brmap\n - !arenamap\n - !news")
        return

client.run(TOKEN)