import numpy as np

indexCounter = 0;

class Node:

    node_state = [];
    node_index = 0;
    parent_node_index = 0;
    
    (i,j) = (0,0);

    def __init__(self, list=[[0,0,0],[0,0,0],[0,0,0]], parent_index=0):
        self.node_state = np.array(list);
        self.parent_node_index = parent_index;

        
        global indexCounter;
        indexCounter += 1;
        self.node_index = indexCounter;

        (self.i,self.j) = self.BlankTileLocation();

    def BlankTileLocation(self):
        for i in range(3):
            for j in range(3):
                if self.node_state[i,j]==0:
                    return (i,j);
                else: pass

    def ActionMoveLeft(self):
        (i,j) = (self.i,self.j);
        if j>0:
            self.node_state[i,j] = self.node_state[i,j-1];
            self.node_state[i,j-1] = 0;
            return Node(self.node_state, self.node_index);
        else: return None;

    def ActionMoveRight(self):
        (i,j) = (self.i,self.j);
        if j<2:
            self.node_state[i,j] = self.node_state[i,j+1];
            self.node_state[i,j+1] = 0;
            return Node(self.node_state, self.node_index);
        else: return None;

    def ActionMoveUp(self):
        (i,j) = (self.i,self.j);
        if i>0:
            self.node_state[i,j] = self.node_state[i-1,j];
            self.node_state[i-1,j] = 0;
            return Node(self.node_state, self.node_index);
        else: return None;

    def ActionMoveDown(self):
        (i,j) = (self.i,self.j);
        if i<2:
            self.node_state[i,j] = self.node_state[i+1,j];
            self.node_state[i+1,j] = 0;
            return Node(self.node_state, self.node_index);
        else: return None;
    
    def GetChildren(self):
        ChildList = [];

        Child = self.ActionMoveLeft();
        ChildList.append(Child) if Child!=None else None;
        Child = self.ActionMoveRight();
        ChildList.append(Child) if Child!=None else None;
        Child = self.ActionMoveUp();
        ChildList.append(Child) if Child!=None else None;
        Child = self.ActionMoveDown();
        ChildList.append(Child) if Child!=None else None;

        print("Found children,", len(ChildList));
        return ChildList;


    def Print(self):
        print(self.node_state[:,0], self.node_state[:,1], self.node_state[:,2]);


def AddNodes(NewNodes):
    global Matrix_8puzzle_Nodes, Matrix_8puzzle_Indices, Matrix_8puzzle_Parents;

    for node in NewNodes:
        # Need to check if new node STATE or not (TODO)
        if node.node_index not in Matrix_8puzzle_Indices:
            print(node.node_state);

            Matrix_8puzzle_Nodes.append(node);
            Matrix_8puzzle_Indices.append(node.node_index);
            Matrix_8puzzle_Parents.append(node.parent_node_index);
        else:
            print("Index already in list");


def CheckGoal(node):
    goal_state = np.array([[1,2,3],[4,5,6],[7,8,0]])
    if node.node_state==goal_state:
        return True;
    else:
        return False;


def BuildTree(n):
    pass


Matrix_8puzzle_Nodes = [];
Matrix_8puzzle_Indices = [];
Matrix_8puzzle_Parents = [];

root_node = Node([[1,2,3],[4,5,6],[7,0,8]]);
AddNodes([root_node]);
#print(root_node.node_state);
#n.Print();
print(root_node.i,root_node.j);

Row1 = root_node.GetChildren();
#print(Row1);
AddNodes(Row1);

Row2 = Row1[0].GetChildren();
#print(Row1[0].node_state);
#print(Row1);
AddNodes(Row2);



print(Matrix_8puzzle_Nodes);
print(Matrix_8puzzle_Indices);
print(Matrix_8puzzle_Parents);

