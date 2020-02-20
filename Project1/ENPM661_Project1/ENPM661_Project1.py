import numpy as np

indexCounter = 0;

class Node:

    node_state = [];
    node_index = 0;
    parent_node_index = 0;
    
    (i,j) = (0,0);

    code = "";

    def __init__(self, list=[[0,0,0],[0,0,0],[0,0,0]], parent_index=0):
        self.node_state = np.array(list);
        self.parent_node_index = parent_index;

        
        global indexCounter;
        indexCounter += 1;
        self.node_index = indexCounter;

        self.code = self.EncodeState();
        (self.i,self.j) = self.BlankTileLocation();

    
    def EncodeState(self):
        code = "";
        # May want to reverse this to match output textfile?
        for i in range(3):
            for j in range(3):
                code += str(self.node_state[i,j]);

        return code;


    def BlankTileLocation(self):
        for i in range(3):
            for j in range(3):
                if self.node_state[i,j]==0:
                    return (i,j);
                else: pass

    
    def ActionMoveLeft(self):
        (i,j) = (self.i,self.j);
        game_state = self.node_state.copy();
        if j>0:
            game_state[i,j] = game_state[i,j-1];
            game_state[i,j-1] = 0;
            return Node(game_state, self.node_index);
        else: return None;

    def ActionMoveRight(self):
        (i,j) = (self.i,self.j);
        game_state = self.node_state.copy();
        if j<2:
            game_state[i,j] = game_state[i,j+1];
            game_state[i,j+1] = 0;
            return Node(game_state, self.node_index);
        else: return None;

    def ActionMoveUp(self):
        (i,j) = (self.i,self.j);
        game_state = self.node_state.copy();
        if i>0:
            game_state[i,j] = game_state[i-1,j];
            game_state[i-1,j] = 0;
            return Node(game_state, self.node_index);
        else: return None;

    def ActionMoveDown(self):
        (i,j) = (self.i,self.j);
        game_state = self.node_state.copy();
        if i<2:
            game_state[i,j] = game_state[i+1,j];
            game_state[i+1,j] = 0;
            return Node(game_state, self.node_index);
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


def CheckGoal(node):
    goal_state = np.array([[1,2,3],[4,5,6],[7,8,0]])
    return np.array_equal(node.node_state, goal_state);



def AddNodes(NewNodes):
    global Matrix_8puzzle_Nodes, Matrix_8puzzle_Indices, Matrix_8puzzle_Parents;

    for node in NewNodes:
        # Need to check if new node STATE or not

        if node.code not in Matrix_8puzzle_States:

            Matrix_8puzzle_Nodes.append(node);
            Matrix_8puzzle_Indices.append(node.node_index);
            Matrix_8puzzle_Parents.append(node.parent_node_index);
            Matrix_8puzzle_States.append(node.code);

            print(node.node_state);
            print("Code", node.code);
            if CheckGoal(node):
                print("Goal found!");
                return True;

        else:
            print("Game state already in list");

    return False;


def BuildTree(nodes):
    res = False;

    for node in nodes:
        Children = node.GetChildren();
        res = AddNodes(Children);
        if res:
            break;
        #nodes.append(Children);
        #nodes.pop(0);
        BuildTree(Children);
    


Matrix_8puzzle_Nodes = [];
Matrix_8puzzle_Indices = [];
Matrix_8puzzle_Parents = [];
Matrix_8puzzle_States = [];  # Plaintext game states

root_node = Node([[1,2,0],[4,5,3],[7,8,6]]);
AddNodes([root_node]);
#print(root_node.node_state);
#n.Print();
print("Empty tile at ", root_node.i,root_node.j);

BuildTree([root_node]);

#Row1 = root_node.GetChildren();
#AddNodes(Row1);

#Row2 = Row1[0].GetChildren();
#print(Row1[0].node_state);
#AddNodes(Row2);



print(Matrix_8puzzle_Nodes);
print(Matrix_8puzzle_Indices);
print(Matrix_8puzzle_Parents);
print(Matrix_8puzzle_States);

