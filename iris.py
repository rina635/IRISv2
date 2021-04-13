
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
import random, re, nltk, os, sys, logging
import pandas as pd 
from nltk.tokenize import word_tokenize
from datetime import datetime

#Creates a log file of all user responses will rewrite the log file every time code executed.
#https://stackoverflow.com/questions/38409450/logging-to-python-file-doesnt-overwrite-file-when-using-the-mode-w-argument-t
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
    print(bot_formatted_name + 'Nice to meet you, {}! To end the session, type "END SESSION". For help, type "HELP". For tips, type "TIPS".'.format(name))  
    
    new_user = input(bot_formatted_name + 'Is this your first time interacting with me?\nType "Yes" or "No"\n')   # ask if first time     
    
    
    while not (new_user.lower() == 'yes' or new_user.lower() == 'no'):
        new_user = input(bot_formatted_name + 'Invalid response. I need to know if this is your first time using IRIS?\n')   # ask for their name and saves inputted value to userName variable
  
    if new_user.lower() == 'yes':
        get_help()
    elif new_user.lower() == 'no':
        print(bot_formatted_name + 'Great! If you need assistance please type in "HELP".')

    print('Let\'s get started!\n')
    print('----------------------\n')
    return name

# calls the instructions for using the program 
def get_help():
    print('\n' + bot_formatted_name + 'Welcome my job here is to help you practice for your interview.')
    print(bot_formatted_name + 'I will ask several questions from various categories. You will have 90 seconds to respond with your answer.')

# calls the tips for using the program
def get_tips():
    print('\n' + bot_formatted_name + 'Here are some tips for doing your best. (need to add***')



# clean the input submitted
def process_input(user_input):
    
    user_input = user_input.lower()
    
    # switch contractions to non-contraction (I'm to I am)
    user_input = decontracted(user_input)
    
    # remove punctuation
    user_input = re.sub(r'[^\w\s]', '', user_input)
    
    return user_input

# function that is used to remove contractions
def decontracted(phrase):
    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    phrase = re.sub(r"he\'s", " is", phrase)
    phrase = re.sub(r"she\'s", " is", phrase)
    
    return phrase

# function to display generic questions
def not_understood_responses():       
    choices = [
        'I\'m not sure I understand. Can you explain that in a different way?',
        'I\'m a little confused... please try saying that again ...',
        'I am lost. Please try a explaining that again.']
   
    iris_response(len(choices)-1, choices)    

# loads the questions from the CSV
def load_questions(file):
    
    # Read data from file 'filename.csv' 
    # (in the same directory that your python process is based)
    # Control delimiters, rows, column names with read_csv (see later) 
    data = pd.read_csv(file)     
    return data

def choose_question(dataframe):
    rand_numb = randomNumbGen(dataframe.index.max())   
    
    ques = dataframe.at[rand_numb, 'question_text']
    cat = dataframe.at[rand_numb, 'category']
    
    
    return ques, cat


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
#print(questions_df)

# start the conversation
userName = start_conversation()

# Reformat the user's name for the chat.
formattedName = userName + ": "

# continue running while the program is running
while running: 

    question, category = choose_question(questions_df)
    question_counter = question_counter + 1
    #I actually don't want to print the category but let's keep it for now to check
    print('{}The category is: {}'.format(bot_formatted_name, category))
    print('{}Question {}:{}'.format(bot_formatted_name, question_counter, question))
    
    # request input from the user, append the formatted user name to the front of the console print, and process the input
    response = process_input(input(formattedName))  # save response from input
    log_response = logging.debug(response)

    # tokenize the words
    tokens = word_tokenize(response)

    # Response to whitespace only
    if re.match(r'^\s*$',response): 
        print('You seem to be quiet. What is on your mind?')

    # match if help is requested
    elif re.match(r'HELP', response, re.IGNORECASE):
        get_help()

    # match if tips is requested
    elif re.match(r'TIPS', response, re.IGNORECASE):
        get_tips()

    # exit the while loop if the user typed end session or END SESSION 
    elif response == 'end session' or response == 'END SESSION':
        running = False   # changes the running global variable to false to end the program
        print(bot_formatted_name + "Thanks for an amazing conversation!")
        
    else:
        print('\n' + bot_formatted_name + 'Thanks for answering! Here is your next question:')


# currently completed logic
# 1. asks for user name (if empty reprompts)
# 2. asks if it is first time (if yes then prints instructions, if no then continue. Anything else, reprompts)
# 3. loads questions into a dataframe (uses working directory for path)
# 4. says lets get started and presents question
# 5. checks if empty string submitted, HELP, TIPS or END selected. If none, then thanks user for entering response, and asks next question