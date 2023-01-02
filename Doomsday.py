#from _typeshed import StrPath
from datetime import date as d,timedelta as t, datetime as dt
import random as r
from numpy import MAY_SHARE_BOUNDS
import pyttsx3
import doomsdayFuncs.highscore as hs
import os
import doomsdayFuncs.streak as st

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
    endOfCentury = md.year % 100 == 0
    divisibleBy400 = md.year % 400 == 0
    if endOfCentury:
        if divisibleBy400:
            return True
        else:
            return False
    else:
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
              2:0}
        day = dd[md.month] + adjust
    
    strDate = str(md.month) + '/' + str(day)
    return md.month, day, strDate

def fix_7s(total):
    if total < 0:
        addor = abs(total)//7 * 7 + 7
        newTotal = total + addor
        print(F'{total} + {addor} is {newTotal}')
        return newTotal
    if total > 7:
        sevens = int(total / 7)
        subtractor = sevens * 7
        newTotal = total - subtractor
        print(f'{total} - {subtractor} = {newTotal}')
        return newTotal
    return total

def printExplanation(dateParts, mysteryDate, dayDict):

    print(f'\nThe day you are trying to find is {mysteryDate.strftime("%B %d, %Y")}')
    if isLeapYear(mysteryDate):
        print('This is a leap year')
    doomsday = calculateDoomsDay(mysteryDate)
    print(f'The Doomsday for {mysteryDate.strftime("%B")} is {doomsday[2]}, so we subtract {doomsday[1]}')
    print(f"Mystery Date({dateParts['day']}) minus the doomsday({doomsday[1]}) is {dateParts['day'] - doomsday[1]}")
    total = dateParts['day'] - doomsday[1]
    total = fix_7s(total)

    centuryAnchor = dayDict[getCenturyAnchor(dateParts['year'])[1]]
    print(F'\nCentury is {(dateParts["year"] // 100)} so century Anchor is {centuryAnchor}')
    print(f'{total}(previous total) + {centuryAnchor}(Century Anchor) is {total + centuryAnchor}')
    total = fix_7s(total + centuryAnchor)
    
    yearinCentury = getCenturyRemainder(dateParts['year']) 
    twelvePart = yearinCentury//12*12
    numOfTwelves = yearinCentury//12
    additionalYears = yearinCentury - twelvePart
    leaps = additionalYears//4

    print(F"\nYear in century is {yearinCentury}")
    print(f'so the closest 12 is {twelvePart} which is {numOfTwelves} to previous total({total}) is {numOfTwelves + total}')
    total = fix_7s(numOfTwelves + total)

    if additionalYears > 0:
        print(f'plus the additional {additionalYears} years is {additionalYears + total}')
        total = fix_7s(additionalYears + total)

    if leaps > 0:
        print(f'plus {leaps} leap years is {total + leaps}')
        total = fix_7s(total + leaps)
    print(mysteryDate.strftime('%A'))
    
def getNumOfTrys():
    success = False
    while not success:
        numOfTrys = input("Number of questions?:")
        try:
            numOfTrys = int(numOfTrys)
            success = True
        except:
            print("\nMust be an integer, try again.\n")
            success = False
    return numOfTrys



if __name__ == '__main__':

    tts = pyttsx3.init()
    while True:
        os.system("cls")
        print("\nDOOMSDAY")
        print("--------\n")
        score = 0
        count = 0
        miss = 0
        level = pick_a_level()
        numOfTrys = getNumOfTrys()
        baseScore = level * 10
        #LowestHighScore = hs.getData()[-1]['Score']
        streak = st.getCurrentStreak()
        print(f'Your current streak is {streak}')
        for trynum in range(numOfTrys):
            print(f'Score: {score} Count: {count}/{count + miss}')    
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
                streak += 1
            else:
                print(f"\nNo, it's a {mDayOfWeek}")
                tts.say(f"\nNo, it's a {mDayOfWeek}\n")
                print(mysteryDate.strftime("%B %d, %Y"))
                printExplanation(dateParts,mysteryDate, dayDict)
                miss += 1  
                streak = st.breakStreak(tts,streak)
                

        st.saveStreak(streak)
        tts.say(f"\nYour current streak is {streak}")
        tts.runAndWait()
        
        #highscores = hs.getData()
        #highscores = hs.compareScores(highscores,score)
        #highscores = hs.sortScores(highscores)
        #hs.writeData(['Name', 'Score'],highscores)
        #print(f"\nFinal Score: {score}, Final Count:{count} out of {count + miss}")
        print(f"Percentage = {(count/(count+miss)):.1%}")
        #if input("Print high scores? (y/n)").upper() == 'Y':
        #    hs.printHighscores(highscores,score)
        if input("Again(y/n): ").upper()[0] == 'N':
            break

