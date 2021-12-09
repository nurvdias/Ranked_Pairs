# -*- coding: utf-8 -*-
"""
Created on Tue Dec 7 17:09:00 2021

@author: Dias_Nurymzhan
"""
import os
import sys
import itertools
import networkx as nx
import matplotlib.pyplot as plt
from flask import Flask, render_template

app = Flask(__name__)

"""
Getting the data from file.
P.S: In IPYNB version it's possible to pass the values from user prompt.
3     --candidates count
a b c --list of candidates
2     --voters count
a c b --voters rank
a b c --voters rank
"""
def get_data_from_file(file):

    filename = open(file, 'r', encoding='utf-8')
    lines = filename.readlines()
    
    candidates_count = int(lines[0].split()[0])
    candidates = lines[1].split()
    voters_count = int(lines[2].split()[0])
    ranks = list()
    for i in range (3, 3 + voters_count):
        ranks.append(lines[i].split())

    filename.close()
    return candidates_count, candidates, voters_count, ranks

"""
This function adds all pairs of candidates, where one candidate is preferred over the other.
"""
def add_pairs(ranks):
    pairs = dict()
    for rank in ranks:
        for pair in list(itertools.permutations(rank, 2)):
            if pair not in pairs:
                pairs[pair] = 0
            if rank.index(pair[0]) < rank.index(pair[1]):
                pairs[pair] += 1
    return pairs
"""
Function for representing preference one candidate over the other.
"""
def record_prefernces(candidates, pairs):
    preferences = dict()
    #get all combinations with 2 over all of the candidates
    for match in list(itertools.combinations(candidates, 2)):
        reverse = tuple(reversed(match))
        if pairs[match] > pairs[reverse]:
            preferences[match] = match[0]
        else:
            preferences[match] = match[1]
    return preferences

"""
Find winner.
"""
@app.route('/winner')
def find_winner():
    file = './app/test.txt'
    candidates_count, candidates, voters_count, ranks = get_data_from_file(file)   
    pairs = add_pairs(ranks)
    preferences = record_prefernces(candidates, pairs)

    """
              |  1st pref | 2nd pref | 3rd pref
    1st voter |     a          c          b
    2nd voter |     a          b          c
    ______________________________________________

       |  a  |  b  |  c
    a  |  -     2     2
    b  |  0     -     1
    c  |  0     1     -
    """
    for candidate in candidates:
        candidate_score = 0
        for preference in preferences:
            if candidate in preference and preferences[preference] == candidate:
                candidate_score += 1
        if candidate_score == len(candidates) - 1:
            return f"Winner is {candidate}"

"""
Build visual representation.
"""
@app.route('/graph')
def build_graph():
    file = './app/test.txt'
    candidates_count, candidates, voters_count, ranks = get_data_from_file(file)   
    pairs = add_pairs(ranks)
    preferences = record_prefernces(candidates, pairs)

    graph = set()
    for i in range(len(preferences)):
        node = list(preferences.values())[i]
        if list(preferences.keys())[i][0] != node:
            graph.add(list(preferences.keys())[i][::-1])
        else:
            graph.add(list(preferences.keys())[i])
    
    G = nx.DiGraph()
    G.add_edges_from(list(graph))

    nx.draw(G, with_labels = True)
    
    plt.savefig('./app/static/images/new_plot.png')
    plt.close()

    return render_template('template.html', name = 'Graph representation', url ='static/images/new_plot.png')

@app.route('/')
def hello_world():
    hello = "Hello, that's the election calculation using Ranked-Pairs (also known as Condorcet method)."
    text1 = "To see the winner on election, go to "
    text2 = "To see the graph representation, go to "
    return render_template('about.html', hello = hello,
                                         text1 = text1,
                                         text2 = text2)

def main():
    #file = sys.argv[1]
    app.run(port=8000, host='0.0.0.0')

if __name__ == '__main__':
    main()



    
