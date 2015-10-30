#ActivityChoiceOptimization
#TODO: Find format of new activity & information it contains
#TODO: Find out how long to explore early on
#TODO: Find out difference between global and local variables in python

import random

# activity_list=[]
# exploit_probability = .95 #Probability of exploiting current information. Must be less than 1
# exploit = True # True if exploiting preferences, and false if exploring

def add_new_activity(new_activity, activity_list):
	#Note each activity is a list of information pertaining to the activity
	return activity_list.append(new_activity)

def activity_completed(activity):
	#update parameters of an activity
	#Possble parameters:
		#time of day completed, day completed, time taken/calories burned
	return activity_list 

def activity_passed_over(activity):
	#change probability of choosing activity
	#potentially note time, day, times in a row, ect. activity has been passed over
	return activity

def push_suggestion(activity):
	#based on time of day & preferences consider asking user to do an activity at a time
	return activity

def exploit_or_explore():
	if random.random() < exploit_probability:
		exploit = True
	else:
		exploit = False
	return exploit 

#Note this function and the one below may be redundant
def organize_activity_list(activity_list):
	#Update how activities are ordered based on some parameter
	#Consider a mix of:
		#Likelihood to do activity
		#Calories that can be burned doing activity
		#Calories user needs to burn
	return activity_list

def order_preferences(activity_list):
	exploit_or_explore()
	if exploit:
		#Potentially just leave this the same if preferences ordered after every activity
		return organize_activity_list(activity_list)
	else:
		#Determine strategy to explore new activities
		return activity_list

def process_completed_activity(activity, activity_list):
	#Find position of activity in list
	current=0
	#Note activites passed over
	if len(activity_list) != 0:
		while(activity_list[current]!=activity):
			# activity_passed_over(activity)
			current+=1
			#Check if activity is a new activity
			if current==len(activity_list):
				add_new_activity(activity, activity_list)
		#Process completed activity
		# activity_completed(activity)
	else:
	    add_new_activity(activity, activity_list)	
	#Appropriately order activity list
	return order_preferences(activity_list)


if __name__ == '__main__':
	activities_list=[["cat"]]
	exploit_probability = .95 #Probability of exploiting current information. Must be less than 1
	exploit = True # True if exploiting preferences, and false if exploring

	print process_completed_activity(["blah"], activities_list)