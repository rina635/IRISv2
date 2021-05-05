#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Assignment: Team 3 - Rafeef Baamer, Ashish Hingle, Rina Lidder, & Andy Nguyen
Description: IRIS (short for INSTRUCTIVE RESPONSE INTERVIEW SIMULATOR) is a chatbot solution that primarily serves as an interview simulator to help users
practice interview questions in a broad context. This project aims to implement the solution as an extension to the ELIZA model, described as the first chatbot
system (Weizenbaum 1976). It is primarily designed for students, but any professional can use the service to practice common interview questions and receive
feedback based on their responses. After the practice session, the chatbot will provide the user a rating score of how they did and describe some aspects that
can be improved.  

This file is to extract the behavioral-interview questions for IRIS

Program Logic webscraper.py:
    1. Load the url
    2. Parses out the relevant text from the HTML tags
    3. Creates 7 individual dataframes by indexing the website text
       for each section.
    4. Create one final dataframe by merging each category's dataframe
       together.
    5. Export the csv file containing the questions.
    
Resources used for this code come from:
    - [1] https://stackoverflow.com/questions/28396036/python-3-4-urllib-request-error-http-403
    - [2] https://stackoverflow.com/questions/13682044/remove-unwanted-parts-from-strings-in-a-column
    
"""
#import libraries.
import bs4, urllib.request
import numpy as np
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import csv, sys, os, re
import pandas as pd


#Attach the url for our career questions data source
url = 'https://www.contractrecruiter.com/list-behavioral-interview-questions/'

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read()
#Parse out the webpage section where it contains the relevant data needed.
page_soup = soup(html, 'html.parser')
whole_section = page_soup.find('div',{'class':'fl-post-content clearfix'})
whole_section.find('p')
#only getting the text from the paragraph no HTML tags.
all_text = whole_section.getText()
#break apart each line.
split_text = all_text.split('\n')

#Uses variable q regex to locate where in the text there is a digit followed by a capital letter
#Specifically used to identify where the question text is.
q = re.compile("^\d+.\s[A-Z]")

#Gather all questions in Leadership Category and create a df
#Using indexing to gather the questions
leadership =  split_text[63:90]
#Using indexing to gather the category name.
lead_head = split_text[63]
#Create a list of just the question by searching using q
lead_qlist = list(filter(q.match, leadership))

#Creates the leadership dataframe with the questions and category name.
df_leadership = pd.DataFrame(lead_qlist, columns = ['Question'])
df_leadership['Category'] = lead_head

#Gathers all questions in Teamwork Category and creates a df
teamwork =  split_text[90:114]
team_head = split_text[90]
team_qlist = list(filter(q.match, teamwork))

df_team = pd.DataFrame(team_qlist, columns = ['Question'])
df_team['Category'] = team_head

#Gathers all questions in Goals and Ambition category and creates a df
goals =  split_text[114:140]
goals_head = split_text[114]
goals_qlist = list(filter(q.match, goals))

df_goals = pd.DataFrame(goals_qlist, columns = ['Question'])
df_goals['Category'] = goals_head


#Gathers all questions in Stress Management category and creates a df
stress =  split_text[140:175]
stress_head = split_text[140]
stress_qlist = list(filter(q.match, stress))

df_stress = pd.DataFrame(stress_qlist, columns = ['Question'])
df_stress['Category'] = stress_head

#Gathers all questions in Morality and Ethics category and creates a df
ethics =  split_text[175:199]
ethics_head = split_text[175]
ethics_qlist = list(filter(q.match, ethics))

df_ethics = pd.DataFrame(ethics_qlist, columns = ['Question'])
df_ethics['Category'] = ethics_head


#Gathers all questions in Interactions category and creates a df
interact =  split_text[218:240]
interact_head = split_text[218]
interact_qlist = list(filter(q.match, interact))

df_interact = pd.DataFrame(interact_qlist, columns = ['Question'])
df_interact['Category'] = interact_head


#Gathers all questions in Miscellaneous category and creates a df
misc =  split_text[240:261]
misc_head = split_text[240]
misc_qlist = list(filter(q.match, misc))

df_misc= pd.DataFrame(misc_qlist, columns = ['Question'])
df_misc['Category'] = misc_head


#Puts all dataframes into one large one by concating them
frames = [df_leadership, df_team, df_stress, df_goals, df_ethics, df_interact, df_misc]
result = pd.concat(frames)

#Remove numbers from questions 
result['Question'] = result['Question'].str.replace(r'\d\d*\.', '')       
#remove the 'Questions about' phrase from each of the category labels
result['Category'] = result['Category'].str.replace(r'Questions about ', '')


#Export the final dataframe as csv without the index.
abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath) + '/questions3333.csv'
result.to_csv(dname, encoding="utf-8", index=False)
