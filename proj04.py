####################################################
#              CSE 231 Project 4
#
#  Compose game of craps
#  Two dice with six faces each 
#  look at sum of die (up to 12)
#  if sum on first throw is 7 or 11, player wins
#  if sum is 3,2 or 12, player loses(craps)
#  any other number on first throw is a "point"
#  if you "make a point" you win
#  if you make a 7, you lose
#  keep track of bank balance
#  track wager amount
#  
####################################################


#
from random import randint  # the real Python random
#from cse231_random import randint  # the cse231 test random for Mimir testing

def display_game_rules():
    print('''A player rolls two dice. Each die has six faces.
          These faces contain 1, 2, 3, 4, 5, and 6 spots. 
          After the dice have come to rest, 
          the sum of the spots on the two upward faces is calculated. 
          If the sum is 7 or 11 on the first throw, the player wins. 
          If the sum is 2, 3, or 12 on the first throw (called "craps"), 
          the player loses (i.e. the "house" wins). 
          If the sum is 4, 5, 6, 8, 9, or 10 on the first throw, 
          then the sum becomes the player's "point." 
          To win, you must continue rolling the dice until you "make your point." 
          The player loses by rolling a 7 before making the point.''')

def get_bank_balance(balance):
    
    balance = int(input("Enter an initial bank balance (dollars): "))
    return balance

def add_to_bank_balance(balance): #function for if user wants to add funds
        balance = int(input('Enter how many dollars to add to your balance: '))
        return balance
    
        

def get_wager_amount():
    
    wager_int = int(input("Enter a wager (dollars): "))
    return wager_int

def is_valid_wager_amount(wager, balance):

      return wager <= balance #returns true or false 
      

def roll_die():
    
    die1_value = randint(1,6)  #calculates value of one of the die
    
    return die1_value 
        

def calculate_sum_dice(die1_value, die2_value):

    sum_dice = die1_value + die2_value #calculates sum of dice
    
    
    return sum_dice

def first_roll_result(sum_dice):
    if sum_dice == 7 or sum_dice==11:
            return 'win'
    elif sum_dice == 2 or sum_dice ==3 or sum_dice ==12:
            return 'loss'
    else: 
        
        return 'point'
    
    
    
def subsequent_roll_result(sum_sub, point_value):
    if sum_sub == point_value:
        return 'point'
    elif sum_sub == 7:
        return 'loss'
    else:
        return "neither"
    
   

def main(): #Function for running the game   
    
    game_start = True #Automatically starts game
    
    while game_start == True: #Checks to see if user wants to play
        
        display_game_rules() #Runs function for displaying game rules
        game_rule_skip = True
         
          
        
        balance = int(get_bank_balance('balance')) #saves balance function 
        
        
        balance_skip = True    #skips the initial balance  
        
        while game_rule_skip == True and balance_skip == True:
            
          wager = get_wager_amount() #saves wager function
          
          is_valid_wager_amount(wager, balance) 
          if wager > balance:
              print('Error: wager > balance. Try again.')
              continue
          else:
              pass
          first_roll = True
          while first_roll == True:
            
            die1_value = roll_die() #saves random dice roll to a value
            die2_value = roll_die() # saves a second random dice roll to a value
            sum_dice = calculate_sum_dice(die1_value, die2_value) #sum of the 
            #first roll
            
        
            first_roll_result('sum_dice') #import first roll result funtion
            print("Die 1:",die1_value)
            print("Die 2:",die2_value)
            print("Dice sum:", sum_dice)
            if first_roll_result(sum_dice) == 'loss':
                print('Craps.')
                print('You lose.')
                balance-= wager
                print("Balance:", balance)
                
                first_roll = False #keeps in mind that first roll is over
                game_start = False #game ends
                
                choice = input('Do you want to continue? ')
                if choice == 'yes':
                    first_roll = True
                    add_balance= input('Do you want to add to your balance? ')
                    if add_balance == 'yes':
                       balance_add = add_to_bank_balance(balance)
                       balance += balance_add
                       print('Balance:',balance)
                       
                       
                       game_start = True#resets the game
                       break
                    else: 
                        if balance == 0:
                            game_start = False
                            first_roll = False
                            game_rule_skip = False
                            balance_skip = False
                            print("You don't have sufficient balance to continue.")
                            break
                        else:
                            game_start = True
                        break
                elif choice == 'no':
                    game_start = False
                    first_roll = False
                    game_rule_skip = False
                    balance_skip = False
                    
                    break
            elif first_roll_result(sum_dice) =='win': #checks to see if player
                #won on first roll
                
                print('Natural winner.')
                print('You WIN!')
                balance += wager #adds wager to balance
                print("Balance:", balance)
                
                game_start = False
                first_roll= False #marks that it is no longer first roll
                
                choice = input('Do you want to continue? ')
                if choice == 'yes': #signifies player wants to continue
                    first_roll = True
                    add_balance = input('Do you want to add to your balance? ')
                    if add_balance == 'yes': #signifies player wants to add 
                        #funds to their balance
                        
                       balance_add = add_to_bank_balance(balance)
                       balance += balance_add #adds more money to balance
                       print('Balance:',balance)
                       game_start = True
                       
                       break
                    else:
                        game_start = True
                        break
                       
                    
                elif choice == 'no':
                    game_start = False
                    first_roll = False
                    game_rule_skip = False
                    balance_skip = False
                    break
            else:
                print('''*** Point:''', sum_dice)
                first_roll = False #automatically triggers subsequent roll 
                #function
                
                point_value = sum_dice #assigns the sum as the value of the 
                #point
                break
                
                
                 
                
            first_roll = False
            break
        
          
          while first_roll != True and game_start == True: 
              
              point_value = sum_dice #assigns point value to sum dice of 
              # first roll
              
              die3_value = roll_die() #new dice value
              die4_value = roll_die() #new dice value
              sum_sub = calculate_sum_dice(die3_value, die4_value)
              
              
              subsequent_roll_result(sum_sub, point_value) # new roll result
              
              
              
              if sum_sub == point_value: #checks to see if player matches point
                  print("Die 1:",die3_value)
                  print("Die 2:",die4_value)
                  print("Dice sum:", sum_sub)
                  print('You matched your Point.')
                  print('You WIN!')
                  balance += wager
                  print("Balance:", balance)
                  game_rule_skip = False
                  game_start = False
                  first_roll = False
                  
                  choice = input('Do you want to continue? ')
                  if choice == 'yes': #signifies player wants to continue
                    
                    add_balance = input('Do you want to add to your balance? ')
                    if add_balance== 'yes': #signifies player wants to add funds 
                        #to their balance
                        
                       balance_add = add_to_bank_balance(balance)
                       balance += balance_add
                       print('Balance:',balance)
                       game_start = True
                       game_rule_skip = True
                       break
                    else:
                        game_start = True
                        game_rule_skip = True
                        break
                       
                    game_start = True #allows player to play again
                    break
                  else:
                    game_start = False #game is over
                    first_roll = False
                    break
                  
                  break
                  
              elif sum_sub == 7: #checks to see if player lost 
                  print("Die 1:",die3_value)
                  print("Die 2:",die4_value)
                  print("Dice sum:", sum_sub)
                  print('You lose.')
                  balance -= wager
                  print("Balance:", balance)
                  game_rule_skip = False
                  game_start = False
                  first_roll = False
                  
                  choice = input('Do you want to continue? ')
                  if choice == 'yes': #signifies player wants to continue
                    
                    add_balance = input('Do you want to add to your balance? ')
                    if add_balance== 'yes': #signifies player wants to add funds 
                        #to their balance
                        
                       balance_add = add_to_bank_balance(balance)
                       balance += balance_add
                       print('Balance:', balance)
                       game_start = True
                       game_rule_skip = True
                       break
                    else:
                        if balance == 0:
                            game_start = False
                            first_roll = False
                            game_rule_skip = False
                            balance_skip = False
                            print("You don't have sufficient balance to continue.")
                            break
                        else:
                          game_start = True
                          game_rule_skip = True
                        break
                       
                    game_start = True #allows player to play again
                    break
                  else:
                    game_start = False #game is over
                    first_roll = False
                    break
                  
                  break
                  
                  
              else:
                  print("Die 1:",die3_value)
                  print("Die 2:",die4_value)
                  print("Dice sum:", sum_sub)
                  continue
        
     
    else:
        print('Game is over.') #game ends
        
        
    

if __name__ == "__main__": #runs main function
    main()     