####################
# Project 09       #
# CSE 231 Sect 007 #
####################

#############################################################################
# Assignment Overview                                                       
#   Pokemon Statistics                                                      
#       Prompts the User For File to Read                                   
#           Re-loops until Readable File is Entered                         
#       Outputs Menu Options                                                
#           Ensures Input is Possible Listed Menu Option                    
#       Outputs Data Based on Menu Option
#           User May Input Pokemon, Abilties, or Find Matchups for Specific Pokemon                               
#       Loops Until User Quits                                              
#                                                                           
#############################################################################

#Starter Code

import csv,copy
from typing import List


EFFECTIVENESS = {0.25: "super effective", 0.5: "effective", 1:"normal", 2:"weak", 4:"super weak", 0:"resistant"}
MATCHUP_TYPES = {"resistant", "super effective", "effective", "normal", "weak", "super weak"}
TYPES = ['bug', 'dark', 'dragon', 'electric', 'fairy', 'fight', 'fire', 'flying', 'ghost', 'grass', 'ground',
 'ice', 'normal','poison', 'psychic', 'rock', 'steel', 'water']

PROMPT = '''
\nTo make a selection, please enter an option 1-3:\n
\tOPTION 1: Find Pokemon
\tOPTION 2: Find Pokemon From Abilities
\tOPTION 3: Find Matchups
\nEnter an option: '''


#Functions

def open_file(s):
    """
    Prompts user for a file
    Attemps to open file
    Loops error if invalid file
    """
    loop = True 
    while loop == True: 
        try: #loops until file is accepted
            prompt = input("Please enter a {} filename: ".format(s))
            filename = open(prompt, encoding="utf-8")
            loop = False
        except FileNotFoundError: #Error Loop
            print("This {} file does not exist. Please try again.".format(s))
    # if prompt == "pokemon.csv":
    #     file = open("pokemon.csv",encoding="utf-8")
    # elif prompt == "pokemon_small.csv":
    #     file = open("pokemon.csv",encoding="utf-8")
    return filename


def read_file(fp):
    """
    Intakes user file
    Creates a triple dictionary of:
        Generation
            Type
                Pokemon (and their stats)
    Returns Pokedex Dictionary
    """

    reader = csv.reader(fp) # attaches a reader to the file fp
    next(reader,None) # skips header line

    pokedex = {} #starting dictionary 


    '''
    #type list maker
    reader2 = reader
    for row2 in reader2:
            typesx = []
            for Types2 in reader2:
                if Types2[36] not in typesx:
                    x = Types2[36]
                    typesx.append(x)'''


    for row in reader:
        #Stats per pokemon row assignment
        gen = int(row[39])
        name = row[30]
        hp = int(row[28])
        speed = int(row[35])
        weight = float(row[38])
        caprate = int(row[23])
        legendary = row[40]
        abilities = row[0]

        #Turns legendary status into a True/False
        if legendary == '0':
            leg = False
        elif legendary == '1':
            leg = True


        #Creates 'none' type if pokemon only has 1 nature
        type1 = row[36]
        if row[37] == '':
            type2 = None
        else:
            type2 = row[37]

        type = tuple([type1,type2])


        #Creating dictionaries
        if gen not in pokedex.keys(): #dictionary of generations
            pokedex[gen] = {}

        if type not in pokedex[gen].keys(): #dictionary of types in generations
            pokedex[gen][type] = {}

        pokedex[gen][type][name] = [] #list in dictionary of names within gen/type dictionary


        stat = {}
        for m in MATCHUP_TYPES: #matchup maker
            stat[m] = set()

        #loop for matchup types and adding to pokemon dict
        #TYPES2 = typesx
        TYPES2 = TYPES
        for m in range(1,19):
            if float(row[m]) == 0:
                stat["resistant"].add(TYPES2[m-1])
            elif float(row[m]) == 0.25:
                stat["super effective"].add(TYPES2[m-1])
            elif float(row[m]) == 0.5:
                stat["effective"].add(TYPES2[m-1])
            elif float(row[m]) == 1:
                stat["normal"].add(TYPES2[m-1])
            elif float(row[m]) == 2:
                stat["weak"].add(TYPES2[m-1])
            elif float(row[m]) == 4:
                stat["super weak"].add(TYPES2[m-1])
            else: #debug catcherood
                print("BROKEN")


        list = []
        list.append(stat) #adds matchup type stats to  list

 
        #gets rid of default separators for abilities
        abilities = abilities.strip("']")
        abilities = abilities.strip("['")
        abilities = abilities.split(",")
        
        l = []
        
        #creates new separators
        for row in abilities:
            l.append(row.strip(" ,'")) #cleans up abilities
        
        l = set(l) #list into set of abilities

        #putting together list for pokemon dict
        list.append(l)
        list.append(hp)
        list.append(caprate)
        list.append(weight)
        list.append(speed)
        list.append(leg)

        pokedex[gen][type][name] = list #deepest part of triple dict

    return pokedex



def find_pokemon(pokedex, names):
    """
    Uses Dictionary and User Input
    Grabs pokemon based on Pokemon Names selected
    Returns dict
    """
    #finding by keys
    d = {}
    for list in names: #runs for every pokemon in names input

        for gen,v1 in pokedex.items(): #for generation dict

            for type,v2 in pokedex[gen].items(): #for type dict

                for pokemon,v3 in pokedex[gen][type].items(): #for pokemon dict

                    if list == pokemon: #for the pokemon in the names list..

                        better = []
                        grabber = pokedex[gen][type][pokemon] #copies and grabs
                        for x in grabber: # grabs each value in the grabber
                            if x == grabber[0]: # Checks whether the value in the grabber is the first value in order to get rid of it from the list
                                pass
                            else:
                                better.append(x) # Appends every value except the first
                        better.append(int(gen))
                        better.append(type)
                        d[list] = better #creates dictionary of the name listed pokemon and their stats

    return d
 
    
def display_pokemon(name, info):
    """
    Intakes pokemon name and dictionary
    Indexes and Organizes statistics for 'print'
    Returns a print statement of stats
    """
    name = name
    #pokedex  = [{'Lightningrod', 'Static'}, 35, 190, 6.0, 90, False, 1, ('electric', None)]
    pokedex = info

    #indexing stats
    gen = pokedex[6]
    hp = pokedex[1]
    capture = pokedex[2]
    weight = pokedex[3]
    speed = pokedex[4]


    #Legendary Display
    if pokedex[5] == True:
        legendary = "Legendary"
    elif pokedex[5] == False:
        legendary = "Not Legendary"
    else: #debugging catcher
        legendary = "?"

    l1 = []
    l2 = []

    #Combines Abilities into One Line
    for item in pokedex[0]:
        l2.append(item)
        l2.sort()
        abilities = ', '.join(l2)

    #Removes 'None' in Printing
    for piece in pokedex[7]:
        if piece != None:
            l1.append(piece)
    types = ", ".join(l1)

    #Printer
    print3 = ("\n{}\n\tGen: {}\n\tTypes: {}\n\tAbilities: {}\n\tHP: {}\n\tCapture Rate: {}\n\tWeight: {}\n\tSpeed: {}\n\t{}".format(
        name, gen, types, abilities, hp, capture, weight, speed, legendary))

    '''
    #Print Statements
    print("\n{}".format(name))
    print("\tGen: {}".format(gen))
    print("\tTypes: {}".format(types))
    print("\tAbilities: {}".format(abilities))
    print("\tHP: {}".format(hp))
    print("\tCapture Rate: {}".format(capture))
    print("\tWeight: {}".format(weight))
    print("\tSpeed: {}".format(speed))
    print("\t{}".format(legendary))
    '''

    return print3




def find_pokemon_from_abilities(pokedex, abilities): #Option 2
    """
    Intakes Pokedex dict and abilities list
    Filters through pokemon searching for list
    Returns pokemon with those specific list of abilities
    """
    pokemon = set()

    for gen,v1 in pokedex.items(): #for generation dict

        for type,v2 in pokedex[gen].items(): #for type dict

            for poke,v3 in pokedex[gen][type].items(): #for pokemon dict

                #print((pokedex[gen][type][poke][1]))
                #print(abilities)
                if (pokedex[gen][type][poke][1]) >= abilities: #checks to see if specific ability matches a 
                    #pokemon's abilities
                    
                    pokemon.add(poke) #adds specific pokemon to the set of pokemon

    return pokemon




                    
def find_matchups(pokedex, name, matchup_type): #Option 3
    """
    Finds matchups with dict, pokemon name, and certain type of matchup parameters
    Scopes through dictionaries to locate data
    Returns data
    """
    set1 = list()
    for gen,v1 in pokedex.items(): #for generation dict
        for types,v2 in pokedex[gen].items(): #for type dict
            for pokemon,v3 in pokedex[gen][types].items(): #for pokemon dict
                if name == pokemon: #if pokemon is in input list
                    try:
                        set1.append((pokedex[gen][types][pokemon][0][matchup_type])) #appends for each pokemon
                    except:
                        break #leads to None return if pokemon does not exist
    
    list3 = []
    setset = set()
    try:
        setset = set1[0] #first item in matchup_type keys
    except: #another leading to None return if pokemon does not exist
        pass
    for generation,va1 in pokedex.items(): #for generation dict
        for type,va2 in pokedex[generation].items(): #for type dict..
            type1 = set(type)
            andd = type1.intersection(setset) #intersection between setset(set of first items) and type 1(of abilities)


            if len(andd) != 0:
                for poke in pokedex[generation][type].keys(): #for pokemon dict..
                    list1 = []
                    list2 = []
                    list1.append(poke) #appends pokemon
                    list2.append(type[0]) #appends type of pokemon
                    #print(type[0])

                    if type[1] != None: #adds to list2
                        list2.append(type[1]) #appends type2 of pokemon if it exists
                    elif type[1] == None:
                        pass #Ignores type2 == none
                    else: #debug catcher
                        print("broke function matchup")

                    #Switching between lists
                    list2 = tuple(list2) #turns types of pokemon into tuple
                    list1.append(list2) #adds tuple after pokemon name
                    list1 = tuple(list1) #turns name,types into tuple
                    list3.append(list1) #combines into one list


    list3.sort() #sorts the final list
                    

    if len(list3) > 0:
        return list3 #Returns none if nothing, returns list if something




def main():
    '''
    As always, the main function
    Holds roots for all code and calls functions
    Prints data based on user input selections
    Loops until user quits
    '''
    #Given
    print("Welcome to your personal Pokedex!\n")
    fp = open_file("pokemon")
    pokedex = read_file(fp)
    option = input(PROMPT)


    while option != 'q' and option !='Q': #Loops until user quits
        if option == "1": #find pokemon
            inputlist1 = []
            printer1 = []
            
            inputs = input("\nEnter a list of pokemon names, separated by commas: ")
            
            #Splits by commas into list
            inputsplit1 = inputs.split(",")
            
            #print(inputsplit)
            for item1 in inputsplit1: #remakes inputs list(but stripped)
                #if item.strip():
                    #inputlist1.append(item)
                inputlist1.append(item1.strip())


            set1 = set(inputlist1) #turns into set
            find_pokemon1 = find_pokemon(pokedex,set1) #inputs (dict,set)

            #After Return

            for name,info in find_pokemon1.items(): #for key,value in returned dict
                display = display_pokemon(name,info)
                #print(dis) #>>>>>Prints out of order
                printer1.append(display) #adds to new list

            printer1.sort() #sorts print statements within list
            #print(printer1)
            for item2 in printer1:
                print(item2) #prints per item in list
            

            option = input(PROMPT) #Looper
        elif option == "2": #find pokemon from abilities
            inputlist2 = []
            #printer2 = []

            inputs2 = input("Enter a list of abilities, separated by commas: ")
            
            inputsplit2 = inputs2.split(",") #Splits by commas
            

            #print(inputsplit2)
            for item3 in inputsplit2: #remakes inputs list(but stripped)
                #if item3.strip():
                    #inputlist2.append(item3)
                #item3.strip()
                inputlist2.append(item3.strip())

            #Same code as Option 2 ^^, splits input into list then strips

            find_pokemon2 = find_pokemon_from_abilities(pokedex,set(inputlist2))
            list1 = list(find_pokemon2) #obtains from func and makes a list

            #After return

            list1.sort() #sorts list

            printer2 = ", ".join(list1) #seperaters
            print("Pokemon:", printer2) #prints



            option = input(PROMPT) #looper
        elif option == "3": #find matchup
            inputs = input("Enter a pokemon name: ")
            types = input("Enter a matchup type: ")

            matchup = find_matchups(pokedex,inputs,types) #grabs from function

            #fail if name doesnt exist
            if matchup == None: #fails immediately if not a real pokemon
                print("Invalid input")
                #go to option = input(PROMPT)
            elif matchup != None:
                for item in matchup: #per item
                    printy = ", ".join(item[1]) #item seperators
                    print("{}: {}".format(item[0], printy)) #prints if valid
            else: #debug chatcher
                print("Error - Option 3")


            option = input(PROMPT) #looper

        else: #fail catch
            print("Invalid option {}".format(option))
            option = input(PROMPT) #looper




if __name__ == "__main__":
    main()





'''
====Strings====
"Welcome to your personal Pokedex!\n"
"Please enter a {} filename: "
"This {} file does not exist. Please try again."
"\n" 
"\tGen: " 
"\tTypes: "
", " 
"\tAbilities: "
"\tHP: " 
"\tCapture Rate: " 
"\tWeight: " 
"\tSpeed: " 
"\tLegendary" 
"\tNot Legendary"    
"Enter an option: "
"Invalid option {}"
"\nEnter a list of pokemon names, separated by commas: "
"Enter a list of abilities, separated by commas: "
"Enter a pokemon name: "
"{}: {}"
"{}: {}, {}"
"Invalid input"

\nTo make a selection, please enter an option 1-3:\n
\tOPTION 1: Find Pokemon
\tOPTION 2: Find Pokemon From Abilities
\tOPTION 3: Find Matchups
\nEnter an option:
'''
