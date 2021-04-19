
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Final Assignment: Team 3 - Rafeef Baamer, Ashish Hingle, Rina Lidder, & Andy Nguyen

#general logic
# load all questions from csv file 
# take in name, number of questions
# start timer
# pick a question from each category 
# take in answer input 
# if input > 90 seconds, ask if they want a hint
# evaluate answer (NER, POS Tagging)
# add question and answer to log file (whole conversation) 
# exit and print final feedback

Resources used for this lab come from the materials provided in the AIT 590 course materials.
- Lecture powerpoints (AIT 590)
- Stanford University Prof. Dan Jurafsky's Video Lectures (https://www.youtube.com/watch?v=zQ6gzQ5YZ8o)
- Joe James Python: NLTK video series (https://www.youtube.com/watch?v=RYgqWufzbA8)
- w3schools Python Reference (https://www.w3schools.com/python/)
- regular expressions 101 (https://regex101.com/)
- Timer examples understood from: https://stackoverflow.com/questions/15528939/python-3-timed-input
"""
#import and initialize libraries
import random, re, nltk, os, sys, logging, time
import pandas as pd 
from nltk.tokenize import word_tokenize
from datetime import datetime
from threading import Thread

#Creates a log file of all user responses will rewrite the log file every time code executed.
#https://stackoverflow.com/questions/38409450/logging-to-python-file-doesnt-overwrite-file-when-using-the-mode-w-argument-t
#https://www.youtube.com/watch?v=-ARI4Cz-awo&t=616s
log_filename = 'user_response.log'
logging.basicConfig(filename= log_filename, level = logging.DEBUG, format = '%(message)s')
handler = logging.FileHandler(log_filename, 'w+')

# global variables
bot_name = 'IRIS'
#Name used in chat
bot_formatted_name = 'IRIS: '


# this function randomly generates a number between 1 and maximum from df
def randomNumbGen(max_numb):
    r = random.randint(1, max_numb)
    return r

#Customizes IRIS greeting based on time of day.
def greeting():
    now = datetime.now()
    time_holder = now.strftime('%H:%M')
               
    if time_holder > "12:00" and time_holder < "16:00":
        greeting = "Good afternoon"
    elif time_holder > "16:01" and time_holder < "23:59":
        greeting = "Good evening"
    else:
        greeting = "Good morning"
    
    return greeting


# prints IRIS's response based on the number of choices and a list of possible choices
def iris_response(numb_choices, choices):
    
    rand_numb = randomNumbGen(numb_choices)
    print(choices[rand_numb])

# function to start IRIS
def start_conversation():
    # start of program and logic
    # first interaction with user
    print('{}{}, I am {} the Instructive Response Interview Simulator. Here to help you prepare for your next interview!'.format(bot_formatted_name, greeting(), bot_name))
    
    
    # save the users name as an input
    name = input(bot_formatted_name + 'Before we begin, what is your name?\n')   # ask for their name and saves inputted value to userName variable
    
    # check if name is empty before contnuing
    while name == '':
        name = input(bot_formatted_name + 'Invalid response. I need to know how to address you. What is your name?\n')   # ask for their name and saves inputted value to userName variable
    
    #Provides instructions to user.
    print(bot_formatted_name + 'Nice to meet you, {}! To end the session, type "END SESSION". For help, type "HELP".'.format(name))  
    
    new_user = input(bot_formatted_name + 'Is this your first time interacting with me?\nType "Yes" or "No"\n')   # ask if first time     

    
    while not (new_user.lower() == 'yes' or new_user.lower() == 'no'):
        new_user = input(bot_formatted_name + 'Invalid response. I need to know if this is your first time using IRIS?\n')   # ask for their name and saves inputted value to userName variable
  
    if new_user.lower() == 'yes':
        get_help()
    elif new_user.lower() == 'no':
        print(bot_formatted_name + 'Great! If you need assistance please type in "HELP".')
    #2 second delay - https://www.guru99.com/python-time-sleep-delay.html
    time.sleep(2)
    print('Let\'s get started!\n')
    print('----------------------\n')
    return name

# calls the instructions for using the program 
def get_help():
    print('\n' + bot_formatted_name + '''Welcome my job here is to help you practice for your interview by providing unlimited number of questions.
     Each question is graded on a scale from 1-10 and you will have up to 2 minutes to respond with your answers.
     After 2 minutes has been reached there will be a '*' denoted on the log, but you will still be able to respond.
     Exceeding 2 minutes will result in a 2 point infraction.\n''')
    time.sleep(5)


#DO WE NEED THESE THREE FUNCTIONS AT ALL?

# clean the input submitted
def process_input(user_input):
    
    user_input = user_input.lower()
    
    # switch contractions to non-contraction (I'm to I am)
    user_input = decontracted(user_input)
    
    # remove punctuation
    user_input = re.sub(r'[^\w\s]', '', user_input)
    
    return user_input


# loads the questions from the CSV
def load_questions(file):
    data = pd.read_csv(file)     
    return data

def choose_question(dataframe):
    rand_numb = randomNumbGen(dataframe.index.max())   
    #Need to stop it from picking same numbers during the session.
    ques = dataframe.at[rand_numb, 'Question']
    cat = dataframe.at[rand_numb, 'Category']
    
    
    return ques, cat

#Iris response when user is idle for 2 minutes.
def idle_check():
    time.sleep(5)
    if answer != None:
        print('\n')
    elif answer == 'end session':
        print('\n')
    elif answer == 'END SESSION':   
        print('\n')
#Time exceeded character won't print to console but will be logged.
    x = '*'
    logging.debug(x) 
    

#----------------------------------------------
# start of code, end of functions
#----------------------------------------------

#initialize the response and running variables
response = ''
running = True
answer = None
question_counter = 0

# save the path to the current working directory
abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath) + '/questions.csv'

# load questions from the CSV file and save them to a data frame
questions_df = load_questions(dname)

# start the conversation
userName = start_conversation()

# Reformat the user's name for the chat.
formattedName = userName + ": "

# continue running while the program is running
while running: 

    question, category = choose_question(questions_df)
    question_counter = question_counter + 1
    
    print('{}The category is: {}'.format(bot_formatted_name, category))
    print('{}Question {}:{}'.format(bot_formatted_name, question_counter, question))
    #Start timining how long user takes to respond after question has been printed out.
    Thread(target = idle_check).start()
    
    #logs IRIS Category and question declaration.
    logging.debug('{}The category is: {}'.format(bot_formatted_name, category))
    logging.debug('{}Question {}:{}\n'.format(bot_formatted_name, question_counter, question))

    #records user's responses and processes it.
    response = process_input(input(formattedName))
    #logging user's response into log file without their name.
    log_response = logging.debug('{}'.format(response))

    # tokenize the words
    tokens = word_tokenize(response)

    # Response to whitespace only
    if re.match(r'^\s*$',response): 
        print('You seem to be quiet. What is on your mind?')

    # match if help is requested
    elif re.match(r'HELP', response, re.IGNORECASE):
        get_help()


    # exit the while loop if the user typed end session or END SESSION 
    elif response == 'end session' or response == 'END SESSION':
        running = False   # changes the running global variable to false to end the program
        print(bot_formatted_name + "Thanks for an amazing conversation!")
        
    else:
        print('\n' + bot_formatted_name + 'Thanks for answering! Here is your next question:')
