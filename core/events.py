events = {}

def registerEvent(name,func,priority=5):
	"""Registers an event handler"""
	global events

	# Max priority of 5
	if priority > 5: 
		priority = 5

	if priority < 0:
		priority = 0

	# No such event, add it
	if name not in events:
		events[name] = {}

	# No such priority, add it
	if priority not in events[name]:
		events[name][priority] = []

	# Append and return the reference function
	events[name][priority].append(func)
	return {'name':name,'func':func,'priority':priority}

def unregisterEvent(name,func):
	"""Unregisters a registered event handler"""
	global events

	# Does the event name exist?
	if name not in events:
		# Failed to unregister
		return False 

	if func != None:

		for priority in events[name]:
			i=0

			for f in events[name][priority]:

				if f == func:
					events[name][priority].pop(i)
					del i

					# Unregistered event
					return True

				i += 1

	# Welp, event not found. sucks.
	return False

def force_unregisterEvent(funct):
	"""Unregisters an event handler without knowing where it came from (slower)"""
	global events

	for name in events:
		for priority in events[name]:
			if funct in events[name][priority]:
				events[name][priority].remove(funct)


def callEvent(name,*args):
	"""Calls an event"""
	if name not in events:
		return True

	x = None

	# Loop through event names
	for priority in events[name].keys():

		# Leep through event's priorities
		for func in events[name][priority]:

			# Try to run the function.
			try:
				if x == None:
					x = args
				x = func(*x)
			except Exception,e:
				print("An exception occurred!")
				print(e)

				# To prevent bad things from happening,
				## stop the event from continuing
				return False

			# If it's not True or None, stop the event.
			if x == False:
				return False

	# Event was good, congrats!
	return True


