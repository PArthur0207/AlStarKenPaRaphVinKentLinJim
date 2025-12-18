from graph_detail import Graph
from stations import lrt1, lrt2, mrt3, interchanges

g = Graph()

for station in lrt1 + lrt2 + mrt3:
    g.add_vertex(station)

for line in [lrt1 + lrt2 + mrt3]:
    for i in range (len(line)-1) :
        g.add_edge(line[i], line[i+1])
        g.add_edge(line[i+1], line[i])

for a,b in interchanges:
    g.add_edge (a , b)            
    g.add_edge(b , a)           
    
start = input("Enter a starting station:")
end = input("Enter a destination:")

route = g.bfs (start, end)

print("Fastest route:")
if route:
    print ("-->".join(route))
else:
    print ("No route found")        