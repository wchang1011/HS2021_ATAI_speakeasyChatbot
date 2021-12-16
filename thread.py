# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 08:07:40 2021

@author: Wenqing
"""
import threading, requests, json, time
from openNewChatRoom import openNewChatRoom
from agentPerRoom import agentPerRoom
from agent import agent
# url of the speakeasy server
url = "https://speakeasy.ifi.uzh.ch"

# get the api specification
r = requests.get(url + "/client-specs")
spec = json.loads(r.text)

print(json.dumps(spec["paths"]["/api/login"], indent=4))

print(json.dumps(spec["components"]["schemas"]["LoginRequest"], indent=4))

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

agt = agent(username,password,url)


agent_details = agt.login(url).json()
chatroom_messages = {}
while True:
    current_rooms = agt.check_rooms(url,session_token=agent_details["sessionToken"]).json()["rooms"]
    print("--- {} chatrooms available".format(len(current_rooms)))

    for idx, room in enumerate(current_rooms):
        room_id  = room["uid"]
        print("chat room - {}: {}".format(idx, room_id))
        apr = agentPerRoom(username, password, url, room_id)
        # thread = threading.Thread(target=openNewChatRoom, args=([apr,url,room_id,agent_details,chatroom_messages]))
        # thread.start()
        # print(threading.current_thread().name)
        # print(thread.name+' is alive ', thread.isAlive())
        openNewChatRoom(apr, url, room_id, agent_details, chatroom_messages)
            
    time.sleep(3)
    print("")
    #%%
# thread.terminate()