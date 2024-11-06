#!/usr/bin/python3
import itertools


##################################
# ORGANISATION WORDLIST FUNCTION #
##################################
def create_org_wordlist(name, dob):
  # Split the name and the date of birth by spaces
  name_parts = name.split()
  dob_parts = dob.split()
  # Take year out of dob
  yob = dob[-2:]
  yob_full = dob[-4:]
  db = dob[:+2]

  # Initialize an empty list to store the words
  wordlist = []

  # Initialise a list to store commonly used symbols
  symbols = ["!", "?", "*"]

  # Loop through the name parts and add them to the wordlist
  for part in name_parts:
    wordlist.append(part)

  # Loop through the name parts and the date of birth parts and combine them in different ways
  for i in range(len(name_parts)):
    for j in range(len(dob_parts)):
      # Add the name part followed by the date of birth part, db, yob and yob_full
      wordlist.append(name_parts[i] + yob)
      wordlist.append(name_parts[i] + yob_full)
      wordlist.append(name_parts[i] + db)
      # Add the date of birth part followed by the name part
      wordlist.append(dob_parts[j] + name_parts[i])

  #DO MORE CHANGING AND SWAPPING WORK HERE

  #GET THE SCRIPT TO LOG THE WORDLIST IN A TEXT FILE

  return wordlist

##############################
# PERSONAL WORDLIST FUNCTION #
##############################
def create_person_wordlist(name, dob, petNames, nick, hobbies):
  # Split the lists provided in questions by spaces
  name_parts = name.split()
  dob_parts = dob.split()
  petNames_parts = petNames.split()
  nick_parts = nick.split()
  hobbies_parts = hobbies.split()

  # Take year out of dob
  yob = dob[-2:]
  yob_full = dob[-4:]
  # Take day out of dob
  db = dob[:+2]

  # Initialize an empty list to store the words
  wordlist = []
  
  # Initialise a list to store commonly used symbols
  symbols = ["!", "?", "*", "#", "$"]

  # Loop through the parts and add them to the wordlist
  for part in name_parts:
    wordlist.append(part)
  for part in nick_parts:
    wordlist.append(part)
  for part in dob_parts:
    wordlist.append(part)
  for part in petNames_parts:
    wordlist.append(part)
  for part in hobbies_parts:
    wordlist.append(part)

  # Loop through the name parts and the date of birth parts and combine them in different ways
  for i in range(len(name_parts)):
    # Add the name part followed by the date of birth part, db, yob and yob_full
    wordlist.append(name_parts[i] + yob)
    wordlist.append(name_parts[i] + yob_full)
    wordlist.append(name_parts[i] + db)

  # Loop through the Nickname parts and the date of birth parts and combine them in different ways
  for i in range(len(nick_parts)):
    # Add the name part followed by the date of birth part, db, yob and yob_full
    wordlist.append(nick_parts[i] + yob)
    wordlist.append(nick_parts[i] + yob_full)
    wordlist.append(nick_parts[i] + db)

  # Loop through pet name parts and put the dob at the end
  for l in range(len(petNames_parts)):
    wordlist.append(petNames_parts[l] + yob)
    wordlist.append(petNames_parts[l] + yob_full)
    wordlist.append(petNames_parts[l] + db)

  # Loop through hobbies parts and put the dob at the end
  for q in range(len(hobbies_parts)):
    wordlist.append(hobbies_parts[q] + yob)
    wordlist.append(hobbies_parts[q] + yob_full)
    wordlist.append(hobbies_parts[q] + db)

  # Loop through the name parts and the date of birth parts and combine them in different ways
  for i in range(len(name_parts)):
    # Add the name part followed by the date of birth part, db, yob and yob_full
    wordlist.append(yob + name_parts[i])
    wordlist.append(yob_full + name_parts[i])
    wordlist.append(db + name_parts[i])

  # Loop through the Nickname parts and the date of birth parts and combine them in different ways
  for i in range(len(nick_parts)):
    # Add the name part followed by the date of birth part, db, yob and yob_full
    wordlist.append(yob + nick_parts[i])
    wordlist.append(yob_full + nick_parts[i])
    wordlist.append(db + nick_parts[i])

  # Loop through pet name parts and put the dob at the end
  for l in range(len(petNames_parts)):
    wordlist.append(yob + petNames_parts[l])
    wordlist.append(yob_full + petNames_parts[l])
    wordlist.append(db + petNames_parts[l])

  # Loop through pet name parts and put the dob at the end
  for e in range(len(hobbies_parts)):
    wordlist.append(yob + hobbies_parts[e])
    wordlist.append(yob_full + hobbies_parts[e])
    wordlist.append(db + hobbies_parts[e])

  # Loop through each item of wordlist and add common symbols to end 
  # Probably needs to be the last thing to run before changin case and swapping numbers
  for k in range(len(wordlist)):
    for h in range(len(symbols)):
      wordlist.append(wordlist[k] + symbols[h])

  # Call caps combinations function to loop through all combinations of capital letters
  combinations = all_caps_combinations(wordlist)
  wordlist.extend(combinations)

  # Deduplicate (can be improved)
  deduplicated_list = [] 
  for word in wordlist: 
    if word not in deduplicated_list: 
      deduplicated_list.append(word)


# IDEAS:
# - Peplace some characters with numbers ie o to 0 etc

  # Return the wordlist
  return deduplicated_list

def all_caps_combinations(wordlist):
    all_combinations = []
    for word in wordlist:
        # Get all combinations of capital letters for the wordlist
        combinations = [''.join(c) for c in itertools.product(*((char.lower(), char.upper()) for char in word))]
        all_combinations.extend(combinations)
        # Remove duplicates by converting to a set and then back to a list 
       # all_combinations = list(set(all_combinations))
    return all_combinations


# Ask the user what type of target is in sight
type = input("\nTarget type:\n\n[o] Organisation  [p] Person\n\n")
##########################
# Organisation Questions #
##########################
if type == "o":
  print("\n\nEnter the following information to generate your wordlist:\n")
  name = input("Enter the name of the organisation, with any variations seprated by spaces (e.g Doodoo Dyncmics Doodoo Dymamics Ltd): ") # Maybe change this to be comma seperated
  dob = input("Enter any memorable dates seperated by spaces (e.g Date founded dd/mm/yyyy): ")
  file_name = input("Name your wordlist: ")
  wordlist = create_org_wordlist(name, dob)
  # Open the file in write mode and write each item on a new line
  with open(file_name, 'w') as file:
    for item in wordlist:
      file.write(f"{item}\n")
  print(f"Contents of the list have been written to {file_name}")

  exit
######################
# Personal Questions #
######################
elif type == "p":
  print("Enter the following information to generate your wordlist:\n")
  name = input("Enter the persons name (e.g John Smith): ")
  nick = input("Enter the persons nicknames seperated by spaces: ")
  dob = input("Enter the persons date of birth (dd/mm/yyyy): ")
  hobbies = input ("Enter any hobbies/characters/celebs that they like, seperated by spaces: ")
  petNames = input("Enter their pets name seperated by spaces: ")
  file_name = input("Name your wordlist (with .txt as the ext): ")
  deduplicated_list = create_person_wordlist(name, dob, petNames, nick, hobbies)
  # Open the file in write mode and write each item on a new line
  with open(file_name, 'w') as file:
    for item in deduplicated_list:
      file.write(f"{item}\n")
  print(f"Contents of the list have been written to {file_name}")
  exit
else:
  print("I gave you two options, chose one of them next time")
  exit
