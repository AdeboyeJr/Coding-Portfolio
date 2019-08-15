################################################
#
#                  Project 11
#
#-Create a game with virtual pets
#-Edit attributes in pet class
#-Design methods for eating and drinking
#-Create status methods
#-Allow user to alter default attributes of 
#either dog or cat
#-Run code and prompt for activity
#-Allow user to display pet status
################################################

from cse231_random import randint
from edible import *

MIN, MAX = 0, 10
dog_edible_items = [DogFood]
cat_edible_items = [CatFood]
dog_drinkable_items = [Water]
cat_drinkable_items = [Water]
#edible items for each species of pet

class Pet(object):
    def __init__(self, name='fluffy', species='dog', gender='male',\
                 color='white'):
        '''Construct and give attributes to Pet object'''
        
        self._name = name.capitalize()
        self._species = species.capitalize()
        self._gender = gender.capitalize()
        self._color = color.capitalize()
        self._edible_items = []
        self._drinkable_items = []
        #define attributes for pet object

        self._hunger = randint(0,5)
        self._thirst = randint(0,5)
        self._smell = randint(0,5)
        self._loneliness = randint(0,5)
        self._energy = randint(5,10)
        #save instance status attributes to random integers

        self._reply_to_master('newborn')
        #start off with newborn string

    def _time_pass_by(self, t=1):
        # this function is complete
        self._hunger = min(MAX, self._hunger + (0.2 * t))
        self._thirst = min(MAX, self._thirst + (0.2 * t))
        self._smell = min(MAX, self._smell + (0.1 * t))
        self._loneliness = min(MAX, self._loneliness + (0.1 * t))
        self._energy = max(MIN, self._energy - (0.2 * t))
        
        #allows natural progression of time

    def get_hunger_level(self):
        '''Returns hunger level'''
        return self._hunger
        

    def get_thirst_level(self):
        '''Returns thirst level''' 
    
        return self._thirst

    def get_energy_level(self):
        '''Returns energy level'''
        return self._energy
    
    def drink(self, liquid):
        '''Pet quenches thirst'''
        
        if isinstance(liquid, tuple(self._drinkable_items)):
            #checks if instance can be found within list of drinkable items
            self._time_pass_by(t=1)
            
            drink_quantity = liquid.get_quantity()
            #retrieve qunatity of liquid for consumption
            
            if self._thirst >= 2:
                #checks if thirst is above threshold
                
                if self._thirst > drink_quantity:    
                    self._thirst -= drink_quantity 
                    #if thrist is above drinking quantity, subtract quantity
                    #from thirst
                    
                else:
                    self._thirst = 0
                    #if drinking quantity is greater than thirst, set thirst 
                    #equal to zero to prevent negative numbers
                    
                self._reply_to_master('drink')   
            else:
                print("Your pet is satisfied, no desire for sustenance now")
                #print statement if thirst is too low
        else:
            print('Not drinkable')
        
        
        
        self._update_status()
        

    def feed(self, food):
        '''Pet is fed'''
        
       
        if isinstance(food, tuple(self._edible_items)):
            self._time_pass_by(t=1)
          
               
            feed_quantity = food.get_quantity()
            if self._hunger >= 2:
                #checks if hunger is above threshold
                
                if self._hunger > feed_quantity:
                        self._hunger -= feed_quantity
                        #if hunger is greater than the food quantity, subract
                        #the quantity from hunger
                        
                else:
                        self._hunger = 0
                        #set hunger to zero to avoid negatives
                        
                self._reply_to_master('feed')
                
            else:
                print("Your pet is satisfied, no desire for sustenance now")
        else:
            print('Not edible')
                
        
        self._update_status()


    def shower(self):
        '''Clean pet'''
        self._time_pass_by(t=4)
        #set default time pass to 4 units
        self._smell = 0
        #set smell down to zero
        
        if self._loneliness > 4:
            self._loneliness -= 4
            #subtract 4 for loneliness so long as its value is greater than 4
        else:
            self._loneliness = 0
        
        self._update_status()
        self._reply_to_master('shower')


    def sleep(self):
        '''Allow pet to sleep'''
        self._time_pass_by(t=7)
        self._energy += 7
        #add 7 to the energy status
        
        if self._energy > MAX:
            #set energy to 10 if it is above the max value
            
            self._energy = 10
            
        self._update_status()
        self._reply_to_master('sleep')
            
    def play_with(self):
        '''Play with pet'''
        self._time_pass_by(t=4)
        self._energy -= 4
        #subtract energy by 4
        
        self._loneliness -= 4
        #subtract loneliness by 4
        
        self._smell += 4
        #increse smell by 4
        
        if self._energy < MIN:
            #set energy to zero is its value is below the minimum value
            
            self._energy = 0
            
        if self._loneliness < MIN:
            self._loneliness = 0
            #set loneliness to zero if loneliness goes below the minimum value
            
            
        if self._smell > MAX:
            self._smell = 10
            #set smell to 10 if smell goes above the maximum value
            
        self._update_status()
        self._reply_to_master('play')
        
    def _reply_to_master(self, event='newborn'):
        '''Virtual pet responds to master using adorable emoticons'''
        
        faces = {}
        talks = {}
        faces['newborn'] = "(๑>◡<๑)"
        faces['feed'] = "(๑´ڡ`๑)"
        faces['drink'] = "(๑´ڡ`๑)"
        faces['play'] = "(ฅ^ω^ฅ)"
        faces['sleep'] = "୧(๑•̀⌄•́๑)૭✧"
        faces['shower'] = "( •̀ .̫ •́ )✧"

        talks['newborn'] = "Hi master, my name is {}.".format(self._name)
        talks['feed'] = "Yummy!"
        talks['drink'] = "Tasty drink ~"
        talks['play'] = "Happy to have your company ~"
        talks['sleep'] = "What a beautiful day!"
        talks['shower'] = "Thanks ~"

        s = "{} ".format(faces[event])  + ": " + talks[event]
        print(s)

    def show_status(self):
        '''Display attribute data'''
        name = ['Energy','Hunger','Loneliness','Smell','Thirst']
        #list to display status
        
        data_list = (self._energy,self._hunger,self._loneliness,self._smell,\
                     self._thirst)
        #data stored in alphabetical order
        
        i = 0
        
        for attribute in data_list:
            attr_name = name[i] 
            #use the variable to iterate through name list
            s = "{:<12s}: [{:<20s}]".format(attr_name,'#'*(round(attribute)*2))\
                 + "{:5.2f}/{:2d}".format(attribute,10)
                 
            i += 1
            #add to variable to get next name
            
            print(s)
        
        
    def _update_status(self):
        '''Updates status of pet'''
        # this function is complete #
        faces = {}
        talks = {}
        faces['default'] = "(๑>◡<๑)"
        faces['hunger'] = "(｡>﹏<｡)"
        faces['thirst'] = "(｡>﹏<｡)"
        faces['energy'] = "(～﹃～)~zZ"
        faces['loneliness'] = "(๑o̴̶̷̥᷅﹏o̴̶̷̥᷅๑)"
        faces['smell'] = "(๑o̴̶̷̥᷅﹏o̴̶̷̥᷅๑)"

        talks['default'] = 'I feel good.'
        talks['hunger'] = 'I am so hungry ~'
        talks['thirst'] = 'Could you give me some drinks? Alcohol-free please ~'
        talks['energy'] = 'I really need to get some sleep.'
        talks['loneliness'] = 'Could you stay with me for a little while ?'
        talks['smell'] = 'I am sweaty'

class Cat(Pet):
    '''Inherits most of the attributes from Pet Class'''
    def __init__(self,name='fluffy',gender='male',color='white',species='cat'):
        
        Pet.__init__(self,name,'Cat', gender,color)

        self._edible_items.extend(cat_edible_items)
        self._drinkable_items.extend(cat_drinkable_items)
        #add consumable cat items to empty lists in pet class
        

class Dog(Pet):
    '''Inherits most of the attributes from Pet Class'''
    def __init__(self,name='fluffy',gender='male',color='white',species='dog'):
       
        Pet.__init__(self,name,'Dog', gender,color)
       
        self._drinkable_items.extend(dog_drinkable_items)
        self._edible_items.extend(dog_edible_items)
        #add consumable dog items to empty lists in pet class
        
        
        
        
   

def main():
    '''Runs all functions and  uses cat or dog subclasses'''
    
    print("Welcome to this virtual pet game!")
    play = True
    #initial condition for checking if player wants to play
    while play:
        prompt = '''Please input the species (dog or cat), name, gender\
 (male / female), fur color of your pet, seperated by space \n
 ---Example input:  [dog] [fluffy] [male] [white] \n
 (Hit Enter to use default settings): '''
    
        user_input = input(prompt).strip().split()
        #prompts user to input species, name, gender and color of their ideal
        #pet
        
        species = ''.join(user_input[0])
        name = ''.join(user_input[1])
        gender = ''.join(user_input[2])
        color = ''.join(user_input[3])
        #saves each element in the list as a variable
        
      
            
               
        
            
       
        if species.lower() == "dog":
            pet = Dog(name,species,gender,color)
            
        elif species.lower() == "cat":
            pet = Cat(name, species, gender, color)
        else:
            continue
        #if the species is neither a cat nor dog, go through process again
            
       
        q = False
        #checks if player wants to quit game
        
        intro = "\nYou can let your pet eat, drink, get a shower, \
get some sleep, or play with him or her by entering each of the following\
 commands:\n --- [feed] [drink] [shower] [sleep] [play]\n You can also check \
the health status of your pet by entering:\n --- [status]."
        print(intro)
        
        while not q:
            feed = True
            #allows pet to eat
            
            drink = True
            #allows pet to drink
            
            prompt = "\n[feed] or [drink] or [shower] or [sleep] or [play] or\
 [status] ? (q to quit): "
            activity = input(prompt).lower()
            #variable that is used to determine what to do with pet
            
            if activity == 'feed':
                
                while feed:
                
                    food_amount = input('How much food ? 1 - 10 scale: ')
                    
                    
                    if food_amount.isdigit() == False:
                        #checks to see if user input words instead of numbers
                        
                        print('Invalid input.')
                        continue
                    
                    elif int(food_amount) < 1 or int(food_amount) >10:
                        #checks if user input falls within range
                        print('Invalid input.')
                        continue
                    
                    else:
                        if species.lower() == 'dog':
                            
            
                            food = DogFood(int(food_amount))
                            pet.feed(food)
                            #feeds dog dog food
                            
                            feed = False
                            break
                            
                        elif species.lower() == 'cat':
            
                            food = CatFood(int(food_amount))
                            pet.feed(food)
                            #feeds cat cat food
                            
                            feed = False
                            break
                        
                
            elif activity == 'drink':
                
                while drink:
                    liquid_amount = input('How much drink ? 1 - 10 scale: ')
                    
                    if liquid_amount.isdigit() == False:
                        #checks if user input words instead of numbers
                        print('Invalid input.')
                        continue
                    
                    elif int(liquid_amount) < 1 or int(liquid_amount) > 10:
                        #checks if user input falls within range
                        print('Invalid input.')
                        continue
                    
                    else:
                        water = Water(int(liquid_amount))
                        pet.drink(water)
                        #feeds either pet water
                        
                        drink = False
                        break
                    
            elif activity == 'shower':
                pet.shower()
                #cleans pet
                
            elif activity == 'sleep':
                pet.sleep()
                #allows pet to rest
                
            elif activity == 'play':
                pet.play_with()
                #play with pet
                
            elif activity == 'status':
                pet.show_status()
                #display table of pet's status conditions
                
            elif activity == 'q':
                q = True
                play = False
                #player chooses to exit game; program ends
                
                break
            else:
                
                #if user input a command that doesn't follow pet guidelines
                print('Invalid command.')
       

    print("Bye ~")



if __name__ == "__main__":
    main()