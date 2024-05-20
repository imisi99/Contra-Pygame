# Contra-Pygame
This is an objective game built using pygame and pyinstaller.  
The game requires the player to kill all the enemies on the map while avoiding being killed by them  
The project can be cloned [here](https://github.com/imisi99/Contra-Pygame)    
What the game entails:
 - The game can be played by using the keyboard buttons
 - Players can move the avatar anywhere on the screen to avoid the enemies that can attack by shooting
 - Players can attack by pressing the space bar key which causes the player to shoot
 - There is a total of 10 life for a player in the beginning of the game but this can go down: 
   - If any enemy successfully performs his attack, and it makes contact with the player there is a single life deduction
 - Throughout the event of the game the player can have a max of 10 life only
    -
 - Once a plyer life is below zero then it is game-over for the player and the player can do the following:
   - Press the p button to restart the game.
   - Press the q button to quit the game .
 - If a player successfully reaches the ending of the game, That is if the player successfully defeats all the enemy he can decide to play again by pressing p.
 - There is a guide on how to play the game displayed on the screen for a brief second in the beginning of the game 

The game has been made into an executable file using pyinstaller therefore there is no need for any package installation to run the game, It can be downloaded [here](https://github.com/imisi99/Contra-Pygame/blob/main/contra.zip)    
This is the installation Process:
 - After downloading the zip folder extract it to a folder. 
 - After extraction navigate to the app folder and you would find an executable file contra.
 - You can create a shortcut of the game to your desktop for easy access.
 - After extraction the order of the folder should be left as it is as the game depends on all the data and would not run if the order isn't set well.

To run the game on your terminal however you would have to clone the project and run this command on your terminal:
 -      pip install requirements.txt
 -      cd app
 -      python main.py

It was fun creating the game and I hope you enjoy it if you did, you can star the repository
