import ball
import my_event
import turtle
import random
import heapq
import paddle
import time
from tkinter import messagebox


from datetime import datetime

class BouncingSimulator:
		def __init__(self, num_balls, player_name, Mode):
				
				self.player_name = player_name
				self.score = 0
				self.mode = Mode
				self.CHECK = 0

				#TJ - effect
				self.EFFECT_BALL = []
				self.EFFECT = 0
				self.EFFECT_TIME = None
				self.EFFECT_TIMEOUT = 0
				self.EFFECT_ACTIVE = False
				self.TIMEOUT_LIMIT = 30
				
				self.num_balls = num_balls
				self.ball_list = []
				self.t = 0.0
				self.pq = []
				self.HZ = 4
				turtle.speed(0)
				turtle.tracer(0)
				turtle.hideturtle()
				turtle.colormode(255)
				self.canvas_width = turtle.screensize()[0]
				self.canvas_height = turtle.screensize()[1]

				if self.mode == "NORMAL":
						ball_radius = 0.05 * self.canvas_width
						x = -self.canvas_width + (0+1)*(2*self.canvas_width/(self.num_balls+1))
						y = 0.0
						vx = 10*0.6
						vy = 10*0.6
						ball_color = (255, 0, 0)
						self.ball_list.append(ball.Ball(ball_radius, x, y, vx, vy, ball_color, 0))
						for i in range(1, self.num_balls):
								x = -self.canvas_width + (i+1)*(2*self.canvas_width/(self.num_balls+1))
								y = 0.0
								ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
								while ball_color[0] >= 150:
										ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
										
								self.ball_list.append(ball.Ball(ball_radius, x, y, vx, vy, ball_color, i))
				elif self.mode == "HARD":
						ball_radius = 0.05 * self.canvas_width
						x = -self.canvas_width + (0+1)*(2*self.canvas_width/(self.num_balls+1))
						y = 0.0
						vx = 10*0.4
						vy = 10*0.4
						ball_color = (255, 0, 0)
						self.ball_list.append(ball.Ball(ball_radius, x, y, vx, vy, ball_color, 0))
						for i in range(1, self.num_balls):
								x = -self.canvas_width + (i+1)*(2*self.canvas_width/(self.num_balls+1))
								y = 0.0
								ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
								while ball_color[0] >= 150:
										ball_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
										
								self.ball_list.append(ball.Ball(ball_radius, x, y, vx, vy, ball_color, i))
				else:
						print(" --> Mode: Practice")
						ball_radius = 0.05 * self.canvas_width
						x = -self.canvas_width + (0+1)*(2*self.canvas_width/(self.num_balls+1))
						y = 0.0
						vx = 10*0.4
						vy = 10*0.4
						ball_color = (255, 0, 0)
						self.ball_list.append(ball.Ball(ball_radius, x, y, vx, vy, ball_color, 0))

				self.Player = turtle.Turtle()
				self.Player.penup()
				self.Player.hideturtle()
				self.Player.pencolor((0, 0, 0))
				self.Player.goto(-370, 310)
				self.Player.write(f"Player Name: {self.player_name}", font=('Courier', 24, 'bold'))
				self.Player.goto(180, 310)
				self.Player.write(f"Score: {self.score}", font=('Courier', 24, 'bold'))

				if self.mode == "NORMAL":
						tom = turtle.Turtle()
						self.my_paddle = paddle.Paddle(150, 50, (255, 0, 0), tom)
						self.my_paddle.set_location([0, -150])
				elif self.mode == "HARD":
						tom = turtle.Turtle()
						self.my_paddle = paddle.Paddle(100, 50, (255, 0, 0), tom)		#TJ - adjust HARD - padding witdh
						self.my_paddle.set_location([0, -150])
				else:
						tom = turtle.Turtle()
						self.my_paddle = paddle.Paddle(200, 50, (255, 0, 0), tom)
						self.my_paddle.set_location([0, -150])

				self.screen = turtle.Screen()

				T = datetime.now()
				self.START_TIME = T
				self.START_T = T.second
				self.START_MIN = T.minute

		def random_effect(self):
				ball_radius = 0.03 * self.canvas_width
				x = random.randint(-self.canvas_width+10, self.canvas_width-10)
				y = self.canvas_height - 30
				vx = 0
				vy = -4
				if self.mode == "HARD":
						self.EFFECT = random.randint(1, 4)
				else:
						self.EFFECT = random.randint(1, 3)
				print(f"self.EFFECT:{self.EFFECT}")
				match self.EFFECT:
						case 1:
							ball_color = (255,0,0)
							ball_color2 = (255,255,0)
						case 2:
							ball_color = (0,255,0)
							ball_color2 = (255,0,255)
						case 3:
							ball_color = (0,0,255)
							ball_color2 = (255,255,255)
						case 4:
							ball_color = (0,0,0)
							ball_color2 = (255,0,0)
				self.EFFECT_BALL.append(ball.Ball(ball_radius, x, y, vx, vy, ball_color, 999, ball_color2))

		def __predict(self, a_ball):
				if a_ball is None:
						return

				for i in range(len(self.EFFECT_BALL)):
						if self.EFFECT_BALL[i] != None:
								dt = a_ball.time_to_hit(self.EFFECT_BALL[i])
								# insert this event into pq
								heapq.heappush(self.pq, my_event.Event(self.t + dt, a_ball, self.EFFECT_BALL[i], None))
				for i in range(len(self.ball_list)):
						dt = a_ball.time_to_hit(self.ball_list[i])
						# insert this event into pq
						heapq.heappush(self.pq, my_event.Event(self.t + dt, a_ball, self.ball_list[i], None))

				dtX = a_ball.time_to_hit_vertical_wall()
				dtY = a_ball.time_to_hit_horizontal_wall()
				heapq.heappush(self.pq, my_event.Event(self.t + dtX, a_ball, None, None))
				heapq.heappush(self.pq, my_event.Event(self.t + dtY, None, a_ball, None))
		
		def __draw_border(self):
				turtle.penup()
				turtle.goto(-self.canvas_width, -self.canvas_height)
				turtle.pensize(10)
				turtle.pendown()
				turtle.color((0, 0, 0))   
				for i in range(2):
						turtle.forward(2*self.canvas_width)
						turtle.left(90)
						turtle.forward(2*self.canvas_height)
						turtle.left(90)

		def __redraw(self):
				turtle.clear()
				self.my_paddle.clear()
				self.__draw_border()
				self.my_paddle.draw()
				for i in range(len(self.ball_list)):
						self.ball_list[i].draw()
				#TJ - effect ball
				for i in range(len(self.EFFECT_BALL)):
						if self.EFFECT_BALL[i] != None:
								self.EFFECT_BALL[i].draw()
								if self.EFFECT_BALL[i].y < -300:
										self.EFFECT = 0
										self.EFFECT_BALL[i] = None
				turtle.update()
				heapq.heappush(self.pq, my_event.Event(self.t + 1.0/self.HZ, None, None, None))

		def __paddle_predict(self):
				for i in range(len(self.EFFECT_BALL)):
						if self.EFFECT_BALL[i] != None:
									a_ball = self.EFFECT_BALL[i]
									dtP = a_ball.time_to_hit_paddle(self.my_paddle)
									heapq.heappush(self.pq, my_event.Event(self.t + dtP, a_ball, None, self.my_paddle))
				for i in range(len(self.ball_list)):
						a_ball = self.ball_list[i]
						dtP = a_ball.time_to_hit_paddle(self.my_paddle)
						heapq.heappush(self.pq, my_event.Event(self.t + dtP, a_ball, None, self.my_paddle))

		def move_left(self):
				if (self.my_paddle.location[0] - self.my_paddle.width/2 - 40) >= -self.canvas_width:
						self.my_paddle.set_location([self.my_paddle.location[0] - 40, self.my_paddle.location[1]])
		def move_right(self):
				if (self.my_paddle.location[0] + self.my_paddle.width/2 + 40) <= self.canvas_width:
						self.my_paddle.set_location([self.my_paddle.location[0] + 40, self.my_paddle.location[1]])

		def run(self):
				for i in range(len(self.EFFECT_BALL)):
						if self.EFFECT_BALL[i] != None:
									self.__predict(self.EFFECT_BALL[i])
				for i in range(len(self.ball_list)):
						self.__predict(self.ball_list[i])
				heapq.heappush(self.pq, my_event.Event(0, None, None, None))

				self.screen.listen()
				self.screen.onkeypress(self.move_left, "Left")
				self.screen.onkeypress(self.move_right, "Right")

				old_timer = -1
				old_left_effect = -1

				while (True):
						T = datetime.now()

						diff = (T - self.START_TIME).seconds + 1
						
						if self.EFFECT_TIME != None:
								diff_effect = (T - self.EFFECT_TIME).seconds
								left_effect = self.EFFECT_TIMEOUT - diff_effect
								if left_effect != old_left_effect:
										old_left_effect = left_effect
										self.Player.penup()
										self.Player.goto(-400, -370)
										self.Player.pencolor("white")
										self.Player.fillcolor("white") 
										self.Player.begin_fill() 
										self.Player.pendown()
										self.Player.forward(50)
										self.Player.left(90)
										self.Player.forward(55)
										self.Player.left(90)
										self.Player.forward(50)
										self.Player.left(90)
										self.Player.forward(55)
										self.Player.left(90)
										self.Player.end_fill()
										self.Player.pencolor("green")
										self.Player.goto(-380, -340)
										self.Player.write(f"{left_effect}", font=('Courier', 18, 'bold'), align='right')

								if left_effect <= 0:
										self.EFFECT_ACTIVE = False
										self.EFFECT_TIME = None
										self.Player.penup()
										self.Player.goto(-400, -370)
										self.Player.pencolor("white")
										self.Player.fillcolor("white") 
										self.Player.begin_fill() 
										self.Player.pendown()
										self.Player.forward(50)
										self.Player.left(90)
										self.Player.forward(55)
										self.Player.left(90)
										self.Player.forward(50)
										self.Player.left(90)
										self.Player.forward(55)
										self.Player.left(90)
										self.Player.end_fill()
										

						if T.second >= self.START_T:
								Total_Time = T.second - self.START_T
						else:
								Total_Time = (T.second + 60) - self.START_T

						if random.randint(1, 1000) == 5:
								if self.EFFECT == 0:
										self.random_effect()

						if diff >= self.TIMEOUT_LIMIT:
								print(" --> FINISH")
								self.Player.pencolor((0, 0, 0))
								self.Player.goto(0, 0)
								self.Player.write(f"Total Score: {self.score}", font=('Courier', 48, 'bold'), align='center')

								f = open("highscore.dat", "r")
								high1 = f.readline().strip().split(",")
								high2 = f.readline().strip().split(",")
								high3 = f.readline().strip().split(",")
								f.close()

								if self.mode == "NORMAL":
										if self.score > int(high1[1]):
												high1[0] = self.player_name
												high1[1] = str(self.score)
								if self.mode == "HARD":
										if self.score > int(high2[1]):
												high2[0] = self.player_name
												high2[1] = str(self.score)
								if self.mode == "PRACTICE":
										if self.score > int(high3[1]):
												high3[0] = self.player_name
												high3[1] = str(self.score)
								f = open("highscore.dat", "w")
								f.write(f"{high1[0]},{high1[1]}\n")
								f.write(f"{high2[0]},{high2[1]}\n")
								f.write(f"{high3[0]},{high3[1]}\n")
								f.close()

								self.Player.goto(0, -30)
								self.Player.write(f"name:{self.player_name} mode:{self.mode}  ", font=('Courier', 24, 'bold'), align='center')
								self.Player.goto(-380, -220)
								self.Player.write(f"HIGHSCORE-NORMAL   :: {high1[0]} @{high1[1]}", font=('Courier', 24, 'bold'), align='left')
								self.Player.goto(-380, -255)
								self.Player.write(f"HIGHSCORE-HARD     :: {high2[0]} @{high2[1]}", font=('Courier', 24, 'bold'), align='left')
								self.Player.goto(-380, -290)
								self.Player.write(f"HIGHSCORE-PRACTICE :: {high3[0]} @{high3[1]}", font=('Courier', 24, 'bold'), align='left')
								answer = messagebox.askyesno("Play Again!!", "Want to play game again ?")
								if answer == True:
										Greeting.clear()
										Menu.clear()
										my_simulator = BouncingSimulator(self.num_balls, self.player_name, self.mode)
										my_simulator.run()
								else:
										exit()
								
								break
						
						e = heapq.heappop(self.pq)
						if not e.is_valid():
								continue

						ball_a = e.a
						ball_b = e.b
						paddle_a = e.paddle

						for i in range(len(self.EFFECT_BALL)):
								if self.EFFECT_BALL[i] != None:
											self.EFFECT_BALL[i].move(e.time - self.t)
						for i in range(len(self.ball_list)):
								self.ball_list[i].move(e.time - self.t)
						self.t = e.time

						if (ball_a is not None) and (ball_b is not None) and (paddle_a is None):
								if ball_a.Get_Ball_ID() == 999 or ball_b.Get_Ball_ID() == 999:
										continue
								ball_a.bounce_off(ball_b)
						elif (ball_a is not None) and (ball_b is None) and (paddle_a is None):
								ball_a.bounce_off_vertical_wall()
						elif (ball_a is None) and (ball_b is not None) and (paddle_a is None):
								ball_b.bounce_off_horizontal_wall()
						elif (ball_a is None) and (ball_b is None) and (paddle_a is None):
								self.__redraw()
						elif (ball_a is not None) and (ball_b is None) and (paddle_a is not None):
								if ball_a.Get_VY() > 0:
										continue
								
								ball_a.bounce_off_paddle()
								
								if ball_a.Get_Ball_ID() == 0:
										print(" --> Ball = ", ball_a.Get_Ball_ID())
										if self.EFFECT_ACTIVE:
												self.score = self.score + 10
										else:	
												self.score = self.score + 5
										self.Player.penup()
										self.Player.goto(180, 310)
										self.Player.pencolor("white")
										self.Player.fillcolor("white") 
										self.Player.begin_fill() 
										self.Player.pendown()
										self.Player.forward(200)
										self.Player.left(90)
										self.Player.forward(35)
										self.Player.left(90)
										self.Player.forward(200)
										self.Player.left(90)
										self.Player.forward(35)
										self.Player.left(90)
										self.Player.end_fill()

										self.Player.pencolor((0, 0, 0))
										self.Player.goto(180, 310)
										self.Player.write(f"Score: {self.score}", font=('Courier', 24, 'bold'))
								elif ball_a.Get_Ball_ID() == 999:		#TJ - effect ball
										match self.EFFECT:
												case 1:
														self.EFFECT_ACTIVE = True
														self.EFFECT_TIME = datetime.now()
														self.EFFECT_TIMEOUT = 8
												case 2:
														self.TIMEOUT_LIMIT += 10
												case 3:
														self.TIMEOUT_LIMIT -= 5
												case 4:
														self.TIMEOUT_LIMIT = 0
										
										self.EFFECT = 0
										self.EFFECT_BALL.clear()
										self.Player.penup()
										self.Player.goto(340, -370)
										self.Player.pencolor("white")
										self.Player.fillcolor("white") 
										self.Player.begin_fill() 
										self.Player.pendown()
										self.Player.forward(50)
										self.Player.left(90)
										self.Player.forward(55)
										self.Player.left(90)
										self.Player.forward(50)
										self.Player.left(90)
										self.Player.forward(55)
										self.Player.left(90)
										self.Player.end_fill()
										self.Player.pencolor("red")
										self.Player.goto(380, -340)
										self.Player.write(f"{self.TIMEOUT_LIMIT-diff}", font=('Courier', 18, 'bold'), align='right')
								else:
										print("NONE=", i)
										
										if not self.EFFECT_ACTIVE:
												self.score = self.score - 1
										self.Player.penup()
										self.Player.goto(180, 310)
										self.Player.pencolor("white")
										self.Player.fillcolor("white") 
										self.Player.begin_fill() 
										self.Player.pendown()
										self.Player.forward(200)
										self.Player.left(90)
										self.Player.forward(35)
										self.Player.left(90)
										self.Player.forward(200)
										self.Player.left(90)
										self.Player.forward(35)
										self.Player.left(90)
										self.Player.end_fill()

										self.Player.pencolor((0, 0, 0))
										self.Player.goto(180, 310)
										self.Player.write(f"Score: {self.score}", font=('Courier', 24, 'bold'))


						self.__predict(ball_a)
						self.__predict(ball_b)

						if Total_Time != old_timer:
								old_timer = Total_Time
								self.Player.penup()
								self.Player.goto(340, -370)
								self.Player.pencolor("white")
								self.Player.fillcolor("white") 
								self.Player.begin_fill() 
								self.Player.pendown()
								self.Player.forward(50)
								self.Player.left(90)
								self.Player.forward(55)
								self.Player.left(90)
								self.Player.forward(50)
								self.Player.left(90)
								self.Player.forward(55)
								self.Player.left(90)
								self.Player.end_fill()
								self.Player.pencolor("red")
								self.Player.goto(380, -340)
								self.Player.write(f"{self.TIMEOUT_LIMIT-diff}", font=('Courier', 18, 'bold'), align='right')

						self.__paddle_predict()



				turtle.done()

def Menu_UP():
		global Choose
		global Choose_X
		global Choose_Y

		if Choose_Y < 130:
				Choose_Y += 50
				
		Choose.hideturtle()
		Choose.goto(Choose_X, Choose_Y)
		Choose.showturtle()
		
def Menu_DOWN():
		global Choose
		global Choose_X
		global Choose_Y
		if Choose_Y > 0:
				Choose_Y -= 50
				
		Choose.hideturtle()
		Choose.goto(Choose_X, Choose_Y)
		Choose.showturtle()

def Menu_ENTER():
		global Choose
		global Choose_X
		global Choose_Y
		global Player_Name

		Greeting.clear()
		Greeting.bgcolor("orange")

		Menu.clear()
		Menu.penup()
		Menu.hideturtle()
		Menu.pencolor((0, 0, 0))
		Menu.goto(0, 270)
		Menu.write(f"INFO", font=('Courier', 48, 'bold'), align='center') # font=('Courier', FONT_SIZE, 'bold')
		
		"""
		case 1:
			ball_color = (255,0,0)
			ball_color2 = (255,255,0)
		case 2:
			ball_color = (0,255,0)
			ball_color2 = (255,0,255)
		case 3:
			ball_color = (0,0,255)
			ball_color2 = (255,255,255)
		case 4:
			ball_color = (0,0,0)
			ball_color2 = (255,0,0)
		"""
				
		if Choose_Y > 80:
				Game_Level = "PRACTICE"
				num_balls = 1
		elif Choose_Y < 60:
				Game_Level = "HARD"
				num_balls = 5		#TJ - adjust HARD
		else:
				Game_Level = "NORMAL"
				num_balls = 3
		
		Menu.speed(0)

		Menu.penup()
		Menu.color((1,0,0))
		Menu.fillcolor((1,1,0))
		Menu.goto(-150, 170)
		Menu.pendown()
		Menu.begin_fill()
		Menu.width(4)
		Menu.circle(15)
		Menu.end_fill()
		Menu.penup()
		Menu.goto(-100, 175)
		Menu.pencolor((1, 1, 1))
		Menu.write(f"item #1 - Powerful ", font=('Courier', 16, 'bold'), align='left') # font=('Courier', FONT_SIZE, 'bold')

		Menu.penup()
		Menu.color((0,1,0))
		Menu.fillcolor((1,0,1))
		Menu.goto(-150, 120)
		Menu.pendown()
		Menu.begin_fill()
		Menu.circle(15)
		Menu.end_fill()
		Menu.penup()
		Menu.goto(-100, 125)
		Menu.pencolor((1, 1, 1))
		Menu.write(f"item #2 - Increase 10 sec", font=('Courier', 16, 'bold'), align='left') # font=('Courier', FONT_SIZE, 'bold')
		
		Menu.penup()
		Menu.color((0,0,1))
		Menu.fillcolor((1,1,1))
		Menu.goto(-150, 70)
		Menu.pendown()
		Menu.begin_fill()
		Menu.circle(15)
		Menu.end_fill()
		Menu.penup()
		Menu.goto(-100, 75)
		Menu.pencolor((1, 1, 1))
		Menu.write(f"item #3 - Decrease 5 sec", font=('Courier', 16, 'bold'), align='left') # font=('Courier', FONT_SIZE, 'bold')

		if Game_Level == "HARD":
				Menu.penup()
				Menu.color((0,0,0))
				Menu.fillcolor((1,0,0))
				Menu.goto(-150, 20)
				Menu.pendown()
				Menu.begin_fill()
				Menu.circle(15)
				Menu.end_fill()
				Menu.penup()
				Menu.goto(-100, 25)
				Menu.pencolor((1, 1, 1))
				Menu.write(f"item #4 - End Game", font=('Courier', 16, 'bold'), align='left') # font=('Courier', FONT_SIZE, 'bold')

		for i in range(4):
				Menu.goto(-25, -330)
				Menu.penup()
				Menu.pencolor("orange")
				Menu.fillcolor("orange") 
				Menu.pendown()
				Menu.begin_fill() 
				Menu.forward(50)
				Menu.left(90)
				Menu.forward(50)
				Menu.left(90)
				Menu.forward(50)
				Menu.left(90)
				Menu.forward(50)
				Menu.left(90)
				Menu.end_fill()
				Menu.penup()
				Menu.goto(0, -330)
				Menu.pencolor((1, 1, 1))
				Menu.write(f"{4-i-1}", font=('Courier', 28, 'bold'), align='center') # font=('Courier', FONT_SIZE, 'bold')
				time.sleep(1.0)


		Greeting.clear()
		Menu.clear()
		my_simulator = BouncingSimulator(num_balls, Player_Name, Game_Level)
		my_simulator.run()


Screen_W = 800 
Screen_H = 600

Greeting = turtle.Screen()  
Greeting.setup(Screen_W + 50, Screen_H + 100)  
Greeting.title("Advance Pingpong Game")
Greeting.bgcolor("orange") # Screen Color

Player_Name = Greeting.textinput("Player Name", "Name")

Menu = turtle.Turtle()
Menu.penup()
Menu.hideturtle()
Menu.pencolor((1, 0, 0))
Menu.goto(0, 270)
Menu.write(f"Bounce King", font=('Courier', 48, 'bold'), align='center') # font=('Courier', FONT_SIZE, 'bold')
Menu.goto(0, 220)
Menu.write(f"Hello {Player_Name}", font=('Courier', 34, 'bold'), align='center') # font=('Courier', FONT_SIZE, 'bold')
Menu.pencolor((0, 0, 0))
Menu.goto(-70, 0)
Menu.write("HARD", font=('Courier', 36, 'bold'))
Menu.goto(-70, 50)
Menu.write("NORMAL", font=('Courier', 36, 'bold'))
Menu.goto(-70, 100)
Menu.write("PRACTICE", font=('Courier', 36, 'bold'))
Menu.pencolor((0, 0.3, 0))
Menu.goto(0, 160)
Menu.write("mode", font=('Courier', 24, 'bold'), align='center')


Choose_X = -80
Choose_Y = 75
Choose = turtle.Turtle()
Choose.penup()
Choose.goto(Choose_X, Choose_Y)
Choose.turtlesize(5)

Greeting.listen()
Greeting.onkeypress(Menu_UP, "Up")
Greeting.onkeypress(Menu_DOWN, "Down")
Greeting.onkeypress(Menu_ENTER, "Return")
Greeting.mainloop()

