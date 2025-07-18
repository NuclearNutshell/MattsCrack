#!/usr/bin/env python3
import itertools
import sys

LETTER_TO_NUMBER = {
    'a': ['4', '@'],
    'e': ['3'],
    'i': ['1'],
    'l': ['1'],
    'o': ['0'],
    's': ['5'],
    't': ['7'],
}

SYMBOLS = ["!", "*", "123", "1234", "12345", "123!", "1234!", "12345!"] # Array of commonly used symbols.

# Replace lower case letters with their similar numbers.
def replace_with_numbers(word: str) -> set:
    reps = ['']
    for ch in word:
        next_round = []
        subs = LETTER_TO_NUMBER.get(ch.lower(), [])
        for base in reps:
            next_round.append(base + ch)
            for s in subs:
                next_round.append(base + s)
        reps = next_round
    return set(reps)

# Build a list of tokens using user input.
def build_base_tokens(name, dob, pet_names, nicknames, hobbies) -> list:
    nm = set(name.split())
    nk = set(nicknames.split())
    pt = set(pet_names.split())
    hb = set(hobbies.split())

    yob2 = dob[-2:]   # Year of birth short
    yob4 = dob[-4:]   # Year of birth full
    d2   = dob[:2]    # Day of birth

    # Combine date variants with base tokens.
    base = set()
    for part in nm | nk | pt | hb:
        vs = {
            part, part+yob2, part+yob4, part+d2,
            yob2+part, yob4+part, d2+part
        }
        base |= vs

    # Combine all tokens together.
    groups = [nm, nk, pt, hb]
    for i in range(len(groups)):
        for j in range(i+1, len(groups)):
            for x in groups[i]:
                for y in groups[j]:
                    if x != y:
                        base.add(x+y)
                        base.add(y+x)

    return list(base)

def main():
    print("\nWelcome to Matts Crack!")
    t = input("Target type: [o] Org  [p] Person]\n> ").strip().lower()
    if t == 'o':
        name     = input("Organisation names (space-separated): ").strip()
        dob      = input("Dates (dd/mm/yyyy space-separated): ").strip()
        nick = pet = hobbies = ""
    elif t == 'p':
        name     = input("Person's full name: ").strip()
        nick     = input("Nicknames (space-separated): ").strip()
        dob      = input("Date of birth (dd/mm/yyyy): ").strip()
        hobbies  = input("Hobbies/likes (space-separated): ").strip()
        pet      = input("Pet names (space-separated): ").strip()
    else:
        sys.exit("Invalid choice, exiting.")

    out_file = input("Output filename (e.g. wordlist.txt): ").strip()
    count = 0

    base_tokens = build_base_tokens(name, dob, pet, nick, hobbies)

    with open(out_file, 'w', encoding='utf-8') as fw:
        for token in base_tokens:
            for num_variant in replace_with_numbers(token):
                # build pools: letters get (lower, upper), others stay single
                pools = [
                    (c.lower(), c.upper()) if c.isalpha() else (c,)
                    for c in num_variant
                ]
                # iterate all-case permutations without duplicates
                for caps in itertools.product(*pools):
                    word = ''.join(caps)
                    fw.write(word + "\n")
                    count += 1
                    # symbol suffixes
                    for sym in SYMBOLS:
                        fw.write(word + sym + "\n")
                        count += 1

                    if count % 100_000 == 0:
                        print(f"\rWritten {count:,} words...", end='', flush=True)

    print(f"\n\nDone. {count:,} words written to {out_file}")

if __name__ == "__main__":
    main()
