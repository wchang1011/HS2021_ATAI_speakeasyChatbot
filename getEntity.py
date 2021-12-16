# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 11:20:02 2021

@author: Wenqing
"""
#### use nltk to tokenize a text ####

import nltk, re, editdistance
from transformers import pipeline
from sklearn.metrics import pairwise_distances

ner = pipeline('ner')

class getEntity:
    def __init__(self):
        pass
    
    def getTokens(self,question):
        tokens = nltk.word_tokenize(question)
        pos_tokens = nltk.pos_tag(tokens)
        return pos_tokens
    
    def returnNouns(self,pos_tokens):
        idxlist =[]
        nouns = []
        for idx,tup in enumerate(pos_tokens):
            if "NN" in tup[1]:
                idxlist.append(idx)
        for idx in idxlist:
            nouns.append(pos_tokens[idx][0])
        return nouns
    
    ## this method get nouns after the word recommend
    def returnNAfRcmd(self,pos_tokens):
        idxlist =[]
        words = []
        recIdx = 999
        for idx,tup in enumerate(pos_tokens):
            if "recommend" in tup[0].lower():
                recIdx = idx
            if idx > recIdx and "NN" in tup[1]:
                idxlist.append(idx)
        for idx in idxlist:
            words.append(pos_tokens[idx][0])
        return words
    
    ## this method get nouns before the word movie or film
    def returnNounBfMovie(self,pos_tokens):
        movieIdx = 0
        for idx,tup in enumerate(pos_tokens):
            if "movie" in tup[0].lower() or "film" in tup[0].lower():
                movieIdx = idx
        for idx,tup in enumerate(pos_tokens):
            if idx == movieIdx - 1 and "NN" in tup[1]:
                genre = pos_tokens[idx][0]      
        return genre
    
    def getEnt(self,question):
        entities = ner(question, aggregation_strategy="simple")
        entList = []
        for idx,ent in enumerate(entities):
            entList.append(ent["word"])
        return entList
    
    def getEntURI(self,graph,entity):
        # entity label to URIs
        query_entURI = '''
            prefix wdt: <http://www.wikidata.org/prop/direct/>
            prefix wd: <http://www.wikidata.org/entity/>
            
            SELECT ?sujU
            WHERE{{
                ?sujU rdfs:label "{}"@en.
                }}'''.format(entity)
        entURIList = list(graph.query(query_entURI))
        entURIs = []
        for idx, entURI in enumerate(entURIList):
            entURIs.append(str(entURI[0]))
        print("entURI: ",entURIs)
        return entURIs
    
    def getEntIdByURI(self,WD,entURI):
        entId = []
        if WD in entURI:
            wdIdPattern = "{}(.*)".format(WD)
            entId = re.search(wdIdPattern, entURI).group(1)        
        return entId
    
    def checkTypo(self,entLblList,entity):
        entTypoCorr = []
        threshold = 9999
        for idx, entlbl in enumerate(entLblList):
            dist = editdistance.eval(entity,entlbl)
            if dist < threshold:
                threshold = dist
                matchnode = idx
        entTypoCorr = entLblList[matchnode]
        return entTypoCorr

    
    def getNearestEntEmb(self,WD,ent2id,ent2lbl,lbl2ent,id2ent,entity_emb,word):
        ent = ent2id[lbl2ent[word]]
        emb = entity_emb[ent]
        dist = pairwise_distances(emb.reshape(1, -1), entity_emb).reshape(-1)
        most_likely = dist.argsort()
        qids = []
        lbls = []
        for rank, idx in enumerate(most_likely[:15]):
            qids.append(id2ent[idx][len(WD):])
            lbls.append(ent2lbl[id2ent[idx]])
        return qids,lbls
    
    def clarifyEnt(self,qids,lbls):
        qid = qids[10]
        lbl = lbls[10]
        return qid, lbl
