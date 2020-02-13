#!/usr/bin/env python3

import re

def dyn_named_reg_maker(*alts):
    """
    Dynamic named alternation Regex Maker
    For quickly visualizing how a range of values tested against a 
    Regex, which is made up of several alternations, behaves
    *alts -- dynamic number of Regex alternations passed to the function
    """
    # this gets filled out with the full named captures Regex
    full_reg = rf""
    # this gets filled out with the same Regex, but un-named captures
    full_plain_reg = rf""
    # mapping of labels like "label0", "label1" etc to Regexes
    # between each alternation, ie between each ("|"), 
    reg_to_label_map = {}
    for i, v in enumerate(alts):
        # { "label0" : "someregex passed to *alts"} ..
        reg_to_label_map[f"label{i}"] = v
    for k, v in reg_to_label_map.items():
        # (P<label0>someregex) ...
        full_reg += rf"(?P<{k}>{v})"
        full_plain_reg += rf"({v})"
    # add the alternation metacharacter between )( 
    # ie, after the end of one capture group, and before the next
    full_reg = re.sub(r"\)\(", r")|(", full_reg) 
    full_plain_reg = re.sub(r"\)\(", r")|(", full_plain_reg) 

    return [full_reg, reg_to_label_map, full_plain_reg]

# first alternation to pass to dyn_named_reg_maker()
first_alt = r"2[0-4]\d"

# second alternation to pass to dyn_named_reg_maker()
second_alt = r"25[0-5]"

# create the regex
reg = dyn_named_reg_maker(first_alt, second_alt)

# compiled regex
creg = re.compile(reg[0])

# iterable collection to test against the above compiled regex
iterable_to_test = range(220,256)

for i in iterable_to_test:
    match = creg.match(str(i))
    if match:
        # loop through the reg_to_label_map created in dyn_named_reg_maker()
        # which associates each key with one part of the Regex alternation
        for k, v in reg[1].items():
            # if the "label0" type key in the reg_to_label_map is in 
            # the match object (and we know it is, since this is all
            # under "if match:"), print the associated value, which 
            # is the part of the Regex alternation that matched
            if match[k]:
                # print what was checked against the Regex, and the value 
                # from that key; ie, print the Regex alternation that matched
                print(f"{i} matches {reg[1][k]}")
    else:
        print(f"{i} does NOT match")
       
print()
print("Regex tested against:")
print(f"non-named captures: {reg[2]}")
print(f"named captures: {reg[0]}")
