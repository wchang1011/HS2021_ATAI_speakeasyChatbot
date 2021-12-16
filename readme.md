# This is the 2021 Fall ATAI chatbot project of bot_922.
-*- coding: utf-8 -*-
"""
Created on Wed Dec 15 12:11:51 2021

@author: Wenqing
"""


First, to run the project, one should follow the following steps.

1. Import the data. 
By importing data, you should run the datas.py file cell by cell and also run the crowd.py file.
The dataset files are in the Dataset folder. The datas.py file imports all the data, except for the crowdsource data.
The crowd source data are imported and managed in the crowd.py file.

2. Login the bot and check chatrooms.
Open the chat.py file, you should run this file from top, cell by cell.

3. Now the bot is good to go, you could ask it questions in the speakeasy webpage.


Second, brief introduction of the files.

1. The 'unfinished' files.
They are something I tried to implement yet failed to finish in time.
Including: agentPerRoom, openNewChatRoom, thread, questionTemps.
The first three are something I tried to implement multi-threading to increase agent response speed, yet still need to debug and left unfinish.
The last one is what I tried to add to increase my bot's ability to asnwer more format of questions, unfinished.

2. The file for debug.
The search.py file is my debugging file, not used when running the bot.

3. The file for agent and chat.
agent.py, chat.py

4. The file for parsing message.
getEntity.py, getRelation.py, humanOrFilm.py, Recommendation.py, showPic.py, checkCrowd.py

5. Main logic flow.
The main.py file handles the main logic and imported all the data and all the files in 4.

6. Query templates
The SPARQL query templates are stored in queryTemps.py
