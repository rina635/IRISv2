
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Final Assignment: Team 3 - Rafeef Baamer, Ashish Hingle, Rina Lidder, & Andy Nguyen



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


# clean the input submitted
def process_input(user_input):
    
    return user_input


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

#IRIS will log when the user has exceeded 2 minutes without a response with asterisk.
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
    

#----------------------------------------------
# start of code, end of functions
#----------------------------------------------

#initialize the response and running variables
response = ''
answer = None
question_counter = 0
    
# save the path to the current working directory
abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath) + '/questions.csv'

# load questions from the CSV file and save them to a data frame
questions_df = load_questions(dname)

# start the conversation
userName = start_conversation()
n = int(input('{}How many questions would you like for today? \nPlease select a number between 5 and 10.\n'.format(bot_formatted_name)))
# Reformat the user's name for the chat.
formattedName = userName + ": "

# Interview session will continue until the number of questions has been reached.
while question_counter < n: 
    
    
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
    #response = process_input(input(formattedName))
    response = input(formattedName)
    #logging user's response into log file without their name.
    log_response = logging.debug('{}'.format(response))


    # Response to whitespace only
    if re.match(r'^\s*$',response): 
        print('Okay, I will move on to the next question.')

    # match if help is requested
    elif re.match(r'HELP', response, re.IGNORECASE):
        get_help()


    # exit the while loop if the user typed end session or END SESSION 
    elif response == 'end session' or response == 'END SESSION':
        running = False   # changes the running global variable to false to end the program
        print(bot_formatted_name + "Thanks for an amazing conversation!")

print(bot_formatted_name + "It was really great learning more about you, the maximum number of questions has been reached.")