## IRIS (INSTRUCTIVE RESPONSE INTERVIEW SIMULATOR)
#### Final Assignment: AIT 590 Spring 2021
Team 3 - Rafeef Baamer, Ashish Hingle, Rina Lidder, & Andy Nguyen

### Description

**IRIS** (short for INSTRUCTIVE RESPONSE INTERVIEW SIMULATOR) is a chatbot solution that primarily serves as an interview simulator to help users practice interview questions in a broad context. This project aims to implement the solution as an extension to the ELIZA model, described as the first chatbot system (Weizenbaum 1976). It is primarily designed for students, but any professional can use the service to practice common interview questions and receive feedback based on their responses. After the practice session, the chatbot will provide the user a rating score of how they did and describe some aspects that can be improved.

The baseline solution for **IRIS** serves to match currently available commercial solutions, it allows users to engage in real-time with a system that mimics the question-and-answer aspect of an interview.  Using the model prescribed in the proposal, we set out to build an initial program that 1.) Presents questions to the user, and 2.) Provides a feedback response.

**IRIS** can provide various behavioral-based interview questions in 7 different categories: Leadership, Teamwork, Interactions, Morality & Ethics, Stress & Adaptability, and Miscellaneous. Users cannot predict the exact questions they will be asked but using a dataset of 93 questions for IRIS to pick from keeps the user engaged and challenged in a learning environment.

**IRIS** keeps a log of the user's interview responses, allowing the user to review the log as soon as the session is complete. This environment is similar to video interview simulations, where a user's responses are recorded and then played back to them at the end. Allowing a user to have a tangible record of their interview session helps them see what type of questions they seem to be struggling with.

### Input and user interface example

> IRIS: Good afternoon, I am IRIS the Instructive Response Interview Simulator. Here to help you prepare for your next interview!
>
>Before we begin, what is your name?
>User Name
>IRIS: Nice to meet you, User Name! To end the session, type "END SESSION". For help, type "HELP".>
>
>IRIS: Is this your first time interacting with me?
>Type "Yes" or "No"
>Yes
>
>IRIS: Welcome! My job here is to help you practice your interview skills. Here are the instructions to interact with me:
>1) Choose the number of questions (5 - 10 questions).
>2) Answer each question within 2 minutes.
>3) After you have completed your session, use the feedback.py file to score your responses.
>Some information to help you succeed with your preperation:
>- The goal of interacting with me is to ensure you're able to answer the questions in the best way you can.
>- You should discuss specific experiences and details, including names of companies, organizations and supervisors.
>- Express your past experiences in detail and use descriptive language. Aim for at least 3 full sentences.
>- I will allow you to submit a response even if you exceed the 2-minute time limit. However, this will affect your score.
>- Any blank responses will not be graded.
>
>Let's get started!
>
>----------------------
>How many questions would you like for today? 
>Please select a number between 5 and 10.
>
>5
>
>IRIS: The category is: Interactions
>IRIS: Question 1:  Tell me about the best review you’ve ever gotten from a customer.
>
>User Name: While I worked on a team at George's Ice-cream Parlor, one of our clients gave me a review that said, "I went above an >beyond what was required to get the project right." That was the best review I have ever got. I think it also describes my attitude >towards customer service in all the jobs I have held before.
>
>IRIS: The category is: Teamwork
>IRIS: Question 2:  What would you do if your team was waiting on another department dragging their heels?
>
>User Name: END SESSION
>
>Would you like to run feedback now? Please respond with "Yes" or "No"(You can manually run feedback later if you say no now.) 
>Yes
>IRIS FEEDBACK
>Generated on: May 01, 2020 at 12:00
>
>
>-----------------------------------------------
>
>Question 1:  Tell me about the best review you’ve ever gotten from a customer.
>Answer 1: While I worked on a team at Amazon, one of our clients gave me a review that said, "I went above an beyond what was >required to get the project right." That was the best review I have ever got. I think it also describes my attitude towards >customer service in all the jobs I have held before.
>
>Score: 4/4
>Detailed Feedback: 
>-You answered within 2 minutes.
>-Your answer was sufficient in length.
>-You included identifying information for the organizations you worked for.
>-The sentiment of your response matches the question asked.
>Sample answer: "While I worked on a team at Amazon, one of our clients gave me a review that said, "I went above an beyond what was >required to get the project right." That was the best review I have ever got. I think it also describes my attitude towards >customer service in all the jobs I have held before."
>
>-----------------------------------------------
>
>The graded feedback file has been created for your reference.
>IRIS: It was really great learning more about you, User Name this is the end of our session.
>----------------------------

### Library Dependancies

1. NLTK
2. NLTK VADER Corpus
3. Pandas
4. spaCy
5. numpy