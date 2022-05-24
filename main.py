from classe import *
from fonctions import *

'''R1 = rule("S", ['A', 'B'])
R2 = Rule("S", ['C', 'A'])
R3 = Rule("B", ['A', 'B'])
R4 = Rule("B", ['E', 'A'])
R5 = Rule("C", ['a', 'B'])
R6 = Rule("C", ['b'], [1])
R7 = Rule("E", ['B', 'A'])
R8 = Rule("A", ['a'])
R9 = Rule("D", ['a', 'C'])
G = Grammar(['a','b'], ['A','B','C','D','E','S'], 'S', [R1,R2,R3,R4,R5,R6,R7,R8,R9])

R10 = Rule("B", ['a'])
R11 = Rule('S', ['A','B','a'])
R12 = Rule('A', ['B', 'b'])
G2 = Grammar(['a','b'], ['A','B','S'], 'S', [R10,R11,R12])'''

R13 = Rule("B", ['epsi'])
R14 = Rule("A", ['B'])
R15 = Rule('A', ['S'])
R16 = Rule('S', ['A','S','A'])
G3 = Grammar(['epsi'], ['A','B','S'], 'S', [R13,R14,R15,R16])



R17 = Rule('S', ['S','(','S',')'])
R18 = Rule('S',['epsi'])
G4 = Grammar(['epsi','(',')'],['S'],'S',[R17,R18])

R19 = Rule('S',['A','S','B','A','C','A','B'])
#R20 = Rule('S',['epsi'])
R21 = Rule('A',['epsi'])
R22 = Rule('B',['epsi'])
R23 = Rule('C',['epsi'])
G5 = Grammar(['epsi'], ['A','B','S','C'], 'S', [R19,R21,R22,R23])

R24 = Rule('S',['A'])
R25 = Rule('A',['a','B','a'])
R26 = Rule('A',['a'])
R27 = Rule('B',['b','A','b'])
R28 = Rule('B',['b'])
G6 = Grammar(['a','b'], ['A','B','S'], 'S', [R24,R25,R26,R27,R28])




G6.printGrammar()
#G_modified = G2.unnecessaryVar()

G_modified = G6.unitsProductions()
#print(len(G_modified.productions))
print()
G_modified.printGrammar()


