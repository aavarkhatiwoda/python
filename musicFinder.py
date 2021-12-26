# FOR MAC ONLY:
    # The song must be downloaded through Apple Music on Mac.
    # change the computer name in constPath to your Mac's name
    # from terminal go to the file's directory and run the file through the
    # commands:
        # python3
        # from musicFinder import play
        # play()
    # from now on, just type in any substring of the song,
    # or any substring of the song, ' by ', and any substring of the artist,
    # or 'exit' to exit.
    
    # If any songs or artists have a forward slash, replace this with an underscore.
    

import os

def completeCommand(command):
    command = command.replace(' ', '\ ')
    command = command.replace('(','\(')
    command = command.replace(')','\)')
    command = command.replace('&','\&')
    command = command.replace("'","\\'")
    command = 'open ' + command
    return command


# The parameter input is the command in the format
    # X by Y
    # where X is the song and Y is the artist
# X can be a substring of the song name, ex: 'Rolling in' for
    # 'Rolling in the Deep'
# Y can be a substring of the artist, ex: "Ade" for "Adele"
    # The input doesn't consider capitalization
def findSong(input):

    # replace /aavar/ with the name of your computer. Upon opening terminal,
        # it is the text before the @, ex: aavar@aavars-MBP
    constPath = '/Users/aavar/Music/Music/Media.localized/Apple Music/'
    artistDirectory = os.listdir(constPath)
    potentialSongs = []
    compilationsPotentialSongs = []

    # X by Y format where X = song substring and Y = artist substring
    if 'by' in input:
        inputDivider = input.index('by')
        inputSong = input[:inputDivider-1]
        inputArtist = input[inputDivider+3:]
    else:
        inputSong = input # If just X is given
        inputArtist = ''

    for i in artistDirectory:
        if i != '.DS_Store':
            albumDirectory = os.listdir(constPath + i)
            for j in albumDirectory:
                if j != '.DS_Store':
                    songDirectory = os.listdir(constPath + i + '/' + j)
                    for k in songDirectory:
                        if inputSong.lower() in k.lower():
                            if i != 'Compilations':
                                potentialSongs.append(i + '/' + j + '/' + k)
                            else:
                                compilationsPotentialSongs.append(i + '/' + j + '/' + k)

    if len(compilationsPotentialSongs) > 0:
        command = constPath + compilationsPotentialSongs[0]
        command = completeCommand(command)
        print(compilationsPotentialSongs[0])
        print()
        return os.system(command)
    if len(potentialSongs) == 0:
        print('No songs found')
    elif len(potentialSongs) == 1:
        command = constPath + potentialSongs[0]
        command = completeCommand(command)
        print(potentialSongs[0])
        print()
        return os.system(command)
    else:
        for i in potentialSongs:
            fullArtistUntil = i.index('/')
            fullArtist = i[:fullArtistUntil]
            # will return first instance of inputArtist substring in fullArtist
            if inputArtist.lower() in fullArtist.lower():
                command = constPath + i
                command = completeCommand(command)
                print(i)
                print()
                return os.system(command)
        print('Song not associated with artist or not enough information given')



def play():
    inp = ''
    print()
    print('X, X by Y, or \'exit\'. X = song substring, Y = artist substring.')
    print()
    while inp != 'exit':
        inp = input()
        if inp == 'exit':
            break
        findSong(inp)





#
