#!/usr/bin/python3
import itertools
import sys

# Dictionary to map letters to potential number replacements
letter_to_number = {
    'a': ['4'],
    'e': ['3'],
    'i': ['1'],
    'l': ['1'],
    'o': ['0'],
    's': ['5'],
    't': ['7'],
    'a': ['@'],
}

# Function to replace letters with similar numbers
def replace_with_numbers(word):
    if not word:
        return []
    
    replacements = ['']
    for char in word:
        if char.lower() in letter_to_number:
            new_replacements = []
            for replacement in replacements:
                new_replacements.append(replacement + char)
                for number in letter_to_number[char.lower()]:
                    new_replacements.append(replacement + number)
            replacements = new_replacements
        else:
            replacements = [replacement + char for replacement in replacements]

    return replacements

def print_overwrite(word): 
  sys.stdout.write(f'\r{" " * 20}\r{word}') 
  sys.stdout.flush()

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

  # Combine inputs in different ways
  print("\nCombining inputs...")
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

  #combine parts together
  #for part in name_parts:
  #  wordlist.update([part + nick_parts, part + petNames_parts, part + hobbies_parts])
 # for part in nick_parts:
#    wordlist.update([part + hobbies_parts, part + petNames_parts, + part + name_parts])

  # Combine inputs in different ways
 # deliminators = ["-", "."]
  for part in name_parts + nick_parts + petNames_parts + hobbies_parts: 
    wordlist.update([part, part + yob, part + yob_full, part + db]) 
    wordlist.update([yob + part, yob_full + part, db + part])

  # Combine the inputs with deliminators inbetween
  #  for deliminator in deliminators:
 #     wordlist.update([part + deliminator + yob, part + deliminator + yob_full, part + deliminator + db])
#      wordlist.update([yob + deliminator + part, yob_full + deliminator + part, db + deliminator + part])

  # Initialise a list to store commonly used symbols
  symbols = ["!", "?", "*", "#", "$", "123", "1234", "12345"]
  wordlist.update([word + symbol for word in wordlist for symbol in symbols])

  # Call number replacment function
  final_wordlist = set(wordlist)
  for word in wordlist:
    final_wordlist.update(replace_with_numbers(word))

  # Iterate through each combination of capitalisations
  capital_combinations = [''.join(c) for word in final_wordlist for c in itertools.product(*((char.lower(), char.upper()) for char in word))] 
  final_wordlist.update(capital_combinations)

  return list(final_wordlist)

# Ask the user questions
print("\nWelcome to Matt's Crack, a custom wordlist generator, choose the type of target:")
type = input("\nTarget type:\n\n[o] Organisation  [p] Person\n\n")
if type == "o":
  print("\nEnter the following information to generate your wordlist:\n")
  name = input("Enter the name of the organisation, with any variations seprated by spaces (e.g Doodoo Dyncmics Doodoo Dymamics Ltd): ") # Maybe change this to be comma seperated
  dob = input("Enter any memorable dates seperated by spaces (e.g Date founded dd/mm/yyyy): ")
  file_name = input("Name your wordlist: ")
  wordlist = create_org_wordlist(name, dob)
elif type == "p":
  print("\nEnter the following information to generate your wordlist:\n")
  name = input("Enter the persons name (e.g John Smith): ")
  nick = input("Enter the persons nicknames seperated by spaces: ")
  dob = input("Enter the persons date of birth (dd/mm/yyyy): ")
  hobbies = input ("Enter any hobbies/characters/celebs that they like, seperated by spaces: ")
  petNames = input("Enter their pets name seperated by spaces: ")
  file_name = input("Name your wordlist (with .txt as the ext): ")
  print("Genrating Wordlist:\n")
  wordlist = create_person_wordlist(name, dob, petNames, nick, hobbies)
else:
  print("I gave you two options, chose one of them next time")
  exit
# Open the file in write mode and write each item on a new line 
with open(file_name, 'w') as file: 
  for item in wordlist: 
    file.write(f"{item}\n")
# Open file in read mode and count amount of words in file
with open(file_name, 'r') as file:
  line_count = sum(1 for line in file)

print(f"\r{line_count} words have been written to {file_name}")
