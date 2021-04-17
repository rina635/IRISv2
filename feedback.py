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
from gensim.summarization import keywordss

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
    lines = file.read().splitlines() #creates a list of each line in log file


#Printing these just to see what I'm dealing with here.
len(lines)
lines[0]
lines[1]
lines[2]
lines[3]
lines[4]

'''
grab nounn chunks from each question into a list
search response list for substrings that contains any
add list of scores to dictionary'''

#user response stores starting at index 3 and 4 lines after that
#Creating a searate list of the user's answers for analyses.
user_responses = []
for i in range(3, len(lines),4):
    response = (lines[i])
    clean_response = response.split(': ')
    resp_only = clean_response[1]
    user_responses.append(resp_only)

#Creates list of the questions IRIS asked but removes the chatbot's name
questions = []
for i in range(1, len(lines),4):
    q = lines[i]
    clean_q = q.split(': ')
    q_only = clean_q[2]
    questions.append(q_only)
    
    
#Create dictionary of question and answers:
 #https://careerkarma.com/blog/python-convert-list-to-dictionary/
qa_dictionary = dict(zip(questions, user_responses))    
#https://realpython.com/iterate-through-dictionary-python/#iterating-through-keys-directly
#prints the noun chunks for each of the questions - want to search the respective answers to see if they contain them to dictate if appropriate context
for key in qa_dictionary:
    doc = nlp(key)
    for np in doc.noun_chunks:
        print(np.text)
#https://stackoverflow.com/questions/12376079/check-if-any-value-of-a-dictionary-matches-a-condition
#https://www.programiz.com/python-programming/methods/built-in/any

#Returns true or false if string is in answer but has to be the entire string
#doesn't do substring bc one of answers only had this will print True
any(v == 'blah ba' for v in qa_dictionary.values())
    

#Create a list of keyword criteria from dictionary?
#Evaluate the list of user responses based on that


#Locates the Leadership Category Index
def find_leadership(list):
    lead_q = [i for i in lines if re.search(r'Leadership', i) ]
    category_L = (", ".join(lead_q))
    leadership_index = lines.index(category_L)
    return leadership_index

#Uses Leadership Category Index to find the question asked
def lead_q(list):
    leadership_index = find_leadership(lines)
    leadership_q =  leadership_index + 1
    question = list[leadership_q]
    return question

def lead_response(list):
    question_index = find_leadership(lines) + 1
    l_index = question_index + 1
    l_response = list[l_index]
    return l_response

#Prints out the leadership question Iris asked.
lead_q(lines)
#Prints out user's response to leadership question.
lead_response(lines)

text = lead_response(lines)


#Before we can evaluate how well the user's answer is, must remove the chatname
def clean_response(answer):
    clean_a = answer.split(': ')
    return clean_a[1]

#To assess each question approrpiately, must remove extraneous text 
def clean_question(question):
    clean_q = question.split(': ')
    return clean_q[2]



'''
RINA NOTES TO SELF.
#If i want to separate by Category, find category and then that index + 2 includes the questions
#and the user's response to question.
#https://stackoverflow.com/questions/29696641/find-a-specific-pattern-regular-expression-in-a-list-of-strings-python
lead_q = [i for i in lines if re.search(r'Leadership', i) ]
#https://stackoverflow.com/questions/13207697/how-to-remove-square-brackets-from-list-in-python
category_L = (", ".join(lead_q))

type(lead_q)
category_L = str(lead_q)
print(category_L)
#https://www.programiz.com/python-programming/methods/list/index
lines.index(category_L)

'''