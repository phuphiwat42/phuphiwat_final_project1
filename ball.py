import turtle
import math


class Ball:
		def __init__(self, size, x, y, vx, vy, color, id, color2=None):
				self.size = size
				self.x = x
				self.y = y
				self.vx = vx
				self.vy = vy
				self.color = color
				self.color2 = color2
				self.mass = 100*size**2
				self.count = 0
				self.id = id
				self.canvas_width = turtle.screensize()[0]
				self.canvas_height = turtle.screensize()[1]
				

		def draw(self):
				turtle.penup()
				turtle.color(self.color)
				if self.id == 999:
						turtle.color(self.color)
				turtle.fillcolor(self.color)
				if self.id == 999:
						turtle.fillcolor(self.color2)
				turtle.goto(self.x, self.y-self.size)
				turtle.pendown()
				turtle.begin_fill()
				turtle.circle(self.size)
				turtle.end_fill()

		def bounce_off_vertical_wall(self):
				self.vx = -self.vx
				self.count += 1

		def bounce_off_horizontal_wall(self):
				self.vy = -self.vy
				self.count += 1

		def bounce_off(self, that):
				dx  = that.x - self.x
				dy  = that.y - self.y
				dvx = that.vx - self.vx
				dvy = that.vy - self.vy
				dvdr = dx*dvx + dy*dvy;
				dist = self.size + that.size

				magnitude = 2 * self.mass * that.mass * dvdr / ((self.mass + that.mass) * dist)

				fx = magnitude * dx / dist
				fy = magnitude * dy / dist

				self.vx += fx / self.mass
				self.vy += fy / self.mass
				that.vx -= fx / that.mass
				that.vy -= fy / that.mass
				self.count += 1
				that.count += 1

		def distance(self, that):
				x1 = self.x
				y1 = self.y
				x2 = that.x
				y2 = that.y
				d = math.sqrt((y2-y1)**2 + (x2-x1)**2)
				return d

		def move(self, dt):
				self.x += self.vx*dt
				self.y += self.vy*dt

		def time_to_hit(self, that):
				if self is that:
						return math.inf
				dx  = that.x - self.x
				dy  = that.y - self.y
				dvx = that.vx - self.vx
				dvy = that.vy - self.vy
				dvdr = dx*dvx + dy*dvy
				if dvdr > 0:
						return math.inf
				dvdv = dvx*dvx + dvy*dvy
				if dvdv == 0:
						return math.inf
				drdr = dx*dx + dy*dy
				sigma = self.size + that.size
				d = (dvdr*dvdr) - dvdv * (drdr - sigma*sigma)

				if d < 0:
						return math.inf
				t = -(dvdr + math.sqrt(d)) / dvdv


				if t <= 0:
						return math.inf

				return t

		def time_to_hit_vertical_wall(self):
				if self.vx > 0:
						return (self.canvas_width - self.x - self.size) / self.vx
				elif self.vx < 0:
						return (self.canvas_width + self.x - self.size) / (-self.vx)
				else:
						return math.inf

		def time_to_hit_horizontal_wall(self):
				if self.vy > 0:
						return (self.canvas_height - self.y - self.size) / self.vy
				elif self.vy < 0:
						return (self.canvas_height + self.y - self.size) / (-self.vy)
				else:
						return math.inf

		def time_to_hit_paddle(self, paddle):
				if (self.vy > 0) and ((self.y + self.size) > (paddle.location[1] - paddle.height/2)):
						return math.inf
				if (self.vy < 0) and ((self.y - self.size) < (paddle.location[1] + paddle.height/2)):
						return math.inf

				dt = (math.sqrt((paddle.location[1] - self.y)**2) - self.size - paddle.height/2) / abs(self.vy)
				paddle_left_edge = paddle.location[0] - paddle.width/2
				paddle_right_edge = paddle.location[0] + paddle.width/2
				if paddle_left_edge - self.size <= self.x + (self.vx*dt) <= paddle_right_edge + self.size:
						return dt
				else:
						return math.inf

		def bounce_off_paddle(self):
				self.vy = -self.vy
				self.count += 1
	
		def Get_Ball_ID(self):
				return self.id
		
		def Get_VY(self):		#TJ - return vy
				return self.vy

		def __str__(self):
				return str(self.x) + ":" + str(self.y) + ":" + str(self.vx) + ":" + str(self.vy) + ":" + str(self.count) + str(self.id)
