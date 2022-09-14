import os

def completeCommand(command):
    command = command.replace(' ', '\ ')
    command = command.replace('(','\(')
    command = command.replace(')','\)')
    command = command.replace('&','\&')
    command = command.replace("'","\\'")
    command = 'open ' + command
    return command

constPath = '/Users/aavar/Music/Music/Media.localized/Apple Music/'
artistDirectory = os.listdir(constPath)

# Find titles that contain the passed in word
# Lists all potential songs to terminal
# User selects the intended song by choosing that song's associated
#   number in the list
# '.DS_Store' will interfere, all occurances of '.DS_Store' are ignored
def findSong(wordInSong):
    artist = ''
    potentialSongsList = []

    for artist in artistDirectory:

        if artist != '.DS_Store':
            albumDirectory = os.listdir(constPath + artist)

            for album in albumDirectory:

                if album != '.DS_Store':
                    songDirectory = os.listdir(constPath + artist + '/' + album)

                    for song in songDirectory:

                        if wordInSong.lower() in song.lower():
                            potentialSongsList.append(artist + '/' + album + '/' + song)

    if len(potentialSongsList) == 0:
        print('No songs found')
        print()

    else:
        for songPossibility in range(len(potentialSongsList)):
            print(" {}. {}".format(songPossibility + 1, potentialSongsList[songPossibility]))

        numInput = input("Input the number corresponding with the intended song: ")
        numInputIsInt = False

        try:
            numInput = int(numInput)
            numInputIsInt = True
            
        except ValueError:
            print("You did not enter a valid input.")
            print()

        if numInputIsInt:

            if (numInput < 1 or numInput > len(potentialSongsList)):
                print("You did not enter a valid input.")
                print()

            else:
                command = constPath + potentialSongsList[numInput - 1]
                command = completeCommand(command)
                print(potentialSongsList[numInput - 1])
                print()
                return os.system(command)

def play():
    inp = ''
    print()
    print('Enter a word or phrase in the title of the intended song to play, or \'exit\' to exit.')
    print()
    while inp != 'exit':
        inp = input()
        if inp == 'exit':
            break
        findSong(inp)











#


