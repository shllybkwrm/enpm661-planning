import math
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt


w = 300
h = 200


##### Input functions #####
def get_parameters():
    print("\nPlease enter the rigid robot parameters.")
    ans=(input("Enter the radius (default=3): "))
    if ans=='':  radius=3
    else:  radius=int(ans)
    ans=(input("Enter the obstacle clearance (default=2): "))
    if ans=='':  clearance=2
    else:  clearance=int(ans)
    ans=(input("Enter the robot step size (1-10, default=1): "))
    if ans=='':  step=1
    elif int(ans)>10:  step=10
    else:  step=int(ans)

    return radius, clearance, step

def get_start():
    print("\nPlease enter the initial coordinates of the robot.")
    ans=(input("Enter the x coordinate (default=0): "))
    if ans=='':  x=0
    else:  x=int(ans)
    ans=(input("Enter the y coordinate (default=0): "))
    if ans=='':  y=0
    else:  y=int(ans)
    ans=(input("Enter the starting theta (30-deg increments, default=30): "))
    if ans=='':  theta_s=30
    else:  theta_s=int(ans)

    return [x, y], theta_s

def get_goal():
    print("\nPlease enter the coordinates of the robot's goal.")
    ans=(input("Enter the target x coordinate (default=0): "))
    if ans=='':  x=0
    else:  x=int(ans)
    ans=(input("Enter the target y coordinate (default=2): "))
    if ans=='':  y=2
    ans=(input("Enter the goal theta (30-deg increments, default=same as start): "))
    if ans=='':  theta_g=theta_s
    else:  theta_g=int(ans)

    return [x, y], theta_g


# Get input parameters
radius, clearance, step = get_parameters()  # NOTE:  Still need to incorporate clearance ###
start_point, theta_s = get_start()
goal_point, theta_g = get_goal()



########### SET ROBOT COORDINATE ##############
robot_x_coord=w//2
robot_y_coord=h//2
robot_height=radius
robot_breadth=radius
x=np.linspace((robot_x_coord-robot_breadth/2),(robot_x_coord+robot_breadth/2),robot_breadth+1,dtype=int)
y=np.linspace((robot_y_coord+robot_height/2),(robot_y_coord-robot_height/2),robot_height+1,dtype=int)
x_1,y_1=np.meshgrid(x,y, indexing='xy')
points = np.array(list(zip(x_1.flatten(),y_1.flatten())))
########### PLOTTING THE ROBOT - change to circle ################
rcodes = [Path.MOVETO] + [Path.LINETO]*3 + [Path.CLOSEPOLY]
rvertices = [((robot_x_coord-robot_breadth/2), (robot_y_coord-robot_height/2)), ((robot_x_coord-robot_breadth/2), (robot_y_coord+robot_height/2)), ((robot_x_coord+robot_breadth/2), (robot_y_coord+robot_height/2)), ((robot_x_coord+robot_breadth/2), (robot_y_coord-robot_height/2)), (0, 0)]
robot = Path(rvertices,rcodes)
robotpatch = PathPatch(robot, facecolor='green', edgecolor='green')
########### Prepare Searchable Nodes ################
xm=np.linspace(0,w,num=w,endpoint=False,dtype=int)
ym=np.linspace(h,0,num=h,endpoint=False,dtype=int)
x_m,y_m=np.meshgrid(xm,ym)
map=np.array(list(zip(x_m.flatten(),y_m.flatten())))
cost=(((robot_x_coord-x_m)**2)+((robot_y_coord-y_m)**2))**(0.5)
##print(map.shape)
# PREPARE OBSTACLE SPACE
line1x=((x_m<=25)&(x_m>=20))
line1y=(y_m<=((120+(13*(x_m-20)))))
line2x=((x_m<=75)&(x_m>=25))
line2y=(y_m<=185)
line3x=((x_m<=50)&(x_m>=20))
line3y=(y_m>=((((65/55)*(x_m-20))+120)))
line4x=((x_m<=100)&(x_m>=75))
line4y=(y_m<=(((35/25)*(100-x_m))+150))
line5x=((x_m<=100)&(x_m>=75))
line5y=(y_m>=((30/25)*(x_m-75))+120)
line6x=((x_m<=75)&(x_m>=50))
line6y=(y_m>=((30/25)*(75-x_m))+120)
line7x=((x_m<=95)&(x_m>=30))
line7y=(y_m>=0.57763130100345*(95-x_m)+30)
line8x=((x_m<=105)&(x_m>=95))
line8y=(y_m>=1.73373802511719*(x_m-95)+30)
def obstacle_halfplane(map):
    for i in range(0,len(map)):
        ox=map[i][0]
        oy=map[i][1]
        crown=np.where(20<=ox>=25)
        print(oy)
########### PLOTTING THE MAP SPACE #############
vertices = []
codes = []
######## POLYGON OBSTACLES ###################
codes = [Path.MOVETO] + [Path.LINETO]*5 + [Path.CLOSEPOLY]
vertices = [(20, 120), (25, 185), (75, 185), (100, 150), (75,120),(50,150),(0, 0)]
codes += [Path.MOVETO] + [Path.LINETO]*3 + [Path.CLOSEPOLY]
vertices += [(30, 67.54603), (40, 84.88341025), (105,47.32472), (95, 35), (0, 0)]
codes += [Path.MOVETO] + [Path.LINETO]*3 + [Path.CLOSEPOLY]
vertices += [(200, 25), (225,40), (250,25), (225,10), (0, 0)]
vertices = np.array(vertices, float)
path = Path(vertices, codes)
####### CIRCLE OBSTACLE #####################
circle=Path.circle((225,150),radius=25,readonly=False)
####### ELIPSE OBSTACLE ####################
elipse=Ellipse((150,100),80,40,0,facecolor='None', edgecolor='green')
###### PATCHING THEM TOGETHER ###############
pathpatch = PathPatch(path, facecolor='None', edgecolor='green')
pathpatch2 = PathPatch(circle, facecolor='None', edgecolor='green')
pathpatch3= Ellipse((150,100),80,40,0,facecolor='None', edgecolor='green')

####### CHECKING TO SEE IF ROBOT IS IN OBSTACLE ################
inside_polygons = (path.contains_points(points, radius=1e-9))#true if it is inside the polygon,otherwise false
inside_elipse= (elipse.contains_points(points,radius=1e-9))
inside_circle= (circle.contains_points(points,radius=1e-9))
inside_obstacle=(any(inside_polygons==True)) or (any(inside_circle==True)) or (any(inside_elipse==True))
if inside_obstacle:
    print("inside the obstacle you are, you little thing")
####################### REDUCING SEACH NODES BY SUBTRACTING OBSTACLES ################
inside_polygons2 = np.where((path.contains_points(map, radius=1e-9)),20000,0)
inside_elipse2= np.where((elipse.contains_points(map,radius=1e-9)),20000,0)
inside_circle2= np.where((circle.contains_points(map,radius=1e-9)),20000,0)
mask=(inside_polygons2+inside_elipse2+inside_circle2)
reduced=np.array(list(zip(x_m.flatten(),y_m.flatten(),mask.flatten())))
reduced2=np.vstack((x_m.flatten(),y_m.flatten(),mask)).T
newmap=reduced[np.all(reduced<20000, axis=1),:]# if any value in reduced map is True remove it
newmap=np.delete(newmap,2,axis=1)

###### PLOTTING #####################
fig, ax = plt.subplots()
ax.add_patch(robotpatch)
ax.add_patch(pathpatch)
ax.add_patch(pathpatch2)
ax.add_patch(pathpatch3)
ax.set_title('Map Space')
print(ax)
ax.autoscale_view()
plt.xlim(0,w)
plt.ylim(0,h)
plt.show()



####################### A STAR ################
class Node:
    def __init__(self, node_no, coord, parent=0, g=0, h=0, theta=0):
        self.node_no = node_no
        self.parent = parent
        self.coord = coord
        self.g=g
        self.h=h
        self.cost = g+h
        self.theta = theta


def distance_2(p1,p2):
    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
    return distance

def get_and_replace_min_cost(node):
    for i in node_q:
        costfinder={i.cost:i}
        k=min(costfinder.keys())
        node_q.remove(costfinder[k])
        node_q.insert(0,costfinder[k])
        return node_q

# Needs collision and bound checking
# Map for duplicate checking
visited = np.zeros((w*2,h*2,12), dtype=bool)
def generate_node_successor(coord):
    new_positions=[]
    updated=[]
    thetas=np.linspace(0, 2*np.pi, 12, endpoint=False)
    for i,t in enumerate(thetas):
        # NOTE:  Incorporated robot step size here
        new_point = np.array([(coord[0] + step*np.cos(t)), (coord[1] + step*np.sin(t))])
        new_point = ( np.round(new_point*2, decimals=0) ) / 2
    
        # Check for duplicates
        a = int(new_point[0]*2)
        b = int(new_point[1]*2)
        if visited[a, b, i]:
            print("node already visited: ", new_point)
            pass
        else:
            visited[a, b, i] = True
            new_positions.append(new_point)
    
    # This shouldn't be needed with the new duplicate checking
#    for i in range(0,len(new_positions)):
#        for j in range(1,(len(new_positions)-1)):
#            distance=distance_2(new_positions[j],new_positions[i])
###            print("dis",distance)
#        if distance>0.5:
#            updated.insert(0,new_positions[i]) 
#    return updated

    return new_positions


def get_gscore(previous,current):
    return (previous.g + distance_2(previous.coord, current))
    # Calculate g incrementally, so angle of approach is not needed

def get_hscore(current):
    return distance_2(current, goal_point)

# Not used?  Taking out to make things simpler
#def get_fscore(current_score,gscore,hscore):
#    return (current_score + gscore + hscore)


#start_point=[0,0]
#goal_point=[0,2]
print("\nThe start point is", start_point)
print("The goal point is", goal_point)
starth = get_hscore(start_point)
print("The distance to goal is", starth, '\n')

start_node=Node(0, start_point, parent=0, g=0, h=starth, theta=theta_s)
node_q=[start_node]  # Put node_start in the OPEN list
visited_coord=[]
final_nodes = []  # closed
final_nodes.append(node_q[0])  # Only writing data of nodes in seen
visited_coord.append(node_q[0].coord)
node_counter = 0  # To define a unique ID to all the nodes formed

##for i in range(1):#while node_q:  # UNCOMMENT FOR DEBUGGING 
while node_q: #while the OPEN list is not empty
##    node_q=get_and_replace_min_cost(node_q)
    current_root = node_q.pop(0)
    # Don't need to re-calculate these, nothing changed?  Also they are not used
    #currentg=get_gscore(start_node, current_root.coord)
    #currenth=get_hscore(current_root.coord)
    #current_cost= get_gscore(start_node, current_root.coord) + get_hscore(current_root.coord)
    if int(current_root.coord[0])==goal_point[0] and int(current_root.coord[1])==goal_point[1]:
        print("Goal reached:  ", current_root.coord, current_root.node_no)
        #print(child_node, final_nodes)  # not sure what "close" was?

    temp_coords=generate_node_successor(current_root.coord)
    for temp in temp_coords:
        print("new point: ",temp)
        node_counter+=1
        print("node count: ",node_counter)
        # Note - g should be from *previous* node to current, plus the previous g
        tempg=get_gscore(current_root, temp)
        temph=get_hscore(temp)
        #temp_cost= get_gscore(start_node, temp) + get_hscore(temp)
        child_node = Node(node_counter, temp, current_root, tempg, temph)
        # Need to check for duplicates somewhere here
        if child_node not in node_q:
            if (child_node.g) <=(child_node.cost):
                node_q.append(child_node)
            elif child_node in final_nodes:
                if (child_node.g) <=(child_node.cost):
                    node_q.append(child_node)
            else:
                final_nodes.append(child_node)
        final_nodes.append(current_root)

