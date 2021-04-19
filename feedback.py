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
import numpy as np
nlp = spacy.load('en_core_web_sm')

#Finds location of log file
#https://stackoverflow.com/questions/33832184/open-a-log-extension-file-in-python
abspath = os.path.abspath(sys.argv[0])
for filename in os.listdir(abspath):
    if filename == 'user_response.log':
       f  = open(os.path.join(abspath, 'user_response.log'), "r")
       #print (f.read()) - Don't need just to check.
      
#https://stackoverflow.com/questions/37912556/converting-a-log-file-into-a-csv-file-using-python
#Opens log file as a list
with open('user_response.log') as file:
    interview = file.read().splitlines()
    
#Searches Interview list to find all the questions IRIS asked during interview.
def q_search(list):
    iris_questions = [i for i in list if re.search(r'IRIS: Question', i)]
    #Loop here will clean so only get the question text.
    questions = []
    for i in range(0, len(iris_questions)):
        q = iris_questions[i]
        clean_q = q.split(': ')
        q_only = clean_q[2]
        questions.append(q_only)
    return questions

#seperate out all of IRIS's statements - Might get rid of category altogether.
all_iris = [i for i in interview  if re.search(r'IRIS:', i) ]
#Use list comprehension to isolate the user's answers
#https://stackoverflow.com/questions/41125909/python-find-elements-in-one-list-that-are-not-in-the-other
answers_list = [item for item in interview if item not in all_iris]
#Gets rid of empty rows
answers_list = list(filter(None,answers_list))
#Removes * character - Final list of answers:
answers = [ x for x in answers_list if "*" not in x ]
#Final list of questions asked.
questions = q_search(interview)

#Create a dataframe of Interview session with just the questions and answers
interview_df = pd.DataFrame(list(zip(questions, answers)), columns = ['questions', 'answers'])
#if user says end session delete row.
interview_df = interview_df[interview_df.answers != 'end session']
#Third column is the score, defaults to 0.
interview_df['score'] = 0

#SEARCH FOR (*) DENOTING OVERTIME:
##https://stackoverflow.com/questions/36519939/using-index-with-a-list-that-has-repeated-elements  
##https://stackoverflow.com/questions/3675144/regex-error-nothing-to-repeat   
def overtime_q(list):
    asterisk = re.compile(r"(\*)")    
    overtime_qs = []
    for i in range(len(interview)):
        if re.search(asterisk, interview[i]):
            q_index = i - 2
            overtime_q = interview[q_index]    
            overtime_qs.append(overtime_q)
            
    return overtime_qs

#Cleaning up overtime questoin list by removing asterisk and blank lines of list.
#https://stackoverflow.com/questions/3416401/removing-elements-from-a-list-containing-specific-characters
all_overtime = overtime_q(interview)    
all_overtime = [ x for x in all_overtime if "*" not in x ]
all_overtime = list(filter(None,all_overtime))

#Remove IRIS: Question: from list - Clean so can search dictionary
clean_overtime_q =[]
for i in range(0, len(all_overtime)):
    q = all_overtime[i]
    clean_q = q.split(': ')
    q_only = clean_q[2]
    clean_overtime_q.append(q_only)

#https://stackoverflow.com/questions/37976823/how-to-conditionally-update-dataframe-column-in-pandas-based-on-list
#1. SCORE - if user went over time for that questions -2 from score
interview_df.loc[interview_df.questions.isin(clean_overtime_q), 'score'] = interview_df['score'] - 2

#Creating a list of all the answers where user responded in less than 3 sentences.
short_answers = []
for i in range(0, len(answers)):
    sent_tokens = sent_tokenize(answers[i])
    if len(sent_tokens) < 3:
        short_answers.append(answers[i])

#2. SCORE - if user's answer is too short -2 from score again.
interview_df.loc[interview_df.answers.isin(short_answers), 'score'] = interview_df['score'] - 2

    
#3. If user's answers used less than 1 named entity
interview_df.loc[interview_df.answers.isin(no_ents), 'score'] = interview_df['score'] - 2
#Function iterates through all answers to see if user used at least 1 named entity, if they did it adds to the entity list
#Need a list of entities the answer had to check if the length was at least 1.
#But want a dictionary of answer and respective list of entities
#Want the output to be a list of the answers where user did not meet this criteria to decide which rows in the dataframe we need to subtract from.    
def get_ents(answers):
    entity = []
    for i in range(0, len(answers)):
        doc = nlp(answers[i])
        for ent in doc.ents:
            x = (ent.label_)
            entity.append(x)   
            
    return entity

def eval_ents():
    no_ents = []
    entity = get_ents()
    if len(entity) > 1:
        #put the list of answers into no_ents
