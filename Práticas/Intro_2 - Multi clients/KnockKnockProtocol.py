class KnockKnockProtocol:
    clues = { "Turnip", "Little Old Lady", "Atch", "Who", "Who" }
    answers = { "Turnip the heat, it's cold in here!", "I didn't know you could yodel!", "Bless you!", "Is there an owl in here?","Is there an echo in here?" }
    state = 0
    theOutput = 0
    NUMJOKES = 5

    def __init__(self):
        global state
        state = 0
        global NUMJOKES
        NUMJOKES = 5
        global currentJoke
        currentJoke = 0
        global theOutput
        theOutput = 0
        global clues
        clues = [ "Turnip", "Little Old Lady", "Atch", "Who", "Who" ]
        global answers
        answers = [ "Turnip the heat, it's cold in here!", "I didn't know you could yodel!", "Bless you!", "Is there an owl in here?","Is there an echo in here?" ]

    def processInput(self,theInput):
        global theOutput
        global state
        global clues
        global answers
        global currentJoke
        global NUMJOKES


        if (state == 0):
            theOutput = "Knock! Knock!"
            state = 1
        else:
            if (state == 1):
                if (theInput == "Who's there?"):
                    theOutput = clues[currentJoke]
                    state = 2
                else:
                    theOutput = "You're supposed to say \"Who's there?\"! " + "Try again. Knock! Knock!"

            elif (state == 2):
                if (theInput == (clues[currentJoke] + " who?")):
                    theOutput = answers[currentJoke] + " Want another? (y/n)"
                    state = 3;
                else:
                    theOutput = "You're supposed to say \"" + clues[currentJoke] +  " who?\"" + "! Try again. Knock! Knock!"
                    state = 1
            elif (state == 3):
                if (theInput == "y"):
                    theOutput = "Knock! Knock!"
                    if (currentJoke == (NUMJOKES - 1)):
                        currentJoke = 0
                    else:
                        currentJoke += 1
                        state = 1
                else:
                    theOutput = "Bye."
                    state = 0
        return theOutput

    