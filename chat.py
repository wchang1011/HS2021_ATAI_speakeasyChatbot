# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 08:26:52 2021

@author: Wenqing
"""

# import packages
import requests, json, time
from agent import agent
from main import mainPro
from datas import graph,WDT,WD,images
# from IPython.display import Javascript

#%%

# url of the speakeasy server
url = "https://speakeasy.ifi.uzh.ch"

# get the api specification
r = requests.get(url + "/client-specs")
spec = json.loads(r.text)

print(json.dumps(spec["paths"]["/api/login"], indent=4))

print(json.dumps(spec["components"]["schemas"]["LoginRequest"], indent=4))

#%%
# Data to be written
dictionary ={
    "agent2": {
        "username": 'bot_922',
        "password": 'nMFDcN2TY1'
    } 
}
  
# Serializing json 
json_object = json.dumps(dictionary, indent = 4)
  
# Writing to sample.json
with open("Dataset\\credentials.json", "w") as outfile:
    outfile.write(json_object)

# load credentials from a json file
with open("Dataset\\credentials.json", "r") as f:
    credentials = json.load(f)
username = credentials["agent2"]["username"]
password = credentials["agent2"]["password"]
print(username)
#%%
agt = agent(username,password,url)

agent_details = agt.login(url).json()
print("--- agent details:")
print(json.dumps(agent_details, indent=4))

chatroom_messages = {}
while True:
    current_rooms = agt.check_rooms(url,session_token=agent_details["sessionToken"]).json()["rooms"]
    print("--- {} chatrooms available".format(len(current_rooms)))

    for idx, room in enumerate(current_rooms):
        room_id = room["uid"]
        print("chat room - {}: {}".format(idx, room_id))

        new_room_state = agt.check_room_state(url,room_id=room_id, since=0, session_token=agent_details["sessionToken"]).json()
        new_messages = new_room_state["messages"] ##### actually the input of user
        print("found {} messages".format(len(new_messages)))
        
        if room_id not in chatroom_messages.keys():
            chatroom_messages[room_id] = []

        if len(chatroom_messages[room_id]) != len(new_messages):
            #### for each user input (as in---message)
            for message in new_messages:
                if message["ordinal"] >= len(chatroom_messages[room_id]) and message["session"] != agent_details["sessionId"]:
                    #### parse the message
                    try:
                        response = "Hey Sweetie~~ Got your message \"{}\" at {}.".format(message["message"], time.strftime("%H:%M:%S, %d-%m-%Y", time.localtime()))
                        agt.post_message(url,room_id=room_id, session_token=agent_details["sessionToken"], message=response)
                        
                        mP = mainPro(message["message"])
                        response = mP.parseMsg(graph, WDT,WD, images)
                        agt.post_message(url,room_id=room_id, session_token=agent_details["sessionToken"], message=response)
                        
                    except:
                        response = 'Sorry, there seems no answer to your question.'
                        agt.post_message(url,room_id=room_id, session_token=agent_details["sessionToken"], message=response)
                        
                    #### pass in the response
                    # imgids = ['image:1298/rm4086331136', 'image:0792/rm4013116160', 'image:2721/rm4089497088', 'image:0466/rm4039165440', 'image:3530/rm3376092928', 'image:1829/rm3928251904', 'image:3369/rm3957474816', 'image:0885/rm2738554880']
                    # response = "Hi, this is the image you requested.{}".format(imgids)
                    # response = 'imdb:nm0000229'
                                     
        ####### here the post_message(message=response) is possible interface with KG etc.
        chatroom_messages[room_id] = new_messages

    time.sleep(3)
    print("")
#%%
print("--- log out")
r = agt.logout(url,session_token=agent_details["sessionToken"])
print(r.json())