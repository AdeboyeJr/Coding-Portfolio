####################################################
#
#                    Project 9
#
#-Take a csv file and compare song artists and the
#amount of words used in their songs
#-Check to see if words in their lyrics is a stop
#word. If it is, remove it
#-Display singers and calculate average word count
#-Create a search function that allows users to 
#find artist and song title by typing a string of 
#text
#-Display graph detailing lexicon of each artist
#in their songs
#
####################################################

import csv #makes reading csv file easier
import string
import pylab
from operator import itemgetter #sorting 

def open_file(message):
    '''Opens file for reading''' 
    
    while True:
        try:
            filename = input(message, ) #message is whatever is displayed in 
            #main
            
            fp = open(filename, 'r', encoding ="windows-1252")
            return fp
        except FileNotFoundError:
            print("File is not found! Try Again!") 

def read_stopwords(fp):
    '''Reads lines in text file and adds each word to a set''' 
    stopwords = set() #create empty set to be filled
    
    lines = fp.readlines() #reads lines in text file
    
    for word in lines:
        word = word.strip('\n') #removes carriage returns from text
        
        if word not in stopwords:
            
            stopwords.add(word) #adds word into set if not already in set,
            #ignoring duplicates
           
    return stopwords

def validate_word(word, stopwords):
    ''' Checks if word can be found in stopword set''' 
    
    if word.lower() in stopwords: #if word can be found in stopword set,
        # it is not valid
        
        return False
    elif word not in stopwords:
        if word.isalpha() == False: # if word contains digits or punctuation,
            #it is not valid
            
            return False
        elif word.isalpha() == True: #if word is not a stop word or if it 
            #contains no digits or punctuation, it is valid
            
            return True

def process_lyrics(lyrics, stopwords):
    ''' Takes words in lyrics. Checks to see if word is a stopword.
    If not, a new set with lyric words will be created'''
    
    lyrical_set = set() # create empty set
    
    words = lyrics.lower().split() #change to lower case and make into a list
    
    for word in words:
        word = word.strip().strip(string.punctuation)
        word_check = validate_word(word,stopwords)
        #call validate word function to check for stop words
        
        if word_check == True:
            lyrical_set.add(word)
            
        
    return lyrical_set
    
def read_data(fp, stopwords):
    '''Read through each line in csv file. Extract singer name, song title
    and lyrics. Use process lyrics function and update_dictionary function
    to create a new dictionary with a set of lyrics embedded within it''' 
    
    reader = csv.reader(fp) #csv reader compensates for csv files that have
    #multiple rows in each cell
    
    next(reader) #skips header
    
    singer_dictt = {} #create empty dictionary
    
    for row in reader:
        
        column_0 =  str(row[0]) #artist name
        
        column_1 = str(row[1]) #song title
        
        column_2 = str(row[2]).lower() #song lyrics
        
        
        lyrics_set = process_lyrics(column_2,stopwords)
            
            
        update_dictionary(singer_dictt,column_0,column_1,lyrics_set)
        #updates empty dictionary by calling another function
    
    return singer_dictt

def update_dictionary(data_dict, singer, song, words):
    '''Create and update a dictionary with a singer, song title and set of
    words per song''' 
    
    word_set = set() 
           
    if singer not in data_dict:  #checks to see if key is in dictionary   
        data_dict[singer] = {}
        #if not, create new key and set value as another dictionary
        
    if song not in data_dict[singer]: #checks to see if key is in newly created
        #dictionary
        
        data_dict[singer][song] = word_set #if not, create new key and set value
        #as a set
        
    for word in words:
        if word not in word_set:
            data_dict[singer][song].add(word)
            #add words to the empty set
                
            
def calculate_average_word_count(data_dict):
    ''' Calculate average word use for each artist'''
    
    avg_dict = {} #create new dictionary

    for artist in data_dict:
        
        word_count = 0 
        song_count = 0
        #counters for words and songs
    
        if artist not in avg_dict:
            avg_dict[artist] = {}
            #creates new key with a dictionary as its value if it didn't already
            #exist
            
                      
        
        for song in data_dict[artist]:
                
            song_count += 1
                  
            for data_set in data_dict[artist][song]:
                      
                word_count += 1
            
        avg_dict[artist] = float(word_count/song_count)
        #average is the total count of unique words used by artist divided by
        #the total number of songs they dropped
            
    return avg_dict
        
    

def find_singers_vocab(data_dict):
    ''' Displays set of distict words for each singer''' 
    unique_dict = {} #takes empty dicitonary
    
    
    for artist in data_dict.keys():
        
        word_set = set() #creates an empty set for each artist
        
        if artist not in unique_dict:
            unique_dict[artist]= {}
            #creates a new key and dictionary value for unique dictionary
            
        for song in data_dict[artist]:
           
            song_words = data_dict[artist][song]
            
            word_set= word_set | (song_words)
            #checks to see if set of words can be found in song lyrics,
            #returns overlapping words
            
             
        unique_dict[artist] = word_set
        

    return unique_dict

def display_singers(combined_list):
    ''' Format data for each singer''' 
    print("\n{:^80s}".format("Singers by Average Word Count (TOP - 10)"))
    print("{:<20s}{:>20s}{:>20s}{:>20s}".format("Singer","Average Word Count",\
          "Vocabulary Size", "Number of Songs"))
    print('-' * 80)
    i = 0
    #counter for tracking number of artists displayed
    
    display_data = True #condition for checking whether to keep looping
   
    combined_list = sorted(combined_list, key = lambda x: x[1], reverse = True)
    #sorts list by average word count
    
    while display_data == True:
        for tup in combined_list:
             
            singer = tup[0]
            avg_count = tup[1]
            vocab_size = tup[3]
            song_count = tup[2]
                
            print("{:<20s}{:>20.2f}{:>20d}{:>20d}".format(singer,avg_count,\
                  vocab_size, song_count))
            i += 1
            if i == 10:
                display_data = False
                #only allows function to print off top 10 artists
                
                break
            

def vocab_average_plot(num_songs, vocab_counts):
    """
    Plot vocab. size vs number of songs graph
    num_songs: number of songs belong to singers (list)
    vocab_counts: vocabulary size of singers (list)
        
    """       
    pylab.scatter(num_songs, vocab_counts) #takes in list created in main
    pylab.ylabel('Vocabulary Size')
    pylab.xlabel('Number of Songs')
    pylab.title('Vocabulary Size vs Number of Songs')
    pylab.show()

def search_songs(data_dict, words):
    ''' Use the words provided by user to find artist name and song title'''
    
    song_list = [] #creates empty list
    for artist, songs in data_dict.items():
        
        for title, song in songs.items():
        
            if words.issubset(song): #checks if words can be found in song
                
                artist_song_tup = (artist,title)
                song_list.append(artist_song_tup) 
                #extract artist name and song title if words are found
                    
    song_list = sorted(song_list, key = itemgetter(0,1))
    #sort list alphabetically
        
    return song_list   
    

def main():
    ''' Calls other functions and houses graph''' 
    
    RULES = """1-) Words should not have any digit or punctuation
2-) Word list should not include any stop-word"""
    
    message1 = 'Enter a filename for the stopwords: '
    message2 = 'Enter a filename for the song data: '
    #messages to be displayed in open file function
    
    fp1 = open_file(message1)
    fp2 = open_file(message2)
    
    stopwords = read_stopwords(fp1) #set of stopwords for validation
    
    data_dictt = read_data(fp2, stopwords) #create dictionary
    
    artist_lst = [] #used to display artist tuples
    song_list = [] #used for plotting
    vocab_list = [] #used for plotting
    
    for artist in data_dictt:
        
        
        song_count = 0
        vocab_set = set() #use length of completed set to find vocabulary size
        
        for song, lyrics in data_dictt[artist].items():
            
            song_count += 1
            
            
            for word in lyrics:
                
                vocab_set.add(word)
                #add words to vocabulary set in order to find vocab size for
                #each artist
                
            
          
        song_list.append(song_count) 
        vocab_list.append(len(vocab_set))
        word_avg = calculate_average_word_count(data_dictt)
        
        tup = (artist,word_avg[artist],song_count,len(vocab_set))
        #create a tuple for every artist
        
            
        artist_lst.append(tup)
        #append tuple to list to have a collection
        

    display_singers(artist_lst)   
    
    
    
    
    plot_input = input('Do you want to plot (yes/no)?: ')
    if plot_input == 'yes':
    
        vocab_average_plot(song_list,vocab_list)
    else:
        pass
    
        
    print("\nSearch Lyrics by Words")
    search = True
    
    while search == True:
        
        i = 0 #variable that will be used to limit display to top 5 artists
        
        valid = True #checks if word is a stop word
        
        song_count = 0 
        word_set = set()
        word = input("Input a set of words (space separated), \
press enter to exit: ")

        [print(RULES) for element in word.split() if element.isdigit()\
         == True]
        #list comprehension for checking if set of words has digits
        
        [print(RULES) for element in word.split() if element.lower()\
         in stopwords]
        #list comprehension for checking if set of words contains stop words
        
        if word == '': #checks if user pressed Enter key
            
            search = False
            break
        if word.isdigit() == True:
            continue
            
        
        else:
            
            word_list = word.split()           
            for word in word_list:
               
                    word = word.lower()
                        
                    word_set.add(word)
                    if word in stopwords:
                        valid = False
                        break
                                    
            song_list = search_songs(data_dictt, word_set) 
            #calls function to identify songs containing input words
            
            for element in song_list:
                song_count += 1
                #counts # of songs
                        
            while valid == True:                        
                
                if song_count == 0:
                    print("There are {} songs containing the given words!"\
                                            .format(song_count))  
                    
                    valid = False
                    break
                                            
                else:
                    print("There are {} songs containing the given words!"\
                                            .format(song_count))  
                    print("{:<20s} {:<s}".format('Singer','Song'))             
                                            
                
                for element in song_list:
                          if i <5: #only allows for no more than 5 entries
                                                
                             print("{:<20s} {:<s}".format(element[0],\
                                   element[1]))
                             i += 1
                          else:
                             valid = False
                             break
                                    
                        
    
    

if __name__ == '__main__':
    main()           
