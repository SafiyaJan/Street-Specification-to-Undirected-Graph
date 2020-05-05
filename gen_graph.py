
import sys
import math
import re

def point_parser(points):

	#print("Print Points", points)

	temp = re.findall(r'(\s*-?\d+\s*,\s*-?\d+\s*)',points)
	for i in range (len(temp)):
		temp[i] = re.sub(r'\s+', '',temp[i]).split(',')


	return temp

class Point:

	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)

	def __eq__(self,other):
		return self.x == other.x and self.y == other.y

	def __cmp__(self,other):
		return cmp((self.x, self.y), (other.x, other.y))
        
		
	def __hash__(self):
		return 0

	def __str__(self):
		return ("(" + "{0:.2f}".format(self.x) + "," + "{0:.2f}".format(self.y) + ")")

class Street_Database:

	# instantiating street database
	def __init__(self):

		# street name and coordinates have a 1 to 1 correlation
		#self.street_names = []
		#self.street_points = []

		self.street_database = dict()
		self.intersect_list = dict()


	# def __str__(self):

	# 	print_str = ""
	# 	point_str = ""
	# 	for i in range(street_points):

	# 		for j in range(len(street_points[i])):



	# add street to database 
	def add(self, user_input):

		# check if the street is in database
		if user_input[1].lower() in self.street_database:
			print ("Error: Street already added.", file=sys.stderr)
			return
		
		# if not add street to database with name and points
		else:

			# add street name
			name = user_input[1].lower()
			#print ("Name of street",name)
			#self.street_names.append(name)
			points_list = []

			coord_list = point_parser(user_input[2])
			#print ("Coord List",coord_list)
			
			for point in coord_list:

				#temp = point_parser(point)
				coord = Point(float(point[0]),float(point[1]))
				#coord = [float(point[0]),float(point[1])]
				#print(coord)
				points_list.append(coord)
			
			# add points that make up the street
			#print (points_list)
			#self.street_points.append(points_list)

			self.street_database[name] = points_list
			#print ("Printing dict", self.street_database)

			#print ("Street added")
			
			return

	def remove(self, user_input):

		#test
		len_db = len(self.street_database)
		
		# check if street is in database
		name = user_input[1].lower()

		if name not in self.street_database:
			print("Error: street does not exist, therefore cannot be removed", file = sys.stderr)
			return 

		else:

			del self.street_database[name]

			# find street location in street_names and delete from list 
			# index = self.street_names.index(name)
			# self.street_names.pop(index)
			# self.street_points.pop(index)
			
			assert(name not in self.street_database)
			
			assert(len(self.street_database) == len_db-1)
			#print (self.street_database)
			
			#print("Street removed")

			return 

	def change(self, user_input):

		# check if street in database 
		name = user_input[1].lower()
		
		if name not in self.street_database:
			print("Error: street does not exist, therefore cannot be changed", file = sys.stderr)
			return

		else:

			# find street location in street_names  
			#index = self.street_names.index(name)

			points_list = []

			coord_list = point_parser(user_input[2])
			
			for point in coord_list:

				#temp = point_parser(point)
				#coord = [float(point[0]),float(point[1])]
				#print(coord)
				coord = Point(float(point[0]),float(point[1]))
				points_list.append(coord)
			
			# update street points 
			#print (points_list)
			#self.street_points[index] = points_list
			self.street_database[name] = points_list
			#print ("Printing dict", self.street_database)
			#print ("Street changed")

			return


	def intersect(self,p1,p2,p3,p4):

		
		x1,y1 = p1.x, p1.y
		x2,y2 = p2.x, p2.y
		x3,y3 = p3.x, p3.y
		x4,y4 = p4.x, p4.y


		try: 


			t_val = ((x1-x3)*(y3-y4)) - ((y1-y3)*(x3-x4))
			t_val_denom = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))

			u_val = -(((x1-x2)*(y1-y3)) - ((y1-y2)*(x1-x3)))
			u_val_denom = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))

			t = t_val/t_val_denom
			u = u_val/u_val_denom

			if (0<=t<=1 and 0<=u<=1):

				x = x1 + (t*(x2-x1))
				y = y1+(t*(y2-y1))
				inter_point = Point(x,y)
				return [inter_point]

			else:

				return None

		except Exception as exception:

			# Completely overlap case #

			# Case 1  - x1,x1 are enclosed in x3,x4

			if ((x3<=x1<=x4 and x3<=x2<=x4 and y3<=y1<=y4 and y3<=y2<=y4) or (x4<=x1<=x3 and x4<=x2<=x3 and y4<=y1<=y3 and y4<=y2<=y3) or (x3<=x1<=x4 and x3<=x2<=x4 and y3>=y1>=y4 and y3>=y2>=y4) or (x4<=x1<=x3 and x4<=x2<=x3 and y4>=y1>=y3 and y4>=y2>=y3)):

				
				inter_point1 = Point(x1,y1)
				inter_point2 = Point(x2,y2)
				return [inter_point1,inter_point2]


			# Case 2  - x3,x4 are enclosed in x1,x2

			if ((x2<=x3<=x1 and x2<=x4<=x1 and y2<=y3<=y1 and y2<=y4<=y1) or (x1<=x3<=x2 and x1<=x4<=x2 and y1<=y3<=y2 and y1<=y4<=y2) or (x2<=x3<=x1 and x2<=x4<=x1 and y2>=y3>=y1 and y2>=y4>=y1) or (x1<=x3<=x2 and x1<=x4<=x2 and y1>=y3>=y2 and y1>=y4>=y2)):

				inter_point1 = Point(x3,y3)
				inter_point2 = Point(x4,y4)
				return [inter_point1,inter_point2]
				#return [[x3,y3],[x4,y4]]

			# Partial overlap case #

			# Case 1

			if ((x1<=x3<=x2<=x4 and y1>=y3>=y2>=y4) or (x4<=x2<=x3<=x1 and y4>=y2>=y3>=y1) or (x1>=x3>=x2>=x4 and y1>=y3>=y2>=y4) or (x4>=x2>=x3>=x1 and y4>=y2>=y3>=y1)):
	
				inter_point1 = Point(x3,y3)
				inter_point2 = Point(x2,y2)
				return [inter_point1,inter_point2]
				

			# Case 2

			if ((x1<=x4<=x2<=x3 and y1>=y4>=y2>=y3) or (x3<=x2<=x4<=x1 and y3>=y2>=y4>=y1) or (x1>=x4>=x2>=x3 and y1>=y4>=y2>=y3) or (x3>=x2>=x4>=x1 and y3>=y2>=y4>=y1)):

				inter_point1 = Point(x2,y2)
				inter_point2 = Point(x4,y4)
				return [inter_point1,inter_point2]
		

			# Case 3

			if ((x2<=x4<=x1<=x3 and y2>=y4>=y1>=y3) or(x3<=x1<=x4<=x2 and y3>=y1>=y4>=y2) or (x2>=x4>=x1>=x3 and y2>=y4>=y1>=y3) or (x3>=x1>=x4>=x2 and y3>=y1>=y4>=y2)):
			
				inter_point1 = Point(x1,y1)
				inter_point2 = Point(x4,y4)
				return [inter_point1,inter_point2]
		

			# Case 4

			if  ((x4<=x1<=x3<=x2 and y4>=y1>=y3>=y2) or (x2<=x3<=x1<=x4 and y2>=y3>=y1>=y4) or (x4>=x1>=x3>=x2 and y4>=y1>=y3>=y2) or (x2>=x3>=x1>=x4 and y2>=y3>=y1>=y4)):

				inter_point1 = Point(x1,y1)
				inter_point2 = Point(x3,y3)
				return [inter_point1,inter_point2]


		return None


	def sort_points_by_dist(self,ref,points):
		points.sort(key=lambda x:euclid_dist(ref,x))
		return points

	def inter_point(self,street,edge_list):


		if (len(self.street_database) == 0):
			print("Error: You have not added any streets, therefore a graph cannot be generated", file = sys.stderr)
			return

		else:

			#edge_list = []

			interpoint_dict = dict()


			current_segments = self.street_database[street]

			for i in range(0, len(current_segments)-1):

				p1 = current_segments[i]
				p2 = current_segments[i+1]

				for key in self.street_database:

					if key != street:

						comp_segments = self.street_database[key]

						for j in range(0, len(comp_segments)-1):

							p3 = comp_segments[j]
							p4 = comp_segments[j+1]

							inter_point = self.intersect(p1,p2,p3,p4)

							if (inter_point != None):

								for point in inter_point:

									if point not in interpoint_dict:
										interpoint_dict[point] = [p1,p2,p3,p4]

									else:
										interpoint_dict[inter_point[0]].append(p1)
										interpoint_dict[inter_point[0]].append(p2)
										interpoint_dict[inter_point[0]].append(p3)
										interpoint_dict[inter_point[0]].append(p4)


			# for each segment 
			for i in range(0, len(current_segments)-1):


				P1 = current_segments[i]
				P2 = current_segments[i+1]

				inter_points = []

				for key in interpoint_dict:
					#print("Print KEY", key)
					value = interpoint_dict.get(key)
					for j in range(0,len(value)-1,2):
						if ((value[j] == P1) and (value[j+1] == P2)):
							if key not in inter_points:
								#print("Key added")
								#print (key)
								inter_points.append(key)
								
							#print("Key add ", key)
							break;

				if len(inter_points)>1:
					inter_points = self.sort_points_by_dist(P1,inter_points)

				if len(inter_points)>=1:
					inter_points.insert(0,P1)
					inter_points.append(P2)
					assert(len(inter_points)>=3)

				inter_points = list(dict.fromkeys(inter_points))


				if len(inter_points) >= 2:
					for k in range(0,len(inter_points)-1):
						#print ("Value of k ", k)
						edge_list.append((inter_points[k],inter_points[k+1]))



	def graph(self):

		if (len(self.street_database) == 0):
			print("Error: You have not added any streets, therefore a graph cannot be generated", file = sys.stderr)
			return

		else:

			edge_list = []

			final_edge_list = []

			vert_dict = dict()

			for key in self.street_database:
				self.inter_point(key,edge_list)

			edge_list = list(dict.fromkeys(edge_list))

			k = 1

			for x in range(0,len(edge_list)):

				if(edge_list[x][0] not in vert_dict):
					vert_dict[edge_list[x][0]] = k
					k = k + 1

				if(edge_list[x][1] not in vert_dict):
					vert_dict[edge_list[x][1]] = k
					k = k + 1

				#print (edge_list[x][0], "->", edge_list[x][1])

				#k = k + 1


			for edge in range(0,len(edge_list)):

				val_1 = vert_dict[edge_list[edge][0]]
				val_2 = vert_dict[edge_list[edge][1]]

				if ((val_1,val_2) not in final_edge_list) and ((val_2,val_1) not in final_edge_list):
					final_edge_list.append((val_1,val_2))


			# print vertices and edges

			print ("V = {")

			for key in vert_dict:
			 	print("\t",vert_dict[key], ":\t", key, sep="")


			print ("}")


			if (len(final_edge_list) == 0):
				print ("E = {")
				print ("}")	
				return

			
			if (len(final_edge_list) == 1):
				print ("E = {")
				print ("\t<",final_edge_list[0][0],",",final_edge_list[0][1],">",sep="")
				print ("}")	
				return


			if(len(final_edge_list) > 1):
				print ("E = {")
				for i in range(0,len(final_edge_list)-1):
					print ("\t<",final_edge_list[i][0],",",final_edge_list[i][1],">,",sep="")

				print ("\t<",final_edge_list[i+1][0],",",final_edge_list[i+1][1],">",sep="")
				print ("}")	
				return
			# for key in vert_dict:
			# 	print(key,vert_dict[key])


def euclid_dist(ref,point):
	x_ref = ref.x
	y_ref = ref.y
	x = point.x
	y = point.y
	return math.sqrt(((x-x_ref)**2 + (y-y_ref)**2))





















