#include<iostream>
using std::ostream; using std::cout; using std::cin; using std::boolalpha; using std::endl;
#include<ostream>
using std::ostringstream;



#include<vector>
using std::vector;
#include<string>
using std::string;
#include "proj06_functions.h"

int main(){
    cout<< boolalpha;
    char letter;
    
    cin >> letter;

    std::vector<long> num = {1,2,3,4,5,6,7,8,9,10,11,12}, num2= {11,12,13,14,15,21,22,23,24,25,31,32,33,34,35,41,42,43,44,45}, num3 = {11};

    switch(letter){
           
        case 'a':{
        
            print_vector(num, cout);
            break;

        }

        case 'b':{
            int rows, cols;
            cin>> rows>> cols;
            
            cout<<four_corner_sum(num, rows, cols) <<endl;
            break;

        }

        case 'c':{
           int rows, cols;
           cin >> rows >> cols;

           print_vector(rotate_rows_up(num2, rows,cols),cout);
           break;
        }

        case 'd':{
            int rows, cols;
            cin >> rows >> cols;

            print_vector(column_order(num2, rows, cols),cout);
            break;
        }

        case 'e':{
            int rows, cols;
            cin >> rows >> cols;

            print_vector(matrix_ccw_rotate(num, rows, cols),cout);
            break;
        }

        case 'f':{
            int rows, cols;
            cin >> rows >> cols;

            cout<< max_column_diff(num2, rows, cols) <<endl;
            break;
        }

        case 'g':{
            int rows, cols;
            cin >> rows >> cols;

            cout<< trapped_vals(num2, rows, cols);
            break;
        }
        

    }//end of switch
    

}//end of main