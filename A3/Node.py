#Alvin Onabolu
#Nahor Yirgaalem

from common import *

class Node:
    #id will be from number of nodes
    #costs will be a 1d array of size num nodes that contain cost to each other node including itself
    def __init__(self, ID, networksimulator, costs):
        self.myID = ID
        self.ns = networksimulator
        num = self.ns.NUM_NODES        
        self.distanceTable = [[0 for i in range(num)] for j in range(num)]
        self.routes = [0 for i in range(num)]
        self.neighbors = [] #list of this nodes neigbors
        self.neighbors_costs = []
    

        # you implement the rest of constructor

        #each node has its own distance table init it here
        for i in range(num):
            for j in range(num):
                if i == self.myID:
                    self.distanceTable[self.myID][j] = costs[j]
                elif i == j:
                    self.distanceTable[i][j] = 0
                else:
                    self.distanceTable[i][j] = self.ns.INFINITY
        
        #Send the intial cost array to it neigboring nodes
        for i in range(num):
            if costs[i] != 999 and i != self.myID:
                self.neighbors.append([i, costs[i]])
            self.routes[i] = i


        self.sendUpdate(costs)
    

    def recvUpdate(self, pkt):
        
        prev = deepcopy(self.distanceTable[self.myID]) #save a copy to see if there was a change
     
        #implement the change that you got from neigboring router 
        #we apply the other routers changes without checking
        #computing Ddestid to source id shortest path
        #make sure to not compute  x =x

        #get all niegbors of this nodes cost 

        
        #We wil do Dx -> i for all other nodes

        #for each of those neigbors get their shortest path to dest (given from matricx)
        self.distanceTable[pkt.sourceid] = pkt.mincosts
        
        #each time we get update we recompute this nodes rows distance to each other router
        # you implement the rest of it  
        #once you get this recv update, if there was an update to this node row send its row to its neigbord
        cost = 999 
    

        #getting shortest distance from this router each other router
        
        for router in range(self.ns.NUM_NODES): #for each router computer Dx to Drouter
            if router != self.myID:
                min_cost = self.distanceTable[self.myID][router] #get the current shortest path from this node to this router
                for neighbor in self.neighbors:
                    #getting each neihbor of this router summing it cost + shortest path from that neighbor to router
                    cost = neighbor[1] + self.distanceTable[neighbor[0]][router]
                    if cost < min_cost:
                        min_cost = cost
                        #can add next hop for this node to router
                        self.routes[router] = neighbor[0]
         
                        #update the router
                        self.distanceTable[self.myID][router] = min_cost




        if (prev != self.distanceTable[self.myID]): #contents have been updated with new min costs
            self.sendUpdate(self.distanceTable[self.myID])


        return 

    
    def sendUpdate(self, changed_costs):
        for i in range(len(self.neighbors)):
            pkt = RTPacket(self.myID, self.neighbors[i][0], changed_costs)
            #send tolayer to self.neigbors[i]
            self.ns.tolayer2(pkt)
        return

    
    def printdt(self):
        print("   D"+str(self.myID)+" |  ", end="")
        for i in range(self.ns.NUM_NODES):
            print("{:3d}   ".format(i), end="")
        print()
        print("  ----|-", end="")
        for i in range(self.ns.NUM_NODES):            
            print("------", end="")
        print()    
        for i in range(self.ns.NUM_NODES):
            print("     {}|  ".format(i), end="" )
            
            for j in range(self.ns.NUM_NODES):
                print("{:3d}   ".format(self.distanceTable[i][j]), end="" )
            print()            
        print()
        
