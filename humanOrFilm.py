# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 12:55:55 2021

@author: Wenqing
"""
### This is a file for checking if an entity is a human or a film

from queryTemps import isHumanTemp, isFilmTemp

def humanOrFilm(graph,entity):
    isHumanQuery = isHumanTemp.format(entity)
    isHuman = set(graph.query(isHumanQuery))
    isFilmQuery = isFilmTemp.format(entity)
    isFilm = set(graph.query(isFilmQuery))
    if len(isHuman)==0:
        human = False
    else:
        for row in isHuman:
            if 'P31' in str(row.rel):
                human = True
                print("ishuman")
    if len(isFilm)==0:
        film = False
    else:
        for row in isFilm:
            if 'P31' in str(row.rel):
                film = True
                print("isfilm")
    return human, film