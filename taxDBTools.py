#A script to parse .dmp files from the NCBI taxonomy database into
# comma separated variable (CSV) files.

import datetime
import time
import csv

import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()


#A function to simply time the length each function takes to run and print
#the result.  Not at all necessary, but I like it.  Remove the "@timer"
#decorator above each function to disable this.
def timer(func):
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        result = func(*args, **kwargs)
        end = datetime.datetime.now()
        print("\tCompleted in "  + str(end - start))
        return(result)
    return(wrapper)

#Open the .dmp file and read into inputData.  Creates a list where each
#item in the list is one line of the .dmp file
@timer
def readfile(file):
    print("\tReading " + str(file))
    with open(file) as dmpFile:
        inputData = dmpFile.readlines()    
    return(inputData)

#Go through each line of text in inputData, and replace all pipe characters
# ("|") with commas.  Split the line into elements of a list separarted by
#commas, delete newlines and tabs, and append that list to a list called
#organismsList. Takes newline separated strings and returns a list of lists,
#where each inner list is a line of text split into elements
@timer
def convertFormat(inputData):
    print("\tConverting data to CSV format...")
    organismsList = []
    for line in inputData:
        organism = line.replace("\t", "")
        organism = organism.replace("|", ",")
        organism = organism.replace("\n", "")
        singleOrganismList = organism.split(",")
        #singleOrganismList[0] = int(singleOrganismList[0])
        organismsList.append(singleOrganismList)
        
    return organismsList

#The taxID numbers in the database are not contiguous, i.e. there are numbers
#in the dataset which have no organism.  Searching this dataset will be
#easier if the position in the list is equal to the taxID (so that to find
# the Archaea, taxID 2157, you simply go to the 2157th item in the list).  To
# achieve this the list needs to be "padded" with blank organisms where a number
#does not match a taxonomy ID number.
#Takes a list of lists where the inner list contains a single organism, and the
# taxID number is the first item in the inner list.  Inserts a blank list
#where a taxID is empty and outputs a list of lists.
@timer
def padCSV(inputData):
    print("\tPadding the data (this may take a few minutes)...")
    finalTaxid = int(inputData[len(inputData)-1][0])
    count = 0

    itemsPerInnerList = len(inputData[0])
    blankList = []
    
    for x in range (1, itemsPerInnerList):
        blankList.append("none")

    for x in range (0, finalTaxid):
        if (int(inputData[x][0]) == count):
            count += 1
        else:
            inputData.insert(x, [str(x)] + blankList)
            count += 1

    return(inputData)
        

def getInputData(fileName):
    #Get a FASTA file to open
    #Loop while a location hasn't been set
    gettingLocation = True
    while (gettingLocation == True):
        print("\nPlease locate the " + fileName + ".dmp file: ")
        #Get a file location, set as inputFASTALocation
        inputFileLocation = filedialog.askopenfilename()
        #Try to open the file, if successful set as FASTAData
        try:
            file = open(inputFileLocation,"r")
            gettingLocation = False
        #If opening the file fails alert the user and try again
        except IOError:
            print("Sorry, I'm unable to open that file location.")
    return(inputFileLocation)

def getOutputLocation():
    #Get a file location to save the output data
    gettingLocation = True
    #Get a file location, set as outputFASTALocation
    while (gettingLocation == True):
        print("\nPlease choose an output file location and file name: ")
        outputFileLocation = filedialog.asksaveasfilename()
        #Try to open the file, if successful set as "file"
        try:
            file = open(outputFileLocation,"w")
            gettingLocation = False
        #If opening the file fails alert the user and try again
        except IOError:
            print("Sorry, I'm unable to open that file location.")
    return(outputFileLocation)
        
@timer
def combineFiles(nodesCSV, lineageCSV):
    print("\nCombining files...")
    start = datetime.datetime.now()
    if (len(nodesCSV) == len(lineageCSV)):
        for x in range (0, len(nodesCSV)):
            lineageCSV[x].insert(1, nodesCSV[x][1])
            lineageCSV[x].insert(2, nodesCSV[x][2])
        return lineageCSV
    else:
        print("ERROR! The number of organisms in the Nodes and Lineage files\
 don't seem to match.  This means that they can't integrate properly.  Aborted\
 process")
############################
#Actual program starts here#
############################

nodesInputFile = getInputData("nodes")
lineageInputFile = getInputData("rankedlineage")

outputFileLocation = getOutputLocation()

scriptStart = datetime.datetime.now()
#process the Nodes file
nodesStart = datetime.datetime.now()
print("\nProcessing the Nodes.dmp file, begun at " + str(scriptStart))

inputData = readfile(nodesInputFile)
sciData = convertFormat(inputData)

sciData.sort(key=lambda x:int(x[0]))

nodesCSV = padCSV(sciData)

nodesEnd = datetime.datetime.now()
print("Finished processing the nodes.dmp file in "  \
      + str(nodesEnd - nodesStart))

#process the Lineage.dmp file
lineageStart = datetime.datetime.now()
print("\nProcessing the lineage.dmp file, begun at " + str(scriptStart))

inputData = readfile(lineageInputFile)
sciData = convertFormat(inputData)

sciData.sort(key=lambda x:int(x[0]))

lineageCSV = padCSV(sciData)

lineageEnd = datetime.datetime.now()
print("Finished processing the lineage.dmp file in "  \
      + str(lineageEnd - lineageStart))

#Combine the two files
combinedData = combineFiles(nodesCSV, lineageCSV)

#Writing to output file
print("Writing data to " + str(outputFileLocation))
start = datetime.datetime.now()
with open(outputFileLocation, "w") as file:
      for line in combinedData:
          file.write(",".join(line) + "\n")
print("Whole script completed in " + str(datetime.datetime.now() - scriptStart))

print("Done!")



