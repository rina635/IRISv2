#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Final Assignment: Team 3 - Rafeef Baamer, Ashish Hingle, Rina Lidder, & Andy Nguyen

Description: IRIS (short for INSTRUCTIVE RESPONSE INTERVIEW SIMULATOR) is a chatbot solution that primarily serves as an interview simulator to help users
practice interview questions in a broad context. This project aims to implement the solution as an extension to the ELIZA model, described as the first chatbot
system (Weizenbaum 1976). It is primarily designed for students, but any professional can use the service to practice common interview questions and receive
feedback based on their responses. After the practice session, the chatbot will provide the user a rating score of how they did and describe some aspects that
can be improved.  

This file is used after the user has already input their responses through iris.py.

Usage Instructions:
1) Run the iris.py file
2) Enter user name on prompt
3) Enter the number of desired questions on prompt
4) Read through the question and enter the response
5) After all questions are answered, or program is terminated, use the associated feedback.py file to score the responses

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
- [7] Finds location of log file: https://stackoverflow.com/questions/37912556/converting-a-log-file-into-a-csv-file-using-python
- [8] Finds location of log file: https://stackoverflow.com/questions/28836781/reading-column-names-alone-in-a-csv-file
- [9] Finds location of log file: https://stackoverflow.com/questions/33832184/open-a-log-extension-file-in-python
- [10] Locating list elements: https://stackoverflow.com/questions/41125909/python-find-elements-in-one-list-that-are-not-in-the-other
- [11] Searching for a string: https://stackoverflow.com/questions/36519939/using-index-with-a-list-that-has-repeated-elements  
- [12] Searching for a string: https://stackoverflow.com/questions/3675144/regex-error-nothing-to-repeat  
- [13] Removing specific characters from a list: https://stackoverflow.com/questions/3416401/removing-elements-from-a-list-containing-specific-characters
- [14] Conditionally update dataframe: #https://stackoverflow.com/questions/37976823/how-to-conditionally-update-dataframe-column-in-pandas-based-on-list
- [15] NLTK tokenizer example: #https://stackoverflow.com/questions/15547409/how-to-get-rid-of-punctuation-using-nltk-tokenizer   

"""
# import and initialize libraries
import os, sys, re, csv, spacy
from nltk import pos_tag
import pandas as pd
from nltk import sent_tokenize, word_tokenize  
import numpy as np
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nlp = spacy.load('en_core_web_sm')

# declare global variables
possible_total_score = 4

'''----------------------------------------------
 Defined functions
----------------------------------------------'''

# If user exited session then need to execute so that can capture before user requested to end the session
def whole_interview(list):    
    end_sesh = re.compile('end session', re.IGNORECASE)
    for i in range(len(interview)):
        if re.search(end_sesh, interview[i]):
            end_index = i
            beg_index = 0
            list = interview[beg_index:end_index]
    return list        
    
# Searches interview list to find all the questions IRIS asked during interview
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

# Isolates the answer's from the user
# code referenced from source [10]
def a_search(interview):
    #seperate out all of IRIS's statements
    all_iris = [i for i in interview  if re.search(r'IRIS:', i) ]
    
    #Use list comprehension to isolate the user's answers   
    not_iris = [item for item in interview if item not in all_iris]
    
    #Gets rid of empty rows
    answers_list = list(filter(None,not_iris))
    
    #Removes * character IRIS denoted if they went overtime.
    answers = [ x for x in answers_list if '*' not in x ] 
    return answers

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

# search for a *, which is used to denote overtime questions
# code referenced from source [11] and [12]  
def overtime_q(list):
    asterisk = re.compile(r'(\*)')    
    overtime_qs = []
    for i in range(len(interview)):
        if re.search(asterisk, interview[i]):
            #Question is 2 rows away, using index to locate question in list
            q_index = i - 2
            overtime_q = interview[q_index] 
            overtime_qs.append(overtime_q)
    return overtime_qs

# compile a list of short sentences (both less than 3 sentences, and less than 45 words)
def length_check(aList):
    sent_check = []
    word_check = []
    
    # Create a list of all the answers where user responded in less than 3 sentences
    for i in range(0, len(aList)):
        #Tokenizes each answer and checks the length of sentence tokens.
        sent_tokens = sent_tokenize(aList[i])
        if len(sent_tokens) < 3:
            sent_check.append(aList[i])
            
    # Create a list of all the answers where the user responded using less than 45 words
    # code referenced from source [15] 
    for i in range(0, len(aList)):
        words= word_tokenize(aList[i])
        #Will not count punctuation in final word count
        words=[word.lower() for word in words if word.isalpha()]
        if len(words) < 45:
            word_check.append(aList[i])
    return sent_check, word_check

# Use sentiment analysis to compare the sentiment of the answer to question
def senti_analysis(dataframe):
    #declare variables needed
    sia = SentimentIntensityAnalyzer()
    questions = []
    answers = []
    
    #calculate sentiment analysis scores for all questions
    for row in dataframe['question']:
        questions.append(sia.polarity_scores(row))
        
    #calculate sentiment analysis scores for all answers
    for row in dataframe['answers']:
        answers.append(sia.polarity_scores(row))
    return answers, questions

'''----------------------------------------------
 start of code execution
----------------------------------------------'''

# Load sample answers for feedback
abspath = os.path.abspath(sys.argv[0])

# Open dataset as a dataframe.  
with open('questions_answers.csv', encoding='utf8', errors='ignore') as f:  
    reader = csv.reader(f)
    i = next(reader)
    rest = list(reader)
    all_questions_df = pd.DataFrame(rest, columns = ['index', 'question', 'category', 'sample'])

# Load log from IRIS.py as a list
# code referenced from source [7], [8], and [9]
with open('user_response.log') as file:
    interview = file.read().splitlines()

# save a copy of the interview before session ends
interview_2 = whole_interview(interview)

# save a list of all user's answers
answers = a_search(interview_2)

# save a list of all questions
questions = q_search(interview_2)

# Create a dataframe of Interview session with just the first 2 columns, questions and answers
# Df removes any questions where the user had an empty response
interview_df = pd.DataFrame(list(zip(questions, answers)), columns = ['question', 'answers'])

# Third column is the score, defaults to the possible total score
interview_df['score'] = possible_total_score

# fourth column is the feedback
interview_df['feedback'] = ''

# Cleaning up overtime question list by removing asterisk and blank lines of list
# code referenced from source [13]
all_overtime = overtime_q(interview_2)    
all_overtime = [ x for x in all_overtime if "*" not in x ]
all_overtime = list(filter(None,all_overtime))

# Remove IRIS: Question part from overtime list so only getting the question text.
clean_overtime_q =[]
iris_questions = [i for i in all_overtime if re.search(r'IRIS: Question', i)]
for i in range(0, len(iris_questions)):
    q = iris_questions[i]
    clean_q = q.split(': ')
    q_only = clean_q[2]
    clean_overtime_q.append(q_only)


'''
Criteria 1: Time
Description: Response given within 2 minutes
Details: if user went over time for a specific question, subtract 1 from score
'''

# if criteria 1 not met, subtract 1 point
# code referenced from source [14]
interview_df.loc[interview_df.question.isin(clean_overtime_q), 'score'] = interview_df['score'] - 1

#if user went over time then will add this feedback
interview_df.loc[interview_df.question.isin(clean_overtime_q), 'feedback'] = interview_df['feedback'] + '''
-You took too long to answer.
 You won't have too much time to think of your answer, so keep practicing with new questions.'''

#adds feedback for responses that did not lose points
interview_df.loc[~interview_df.question.isin(clean_overtime_q), 'feedback'] = interview_df['feedback'] + '''
-You answered within 2 minutes.'''


'''
Criteria 2: Response Length
Description: Response is atleast 3 sentences, and 45 words long
Details: if user did not meet the length requirements for a specific question, subtract 1 from score
'''

# declare lists to hold responses that do not match response length
short_sent = []
less_45_words = []

# use the function to fill the lists with responses that do not match crieria 2
short_sent, less_45_words = length_check(answers)

# Will store user's answers that didn't meet either of the length criteria.
short_answers = sorted(np.unique(short_sent + less_45_words))
     
# if criteria 2 not met, subtract 1 point
interview_df.loc[interview_df.answers.isin(short_answers), 'score'] = interview_df['score'] - 1

#adds feedback for responses that lost points
interview_df.loc[interview_df.answers.isin(short_answers), 'feedback'] = interview_df['feedback'] + '''
-Your answer is too short.
 You should express your answer with more detail. A good answer will be atleast 3 sentences and 45 words long.'''
 
#adds feedback for responses that did not lose points
interview_df.loc[~interview_df.answers.isin(short_answers), 'feedback'] = interview_df['feedback'] + '''
-Your answer was sufficient in length.'''


'''
Criteria 3: Named Entity Recognition (NER)
Description: Response has atleast 1 named entity
Details: if user did not meet the NER requirements for a specific question, subtract 1 from score
'''

# evaluate the answers and return as a list
no_ents = eval_ents(answers)

# if criteria 3 not met, subtract 1 point
interview_df.loc[interview_df.answers.isin(no_ents), 'score'] = interview_df['score'] - 1

#adds feedback for responses that lost points
interview_df.loc[interview_df.answers.isin(no_ents), 'feedback'] = interview_df['feedback'] + '''
-You did not include identifying information, such as company, organization, or supervisor names.
 Including these details can give the interviewer a better understanding of your experience.'''
 
#adds feedback for responses that did not lose points
interview_df.loc[~interview_df.answers.isin(no_ents), 'feedback'] = interview_df['feedback'] + '''
-You included identifying information for the organizations you worked for.'''


'''
Criteria 4: Sentiment Analysis through NLTK
Description: Response's sentiment matches or is better than the question's sentiment
Details: if user did not meet the sentiment analysis requirements for a specific question, subtract 1 from score.
the compound score from the sentiment analysis describes a normalized score of postitive and negative responses on
a scale of 1 - 0, If the question is lower than the answer, it is more positive. Generally only answer scores lower
than a question score is bad, as it means the tone does not match
'''

# declare lists for the sentiment analysis of both questions and answers
answ_holder = []
ques_holder = []

# run the sentinment analysis function and the results to feedback
answ_holder, ques_holder = senti_analysis(interview_df)

# loop through the scored answers and questions and add the feedback
for i in range(0, len(ques_holder)):
        
    # if the compound score of the question is > the answer, subtract 1 point
    if ques_holder[i]['compound'] <= answ_holder[i]['compound']:
        interview_df.at[i, 'feedback'] = interview_df.at[i, 'feedback'] + '''
-The sentiment of your response matches the question asked.'''
    else:
        interview_df.at[i, 'score'] = interview_df.at[i, 'score'] - 1
        interview_df.at[i, 'feedback'] = interview_df.at[i, 'feedback'] + '''
-The sentiment of your response does not match the answer.
 Try to be more positive in your response, as this will leave a better impression.'''

# create a dataframe of questions where user got less than 2/4
low_score_df = interview_df.loc[(interview_df.score <= 2)]

# Add sample answers for low scored questions
low_sample_df = pd.merge(low_score_df, all_questions_df[['question','sample']], left_on='question', 
                        right_on='question', how ='inner')
# merge low scores with original dataframe, anything that do
final_df = pd.merge(interview_df, low_sample_df, on= ['question', 'answers'], how = 'outer')   
 
# merge question and add sample answer into the main dataframe
interview_df = pd.merge(interview_df, all_questions_df[['question','sample']], left_on='question', right_on='question', how ='inner')

# Remove answers where user requested help
#interview_df = interview_df[(interview_df.answers != 'HELP') & (interview_df.answers != 'help')& (interview_df.answers != 'Help')] 
interview_df = interview_df[~interview_df.answers.str.contains("HELP", na=False, case=False)]

# Compile the feedback to be printed and saved to log
# declare a feedback holder that will cummulate all feedback
compl_feedback = 'IRIS FEEDBACK'

# get current date and time for the log file
now = datetime.now()
current_time = now.strftime('%H:%M')
current_date = now.strftime('%B %d, %Y')

# add the date and time to the feedback holder
compl_feedback += '\nGenerated on: ' + current_date + ' at ' + current_time + '\n\n-----------------------------------------------\n'

# declare a count of questions to be used in log
question_counter = 0

# loop through the dataframe and add to the feedback holder
for ind in interview_df.index: 
    question_counter = question_counter +1
    
    compl_feedback += '\nQuestion ' + str(question_counter) + ': ' + interview_df['question'][ind]
    compl_feedback += '\nAnswer ' + str(ind + 1) + ': ' + interview_df['answers'][ind]
    compl_feedback += '\n\nScore: ' + str(interview_df['score'][ind]) + '/' + str(possible_total_score)
    compl_feedback += '\nDetailed Feedback: ' + interview_df['feedback'][ind]
    compl_feedback += '\nSample answer: "'
    compl_feedback += interview_df['sample'][ind] + '"'
    compl_feedback += '\n\n-----------------------------------------------\n'
# print the feedback to console
print(compl_feedback)

# save the feedback to a text file.
f = open('feedback.txt', 'w', encoding='utf-8')
f.write(compl_feedback)
f.close()
print('The graded feedback file has been created for your reference.')