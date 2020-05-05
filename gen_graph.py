
import sys
import math
import re

# Convert (x,y) format into [x,y]
def point_parser(points):

	temp = re.findall(r'(\s*-?\d+\s*,\s*-?\d+\s*)',points)
	for i in range (len(temp)):
		temp[i] = re.sub(r'\s+', '',temp[i]).split(',')

	return temp

# Find the euclid distance between 2 points
def euclid_dist(ref,point):
	x_ref = ref.x
	y_ref = ref.y
	x = point.x
	y = point.y
	return math.sqrt(((x-x_ref)**2 + (y-y_ref)**2))


# Define a class that defines a point on a line segment
class Point:

	# Constuctor
	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)

	# Equality check
	def __eq__(self,other):

		return (abs(self.x-other.x) < 1e-10) and (abs(self.y-other.y) < 1e-10)
		
	def __hash__(self):
		return 0

	# Used to print Point object
	def __str__(self):
		return ("(" + "{0:.2f}".format(self.x) + "," + "{0:.2f}".format(self.y) + ")")

# Defining a class that defines the set of all input streets
class Street_Database:

	# instantiating street database
	def __init__(self):

		# dictionary where key is street name & value is the point that make up the street
		self.street_database = dict()
		
		self.intersect_list = dict()


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
			points_list = []

			# convert the list of points to list of coord -> [[x1,y1],[x2,y2],..]
			coord_list = point_parser(user_input[2])
			
			# create point object for each coord in list
			for point in coord_list:

				coord = Point(float(point[0]),float(point[1]))
				points_list.append(coord)

			# add to dictionary street and its points
			self.street_database[name] = points_list
			
			return

	# Remove street from street database
	def remove(self, user_input):

		#test
		len_db = len(self.street_database)
		
		# check if street is in database
		name = user_input[1].lower()

		if name not in self.street_database:
			print("Error: street does not exist, therefore cannot be removed", file = sys.stderr)
			return 

		# if street in database, delete it
		else:

			# remove street entry from dictionary
			del self.street_database[name]
			
			# ensure that street is not in database
			assert(name not in self.street_database)
			assert(len(self.street_database) == len_db-1)

			return 

	
	# Change street spec
	def change(self, user_input):

		# check if street in database 
		name = user_input[1].lower()
		
		if name not in self.street_database:
			print("Error: street does not exist, therefore cannot be changed", file = sys.stderr)
			return

		else:

			points_list = []

			# convert the list of points to list of coord -> [[x1,y1],[x2,y2],..]
			coord_list = point_parser(user_input[2])
			
			# create point object for each coord in list
			for point in coord_list:
				coord = Point(float(point[0]),float(point[1]))
				points_list.append(coord)
			
			# update street points 
			self.street_database[name] = points_list

			return


	# Find the point(s) of interection of 2 line segs
	# p1,p2,p3,p4 are points that make up the 2 line segs
	def intersect(self,p1,p2,p3,p4):

		# retrieve x,y coords of the points
		x1,y1 = p1.x, p1.y
		x2,y2 = p2.x, p2.y
		x3,y3 = p3.x, p3.y
		x4,y4 = p4.x, p4.y


		# check to see if point of intersection equation evaluates one unique point of intersection
		try: 

			t_val = ((x1-x3)*(y3-y4)) - ((y1-y3)*(x3-x4))
			t_val_denom = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))

			u_val = ( ((x1-x2)*(y1-y3)) - ((y1-y2)*(x1-x3)))
			u_val_denom = ( ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)) )

			t = t_val/t_val_denom
			u = -u_val/u_val_denom

			if (u < 0 or u > 1 or t < 0 or t > 1):
				return None

			if ((0<=t<=1) and (0<=u<=1)):

				x = x1 + (t*(x2-x1))
				y = y1+(t*(y2-y1))
				inter_point = Point(x,y)
				return [inter_point]


		# if exception occurs, the lines are colinear special handling needed
		except Exception as exception:

			# Completely overlap case #

			# Case 1  - x1,x1 are enclosed in x3,x4

			if (t_val_denom == 0 and u_val_denom == 0 and t_val == 0 and u_val == 0):
			
				if ((x3<=x1<=x4 and x3<=x2<=x4 and y3<=y1<=y4 and y3<=y2<=y4) or (x4<=x1<=x3 and x4<=x2<=x3 and y4<=y1<=y3 and y4<=y2<=y3) or (x3<=x1<=x4 and x3<=x2<=x4 and y3>=y1>=y4 and y3>=y2>=y4) or (x4<=x1<=x3 and x4<=x2<=x3 and y4>=y1>=y3 and y4>=y2>=y3)):

					inter_point1 = Point(x1,y1)
					inter_point2 = Point(x2,y2)
					return [inter_point1,inter_point2]


				# Case 2  - x3,x4 are enclosed in x1,x2

				if ((x2<=x3<=x1 and x2<=x4<=x1 and y2<=y3<=y1 and y2<=y4<=y1) or (x1<=x3<=x2 and x1<=x4<=x2 and y1<=y3<=y2 and y1<=y4<=y2) or (x2<=x3<=x1 and x2<=x4<=x1 and y2>=y3>=y1 and y2>=y4>=y1) or (x1<=x3<=x2 and x1<=x4<=x2 and y1>=y3>=y2 and y1>=y4>=y2)):

					inter_point1 = Point(x3,y3)
					inter_point2 = Point(x4,y4)
					return [inter_point1,inter_point2]

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

			if(t_val_denom == 0 and u_val_denom == 0):
				return None

		return None


	# sorts list of points by distance from ref point
	def sort_points_by_dist(self,ref,points):
		points.sort(key=lambda x:euclid_dist(ref,x))
		return points

	

	# Find all the points of intersection between all the streets
	def inter_point(self,street,edge_list):

		# ensure that the street database is not empty
		if (len(self.street_database) == 0):
			print("Error: You have not added any streets, therefore a graph cannot be generated", file = sys.stderr)
			return

		else:

			# create a dictionary to store the points of intersection on each street
			interpoint_dict = dict()

			current_segments = self.street_database[street]

			# for each segment in street find all points of interection on the street
			for i in range(0, len(current_segments)-1):

				p1 = current_segments[i]
				p2 = current_segments[i+1]

				# find points of intersection with current street and every other street
				for key in self.street_database:

					if key != street:

						# get other street points 
						comp_segments = self.street_database[key]

						for j in range(0, len(comp_segments)-1):

							p3 = comp_segments[j]
							p4 = comp_segments[j+1]

							# check if there is point of intersection 
							inter_point = self.intersect(p1,p2,p3,p4)

							# if there is a point of intersection
							if (inter_point != None):

								# add point of intersection to interpoint_dict along with the points that make up the intersection
								for point in inter_point:

									if point not in interpoint_dict:
										interpoint_dict[point] = [p1,p2,p3,p4]

									else:
										interpoint_dict[inter_point[0]].append(p1)
										interpoint_dict[inter_point[0]].append(p2)
										interpoint_dict[inter_point[0]].append(p3)
										interpoint_dict[inter_point[0]].append(p4)


			# for each segment of current street, create a list points + intersection that lie on that segment
			for i in range(0, len(current_segments)-1):

				P1 = current_segments[i]
				P2 = current_segments[i+1]

				inter_points = []

				for key in interpoint_dict:

					value = interpoint_dict.get(key)

					for j in range(0,len(value)-1,2):
						
						if ((value[j] == P1) and (value[j+1] == P2)):
							
							if key not in inter_points:
								inter_points.append(key)
								
							break;

				# if there are multiple points of intersection, sort them by distance from start of street segment
				if len(inter_points)>1:
					inter_points = self.sort_points_by_dist(P1,inter_points)

				if len(inter_points)>=1:
					inter_points.insert(0,P1)
					inter_points.append(P2)
					assert(len(inter_points)>=3)

				# delete duplicate points
				inter_points = list(dict.fromkeys(inter_points))

				# create edge list for current segment
				if len(inter_points) >= 2:

					for k in range(0,len(inter_points)-1):
						edge_list.append((inter_points[k],inter_points[k+1]))


	# Print out vertice list and edge list of entire graph
	def graph(self):

		# make sure street database is not empty 
		if (len(self.street_database) == 0):
			print("Error: You have not added any streets, therefore a graph cannot be generated", file = sys.stderr)
			return

		else:

			edge_list = []

			final_edge_list = []

			vert_dict = dict()

			# create edge list for each street 
			for key in self.street_database:
				self.inter_point(key,edge_list)

			# create dictionry of vertices
			k = 1
			for x in range(0,len(edge_list)):

				if(edge_list[x][0] not in vert_dict):
					vert_dict[edge_list[x][0]] = k
					k = k + 1

				if(edge_list[x][1] not in vert_dict):
					vert_dict[edge_list[x][1]] = k
					k = k + 1


			# create final edge list for entire graph
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

