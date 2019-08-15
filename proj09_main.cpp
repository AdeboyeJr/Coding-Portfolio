#include "proj09_class.h"

#include<string>
using std::string;
#include<vector>
using std::vector;
#include<initializer_list>
using std::initializer_list;
#include<iostream>
using std::ostream; using std::cout; using std::cin; using std::endl;

int main(){

    char c;
    
    cin >> c;

    Element e("mymap", {"a","b","c"});
    Element g("hello", {"a","b","c"});
    Element f("testing",{"h","i","j"});
    MVM mvm({g,e,f});
    

    switch(c){

        case'a':{

            cout<< std:: boolalpha;

           

            /*

            cout <<"test " << e.key_<< endl;

            for(auto c: e.values_){
                cout<< c<< endl;
            }
            */

            cout<< e.operator==(g) <<endl;

            operator<<(cout,e);

            break;
        }

        case'b':{
            
            mvm.find_key("my map");
            mvm.find_value("a");

            break;
        }
        
        case 'c':{

            cout<< std::boolalpha;
            cout<< mvm.add("hello","q")<<endl;

            cout<< mvm.size()<<endl;
            operator<<(cout,mvm);

            break;
        }

        case 'd':{
            operator<<(cout,mvm);

            break;
        }

        case 'e':{

            vector<string> val_vect = mvm.remove_value("a");
            
            for(auto c: val_vect){
                cout<< c<< endl;
            }
            
            operator<<(cout,mvm);
            
            break;
        }
        
        case 'f':{
            cout << std::boolalpha;
            cout<<mvm.remove_key("hello")<<endl;
            operator<<(cout,mvm);
            break;
        }
        

    }


}