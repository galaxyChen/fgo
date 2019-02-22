# -*- coding: utf-8 -*-

from tqdm import tqdm
import numpy as np

cards = ['b','B','B','B','b','b','b','b']
while len(cards)<15:
    cards.append('n')
cards = np.array(cards)
success = 0
turn1 = 0
turn2 = 0
count = 500000

for i in tqdm(range(count)):
    order = np.random.permutation(15)
    card = cards[order][0:5]
    if 'b' in card and 'B' in card:
        turn1+=1
        success+=1
        continue
    card = cards[order][5:10]
    if 'b' in card and 'B' in card:
        turn2+=1
        success+=1
        continue
    
print("success rate:%f"%(success/count))
print("turn1 rate:%f"%(turn1/count))
print("turn2 rate:%f"%(turn2/count))