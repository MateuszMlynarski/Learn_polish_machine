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
book = ''.join([word for word in book if word not in (',','.')])

allWords = data.values.tolist()

def firstWord(array):
    return str(array[0])

verbs = [wordFamily[0] for wordFamily in allWords
              if firstWord(wordFamily)[:firstWord(wordFamily).find(',')].endswith(inflections)]

infinitives = [firstWord(wordFamily)[:firstWord(wordFamily).find(',')]
        for wordFamily in allWords
        if firstWord(wordFamily)[:firstWord(wordFamily).find(',')].endswith(inflections)]

infinitivesToVerbs = dict(zip(infinitives, verbs))

def assign_inflection(verb,index=0):
    if verb.endswith(inflections[index]):
        return inflections[index]
    else:
        return assign_inflection(verb,index+1)

inflectionsAssigned = dict(zip(infinitives, map(assign_inflection, infinitives)))

coreAssigned = dict(
        zip(
                infinitives, [
                        infinitive[:-len(inflectionsAssigned[infinitive])]
                        for infinitive in infinitives
                        ]
                )
        )

coreToFamily = {
        (coreAssigned[infinitive], inflectionsAssigned[infinitive])
        :infinitivesToVerbs[infinitive]
        for infinitive in infinitives
        }


# w tym miejscu trzeba uważać czy cores okreslamy jako liste czy set
# niektore cory nie sa unikatowe np dla bezokol. wić i wyć.
cores = [element[0] for element in coreToFamily.keys()]
inflections = [element[1] for element in coreToFamily.keys()]

coreToInflection = dict(zip(cores, inflections))

countCoreFrequency = [(coreAssigned[infinitive],
                       inflectionsAssigned[infinitive],
                       book.count(coreAssigned[infinitive]),
                       infinitivesToVerbs[infinitive]
                       ) for infinitive in infinitives]

countCoreFrequency.sort(key=itemgetter(2), reverse=True)

# Okreslmy 1% najczęstszych czasowników
maxFeatures = int(0.01 * len(countCoreFrequency))

searchBase = tuple(countCoreFrequency)[:maxFeatures]


# 1.wyszukaj core
# 2. zwróć cały wyraz
# 3. pokaż wyraz po nim



findAllCores = [
        (
            element[0],
            [instance for instance in re.findall('\s\S*' + str(element[0]) + '\S*\s', book)
            if instance in element[3]]
        )
        for element in searchBase
                ]


B = [
        (
            element[0],
            re.findall('\s\S*' + str(element[0]) + '\S*\s', book)
        )
        for element in searchBase
                ]



#del lista


# twórz core czasowników

    

#czaswoniki mają skapitalizowane rzeczowniki! NAPRAW!        
# znaleźć dowolny tekst i sprawdzić które słowa są najczęstsze
# podzielić słowa na core i końcówki, stworzyć zbiór końcówek
# z tekstu wydobyć słowa z końcówkami, sprawdzić czy są w naszym zbiorze czasowników.
# Sprawdzic w jakim są otoczeniu, tzn. jaki tworzą kontekst.