# Below Is Pseudo Code for a Knapsack/Bandit Algorithm for the App BeWell

#1. We need back pain patients to increase their activity by 10% from the past.
#We already know what exercises that they can do or they have done before.
#We need to find a combination of the user's exercises to create a plan - (i)
#easy to do (ii) 10% more than their existing baseline. Note here easy-to-do
#exercises are what user's have done before often/many times - since they are already good at it.

#2.Finding a combination of exercises is very similar to a well known problem called "Knapsack". 
#Look it into wikipedia to see what the problem is. Following two links can also give you ideas about Knapsack.
#You don't need to go to super detail since familiarity of the problem is important and it is not important to 
#figure out the exact algorithm/solution. -https://en.wikipedia.org/wiki/Knapsack_problem -https://www.youtube.com/watch?v=ocZMDMZwhCY


#Knapsack has three aspects: Total size of the knapsack, activities: Which have a size and value, and you want to
#maximize the total value of activities that can fit in your knapsack

#Initialize size of knapsack based on the amount of activity we want to do that day. 
#Update weekly to increase size by 10 % (1.1 * previous weeks activities)

#I assume the data we are given comes with an activity which has a value (how many calories it burns)
#and size (How long it takes to do)
import sys

def knapsack(activities, knapsack_size):
    '''
    Solve the knapsack problem by finding the most valuable
    subsequence of `activities` that weights no more than `knapsack_size`.

    `activities` is a sequence of pairs `(value, weight)`, 
     `value` is a number representing a combination of adhearance and Energy expenditure
     `weight` is a number representing the Energy expenditure alone

    `knapsack_size` is a non-negative integer. Represents the goal amount of energy expenditure

    Return a pair whose first element is the sum of values in the most
    valuable subsequence, and whose second element is the subsequence.

    >>> activities = [(4, 12), (2, 1), (6, 4), (1, 1), (2, 2)]
    >>> knapsack(activities, 15)
    (11, [(2, 1), (6, 4), (1, 1), (2, 2)])
        '''

    #N = len(activities)
    #W = knapsack_size
    # Create an (N+1) by (W+1) 2-d list to contain the running best values 
    # Where bestvalues[i][j] is the best sum of values for any
    # subsequence of the first i activities, whose weights sum
    # to no more than j.
    bestvalues = [[0] * (knapsack_size + 1)
                  for _ in xrange(len(activities) + 1)]

    # Enumerate through the activities and fill in the best-value table
    for i, (value, size) in enumerate(activities):
        for capacity in xrange(knapsack_size + 1):
            # Handle the case where the size of the current item is greater
            # than the "running capacity" - we can't add it to the knapsack
            if size > capacity:
                bestvalues[i+1][capacity] = bestvalues[i][capacity]
            else:
                # Otherwise, we must choose between two possible candidate values:
                # 1) the value of "running capacity" as it stands with the last item
                #    that was computed; if this is larger, then we skip the current item
                # 2) the value of the current item plus the value of a previously computed
                #    set of activities, constrained by the amount of capacity that would be left
                #    in the knapsack (running capacity - item's size)
                candidate1 = bestvalues[i][capacity]
                candidate2 = bestvalues[i][capacity - size] + value

                # Just take the maximum of the two candidates; by doing this, we are
                # in effect "setting in stone" the best value so far for a particular
                # prefix of the activities, and for a particular "prefix" of knapsack capacities
                bestvalues[i+1][capacity] = max(candidate1, candidate2)

    # Reconstruction
    # Iterate through the values table, and check
    # to see which of the two candidates were chosen. We can do this by simply
    # checking if the value is the same as the value of the previous row. If so, then
    # we say that the item was not included in the knapsack (this is how we arbitrarily
    # break ties) and simply move the pointer to the previous row. Otherwise, we add
    # the item to the reconstruction list and subtract the item's size from the
    # remaining capacity of the knapsack. Once we reach row 0, we're done
    reconstruction = []
    i = len(activities)
    j = knapsack_size
    while i > 0:
        if bestvalues[i][j] != bestvalues[i - 1][j]:
            reconstruction.append(activities[i - 1])
            j -= activities[i - 1][1]
        i -= 1

    # Reverse the reconstruction list, so that it is presented
    # in the order that it was given
    reconstruction.reverse()

    # Return the best value, and the reconstruction list
    return bestvalues[len(activities)][knapsack_size], reconstruction





# def main(filename):
# 	with open(filename) as f:
#         lines = f.readlines()

#     knapsack_size = int(lines[0])
#     activities = [map(int, line.split()) for line in lines[1:]]

#     bestvalue, reconstruction = knapsack(activities, knapsack_size)

#     print('Best possible value: {0}'.format(bestvalue))
#     print('activities:')
#     for value, size in reconstruction:
#         print('V: {0}, W: {1}'.format(value, size))

if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print('usage: knapsack.py [file]')
    #     sys.exit(1)
    # main(sys.argv[1])
    run = (4,12)
    swim = (2,1)
    bike = (6,4)
    dance = (1,1)
    walk = (2,2)
    activities = [run, swim, bike, dance, walk]
    print knapsack(activities, 15)



#Have N activities and each activity has an unknown probability of being completed
#and achieving its value (i.e. calories burned)


# About 90% exploit: 
    #Exploit: Uses the list of activities that we have and gives the user a List in order of highest probability of completon
# Explore: Remove Duds (Lowest probability activities of completion) and replace from list of unused activites the best 
# new option to replace it and sees if the activity can be completed wit a higher probability:
     #Note: When storing the dud we also store the probability that we removed it with. 

#3. The problem with traditional knapsack is the underlying rewards/values of activities 
#(in our case minutes spent in doing an exercise per day) don't change. But in our problem, people's
#exercise pattern changes. So, we can only guess what is best for future and have to strategize well 
#for future. That is where the bandit problem comes in. In this regard, I highly recommend to read the following three papers:

#MyBehavior paper that we will build on http://dl.acm.org/citation.cfm?id=2805840&CFID=545998650&CFTOKEN=93655851
#This bandit algorithm survey paper - http://www.princeton.edu/~sbubeck/SurveyBCB12.pdf. 
#[Don't go into details of mathematics of this paper. They are quite hard. Just read the initial few pages of the document.]
#This is the main paper "bandit with knapsack" that we will try to implement http://arxiv.org/pdf/1305.2545v6.pdf

#Given the above, we just need to write an algorithm and run on real data that can do "bandit with knapsack". 
#That will be your task for the semester. I will give you the data soon, but at this moment can you explore the
#above paper and give me work division. I need a report with pesudo code that is relevant to our problem before 
#start of November and implement the algorithm in Novemeber. I think starting a google doc will be a good idea.
