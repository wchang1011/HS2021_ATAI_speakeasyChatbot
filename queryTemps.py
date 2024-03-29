# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 08:47:25 2021

@author: Wenqing
"""
# query entity URI
queryLabel = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?label
    WHERE {{
        wd:{} rdfs:label ?label.
        }}'''

# query for given one entity and on relation, find the other entity qid
query_template1 = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?objU
    WHERE {{
        ?sujU rdfs:label "{}"@en.
        ?sujU wdt:{} ?objU.
        }}'''
    
# query for given two entities and find if relation exist
query_template2 = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?relL
    WHERE {{
        ?sujU rdfs:label "{}"@en.
        ?objU rdfs:label "{}"@en.
        ?objU wdt:P31 wd:Q11424 .
        ?objU ?rel ?sujU .
        ?rel rdfs:label ?relL
        }}'''
    # switch direction
query_template3 = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?relL
    WHERE {{
        ?sujU rdfs:label "{}"@en.
        ?objU rdfs:label "{}"@en.
        ?objU wdt:P31 wd:Q11424 .
        ?sujU ?rel ?objU .
        ?rel rdfs:label ?relL
        }}'''
    
    
## given entity, check entity is instance of human   
isHumanTemp = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?rel
    WHERE {{
        ?sujU rdfs:label "{}"@en.
        ?sujU ?rel wd:Q5 .
        }}'''

## given entity, check entity is instance of film   
isFilmTemp = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?rel
    WHERE {{
        ?sujU rdfs:label "{}"@en.
        ?sujU ?rel wd:Q11424 .
        }}'''


## given director and genre
filmGenreTemp = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?movieLbl ?genreLbl
    WHERE {{
        ?director rdfs:label "{}"@en.
        ?movie wdt:P57 ?director .
        ?movie wdt:P136 ?genre .
        ?genre rdfs:label ?genreLbl .
        ?movie rdfs:label ?movieLbl .      
        }}'''
## connect qid and imdbid   
imdbIdTemp = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?imdb WHERE {{
        ?qid rdfs:label "{}"@en .
        ?qid wdt:P345 ?imdb .
        FILTER(STRSTARTS(str(?imdb), "tt")) .
    }}'''

## given genre search for imdbid
genrePosterTemp = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    prefix ddis: <http://ddis.ch/atai/>
    
    SELECT ?imdb WHERE {{
        ?qid ddis:tag "{}"@en .
        ?qid wdt:P345 ?imdb .
        FILTER(STRSTARTS(str(?imdb), "tt")) .
    }}'''
    
## given movie label seach for actor's imdbid
movie2ActorImdbTemp = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?imdbid
    WHERE {{
        ?film rdfs:label "{}"@en .
        ?actor ?rel ?film .
        ?actor wdt:P106 wd:Q33999 .        
        ?actor rdfs:label ?actorLbl .
        ?actor wdt:P345 ?imdbid .
        }}'''

## given human name search for imdbid
humanImdbIdTemp = '''
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd: <http://www.wikidata.org/entity/>
    
    SELECT ?imdbid
    WHERE {{
        ?human rdfs:label "{}"@en .       
        ?human rdfs:label ?humanLbl .
        ?human wdt:P345 ?imdbid .
        }}'''