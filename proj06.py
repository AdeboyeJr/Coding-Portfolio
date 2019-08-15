#####################################################
#
#                    Project 6
#
# Take two data files to analyze
# Find the indexes of strings in the header
# return tuple of items in both the 2016 file and the
# 2000 file
# Calculate total number of native born citizens,
# naturalized citizens and non citizens
# Ask if user wants to plot a graph
# If yes, plot a graph using pylab 
# (function already given)
#
#####################################################


import pylab   # for plotting
from operator import itemgetter  # useful for sorting

def open_file():
    '''Opens file for reading'''
    while True:
        try: 
            file_name = input("Enter a file name: ")
            fp = open(file_name, 'r')
            
            return fp
        except FileNotFoundError:
            print("Error. Please try again.")

def find_index(header_lst,s):
    '''Searches for header index of string in file'''
    if s in header_lst: #iterates through each string in the header
        
        inx = header_lst.index(s) #saves index as the index of the string
        return inx
    else:
        return None
      
def read_2016_file(fp):
    '''Returns a sorted list of tuples'''
    
    nation = [] 
    pop_count = 0 #count of the total population
    header_lst = fp.readline().strip().split(',')
    fp.readline()
    for line in fp:
        
        line_lst = line.strip().split(',')
        
        state = line_lst[2]
        
        
        native = find_index(header_lst,'EST_VC197') #utilzes find index function
        #takes string finds the index within the header list
        
        native_value = int(line_lst[native]) #finds the actual value of the 
        #line at the index
        
        
        
        
        naturalized = find_index(header_lst, 'EST_VC201')
        naturalized_value = int(line_lst[naturalized])
        
        
        non_citizen = find_index(header_lst, 'EST_VC211')
        non_citizen_value = int(line_lst[non_citizen])
        
        pop_count = native_value + naturalized_value + non_citizen_value
        #sum of all types of residents
        
        ratio_naturalized = naturalized_value/pop_count 
        
        ratio_non_citizen = non_citizen_value/pop_count
        
        st=(state, native_value, naturalized_value, ratio_naturalized,\
            non_citizen_value, ratio_non_citizen)  #save tuple as a variable
        
        nation.append(st) #append variable to empty list
            
    
    
    
    nation.sort(key = itemgetter(5)) #sorts list
    
        
   
    return nation
        
    
    
def read_2000_file(fp2):
    '''Returns sorted list of tuples in second data file'''
    header_lst= fp2.readline().strip().split(',') #splits each line into a list
    #of elements
    
    fp2.readline()[3]
    for line in fp2:
        line_lst = line.strip().split(',') #splits line into a list of elements
        
        total_population = find_index(header_lst,'HC01_VC02') #Implements 
        #fund index funciton and locates string index
        
        pop_value = int(line_lst[total_population])
        
        native = find_index(header_lst,'HC01_VC03')
        native_value = int(line_lst[native])
        
        naturalized = find_index(header_lst,'HC01_VC05')
        naturalized_value = int(line_lst[naturalized])
        
        non_citizen = find_index(header_lst,'HC01_VC06')
        non_citizen_value = int(line_lst[non_citizen])
        
    data_tup = (pop_value,native_value, naturalized_value, non_citizen_value)
    #create new tuple
    
    return data_tup

def calc_totals(data_sorted):
    '''Makes a sorted list of data from file'''
    native_count,naturalized_count,non_citizen_count = 0,0,0
    #counters for residents
    
    total_resident = 0
    for element in data_sorted:
        
        native_count += int(element[1]) #adds second element in tuple to counter
        
        naturalized_count += int(element[2]) #adds third element in tuple to
        #counter
        
        non_citizen_count += int(element[4]) #adds fifth element in tuple ot 
        #counter

    
    total_resident = native_count + naturalized_count + non_citizen_count
    #finds total number of residents
    
    data_sorted = (native_count,naturalized_count,non_citizen_count,\
                   total_resident) #creates a tuple of data

    return data_sorted
        
        
    
    
 

def make_lists_for_plot(native_2000,naturalized_2000,non_citizen_2000,\
                        native_2016,naturalized_2016,non_citizen_2016):
    '''Organize a list of values for plottting'''
    native_lst = [native_2000,native_2016] 
    naturalized_lst = [naturalized_2000,naturalized_2016]
    non_citizen_lst = [non_citizen_2000,non_citizen_2016]
    
    plot_tup = (native_lst,naturalized_lst,non_citizen_lst)
    #creates a tuple of all the lists
    
    return plot_tup
    
def plot_data(native_list, naturalized_list, non_citizen_list):
    '''Plot the three lists as bar graphs.'''

    X = pylab.arange(2)   # create 2 containers to hold the data for graphing
    # assign each list's values to the 3 items to be graphed, include a color
    #and a label
    pylab.bar(X, native_list, color = 'b', width = 0.25, label="native")
    pylab.bar(X + 0.25, naturalized_list, color = 'g', width = 0.25,\
              label="naturalized")
    pylab.bar(X + 0.50, non_citizen_list, color = 'r', width = 0.25,\
              label="non-citizen")

    pylab.title("US Population")
    # label the y axis
    pylab.ylabel('Population (hundred millions)')
    # label each bar of the x axis
    pylab.xticks(X + 0.25 / 2, ("2000","2016"))
    # create a legend
    pylab.legend(loc='best')
    # draw the plot
    pylab.show()
    # optionally save the plot to a file; file extension determines file type
    #pylab.savefig("plot.png")

def main(): 
    '''Execution of program; amalgam of functions'''
    fp = open_file()
    fp2 = open_file()
    
   
    
    
    print('\n{:>80s}'.format('2016 Population: Native, Naturalized,\
 Non-Citizen'))
    print('\n{:<20s}{:>15s}{:>17s}{:>22s}{:>16s}{:>22s}'.format("State",\
          "Native","Naturalized","Percent Naturalized", "Non-Citizen",\
          "Percent Non-Citizen"))
    
    #counters for residents
    native_count = 0
    naturalized_count = 0
    non_citizen_count = 0 
    
    native_count2, naturalized_count2,non_citizen_count2 = 0,0,0
    
    nation_lst = read_2016_file(fp)
    nation_lst2 = read_2000_file(fp2)
    
    
    for tuple in nation_lst:
        #iterate through file and add residents to counters
        
        print('{:<20s}{:>15,}{:>17,}{:>21.1f}%{:>16,}{:>21.1f}%'.format\
              (tuple[0],tuple[1],tuple[2],tuple[3]*100,tuple[4],tuple[5]*100))
        
        native_count += tuple[1]
        naturalized_count += tuple[2]
        non_citizen_count += tuple[4]
       
    for object in nation_lst2:
        native_count2 = nation_lst2[1]
        naturalized_count2 = nation_lst2[2]
        non_citizen_count2 = nation_lst2[3]
        
    print('-'*112) 
    #prints dashed line
    
    
    total_tup = calc_totals(nation_lst)
    total = int(total_tup[3])
    
    
    total2 = native_count2+naturalized_count2+non_citizen_count2
    
    #formatting string for year 2016
    print('{:<20s}{:>15,}{:>17,}{:>21.1f}%{:>16,}{:>21.1f}%'.format('Total\
 2016',native_count,naturalized_count,(naturalized_count/total)*100,\
          non_citizen_count,(non_citizen_count/total)*100))
    
    #formatting string for year 2000
    print('{:<20s}{:>15,}{:>17,}{:>21.1f}%{:>16,}{:>21.1f}%'.format('Total\
 2000',native_count2,naturalized_count2,naturalized_count2/total2*100,\
          non_citizen_count2,non_citizen_count2/total2*100))
    
    pylab_prompt = input("Do you want to plot? ")
    if pylab_prompt == 'yes':
       
     #function for organized graph data
      plot_list = make_lists_for_plot(native_count2,naturalized_count2,\
                          non_citizen_count2,native_count,\
                          naturalized_count,non_citizen_count)
      native_lst = plot_list[0] 
      naturalized_lst = plot_list[1]
      non_citizen_lst = plot_list[2]   
      
      #plot graph from list of data 
      plot_data(native_lst, naturalized_lst, non_citizen_lst)
      
    else:
        pass
    
    #close files
    fp.close()
    fp2.close()
    
if __name__ == "__main__":
    main()
