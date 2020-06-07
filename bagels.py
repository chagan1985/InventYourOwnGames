import random

NUM_DIGITS = 3
MAX_GUESS = 10

def getSecretNumber():
    # Returns a string of a unique random digits that is NUM_DIGITS long.
    numbers = list(range(10))
    random.shuffle(numbers)
    secretNum = ''
    for i in range(NUM_DIGITS):
        secretNum += str(numbers[i])
    return secretNum

def getClues(guess, secretNum):
    # Returns a string with the Pico, Fermi & Bagels clues to the user.
    if guess == secretNum:
        return 'You got it!'

    clues = []
    for i in range(len(guess)):
        if guess[i] == secretNum[i]:
            clues.append('Fermi')
        elif guess[i] in secretNum:
            clues.append('Pico')
    if len(clues) == 0:
        return 'Bagels'

    clues.sort()
    return ' '.join(clues)

def isOnlyDigits(num):
    # Returns True if num is a string of only digits. Otherwise, returns False.
    if num == '':
        return False

    for i in num:
        if i not in '0 1 2 3 4 5 6 7 8 9'.split():
            return False

    return True

print('I am thinking of a {}-digit number. Try to guess what it is.'.format(MAX_GUESS))
print('The clues I give are...')
print('When I say:      That means:')
print(' Bagels          None of the digits are correct.')
print(' Pico            One digit is correct but in the wrong position.')
print(' Fermi           One digit is correct and in the right position.')

while True:
    secretNum = getSecretNumber()
    print('I have thought up a number. You have {} guesses to get it.'.format(NUM_DIGITS))

    guessesTaken = 1
    while guessesTaken <= MAX_GUESS:
        guess = ''
        while len(guess) != NUM_DIGITS or not isOnlyDigits(guess):
            print('Guess #{}:'.format(guessesTaken), end = '')
            guess = input()

        print(getClues(guess, secretNum))
        guessesTaken += 1

        if guess == secretNum:
            break
        if guessesTaken > MAX_GUESS:
            print('You ran out of guesses. The answer was {}.'.format(secretNum))

    print('Do you want to play again? (Yes or No)')
    if not input().lower().startswith('y'):
        break
