# --- Chat BOT based on the technology of Markov Chain from 1906 ---

# --- Importing libraries ---
import random

# --- Loading data ---
with open("dataset.txt","r") as file:
    texts = file.readlines()

tokenizedData = []

# --- Splitting the data into invidivual words ---
for sentence in texts:
    sentence = sentence.split(" ")
    for word in sentence:
        tokenizedData.append(word.lower())

keywords = [tokenizedData[0],tokenizedData[1]]
tokenizedData = tokenizedData[2:]

dictionaryData = {}

# --- Turning the split words into a chain ---
for index in range(len(tokenizedData)):
    dictionaryData[f"{keywords[0].lower()}-{keywords[1].lower()}"] = tokenizedData[index]
    del keywords[0]
    keywords.append(tokenizedData[index])

del tokenizedData

# --- Generating text based on the word chain...
while True:
    shell = input(">>>").split(" ")

    if not (len(shell) >= 2) or f"{shell[0].lower()}-{shell[1].lower()}" not in dictionaryData:
        shell = random.choice(list(dictionaryData.keys())).split("-")
        
    keywords = [shell[-2],shell[-1]]
    output = [keywords[0],keywords[1]]

    for i in range(50):
        if not f"{keywords[0].lower()}-{keywords[1].lower()}" in dictionaryData:
            break
                
        output.append(dictionaryData[f"{keywords[0].lower()}-{keywords[1].lower()}"])
        del keywords[0]
        keywords.append(output[-1])

    print(" ".join(output))