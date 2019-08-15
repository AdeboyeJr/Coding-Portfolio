#include<iostream>
using std::cout; using std::cin; using std::endl; using std::boolalpha;
using namespace std; 
using std::getline;
#include<cmath>
using std::pow;
#include "proj05_functions.h"

#include<string>
using std::string;

/*  
                                                   Project 5
    Steganography. Encode a secret message within plain text and then decode

*/

string s, bit_string, plaintext, secret_message, to_decode;
char c;

string lower_case(const string &s){

    string new_string = "";

    for (auto c : s){ //iterates through each character in string
        
        if (isalpha(c)){
            if (isupper(c)){
                c = tolower(c);
                new_string.append(1,c);
                //makes character lower cased if it is already upper
            }
        
            else{
                new_string.append(1,c);
                continue;
            }
        }
        else{
            new_string.append(1,c);
            continue;
            //if character is not a letter, move on
        }
        
    }
    return new_string;
}

string to_binary(char c){
    
    int index_num, string_num, count = 0;

    string starting_num, num, num_string="", binary_string = "";
    string final_string="";

    
    index_num = static_cast<int>(c) - static_cast<int>('a');
    //use ascii table to find integer value, then subtract integer 
    //value of a to get index value
    

    if(isupper(c))
        return "";
        //return empty string if character isn't lower cased
    if(!isalpha(c))
        return "";

    else{
            if (index_num%2 == 0)
                string_num = 2;
            else
                string_num = 1;
            starting_num = std::to_string(string_num);
            num_string.append(starting_num);
            

            while (index_num >1 && count<=5){
                
                index_num /= 2;
                //Divide number by 2 and set value as new number
                
                string_num = index_num;
                if(string_num >= 10){
                    if(index_num%2 == 0)
                        string_num = 2;
                    else
                        string_num = 1;
                    
                }
               

                num = std::to_string(string_num);
                num_string.append(num);
                //convert value to string and append value to empty string
                
                ++count;
                
            }
            std::reverse(num_string.begin(), num_string.end());
            //once string is complete, reverse it
            
            
            
            binary_string.append(num_string);
            //once reversed, add new_string to binary string that 
            //accomadates number of zeroes

            for (auto c : binary_string){
                int s = (int)c;
                
            
                if(s%2 == 0){


                    
                    c = '0';
                    //set character to zero if number is even
                    
                    final_string.append(1,c);
                    //append to last empty string
                }
                else{
                    c = '1';
                    //set character to 1 if number is odd
                    
                    final_string.append(1,c);
                }
                
            }

            while(final_string.length() < 5)
                final_string = '0' + final_string;

            while(final_string.length() > 5)

                final_string.pop_back();   
                
                //pop of end of string until it is only a length 
                //of 5  
            
            return final_string;

    }
}


char from_binary(const string &bit_string){

    int decimal = 0, pow_num = bit_string.length()-1;
    string letter = "abcdefghijklmnopqrstuvwxyz";
    char chr;

    string num_string;

    if(bit_string.length()> 5)
        return '0';
        //return 0 if the length of string is greater than 5

    for(auto c : bit_string){

        if(isupper(c))
            return '0';
        //if character is upper cased, return 0

        if (c != '1' && c!= '0')
            return '0';
        //if there is a character within the string that isn't 1 or 
        //0, return 0
        
    }

    for (auto c : bit_string){
        int s=0;
        if(c == '0')
            s = 0;

        else if(c == '1')
            s = 1;
            
        decimal += s*pow(2,pow_num);
        //convert bit stirng into an index using arithmetic
        --pow_num;


    }
    
    
    chr = letter[decimal];
    //use decimal as an index to seach for character in letter string

    return chr;
}

bool check_message(const string &plaintext, const string &secret_message){
    int plain_count = 0, secret_count = 0;
    //keeps track of length of plain text and secret message

    for (auto c: plaintext){
        if(isalpha(c))
            ++plain_count;
    }
    //count number of characters within plaintext

    for (auto c: secret_message){
        if(isalpha(c))
            ++secret_count;
    }
    //count number of characters within secret message

    if(plain_count >= secret_count*5)
        return true;
        //the plain text is usable if the number of characters is at lease five 
        //times greater than the amount in secret message

    else
        return false;
    
} 

string encode(const string &plaintext, const string &secret_message){
    string binary_message= "", binary_string, new_message = "",chr, new_string;
    string plain_text = plaintext, secret_text = secret_message;
    int count = 0;

    plain_text=lower_case(plain_text);
    secret_text=lower_case(secret_text);
    
    

    if (!check_message(plain_text,secret_text))
        return "Error";
    //if the plain text doesn't meet the qualifications, an error message
    //is returned

    else{
        

        for(auto c : secret_text){
            if(isalpha(c)){
                binary_string = to_binary(c);
                binary_message.append(binary_string);
                //convert each character to a binary value
                //and create string of binary numbers
            }
            else
                continue;
            
                
        }


        for(auto c: binary_message){
           
            while(!isalpha(plain_text[count])){
                new_message.append(1,plain_text[count]);
                ++count;
                
                //only account for alphabetic characters
            }

            if(c == '1'){
                chr = toupper(plain_text[count]);

                new_message.append(chr);
                ++count;
                //make character in plain text upper cased if 
                //value in binary message is 1
             }

            else if(c == '0'){
                chr = tolower(plain_text[count]);

                    
                new_message.append(chr);
                ++count;
                //make character in plain text lower cased if
                //value in binary message is 0
            }
            
        }
        new_string = plain_text.substr(count);
        new_message += new_string;
        //add remainding parts of plain text to final message
     
    }
    return new_message;
}

string decode(const string &to_decode){
    int count = 0;
    string binary_string= "", decode_string="",final_string="";
    

    for (auto c: to_decode){
        if(isupper(c)){
            
            binary_string.append(1,'1');
            ++count;
        }
        //adds 1 to binary string for every upper cased character

        if(islower(c)){
            binary_string.append(1,'0');
            ++count;
        }
        //adds 0 to binary string for every lower cased character

        if(count== 5){
            binary_string.append(1,'2');
            count = 0;
        }
        //if the count reaches 5, insert an arbitrary separator to indicate
        //end of binary set 
        
     
    }
    

    for(auto c: binary_string){
        if (c != '2'){
            decode_string.append(1,c);
        }
        //append to decode string as long as character isn't arbitrary number
        else{
           
            final_string.append(1,from_binary(decode_string));
            decode_string = "";
            
        }
        //if the character happens to be arbitrary number, call the from 
        //binary function to extract the corresponding character
    }

    return final_string;
}