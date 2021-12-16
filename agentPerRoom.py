# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 09:05:18 2021

@author: Wenqing
"""
import requests

class agentPerRoom:
    def __init__(self,username,password,url,room_id):
        self.username = username
        self.password = password
        self.url = url
        self.room_id = room_id

    # user login
    def login(self,url):
        return requests.post(url=url + "/api/login", json={"username": self.username, "password": self.password})

    # check details of the current user
    def current(self,url,session_token: str):
        return requests.get(url=url + "/api/user/current", params={"session": session_token})

    # user logout
    def logout(self,url,session_token: str):
        return requests.get(url=url + "/api/logout", params={"session": session_token})

    # check the state of a chat room
    ##### this method get the messages in the room as ["messages"]
    def check_room_state(self,url,room_id, since: int, session_token: str):
        return requests.get(url=url + "/api/room/{}/{}".format(room_id, since), params={"roomId": room_id, "since": since, "session": session_token})

    # post a message to a chat room
    def post_message(self,url,room_id, session_token: str, message: str):
        return requests.post(url=url + "/api/room/{}".format(room_id), params={"roomId": room_id, "session": session_token}, data=message)
