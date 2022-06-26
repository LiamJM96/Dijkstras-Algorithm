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
        #self.startnode = 1
        self.nodetable = []
        self.nodetable_populated = False

        if not self.network_populated:
            print "Network not populated!"
            return

        for node in self.network:
            self.nodetable.append(Node())
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
                startnode = ord(line[0]) - 65
                endnode = ord(line[-1]) - 65
                self.startnode = startnode
                self.endnode = endnode
                print "Path to take:", line
        except IOError:
            print "Parse route file could not be found"

    def return_near_neighbour(self):
        nearestneighbour = []
        for index, edge in enumerate(self.network[self.currentnode]):
            if edge > 0 and not self.nodetable[index].visited:
                nearestneighbour.append(index)
        return nearestneighbour

    def calculate_tentative(self):
        '''calculate tentative distance of nearest neighbours'''
        nearestneighbour = self.return_near_neighbour()

        for index in nearestneighbour:
            tentativedist = self.nodetable[self.currentnode].distfromsource + self.network[self.currentnode][index]
            if tentativedist < self.nodetable[index].distfromsource:
                self.nodetable[index].distfromsource = tentativedist
                self.nodetable[index].previous = self.currentnode

    def determine_next_node(self):
        '''determine next node to examine'''
        # the next node might not be a neighbour
        # a node that is unvisited and has the
        # shortest current distance from source
        bestdistance = infinity
        self.currentnode = invalid_node

        for nodeindex, node in enumerate(self.nodetable):
            if not node.visited and node.distfromsource < bestdistance:
                    bestdistance = node.distfromsource
                    self.currentnode = nodeindex

    def calculate_shortest_path(self):
        shortestpath = 0
        print "Calculating Shortest Path:"

        # currentnode=B(1) -> endnode=F(5)
        while self.currentnode != self.endnode:
            # setting currentnode to true before calculating next node to visit
            self.nodetable[self.currentnode].visited = True
            self.calculate_tentative()
            self.determine_next_node()
            print "Current Node:", self.currentnode
            print "Distfromsource:", self.nodetable[self.currentnode].distfromsource, "\n"

        if self.currentnode == self.endnode:
            self.nodetable[self.currentnode].visited = True
            print "End node reached"

    def return_shortest_path(self):
        node = self.endnode
        totaldistance = self.nodetable[self.endnode].distfromsource
        shortestpath = []

        shortestpath.append(chr(node+65))
        while node != self.startnode:
            node = self.nodetable[node].previous
            shortestpath.append(chr(node+65))

        print "Shortest Path:",
        for pathnode in shortestpath[::-1]:
            print pathnode,

        print "\nTotal distance:", totaldistance

if __name__ == '__main__':
    Algorithm = Dijkstra()
    Algorithm.parse_route("parse_route.txt")
    # B(1) -> F(5)
    Algorithm.populate_network("network.txt")
    Algorithm.populate_node_table()
    Algorithm.currentnode = Algorithm.startnode
    Algorithm.calculate_shortest_path()
    Algorithm.return_shortest_path()

    print "Distfromsource, Previous Node, Visited"
    for index, node in enumerate(Algorithm.nodetable):
        print chr(index+65) + ": ", node.distfromsource, node.previous, node.visited
