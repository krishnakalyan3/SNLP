#!/usr/bin/env python2
import sys
import os
import re
from fsa import *

def string2Fsa(s):
    states = map(lambda x:State('q'+str(x),{s[x]:'q'+str(x+1)}),range(len(s)))
    states.append(State('q'+str(len(s))))
    initialState = State('q0')
    finalStates = [State('q'+str(len(s)))]
    return Nfa(states, currentAlphabet, initialState, finalStates)

months = ['January',
'February',
'March',
'April',
'May',
'June',
'July',
'August',
'September',
'October',
'November',
'December']

fsaMonths=map(lambda x: string2Fsa(x),months)

## test these FSA:

for i in range(len(fsaMonths)):
    print fsaMonths[i].recognize(months[i])

    