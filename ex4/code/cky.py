"""
To use this function, you need to provide a PCFG in CNF as a dictionary. The keys of the dictionary are the non-terminal symbols of the grammar, and the values are dictionaries that contain the following fields:

'prob': The probability of the non-terminal symbol.
'rules': A list of tuples of the form (B, C, p), where B and C are the symbols on the right hand side of the rule and p is the probability of the rule.
"""

from collections import defaultdict

def cky(grammar, sentence):
    # Tokenize the sentence
    words = sentence.split()

    # Initialize the probability and backpointer tables
    n = len(words)
    prob = [[0 for i in range(n)] for j in range(n)]
    back = [[None for i in range(n)] for j in range(n)]

    # Iterate over the lengths of the substrings
    for l in range(1, n+1):
        # Iterate over the start indices of the substrings
        for i in range(n-l+1):
            # Initialize the substring
            s = words[i:i+l]

            # Check if the substring is a terminal symbol
            if s[0] in grammar:
                prob[i][i+l-1] = grammar[s[0]]['prob']
                back[i][i+l-1] = s[0]

            # Otherwise, try to expand the substring using non-terminal symbols
            else:
                # Iterate over the non-terminal symbols in the grammar
                for A in grammar:
                    # Iterate over the rules of the form A -> BC
                    for (B, C, p) in grammar[A]['rules']:
                        if B in grammar and C in grammar:
                            # Iterate over the split points
                            for j in range(i, i+l-1):
                                # Check if the substrings B and C can be expanded
                                if prob[i][j] and prob[j+1][i+l-1]:
                                    # Update the probability and backpointer tables
                                    prob[i][i+l-1] += prob[i][j] * prob[j+1][i+l-1] * p
                                    back[i][i+l-1] = (A, j)
                        elif B in grammar:
                            # Iterate over the split points
                            for j in range(i, i+l-1):
                                # Check if the substring B can be expanded
                                if prob[i][j]:
                                    # Update the probability and backpointer tables
                                    if s[j-i+1:] == C:
                                        prob[i][i+l-1] += prob[i][j] * p
                                        back[i][i+l-1] = (A, j)

    # Return the probability and backpointer tables
    return prob, back


