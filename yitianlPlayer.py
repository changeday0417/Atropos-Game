
# coding: utf-8

# In[71]:


import collections
import sys

msg = "Given board " + sys.argv[1] + "\n";
sys.stderr.write(msg);

Input_board = sys.argv[1]

# use str_split to split the input into board list and lastplay
def str_split (Input_board):
    [board_str, last_step] = Input_board.split('LastPlay:')
    b_1 = board_str.split(']')
    board_list = []
    for i in range(0,len(b_1) - 1):
        row_list = []
        now_str = b_1[i]
        for j in range(1, len(now_str)):
            row_list.append(int(now_str[j]))
        board_list.append(row_list)
    return board_list, last_step

# use step_split to change lastplay (c,x,y,z) into a list
def step_split (last_step):
    last_list = [int(last_step[1]),int(last_step[3]),int(last_step[5]),int(last_step[7])]
    return last_list

#Define a Board class to store the board list, last step
class Board:
    def __init__(self, board_list, last_step):
        self.board_list = board_list
        self.size = len(board_list) - 2
        self.deep = deep
        #self.last_pos
        if last_step == 'null':
            self.last_pos = 0
        else:
            self.last_pos = step_split(last_step)
            check_ = self.xyz_xy(self.last_pos[1:4])
            self.board_list[check_[0]][check_[1]] = self.last_pos[0]
 
    # use xyz_xy to change the position of board list into Axis [Height, Left Distance, Right Distance]
    def xyz_xy (self, xyz):
        if len(xyz) == 3:
            if xyz[0] == 0:
                pos = [self.size + 1 - xyz[0], xyz[1]-1]
            else:
                pos = [self.size + 1 - xyz[0], xyz[1]]
        elif len(xyz) == 2:
            if xyz[0] == self.size + 1:
                pos = [self.size + 1 - xyz[0], xyz[1] + 1, xyz[0]-xyz[1]]
            else:
                pos = [self.size + 1 - xyz[0], xyz[1], xyz[0]-xyz[1]+1] 
        return pos
        
    #Use get_zero_pos to get the position of uncolored circle
    def get_zero_pos(self):
        test = self.board_list
        zero_pos = []
        for i in range(1,len(test)):
                for j in range(0,len(test[i])):
                    if test[i][j] == 0:
                        mid = [i,j]
                        mid1 = self.xyz_xy(mid)
                        zero_pos.append(mid1)
        return zero_pos

    # Use check_color to get all possible colors of the input position
    def check_color(self, xyz):
        size = self.size
        pos = xyz
        may_pos = [
            [pos[0],pos[1]-1,pos[2]+1],
            [pos[0]+1,pos[1]-1,pos[2]],
            [pos[0]+1,pos[1],pos[2]-1],
            [pos[0],pos[1]+1,pos[2]-1],
            [pos[0]-1,pos[1]+1,pos[2]],
            [pos[0]-1,pos[1],pos[2]+1],
            [pos[0],pos[1]-1,pos[2]+1],
            ] 
        pos_color = [1,2,3]
        for i in range(0,6):
            [x,y,z] = may_pos[i]
            [x1,y1,z1] = may_pos[i+1]
            
            if (-1 < x < size + 3) & (-1 < y < size + 3) & (-1 < z < size + 3): # within the region  
                if (-1 < x1 < size + 3) & (-1 < y1 < size + 3) & (-1 < z1 < size + 3):
                    cpos_1 = self.xyz_xy(may_pos[i])
                    color_1 = self.board_list[cpos_1[0]][cpos_1[1]]
                    cpos_2 = self.xyz_xy(may_pos[i+1])
                    color_2 = self.board_list[cpos_2[0]][cpos_2[1]]
                    if ((color_1 == 1) & (color_2 == 2)) or ((color_1 == 2) & (color_2 == 1)):
                        if 3 in pos_color:
                            pos_color.remove(3)
                    elif ((color_1 == 2) & (color_2 == 3)) or ((color_1 == 3) & (color_2 == 2)):
                        if 1 in pos_color:
                            pos_color.remove(1)
                    elif ((color_1 == 1) & (color_2 == 3)) or ((color_1 == 3) & (color_2 == 1)):
                        if 2 in pos_color:
                            pos_color.remove(2)
        return pos_color
       
    # Based on the last step, get all possible positions of next step       
    def possible_pos(self):
        possible_pos = []
        size = self.size
        if self.last_pos == 0:
            possible_pos = self.get_zero_pos()
            
        else:
            last_color = self.last_pos[0]
            pos = self.last_pos[1:4]
            may_pos = [
            [pos[0],pos[1]-1,pos[2]+1],
            [pos[0]+1,pos[1]-1,pos[2]],
            [pos[0]+1,pos[1],pos[2]-1],
            [pos[0],pos[1]+1,pos[2]-1],
            [pos[0]-1,pos[1]+1,pos[2]],
            [pos[0]-1,pos[1],pos[2]+1],
            ]
            
            for i in range(0,6):
                [x,y,z] = may_pos[i]
                if (-1 < x < size + 2) & (-1 < y < size + 2) & (-1 < z < size + 2): # within the region
                    
                    check_ = self.xyz_xy(may_pos[i])
                    if self.board_list[check_[0]][check_[1]] == 0:             # there is no color in position [x,y,z]
                        possible_pos.append(may_pos[i])
            if len(possible_pos) == 0:
                possible_pos = self.get_zero_pos()                          # if its neighbors are colored then choose 0 pos
        return possible_pos
    
    # Output the possible position with possible color
    def color_pos(self):
        may_pos = self.possible_pos()
        length = len(may_pos)
        possible_cxyz = []
        for i in range(0, length):
            try_pos = may_pos[i]
            all_color = self.check_color(try_pos)
            for j in range(0,len(all_color)):
                cxyz = [all_color[j]]
                cxyz.extend(try_pos)
                possible_cxyz.append(cxyz)
        return possible_cxyz
 
    # Based on current board list, color a circle in this board and output a new board
    def inset_point(self, cxyz):
        check_ = self.xyz_xy(cxyz[1:4])
        #if self.board_list[check_[0]][check_[1]] == 0: 
        insert_board = Board(self.board_list,'null') # reate a new board
        insert_board.last_pos = cxyz
        insert_board.board_list[check_[0]][check_[1]] = cxyz[0]
        return insert_board
    
# Use generate_tree to generate a tree, deep must be even
def generate_tree(now_Board, deep):
    root_value = now_Board
    myboard_tree = MyTree(root_value)
    if deep == 0:
        return myboard_tree
    else:
        childs = root_value.color_pos()
        if len(childs) > 0 :
            for i in range(0, len(childs)):
                child = childs[i]       
                child_board = root_value.inset_point(child) 
                child_tree = generate_tree(child_board, deep-1)
                myboard_tree.insert_child(child_tree)
        else:
            return myboard_tree
    return myboard_tree


#Define Class MyTree
class MyTree(object):
    # Initial the tree
    def __init__(self, root_value):
        self.root = root_value
        self.child = []
    # insert child_value
    def insert_child(self, child_tree):
            self.child.append(child_tree)
    # set the root value
    def set_root(self, root_value):
        self.root = root_value
    # get the root value
    def get_root(self):
        return self.root
    # get the child_tree
    def get_child(self, child_num):
        return self.child[child_num]
    def get_all_child(self):
        return self.child

#static evaluator
def evaluator(state):

    
    
    board = state.get_root()
    length = len(board.color_pos())
    # If there is no open position, I lose
    if length == 0:
        score = -10000
    else:
        #open position, higher score
        score = len(board.color_pos())*10
    #
    return score
    
#Alpha_Beta prunning Algorithm
def Alpha_Beta(state, change_deep, deep, alpha, beta):
    c_childs = state.get_all_child()
    if (len(c_childs) == 0) & (change_deep != 0): #terminal state
        if change_deep % 2 == 0:
            next_step = state.root
            possible = next_step.possible_pos()
            if len(possible) > 0:
                ec_ = [1]
                ec_.extend(possible[0])
                now_step = next_step.inset_point(ec_)
                return [-10000,now_step]
            return [-10000,next_step]
        else:
            next_step = state.root
            return [10000,next_step]
        
    elif change_deep == 0:
        next_step = state.get_root()
        return [evaluator(state),next_step] # it should be a number
    #Max level 
    elif (change_deep % 2 == 0) & (change_deep > 0) & (len(c_childs) > 0):# MAX level
        v = -10000
        child_tree_list = state.get_all_child()
        next_step = child_tree_list[0].get_root()
        for y in range(0, len(child_tree_list)):
            A_B = Alpha_Beta(child_tree_list[y], change_deep - 1, deep, alpha, beta)
            v1 = max(v, A_B[0])
            if v1 > v:
                next_step = child_tree_list[y].get_root()
            v = v1
            if v >= beta:
                return [v,next_step]
            alpha = max(alpha, v)
    #Min level    
    elif (change_deep % 2 != 0) & (change_deep > 0) & (len(c_childs) > 0):
        v = 10000
        child_tree_list = state.get_all_child()
        next_step = child_tree_list[0].get_root()
        for y in range(0, len(child_tree_list)):
            next_step = child_tree_list[y].get_root()
            A_B = Alpha_Beta(child_tree_list[y], change_deep - 1, deep, alpha, beta)
            v1 = min(v, A_B[0])
            if v1 < v:
                next_step = child_tree_list[y].get_root()
            v = v1
            if v <= alpha:
                return [v,next_step]
            beta = min(alpha, v)
    r = [v, next_step]
    return r
#Main 
deep = 6       # You can change deep to build diffrent depth tree, deep should be even
[board_list, last_step] = str_split(Input_board) 
now_board = Board(board_list, last_step)
test_tree = generate_tree(now_board, deep)
alpha = -10000
beta = 10000
AB = Alpha_Beta(test_tree, deep, deep, alpha, beta)

# use into_output to change the output into standard format
def into_output(cxyz):
    str_ ='(' + str(cxyz[0]) + ',' + str(cxyz[1]) + ',' + str(cxyz[2]) + ','+str(cxyz[3]) + ')'
    return str_
#output
sys.stdout.write(into_output(AB[1].last_pos));


# In[ ]:




