#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Final Assignment: Team 3 - Rafeef Baamer, Ashish Hingle, Rina Lidder, & Andy Nguyen
Description: IRIS (short for INSTRUCTIVE RESPONSE INTERVIEW SIMULATOR) is a chatbot solution that primarily serves as an interview simulator to help users
practice interview questions in a broad context. This project aims to implement the solution as an extension to the ELIZA model, described as the first chatbot
system (Weizenbaum 1976). It is primarily designed for students, but any professional can use the service to practice common interview questions and receive
feedback based on their responses. After the practice session, the chatbot will provide the user a rating score of how they did and describe some aspects that
can be improved.
This file is the initial file used to receive user input. To score user input, please use feedback.py.
The main goals with IRIS were to:
- Create a model that can preprocess, algorithmically-process, and generate sentences. 
- Provide real-time responses to replicate a typical in-person interview. 
- Provide meaningful feedback to the user.
Usage Instructions:
1) Run the iris.py file
2) Enter user name on prompt
3) Enter the number of desired questions on prompt
4) Read through the question and enter the response
5) After all questions are answered, or program is terminated, use the associated feedback.py file to score the responses
'HELP' can be used for additional information, and 'END SESSION' can be used to terminate the program early.
Logic:
External Library dependencies:
NLTK, Pandas 
Resources used for this lab come from the materials provided in the AIT 590 course materials.
- [1] Lecture powerpoints (AIT 590)
- [2] Stanford University Prof. Dan Jurafsky's Video Lectures (https://www.youtube.com/watch?v=zQ6gzQ5YZ8o)
- [3] Joe James Python: NLTK video series (https://www.youtube.com/watch?v=RYgqWufzbA8)
- [4] w3schools Python Reference (https://www.w3schools.com/python/)
- [5] regular expressions 101 (https://regex101.com/)
- [6] Timer examples understood from: https://stackoverflow.com/questions/15528939/python-3-timed-input
- [7] Logging files: https://stackoverflow.com/questions/38409450/logging-to-python-file-doesnt-overwrite-file-when-using-the-mode-w-argument-t
- [8] Logging files: https://www.youtube.com/watch?v=-ARI4Cz-awo&t=616s
- [9] 2 second delay - https://www.guru99.com/python-time-sleep-delay.html
"""
# import and initialize libraries
import random, re , os, sys, logging, time
import pandas as pd 
from datetime import datetime
from threading import Thread
import nltk
from nltk.corpus import words

# creates a log file of interview session, will rewrite the log file every time code executed.
# code referenced from source [7] and [8]
log_filename = 'user_response.log'
logging.basicConfig(filename= log_filename, level = logging.DEBUG, format = '%(message)s')
handler = logging.FileHandler(log_filename, 'w+')

# global variables for IRIS and formatted name
bot_name = 'IRIS'
bot_formatted_name = 'IRIS: '

'''----------------------------------------------
 Defined functions
----------------------------------------------'''

# customize IRIS's greeting based on time of day
def greeting():
    # get the current time
    now = datetime.now()
    time_holder = now.strftime('%H:%M')
    
    # logic to choose which greating to display
    if time_holder > '12:00' and time_holder < '16:00':
        greeting = 'Good afternoon'
    elif time_holder > '16:01' and time_holder < '23:59':
        greeting = 'Good evening'
    else:
        greeting = 'Good morning'
    return greeting

# function to display IRIS initial conversation and instructions
def start_conversation():
    # first interaction with user
    print('{}{}, I am {} the Instructive Response Interview Simulator. Here to help you prepare for your next interview!'
          .format(bot_formatted_name, greeting(), bot_name))
    


    # check if name is empty or not String before contnuing, if so do not move forward until a name is input
    while True:
        name = input("Before we begin, what is your name?\n")
        if any(char.isdigit() for char in name) or name == "" or re.match(r'^\s*$',name):    
            print("Please enter a valid name that must be string")
            continue
        break


    print(bot_formatted_name + 'Nice to meet you, {}! To end the session, type "END SESSION". For help, type "HELP".'.format(name))  
    # ask if user's has used IRIS before
    new_user = input(bot_formatted_name + 'Is this your first time interacting with me?\nType "Yes" or "No"\n')     

    # check for anything other than yes or no being input, if so do not move forward
    while not (new_user.lower() == 'yes' or new_user.lower() == 'no'):
        new_user = input(bot_formatted_name + 'Invalid response. I need to know if this is your first time using IRIS?\n') 
    
    # if yes is entered, display the 'help' instructions, else brief message   
    if new_user.lower() == 'yes':
        iris_instructions()
    elif new_user.lower() == 'no':
        print('\n' + bot_formatted_name + 'Great! If you need assistance please type in "HELP".')
    
    # delay the program for 2 seconds before beginning the program
    # code referenced from source [9]
    time.sleep(2)
    
    #print next steps
    print('Let\'s get started!\n')
    print('----------------------')
    return name

# calls the instructions for using the program 
def iris_instructions():
    print('\n' + bot_formatted_name + '''Welcome! My job here is to help you practice your interview skills. Here are the instructions to interact with me:
1) Choose the number of questions (5 - 10 questions).
2) Answer each question within 2 minutes.
3) After you have completed your session, use the feedback.py file to score your responses.
Some information to help you succeed with your preperation:
- The goal of interacting with me is to ensure you're able to answer the questions in the best way you can.
- You should discuss specific experiences and details, including names of companies, organizations and supervisors.
- Express your past experiences in detail and use descriptive language. Aim for at least 3 full sentences.
- I will allow you to submit a response even if you exceed the 2-minute time limit. However, this will affect your score.
- Any blank responses will not be graded.\n''')
    # wait 5 seconds before displaying next step
    time.sleep(5)

# loads the questions from the CSV
def load_questions(file):
    data = pd.read_csv(file)     
    return data

#Chooses a question from beginning to end of dataset - Won't repeat question.
def choose_question(dataframe):
    lst = range(0, len(dataframe))
    rand_numb = random.sample(lst, 1)
    num = rand_numb[0]
    ques = dataframe.at[num, 'Question']
    cat = dataframe.at[num, 'Category']
    return ques, cat

#IRIS will log when the user has exceeded 2 mins without a response with asterisk.
def idle_check():
    time.sleep(120)
    if answer != None:
        print('\n')
    elif answer == 'end session':
        print('\n')
        
    elif answer == 'END SESSION':   
        print('\n')
        
    #Time exceeded character won't print to console but will be logged.
    x = '*'
    logging.debug(x) 

'''
def handle_nonesense(answer):
    token_answer = nltk.word_tokenize(answer)
    for i in token_answer:
        if i not in words.words():
            #print("Please provide answer with real words")
            return False 
    return True
'''

'''----------------------------------------------
 start of code execution
----------------------------------------------'''

# initialize the response and counter variables
response = ''
answer = None
question_counter = 0
    
# save the path to the current working directory
abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath) + '/questions.csv'

# load questions from the dataset into data frame
questions_df = load_questions(dname)

# start the conversation
userName = start_conversation()

# reformat the user's name for the chat.
user_formatted_name = userName + ': '

# validates integers only and display a message anything else is entered 

while True:
    print("How many questions would you like for today? \nPlease select a number between 5 and 10.\n")
    n = input()
    try:
        n = int(n)
    except:
        print("please enter a numeric digit")
        continue
    if n < 5 or n >10:
        print("Invalid number of questions. Please select a number between 5 and 10")
        continue
    break


# interview session will continue until the number of questions has been reached    
while question_counter < n: 
    # save the question and category from the dataset 
    question, category = choose_question(questions_df)
    
    # keeps track of question number
    question_counter = question_counter + 1
    
    # print the question and category for the user
    print('\n{}The category is: {}'.format(bot_formatted_name, category))
    print('{}Question {}: {}'.format(bot_formatted_name, question_counter, question))
    
    # start timining how long user takes to respond after question has been printed out.
    th = Thread(target = idle_check)
    th.daemon = True
    th.start()
    
    # logs IRIS Category and question declaration
    logging.debug('{}The category is: {}'.format(bot_formatted_name, category))
    logging.debug('{}Question {}: {}\n'.format(bot_formatted_name, question_counter, question))

    # takes user's input
    response = input(user_formatted_name)
    #logging user's response into log file without their name
    log_response = logging.debug('{}'.format(response))

    if response:
         # response to whitespace only, subtracts 1 from the counter
        if re.match(r'^\s*$',response): 
             print('IRIS: Okay, I will move on to the next question.')
             question_counter = question_counter - 1 

        # runs help function with instructions when user calls for help, subtracts 1 from the counter
        elif re.match(r'HELP', response, re.IGNORECASE):
            iris_instructions()
            question_counter = question_counter - 1 

        # exits the conversation if user requests to end session
        elif re.match(r'END SESSION', response, re.IGNORECASE):
            break
    else:
        print('IRIS: You did not answer the question. I will move to the next question')
   
#Once question limit is reached/user ends session , will output this:
print('{}It was really great learning more about you, {} this is the end of our session.'.format(bot_formatted_name, userName))
handler.close()
sys.exit()