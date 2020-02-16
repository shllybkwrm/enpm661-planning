import numpy as np


class Node:

    node_state = [];
    node_index = 0;
    parent_node_index = 0;

    def __init__(self, list=[[0,0,0],[0,0,0],[0,0,0]], parent_index=0):
        self.node_state = np.array(list);
        self.parent_node_index = parent_index;

    def BlankTileLocation(self):
        for i in range(3):
            for j in range(3):
                if self.node_state[i,j]==0:
                    return (i,j);
                else: pass

    def ActionMoveLeft(self):
        (i,j) = self.BlankTileLocation();
        if j>0:
            self.node_state[i,j] = self.node_state[i,j-1];
            self.node_state[i,j-1] = 0;
        return Node(self.node_state, self.node_index);

    def ActionMoveRight(self):
        (i,j) = self.BlankTileLocation();
        if j<2:
            self.node_state[i,j] = self.node_state[i,j+1];
            self.node_state[i,j+1] = 0;
        return Node(self.node_state, self.node_index);

    def ActionMoveUp(self):
        (i,j) = self.BlankTileLocation();
        if i>0:
            self.node_state[i,j] = self.node_state[i-1,j];
            self.node_state[i-1,j] = 0;
        return Node(self.node_state, self.node_index);

    def ActionMoveDown(self):
        (i,j) = self.BlankTileLocation();
        if i<2:
            self.node_state[i,j] = self.node_state[i+1,j];
            self.node_state[i+1,j] = 0;
        return Node(self.node_state, self.node_index);


def AddNode(Matrix_8puzzle_Nodes, NewNode):
    Matrix_8puzzle_Nodes.append(n);
    # Need to check if new node or not

Matrix_8puzzle_Nodes = [];
n = Node([[1,2,3],[4,5,6],[7,0,9]]);
AddNode(Matrix_8puzzle_Nodes, n);

print(n.node_state);
print(n.BlankTileLocation());
NewNode = n.ActionMoveLeft();
print(n.node_state);
print(n.BlankTileLocation());
NewNode = n.ActionMoveRight();
print(n.node_state);
print(n.BlankTileLocation());
NewNode = n.ActionMoveRight();
print(n.node_state);
print(n.BlankTileLocation());
NewNode = n.ActionMoveUp();
print(n.node_state);
print(n.BlankTileLocation());
NewNode = n.ActionMoveUp();
print(n.node_state);
print(n.BlankTileLocation());
NewNode = n.ActionMoveDown();
print(n.node_state);
print(n.BlankTileLocation());

