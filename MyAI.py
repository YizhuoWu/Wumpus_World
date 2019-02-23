# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):

	def __init__( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
		self.current_position = [0,0]
		self.current_point = 0
		self.with_gold = False
		self.with_arrow = True
		self.track_moves = []	
		self.current_direction = "R"		
		self.safe_points = []
		self.wumpus_points = []
		self.pit_points = []
		self.passed_position = []
		self.r_passed =[]
		self.directions = []
		self.wumpus_killed = False
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

	def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
		if self.intelligent_move(stench,breeze) == True:
			return Agent.Action.CLIMB
		else:
			if scream:
				self.wumpus_killed = True
			if (not stench) and (not breeze):
				self.add_safe_point()
			if stench or breeze:
				if stench and breeze:
					self.add_pit_point()
					self.add_wumpus_point()
				elif stench:
					if self.with_arrow == True and self.current_position == [0,0]:
						self.with_arrow = False
						return Agent.Action.SHOOT
					if self.wumpus_killed == False:
						if self.current_position == [0,0]:
							self.safe_points.append(tuple((1,0)))
							#self.safe_points.append(tuple((1,2)))
							self.wumpus_points.append(tuple((0,1)))
							self.add_wumpus_point()
						else:
							self.add_wumpus_point()
					if self.wumpus_killed == True:
						self.add_safe_point()
						self.safe_points.append(tuple((1,0)))
						self.safe_points.append(tuple((0,1)))
					
				elif breeze:
					self.add_pit_point()
						
			self.directions.append(self.current_direction)
			
			return self.best_move(stench,breeze,glitter,bump,scream)
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    
	def intelligent_move(self,stench,breeze):
		
		if (stench and breeze) and self.current_position == [0,0]:
			return True
		if breeze and self.current_position == [0,0]:
			return True
		return False
    
	def best_move(self,stench,breeze,glitter,bump,scream):

		if bump:
			
			self.change_position_when_bump()
			return self.turn_need()
			
		if self.enough_points() == True:
			if self.current_position == [0,0] and self.current_direction == 'L' and self.with_gold==True:
				
				return Agent.Action.CLIMB
			if self.current_position == [0,0] and self.current_direction == 'D':
				
				return Agent.Action.CLIMB			
			else:
				if self.with_gold == True:
					return self.with_gold_route()
				
				if self.current_direction == "L":

					if self.current_position[1] == 0:
						point_to_up = (self.current_position[0],self.current_position[1] + 1)

						if point_to_up in self.safe_points and point_to_up not in self.passed_position:
							self.track_moves.append("TURN_RIGHT")
							self.current_direction = "U"
							return Agent.Action.TURN_RIGHT
						if self.current_position == [0,0] and self.with_arrow == False and self.wumpus_killed == False:
							return Agent.Action.CLIMB

						else:
							return self.move_forward(stench,breeze,glitter,scream)

					
					else:
						if (0,self.current_position[1]) in self.passed_position and self.current_position[0]!=0:
							return self.move_forward(stench,breeze,glitter,scream)
						else:
							self.track_moves.append("TURN_LEFT")
							self.current_direction = "D"
							return Agent.Action.TURN_LEFT							
							
							
				if self.current_direction == "U":
					if (0,self.current_position[1]) in self.passed_position and self.current_position[1]!=0:
						self.track_moves.append("TURN_LEFT")
						self.current_direction = "L"
						return Agent.Action.TURN_LEFT
					else:
						return self.move_forward(stench,breeze,glitter,scream)

				if self.current_direction == "D":
					
					point_to_right = (self.current_position[0]+1,self.current_position[1])
					point_to_right_second = (self.current_position[0]+2,self.current_position[1])
					point_to_right_third = (self.current_position[0]+3,self.current_position[1])					
						

					if point_to_right in self.safe_points and point_to_right not in self.r_passed and self.current_position[0]==0:
						if point_to_right in self.passed_position and point_to_right_second in self.passed_position and point_to_right_third in self.passed_position:
							return self.move_forward(stench,breeze,glitter,scream)
						else:
							self.track_moves.append("TURN_LEFT")
							self.current_direction = "R"
							return Agent.Action.TURN_LEFT	
					elif self.current_position[1] == 0:
						self.track_moves.append("TURN_RIGHT")
						self.current_direction = "L"
						return Agent.Action.TURN_RIGHT
											
					else:
						return self.move_forward(stench,breeze,glitter,scream)

				else:
					if self.current_position[0] == 0:
						point_to_right = (self.current_position[0]+1,self.current_position[1])
						if point_to_right not in self.safe_points:
							self.track_moves.append("TURN_RIGHT")
							self.current_direction = "D"
							return Agent.Action.TURN_RIGHT
						else:
							self.r_passed.append(tuple(self.current_position))
							return self.move_forward(stench,breeze,glitter,scream)

					self.r_passed.append(tuple(self.current_position))
					return self.move_forward(stench,breeze,glitter,scream)
					
						
					if self.current_position[0] == 0 and self.current_direction == 'L' and self.current_position != [0,0]:
						return self.turn_need()
					else:																		
						point_to_right = (self.current_position[0]+1,self.current_position[1])
						if self.current_direction == "D" and point_to_right in self.safe_points and point_to_right not in self.passed_position:
							self.track_moves.append("TURN_LEFT")
							self.current_direction = "R"
							return Agent.Action.TURN_LEFT

						return(self.move_forward(stench,breeze,glitter,scream))
				
		else:
			
			return self.with_gold_route()

	def move_forward(self,stench,breeze,glitter,scream):
						
		if glitter:
			
			self.with_gold = True
			return Agent.Action.GRAB
		if (not stench) and (not breeze):
			
			self.track_moves.append("FORWARD")
			self.passed_position.append(tuple(self.current_position))
			self.change_position()
									
			return Agent.Action.FORWARD
		else:
			if self.is_forward_point_safe():	
				self.track_moves.append("FORWARD")
				self.passed_position.append(tuple(self.current_position))
				self.change_position()
				return Agent.Action.FORWARD
					
			else:
				if self.with_arrow == False and self.wumpus_killed == False and stench and not breeze and self.current_position != [0,0]:
					self.track_moves.append("FORWARD")
					self.passed_position.append(tuple(self.current_position))
					self.change_position()
					return Agent.Action.FORWARD
				else:
					return self.turn_need()
						
	def enough_points(self):
		
		move_count = 0
		for i in self.track_moves:
			if i!="SHOOT" or i!= "GRAB" or i!= "CLIMB":
				move_count += 1
		if len(self.directions) * 2 >= 200:
			return False
		return True

	def turns_count_need(self):
		if self.current_direction == "R":
			return 2
		elif self.current_direction == "L":
			return 0
		elif self.current_direction == "U":
			return 1
		elif self.current_direction == "D":
			return 1

	def turn_need(self):
		if self.current_direction == "R":
			
			self.track_moves.append("TURN_LEFT")
			self.current_direction = "U"
			return Agent.Action.TURN_LEFT


		elif self.current_direction == "L":
			
			if self.current_position[1] == 0:
			
				self.track_moves.append("FORWARD")
				self.current_position[0] -= 1
				return Agent.Action.FORWARD
			
			if (self.current_position[0]-1,self.current_position[1]) in self.safe_points and self.current_position[0] != 0:
				self.track_moves.append('FORWARD')
				self.change_position()
				return Agent.Action.FORWARD
			else:
				self.track_moves.append('TURN_LEFT')
				self.current_direction = 'D'
				return Agent.Action.TURN_LEFT

		elif self.current_direction == "U":
			if self.current_position[0] == 0:
				self.track_moves.append("TURN_RIGHT")
				self.current_direction = "R"
				return Agent.Action.TURN_RIGHT
			else:
				self.track_moves.append("TURN_LEFT")
				self.current_direction = "L"
				return Agent.Action.TURN_LEFT
		
		elif self.current_direction == "D":
			if self.current_position[1] == 0:
				self.track_moves.append('TURN_RIGHT')
				self.current_direction = 'L'
				return Agent.Action.TURN_RIGHT
			else:
				 
				self.track_moves.append("FORWARD")
				self.change_position()
			
				return Agent.Action.FORWARD

	def change_position_when_bump(self):
		if self.current_direction == "R":
			self.current_position[0] -= 1
		
		elif self.current_direction == "U":
			self.current_position[1] -= 1
		

	def change_position(self):
		if self.current_direction == "R":
			self.current_position[0] += 1
		elif self.current_direction == "L":
			self.current_position[0] -= 1
		elif self.current_direction == "U":
			self.current_position[1] += 1
		elif self.current_direction == "D":
			self.current_position[1] -= 1
		
	def add_safe_point(self):

		col = self.current_position[0]
		row = self.current_position[1]

		safe_to_right = (col + 1,row)
		safe_to_left = (col - 1,row)
		safe_to_up = (col,row + 1)
		safe_to_down = (col , row - 1)

		if col == 0 and row == 0:
			self.safe_points.append(safe_to_right)
			self.safe_points.append(safe_to_up)
		else:
			if col == 0:
				self.safe_points.append(safe_to_right)
				self.safe_points.append(safe_to_down)
				self.safe_points.append(safe_to_up)
			elif row == 0:
				self.safe_points.append(safe_to_right)
				self.safe_points.append(safe_to_up)
				self.safe_points.append(safe_to_left)
			else:
				self.safe_points.append(safe_to_right)
				self.safe_points.append(safe_to_left)
				self.safe_points.append(safe_to_up)
				self.safe_points.append(safe_to_down)
		self.safe_points = list(set(self.safe_points))
		
	def add_wumpus_point(self):
		col = self.current_position[0]
		row = self.current_position[1]

		p_to_right = (col + 1,row)
		p_to_left = (col - 1,row)
		p_to_up = (col,row + 1)
		p_to_down = (col,row - 1)

		self.wumpus_points.append(p_to_right)
		self.wumpus_points.append(p_to_left)
		self.wumpus_points.append(p_to_up)
		self.wumpus_points.append(p_to_down)
		for i in self.wumpus_points:
			if i[0] < 0 or i[1] < 0 or i in self.safe_points:
				self.wumpus_points.remove(i)

		self.wumpus_points = list(set(self.wumpus_points))

	def add_pit_point(self):
		col = self.current_position[0]
		row = self.current_position[1]

		p_to_right = (col + 1,row)
		p_to_left = (col - 1,row)
		p_to_up = (col,row + 1)
		p_to_down = (col, row - 1)

		self.pit_points.append(p_to_right)
		self.pit_points.append(p_to_left)
		self.pit_points.append(p_to_up)
		self.pit_points.append(p_to_down)
		for n in self.pit_points:
			if n[0] < 0 or n[1] < 0 or n in self.safe_points:
				self.pit_points.remove(n)

		self.pit_points = list(set(self.pit_points))



	def is_forward_point_safe(self):
		col = self.current_position[0]
		row = self.current_position[1]

		if self.current_direction == "R":
			return True if (col + 1,row) in self.safe_points else False
		elif self.current_direction == "L":
			return True if (col - 1,row) in self.safe_points else False
		elif self.current_direction == "U":
			return True if (col, row + 1) in self.safe_points else False
		elif self.current_direction == "D":
			return True if (col, row - 1) in self.safe_points else False


	def with_gold_route(self):
		
		if self.current_direction == "R":
			
			self.current_direction = "U"
			return Agent.Action.TURN_LEFT

		elif self.current_direction == "U":
			
			self.current_direction = "L"
			return Agent.Action.TURN_LEFT
		
		elif self.current_direction == "D":
		
			if self.current_position == [0,0]:
				return Agent.Action.CLIMB
			elif self.current_position[1] == 0:
				self.current_direction = "L"
				return Agent.Action.TURN_RIGHT
			
			else:
				self.change_position()
				return Agent.Action.FORWARD
		else:
			if self.directions[-3] == "R" and self.directions[-2] == "U":
				if self.current_position[0] == 0:
					self.current_direction = "D"
					return Agent.Action.TURN_LEFT
				else:
					self.change_position()
					return Agent.Action.FORWARD
			elif self.directions[-2] == "U":
				self.current_direction = "D"
				return Agent.Action.TURN_LEFT
			else:
				if self.current_position[0] == 0:
					self.current_direction = "D"
					return Agent.Action.TURN_LEFT
				else:
					self.change_position()
					return Agent.Action.FORWARD
			
			


	#----------------------------------------------------------------------
	
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
