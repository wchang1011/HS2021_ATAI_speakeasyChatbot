# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 08:10:38 2021

@author: Wenqing
"""
from main import mainPro
from datas import graph,WDT,WD,images

def openNewChatRoom(apr, url, room_id,agent_details,chatroom_messages):
    
    

    new_room_state = apr.check_room_state(url,room_id=room_id, since=0, session_token=agent_details["sessionToken"]).json()
    new_messages = new_room_state["messages"] ##### actually the input of user
    print("found {} messages".format(len(new_messages)))
    
    if room_id not in chatroom_messages.keys():
        chatroom_messages[room_id] = []

    if len(chatroom_messages[room_id]) != len(new_messages):
        #### for each user input (as in---message)
        for message in new_messages:
            if message["ordinal"] >= len(chatroom_messages[room_id]) and message["session"] != agent_details["sessionId"]:
                #### parse the message
                mP = mainPro(message["message"])
                response = mP.parseMsg(graph, WDT,WD, images)
                apr.post_message(url,room_id=room_id, session_token=agent_details["sessionToken"], message=response)
                                 
    ####### here the post_message(message=response) is possible interface with KG etc.
    chatroom_messages[room_id] = new_messages
