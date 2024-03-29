# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 10:29:40 2021

@author: Wenqing
"""
### This is the file for recommendation questions

from sklearn.metrics import pairwise_distances
import numpy as np
from datas import entity_emb,ent2id,id2ent,lbl2ent,ent2lbl
from queryTemps import *

class Recommendation:
    def __init__(self):
        pass
    
    ## Positive recommendation given film name
    def posRcmFilm(self,entity):
        # TransE
        print("get entity: ",entity)
        rcmds = []
        topN = 10
        emb = np.atleast_2d(entity_emb[ent2id[lbl2ent[entity]]])
        dist = pairwise_distances(emb, entity_emb)
        print("finish calculating distances")
        for idx in dist.argsort().reshape(-1)[:topN]:
            rcmds.append(ent2lbl[id2ent[idx]])
        print(rcmds)
        
        return rcmds
    
    ## positive recommendation given human name and genre
    def posRcmHuman(self,entity,target,graph):
        # director's movie
        rcmds = []
        queryFilm = filmGenreTemp.format(entity)
        res = set(graph.query(queryFilm))
        for row in res:
            if target[0] in str(row.genreLbl):
                rcmds.append(str(row.movieLbl))
        return rcmds
    
    
    ## unfinished recommendation for negative sentiment
    # def negRcmFilm(self,entity):
    #     return rcmds

    # def negRcmHuman(self,entity,target):
    #     return rcmds