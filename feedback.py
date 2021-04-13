#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 15:45:28 2021

@author: Rina
"""
import os, sys, re
import spacy
from nltk import pos_tag
  
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