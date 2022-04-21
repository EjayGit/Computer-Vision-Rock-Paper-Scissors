import math
import time
from random import random
import cv2
from keras.models import load_model
import numpy as np
model = load_model('/home/ejay/Documents/AIS/AiCore/Computer-Vision-Rock-Paper-Scissors/keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
showArr = [0]*30
playerScore = 0
compScore = 0
gameOn = True

# Print the current score and determine comp selection.
def initialise(playerScore, compScore):
    print('Player score = {}'.format(playerScore))
    print('Computer score = {}'.format(compScore))
    # Select R, P or S for the comp.
    tempComputerSelection = int(math.ceil(3 * random()))
    if tempComputerSelection == 1:
        computerSelection = 'Rock'
    elif tempComputerSelection == 2:
        computerSelection = 'Paper'
    elif tempComputerSelection == 3:
        computerSelection = 'Scissors'
    else:
        print('Error Line 20')
    return tempComputerSelection, computerSelection

# Inform the user that the comp is ready, and that the user should place their hand in front of the camera in 3, 2, 1, now...
def countdown():
    print('The computer is ready to play... Get ready to show!!!')
    time.sleep(2)
    for i in range(3,0,-1):
        print('Ready in {}'.format(i))
        time.sleep(1)
    print('SHOW!!!')

# Acquire hand gesture.
def getSelection(cap, model, showArr, data):
    for i in range(0,30): 
        ret, frame = cap.read()
        resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
        image_np = np.array(resized_frame)
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
        data[0] = normalized_image
        prediction = model.predict(data)
        if prediction[0][0]>0.5:
            showArr[i] = 1
        elif prediction[0][1]>0.5:
            showArr[i] = 2
        elif prediction[0][2]>0.5:
            showArr[i] = 3
        else:
            showArr[i] = 4
    # Record the most popular selection from the list from 30 samples.
    showArrAvg = int(math.ceil(sum(showArr) / len(showArr))) # This records the mean (rounded), however this is not correct for the discrete variables. It should be mode, but I havent spent time dealing with the inevitable errors.
    if showArrAvg == 1:
        humanSelection = 'Rock'
    elif showArrAvg == 2:
        humanSelection = 'Paper'
    elif showArrAvg == 3:
        humanSelection = 'Scissors'
    else:
        humanSelection = 'nothing?! You didnt show your hand clearly enough!! Cheeky!'
    return showArrAvg, humanSelection

# Test to find the winner of the round. -> List of tuples
def test(showArrAvg, tempComputerSelection):
    if (showArrAvg == 1 and tempComputerSelection == 2):
        winner = 2
    elif (showArrAvg == 1 and tempComputerSelection == 3):
        winner = 1
    elif (showArrAvg == 2 and tempComputerSelection == 1):
        winner = 1
    elif (showArrAvg == 2 and tempComputerSelection == 3):
        winner = 2
    elif (showArrAvg == 3 and tempComputerSelection == 1):
        winner = 2
    elif (showArrAvg == 3 and tempComputerSelection == 2):
        winner = 1
    else:
        winner = 3
    return winner

# State the winner of the round and determine if there is a game winner. Inform human.
def winnerIs(computerSelection, humanSelection, playerScore, compScore, gameOn, winner):
    # Determine who has won the round.
    print('The computer chose {}'.format(computerSelection))
    print('You chose {}'.format(humanSelection))
    
    # State whom has won the round and let the human determine when the game continues with a key press.
    if winner == 1:
        print('Congratulation! You won!')
        input('Press any key to continue!')
        playerScore = playerScore + 1
    elif winner == 2:
        print('Unlucky, the computer beat your ass to the ground... haha.')
        input('Press any key to continue!')
        compScore = compScore + 1
    else:
        print("It's a draw!!!")
        input('Press any key to continue!')
    
    # If human wins, state won, and ask to play again or quit.
    if playerScore == 2:
        replay = input("You won the game! Would you like to play again?").lower()
        if (replay == "y" or replay == "yes"):
            playerScore = 0
            compScore = 0
        else:
            gameOn = False
    
    # If comp wins, state lost, and ask to play again or quit.
    if compScore == 2:
        replay = input("You lost the game! Would you like to play again?").lower()
        if (replay == "y" or replay == "yes"):
            playerScore = 0
            compScore = 0
        else:
            gameOn = False
    return gameOn, playerScore, compScore
    
while gameOn:
    (tempComputerSelection, computerSelection) = initialise(playerScore, compScore)
    countdown()
    (showArrAvg, humanSelection) = getSelection(cap, model, showArr, data)
    winner = test(showArrAvg, tempComputerSelection)
    (gameOn, playerScore, compScore) = winnerIs(computerSelection, humanSelection, playerScore, compScore, gameOn, winner)
