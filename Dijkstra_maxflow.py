#! Python 2.7 - Dijkstra.py

infinity = 1000000
invalid_node = -1


class Node:
    previous = invalid_node
    distfromsource = infinity
    visited = False


class Dijkstra:
    def __init__(self):
        self.startnode = 0
        self.endnode = 0
        # list created to hold contents of csvfile
        self.network = []
        # Flag to check if file has been loaded
        self.network_populated = False
        self.nodetable = []
        self.nodetable_populated = False
        self.route = []
        self.route_populated = False
        self.currentnode = 0

    def populate_network(self, filename):
        '''load network/csv file from current directory'''
        self.network_populated = False
        # see if file exists
        try:
            # open file for reading
            networkfile = open(filename, 'r')
        # if IOError raised, file cannot be loaded
        except IOError:
            print "Network file could not be found"
            return
        print filename, "opened"
        # loop through the lines in the file
        # and add them to the list
        for line in networkfile:
            self.network.append(map(int, line.split(",")))
        self.network_populated = True
        networkfile.close()

    def populate_node_table(self):
        '''populate node table'''
        self.nodetable = []
        self.nodetable_populated = False

        if not self.network_populated:
            print "Network not populated!"
            return

        # creates a node for each vertex in the graph/network
        for node in self.network:
            self.nodetable.append(Node())

        # sets values for the start node
        self.nodetable[self.startnode].distfromsource = 0
        self.nodetable[self.startnode].visited = True
        self.nodetable_populated = True

    def parse_route(self, filename):
        '''load in route file'''
        self.route_populated = False
        try:
            with open(filename, 'r') as f:
                self.route_populated = True
                # read entire line and strip the trailing newline
                line = f.readline().strip()
                # converts character to int to be used as start and end nodes
                # e.g. B>F = 1>5
                startnode = ord(line[0]) - 65
                endnode = ord(line[-1]) - 65
                self.startnode = startnode
                self.endnode = endnode
                print "Path to take:", line
        except IOError:
            print "Parse route file could not be found"

    def return_near_neighbour(self):
        nearestneighbour = []
        # returns every neighbour node to the current node by
        # checking if the edge is either greater than 0 (can traverse there)
        # or if it is unvisited
        for index, edge in enumerate(self.network[self.currentnode]):
            if edge > 0 and not self.nodetable[index].visited:
                nearestneighbour.append(index)
        return nearestneighbour

    def calculate_tentative(self):
        '''calculate tentative distance of nearest neighbours'''
        nearestneighbour = self.return_near_neighbour()

        # tentative distance is calculated by adding the current distance by
        # neighbouring node's edge value
        # sets the distance from source for each neighbouring node
        # and also sets their previous node as the current node
        for index in nearestneighbour:
            tentativedist = self.nodetable[self.currentnode].distfromsource + self.network[self.currentnode][index]
            if tentativedist < self.nodetable[index].distfromsource:
                self.nodetable[index].distfromsource = tentativedist
                self.nodetable[index].previous = self.currentnode

    def determine_next_node(self):
        '''determine next node to examine'''
        # the next node might not be a neighbour
        bestdistance = infinity
        self.currentnode = invalid_node

        # checks all nodes that are unvisited and selects the
        #  new node to traverse by selecting the shortest current distance from source
        for nodeindex, node in enumerate(self.nodetable):
            if not node.visited and node.distfromsource < bestdistance:
                    bestdistance = node.distfromsource
                    self.currentnode = nodeindex

    def calculate_shortest_path(self):
        shortestpath = 0
        print "Calculating Shortest Path:"

        # e.g. currentnode=B(1) -> endnode=F(5)
        # runs until end node is reached
        while self.currentnode != self.endnode:
            if self.currentnode is not -1:
                # setting currentnode to true before calculating next node to visit
                self.nodetable[self.currentnode].visited = True
                self.calculate_tentative()
                self.determine_next_node()
                # prints calculations for each node
                print "Current Node:", self.currentnode, "(" + chr(self.currentnode+65) + ")"
                print "Distfromsource:", self.nodetable[self.currentnode].distfromsource, "\n"
            elif self.currentnode is -1:
                print "No shortest path found", "\n"
                return False

        if self.currentnode == self.endnode:
            self.nodetable[self.currentnode].visited = True
            print "End node reached", "\n"
            return True

    def return_shortest_path(self):
        # contains all methods in order to run program
        self.parse_route("parse_route.txt")
        self.populate_network("network.txt")
        self.populate_node_table()
        self.currentnode = self.startnode
        pathfound = self.calculate_shortest_path()  # returns true or false if path is found or not

        # if path is found, print information about the shortest path
        if pathfound is True:
            node = self.endnode
            totaldistance = self.nodetable[self.endnode].distfromsource
            self.route = []

            # traverses the end node's previous nodes to show shortest path
            self.route.append(chr(node+65))
            while node != self.startnode:
                node = self.nodetable[node].previous
                self.route.append(chr(node+65))

            print "Shortest Path:",
            for pathnode in self.route[::-1]:
                print pathnode,

            print "\nTotal distance:", totaldistance, "\n"


class MaxFlow(Dijkstra):  # Inherits from Dijkstra Class
    def __init__(self):
        '''initialise class'''
        Dijkstra.__init__(self)
        self.original_network = []

    def populate_network(self, filename):
        '''Dijkstra Method + need to make copy of original network (hint)'''
        Dijkstra.populate_network(self, filename)
        # need to store copy of self.network in self.original_network
        '''
        Note for original network, use to check if theres an augmented path
        and where the flows are before traversing
        '''
        self.original_network = self.network  # use to check if theres an augmented path and where the flows are

    def return_bottleneck_flow(self):
        '''determine the bottleneck flow of a given path'''
        currentprevious = self.endnode
        bottleneck = infinity

        # finds the bottleneck by checking for the smallest
        # edge value in shortest path by traversing end node's previous
        while currentprevious != self.startnode:
            if bottleneck > self.network[self.nodetable[currentprevious].previous][currentprevious]:
                bottleneck = self.network[self.nodetable[currentprevious].previous][currentprevious]
            currentprevious = self.nodetable[currentprevious].previous

        return bottleneck

    def remove_flow_capacity(self):
        '''remove flow from network and return both the path and the amount removed'''
        currentprevious = self.endnode
        bottleneck = self.return_bottleneck_flow()
        route = []

        # creates a multi-dimensional list that contains each path traversed
        # for the max flow calculations
        route.append(chr(currentprevious+65))
        while currentprevious != self.startnode:
            # takes away and adds capacity to opposite edges by the bottleneck
            # to be able to calculate the total maxflow in subsequent calculations
            # e.g [0, 2] [2, 0] becomes [2, 0], [0, 2]
            self.network[self.nodetable[currentprevious].previous][currentprevious] -= bottleneck
            self.network[currentprevious][self.nodetable[currentprevious].previous] += bottleneck
            currentprevious = self.nodetable[currentprevious].previous
            route.append(chr(currentprevious+65))

        route = route[::-1]  # reverse contents of list

        return bottleneck, route

    def return_max_flow(self):
        '''calculate max flow across network, from start to end and return
        both the max flow value and all the relevant paths'''
        Dijkstra.parse_route(self, "parse_route.txt")
        self.populate_network("directednetwork.txt")

        routes_taken = []
        maxflow = 0
        self.populate_node_table()
        self.currentnode = self.startnode
        pathfound = self.calculate_shortest_path()
        bottleneck, route = self.remove_flow_capacity()
        maxflow += bottleneck
        routes_taken.append(route)

        while pathfound is True:
            self.populate_node_table()
            self.currentnode = self.startnode
            pathfound = self.calculate_shortest_path()
            if pathfound is False:
                break
            bottleneck, route = self.remove_flow_capacity()
            maxflow += bottleneck
            routes_taken.append(route)

        print "Routes Taken:", routes_taken
        print "Maxflow:", maxflow

if __name__ == '__main__':
    Algorithm = Dijkstra()
    Algorithm.return_shortest_path()

    MaxFlow = MaxFlow()
    MaxFlow.return_max_flow()
