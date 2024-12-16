--Bounce King--

-About my project-

The game I made is based on the classic ping-pong game. I used Python and the Turtle library to create it. I also added some new features to make it different from the original game.

One big difference is that my game has three modes to play. The first mode is Practice Mode, where players can practice and learn how to play. The second mode is Normal Mode, which is a little harder and more fun for players who want more challenge. The third mode is Master Mode, which is the hardest mode for players who want the biggest challenge.

Each mode is different because the number of balls and items change. In Normal Mode, there are three items, just like Practice Mode, but in Master Mode, there is one more special item to make it more challenging.

The game also has a high score system. It saves the highest score for each mode, so players can try to beat the top score.

-UML-
![UMLDiagram](https://github.com/user-attachments/assets/506713ab-a5ad-48c2-b39e-8b411c255aaa)



-How to install/run -

1.Fork this repo to your GitHub

2.Clone it to your folder

3.Open the folder and click run Main_1.py

-Usage-

For this game, I will use the arrow keys to control it. The up and down arrow keys will be used to select the game mode, and the Enter key will be used to choose the mode. When we select the mode we want, an arrow will point to it, and if we want to play that mode, we can press Enter to start.
After entering the selected mode, we will use the left and right arrow keys to move. These keys will control the player’s movement during the game.

1.The Ball class is responsible for managing the balls in the game. It includes properties and behaviors related to the movement and collision of the balls.

2.The Paddle class acts as the paddle that players control to hit the balls. It allows the player to move the paddle left and right to intercept the balls.

3.The BouncingSimulator class serves as the main game controller. It handles the creation of balls, the paddle, collision management, and updates the overall game environment.

-Use/Extend/Modify the code -
1. Score System
 • Added a scoring system where points increase when the ball hits the paddle.
 • Bonus points are given if a special effect is active.
 • Points decrease if a non-main ball hits the paddle.
 • The score is displayed on the screen during the game.
 2. High Score System
 • High scores are saved in a file called highscore.dat.
 • If the player’s score is higher than the saved high score, it updates the file.
 • Each game mode (Practice, Normal, Hard) tracks its own high score.
 3. Keyboard Controls
 • Added Menu_UP, Menu_DOWN, Menu_ENTER functions to navigate and select options in the game menu.
 • The arrow keys control the paddle’s movement (left and right).
 • The Enter key selects the game mode.
 4. User Interface (UI) Improvements
 • Added a visual menu system with a cursor to choose game modes.
 • The current score is displayed at the top of the screen.
 • A border was added around the playing area for better visibility.
 5. Special Effects
 • Added special effects to increase score bonuses.
 • Effects may change ball behavior, such as speed or appearance.
 6. Ball Customization
 • Added logic to distinguish the main ball from other balls using ID.
 • Non-main balls reduce the score if they hit the paddle.
 • Customizations like ball color, speed, and size were added.
 7. Paddle Customization
 • Paddle movement is controlled using left and right arrow keys.
 • The paddle’s position, size, and color were customized.
 8. Game Modes
 • Added 3 game modes: Practice, Normal, Hard.
 • Each mode has different difficulty settings, such as ball speed or the number of balls.
 9. Event Handling
 • Added keyboard event handlers for paddle movement and menu navigation.
 • Improved event handling for ball collisions with walls, the paddle, and other balls.


-Description/Bugs known to be resolved -

My Testing Method
Since my game has multiple modes, I play each mode twice every time I make changes to the code. This allows me to compare the results from each playthrough and identify any issues or inconsistencies.

Bugs Found
    
Paddle Movement Bug

•    Problem: When moving the paddle using the left and right arrow keys, sometimes the paddle remains stuck in its position.

•    How I Discovered It: I found this issue after adding a new item — a “bomb” item — that ends the game instantly when triggered. I noticed that when I moved the paddle away from the ball, but the ball landed in the zone where the paddle previously was, the game ended as if the paddle was still there. This made it clear that there was a bug related to paddle position tracking.

Ball Overlapping at the Start

•    Problem: When the game starts, some balls may overlap with each other, causing them to collide immediately.

•    How I Discovered It: I observed that sometimes when the game starts, balls collide right away. This is likely caused by the calculation formula for the initial ball positions, which might not create enough space between the balls.

Frame Rate Issue

•    Problem: The frame rate affects the speed of the ball, leading to different gameplay speeds on different devices.

•    How I Discovered It: I tested the game on both my MacBook and my Windows desktop. The screen on my Windows desktop runs at 120 to 144 Hz, while the MacBook runs at 60 Hz. As a result, the ball moves much faster on Windows compared to Mac.

•    Solution: To make the game run at a consistent speed across devices, I need to adjust the refresh rate (Hz) in the code to ensure consistent gameplay regardless of the screen’s refresh rate.
These are the key bugs I found and how I identified them.

-Sophistication level: 80 -

For my project, it is rated at 80.
A Pong game with more balls and more paddles

This is because my project builds upon the solid foundation of a Ping Pong game. I have enhanced it by creating a user interface that includes a login system, a game mode selection screen, and a leaderboard displaying the highest scores achieved by players in each mode. Additionally, the game system features special effects designed to increase the challenge and excitement for players.
