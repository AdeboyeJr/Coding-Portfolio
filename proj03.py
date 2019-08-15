#!/usr/bin/env python3
# -*- coding: utf-8 -*-

####################################################################
# Computer Project 3
#   
#  Encryption
# 
#   Prompt the user to encrypt, decrypt or quit program
#   loop while not quit
#   make a string of the alphabet and set index equal to zero
#   prompt the user to input a keyword 
#   use an empty key vaiable 
#   create a continuous loop to compare key to alphabet
#   if letter is in alphabet, remove letter from the variable
#   check for repeating variables
#   convert cypher key to affine key
#   allow user to decrypt
####################################################################

answer = input("Would you like to (D)ecrypt, (E)ncrypt or (Q)uit? ")
while answer.upper() != 'Q':
    
    # Fill in the good stuff here instead of the following print
    letters = 'abcdefghijklmnopqrstuvwxyz' #string of the alphabet
    keyword_str = input("Please enter a keyword: ")#keyword user inputs
    error_exists = False
    if keyword_str.isalpha() == False or len(keyword_str)>26:
        print('''There is an error in the keyword. It must be all letters and a 
              maximum length of 26''')
        error_exists = True
    if error_exists == False:    
     message_str = input("Enter your message: ") #message to be encoded 
     if answer.upper() == 'E': #checks to see if user wants to encrypt
      
       newkey_str = '' #Empty string to place characters in
       for letter in keyword_str.lower():
           if letter not in newkey_str and letter.isalpha():
               newkey_str += letter #adds character to empty string from keyword
       for letter in letters:
           if letter not in newkey_str:
               newkey_str += letter
            
       newkey_word_str = ''  
       for letter in message_str:
           if not letter.isalpha():
             newkey_word_str += letter
             
             
           else:
               newkey_word_str += newkey_str[ord(letter.lower())-ord('a')]
               
       a = 5
       b = 8
       Affkey_word_str = '' #empty string for affine key
       for letter in newkey_word_str: #creating affine key
           
           if not letter.isalpha():
               Affkey_word_str += letter
               
           else:    
              Affkey_word_str += newkey_str[((a*newkey_str.index(letter))+b)%26]
       print("your encoded message:  ",Affkey_word_str)
               
       
        
     elif answer.upper() == 'D': #checks to see if user wants to decrypt
         newkey_str = ''
         
         for letter in keyword_str:
             if letter.lower() not in newkey_str and letter.isalpha(): #checks 
                 #to see if 
                 newkey_str += letter.lower()
         for letter in letters:
             if letter not in newkey_str:
                 newkey_str += letter
                 
         Affkey_str =''
         a = 5
         b = 8
         for letter in newkey_str:
            Affkey_str += newkey_str[((a*newkey_str.index(letter))+b)%26]
            newkey_word_str = ''
         for letter in message_str:
             if not letter.isalpha():
                 newkey_word_str += letter
                 
             else: 
                 newkey_word_str += newkey_str[Affkey_str.index(letter)] 
         decrypt_msg = ''
         for letter in newkey_word_str:
             if not letter.isalpha():
                 decrypt_msg += letter
             else:
                 decrypt_msg += letters[newkey_str.index(letter)]
         print("your decoded message:  ", decrypt_msg)
             
       
    
    
     answer = input("Would you like to (D)ecrypt, (E)ncrypt or (Q)uit? ")
    
else:
    print("See you again soon!")    