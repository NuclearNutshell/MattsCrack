#!/usr/bin/env python3
import itertools
import argparse
import sys

# map letters to look-alike digits/symbols
LETTER_TO_NUMBER = {
    'a': ['4', '@'],
    'e': ['3'],
    'i': ['1'],
    'l': ['1'],
    'o': ['0'],
    's': ['5'],
    't': ['7'],
}

# common symbol suffixes
SYMBOLS = ["!", "*", "123", "1234", "12345", "123!", "1234!", "12345!"]

def replace_with_numbers(word: str) -> set:
    """
    Given a base word, return a set containing the original plus all
    single-character substitutions from LETTER_TO_NUMBER.
    """
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

def build_base_tokens(name, dob, pet_names, nicknames, hobbies) -> list:
    """
    Combine name/nick/pet/hobby tokens with date fragments and pairwise
    concatenations to produce a small, unique list of 'base' tokens.
    """
    nm = set(name.split())
    nk = set(nicknames.split())
    pt = set(pet_names.split())
    hb = set(hobbies.split())

    yob2 = dob[-2:]   # last 2 digits of year
    yob4 = dob[-4:]   # full year
    d2   = dob[:2]    # day or month

    base = set()

    # Stage 1: single tokens + date variants
    for part in nm | nk | pt | hb:
        variants = {
            part,
            part + yob2,
            part + yob4,
            part + d2,
            yob2 + part,
            yob4 + part,
            d2   + part,
        }
        base |= variants

    # Stage 2: pairwise concatenations between each category
    groups = [nm, nk, pt, hb]
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            for x in groups[i]:
                for y in groups[j]:
                    if x != y:
                        base.add(x + y)
                        base.add(y + x)

    return list(base)

def generate_wordlist(name, dob, pet_names, nicknames, hobbies):
    """
    Yield every password candidate:
      1) base token
      2) number-replaced variants
      3) all-case permutations
      4) symbol suffixes
    """
    base_tokens = build_base_tokens(name, dob, pet_names, nicknames, hobbies)

    for token in base_tokens:
        for num_var in replace_with_numbers(token):
            # build case-pools: letters branch, others stay singleton
            pools = [
                (c.lower(), c.upper()) if c.isalpha() else (c,)
                for c in num_var
            ]
            for caps in itertools.product(*pools):
                word = ''.join(caps)
                # bare word
                yield word
                # with each symbol suffix
                for sym in SYMBOLS:
                    yield word + sym

def main():
    p = argparse.ArgumentParser(
        description="Generate a custom wordlist to stdout"
    )
    p.add_argument("name",       help="Full name or organisation")
    p.add_argument("dob",        help="Date (dd/mm/yyyy)")
    p.add_argument("nicknames",  help="Space-separated nicknames (or '' )")
    p.add_argument("hobbies",    help="Space-separated hobbies (or '' )")
    p.add_argument("pets",       help="Space-separated pet names (or '' )")
    args = p.parse_args()

    # Stream to stdout so your WP plugin can do: python3 generator.py ... > tmp.txt
    for pw in generate_wordlist(
        args.name,
        args.dob,
        args.pets,
        args.nicknames,
        args.hobbies
    ):
        sys.stdout.write(pw + "\n")

if __name__ == "__main__":
    main()
