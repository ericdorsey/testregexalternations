#!/usr/bin/env python3

import re

#reg = r"(?P<first_alt>2[0-4]\d)|(?P<second_alt>25[0-5])"
#reg = r"(2[0-4]\d)|(25[0-5])"

# first part of the alternation
first_alt = r"2[0-4]\d"

# second part of the alternation
second_alt = r"25[0-5]"

first_alt_label = "first_alt"
second_alt_label = "second_alt"

def named_reg_maker(first_alt, second_alt):
    full_reg = rf"(?P<{first_alt_label}>{first_alt})|(?P<{second_alt_label}>{second_alt})"
    return full_reg

def dyn_named_reg_maker(*alts):
    """
    Dynamic Named Regex Maker
    alts: two or more Regex alternations
    """
    full_reg = rf""
    full_plain_reg = rf""
    reg_to_label_map = {}
    for i, v in enumerate(alts):
        # { "someregex": "0", "anotherregex" : "1", etc.. }
        print(i, v)
        #reg_to_label_map[v] = f"label{i}"
        reg_to_label_map[f"label{i}"] = v
    for k, v in reg_to_label_map.items():
        print(k, v)
        #full_reg += rf"(?P<{v}>{k})"
        full_reg += rf"(?P<{k}>{v})"
        full_plain_reg += rf"({v})"
    print(full_reg)
    # add the alternation metacharacter
    full_reg = re.sub(r"\)\(", r")|(", full_reg) 
    full_plain_reg = re.sub(r"\)\(", r")|(", full_plain_reg) 
    print(full_reg)
    return [full_reg, reg_to_label_map, full_plain_reg]

#reg = named_reg_maker(first_alt, second_alt)
reg = dyn_named_reg_maker(first_alt, second_alt)
print(reg)

# compiled regex
creg = re.compile(reg[0])

#[print(m) for m in range(0, 256) if creg.search(str(m))]
#[print(m) for m in range(0, 256) if creg.findall(str(m))]
#for i in range(0, 256):
#    match = creg.match(str(i))
#    if match:
#        if match[first_alt_label]:
#            print(f"{i} matches {first_alt}")
#        if match[second_alt_label]:
#            print(f"{i} matches {second_alt}")
        #print(match.groupdict())
for i in range(198, 256):
    #print(f"i is {i}")
    match = creg.match(str(i))
    if match:
        # something like .. match is <_sre.SRE_Match object; span=(0, 3), match='251'>
        for k, v in reg[1].items():
            #print(k, v)
            if match[k]:
                #print(f"plain: {reg[2]}")
                #print(f"named: {reg[0]}")
                print(f"{i} matches {reg[1][k]}")
                #print(f"{i} matches {reg[2][k]}")
       
print() 
print(f"plain: {reg[2]}")
print(f"named: {reg[0]}")
                
                
