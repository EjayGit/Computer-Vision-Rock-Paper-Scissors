from ast import If
import math
import time
from random import random
import cv2
from keras.models import load_model
import numpy as np
model = load_model('d:\AIS\AiCore\Rock Paper Scissors\converted_keras\keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
showArr = [0]*30
playerScore = 0
compScore = 0

while True:
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

    # Inform the user that the comp is ready, and that the user should place their hand in front of the camera in 3, 2, 1, now...
    print('The computer is ready to play... Get ready to show!!!')
    time.sleep(2)
    for i in range(3,0,-1):
        print('Ready in {}'.format(i))
        time.sleep(1)
    print('SHOW!!!')

    for i in range(0,30): 
        ret, frame = cap.read()
        resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
        image_np = np.array(resized_frame)
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
        data[0] = normalized_image
        prediction = model.predict(data)
        #cv2.imshow('frame', frame)
        # Press q to close the window
        if prediction[0][0]>0.5:
            showArr[i] = 1
        elif prediction[0][1]>0.5:
            showArr[i] = 2
        elif prediction[0][2]>0.5:
            showArr[i] = 3
        else:
            showArr[i] = 4
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # After the loop release the cap object
    #cap.release()
    # Destroy all the windows
    #cv2.destroyAllWindows()

    # Record the most popular selection from the list from 30 samples.
    showArrAvg = int(math.ceil(sum(showArr) / len(showArr)))
    if showArrAvg == 1:
        humanSelection = 'Rock'
    elif showArrAvg == 2:
        humanSelection = 'Paper'
    elif showArrAvg == 3:
        humanSelection = 'Scissors'
    else:
        humanSelection = 'You didnt show your hand clearly enough!! Cheeky!'

    if (showArrAvg == 1 and tempComputerSelection == 1):
        winner = 3
    elif (showArrAvg == 1 and tempComputerSelection == 2):
        winner = 2
    elif (showArrAvg == 1 and tempComputerSelection == 3):
        winner = 1
    elif (showArrAvg == 2 and tempComputerSelection == 1):
        winner = 1
    elif (showArrAvg == 2 and tempComputerSelection == 2):
        winner = 3
    elif (showArrAvg == 2 and tempComputerSelection == 3):
        winner = 2
    elif (showArrAvg == 3 and tempComputerSelection == 1):
        winner = 2
    elif (showArrAvg == 3 and tempComputerSelection == 2):
        winner = 1
    elif (showArrAvg == 3 and tempComputerSelection == 3):
        winner = 3
    else:
        winner = 3


    # Determine who has won.
    print('The computer chose {}'.format(computerSelection))
    print('You chose {}'.format(humanSelection))
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
    
    if playerScore == 3:
        # Ask to play again or quit.
        replay = input("You won the game! Would you like to play again?").lower()
        if (replay == "y" or replay == "yes"):
            playerScore = 0
            compScore = 0
            continue
        else:
            break
    
    if compScore == 3:
        # Ask to play again or quit.
        replay = input("You lost the game! Would you like to play again?").lower()
        if (replay == "y" or replay == "yes"):
            playerScore = 0
            compScore = 0
            continue
        else:
            break
    