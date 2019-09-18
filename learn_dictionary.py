# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 23:57:06 2019

@author: matim
"""

import pandas as pd
import numpy as np
import re
from operator import itemgetter

inflections = 'ić', 'yć', 'uć', 'eć', 'ać', 'ąć', 'eść', 'iść', 'aść', 'źć'

data = pd.read_csv("DICTIONARY.csv",delimiter=',', names=['Words'])

book = open("pan_tadeusz.txt", "r", encoding="utf8").read()

allWords = data.values.tolist()

def firstWord(array):
    return str(array[0])

verbs = [wordFamily[0] for wordFamily in allWords
              if firstWord(wordFamily)[:firstWord(wordFamily).find(',')].endswith(inflections)]

infinitives = [firstWord(wordFamily)[:firstWord(wordFamily).find(',')]
        for wordFamily in allWords
        if firstWord(wordFamily)[:firstWord(wordFamily).find(',')].endswith(inflections)]

infinitivesToVerbs = {
        infinitives[i]:verbs[i]
        for i in range(len(infinitives))
        }

def assign_inflection(verb,index):
    if verb.endswith(inflections[index]):
        return inflections[index]
    else:
        return assign_inflection(verb,index+1)

inflectionsAssigned = {
        infinitive:assign_inflection(infinitive,0) for infinitive in infinitives
        }

coreAssigned = {
        infinitive:infinitive[:-len(inflectionsAssigned[infinitive])]
        for infinitive in infinitives
        }

coreToFamily = {
        coreAssigned[infinitive]:infinitivesToVerbs[infinitive]
        for infinitive in infinitives
        }

cores = coreToFamily.keys()

countCoreFrequency = [(core, book.count(core)) for core in cores]

countCoreFrequency.sort(key=itemgetter(1), reverse=True)


#del lista


# twórz core czasowników

    

#czaswoniki mają skapitalizowane rzeczowniki! NAPRAW!        
# znaleźć dowolny tekst i sprawdzić które słowa są najczęstsze
# podzielić słowa na core i końcówki, stworzyć zbiór końcówek
# z tekstu wydobyć słowa z końcówkami, sprawdzić czy są w naszym zbiorze czasowników.
# Sprawdzic w jakim są otoczeniu, tzn. jaki tworzą kontekst.