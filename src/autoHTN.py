import pyhop
import json

def check_enough (state, ID, item, num):
	if getattr(state,item)[ID] >= num: return []
	return False

def produce_enough (state, ID, item, num):
	return [('produce', ID, item), ('have_enough', ID, item, num)]

pyhop.declare_methods ('have_enough', check_enough, produce_enough)

def produce (state, ID, item):
	return [('produce_{}'.format(item), ID)]

pyhop.declare_methods ('produce', produce)

def make_method (name, rule):
	def method (state, ID):
			checks = []
			for requirement, quantity in rule["Requires"].items():
				checks.append(('have_enough', ID, requirement, quantity))
			checks.append((name, ID))
			return checks
	return method

def declare_methods (data):
	# some recipes are faster than others for the same product even though they might require extra tools
	# sort the recipes so that faster recipes go first
	# your code here
	# hint: call make_method, then declare the method to pyhop using pyhop.declare_methods('foo', m1, m2, ..., mk)
	
	# keep track of {item: {recipe : time}
	# after iterate through each key and sort recipes by
	recipes_made = {}
	method_names = {}
	
	# iterate through each item recipe in "Recipes"
	for item in data["Recipes"]:
		# create function name sub " " for "_" eg: iron axe for wood -> iron_axe_for_wood
		func_name = item.replace(" ", "_")
		# declare associated operator eg: op_iron_axe_for_wood
		op_name = "op" + "_" + func_name
		# produce is assigned to the item produced
		produce = next(iter(data["Recipes"][item]["Produces"]))
		# create an entry in both dictionaries for item being produced
		if produce not in recipes_made:
			recipes_made[produce] = {}
		if produce not in method_names:
			method_name = "produce" + "_" + produce
			method_names[produce] = method_name		
		# rename function returned by make_method
		func = make_method(op_name, data["Recipes"][item])
		func.__name__ = func_name
		# add to the dictionary associated with item produced in form {item: {function : time}
		recipes_made[produce][func] = data["Recipes"][item]["Time"]

	for key, value in recipes_made.items():
		value = sorted(value.items(), key = lambda item: item[1])
		method = method_names[key]
		function_list = [method]
		for tup in value:
			func = tup[0]
			time = tup[1]
			function_list.append(func)
		print(function_list)
		pyhop.declare_methods(tuple(function_list))

def make_operator (rule):
	def operator (state, ID):
		for requirement, quantity in rule["Requires"].items():
			if getattr(state, requirement) >= quantity:
				continue
			else:
				return False
		for produce, quantity in rule["Produces"].items():
			number = getattr(state, produce) + quantity
			setattr(state, produce, {ID: number})
		for consumed, quantity in rule["Consumes"].items():
			number = getattr(state, consumed) - quantity
			setattr(state, consumed, {ID: number})
		return state
	return operator

def declare_operators (data):
	# your code here
	# hint: call make_operator, then declare the operator to pyhop using pyhop.declare_operators(o1, o2, ..., ok)
	for item in data["Recipes"]:
		func_name = item.replace(" ", "_")
		operator = (make_operator(data["Recipes"][item]))
		operator.__name__ = func_name
		pyhop.declare_operators(operator)
	

def add_heuristic (data, ID):
	# prune search branch if heuristic() returns True
	# do not change parameters to heuristic(), but can add more heuristic functions with the same parameters: 
	# e.g. def heuristic2(...); pyhop.add_check(heuristic2)
	def heuristic (state, curr_task, tasks, plan, depth, calling_stack):
		# your code here
		return False # if True, prune this branch

	pyhop.add_check(heuristic)


def set_up_state (data, ID, time=0):
	state = pyhop.State('state')
	state.time = {ID: time}

	for item in data['Items']:
		setattr(state, item, {ID: 0})

	for item in data['Tools']:
		setattr(state, item, {ID: 0})

	for item, num in data['Initial'].items():
		setattr(state, item, {ID: num})

	return state

def set_up_goals (data, ID):
	goals = []
	for item, num in data['Goal'].items():
		goals.append(('have_enough', ID, item, num))

	return goals

if __name__ == '__main__':
	rules_filename = 'crafting.json'

	with open(rules_filename) as f:
		data = json.load(f)

	state = set_up_state(data, 'agent', time=239) # allot time here
	goals = set_up_goals(data, 'agent')

	declare_operators(data)
	declare_methods(data)
	add_heuristic(data, 'agent')

	#pyhop.print_operators()
	#pyhop.print_methods()

	# Hint: verbose output can take a long time even if the solution is correct; 
	# try verbose=1 if it is taking too long
	pyhop.pyhop(state, goals, verbose=3)
	# pyhop.pyhop(state, [('have_enough', 'agent', 'cart', 1),('have_enough', 'agent', 'rail', 20)], verbose=3)
