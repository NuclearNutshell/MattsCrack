#!/usr/bin/env python3
import argparse
import itertools
import sys
import zipfile

LETTER_TO_NUMBER = {
    'a': ['4', '@'],
    'e': ['3'],
    'i': ['1'],
    'l': ['1'],
    'o': ['0'],
    's': ['5'],
    't': ['7'],
}

SYMBOLS = ["!", "*", "123", "1234", "12345", "123!", "1234!", "12345!"]


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


def build_base_tokens(name, dob, pet_names, nicknames, hobbies) -> list:
    nm = set(name.split())
    nk = set(nicknames.split())
    pt = set(pet_names.split())
    hb = set(hobbies.split())

    yob2 = dob[-2:]
    yob4 = dob[-4:]
    d2   = dob[:2]

    base = set()
    for part in nm | nk | pt | hb:
        vs = {
            part,
            part + yob2,
            part + yob4,
            part + d2,
            yob2 + part,
            yob4 + part,
            d2   + part,
        }
        base |= vs

    groups = [nm, nk, pt, hb]
    for i in range(len(groups)):
        for j in range(i+1, len(groups)):
            for x in groups[i]:
                for y in groups[j]:
                    if x != y:
                        base.add(x + y)
                        base.add(y + x)

    return list(base)


def generate_wordlist(name, dob, pet_names, nicknames, hobbies):
    for token in build_base_tokens(name, dob, pet_names, nicknames, hobbies):
        for num_var in replace_with_numbers(token):
            pools = [
                (c.lower(), c.upper()) if c.isalpha() else (c,)
                for c in num_var
            ]
            for caps in itertools.product(*pools):
                word = ''.join(caps)
                yield word
                for sym in SYMBOLS:
                    yield word + sym


def main():
    p = argparse.ArgumentParser(
        description="Generate a custom wordlist, optionally zipped."
    )
    p.add_argument("name", help="Full name or organisation")
    p.add_argument("dob", help="Date (dd/mm/yyyy)")
    p.add_argument("nicknames", help="Space-separated nicknames, or ''")
    p.add_argument("hobbies", help="Space-separated hobbies, or ''")
    p.add_argument("pets", help="Space-separated pet names, or ''")
    p.add_argument(
        "-o", "--output",
        required=True,
        help="Output path: .txt (plain text) or .zip (compressed)"
    )
    args = p.parse_args()

    out_path = args.output
    is_zip   = out_path.lower().endswith('.zip')

    if is_zip:
        # Create a ZIP and stream into wordlist.txt inside it
        with zipfile.ZipFile(out_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            with zf.open('wordlist.txt', 'w') as writer:
                for pw in generate_wordlist(
                    args.name, args.dob, args.pets,
                    args.nicknames, args.hobbies
                ):
                    line = (pw + '\n').encode('utf-8')
                    writer.write(line)
    else:
        # Plain-text output
        with open(out_path, 'w', encoding='utf-8') as fw:
            for pw in generate_wordlist(
                args.name, args.dob, args.pets,
                args.nicknames, args.hobbies
            ):
                fw.write(pw + '\n')


if __name__ == "__main__":
    main()
