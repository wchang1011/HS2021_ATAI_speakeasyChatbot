# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 09:09:54 2021

@author: Wenqing
"""
### This file parse the message and get relation

import nltk
import re

class getRelation:
    def __init__(self):
        pass
    
    def getTokens(self,question):
        tokens = nltk.word_tokenize(question)
        pos_tokens = nltk.pos_tag(tokens)
        return pos_tokens    
    
    def returnVerbs(self,pos_tokens):
        idxlist =[]
        verbTokens = []
        for idx,tup in enumerate(pos_tokens):
            if "VB" in tup[1]:
                idxlist.append(idx)
        for idx in idxlist:
            verbTokens.append(pos_tokens[idx][0])
        return verbTokens
    
    ## this method match the ... of pattern
    def theOfTokens(self,question):
        theOfPattern = "the (.*) of"
        matching = re.search(theOfPattern,question)
        if not matching:
            return False
        else:
            relation = matching.group(1)
            return [relation]
    ## main method for getting relation
    def getRel(self,question):
        theOf = self.theOfTokens(question)
        if not theOf:
            tbd = True
            pos_tokens = self.getTokens(question)
            verbs = self.returnVerbs(pos_tokens)
            relations = verbs
        else:
            tbd = False
            relations = theOf
        return relations, tbd
    
    ## check if recommend in relation
    def tbdRel(self,relation):
        if 'recommend'in relation:
                return ['recommend']
        return relation
    
    ## search for alias of relation in predAlias dictionary
    def searchAlias(self,relation,predAlias):
        
        swdtPropList = []
        for idx, alt in enumerate(predAlias['propertyAltLabel']):
            # print(idx,alt)
            if isinstance(alt, str):
                listAlt = list(alt.split(', '))
            # print(listAlt)
            if relation in listAlt:
                pd = predAlias.iloc[[idx]]
                wdtProp = pd['propertyLabel']
                swdtProp = wdtProp[pd.index.values[0]]
                swdtPropList.append(swdtProp)
            elif predAlias.iloc[idx].str.contains(relation)['propertyAltLabel'] and isinstance(predAlias.iloc[idx]['propertyAltLabel'],str):
                pd = predAlias.iloc[[idx]]
                wdtProp = pd['propertyLabel']
                swdtProp = wdtProp[pd.index.values[0]]
                swdtPropList.append(swdtProp)
        
        return swdtPropList
    
    ## get relation pid by relation labels
    def getRelWDTid(self,graph,WDT,relations):
        relURIList = self.getRelURI(graph,relations,WDT)
        relIds = self.getRelIdByURI(WDT, relURIList)
        return relIds
    
    ## query for relation URI with relation label as input
    def getRelURI(self,graph,relation,WDT):
        # get Rel URI
        query_relURI = '''
            prefix wdt: <http://www.wikidata.org/prop/direct/>
            prefix wd: <http://www.wikidata.org/entity/>
            
            SELECT ?rel WHERE{{
                ?rel rdfs:label "{}"@en.
                }}'''.format(relation)
        relURIList = list(graph.query(query_relURI))
        relURIs = []
        for idx, relURI in enumerate(relURIList):
            print(relURI)
            if WDT in str(relURI[0]):
                relURIs.append(str(relURI[0]))
        print("relURI: ",relURIs)
        return relURIs
    
    ## query for relation pid with URI as input
    def getRelIdByURI(self,WDT,relURIList):
        # get Rel WDTid
        relIds = []
        for idx, row in enumerate(relURIList):
            print("idx: ",idx,"row: ",row)
            if WDT in row:
                wdtIdPattern = "{}(.*)".format(WDT)
                relId = re.search(wdtIdPattern, row).group(1)
                relIds.append(relId)
        return relIds