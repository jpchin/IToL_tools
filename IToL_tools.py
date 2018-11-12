#A script to take a FASTA file, identify the organism of each sequence by
#reading watever is between square brackes ("[" and "]"), and search that
#against the combined nodes/lineage files from the NCBI taxonomy database.
#It then reports how many organisms it has found at each taxonomic level and
#reports unique taxa at that level.  The user can then specify at which level
#they want their data "clustered", and the script will output code for the
#Interactive Tree of Life's annotation system where each organism has the
#selected taxonomic level highlighted in a label colour unique for that level

#CSV module required to read the combined taxonomic databse
import csv

#Random module required for generating random colours for labels
import random
random.seed()

#Stuff for file selection dialogs
import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()

#Define the file of input FASTA sequences to process
#inputFile = "/home/jason/Desktop/PPX_trees/PPX_deduped.fasta"

#Define the location of the combined nodes/levels of the taxonomic database
#db = "/home/jason/Desktop/PythonScripts/combined.csv"

def taxonomy_range():

    gettingLocation = True
    while (gettingLocation == True):
        print("\nPlease choose an input file with FASTA sequences: ")
        #Get a file location, set as inputFASTALocation
        inputFile = filedialog.askopenfilename()
        #Try to open the file, if successful set as FASTAData
        try:
            test = open(inputFile,"r")
            gettingLocation = False
            #If opening the file fails alert the user and try again
        except IOError:
            print("Sorry, I'm unable to open that file location.")


    gettingLocation = True
    while (gettingLocation == True):
        print("\nPlease select the database file: ")
        #Get a file location, set as inputFASTALocation
        db = filedialog.askopenfilename()
        #Try to open the file, if successful set as FASTAData
        try:
            test = open(db,"r")
            gettingLocation = False
            #If opening the file fails alert the user and try again
        except IOError:
            print("Sorry, I'm unable to open that file location.")


    
    #Define the file of input FASTA sequences to process
    #inputFile = "/home/jason/Desktop/PPX_deduped.fasta"

    #Define the location of the combined nodes/levels of the taxonomic database
    #db = "/home/jason/Desktop/PythonScripts/combined.csv"

    print("Reading the database\n")
    #Read the database CSV file into a CSV object
    taxDB = csv.reader(open(db, "r"), delimiter=",")

    #CSV objects are not subscriptable, which is a pain.  Read each row of the taxDB
    #csv file into a list called taxList
    taxList = []
    for line in taxDB:
        taxList.append(line)

    #Next, process the organisms in the input FASTA file.  Each organism will be
    #inserted into a dictionary, initially just with an element for the seq header
    organisms = []

    print("Opening the FASTA file\n")
    #Open the query (multi-)FASTA file
    with open(inputFile, "r") as file:
        data = file.readlines()

        #Add the header of each seq to a dictionary and append that to a list called
        #"organisms"

        for line in data:
            if(line[0] == ">"):
                organisms.append({"header":line.replace("\n", "")})

        #Extract organism names from the headers and append to an element in the
        #dictionary called "name"
        for organism in organisms:
            header = organism["header"]
            nameStart = header.find("[")
            nameEnd = header.find("]", nameStart)
            name = header[nameStart+1:nameEnd]
            #Clean up any whitespace characters
            name = name.replace("\n", "")
            name = name.replace("\r", "")
            name = name.replace("\t", "")
            #Append all of this to the organism's dictionary
            organism["name"] = name


    #For each organism, find the first item in the taxonomy databasae which is
    #an exact match.  When found, append the taxonomy ID of the organism, and set
    #the name of this taxonomic rank to equal the taxonomic rank (e.g. set the
    #dictionary element "genus" to equal "Escherichia".
    #findingOrganism = True

    print("\nFinding matching taxonomies.  This may take a few minutes...")
    #for each organism in the input list:
    for organism in organisms:
        #get the key of that organism called "name"
        target = organism["name"]
        findingOrganism = True
        #for each organism in the taxonomy database
        for row in taxList:
            #if the name of the organism in the taxDB is the same as the
            #name of the organism in the organisms list
            if row[3] == target:
                findingOrganism = False
                #Create entries in the organism dictionary for the organisms
                #taxID, the taxID it inherits from and the rankname:rank
                organism["taxid"] = row[0]
                organism["inheritsFrom"] = row[1]
                organism[row[2]] = row[3]
        if findingOrganism == True:
            print("WARNING: couldn't find match for " + organism["name"])
            organism["inheritsFrom"] = "1"


    #Go through each organism in the organisms list, and trace their lineage right
    #back to taxID 1 (all life).  For each organism, look at the rank which
    #it inherits from (from the dictionary key "inheritsFrom"), set the name of that
    #rank equal to the value (e.g. "genus" key = value "Escherichia") in the
    #organisms dictionary, and change the "inheritsFrom" value to equal the next
    #taxonomic rank back towards all life.  Repeat this process until the next
    #rank up is "all life" (taxiD 1).  If a lineage stops prematurely report that
    #the script failed to find a lineage, but continue with the other sequeces

    
    for organism in organisms:
        while (organism["inheritsFrom"] != "1"):
            levelUp = taxList[int(organism["inheritsFrom"])]
            organism[levelUp[2]] = levelUp[3]
            organism["inheritsFrom"] = levelUp[1]
    #except:
        #print("WARNING failed to find lineage of " + str(organism))

    #Create variables to count the number of organisms traced back to each level.
    #NOTE: the NCBI taxdB seems to prefer using "superkingdom" over "kingdom", so
    # most organisms will map to SuperKingdom rather than Kingdom.
    kingdom = 0
    superkingdom = 0
    phylum = 0
    Class = 0
    order = 0
    family = 0
    genus = 0
    species = 0

    #Create lists to hold all valid values at that rank, i.e. every time a new genus
    #is identified the name of that genus is appended to the genus list.  This means
    #we can not only see how many organisms are traced to a given taxonomic level,
    #but also which taxons at that taxonomic level are present.
    kingdomList = []
    superkingdomList = []
    phylumList = []
    ClassList = []
    orderList = []
    familyList = []
    genusList = []
    speciesList = []

    #Go through each organisms dictionary and if it's a taxonomic rank then append
    #the taxon name to the appropriate taxonomic level's list
    for organism in organisms:
        for key, value in organism.items():
            if key == "species":
                species += 1
                if value not in speciesList:
                    speciesList.append(value)
            elif key == "genus":
                genus += 1
                if value not in genusList:
                    genusList.append(value)
            elif key == "family":
                family += 1
                if value not in familyList:
                    familyList.append(value)
            elif key == "order":
                order += 1
                if value not in orderList:
                    orderList.append(value)
            elif key == "class":
                Class += 1
                if value not in ClassList:
                    ClassList.append(value)
            elif key == "phylum":
                phylum += 1
                if value not in phylumList:
                    phylumList.append(value)
            elif key == "superkingdom":
                superkingdom += 1
                if value not in superkingdomList:
                    superkingdomList.append(value)
            elif key == "kingdom":
                if value not in kingdomList:
                    kingdomList.append(value)
                kingdom += 1

    print("Opening the FASTA file\n")
    #Open the query (multi-)FASTA file
    with open(inputFile, "r") as file:
        data = file.readlines()

        #Add the header of each seq to a dictionary and append that to a list called
        #"organisms"

        for line in data:
            if(line[0] == ">"):
                organisms.append({"header":line.replace("\n", "")})

        #Extract organism names from the headers and append to an element in the
        #dictionary called "name"
        for organism in organisms:
            header = organism["header"]
            nameStart = header.find("[")
            nameEnd = header.find("]", nameStart)
            name = header[nameStart+1:nameEnd]
            #Clean up any whitespace characters
            name = name.replace("\n", "")
            name = name.replace("\r", "")
            name = name.replace("\t", "")
            #Append all of this to the organism's dictionary
            organism["name"] = name

    #Give the user some stats about how many organisms were traced to each taxonomic
    #level, as well as which taxa are present at that taxonomic level.
    print("There are " + str(len(organisms)) + " organisms in the data.")
    print("Sum of organisms at taxonomic ranks:\n")
    print("\nSuperkingdoms: " + str(superkingdom) + " " + ", ".join(superkingdomList))
    print("\nKingdom: " + str(kingdom)+ " " + ", ".join(kingdomList))
    print("\nPhylum: " + str(phylum)+ " " + ", ".join(phylumList))
    print("\nClass: " + str(Class)+ " " + ", ".join(ClassList))
    print("\nOrder: " + str(order)+ " " + ", ".join(orderList))
    print("\nFamily: " + str(family)+ " " + ", ".join(familyList))
    print("\nGenus: " + str(genus)+ " " + ", ".join(genusList))
    print("\nSpecies: " + str(species)+ " " + ", ".join(speciesList))

    #The point of this scripts is to colour in each organism according to their
    #taxon name in Interactive Tree of Life trees.  Ask the user which taxonomic
    #level should be used to do this.
    target = input("\n\nAt which rank would you like to set colours?\
    [S]uperkingdom, [K]ingdom, [P]hylum, [C]lass, [O]rder, [F]amily, [G]enus, \
    Sp[E]cies\n")
    target = target.upper()

    #Process the user input, desired level is set as "targetLevel"
    if target == "S":
        targetLevel = "superkingdom"
        targetList = superkingdomList
    elif target == "K":
        targetLevel = "kingdom"
        targetList = kingdomList
    elif target == "P":
        targetLevel = "phylum"
        targetList = phylumList
    elif target == "C":
        targetLevel = "class"
        targetList = classList
    elif target == "O":
        targetLevel = "order"
        targetList = orderList
    elif target == "F":
        targetLevel = "family"
        targetList = familyList
    elif target == "G":
        targetLevel = "genus"
        targetList = genusList
    elif target == "E":
        targetLevel = "species"
        targetList = speciesList

    print("Colouring by " + targetLevel)

    #For each taxon at the selected taxonomic level, go through each organisms in
    #the organisms list and if that organism has a taxon at that taxonomic level
    #assign them a key called "colour" with a value unique to that taxon
    for target in targetList:
        for organism in organisms:
            if targetLevel in organism:
                if organism[targetLevel] == target:
                    organism["colour"] = targetList.index(target)

    #Time to generate unique colours for each taxon.  Count how many colours are
    #needed by the size of the "targetList" list
    numRanks = len(targetList)
    colours = []
    #For each colour required, generate random red, green and blue values and append
    #to a list of colours
    for x in range (0, numRanks):
        a = random.randint(0,255)
        b = random.randint(0,255)
        c = random.randint(0,255)
        colour = "rgb(" + str(a) + "," + str(b) + "," + str(c) + ")"
        colours.append(colour)

    #var to keep track of how many organisms will have output data
    found_organisms = 0

    #For each organism, if they've been assigned a colour pull the corresponding
    #string containing R/G/B values and replace their colour value with that string
    for organism in organisms:
        if "colour" in organism:
            found_organisms += 1
            organism["colour"] = colours[organism["colour"]]


    print("\n\nOutputting data for " + str(found_organisms) + " organisms\n\n")



    gettingLocation = True
    while (gettingLocation == True):
        print("\nPlease select an output location: ")
        #Get a file location, set as inputFASTALocation
        outputLocation = filedialog.asksaveasfilename()
        #Try to open the file, if successful set as FASTAData
        try:
            test = open(outputLocation,"w")
            gettingLocation = False
            #If opening the file fails alert the user and try again
        except IOError:
            print("Sorry, I'm unable to open that file location.")

    with open(outputLocation, "w") as file:
        #Print the boilerplate necessary for the colour range file
        file.write("TREE_COLORS\n")
        file.write("SEPARATOR SPACE\n")
        file.write("DATA\n")
        #For each organism, print ITOL coe for colours: the name of the organism,
        #followed by " label " and ending with the string containing colour data
        for organism in organisms:
            if "colour" in organism:
                header = organism["header"]
                headerEnd = header.find(" ")
                header = header[:headerEnd]
                file.write(header[1:] + " range " + str(organism["colour"]) + " " + organism[targetLevel] + "\n")

    print("Done!")


###################################################
# Function for doing binary annotations of a tree #
###################################################
def binary_annotation():

    #Get the FASTA file which was used to generate the tree
    gettingLocation = True
    while (gettingLocation == True):
        print("\nPlease select the FASTA file which was used to draw the tree: ")
        #Get a file location, set as inputFASTALocation
        inputFile = filedialog.askopenfilename()
        #Try to open the file, if successful set as FASTAData
        try:
            test = open(inputFile,"r")
            gettingLocation = False
        #If opening the file fails alert the user and try again
        except IOError:
            print("Sorry, I'm unable to open that file location.")

    #Ask for the title of the overall dataset
    gettingData = True
    while gettingData == True:
        datasetLabel = input("What's the title for this dataset?\n")
        gettingData = False

    #Ask for the default colour of the overall dataset
    gettingData = True
    while gettingData == True:
        colour = input("What colour would you like the default colour to be?\n")
        gettingData = False

    #Ask the user how many datasets they want to annotate with
    gettingData = True
    while gettingData == True:
        numTargets = input("How many datasets would you like to annotate on the tree?\n")
        try:
            inttargets = int(numTargets)
            gettingData = False
        except:
            print("Sorry, you need to enter an integer\n")

    print("Will annotate " + str(inttargets) + " datasets on the tree.\n")

    #Create a list to hold config info about the datasets
    targets = []

    #Get the config data of each dataset to use for annotation
    for x in range (inttargets):
        print("\n\nConfig for dataset " + str(x))
        target = {}
        target["name"] = "target" + str(x)

        #Get the FASTA file to annotate the tree with
        gettingLocation = True
        while (gettingLocation == True):
            print("\nPlease choose the FASTA file to draw symbols with: ")
            #Get a file location, set as inputFASTALocation
            annotationFile = filedialog.askopenfilename()
            #Try to open the file, if successful set as FASTAData
            try:
                test = open(annotationFile,"r")
                gettingLocation = False
                target["file"] = annotationFile
            #If opening the file fails alert the user and try again
            except IOError:
                print("Sorry, I'm unable to open that file location.")

        #Get the symbol shape for this dataset
        gettingData = True
        while gettingData == True:
            shape = input("What shape would you like it to be?\n 1 = square, 2 = circle, 3 = star\
, 4 = right triangle, 5 = left triangle, 6 = tick\n")
            try:
                if (0 < int(shape) < 7):
                    target["shape"] = str(shape)
                    gettingData = False
                else:
                    print("Sorry, you need in input a number from 1 to 6")
            except:
                print("Sorry, you must input a number from 1 to 6")

        #Get the label for this dataset
        gettingData = True
        while gettingData == True:
            label = input("What label would you like it to use?\n")
            target["label"] = str(label)
            gettingData = False

        #Get the colour of this dataset
        gettingData = True
        while gettingData == True:
            fieldColour = input("What colour would you like it to be?\n")
            target["fieldColour"] = str(fieldColour)
            gettingData = False

        #Add the dataset dictionary to the targets list
        targets.append(target)


    #Process the tree sequences, put into tree_seqs
    tree_seqs = []
    print("Opening the trees FASTA file\n")
    #Open the query (multi-)FASTA file
    with open(inputFile, "r") as file:
        data = file.readlines()

        #Add the header of each seq to a dictionary and append that to a list called
        #"tree_seqs"

        for line in data:
            if(line[0] == ">"):
                tree_seqs.append({"header":line.replace("\n", "")})

        #Extract organism names from the headers and append to an element in the
        #dictionary called "name"
        for organism in tree_seqs:
            header = organism["header"]
            nameStart = header.find("[")
            nameEnd = header.find("]", nameStart)
            name = header[nameStart+1:nameEnd]
            #Clean up any whitespace characters
            name = name.replace("\n", "")
            name = name.replace("\r", "")
            name = name.replace("\t", "")
            #Append all of this to the organism's dictionary
            organism["name"] = name

    for target in targets:
        print("Opening the FASTA file\n")
        #Open the query (multi-)FASTA file
        with open(target["file"], "r") as file:
            data = file.readlines()

        names = []
        #If the line is a header:
        for line in data:
            if(line[0] == ">"):
            #Extract organism names from the headers and append to an element in the
            #dictionary called "name"
                nameStart = line.find("[")
                nameEnd = line.find("]", nameStart)
                name = line[nameStart+1:nameEnd]
                #Clean up any whitespace characters
                name = name.replace("\n", "")
                name = name.replace("\r", "")
                name = name.replace("\t", "")
                #Append all of this to the organism's dictionary
                names.append(name)
        target["names"] = names


    for organism in tree_seqs:
        organism["present"] = ""
        for target in targets:
            if organism["name"] in target["names"]:
                organism["present"] = organism["present"] + ",1"
            else:
                organism["present"] = organism["present"] + ",0"

    #####################
    # OUTPUT FORMATTER  #
    #####################


    gettingLocation = True
    while (gettingLocation == True):
        print("\nPlease select an output location: ")
        #Get a file location, set as inputFASTALocation
        outputLocation = filedialog.asksaveasfilename()
        #Try to open the file, if successful set as FASTAData
        try:
            test = open(outputLocation,"w")
            gettingLocation = False
            #If opening the file fails alert the user and try again
        except IOError:
            print("Sorry, I'm unable to open that file location.")

    print("Outputting data to " + outputLocation)
    with open(outputLocation, "w") as file:
        #Print the boilerplate necessary for the colour range file
        file.write("DATASET_BINARY\n")
        file.write("SEPARATOR COMMA\n")
        file.write("DATASET_LABEL, " + datasetLabel + "\n")
        file.write("COLOR," + colour + "\n")


        line = "FIELD_SHAPES"
        for target in targets:
            line += "," + target["shape"]
        line += "\n"
        file.write(line)

        line = "FIELD_LABELS"
        for target in targets:
            line += "," + target["label"]
        line += "\n"
        file.write(line)

        line = "FIELD_COLORS"
        for target in targets:
            line += "," + target["fieldColour"]
        line += "\n"
        file.write(line)

        file.write("DATA\n")
    
        for organism in tree_seqs:
            header = organism["header"]
            headerEnd = header.find(" ")
            header = header[:headerEnd]
            header = header.replace(">", "")
            file.write(header + organism["present"] + "\n")

    print("Done!")
#taxonomy_range()
binary_annotation()
