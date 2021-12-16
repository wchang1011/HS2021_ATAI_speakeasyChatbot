# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 08:34:28 2021

@author: Wenqing
"""

# imports
import csv, json
import numpy as np
import rdflib
from rdflib.term import URIRef, Literal
import pandas as pd
from sklearn.metrics import pairwise_distances
import re
#%%
from getEntity import getEntity
from getRelation import getRelation
gr = getRelation()
ge = getEntity()
#%%

# for _ in range(11):
#             try:
#                 response = requests.post(url=self.url + path,
#                                          params={**params, "session": self.session_token},
#                                          data=message.encode('utf-8')).json()
#                 log.debug(response)
#                 return response
#             except RequestException:
#                 log.warning('Failed.... I am trying to recover')
#                 time.sleep(1)
#         else:
#             raise Exception('Recovering failed.')

#%%
# define some prefixes
WD = rdflib.Namespace('http://www.wikidata.org/entity/')
WDT = rdflib.Namespace('http://www.wikidata.org/prop/direct/')
DDIS = rdflib.Namespace('http://ddis.ch/atai/')
RDFS = rdflib.namespace.RDFS
SCHEMA = rdflib.Namespace('http://schema.org/')

# load the graph
graph = rdflib.Graph().parse('Dataset\\14_graph.nt', format='turtle')
# load the embeddings
entity_emb = np.load('Dataset\\entity_embeds.npy')
relation_emb = np.load('Dataset\\relation_embeds.npy')
#%%
# load the dictionaries
with open('Dataset\\entity_ids.del', 'r') as ifile:
    ent2id = {rdflib.term.URIRef(ent): int(idx) for idx, ent in csv.reader(ifile, delimiter='\t')}
    id2ent = {v: k for k, v in ent2id.items()}
with open('Dataset\\relation_ids.del', 'r') as ifile:
    rel2id = {rdflib.term.URIRef(rel): int(idx) for idx, rel in csv.reader(ifile, delimiter='\t')}
    id2rel = {v: k for k, v in rel2id.items()}
    
ent2lbl = {ent: str(lbl) for ent, lbl in graph.subject_objects(RDFS.label)}
lbl2ent = {lbl: ent for ent, lbl in ent2lbl.items()}

#%%
## subject predicate object

# set graph variables
entities = set(graph.subjects()) | {s for s in graph.objects() if isinstance(s, URIRef)}
# all subjects and the objects which isinstance of URIRef are entities
predicates = set(graph.predicates())
literals = {s for s in graph.objects() if isinstance(s, Literal)}
# all objects which isinstance of Literal are literals

#%%
## get predicate labels into a list of string
predURIList = list(predicates)
predWDTlist = []
predLblList = []
for idx, prd in enumerate(predURIList):
    
    wdtIdPattern = "{}(.*)".format(WDT)
    if re.search(wdtIdPattern, prd):
        predWDT = re.search(wdtIdPattern, prd).group(1)
    predWDTlist.append(predWDT)

def getRelLbl(graph,rel):
        # get Rel URI
        query_relLbl = '''
            prefix wdt: <http://www.wikidata.org/prop/direct/>
            prefix wd: <http://www.wikidata.org/entity/>
            
            SELECT ?relLbl WHERE{{
                wdt:{} rdfs:label ?relLbl.
                }}'''.format(rel)
        relLbl = graph.query(query_relLbl)
        return relLbl
    
for idx,pred in enumerate(predWDTlist):
    predLbl = str(list(getRelLbl(graph, pred))[0][0])
    predLblList.append(predLbl)
    print(predLblList[idx])

#%%
## get Alias of predicate labels as a dataframe
df = pd.read_csv('Dataset\\alias.csv', encoding = "ISO-8859-1")
alias = df.filter(['property','propertyLabel','propertyAltLabel'],axis=1)

# for idx, pred in enumerate(predLblList):
#     selc = alias.query(alias['propertyLabel'] == pred)
predAlias = alias.loc[alias['propertyLabel'].isin(predLblList)]
#%%
## return the label in graph by seaching aliasDataframe 
swdtPropList = []
for idx, alt in enumerate(predAlias['propertyAltLabel']):
    # print(idx,alt)
    if isinstance(alt, str):
        listAlt = list(alt.split(', '))
    # print(listAlt)
    if "directed" in listAlt:
        pd = predAlias.iloc[[idx]]
        wdtProp = pd['property']
        swdtProp = wdtProp[pd.index.values[0]]
        swdtPropList.append(swdtProp)
    elif predAlias.iloc[idx].str.contains("directed")['propertyAltLabel'] and isinstance(predAlias.iloc[idx]['propertyAltLabel'],str):
        pd = predAlias.iloc[[idx]]
        wdtProp = pd['property']
        swdtProp = wdtProp[pd.index.values[0]]
        swdtPropList.append(swdtProp)
#%%
## get Pxx from swdtProp
predId = gr.getRelIdByURI(WD, swdtPropList)
#%%

#%%

from transformers import pipeline

ner = pipeline('ner')
#%%

# question1 = 'Show me the pictures of the lead actors of the movie Jurassic Park.'
question2 = 'Show me the pictures of the lead actors of the movie Jurassic Park.'
# question1 = 'Show me an action movie poster.'


# entity1 = ge.getEnt(question1)
# tokens = ge.getTokens(question1)
# nouns = ge.returnNounBfMovie(tokens)
# print(tokens)
# print("nouns: ",nouns)
# words = ge.returnNAfRcmd(tokens)
# print("words after recommendation: ",words)
entity2 = ge.getEnt(question2)
# relation1,relTbd1 = gr.getRel(entity1,question1)
relation2,relTbd2 = gr.getRel(entity2,question2)
# print("entity: ", entity1, "relation: ", relation1,relTbd1)
print("entity: ",entity2, "relation: ",relation2,relTbd2)

# if relTbd1==True:
#     relation1 = gr.tbdRel(relation1)
if relTbd2==True:
    relation2 = gr.tbdRel(relation2)
print(relation2)

# relid1 = gr.getRelWDTid(graph, WDT, relation1)
# print(relid1)
# relid2 = gr.getRelWDTid(graph, WDT, relation2)
# print(relid2)
#%%
entity = 'Batmans'
uri = ge.getEntURI(graph, entity)
#%%
print({o for o in graph.objects(None,RDFS.label)})
#%%
# check if actor has imdbid
query_template2 = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?actorLbl ?imdbid
    WHERE {{
        ?actor rdfs:label ?actorLbl .
        ?actor wdt:P345 ?imdbid .
        ?actor wdt:P106 wd:Q33999 .
        }}'''
res = set(graph.query(query_template2))
print(res, len(res))

#%%
## given human name search for imdbid
humanImdbIdTemp = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?imdbid
    WHERE {{
        ?human rdfs:label "{}"@en .     
        ?human wdt:P345 ?imdbid .
        }}'''.format('Christopher Nolan')
res = set(graph.query(humanImdbIdTemp))
print(res, len(res))
#%%
# check actors of a movie
query_template2 = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?actorLbl ?imdbid
    WHERE {{
        ?film rdfs:label "{}"@en .
        ?actor ?rel ?film .
        ?actor rdfs:label ?actorLbl .
        ?actor wdt:P345 ?imdbid .
        }}'''.format('Jurassic Park')
res = set(graph.query(query_template2))
print(res, len(res))
#%%
query_template2 = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?rel
    WHERE {{
        ?sujU rdfs:label "{}"@en.
        ?objU rdfs:label ?objL .
        ?objU ?rel ?sujU .
        FILTER(CONTAINS(str(?objL), "{}")) .
        }}'''.format('Christopher Nolan','Batman')
res = set(graph.query(query_template2))
print(res, len(res))
#%%
query_template2 = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?sujU ?objU
    WHERE {{
        ?sujU rdfs:label "{}"@en.
        ?objU rdfs:label ?objL .
        ?objU ?rel ?sujU .
        ?rel rdfs:label ?relL.       
        FILTER(CONTAINS(str(?objL), "{}")) .
        }}'''.format('Christopher Nolan','Batman')
res = set(graph.query(query_template2))
print(res, len(res))
#%%
# get wdt:P of acting
query_template2 = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?imdbid ?actor
    WHERE {{
        ?film rdfs:label "{}"@en .
        ?actor ?rel ?film .
        ?actor wdt:P106 wd:Q33999 .        
        ?actor rdfs:label ?actorLbl .
        ?actor wdt:P345 ?imdbid .
        }}'''.format('Jurassic Park')
res = set(graph.query(query_template2))
print(res, len(res))

#%%
# try if could get actor image of wikidata
query_template2 = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?pic
    WHERE {{
        wd:Q229775 wdt:P18 ?pic .
        
        }}'''
res = set(graph.query(query_template2))
print(res, len(res))
#%%
query_template2 = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?relL
    WHERE {{
        ?sujU rdfs:label "{}"@en.
        ?sujU wdt:P31 wd:Q11424 .
        ?objU rdfs:label "{}"@en.
        ?sujU ?rel ?objU.
        ?rel rdfs:label ?relL
        }}'''.format(entities[1],entities[0])
res = set(graph.query(query_template2))
print(res, len(res))
#%%
query_template2 = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?relL
    WHERE {{
        ?sujU wdt:P31 wd:Q11424 .
        ?sujU rdfs:label ?sujL .
        filter contains(?sujL,"{}")
        }}'''.format(entities[1])
res = set(graph.query(query_template2))
print(res, len(res))
#%%
entities = ['Tim Burton', 'Batman']
query_template2 = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?rel ?relL
    WHERE {{
        ?sujU rdfs:label "{}"@en.
        ?objU rdfs:label "{}"@en.
        ?objU wdt:P31 wd:Q11424 .
        ?objU ?rel ?sujU .
        ?rel rdfs:label ?relL
        }}'''.format(entities[0],entities[1])
res = set(graph.query(query_template2))
print(res, len(res))
#%%
# search entity if is instance of human
humanName = 'Steven Spielberg'
query_template2 = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?rel ?sujU
    WHERE {{
        ?sujU rdfs:label "{}"@en.
        ?sujU ?rel wd:Q5 .
        }}'''.format(humanName)
res = set(graph.query(query_template2))
print(res, len(res))
#%%
humanQid = 'Q8877'
query_template2 = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?rel
    WHERE {{
        wd:{} ?rel wd:Q5 .
        }}'''.format(humanQid)
res = set(graph.query(query_template2))
print(res, len(res))
#%%
# query with human name and movie genre
entity = ['Steven Spielberg']
target = ['action', 'movies']
query_template2 = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?movieLbl ?genreLbl
    WHERE {{
        ?director rdfs:label "{}"@en.
        ?movie wdt:P57 ?director .
        ?movie wdt:P136 ?genre .
        ?genre rdfs:label ?genreLbl .
        ?movie rdfs:label ?movieLbl .      
        }}'''.format(entity[0])
res = set(graph.query(query_template2))
print(res, len(res))
#%%
## read in images.json
with open("Dataset\\images.json", "r") as f:
    images = json.load(f)
#%%

ents = {
    qid: lbl
    for qid, imdb in graph.subject_objects(WDT.P345)
    for lbl in graph.objects(qid, RDFS.label)
    if imdb.startswith('tt')
    }
print(ents)

#%%
q1 = 'Show me an action movie poster.'
"show" in q1.lower()

entity1 = ge.getEnt(q1)
tokens = ge.getTokens(q1)
nouns = ge.returnNouns(tokens)
print("nouns: ",nouns)
words = ge.returnNAfRcmd(tokens)
print("words after recommendation: ",words)
relation1,relTbd1 = gr.getRel(entity1,q1)
print("entity: ", entity1, "relation: ", relation1,relTbd1)
if relTbd1==True:
    relation1 = gr.tbdRel(relation1)

# relid1 = gr.getRelWDTid(graph, WDT, relation1)
# print(relid1)
# relid2 = gr.getRelWDTid(graph, WDT, relation2)
# print(relid2)
#%%
# try labels for entity and relation and see if different
queryLabel = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?label
    WHERE {{
        wdt:{} rdfs:label ?label.
        }}'''.format('P2142')
res = list(graph.query(queryLabel))
print(res, len(res))
#%%
queryEntityLabel = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?label
    WHERE {{
        wd:{} rdfs:label ?label.
        }}'''.format('Q132863')
res = list(graph.query(queryLabel))
print(res, len(res))
#%%
# try imdb id connection
queryImdb = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?imdb WHERE {{
        ?qid rdfs:label "{}"@en .
        ?qid wdt:P345 ?imdb .
        FILTER(STRSTARTS(str(?imdb), "tt")) .
    }}'''.format("Batman")
   
res = list(graph.query(queryImdb))
print(res, len(res))
#%%
# try ways of searching images list
# batman1 = list(filter(lambda film: 'nm0923516' in film['cast'], images))
# films = list(filter(lambda film: film['movie'] == ['tt0313043'] and len(film['cast']) != 0, images))
gC = list(filter(lambda film: '2857/rm2490341376' in film['img'], images))
print(gC)
# batman2 = list(filter(lambda film: film['movie'] == ['tt0059968'], images))
# batman3 = list(filter(lambda film: film['movie'] == ['tt0096895'], images))
#%%
picTypList = []
for idx, film in enumerate(images):
    picTyp = film['type']
    
    if picTyp not in picTypList:
        picTypList.append(picTyp)
        
#%%
genre = "action"
queryDDIS = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    prefix ddis: <http://ddis.ch/atai/>
    
    SELECT ?imdb WHERE {{
        ?qid ddis:tag "{}"@en .
        ?qid wdt:P345 ?imdb .
        FILTER(STRSTARTS(str(?imdb), "tt")) .
    }}'''.format(genre)
res = list(graph.query(queryDDIS))
print(res, len(res))

#%%
entity = 'Steven Spielberg'
humanImdbIdTemp = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?imdbid
    WHERE {{
        ?human rdfs:label "{}"@en .       
        ?human rdfs:label ?humanLbl .
        ?human wdt:P345 ?imdbid .
        }}'''.format(entity)
res = list(graph.query(humanImdbIdTemp))
print(res, len(res))
#%%
query_template1 = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?movie ?box
    WHERE {{
        ?movie rdfs:label 'The Firm'@en.
        ?movie wdt:P2142 ?box.
        }}'''
res = set(graph.query(query_template1))
print(res, len(res))
   
#%%

SS = list(filter(lambda film: film['cast'] ==['nm0000229'], images))
print(SS)
#%%
# if find nothing, list nearest entities and request clarification
if len(res)==0:
    qids,lbls = ge.getNearestEnt(WD, ent2id,ent2lbl, lbl2ent, id2ent, entity_emb, entity)
    print(qids,lbls)

qid,lbl = ge.clarifyEnt(qids, lbls)
#%%
# parse res set into list of strings
answers = []
for row in res:
    answers.append(str(row.objL))

#%%
answer_template = "Hi, {} of {} is {}".format(relation,entity,answers)
print(answer_template)
#%%
# entId = ent2id[lbl2ent[entity]]
# print(lbl2ent[relation])
# relId = rel2id[lbl2ent[relation]]
# print(entId,relId)