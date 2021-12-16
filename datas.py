# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 09:38:54 2021

@author: Wenqing
"""
# imports

import numpy as np
import pandas as pd
import re,json,csv,rdflib
from rdflib.term import URIRef, Literal

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
# external dataset
top250 = set(open('Dataset\\imdb-top-250.t').read().split('\n')) - {''}

print(pd.DataFrame([
    ('Top-250 coverage', '{:n}'.format(
        len(top250 & {str(o) for o in graph.objects(None, WDT.P345) if o.startswith('tt')}))),
    ('Entities with IMDb ID', '{:n}'.format(
        len({str(o) for o in graph.objects(None, WDT.P345) if o.startswith('tt')}))),
    ('Plots linked to a movie', '{:n}'.format(
        len({qid for qid, plot in csv.reader(open('Dataset\\plots.csv',encoding='utf-8')) if URIRef(qid) in entities}))),
    ('Comments linked to a movie', '{:n}'.format(
        len([qid for qid, rating, sentiment, comment in csv.reader(open('Dataset\\user-comments.csv')) if URIRef(qid) in entities]))),
    ('Movies having at least one comment', '{:n}'.format(
        len({qid for qid, rating, sentiment, comment in csv.reader(open('Dataset\\user-comments.csv')) if URIRef(qid) in entities}))), 
    ]))
#%%
# literal predicates
ent_lit_preds = {p for s,p,o in graph.triples((None, None, None)) if isinstance(o, Literal)}
ent_lit_preds
print(pd.DataFrame([
    ('# entities', '{:n}'.format(
        len(entities))),
    ('DDIS.rating', '{:n}'.format(
        len(set(graph.subjects(DDIS.rating, None))))),
    ('DDIS.tag', '{:n}'.format(
        len(set(graph.subjects(DDIS.tag, None))))),
    ('SCHEMA.description', '{:n}'.format(
        len({s for s in graph.subjects(SCHEMA.description, None) if s.startswith(WD)}))),
    ('RDFS.label', '{:n}'.format(
        len({s for s in graph.subjects(RDFS.label, None) if s.startswith(WD)}))),
    ('WDT.P18 (wikicommons image)', '{:n}'.format(
        len(set(graph.subjects(WDT.P18, None))))),
    ('WDT.P2142 (box office)', '{:n}'.format(
        len(set(graph.subjects(WDT.P2142, None))))),
    ('WDT.P345 (IMDb ID)', '{:n}'.format(
        len(set(graph.subjects(WDT.P345, None))))),
    ('WDT.P577 (publication date)', '{:n}'.format(
        len(set(graph.subjects(WDT.P577, None))))),
    ]))
#%%
## read in images.json
with open("Dataset\\images.json", "r") as f:
    images = json.load(f)
#%%
## get all entity labels into a list of string
entLblList = []
for o in graph.objects(None, RDFS.label):
    entLblList.append(str(o))
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
# ## read crowdsource data
# crowdSource = pd.read_csv('Dataset\\ATAI_crowd_data.tsv', sep='\t')
# # #%%
# # def filterMalicious(crowdSource):
# #     workTime = crowdSource.filter(['HITId','WorkTimeInSeconds', 'WorkerId'],axis=1)
# #     malHits = workTime.loc[workTime.groupby('HITId')['WorkTimeInSeconds'].idxmin()]
# #     malWorkers = malHits['WorkerId'].unique()
# #     cleanCrowd = crowdSource
# #     for idx, malWk in enumerate(malWorkers):
# #         cleanCrowd = cleanCrowd.drop(cleanCrowd[(cleanCrowd['WorkerId'] == malWk)].index)
# #     return cleanCrowd

# # def aggregateAnswer(cleanCrowd):
# #     aggAns = cleanCrowd.groupby('HITId')['AnswerLabel'].agg(pd.Series.mode).to_frame()
# #     return aggAns

# # def interRaterCompute(cleanCrowd):
# #     zdf = cleanCrowd.filter(['HITId','AnswerLabel'])
# #     numCnt = zdf.groupby('HITId')['AnswerLabel'].value_counts().to_frame()
# #     counts = zdf.groupby('HITId')['AnswerLabel'].value_counts('counts').to_frame()
# #     irate = counts.groupby('HITId')['AnswerLabel'].max()
# #     return numCnt, irate

# # # def addCrowdToGraph(aggAns, irPerHit):
# # #     return crowdGraph
# #%%
# workTime = crowdSource.filter(['HITId','WorkTimeInSeconds', 'WorkerId'],axis=1)
# malHits = workTime.loc[workTime.groupby('HITId')['WorkTimeInSeconds'].idxmin()]
# malWorkers = malHits['WorkerId'].unique()
# cleanCrowd = crowdSource
# for idx, malWk in enumerate(malWorkers):
#     cleanCrowd = cleanCrowd.drop(cleanCrowd[(cleanCrowd['WorkerId'] == malWk)].index)

# aggAns = cleanCrowd.groupby('HITId')['AnswerLabel'].agg(pd.Series.mode).to_frame()

# zdf = cleanCrowd.filter(['HITId','AnswerLabel'])
# numCnt = zdf.groupby('HITId')['AnswerLabel'].value_counts().to_frame()
# counts = zdf.groupby('HITId')['AnswerLabel'].value_counts('counts').to_frame()
# irate = counts.groupby('HITId')['AnswerLabel'].max()


# # #%%
# cleanCrowd = filterMalicious(crowdSource)
# aggAns = aggregateAnswer(cleanCrowd)
# numCnt, irate = interRaterCompute(cleanCrowd)
