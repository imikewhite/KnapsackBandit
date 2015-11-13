# Michael White, Matt Wolfson
#ActivityChoiceOptimization

import random
import sys
import os.path
import re
import numpy as np 


'''Note:: This program requires that the arguments passed in are as follows:
		1 argument = First time the program is being run, argument is data of activities, payoffs, locations, etc.
		2 arguments = First is data from the previous day named Newest_data.txt (as the program outputs)
					  Second argument is new data that we want to combine with our previous data. '''



def add_new_activity(activity_list, payoff, length, argument):
	#adds any new activities to the list
	with open(argument , "r") as filestream:
		for line in filestream:
			currentline = line.split(",")
			activity = [float(currentline[1]), float(currentline[2])]
			leng = currentline[6]
			p = [float(currentline[3])]
			l = [float(leng[:-1])]
			if (activity not in activity_list):
				activity_list.append(activity)
				payoff.append(p)
				length.append(l)
	#Updates running data file with newest list of activites and payoffs etc. 
	if os.path.isfile('Newest_data.txt'):
		open('Newest_data.txt', 'w').close()
	file = open('Newest_data.txt', 'w') 
	file.write("Activities: [")
	file.write(str(activity_list).strip('[]') + '] end')
	file.write("\n \nPayoffs: [")
	file.write(str(payoff).strip('[]') + '] end')
	file.write("\n \nLengths: [")
	file.write(str(length).strip('[]') + '] end')
	file.close()

def activity_completed(activity):
	#update the items 'value' with adhearence being set to true.
	return activity_list 

def activity_passed_over(activity):
	#update the items 'value' with adhearence being set to false.
	return activity

def exploit_or_explore(knapsack_list):
	# NEED TO MODIFY: Should also, in addition to random exploration,
	# explore if the 'value' falls under a certain threshold 
	# (This threshold should be the overall mean of all possible activities values) 
	if random.random() < 0.95:
		exploit = True
	else:
		exploit = False
	return exploit 


def organize_activity_list(activity_list):
	#Calls knapsack with list of activities and goal amount of energy expenditure for the day.
	knapsack_list = []
	# Check if we are exploiting or exploring 
	exploit = exploit_or_explore(knapsack_list)
	if exploit:
		#if exploiting just return the result from knapsack
		return activity_list
	else:
		# Remove the lowest 'valued' item in the resulting knapsack list from above
		# recall knapsack with:
		#     1.) a knapsack size of (origial goal expenditure (used above) - total expenditure of items inside the current knapsack) 
																							#(i.e without the dropped activity))
		#     2.) the (original list of activities used above - the current knapsack of items AND - the removed activity)
		# This will return the activity(ies) that will replace the removed activity, append them onto the original knapsack list and return
		return activity_list


# Parses yesterdays data to retrive the information stored in it.
def string_to_list(lst,string):
	if len(string) == 0:
		return lst
	else:
		first_entry = string[:string.find(',')]
		working_second = string[string.find(',')+2:]
		if working_second.find(',') == -1:
			second_entry = working_second
			lst.append([float(first_entry),float(second_entry)]) 
			return lst
		else:
			second_entry = working_second[:working_second.find(',')] 
			lst.append([float(first_entry),float(second_entry)]) 
			return string_to_list(lst, working_second[working_second.find(',')+2:])

def string_to_list_single(lst,string):
	if len(string) == 0:
		return lst
	else:
		entry = string[:string.find(',')]
		last = string[string.find(',')+2:]
		if last.find(',') == -1:
			lst.append([float(entry)])
			lst.append([float(last)]) 
			return lst
		else:
			lst.append([float(entry)])
			return string_to_list_single(lst, last)

# Working on keeping a running mean with adhearance.
# Where x is a vector of the values for an activity each day (where value is a combination of )
# and N is the number of days that have passed thus far (length of x)

def runningMean(x, N):
	return np.convolve(x, np.ones((N,))/N)[(N-1):]

def append_newest_value(days_values, current_day, adhearance):
	if adhearance:
		days_values.append(days_values[current_day-1] + (runningMean(days_values,current_day)[0]/current_day))
	else:
		days_values.append(days_values[current_day-1] - (runningMean(days_values,current_day)[0]/current_day))
	print days_values


def main():
	activity_list = []
	payoff = []
	length = []
	if len(sys.argv)==1:
		return "No Data",  "Was Given" 
	if len(sys.argv)==2:
		# create a list of activities and their payoffs_lengths
		add_new_activity(activity_list, payoff, length, sys.argv[1]) 
		return activity_list , payoff, length
	if len(sys.argv)==3:
		# First argument (after script name) is data from last day
		with open(sys.argv[1] , "r") as filestream:
			# retrieves lists of last days activity_list and payoffs, and length
			data = filestream.read()
			get_acts = re.findall(r'Activities: (.*?) end',data,re.DOTALL)
			format_acts = get_acts[0].replace('[','').replace(']','')
			activity_list = string_to_list([],format_acts)
			get_payoffs = re.findall(r'Payoffs: (.*?) end',data,re.DOTALL)
			format_payoffs = get_payoffs[0].replace('[','').replace(']','')
			payoff = string_to_list_single([],format_payoffs)
			get_lengths = re.findall(r'Lengths: (.*?) end',data,re.DOTALL)
			format_lengths = get_payoffs[0].replace('[','').replace(']','')
			length = string_to_list_single([],format_lengths)

			# Now using new data and yesterdays data it sees if there are
			# any new activities and adds them to the list as appropriate.
			print "\nActivity Length Start: " + str(len(activity_list)) + "\nPayoffs Length Start: " + str(len(payoff)) + "\nLengths len start: " + str(len(length))
			add_new_activity(activity_list, payoff, length, sys.argv[2])
			print "\nActivity Length End: " + str(len(activity_list)) + "\nPayoffs Length End: " + str(len(payoff)) + "\nLengths len end: " + str(len(length))
			return activity_list , payoff, length



if __name__ == '__main__':
	# Calls the main function and prints results to Newest_data.txt
	a, p, l = main()
	print "\n len a:" + str(len(a)) + "\n Len p: " + str(len(p))
	# Prints out demonstration of how running mean works over the course of 6 days with a starting value of 1 showing
	# how the equation adjust appropriately the value based off of adhearence. 
	days_values = [1]
	for i in range(6):
		current_day = i+1
		if current_day >= 4:
			adhearance = False
		else:
			adhearance = True

		append_newest_value(days_values,current_day,adhearance)

	l_flatten = sum(l, [])
	l_mean= sum(l_flatten)/len(l)
	print l_mean



	
#QUESTIONS:
	# How do we know if a person has 'adheared' to an activity? I.e. completed or passed over the activity. 
	# What is our original goal expenditure? I.E How do we find out the starting 
	


