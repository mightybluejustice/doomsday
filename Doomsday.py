#from _typeshed import StrPath
from datetime import date as d,timedelta as t, datetime as dt
import random as r
import pyttsx3
import doomsdayFuncs.highscore as hs


oneMinute = t(minutes=1)
dayDict = {'Sunday':0,
           'Monday':1,
           'Tuesday':2,
           'Wednesday':3,
           'Thursday':4,
           'Friday':5,
           'Saturday':6}

def pick_a_date(level):
    while True:
        today = d.today()
        if level == 1:
            year = today.year
        elif level == 2:
            year = r.randint(1900,2100)
        elif level == 3:
            year = r.randint(1800,2199)
        elif level == 4:
            year = r.randint(0,9999)
        day = r.randint(1,31)
        month = r.randint(1,12)
    
        try:
            mysteryDate = d(year,month,day)
            break
        except:
            pass
    return mysteryDate, {'month':month,'day':day,'year':year}

def isDay(guess):
    ''' Tests if users guess is day of the week
        Returns True or False
    '''
    days = ['Sunday','Monday','Tuesday','Wednesday','Thursday',
            'Friday','Saturday']
    if guess.title() in days:
        return True
    else:
        return False
    
def getGuess(mysteryDate):
    '''Gets a guess from the user in the form of a day of 
       the week.
       Returns guess with first letter capitalized
    '''
    while True:
        tts.say(mysteryDate.strftime("%B %d, %Y"))
        tts.runAndWait()
        guess = input('?' + ': ')
        print(guess)
        if isDay(guess):
            break
        elif guess[0].upper() == 'A':
            pass
        else:
            print('Not a day of the week')
            print('Try Again...')
    return guess.title()

def pick_a_level():
    '''Asks user to input level
       Returns level picked
    '''
    while True:
        level = input("Level 1-4: ")
        if isLevel(level):
            level = int(level)
            break
        else:
            print("Not a level. Please pick level 1 - 4: ")
    return level

def isLevel(level):
    ''' Tests if level is '1' or '2'
        Returns True or False
    '''
    answer = True
    if level not in ['1','2','3','4']:
        answer = False
    return answer

def getCenturyAnchor(year):
    century = year//100
    anchorKey = century % 4
    anchor = {0:'Tuesday',
              1:'Sunday',
              2:'Friday',
              3:'Wednesday'}
    return anchorKey,anchor[anchorKey]

def getCenturyRemainder(year):
    century = (year//100) * 100
    return year - century

def isLeapYear(md):
    centuryRemainder = getCenturyRemainder(md.year)
    if centuryRemainder % 4 == 0:
        return True
    else:
        return False

def calculateDoomsDay(md):
    '''input mysteryDate (md)
       Return doomsday
    '''
    if md.month > 3 and md.month % 2 == 0:
        day = md.month
    elif md.month == 3:
        day = 14
        date = '3/14'
    elif md.month in [9,5,7,11]:
        store = {9:5,
                 5:9,
                 7:11,
                 11:7}
        day = store[md.month]
    else:
        if isLeapYear(md):
            adjust = 1
        else:
            adjust = 0
        dd = {1:3,
              2:28}
        day = dd[md.month] + adjust
    
    strDate = str(md.month) + '/' + str(day)
    return md.month, day, strDate

def printExplanation(dateParts):
    centuryAnchor = getCenturyAnchor(dateParts['year'])
    centuryRemainder = getCenturyRemainder(dateParts['year'])
    centuryPart = centuryRemainder//12*12
    centuryPartRemainder = centuryRemainder-centuryPart

    print(F'Century is {(dateParts["year"] // 100)} so century Anchor is {centuryAnchor[1]} which is a {dayDict[centuryAnchor[1]]}')
    print(F"Year in century is {centuryRemainder}\n")

    print(F"Begin with {dayDict[centuryAnchor[1]]}")
    print(F"Add centry part ({centuryPart}) which is {centuryRemainder//12}. ({dayDict[centuryAnchor[1]]} + {centuryRemainder//12} = {dayDict[centuryAnchor[1]] + centuryRemainder//12})")
    carry = dayDict[centuryAnchor[1]] + centuryRemainder//12
    print(F"Plus {centuryPartRemainder} to make ({centuryRemainder}) is {centuryPartRemainder + carry}")
    carry += centuryPartRemainder
    print(F"Plus {centuryPartRemainder//4} leapyears is {carry + centuryPartRemainder//4}")
    carry += centuryPartRemainder//4
    print(F"Remove the Sevens is {carry%7}")
    mMonth,mDay,strDate = calculateDoomsDay(mysteryDate)
    print(F"\nFor {mysteryDate.strftime('%m/%d')} the doomsday is {strDate}")   

if __name__ == '__main__':
    tts = pyttsx3.init()
    while True:
        print('\n'*100)
        score = 0
        count = 0
        level = pick_a_level()
        baseScore = level * 10
        LowestHighScore = hs.getData()[-1]['Score']
        print(f'The score to beat is {LowestHighScore}')
        while True:
            print(f'Score: {score} Count: {count}')    
            mysteryDate, dateParts = pick_a_date(level)
            mDayOfWeek = mysteryDate.strftime('%A')
            startTime = dt.now()
            guess = getGuess(mysteryDate)
            endTime = dt.now()
            if guess == mDayOfWeek:
                speed = endTime-startTime
                print('Yes! You win!', (speed))
                ratio = speed / oneMinute if speed / oneMinute < 1 else 1
                score += int(round(baseScore - baseScore * ratio,0))
                score = int(round(score,0))
                count += 1
            else:
                tts.say(f"\nNo, it's a {mDayOfWeek}\n")
                tts.say(f"\nYour final score is {score}")
                tts.runAndWait()
                print(f"\nNo, it's a {mDayOfWeek}")
                print(mysteryDate.strftime("%B %d, %Y"))             
                #printExplanation(dateParts)
                highscores = hs.getData()
                highscores = hs.compareScores(highscores,score)
                highscores = hs.sortScores(highscores)
                hs.writeData(['Name', 'Score'],highscores)
                print(f"\nFinal Score: {score}, Final Count:{count}")
                if input("Print high scores? (y/n)").upper() == 'Y':
                    hs.printHighscores(highscores,score)
                break
        
        if input("Again(y/n): ").upper()[0] == 'N':
            break

