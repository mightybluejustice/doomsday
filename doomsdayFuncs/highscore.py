import csv

dataHeaders = ['Name', 'Score']
data = [{'Name':'Brad', 'Score':0},
        {'Name':'Angie', 'Score':100}]

def getData():
    '''
    Imports list of highScores, returns a list of dictionaries
    '''
    dictData = []
    with open('doomsdayFuncs/highScores.txt', 'r') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            dictData.append(row)
    return dictData   

def writeData(dataHeaders,data):
    '''
    Saves data to highScores
    '''    
    with open('doomsdayFuncs/highScores.txt', 'w') as csvFile:
        csvWriter = csv.DictWriter(csvFile, fieldnames=dataHeaders)
        
        csvWriter.writeheader()
        csvWriter.writerows(data)

def compareScores(dictData,score):
    '''
    Compares score to high scores in dictData. If score is larger than any in the list,
    asks for your name and adds score to list
    '''
    for index,highScore in enumerate(dictData):
        if score >= int(highScore['Score']) and score != 0:
            print('\nHIGH SCORE!')
            playerName = input('Name: ')
            dictData.append({'Name':playerName, 'Score':score})
            break
    return dictData

def sortScores(dictData):
    '''
    Sort high scores, reduce list to ten items
    returns dictData
    '''
    dictData.sort(key = lambda key: int(key['Score']), reverse=True)
    while len(dictData) > 10:
        dictData.pop()
    return dictData

def printHighscores(highscores,score):
    for index,s in enumerate(highscores):
        print(index + 1, s['Name'],"\t",s['Score'], end = '')
        if score == s['Score']:
            print(' <<')
        else:
            print()

if __name__ == '__main__':
    writeData(dataHeaders, data)
    dictData = getData()

    dictData = compareScores(dictData,0)
    dictData = sortScores(dictData)