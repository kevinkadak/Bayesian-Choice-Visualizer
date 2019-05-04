import pandas as pd
import statistics
from matplotlib import pyplot as plt

df_path = r'C:\Users\kevin\OneDrive\Uni\Miller Lab\Bayesian Experiment\Thesis\Bayesian Thesis Modelling\Finalized Dataframe.xlsx' #Path of the CSV containing fish data
df_file = pd.ExcelFile(df_path) #Link the directory path to this variable <<<
df = pd.read_excel(df_file) #Load the DF into this variable, skip the first column in the file <<<

def GatherData(df): #Scrape the data from each row (starting from last item to first) and place it in a list, then place each list in a single meta_list holding all data
    meta_seq = []
    for index, row in df.iterrows():
        sequence = []
        for item in row:
            sequence.append(item)
        meta_seq.append(sequence)
    return meta_seq
alldata = GatherData(df)

StimFishChoices = []
TestFishChoice = []

def TrialToChoices(alldata):
    for list in alldata:
        list_no_null = [item for item in list if str(item) != 'nan'] #While iterating through each list of the meta-sequence holder, remove all null (nan) values from each
        all_choices = list_no_null[4:]

        ROUND = list[0]
        print ('Round: {}'.format(ROUND))
        DAY = list[1]
        print ('Day: {}'.format(DAY))

        TRIAL = list[2]
        print ('Trial: {}'.format(TRIAL))

        ID = list[3]
        print ('Fish ID: {}'.format(ID))

        print('All trial choices: {}'.format(all_choices))

        TrialChoices = [] #From all the choices made in a single trial, starting from the end of the list, scrape each choice and append it if it's a positive number.  Stop appending once the length of the list = 5.  Reverse the final choices list
        for choice in all_choices[::-1]:
            if choice > 0 and len(TrialChoices) < 5:
                TrialChoices.append(choice)
        TrialChoices.reverse()

        StimFishChoices.append(TrialChoices[0:4])
        TestFishChoice.append(TrialChoices[-1])

        print ('Trial final choices: {}'.format(TrialChoices))
        print()
TrialToChoices(alldata)

print("***")
print()
print ('StimFishChoices: {}'.format(StimFishChoices))
print ('TestFishChoices: {}'.format(TestFishChoice))
print()

#1 = left, 2 = right
all_sequences = [[1, 1, 1, 1], [2, 1, 1, 1], [1, 2, 1, 1], [1, 1, 2, 1], [1, 1, 1, 2], [1, 2, 2, 1], [1, 2, 1, 2], [1, 1, 2, 2], [2, 2, 2, 2], [1, 2, 2, 2], [2, 1, 2, 2], [2, 2, 1, 2], [2, 2, 2, 1], [2, 1, 1, 2], [2, 1, 2, 1], [2, 2, 1, 1]]

unique_sequences_scores = [
['{1,1,1,1}', 0, 0], #item zero = unique majority-dissent sequences, item one = n of sequence, item two = number of trial choices in which the test fish followed the majority choice
['{0,1,1,1}', 0, 0],
['{1,0,1,1}', 0, 0],
['{1,1,0,1}', 0, 0],
['{1,1,1,0}', 0, 0],
['{1,0,0,1}', 0, 0],
['{1,0,1,0}', 0, 0],
['{1,1,0,0}', 0, 0]
]

def SeqAndChoice(StimFishChoices, TestFishChoice, all_sequences): #Function to count the total number of trials in a sequence and the percentage of majority choices by the test fish in each
    for single_seq, choice in zip(StimFishChoices, TestFishChoice):
        #N of sequence
        stype = all_sequences.index(single_seq) #stype = index of a given trial sequence within the list of unique sequence
        if stype > 7:
            stype = stype - 8 #If the index is greater than 8, code the sequence in the same common item
        unique_sequences_scores[stype][1] += 1 #Update the n of a given sequence in the master unique_sequences_scores
        #Test fish choice in sequence
        if statistics.mean(single_seq) == 1.5 and choice == single_seq[0]: #This isn't an elif statement below because the try: seems to be messing it up
            unique_sequences_scores[stype][2] += 1
        try:
            if choice == statistics.mode(single_seq):
                unique_sequences_scores[stype][2] += 1
        except statistics.StatisticsError:
            continue
SeqAndChoice(StimFishChoices, TestFishChoice, all_sequences)
print ('Unique sequence scores: {}'.format(unique_sequences_scores))

def GraphData(unique_sequences_scores): #Function to generate a graph from the unique sequence scores
    simple = [0.867613, 0.719101, 0.719101, 0.719101, 0.719101, 0.5, 0.5, 0.5] #Projected choice data for the simple,
    complex = [0.946065, 0.915066, 0.881952, 0.795311, 0.448956, 0.666481, 0.257618, 0.15288] #complex.
    follow_last = [0.832018, 0.832018, 0.832018, 0.832018, 0.167982, 0.832018, 0.167982, 0.167982]# and 'follow last' model

    n = []
    x = []
    y = []
    for i in unique_sequences_scores:
        n.append(i[1]) #From each unique sequence: append the n
        x.append(i[0]) #append the titles
        y.append(i[2]/i[1]) # append the majority choices divided by the total number of trials (ie. percentages)

    fig, ax = plt.subplots()

    ax.scatter(x, y, zorder = 4, label = "Collected data") #Plot individual points of the collected data
    ax.plot(x, simple, c = 'gold', zorder = 1, label = "Simple model projection") #Plot simple model porjected data as a line
    ax.plot(x, complex, c = "orangered", zorder = 2, label = "Complex model projection") #Plot complex model porjected data as a line
    ax.plot(x, follow_last, c = "crimson", zorder = 3, label = "'Follow last' model projection") #Plot 'follow last' model porjected data as a line

    ax.set_title("Rate of Following Majority Choice Compared to Model Projections")
    ax.set_xlabel("Unqiue Sequences")
    ax.set_ylabel("P(Following Majority)")

    plt.yticks(ticks=[0,.2,.4,.6,.8,1]) #Make y-axis ticks increment by from 0 to 1 by .2
    ax.legend(loc='best', prop = {'size':9}) #Place the legend in the most open space

    plt.show()
GraphData(unique_sequences_scores)
