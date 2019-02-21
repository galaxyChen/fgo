# -*- coding: utf-8 -*-

from tqdm import tqdm
import numpy as np

cards = ['b','b','B','B','b','b','b']
while len(cards)<15:
    cards.append('n')
cards = np.array(cards)
success = 0
count = 500000
for i in tqdm(range(count)):
    order = np.random.permutation(15)
    card = cards[order][0:5]
    if sum(card!='n')>=3 and 'B' in card:
        success+=1
        continue
    card = cards[order][5:10]
    if sum(card!='n')>=3 and 'B' in card:
        success+=1
        continue
    card = cards[order][10:15]
    if sum(card!='n')>=3 and 'B' in card:
        success+=1
        continue
print("success rate:%f"%(success/count))