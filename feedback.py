#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 15:45:28 2021

@author: Rina
"""
import os, sys, re
import spacy
from nltk import pos_tag
import pandas as pd
import csv
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
from nltk import sent_tokenize

nlp = spacy.load('en_core_web_sm')

#Finds location of log file
#https://stackoverflow.com/questions/33832184/open-a-log-extension-file-in-python
abspath = os.path.abspath(sys.argv[0])
for filename in os.listdir(abspath):
    if filename == 'user_response.log':
       f  = open(os.path.join(abspath, 'user_response.log'), "r")
       print (f.read())
       

#https://stackoverflow.com/questions/37912556/converting-a-log-file-into-a-csv-file-using-python
with open('user_response.log') as file:
    interview = file.read().splitlines() #creates a list of each line in log file

#seperate out all of IRIS's statements - Might get rid of category altogether.
##https://stackoverflow.com/questions/29696641/find-a-specific-pattern-regular-expression-in-a-list-of-strings-python
all_iris = [i for i in interview  if re.search(r'IRIS:', i) ]
#Use list comprehension to isolate the user's answers
#https://stackoverflow.com/questions/41125909/python-find-elements-in-one-list-that-are-not-in-the-other
answers_list = [item for item in interview if item not in all_iris]
#Gets rid of empty rows
answers_list = list(filter(None,answers_list))

def q_search(list):
    iris_questions = [i for i in list if re.search(r'IRIS: Question', i) ]
    return iris_questions

iris_questions = q_search(interview)
#removes IRIS: and Question Numbers from question text:
questions = []
for i in range(0, len(iris_questions)):
    q = iris_questions[i]
    clean_q = q.split(': ')
    q_only = clean_q[2]
    questions.append(q_only)

   
#Create dictionary of question and answers:
 #https://careerkarma.com/blog/python-convert-list-to-dictionary/
qa_dictionary = dict(zip(questions, answers_list))    
#https://realpython.com/iterate-through-dictionary-python/#iterating-through-keys-directly
#prints the noun chunks for each of the questions - want to search the respective answers to see if they contain them to dictate if appropriate context
for key in qa_dictionary:
    doc = nlp(key)
    for np in doc.noun_chunks:
        x = (np.text)
        #print (x, key) #specific token and question it comes from.
        print(x, np)
#https://stackoverflow.com/questions/12376079/check-if-any-value-of-a-dictionary-matches-a-condition
#https://www.programiz.com/python-programming/methods/built-in/any

#Returns true or false if string is in answer but has to be the entire string
#doesn't do substring bc one of answers only had this will print True
any(v == 'blah ba' for v in qa_dictionary.values())

#basic scoring method for answer lists - Need to revise to add as value to dicitonary
len_score = []
for item in answers_list:
    sent = sent_tokenize(item)
    if len(sent) > 3:
        s = 2
        len_score.append(s)
    else:
        s = -2
        len_score.append(s)