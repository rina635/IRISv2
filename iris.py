
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Final Assignment: Team 3 - Rafeef Baamer, Ashish Hingle, Rina Lidder, & Andy Nguyen

Description: IRIS is a chatbot originally designed to act as a therapist, with COVID-19 looming many 
have found themselves in dire need of professional help. Team 3 has built an IRIS chatbot to assist 
those people in getting the help they need. Our IRIS works to encourage the flow of communication 
to get user’s comfortable in discussing their feelings. IRIS has been built with pre-defined 
functions to recognize human emotion in commonly used phrases. For example, IRIS’s functions’ 
use certain cues to label the user’s responses as positive or negative. These functions 
are designed in a way where new responses and triggers can be added easily. To make the 
conversation feel natural, IRIS will loop through the program to prompt the user to keep 
the conversation going and will end the conversation when the user is comfortable leaving it. 
The algorithm used in this program is similar to a tree, where each of the responses leads
 to a specific branch. Many of IRIS's responses are randomized to provide some variability 
 to input, just like a human would do. If none of the logic is triggered, then IRIS has a 
 default set of questions that can be used to continue the conversation.

Some common inputs include "I am happy", "I'll remember the name of the dog", "Can I count to 15?", "Hello IRIS!", 
"Computers scare me", "Draw me a fish"

In addition to basic functionality, the program has a help feature that provides instructions to the user, a 20 second timer 
to encourage the user to interact with IRIS, and the ability to draw ASCII animals. 

Resources used for this lab come from the materials provided in the AIT 590 course materials.
- Lecture powerpoints (AIT 590)
- Stanford University Prof. Dan Jurafsky's Video Lectures (https://www.youtube.com/watch?v=zQ6gzQ5YZ8o)
- Joe James Python: NLTK video series (https://www.youtube.com/watch?v=RYgqWufzbA8)
- w3schools Python Reference (https://www.w3schools.com/python/)
- regular expressions 101 (https://regex101.com/)
- Timer examples understood from: https://stackoverflow.com/questions/15528939/python-3-timed-input
"""
#import and initialize libraries
import random, re, nltk, time, logging
from nltk.tokenize import word_tokenize
from datetime import datetime
from threading import Thread

# global variables
bot_name = "IRIS"
suffix = ": "

# this function randomly generates a number between 1 and 4
# dependency includes random library
def randomNumbGen(max_numb):
    r = random.randint(0, max_numb)
    return r

#This function will allow IRIS to retrieve the current time
def time_now():
    now = datetime.now()
    time_holder = now.strftime('%H:%M')
    #print('IRIS: The time is:', time)
            
    if time_holder > "12:00" and time_holder < "16:00":
        greeting = "afternoon."
    elif time_holder > "16:01" and time_holder < "23:59":
        greeting = "evening."
    else:
        greeting = "morning."
    
    return greeting

# this function prints a hello message. A name must be passed in, a number can be chosen to randomly pick a message to display
def hello(name, numb):

    greeting = time_now()
    
    if numb == 1:
        print(bot_name + suffix + 'Good', greeting, 'It is good to meet you, {}. How can I help you?'.format(name))
    elif numb == 2:
        print(bot_name + suffix + 'Good', greeting, '{}, great to make your acquaintance... how can I help you?'.format(name))
    elif numb == 3:
        print(bot_name + suffix + 'Good', greeting, '{}! It\'s a lovely day... how can I help you?'.format(name))

# prints IRIS's response based on the number of choices and a list of possible choices
def iris_response(numb_choices, choices):
    
    rand_numb = randomNumbGen(numb_choices)
    print(choices[rand_numb])

# function to continue the conversation if there is a delay
def any_other():
    print(bot_name + suffix + "Anything else I can help with?")  

# function to display generic questions
def not_understood_responses():       
    choices = [
        'I\'m not sure I understand. Can you explain that in a different way?',
        'I\'m a little confused... please try saying that again ...',
        'I am lost. Please try a explaining that again.']
   
    iris_response(len(choices)-1, choices)       

# function that is used to respond to negative words based on a list
def negative_responses(): 
    choices = [
        'That is unforunate. Can you tell me why?',
        'Feelings are hard to navigate. Tell me more...',
        'Can you elaborate why?']
   
    iris_response(len(choices)-1, choices)       

# function that is used to respond to positive words based on a list
def positive_responses():
    choices = [
        'Can you tell me why?',
        'Tell me more...',
        'Can you elaborate why?']
   
    iris_response(len(choices)-1, choices)

# function that is used to respond to "questions"
def question_responses(numb):
    choices = [
        'Good question! What do you think?',
        'Can you elaborate why you are curious?',
        'Can you provide some more detail?']
   
    iris_response(len(choices)-1, choices)
        
# function that is used to respond to "thanks"
def thanks_responses(numb):
    choices = [
        'You are welcome!',
        'This is my job!',
        'I am here to help you.']
   
    iris_response(len(choices)-1, choices)
        
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

# function that is used to change the ownership words to pose a question bacl
def question_reply(phrase):
    #phrase = re.sub(r"([Aa]m I)", "are you", phrase)
    phrase = re.sub(r"([Aa]re you)", "am I", phrase)
    phrase = re.sub(r"([Cc]an I)", "would you", phrase)
    phrase = re.sub(r"([Ss]hould I)", "should you", phrase)
    phrase = re.sub(r"([Cc]ould I)", "would you", phrase)
    phrase = re.sub(r"(([Dd]o )?[Ii] feel)", "do you feel", phrase)
    phrase = re.sub(r"(([Dd]o )?[Ii] know)", "do you understand", phrase)
    phrase = re.sub(r"(([Dd]o )?[Ii] try)", "have you tried", phrase)
    phrase = re.sub(r"(([Dd]o )?[Ii] remember)", "do you have memories about", phrase)
    phrase = re.sub(r"(([Dd]o )?[Ii] want)", "would you like", phrase)
    phrase = re.sub(r"(([Dd]o )?[Ii] would)", "would you", phrase)
    phrase = re.sub(r"(([Dd]o )?[Ii] need)", "do you require", phrase)
    phrase = re.sub(r"(([Dd]o )?[Ii] think)", "do you suppose", phrase)
    phrase = re.sub(r"(([Dd]o )?[Yy]ou feel)", "would I feel", phrase)
    phrase = re.sub(r"(([Dd]o )?[Yy]ou know)", "would I know", phrase)
    phrase = re.sub(r"(([Dd]o )?[Yy]ou try)", "would I try", phrase)
    phrase = re.sub(r"(([Dd]o )?[Yy]ou remember)", "would I remember", phrase)
    phrase = re.sub(r"(([Dd]o )?[Yy]ou want)", "would I want", phrase)
    phrase = re.sub(r"(([Dd]o )?[Yy]ou would)", "would I", phrase)
    phrase = re.sub(r"(([Dd]o )?[Yy]ou need)", "would I need", phrase)
    phrase = re.sub(r"(([Dd]o )?[Yy]ou think)", "would I think", phrase)
    phrase = re.sub(r"( me )", "you", phrase)

    return phrase

# function that is used to flip words around to pose a question bacl
def conversation_reply(phrase):
    phrase = re.sub(r"my", "your", phrase)
    phrase = re.sub(r"[Ii] am", "are you", phrase)
    phrase = re.sub(r"[Yy]ou are", "am I", phrase)
    phrase = re.sub(r"([Ii] feel)", "are you feeling", phrase)
    phrase = re.sub(r"([Ii] know)", "do you understand", phrase)
    phrase = re.sub(r"([Ii] try)", "have you tried", phrase)
    phrase = re.sub(r"([Ii] remember)", "do you have memories about", phrase)
    phrase = re.sub(r"([Ii] want)", "would you like", phrase)
    phrase = re.sub(r"([Ii] would)", "would you", phrase)
    phrase = re.sub(r"([Ii] need)", "do you require", phrase)
    phrase = re.sub(r"([Ii] think)", "do you suppose", phrase)
    phrase = re.sub(r"([Yy]ou know)", "would I know", phrase)
    phrase = re.sub(r"([Yy]ou try)", "would I try", phrase)
    phrase = re.sub(r"([Yy]ou remember)", "would I remember", phrase)
    phrase = re.sub(r"([Yy]ou want)", "would I want", phrase)
    phrase = re.sub(r"([Yy]ou would)", "would I", phrase)
    phrase = re.sub(r"([Yy]ou need)", "would I need", phrase)
    phrase = re.sub(r"([Yy]ou think)", "would I think", phrase)
    phrase = re.sub(r"( me )", "you", phrase)

    return phrase

# function to start IRIS
def start_conversation():
    # start of program and logic
    # first interaction with user
    print(bot_name + suffix + 'Hello! I am ' + bot_name + '... I am a great listener.\n' + bot_name + suffix +'Let\'s talk about what\'s on your mind.') # greeting
    print(bot_name + suffix + 'If you need guidance, please type "IRIS HELP')
    
    # save the users name as an input
    name = input(bot_name + suffix + 'What is your name?\n')   # ask for their name and saves inputted value to userName variable
    
    # check if name is empty before contnuing
    while name == '':
        name = input(bot_name + suffix + 'I need to know how to address you. What is your name?\n')   # ask for their name and saves inputted value to userName variable
    
    # calls the hello function that prints a message based on the name and number passed 
    hello(name, randomNumbGen(3))   
    print('IRIS: If you would like to end our conversation, please type "END SESSION"\n----------------------')  
    
    return name

#function will check if the user has been idle for 20 seconds and say "Anything else I can help you with?"
def idle_check():
    time.sleep(20)
    if answer != None:
        return
    any_other()

# clean the input submitted
def process_input(user_input):
    
    user_input = user_input.lower()
    
    # switch contractions to non-contraction (I'm to I am)
    user_input = decontracted(user_input)
    
    # remove punctuation
    user_input = re.sub(r'[^\w\s]', '', user_input)
    
    return user_input


def process_rules():
    rules = [
        r'I need (.*)',
        r'([Ii]|[Yy]ou) ([Aa]m|[Aa]re|[Ff]eel|[Kk]now|[Tt]ry|[Rr]emember|[Ww]ant|[Ww]ould|[Nn]eed|[Tt]hink)(.*)?'
        
        
        ]





#----------------------------------------------
# start of code, end of functions
#----------------------------------------------

#initialize the response and running variables
response = ''
running = True
answer = None

# start the conversation
userName = start_conversation()

# format a userName logger
formattedName = userName + ": "

# continue running while the program is running
while running: 
    # checks to see if user has been idle for 20 seconds
    #Thread(target = idle_check).start()

    # request input from the user, append the formatted user name to the front of the console print, and process the input
    response = process_input(input(formattedName))   # save response from input

    # tokenize the words
    tokens = word_tokenize(response)

    # this is the start of logic
    # Response to whitespace only
    if re.match(r'^\s*$',response): 
        print('You seem to be quiet. What is on your mind?')

    # Catch blank response
    elif response == '': #Response to blanks.
        any_other()    
    
    # Check to see if user requests instructions 
    elif re.match(r'IRIS HELP', response, re.IGNORECASE):
        print(bot_name + suffix + "Gladly! I can respond to simple questions and statements. I am still learning, so complex statements can confuse me.")
        print(bot_name + suffix + "Try something like \"I am happy\" or \"Are you real?\" and I will do my best to respond. Remember, I am here to help you.")
        print(bot_name + suffix + "I can also draw a cat, dog or fish for you, if you ask me to \"Draw a fish!\".")
        print(bot_name + suffix + "Let\'s get started! What can I help you with?")
        
    # Exit the while loop if the user typed end session or END SESSION 
    elif response == 'end session' or response == 'END SESSION':
        running = False   # changes the running global variable to false to end the program
        print("IRIS: Thanks for an amazing conversation!")
        
    # Responses to i need statements
    elif re.match(r'I need (.*)', response):
        need_response = re.sub(r'I', 'Do you', response + '?')
        print(bot_name + suffix + need_response)    
       
    # matches a sentence with the structure of 'I or You [verb]'
    elif re.match(r'([Ii]|[Yy]ou) ([Aa]m|[Aa]re|[Ff]eel|[Kk]now|[Tt]ry|[Rr]emember|[Ww]ant|[Ww]ould|[Nn]eed|[Tt]hink)(.*)?', response):
        holder = 'Why ' + conversation_reply(response) + '?'
        print("IRIS:", holder)   #print IRIS's response

    # matches a sentence with the structure of '[verb] I or You' question
    elif re.match(r'([Aa]re|[Aa]m|[Ff]eel|[Kk]now|[Tt]ry|[Rr]emember|[Ww]ant|[Ww]ould|[Nn]eed|[Tt]hink) ([Ii]|[Yy]ou)(.*)?', response):
        holder = 'Why ' + question_reply(response) + '?'
        print("IRIS:", holder)   #print IRIS's response
        
    # matches a sentence with the structure of 'Do I [verb]'
    elif re.match(r'Do ([Ii]|[Yy]ou) (feel|know|try|remember|want|need|think)(.*)?', response):
        holder = 'Why ' + question_reply(response) + '?'
        print("IRIS:", holder)   #print IRIS's response
        
    # matches a sentence with the structure of 'Can or Should or Could I ...'
    elif re.match(r'([Cc]an|[Ss]hould|[Cc]ould) I(.*)?', response):
        holder = 'Why ' + question_reply(response) + '?'
        print("IRIS:", holder)   #print IRIS's response 

    # Match any sentence with computer word
    elif re.match(r'(.*)?computer(.*)?', response):
        print(bot_name + suffix + 'Sorry, I am afraid of computers.')
        any_other()

    # Match any sentence with problem word
    elif re.match(r'(.*)? problem(.*)?', response):
        print(bot_name + suffix + 'What is your problem, Can you explain it more?')

    # Match any sentence with died word
    elif re.match(r'(.*)? die(.*)?', response):
        print(bot_name + suffix + 'I am sad to hear that! How can I help you?')

    # if user starts response with the word sorry, IRIS comforts them
    elif tokens[0] == 'sorry':
        print(bot_name + suffix + 'Do not apologize ' + userName)

    # If the user say help
    elif re.match(r'(.*)?[Hh]elp(.*)?', response):
        print(bot_name + suffix + 'How can I help you? ' + userName)    
           
    # Display an ASCII character based on dog, cat and fish
    elif re.match(r'(.*)?(dog|cat|fish)(.*)?', response, re.IGNORECASE):
            if re.match(r'(.*)?(dog)(.*)?', response, re.IGNORECASE):
                print(bot_name + suffix + 'Here is my favorite dog:\n  __      _\no\'\')}____//\n `_/      )\n (_(_/-(_/')
            elif re.match(r'(.*)?(cat)(.*)?', response, re.IGNORECASE):
                print(bot_name + suffix + 'Here is my favorite cat:\n|\---/|\n| o_o |\n \_^_/')
            elif re.match(r'(.*)?(fish)(.*)?', response, re.IGNORECASE):
                print(bot_name + suffix + 'Here is my favorite fish:\n      /`·.¸\n     /¸...¸`:·\n ¸.·´  ¸   `·.¸.·´)\n: © ):´;      ¸  {\n `·.¸ `·  ¸.·´\`·¸)\n     `\\´´\¸.·´')
        
    # catches all questions start with any question words  
    elif re.match(r'(.*)?([Ww]hat|[Ww]here|[Ww]hen|[Hh]ow|[Ww]hy|[Ww]hich|[Ww]hose|[Ww]hom)(.*)?', response, re.IGNORECASE):
        question_responses()
        
    # Responses to any negative words
    elif re.match(r'(.*)?(sad|unhappy|fear|anger|disgust|sadness|rage|stress|hate|dislike|bad|depressed|depression)(.*)?', response, re.IGNORECASE):
        negative_responses()

    # Responses to any positive words
    elif re.match(r'(.*)?(joy|gratitude|serenity|hope|awe|amuse|cheer|enjoy|happy|love|like|good)(.*)?', response, re.IGNORECASE):
        positive_responses()

    # Responses to greetings
    elif re.match(r'(.*)?(hello|hi|greetings)(.*)?', response, re.IGNORECASE):
        print(bot_name + suffix + 'Hello ' + userName + "! How can I help you?")
        
    # Match Thank statement  
    elif re.match(r'thank(.*)', response, re.IGNORECASE):
            thanks_responses(randomNumbGen(2)) 
  
    else:
        not_understood_responses()
