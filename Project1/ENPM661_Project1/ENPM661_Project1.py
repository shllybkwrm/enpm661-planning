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
        #code = "";
        # Match output textfile
        #for i in range(3):
        #    for j in range(3):
        #        code += str(self.node_state[i,j]);
        
        code_1 = ' '.join(str(x) for x in self.node_state[:,0]);
        code_2 = ' '.join(str(x) for x in self.node_state[:,1]);
        code_3 = ' '.join(str(x) for x in self.node_state[:,2]);

        return ' '.join([code_1, code_2, code_3]);


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

        print(" > Found children,", len(ChildList));
        return ChildList;


    def Print(self):
        print(self.node_state[:,0], self.node_state[:,1], self.node_state[:,2]);


def CheckGoal(node):
    goal_state = np.array([[1,2,3],[4,5,6],[7,8,0]])
    return np.array_equal(node.node_state, goal_state);



def AddNodes(NewNodes):
    global Matrix_8puzzle_Nodes, Matrix_8puzzle_Indices, Matrix_8puzzle_Parents;
    global NodesInfoFile, AllNodesFile;

    for node in NewNodes:
        # Need to check if new node STATE or not

        if node.code not in Matrix_8puzzle_States:
            print("Adding node", node.node_index);

            #Matrix_8puzzle_Nodes.append(node);
            Matrix_8puzzle_Nodes[node.node_index] = node;
            Matrix_8puzzle_Indices.append(node.node_index);
            Matrix_8puzzle_Parents.append(node.parent_node_index);
            Matrix_8puzzle_States.append(node.code);

            AllNodesFile.write(node.code+'\n');
            NodesInfoFile.write(str(node.node_index) + ' ' + str(node.parent_node_index) + ' 0 \n');

            #print(node.node_state);
            #print("Code:", node.code);
            if CheckGoal(node):
                print("--- Goal found! ---");
                return True;

        else:
            print("Game state already visited!  Skipping node", node.node_index);

    return False;


def BuildTree(NodeList):
    res = False;
    ChildList = [];

    # Build tree level by level
    print(">> Tree level ", NodeList[0].parent_node_index+1);
    for node in NodeList:
        Children = node.GetChildren();
        res = AddNodes(Children);
        if res:  # Returns true if goal found
            return;

        ChildList.extend(Children);

    BuildTree(ChildList);


def Backtrack():
    print(">> Backtracking...");
    global Matrix_8puzzle_Nodes, Matrix_8puzzle_Indices, Matrix_8puzzle_Parents;
    global nodePathFile;
    path = [];

    # Start with goal, should be last visited node
    goal_node = Matrix_8puzzle_Nodes[Matrix_8puzzle_Indices[-1]];
    parent_index = goal_node.parent_node_index;
    
    print(goal_node.node_state);
    print("Code:", goal_node.code);
    path.append(goal_node.code);
    #nodePathFile.write(goal_node.code+'\n');  # Need to reverse this!!

    while parent_index != 0:
        parent = Matrix_8puzzle_Nodes[parent_index];
    
        print(parent.node_state);
        print("Code:", parent.code);
        path.append(parent.code);
        #nodePathFile.write(parent.code+'\n');

        # Get next parent
        parent_index = parent.parent_node_index;

    # Write to file in traversal order (reversed)
    for node_code in reversed(path):
        nodePathFile.write(node_code + '\n');

    return;
    

# Global variables to hold visited nodes
Matrix_8puzzle_Nodes = {};
Matrix_8puzzle_Indices = [];
Matrix_8puzzle_Parents = [];
Matrix_8puzzle_States = [];  # Plaintext game states


# File objects for output
nodePathFile = open('nodePath.txt', 'w');
NodesInfoFile = open('NodesInfo.txt', 'w');
AllNodesFile = open('Nodes.txt', 'w');


#  TODO:  Check if initial state is solvable
root_node = Node([[0,1,2],[4,5,3],[7,8,6]]);
AddNodes([root_node]);
#print(root_node.node_state);
#root_node.Print();
print("Empty tile starts at ", root_node.i, root_node.j);

BuildTree([root_node]);

Backtrack();



print(Matrix_8puzzle_Nodes);
print(Matrix_8puzzle_Indices);
print(Matrix_8puzzle_Parents);
#print(Matrix_8puzzle_States);


nodePathFile.close();
NodesInfoFile.close();
AllNodesFile.close();