#include "proj09_class.h"

#include<string>
using std::string;
#include<vector>
using std::vector;
#include<initializer_list>
using std::initializer_list;
#include<iostream>
using std::ostream; using std::cout; using std::cin; using std::endl;
#include<sstream>
using std::ostringstream;

/*
                                                Project 9
                            Construct multi-variable map that contains vectors
                                                of strings 
*/
Element::Element(string key, initializer_list<string> values){

    key_ = key;
    //take in key value

    for(auto c: values){
        values_.push_back(c);
        //push back values in initializer list to string vector
    }

}


bool Element::operator==(const Element& e)const{


    if(this -> key_ == e.key_){
        //compare keys

        if(this -> values_ == e.values_){
            //compare values in keys
            return true;

        }  
    }

    return false;
    //return false if none of the criteria is met
}

ostream& operator<<(ostream& out, Element& e){
    ostringstream oss;
    oss<< e.key_<<":";
    //take in key

    copy(e.values_.cbegin(), e.values_.cend()-1, 
    std::ostream_iterator<string>(oss, ","));
    //copy elements until before last element

    oss<<e.values_.back();
    //take last element without comma

    out << oss.str();
    return out;
}

MVM::MVM(initializer_list<Element> list){

    data_ = list;
    //set data vector to initializer list

}

vector<Element>::iterator MVM::find_key(string key){
    return std::lower_bound(data_.begin(), data_.end(), key, 
            [](const Element &elem, const string &key){

                return elem.key_ < key;
                //return pointer for key inside element

            });  

}

vector<string> MVM::find_value(string val){
    vector<string> found_vect;

    for(auto c: data_){
        //iterate through multi map
        for(auto f : c.values_){
            //iterate through element

            if(f == val){
                found_vect.push_back(c.key_);
                //push back the key that contains the value
            }
        }
    }

    return found_vect;

}

bool MVM::add(string key,string value){


    vector<Element>::iterator itr = find_key(key);

    cout<< itr -> key_<<endl;
    
    if(itr != data_.end()){
        //check if key is in multi map

        

        if(itr->key_ == key){
            //if key iterator matches assigned key

            

            for(auto c: itr -> values_){
                
                cout<< c<< endl;
                
                if(c == value){
                    return false;
                    //return false if both key 
                    //and value are present
                }

               
            }

            itr -> values_.push_back(value);
            //push back onto values vector
            

        }

        else{

    
            data_.insert(itr,Element(key,{value}));
            //insert into vector if it isn't there
            
        }
         
    }

    else{
        
        data_.insert(itr,Element(key,{value}));
        //insert once end of vector has been reached  
           
    }

    return true;
    
}

size_t MVM::size(){
    size_t cnt = 0;
    for(auto c: data_){
        ++cnt;
        //increment count for every element
        //found in data
    }
    return cnt;
}

bool MVM::remove_key(string key){
    vector<Element>::iterator itr = find_key(key);

    if(itr != data_.end()){
        //check to see if end of mvm is
        //reached 

        if(itr->key_ == key){
            //if iterator key equals
            //given key

            for(auto& c: data_){
                if(c.key_ == key){
                    data_.erase(std::remove(data_.begin(),
                    data_.end(),c),data_.end());
                    //erase vector that contains key
                    
                }
            }
            return true;
        }

        else{
            return false;
        }

    }
   
    return false;
    
}



vector<string> MVM::remove_value(string value){
    vector<string> key_vect;

    for(auto& c: data_){

        size_t size1 = c.values_.size();
        //variable to compare vector size
    

        c.values_.erase(std::remove(begin(c.values_),
        end(c.values_),value),end(c.values_));
        //remove element in each vector that
        //matches value

        if(c.values_.size() < size1){
            key_vect.push_back(c.key_);
            //if the size of the vector is less than
            //original size append key to new vector
        }
    }
        
    return key_vect;
}


ostream& operator<<(ostream& out, MVM& mvm){
    ostringstream oss;
    for(auto c: mvm.data_){
        oss<< c.key_ << ":";

        copy(c.values_.cbegin(), c.values_.cend()-1, 
        std::ostream_iterator<string>(oss, ","));
        //copy elements until before last element

        oss<<c.values_.back();
        //take last element without comma

       oss<< " ";

    }


    out << oss.str().substr(0, oss.str().size()-1);
    //remove last space at the end

    return out;

}
