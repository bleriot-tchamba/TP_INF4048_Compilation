class Rule():
	"""docstring for Rule"""
	
	def __init__(self, leftPart,rightPart):
		
		self.leftPart = leftPart
		self.rightPart = rightPart
	

	def __repr__(self):
	

		s = f"{self.leftPart}--------->"
		for i in range(len(self.rightPart)):
			s = s + f"{self.rightPart[i]}"
		return s
		
	def equal(self, other):
		res = True
		if len(self.rightPart) != len(other.rightPart):
			return False
		else:
			for i in range(len(self.rightPart)):
				if self.rightPart[i] != other.rightPart[i]:
					res = False
		return (self.leftPart == other.leftPart) and res

	def content(self,liste):
		res = False
		for rule in liste:
			if self.equal(rule):
				res = True
		return res

	def is_unitary(self,grammar):
		return len(self.rightPart) == 1 and self.rightPart[0] in grammar.Vn

class Grammar():
	"""docstring for Etat"""
	def __init__(self, Vt, Vn, axiome, productions):

		self.Vt = Vt
		self.Vn = Vn
		self.axiome = axiome
		self.productions = productions
	

	def printGrammar(self):
		print("L'axiome est :", self.axiome)
		print(" ")
		print("Les symboles terminaux sont :", end = " ")
		for i in self.Vt:
			print(i, end = " , ")
		print(" ")
		print(" ")
		
		print("Les symboles non terminaux sont :", end = " ")
		for i in self.Vn:
			print(i, end = " , ")
		print(" ")
		print(" ")
		
		print("Les règles de production sont : \n")
		for i in self.productions:
			#print(i, end = " , ")
			print(i,)

		print(" ")
		print(" ")

	def unnecessaryVar(self):
		P_final= [] 
		P = []
		utils = []
		verif = []

		#Step 1.1
		for i in self.productions:
			
			if type1(i, self.Vt):
				P.append(i)
				utils.append(i.leftPart)

		#Step 1.2
		for i in self.productions:
			if i not in P and type2(i, self.Vt, utils):
				P.append(i)
				utils.append(i.leftPart)
		
		#Step 1.2 again
		for i in self.productions:
			if i not in P and type2(i, self.Vt, utils):
				P.append(i)
				utils.append(i.leftPart)

		
		for i in P:
			verif.extend(i.rightPart)
		verif.append(self.axiome)
		
		#Step 2.2
		for i in P:
			if i.leftPart in verif:
				P_final.append(i)

		#Construct Vt
		Vt = []
		Vn = [self.axiome]
		for i in P_final:
			for j in i.rightPart:
				if j in self.Vt:
					Vt.append(j)
				if j in self.Vn:
					Vn.append(j)

		G_Modified = Grammar(Vt, Vn, self.axiome, P_final)
		return G_Modified

	def epsilonProd(self):
		final_rules = []
		#take variables who product directly epsilon
		annul_G = []
		for i in self.productions:
			if len(i.rightPart) == 1 and i.rightPart[0] == "epsi":
				annul_G.append(i.leftPart)

		#take variables which product indirectly epsilon
		for k in range(2):
			for i in self.productions:
				if annulVar(i, annul_G) and i.leftPart not in annul_G:
					annul_G.append(i.leftPart)
			
		#generated all the rules after modifications of all annul variables in productions
		for rule in self.productions:
			rules_generated = generateRule(rule,annul_G, len(rule.rightPart))

			#To select only rules which not be in a list of final rules
			for r in rules_generated:
				if not r.content(final_rules) and not true_Unnecessary_rule(r) and not epsi_Rule(r):
					final_rules.append(r)

		#To verify if axiome is annulable and then return the new grammar
		if self.axiome in annul_G:
			R1 = Rule('NEW_AXIOME', ['epsi'])
			R2 = Rule('NEW_AXIOME', [self.axiome])
			final_rules.append(R1)
			final_rules.append(R2)
			new_Vn = list(self.Vn)
			new_Vn.append('NEW_AXIOME')
			return Grammar(self.Vt, new_Vn, 'NEW_AXIOME', final_rules)

		#To return the new grammar in a case we don't have a new axiome (axiome is not annulable) 
		new_Vt = list(self.Vt)
		new_Vt = del_epsi(new_Vt)
		return Grammar(new_Vt, self.Vn, self.axiome, final_rules)

	def unitsProductions(self):
		#We stock all unitary rules in list L_units_rule
		L_units_rule = []
		for rule in self.productions:
			if rule.is_unitary(self):
				L_units_rule.append(rule)
		print(L_units_rule)
		print()

		#We transform all units rules and stock them in a list finals_rules
		finals_rules = []
		for rule in L_units_rule:
			unit_symbol = rule.rightPart[0]
			for rule2 in self.productions:
				if rule2.leftPart == unit_symbol:
					copie = list(rule2.rightPart)
					R = Rule(rule.leftPart, copie)
					if not R.content(finals_rules):
						finals_rules.append(R) 

		#We complete the list of finals_rules
		for rule in self.productions:
			if not rule.content(finals_rules) and not rule.is_unitary(self):
				finals_rules.append(rule)
		return Grammar(self.Vt, self.Vn, self.axiome, finals_rules)


		

	


def type1(regle, Vt):
	dec = True
	for i in regle.rightPart:
		if i not in Vt:
			dec = False
	return dec
	
def type2(regle, Vt, utils):
	dec = True
	for i in regle.rightPart:
		if i not in Vt and i not in utils:
			dec = False
	return dec

def annulVar(regle, annulVar):
	dec = True
	for i in regle.rightPart:
		if i not in annulVar:
			dec = False
	return dec

#Fonction which take a rule and a variable and return a list of all rules obtains after permut the variable in a rule
def generateRule(rule,annul_G, nbr): #nbr is the number of variables in the right part of the rule
	rules = [rule]
	
	#Construct a list of differents permutaions
	permutations = []
	for i in range(2**nbr -1):
		p = bin(i,nbr)
		permutations.append(p)
		
	for j in range(len(permutations)): #For every permutation
		copie = []
		#course of all variables of the right part of the rule
		for i in range(len(rule.rightPart)):
			if (rule.rightPart[i] in annul_G and permutations[j][i] == '1') :

				copie.append(rule.rightPart[i])
			
			elif rule.rightPart[i] not in annul_G :
				copie.append(rule.rightPart[i])
				
		#construct of new rule
		leftPart = rule.leftPart
		R = Rule(leftPart, copie)
		if len(copie) != 0 :
			rules.append(R)
	return rules


#Fonction which return a number occurence of a variable in a right part of a rule
def nb_occur(rule, var):
	nb = 0
	for i in rule.rightPart:
		nb = nb+1 if i== var else nb+0
	return nb

#to convert a number n in binary with k bits 
def bin(n,k) :
	res = []

	i = 1 << k-1
	while(i > 0) :
		if((n & i) != 0) :
			res.append('1')
		else :
			res.append('0')
		i = i // 2

	s = ""
	s = s.join(res) 
	return s

#Fonction which verify if a rule can subit a modification (in case of variable annul)
def canBeModified(rule, var):
	l = rule.rightPart
	result = l.count(l[0]) == len(l)
	if result and l[0] == var:
		return not result
	else:
		return True

#Fonction which verify if a rule is in form   S----->S
def true_Unnecessary_rule(rule):
	return (len(rule.rightPart) == 1) and (rule.rightPart[0] == rule.leftPart)

#Fonction which verify if a rule is in form   S----->epsi
def epsi_Rule(rule):
	return (len(rule.rightPart) == 1) and (rule.rightPart[0] == 'epsi')

#Fonction which delete epsilon_variable in a list of terminal symbols
def del_epsi(Vt):
	new_Vt = []
	for terminal in Vt:
		if terminal != 'epsi':
			new_Vt.append(terminal)
	return new_Vt










