# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 23:57:06 2019

@author: matim
"""

import pandas as pd
import numpy as np
import re
from operator import itemgetter
import string
from indices import indices

inflections = 'ić', 'yć', 'uć', 'eć', 'ać', 'ąć', 'eść', 'iść', 'aść', 'źć'

data = pd.read_csv("DICTIONARY.csv",delimiter=',', names=['Words'])

# Procesowanie książki
#book = open("pan_tadeusz.txt", "r", encoding="utf8").read()
book = open("zbrodnia_i_kara.txt", "r", encoding="utf8").read()
book.replace('\n', ' ').replace(',', ' ,').replace('.', ' .').replace(';', ' ;').replace(':', ' :')
#book = ''.join([word for word in book if word not in (',','.',';'':')])
#Preprocessing
#no_punctuation_book = re.sub(r'[^\w\s]','',book)
book_split = book.split()

allWords = data.values.tolist()

def firstWord(array):
    return str(array[0])

verbs = np.asarray([wordFamily[0].split(', ') for wordFamily in allWords
              if firstWord(wordFamily)[:firstWord(wordFamily).find(',')].endswith(inflections)])

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
list_of_forms = [form[3] for form in searchBase]

# 1.wyszukaj core
# 2. zwróć cały wyraz
# 3. pokaż wyraz po nim
indexes = [[] for i in range(maxFeatures)]
for i, forms in enumerate(list_of_forms):
    for form in forms:
        indexes[i] = indexes[i] + indices(book_split, form)

next_indexes = [ [element + 1 for element in index] for index in indexes ]

next_word = [ [book_split[element] for element in index] for index in next_indexes ]

pairs = [ [(book_split[element], book_split[element+1]) for element in index] for index in indexes ]

#values = np.array([1,2,3,1,2,4,5,6,3,2,1])
#searchval = 3
#ii = np.where(values == searchval)[0]

#findAllCores = [
#        (
#            element[0],
#            [instance for instance in re.findall('\s\S*' + str(element[0]) + '\S*\s', book)
#            if instance in element[3]]
#        )
#        for element in searchBase
#                ]
#

#B = [
#        (
#            element[0],
#            re.findall('\s\S*' + str(element[0]) + '\S*\s', book)
#        )
#        for element in searchBase
#                ]




#m = re.search('(?<=abc)def', 'abcdef')

#del lista


# twórz core czasowników

    

#czaswoniki mają skapitalizowane rzeczowniki! NAPRAW!        
# znaleźć dowolny tekst i sprawdzić które słowa są najczęstsze
# podzielić słowa na core i końcówki, stworzyć zbiór końcówek
# z tekstu wydobyć słowa z końcówkami, sprawdzić czy są w naszym zbiorze czasowników.
# Sprawdzic w jakim są otoczeniu, tzn. jaki tworzą kontekst.