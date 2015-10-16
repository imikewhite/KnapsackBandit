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


#Knapsack has three aspects: Total size of the knapsack, items: Which have a size and value, and you want to
#maximize the total value of items that can fit in your knapsack

#Initialize size of knapsack based on the amount of activity we want to do that day. (1.1 * previous days activities)
knapsack_size = 0

#I assume the data we are given comes with an activity which has a value (minutes it takes to do it)
#and size (How long it takes to do)











#3. The problem with traditional knapsack is the underlying rewards/values of items 
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