#include<iostream>
using std::ostream; using std::cout; using std::endl;

#include<vector>
using std::vector;
#include<string>
using std::string;
#include "proj06_functions.h"


/*
                                                Project 6
                                Work with streams and manipulate 2D vectors
*/

ostream& print_vector(const vector<long>&v, ostream& out){
    
    for(auto element : v){

        if(element!= v.back())

            out << element << ",";
            //iterate through vector and add comma to the end
            //so long as the for loop doesn't reach the end of vector

        else
            out<<element;
            //print just the element once end of vector
            //is reached
     
    }
    
    return out;  
}


long four_corner_sum(const vector<long>& v, int rows, int cols){
    long sum= 0;
    
    
    if(rows <=2 && cols <= 2)
        return 0;
        //return 0 if the vector is too small

    else{
        
        sum += v.front() + v[cols-1] + v[v.size()-cols] + v.back();
        //add together all the four corners corresponding to their
        //indeces
        
        return sum;
       
    }
   
}

vector<long> rotate_rows_up(const vector<long>& v, int rows, int cols){
    vector<long> vector;

    if(rows < 2)
        return vector;
        //return empty vector if number of rows is less than two

    else{
        for(int i = cols; i<v.size();++i){
            vector.push_back(v[i]);
            //append elements starting with second row
        }
        for(int i= 0; i<cols; ++i){
            vector.push_back(v[i]);
            //add elements from the first row to the end of vector
        }
    }
    
    return vector;

    
}

vector<long> column_order(const vector<long>& v, int rows, int cols){

    vector<long> vector;//create new vector
   
    for(int i = 0; i < cols; ++i){//iterate through each column

        for(int j=i; j < v.size(); j+= cols){//iterate through each row

            int num = v[j];
            
            
            vector.push_back(num);//add number to empty vector     
        }
    }
    return vector;
    
}


vector<long> matrix_ccw_rotate(const vector<long>& v, int rows, int cols){

    vector<long> vector;//create new vector

    
    for(int i = cols-1; i >= 0; --i){//iterate through each column in reverse

            for(int j=i; j < v.size(); j += cols){//iterate through each row

                int num = v[j];
                
                cout <<num << endl;
                vector.push_back(num);//add number to empty vector     
            }
    }

    return vector;
}

long max_column_diff(const vector<long>& v, int rows, int cols){
    long first_column_sum = 0, subsequent_column_sum=0, max_diff = 0, diff;
    //keepts track of sums

    for(int i=0; i<v.size(); i +=cols){
        first_column_sum += v[i];
        //find first sum
    }
    

    for(int i=1; i<cols; ++i){
        for(int j=i; j< v.size(); j+=cols){
            subsequent_column_sum += v[j];
            //find sum of each column in matrix
        }
        

        diff = subsequent_column_sum - first_column_sum;
        //subtract first sum from each of the
        //subsequent columns
        

        if(diff > max_diff)
            max_diff = diff;
            //if difference is greater than current max diffrence,
            //difference becomes the new max

        subsequent_column_sum = 0;
    }

    return max_diff;

}

bool check_neighbors(const vector<long>& v, int rows, int cols, long e){
    int neighbors = 0, front, behind, below, above, column_track= 0;

    
        for(int i=0; i < v.size(); ++i){
            
            
            if(v[i] == e){
                front = v[i+1];
                behind = v[i-1];
                above = v[i-cols];
                below = v[i+cols];
                //default positions of neigboring values
                
                if((i+1)%cols == 0){
                    ++column_track;
                    //keepts track of column

                }
        
                

                if(i%cols == 0){// if it is the far left vertical column
                    
                    behind = v[i+(cols-1)];
 
                }

                if(i < cols){//if it is the top horizontal column
                    
                    above = v[i+(cols*(rows-1))];
                   
                }


                
                
                if(column_track > 0){//if it is the far right vertical column
                    front =  v[i-(cols-1)];
                    column_track = 0;
                    
                }

                if(i >= (rows-1)*cols){//if it is the bottom horizontal column
                   
                    below = v[i-(cols*(rows-1))];

                }
                
                
            }

        }

        //checking to see if the number in question is trapped
        if(front > e)
            ++neighbors;

        if(behind > e)

            ++neighbors;

        if(above > e)
            ++neighbors;
                
        if(below > e)
            ++neighbors;
        

        if(neighbors == 4)
             return true;
        //if all neigboring numbers are greater than given number
        //it is indeed trapped
        
        return false;
      
}

long trapped_vals(const vector<long>& v, int rows, int cols){
    long trapped_count = 0;

    for(auto c: v){//iterate through every element in vector

        if(check_neighbors(v, rows, cols, c)){
            ++trapped_count;
        }
        //pass bool function to check if value is trapped
        //if it is, add to count

    }

    return trapped_count;
}