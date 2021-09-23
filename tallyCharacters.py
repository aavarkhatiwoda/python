# this program will tally all characters in a string input.
# indifferent of lowercase or uppercase
# characters a-z A-Z, 0-9, space, and others
# will use  decimal 65-90 for 'A' - 'Z' (will convert from default to all uppercase),
#           demical 48-57 for '0' - '9',
#           decimal 32 for 'space',
#           none of the above will result in 'other'

# If a character appeares 0 times, it will be skipped in the final tally output

# ord() converts from character to its dec value
# str() converts from dec value to its character

# 26 characters (a-z and A-Z, indifferent of lowercase of uppercase),
# 10 numbers (0-9),
# 1 space,
# 1 other
# = 38-size list

tallyList = [0]*38
# index 0-25 is a-z A-Z, 26-35 is 0-9, 36 is space, 37 is other

def inputString(stringInput):

    if type(stringInput) is str:

        stringInput = stringInput.upper()

        for char in stringInput:
            if ord(char) >= 65 and ord(char) <= 90:     # ASCII A-Z is 65-90
                tallyList[ord(char)-65] += 1            # shift 65-90 to indices 0-25
            elif ord(char) >= 48 and ord(char) <= 57:   # ASCII 0-9 is 48-57
                tallyList[ord(char)-22] += 1            # shift 48-57 to indices 26-35
            elif ord(char) == 32:                       # ASCII space is 32
                tallyList[36] += 1                      # increment index 35 by 1
            else:
                tallyList[37] += 1                       # any other character will increment index 37 by 1

        for letters in range(26):
            if tallyList[letters] > 0:
                print(chr(letters+65) + ": " + str(tallyList[letters]))

        for numbers in range(10):
            if tallyList[numbers+26] > 0:
                print(chr(numbers+48) + ": " + str(tallyList[numbers+26]))

        if tallyList[36] > 0:
            print("Spaces: " + str(tallyList[36]))

        if tallyList[37] > 0:
            print("Other: " + str(tallyList[37]))

    else:
        print("Not a valid input")


# Edit the stringInput value below to pass in a unique string for tallying
stringInput = "Hello world"
inputString(stringInput)















#
