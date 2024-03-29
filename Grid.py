#imports
import numpy as np
import time 
import os

def clearConsole():
    '''
    clear the console
    '''
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

# try new output type
class Gridworld:
    """
    This methods creates a gridworld for a RL algorithm
    Attributes: 
        initial state
        current state
        initial agent
        current agent
    """
    
     # Constructor
    def __init__(self,x_dim = 5, y_dim = 5, epsilon = 0.1, start = [0,0], terminal = [4,0],
                 neg_reward=[[0,4,-1],[2,1,-1],[4,4,-1]],
                barrier = [[1,2],[2,0],[2,3]]):
        """
        Initializes a gridworld with all parameters
        gives one positive reward in the terminal state
        state transition funktion: probability epsilon of going in a random different state
        all states as [y,x] in the code, in constructor parameters as [x,y] for convenience
        
        # create an empty grid world default hardcoded
        #  s  0  X  0 10
        #  0  0 -1  0  0
        #  0  X  0  0  0
        #  0  0  X  0  0
        # -1  0  0  0 -1
        
        Attributes:
            x_dim (int>0) : x dimension of gridworld
            y_dim (int>0) : y dimension of gridworld
            epsilon (0<float<1) : for epsilon-greedy state transition function
            start [x,y] = starting state of agent for each episode
            terminal [x,y] = terminal state with a positive reward
            neg_rewards [[x,y,reward],[x,y,reward],...] = list of fields with negative rewards
            barrier [[x,y],[x,y],...] = list of fields that are barriers
        """
        
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.epsilon = epsilon
        self.agent = [start[1],start[0]] # [y,x]
        self.initial_agent = [start[1],start[0]] # needed for reset
        self.terminal = [terminal[1],terminal[0]] # [y,x]
        
        self.action = ['up', 'down' , 'left' , 'right']
        
        # create empty gridworld
        world =np.zeros(shape=(self.y_dim,self.x_dim))
        
        # put terminal
        world[self.terminal[0],self.terminal[1]] = 10 # [y,x]
        
        # put negative rewards in gridworld
        for r in neg_reward:
            world[r[1],r[0]] = r[2]
            
        # put barrier in gridworld
        for b in barrier:
            world[b[1],b[0]] = np.NaN
        
        self.world = world
        
    # getter and setter
    def getXdim(self):
        return self.x_dim
    
    def getYdim(self):
        return self.y_dim
    
    def getActions(self):
        return self.action
    
    def getTerminal(self):
        return self.terminal # [y,x]
    
    def getState(self):
        return self.agent # [y,x]
    
    # methods
    def isValid(self,x,y):
        """
        checks whether coordinates are in the gridworld and not on a barrier
        """
        # check whether in the Gridworld
        if(x>=0 and x<self.x_dim and y>= 0 and y<self.y_dim):
            # check whether the state is a barrier
            if not np.array_equal(self.world[y,x], np.NaN, equal_nan=True):
                return True
        return False
    
    def inTerminal(self):
        """
        checks whether the current agent is in the terminal state
        """
        if self.agent == self.terminal: # [y,x]
            return True
        return False
        
        
    def reset(self):
        """
        resets the gridworld to its initial state
        """
        self.agent = self.initial_agent
        return self.initial_agent
    
    def step(self, action):
        """
        applies the state transition dynamics and reward dynamics 
        based on the state of the environment and the action argument
        Arguments: 
            action int : [0,1,2,3] for ['up', 'down' , 'left' , 'right'] =
            
        returns: 
            the new state
            reward of this step
            a boolean indication whether this state is terminal
        """
        
        # state transition policy
        # check whether action or for epsilon random other one
        take_action = np.random.choice([True,False],p=[1-self.epsilon, self.epsilon])
        
        # take random action
        if (not take_action):
            action = np.random.choice(len(self.action))
            
        # get new place after action
        y,x = self.agent[0], self.agent[1] # [y,x]
        if action == 0: # up
            y -= 1
        elif action == 1: # down
            y += 1
        elif action == 2: # left
            x -= 1
        elif action == 3: # right
            x += 1
           
        # gets the reward later
        reward = -0.1
        
        # check if action is valid, then do action
        if self.isValid(x,y):
            self.agent = [y,x]
            reward = self.world[self.agent[0],self.agent[1]]
        else:
            reward = -0.5
        
        # return state of agent, reward, if new state is terminal
        return self.agent, reward , self.inTerminal()
        
        
    def visualize(self):
        """
        visualizes the current state
        """
        
        #os.system('cls') # for Windows
        clearConsole() # should always work
        print("")
        
        for y in range(self.y_dim):
            
            firstLine = "    ||"
            thisLine = ("      " + str(y) + " ||")[-6:]
            nextLine =  "____||"
            
            for x in range(self.x_dim):
                val = self.world[y,x]
                
                # print one field if agent is there
                if ([y,x]==self.agent):
                    nextLine += "__A__|"
                elif np.array_equal(val, np.NaN, equal_nan=True): # if it is a barrier
                    nextLine += "XXXXX|"
                else:
                    nextLine +=  "_____|"
                    
                # print vlaues on field
                if (val==0.0): # if 
                    firstLine += "     |"
                    thisLine += "     "
                elif np.array_equal(val, np.NaN, equal_nan=True): # if it is a barrier
                    firstLine += "XXXXX|"
                    thisLine += "XXXXX"
                else: # if it has a reward
                    firstLine += "     |"
                    thisLine += ( "     " + str(int(val)) )[-5:]
                thisLine += "|"
                
            # print and go to next line
            print(firstLine)
            print(thisLine)
            print(nextLine)
            
        # at the bottom of the print
        topLine = "____||"
        line = "    ||"
        middleLine = "    ||"
        for x in range(self.x_dim):
            line += "     |"
            middleLine += ("      " + str(x) + " |")[-6:]
            topLine += "_____|"
            
        print(topLine)
        print(line)
        print(middleLine)
        print(line)
        print("")
        
