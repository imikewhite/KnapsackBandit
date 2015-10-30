activity_list = []
payoff_length = [] 



with open("suggestions_gps2.txt" , "r") as filestream:
   	for line in filestream:
		currentline = line.split(",")
		activity = [currentline[1], currentline[2]]
		length = currentline[6]
		p_and_l = [currentline[3], length[:-1]]
		if (activity not in activity_list):
			activity_list.append(activity)
			payoff_length.append(p_and_l)
		else:
			pass
	print "Here is activity list: " 
	print activity_list 
	print "\n"
	print "Here is payoffs and lengths" 
	print payoff_length 
	print "\n"




#Did we get a 'benchmark' value for overall increase

# How should we keep track of pay-offs?

#Still trying to find a mathematical function to adjust the value (which)
# is a combination of adhearance and energy expenditure) apprpriately.
#Mainly this week we focused on parsing the given informaton and formulated

# some idea on what exactly itmeans/we want to do with it

#Dont really need to make note of this:
#Thinking of EXP 3 like suggested, but some changes may have to be made.


