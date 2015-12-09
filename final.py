# Michael White, Matt Wolfson
#ActivityChoiceOptimization

import random
import sys
import os.path
import re
from datetime import date, datetime, timedelta
import datetime
import math

'''Note:: This program requires that the arguments passed in are as follows:
		1 argument = First time the program is being run, argument is data of activities, payoffs, locations, etc.
		2 arguments = First is data from the previous day named Newest_data.txt (as the program outputs)
					  Second argument is new data that we want to combine with our previous data.

		In addition: This is set to run whenever a activity is completed, even if it is the same day. 
		In other words, newest activities must be added in order of time completed '''

# Global variables used and updated by the program
min_desired_activity=100 #Amount of activity we want users to do, may be specific to person, waiting comments from physios. # Also There needs to be a cap as well!!
weekly_activity_increase=1.1 #Set to increase activity by 10% per week, again waiting comments from physios
max_overflow_percent= 1.5 # If knapsack is filled this percentage more than its
						  # minimum desired activity, it is weighted closer to adherence
days_scored=21 #Number of days in the past used to calculate user compliance
			   #Must be >= 2
knapsack_limit=15 #Number of activities suggested
rating_weights=[1,.75,.5,.35,.25,.2,.1]
adherence_weight = .95 #Must be between 0 and 1, payoff weight will be 1-adherence weight
exploit_probability=.95
input_titles=["Time","ID 1","ID 2","Avg Payoff","Latitude","Longitude","Length"]
info_titles=["Activity ID","Adherence Rating","Payoff Rating","Final Rating","Avg Payoff","Avg Length (min)","Times Completed","Recent Activity"]
knapsack=[]
activity_list = []
activity_info =[]
current_day = None
days_left_in_week = 7
total_days_using_app = 0
first_line = False 
max_raw_score = [0,0] #First index is for adherence and second is for payoff
max_raw_score_index = [0,0]
min_knapsack_score = 0
min_knapsack_score_item = None
	
# "decodes" the line of information from the data
def unpack_raw_data(activity):
	activity_id = [int(activity[input_titles.index("ID 1")]), int(activity[input_titles.index("ID 2")])]
	payoff = float(activity[input_titles.index("Avg Payoff")])
	length = float(activity[input_titles.index("Length")])
	return activity_id, payoff, length

def max_score_needs_update(activity_index,raw_score,score_index,column_name):
	global activity_info, max_raw_score, max_raw_score_index
	if raw_score > max_raw_score[score_index]:
		for activity in range(len(activity_info)):
			old_final_score = activity_info[activity][info_titles.index(column_name)]
			new_final_score = old_final_score*max_raw_score[score_index]/raw_score
			activity_info[activity][info_titles.index(column_name)] = new_final_score
		max_raw_score[score_index] = raw_score
		max_raw_score_index[score_index] = activity_index
		activity_info[activity_index][info_titles.index(column_name)] = 10
		return True
	elif (activity_index == max_raw_score_index[score_index]) & (raw_score < max_raw_score[score_index]):
		old_max_raw_score = max_raw_score[score_index]
		new_max_raw_score = raw_score
		for activity in range(len(activity_info)):
			old_final_score = activity_info[activity][info_titles.index(column_name)]
			old_raw_score = old_final_score*old_max_raw_score/10
			if old_raw_score > new_max_raw_score:
				new_max_raw_score = old_raw_score
				max_raw_score_index[score_index] = activity
		max_raw_score[score_index] = new_max_raw_score
		for activity in range(len(activity_info)):
			old_final_score = activity_info[activity][info_titles.index(column_name)]
			new_final_score = old_final_score*old_max_raw_score/new_max_raw_score
			activity_info[activity][info_titles.index(column_name)] = new_final_score
		return True
	else:
		return False

def calculate_adherence_rating(activity_id):
	global activity_info, max_raw_score, max_raw_score_index
	score_index=0
	column_name="Adherence Rating"
	activity_index=activity_list.index(activity_id)
	recent_activity=activity_info[activity_index][info_titles.index("Recent Activity")]
	
	raw_score=float(0)
	for past_days in range(days_scored):
		weight_index=int(math.floor(past_days*len(rating_weights)/days_scored))
		current_weight=rating_weights[weight_index]
		raw_score=raw_score+current_weight*recent_activity[past_days]
	if max_score_needs_update(activity_index,raw_score,score_index,column_name)==False:
		activity_info[activity_index][info_titles.index(column_name)]=raw_score/max_raw_score[score_index]*10
	return activity_info[activity_index][info_titles.index(column_name)]

def calculate_payoff_rating(activity_id):
	global activity_info, max_raw_score, max_raw_score_index
	activity_index = activity_list.index(activity_id)
	payoff = activity_info[activity_index][info_titles.index("Avg Payoff")]
	if (payoff > max_raw_score[1]) | ((max_raw_score_index[1]==activity_index) & (max_raw_score[1]>activity_info[activity_index][info_titles.index("Avg Payoff")])):
		max_raw_score[1] = 0
		for activity in range(len(activity_info)):
			payoff=activity_info[activity][info_titles.index("Avg Payoff")]
			if payoff > max_raw_score[1]:
				max_raw_score[1]=payoff
				max_raw_score_index[1]=activity
		for activity in range(len(activity_info)):
			payoff = activity_info[activity][info_titles.index("Avg Payoff")]
			payoff_score = payoff/max_raw_score[1]*10
			activity_info[activity][info_titles.index("Payoff Rating")] = payoff_score
	else:
		payoff = activity_info[activity_index][info_titles.index("Avg Payoff")]
		payoff_score = payoff/max_raw_score[1]*10
		activity_info[activity_index][info_titles.index("Payoff Rating")] = payoff_score
	return activity_info[activity_index][info_titles.index("Payoff Rating")]

def calculate_final_rating(activity_id):
	adherence = calculate_adherence_rating(activity_id)
	payoff = calculate_payoff_rating(activity_id)
	final_score = adherence_weight*adherence+(1-adherence_weight)*payoff

	activity_index = activity_list.index(activity_id)
	activity_info[activity_index][info_titles.index("Final Rating")]=final_score

# Gets the total payoff of all the activites in the knapsack
def knapsack_total_payoff():
	total_payoff = 0
	for item in knapsack:
		total_payoff = total_payoff + activity_info[activity_list.index(item)][info_titles.index("Avg Payoff")]
	return total_payoff

# Updates global variable to hold the smallest item in the knapsacks information (for easy removal)
def find_smallest_knapsack_item():
	global min_knapsack_score, min_knapsack_score_item
	min_knapsack_score = float("inf")
	min_knapsack_score_item = None
	for item in knapsack:
		item_index = activity_list.index(item)
		item_score = activity_info[item_index][info_titles.index("Final Rating")]
		if item_score < min_knapsack_score:
			min_knapsack_score = item_score
			min_knapsack_score_item = item

# Replaces wors activity in knapsack with a new one
def replace_knapsack_item(min_knapsack_score_item,activity_id):
	global knapsack
	knapsack.remove(min_knapsack_score_item)
	knapsack.append(activity_id)
	find_smallest_knapsack_item()

#Adds activity to knapsack if there is room or activity is better than an existing one in the knapsack
def add_to_knapsack_attempt(activity_id):
	global knapsack, min_knapsack_score, min_knapsack_score_item
	activity_index = activity_list.index(activity_id)
	if len(knapsack)<knapsack_limit:
		knapsack.append(activity_id)
		find_smallest_knapsack_item()
	elif activity_info[activity_index][info_titles.index("Final Rating")] > min_knapsack_score:
		replace_knapsack_item(min_knapsack_score_item,activity_id)

# Adds new activity to the list and attempts to add it to the knapsack
def add_new_activity(activity_id,payoff,length):
	global activity_list, activity_info
	activity_list.append(activity_id)
	activity_info.append([activity_id,0,0,0,payoff,length,1,[0]*days_scored])
	activity_info[activity_list.index(activity_id)][info_titles.index("Recent Activity")][0]=1
	calculate_final_rating(activity_id)
	add_to_knapsack_attempt(activity_id)

#Post: Knapsack with optimum combination of acttivites
def reorder_knapsack(attempts):
	global adherence_weight
	for activity in activity_info:
		# Gets activity
		rating = activity[info_titles.index("Final Rating")]
		activity_id = activity[info_titles.index("Activity ID")]
		# If its better than something in the list it replaces it
		if (activity_id not in knapsack) & (rating > min_knapsack_score):
			replace_knapsack_item(min_knapsack_score_item, activity_id)
	# If a list cannot be made above minimum desired activity and below maximum, output most recent list.
	# Note, this shouldn't really happen, however it is possible for the below ifs to get caught in a loop
	# So to account for this we put maximum attempts at 5 for creating perfectly acceptable list.
	if attempts == 5:
		pass
	# If we added to much to the knapsack, give adhearence more weight
	elif knapsack_total_payoff()>max_overflow_percent*min_desired_activity:
		new_weight = (adherence_weight+1)/2
		if new_weight < .99999:
			adherence_weight=new_weight
			for item in knapsack:
				calculate_final_rating(activity_info[activity_list.index(item)][info_titles.index("Activity ID")])
				find_smallest_knapsack_item()
			reorder_knapsack(attempts + 1)
	# If we calculated below our minimum desired activity, give payoffs more weigh
	elif knapsack_total_payoff() < min_desired_activity:
		if adherence_weight > .15:
			new_weight = adherence_weight-.1
		else:
			new_weight = adherence_weight/1.5
		if new_weight > .05:
			adherence_weight=new_weight
			for item in knapsack:
				calculate_final_rating(activity_info[activity_list.index(item)][info_titles.index("Activity ID")])
				find_smallest_knapsack_item()
			reorder_knapsack(attempts + 1)

# Allows us to randomly explore with a low probability
def explore_today():
	if random.random() > exploit_probability:
		explore = True
	else:
		explore = False
	return explore

# Starts a new week
def update_week():
	global min_desired_activity, days_left_in_week
	min_desired_activity=min_desired_activity*weekly_activity_increase
	days_left_in_week=7

def update_day(last_activity_day,current_day):
	#TODO: Make sure it accurately updates if multiple days skipped in new month
	global activity_info, days_left_in_week, total_days_using_app, knapsack
	if current_day > last_activity_day:
		days_since_last_use = current_day - last_activity_day
		days_left_in_week = days_left_in_week - days_since_last_use
		total_days_using_app = total_days_using_app + days_since_last_use
	else:
		days_left_in_week = days_left_in_week - current_day
		total_days_using_app = total_days_using_app + current_day
	if days_left_in_week <= 0:
		update_week()

	#Update newest activities rating
	for i in range(len(activity_info)):
		j=info_titles.index("Recent Activity")
		activity_info[i][j][1:days_scored]=activity_info[i][j][0:days_scored-1]
		activity_info[i][j][0]=0
		calculate_final_rating(activity_info[i][info_titles.index("Activity ID")])

	# If exploring, remove worst 2 items from knapsack and replace with random activities
	if explore_today():
		knapsack.remove(min_knapsack_score_item)
		find_smallest_knapsack_item()
		knapsack.remove(min_knapsack_score_item)
		activities_added_to_knapsack=0
		while (activities_added_to_knapsack < 2):
			random_activity = activity_list[int(random.random()*len(activity_list))]
			if random_activity not in knapsack:
				knapsack.append(random_activity)
				activities_added_to_knapsack += 1
		# print knapsack
		find_smallest_knapsack_item()

	# else update the knapsack to have the best combination of activites
	else:
		reorder_knapsack(0)


def check_and_process_new_day(last_activity_day,activity):
	global current_day, first_line
	current_day=int(datetime.datetime.fromtimestamp(
	        int(activity[input_titles.index("Time")][0:10])
	    ).strftime('%d'))
	if first_line:
		first_line=False
	elif last_activity_day != current_day:
		update_day(last_activity_day,current_day)

#Updates activity info for the activity currently being worked with
def update_activity_info(activity_id,payoff,length):
	global activity_info

	index=activity_list.index(activity_id)
	old_total=activity_info[index][info_titles.index("Times Completed")]
	new_total=old_total+1

	old_length=activity_info[index][info_titles.index("Avg Length (min)")]
	new_length=(old_length*old_total+length)/new_total

	old_payoff=activity_info[index][info_titles.index("Avg Payoff")]
	new_payoff=(old_payoff*old_total+payoff)/new_total

	activity_info[index][info_titles.index("Avg Payoff")]=new_payoff
	activity_info[index][info_titles.index("Avg Length (min)")]=new_length
	activity_info[index][info_titles.index("Times Completed")]=new_total
	activity_info[index][info_titles.index("Recent Activity")][0]=activity_info[index][info_titles.index("Recent Activity")][0]+1

#Post:Updates running data file with global variables, activities, etc.
def update_data_file():
	if os.path.isfile('Newest_data.txt'):
		open('Newest_data.txt', 'w').close()
	file = open('Newest_data.txt', 'w') 
	file.write("Important Variables: [")
	important_variables=[total_days_using_app,min_desired_activity,days_left_in_week,
		current_day,max_raw_score,max_raw_score_index,min_knapsack_score,
		min_knapsack_score_item, adherence_weight, knapsack]
	file.write(str(important_variables[0]))
	for var in important_variables[1:]:
		file.write(', ' + str(var))
	file.write('] end')
	file.write("\n \nActivities: [")
	file.write(str(activity_list).strip('[]') + '] end')
	file.write("\n \nActivity Info: [[")
	file.write(str(activity_info).strip('[]') + ']] end')
	file.close()

#Post: Outputs a new Knapsack list, and updates Newest_data 
def process_activity(new_input):
	#Updates or adds any activity to the list from file
	global activity_info, activity_list, current_day
	with open(new_input, "r") as raw_data:
		for raw_activity in raw_data:
			activity = raw_activity.split(",")
			activity_id, payoff, length = unpack_raw_data(activity)

			if (activity_id not in activity_list):
				add_new_activity(activity_id,payoff,length)
			else:
				update_activity_info(activity_id,payoff,length)

			check_and_process_new_day(current_day,activity)

	update_data_file()


#The following string_to functions are for writing to the file, storing information
#Or to retrieve information from said file

def string_to_list_single(lst,string):
	if len(string) == 0:
		return lst
	else:
		entry = string[:string.find(',')]
		next_entries = string[string.find(',')+2:]
		if entry.find('.') == -1:
			lst.append(int(entry))
		else:
			lst.append(float(entry))
		next_entries_index = next_entries.find(',')
		end_of_list_index = next_entries.find(']')
		next_list_index = next_entries.find('[')
		if (next_list_index != -1) & (next_entries_index > next_list_index):
			return lst, next_entries
		elif(end_of_list_index !=-1 & next_entries_index > end_of_list_index):
			entry = next_entries[:end_of_list_index]
			if entry.find('.') == -1:
				lst.append(int(entry))
			else:
				lst.append(float(entry))
			next_entries=next_entries[end_of_list_index+1:]
			return lst, next_entries
		elif next_entries_index == -1:
			if next_entries.find('.') == -1:
				lst.append(int(next_entries[:next_entries.find(']')]))
			else:
				lst.append(float(next_entries[:next_entries.find(']')]))
			return lst
		else:
			return string_to_list_single(lst, next_entries)

#Parse Activity_info
def string_to_list_of_list(list_of_list,string):
	if len(string) == 0 | string.find('[[')==-1:
		return list_of_list
	else:
		new_list=[]
		entry = string[:string.find(']]')+2]
		activity_id_1=int(entry[entry.find('[[')+2:entry.find(',')])
		activity_id_2=int(entry[entry.find('[[')+5:entry.find(']')])
		activity_id=[activity_id_1, activity_id_2]
		new_list.append(activity_id)
		entry = entry[entry.find(']')+3:]
		new_list, next_entries = string_to_list_single(new_list,entry)
		recent_activity_list = string_to_list_single([],next_entries[next_entries.find('[')+1:])
		new_list.append(recent_activity_list)
		list_of_list.append(new_list)
		next_entries = string[string.find(']]')+4:]
		if next_entries.find(']]')==-1:
			return list_of_list
		else:
			return string_to_list_of_list(list_of_list,next_entries)

# Parses yesterdays data to retrive the information stored in it.
def string_to_list(lst,string):
	if len(string) == 0:
		return lst
	else:
		first_entry = string[:string.find(',')]
		working_second = string[string.find(',')+2:]
		if working_second.find(',') == -1:
			second_entry = working_second
			lst.append([int(first_entry),int(second_entry)]) 
			return lst
		else:
			second_entry = working_second[:working_second.find(',')] 
			lst.append([int(first_entry),int(second_entry)]) 
			return string_to_list(lst, working_second[working_second.find(',')+2:])

#Parse Variable list. Works when the only list of list is the knapsack
def string_to_variable_list(variable_list,string):
	if len(string) == 0 | string.find('[[')==-1:
		return list_of_list
	else:
		new_list=[]
		new_list, next_entries=string_to_list_single(new_list,string[1:])
		more_items = True
		while more_items:
			new_item=[]
			double_bracket_index = next_entries.find('[[') if next_entries.find('[[') !=-1 else float("inf")
			bracket_index = next_entries.find('[') if next_entries.find('[')!=-1 else float("inf")
			new_item_index = next_entries.find(',') if next_entries.find(',')!=-1 else float("inf")
			end_item_index = next_entries.find(']')
			if (len(next_entries)==0) | (all(x>end_item_index for x in (double_bracket_index, bracket_index, new_item_index))):
				break
			if double_bracket_index <= bracket_index & double_bracket_index < new_item_index:
				end_index=next_entries.find(']]')
				next_entry=next_entries[:end_index].replace('[','').replace(']','')
				new_item = string_to_list(new_item,next_entry)
				new_list.append(new_item)
				next_entries = next_entries[end_index+2:]
			elif bracket_index < new_item_index:
				new_item, next_entries = string_to_list_single(new_item,next_entries[next_entries.find('[')+1:])
				next_entries = next_entries[next_entries.find(',')+1:]
				new_list.append(new_item)
			else:
				new_list, next_entries=string_to_list_single(new_list,next_entries)
		return new_list

# Sets global variables according to previous day's values
def update_variables(variables_list):
	global total_days_using_app, min_desired_activity, days_left_in_week, current_day, \
		max_raw_score, max_raw_score_index, min_knapsack_score, \
		 min_knapsack_score_item, adherence_weight, knapsack
	total_days_using_app = variables_list[0]
	min_desired_activity = variables_list[1]
	days_left_in_week = variables_list[2]
	current_day = variables_list[3]
	max_raw_score = variables_list[4]
	max_raw_score_index = variables_list[5]
	min_knapsack_score = variables_list[6]
	min_knapsack_score_item = variables_list[7]
	adherence_weight = variables_list[8]
	knapsack = variables_list[9]

def main():
	global first_line,current_day, activity_info, activity_list
	# First time it is run
	if len(sys.argv)==2:
		first_line=True
		process_activity(sys.argv[1])
	# Being run with previous data and new activity
	if len(sys.argv)==3:
		# First argument (after script name) is data from last day
		with open(sys.argv[1] , "r") as filestream:
			# retrieves lists of last days information
			data = filestream.read()
			get_variables = re.findall(r'Important Variables: (.*?) end',data,re.DOTALL)
			variables_list = string_to_variable_list([],str(get_variables[0]))
			update_variables(variables_list)
			get_activities = re.findall(r'Activities: (.*?) end',data,re.DOTALL)
			format_activities = get_activities[0].replace('[','').replace(']','')
			activity_list = string_to_list([],format_activities)
			get_info = re.findall(r'Activity Info: (.*?) end',data,re.DOTALL)
			activity_info = string_to_list_of_list([],str(get_info[0]))
			# Now using new data and yesterdays data it calculates a new knapsack list.
			process_activity(sys.argv[2])
			
if __name__ == '__main__':
	# Calls the main function and prints results to Newest_data.txt
	if len(sys.argv)==1:
		print "No Data",  "Was Given" 
	else:
		main()
		print 
		print "Days Using App: " + str(total_days_using_app) 
		print "Total Unique Activities: " + str(len(activity_list))
		print
		print "Final Knapsack:"
		print "Item/Final score/Payoff/Adherence"
		running_sum = 0
		for item in knapsack:
			print (
				str(item) +
				" / " + str(activity_info[activity_list.index(item)][info_titles.index("Final Rating")])[0:4]
				+ " / " + str(activity_info[activity_list.index(item)][info_titles.index("Payoff Rating")])[0:4]
				+ " / " + str(activity_info[activity_list.index(item)][info_titles.index("Adherence Rating")])[0:4]
				)
		print "Payoff Goal: " + str(min_desired_activity)
		print "Total Payoff of all Activities: " + str(knapsack_total_payoff())
		print "Total Adherence Weight: " + str(adherence_weight)


		# I think instead of having to store data and output a file we should be able to just run this on a 
		# given set of data and output a knapsack. Which is what I think your other version had done. 
