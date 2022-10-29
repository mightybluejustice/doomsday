def getCurrentStreak():
    with open('doomsdayFuncs\streak.txt','r') as file:
        streak = file.read()
        streak = int(streak)
    return streak


def breakStreak():
    with open('doomsdayFuncs\streak.txt','w') as file:
        file.write('0')
    return 0

def saveStreak(streak):
    with open('doomsdayFuncs\streak.txt','w') as file:
        file.write(str(streak))

