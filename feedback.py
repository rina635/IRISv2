#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 15:45:28 2021

@author: Rina
"""
#importing libraries
import os, sys, re, csv, spacy
from nltk import pos_tag
import pandas as pd
from nltk import sent_tokenize
import numpy as np
from datetime import datetime
nlp = spacy.load('en_core_web_sm')

#Finds location of log file
#https://stackoverflow.com/questions/33832184/open-a-log-extension-file-in-python
#https://stackoverflow.com/questions/37912556/converting-a-log-file-into-a-csv-file-using-python
#https://stackoverflow.com/questions/28836781/reading-column-names-alone-in-a-csv-file

#Load sample answers for feedback.
abspath = os.path.abspath(sys.argv[0])
#Open dataset as a dataframe.  
with open('questions_answers.csv', encoding='utf8', errors='ignore') as f:  
    reader = csv.reader(f)
    i = next(reader)
    rest = list(reader)
    all_questions_df = pd.DataFrame(rest, columns = ['index', 'question', 'category', 'sample'])

#Load log from IRIS.py as a list.
with open('user_response.log') as file:
    interview = file.read().splitlines()

#If user exited session then need to execute so that can capture before user requested to end the session.
def whole_interview(list):    
    for i in range(len(list)):
        if re.search('end session', list[i]):
            end_index = i
            beg_index = 0
            list = list[beg_index:end_index]
        elif re.search('END SESSION', list[i]):
            end_index = i
            beg_index = 0
            list = list[beg_index:end_index]
    return list        
    
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

#Isolates the answer's from the user.
#Adpated from: #https://stackoverflow.com/questions/41125909/python-find-elements-in-one-list-that-are-not-in-the-other
def a_search(interview):
#seperate out all of IRIS's statements
    all_iris = [i for i in interview  if re.search(r'IRIS:', i) ]
    #Use list comprehension to isolate the user's answers   
    answers_list = [item for item in interview if item not in all_iris]
    #Gets rid of empty rows
    answers_list = list(filter(None,answers_list))
    #Removes * character IRIS denoted if they went overtime.
    answers = [ x for x in answers_list if "*" not in x ] 
    return answers

#Only getting the interview before the session ends
interview_2 = whole_interview(interview)
#Retrieving all user's answers
answers = a_search(interview_2)
#Final list of questions asked.
questions = q_search(interview_2)

#Create a dataframe of Interview session with just the questions and answers
#Df removes any questions where the user had an empty response.
interview_df = pd.DataFrame(list(zip(questions, answers)), columns = ['question', 'answers'])
#Third column is the score, defaults to 7.
interview_df['score'] = 7
#fourth column is the feedback
interview_df['feedback'] = ''

#merge question and add sample answer into the main dataframe
interview_df = pd.merge(interview_df, all_questions_df[['question','sample']], left_on='question', 
                        right_on='question', how ='inner')

#SEARCH FOR (*) DENOTING OVERTIME:
##https://stackoverflow.com/questions/36519939/using-index-with-a-list-that-has-repeated-elements  
##https://stackoverflow.com/questions/3675144/regex-error-nothing-to-repeat   
def overtime_q(list):
    asterisk = re.compile(r"(\*)")    
    overtime_qs = []
    for i in range(len(interview)):
        if re.search(asterisk, interview[i]):
            #Question is 2 rows away, using index to locate question in list
            q_index = i - 2
            overtime_q = interview[q_index]    
            overtime_qs.append(overtime_q)
    return overtime_qs

#Cleaning up overtime question list by removing asterisk and blank lines of list.
#https://stackoverflow.com/questions/3416401/removing-elements-from-a-list-containing-specific-characters

all_overtime = overtime_q(interview_2)    
all_overtime = [ x for x in all_overtime if "*" not in x ]
all_overtime = list(filter(None,all_overtime))

#Remove IRIS: Question: so only getting the question text.
clean_overtime_q =[]
IRIS_q_string = 'IRIS: Question:'
if IRIS_q_string in all_overtime:
    for i in range(0, len(all_overtime)):
        q = all_overtime[i]
        clean_q = q.split(': ')
        q_only = clean_q[2]
        clean_overtime_q.append(q_only)
else:
    clean_overtime_q.append('')        

#https://stackoverflow.com/questions/37976823/how-to-conditionally-update-dataframe-column-in-pandas-based-on-list
#1. SCORE - if user went over time for that questions -2 from score column
interview_df.loc[interview_df.question.isin(clean_overtime_q), 'score'] = interview_df['score'] - 2
#if user went over time then will add this feedback:
interview_df.loc[interview_df.question.isin(clean_overtime_q), 'feedback'] = interview_df['feedback'] + '''
You took too long to answer.'''
#adds feedback for responses that did not lose points
interview_df.loc[~interview_df.question.isin(clean_overtime_q), 'feedback'] = interview_df['feedback'] + '''
You answered within 2 minutes.'''

#Creating a list of all the answers where user responded in less than 3 sentences.
short_answers = []
for i in range(0, len(answers)):
    #Tokenizes each answer and checks the length of sentence tokens.
    sent_tokens = sent_tokenize(answers[i])
    if len(sent_tokens) < 3:
        short_answers.append(answers[i])

#2.SCORE - if user's answer is too short -2 from score column.
interview_df.loc[interview_df.answers.isin(short_answers), 'score'] = interview_df['score'] - 2
#adds feedback for responses that lost points
interview_df.loc[interview_df.answers.isin(short_answers), 'feedback'] = interview_df['feedback'] + '''
Your answer is too short. You should use the time to express your answer with more detail.'''
#adds feedback for responses that did not lose points
interview_df.loc[~interview_df.answers.isin(short_answers), 'feedback'] = interview_df['feedback'] + '''
Your answer was sufficient in length.'''

#uses spacy to identify entities, saves entity text and label to a dictionary
def get_ents(responses):
    entity ={}

#loop through each answer, and save the entities from the text
    for i in range(0, len(answers)):
        doc = nlp(answers[i])
        for ent in doc.ents:
            x = (ent.text)
            y = (ent.label_)
            
            # check to avoid duplicated keys
            if x not in entity.keys():
                entity[x] = y    
    return entity

#evaluates the sentences to see if an Entity is present. If a sentence does not have an entity, save it to no_entity list.
def eval_ents(responses):
    # Create a new empty dictionary
    accpetable_entity_dict = {} 
    # Create a new empty list
    acceptable_entity_list = []  
    no_entity = []

    # run the get_ents method to create a list of all entities
    all_entity = get_ents(responses)
    
    # create an acceptable entity list with only desired entities (persons and organizations)
    for key, value in all_entity.items():
        if value == 'ORG' or value == 'PERSON':
            accpetable_entity_dict[key] = value
            acceptable_entity_list.append(key)

    #loop through the responses to isolate responses with no entities
    for i in range(0, len(answers)):
        for j in range(0, len(acceptable_entity_list)):
            
            # search for the entity within the sentence
            if re.search(acceptable_entity_list[j], answers[i]):
                #if an entity was found, but was added to the no_entity list earlier, try to remove it from the list
                try:
                    no_entity.remove(answers[i])
                except ValueError:
                    pass  
                #if a entity is found in a sentence, no need to search for more entities in that sentence, break to next sentence
                break
            #check if a sentence is already in the cumulative list, dont do anything if true (otherwise duplicates sentences)
            elif answers[i] in no_entity:
                pass
            #add the sentence to the cumulative list
            else:
                no_entity.append(answers[i])
                
        #condition to add items to the no_entity list if there are 0 entities in any of the answers
        if not acceptable_entity_list:
            no_entity.append(answers[i])
    return no_entity

#Function iterates through all answers to see if user used at least 1 named entity, if they did it adds to the entity list
#Need a list of entities the answer had to check if the length was at least 1.
#But want a dictionary of answer and respective list of entities
#Want the output to be a list of the answers where user did not meet this criteria to decide which rows in the dataframe we need to subtract from.    

# evaluate the answers and return as a list
no_ents = eval_ents(answers)

#3. If user's answers used less than 1 named entity
interview_df.loc[interview_df.answers.isin(no_ents), 'score'] = interview_df['score'] - 3
#add the feedback to the dataframe
#adds feedback for responses that lost points
interview_df.loc[interview_df.answers.isin(no_ents), 'feedback'] = interview_df['feedback'] + '''
You did not include identifying information, such as company names. Including these details can give the 
interviewer a better understanding of your experience.'''
#adds feedback for responses that did not lose points
interview_df.loc[~interview_df.answers.isin(no_ents), 'feedback'] = interview_df['feedback'] + '''
You included identifying information for the organizations you worked for. Great work!'''

# Compile the feedback to be printed and saved to log
# declare a feedback holder
compl_feedback = 'IRIS FEEDBACK'

#get current date and time for the log file
now = datetime.now()
current_time = now.strftime('%H:%M')
current_date = now.strftime('%B %d, %Y')

#add the date and time to the feedback holder
compl_feedback += '\nGenerated on: ' + current_date + ' at ' + current_time

#loop through the dataframe and add to the feedback holder
for ind in interview_df.index: 
    compl_feedback += '\n\nQuestion ' + str(ind + 1) + ': ' + interview_df['question'][ind]
    compl_feedback += '\nAnswer ' + str(ind + 1) + ': ' + interview_df['answers'][ind]
    compl_feedback += '\nScore: ' + str(interview_df['score'][ind]) + '/7'
    compl_feedback += '\nDetailed Feedback: ' + interview_df['feedback'][ind]
    compl_feedback += '\nSample answer: "'
    compl_feedback += interview_df['sample'][ind] + '"'
#print the feedback to console
print(compl_feedback)

#save the feedback to a text file.
f = open('feedback.txt', 'w', encoding='utf-8')
f.write(compl_feedback)
f.close()
print('\nThe graded feedback file has been created for your reference.')
