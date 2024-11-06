#!/usr/bin/python3
import itertools

def create_org_wordlist(name, dob):
  # Split the name and the date of birth by spaces
  name_parts = name.split()
  dob_parts = dob.split()
  # Take year out of dob
  yob = dob[-2:]
  yob_full = dob[-4:]
  db = dob[:2]

  # Initialize an empty set to store the words
  wordlist = set()

  # Initialise a list to store commonly used symbols
  symbols = ["!", "?", "*", "#", "$"]

  # Combine inputs in different ways
  for part in name_parts: 
    wordlist.update([part, part + yob, part + yob_full, part + db]) 
    wordlist.update([dob_part + part for dob_part in dob_parts])

  return list(wordlist)

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

  # Initialize an empty set to store the words
  wordlist = set()

  for part in name_parts + nick_parts + petNames_parts + hobbies_parts: 
    wordlist.update([part, part + yob, part + yob_full, part + db]) 
    wordlist.update([yob + part, yob_full + part, db + part])
  
  # Initialise a list to store commonly used symbols
  symbols = ["!", "?", "*", "#", "$"]
  wordlist.update([word + symbol for word in wordlist for symbol in symbols])

  # Iterate through each combination of capitalisations
  wordlist.update([''.join(c) for word in wordlist for c in itertools.product(*((char.lower(), char.upper()) for char in word))])

  return list(wordlist)

# Ask the user questions
type = input("\nTarget type:\n\n[o] Organisation  [p] Person\n\n")
if type == "o":
  print("\n\nEnter the following information to generate your wordlist:\n")
  name = input("Enter the name of the organisation, with any variations seprated by spaces (e.g Doodoo Dyncmics Doodoo Dymamics Ltd): ") # Maybe change this to be comma seperated
  dob = input("Enter any memorable dates seperated by spaces (e.g Date founded dd/mm/yyyy): ")
  file_name = input("Name your wordlist: ")
  wordlist = create_org_wordlist(name, dob)
elif type == "p":
  print("Enter the following information to generate your wordlist:\n")
  name = input("Enter the persons name (e.g John Smith): ")
  nick = input("Enter the persons nicknames seperated by spaces: ")
  dob = input("Enter the persons date of birth (dd/mm/yyyy): ")
  hobbies = input ("Enter any hobbies/characters/celebs that they like, seperated by spaces: ")
  petNames = input("Enter their pets name seperated by spaces: ")
  file_name = input("Name your wordlist (with .txt as the ext): ")
  wordlist = create_person_wordlist(name, dob, petNames, nick, hobbies)
else:
  print("I gave you two options, chose one of them next time")
  exit
# Open the file in write mode and write each item on a new line 
with open(file_name, 'w') as file: 
  for item in wordlist: 
    file.write(f"{item}\n")

print(f"Contents of the list have been written to {file_name}")