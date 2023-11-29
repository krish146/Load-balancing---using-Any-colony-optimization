import numpy as np

# from ant_colony import AntColony
import random as rn
from numpy.random import choice as np_choice

class AntColony(object):

    def __init__(self,capacity,load,performance_measure, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1,gamma=1):
        """
        Args:
            load(1D list of len(distance) size): load % at each node of the graph waiting for computation.
            
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            decay (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1
            gamma (int or float): exponent on load%, same as above detail
        Example:
            ant_colony = AntColony(german_distances, 100, 20, 2000, 0.95, alpha=1, beta=2)          
        """
        self.capacity=capacity
        self.load=load
        self.performance_measure=performance_measure
        
        self.distances  = distances
        self.pheromone = np.ones(self.distances.shape)/(len(distances)-1) #normalization of pheromone values
        self.all_inds = range(len(distances)) #
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.gamma=gamma

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        x=1
        for i in range(self.n_iterations):
            for j in range(self.n_ants): #for starting at different nodes
                all_paths = self.gen_all_paths(j)
                self.spread_pheronome(all_paths, self.n_best)
                print(all_paths,"iteration no: ",x)
                all_paths=all_paths[0]
            
                if all_paths[1] < all_time_shortest_path[1]:
                    all_time_shortest_path = all_paths            
                self.pheromone = self.pheromone * self.decay 
                #print(self.pheromone, "pheromone :",x)
                x+=1
        return all_time_shortest_path

    def spread_pheronome(self, all_paths, n_best):
        path,dist = all_paths[0]
        for move in path:
            #print("pheromone updates for :",move)
            self.pheromone[move] += 1.0 / dist 
        

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele] 
        return total_dist

    def gen_all_paths(self,currentstart):
        all_paths = []
        path = self.gen_path(currentstart) 
        all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []  
        visited = set()
        prev = start 
        visited.add(start)
        
        predicted_load=[]
        actual_load=[] # in terms of actual memory
        deduction_load=[]
        
        for i, j in zip(self.load, self.capacity):
            actual_load.append(i * j)
       # actual_load=(self.load*self.capacity)
        for i, j in zip(actual_load,self.performance_measure):
            deduction_load.append(i*j)
            
      #  deduction_load=actual_load*self.performance_measure #performance measure is constant , which should be dynamic for real
        for i, j in zip(actual_load,deduction_load):
            predicted_load.append(i-j)
            
        predicted_load=np.array(predicted_load)
        #print("predicted load: ",predicted_load)
        self.load=((predicted_load*100)/self.capacity)
        
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev],predicted_load,visited)
            path.append((prev, move)) 
            prev = move
            visited.add(move)
        path.append((prev, start))     
        
        #print("load changes: ",self.load)
        return path

    def pick_move(self, pheromone, dist,predicted_load, visited):#####
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0
        
#         row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)*((1.0/(load-(performance_measure/100)*20))**self.gamma) #############
       
        
#print(type(dist)," ",type(predicted_load)) type checking error 

       
        row = pheromone ** self.alpha * (( 1.0 / dist) ** self.beta)*((1.0/(predicted_load))**self.gamma) #############
    
#         self.load=(predicted_load*100/self.capacity)
        
#         print("predicted load : ",predicted_load)
 

        norm_row = row / row.sum()  #probability for each node is calculated
        move = np_choice(self.all_inds, 1, p=norm_row)[0] 
        return move
    

distances = np.array([[np.inf, 2, 2, 5, 7],
                      [2, np.inf, 4, 8, 2],
                      [2, 4, np.inf, 1, 3],
                      [5, 8, 1, np.inf, 2],
                      [7, 2, 3, 2, np.inf]])
#load=[20,30,15,17,80] # found in precalculations %load of the whole capacity
#performance_measure=[14,1,5,10,6] #precalculated in a simulation of iterations, let it be percent of the load that will disappear
load=[0.20,0.30,0.15,0.17,0.80] 
performance_measure=[0.14,0.01,0.05,0.10,0.06] ###direct percentages
capacity=[5.0,3.0,8.0,8.0,1.0] #given for each node

# for i in range(0,len(distances)):
#     load.append(input(f"Enter load for {i}: "))
    
    
ant_colony = AntColony(capacity,load,performance_measure,distances,len(distances), 1, 5, 0.95, alpha=1, beta=1,gamma=2)
shortest_path = ant_colony.run()
print ("shorted_path: {}".format(shortest_path))
print(ant_colony.gen_all_paths(4))