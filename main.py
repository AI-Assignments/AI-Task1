# import the network
import networkx as nx
import matplotlib.pyplot as plt
from classess.bfs import BfsTraverser

g=nx.Graph();

nodes=["Sports_complex","Siwaka","Ph1A","Ph1B","STC","Phase2","J1","Mada","Phase3","ParkingLot"]
g.add_nodes_from(nodes)
print(g.nodes())

g.add_edge("Sports_complex","Siwaka",weight="450")
g.add_edge("Siwaka","Ph1A",weight="10")
g.add_edge("Siwaka","Ph1B",weight="230")
g.add_edge("Ph1A","Ph1B",weight="100")
g.add_edge("Ph1A","Mada",weight="850")
g.add_edge("Ph1B","STC",weight="50")
g.add_edge("Ph1B","Phase2",weight="112")
g.add_edge("Phase2","J1",weight="600")
g.add_edge("Phase2","Phase3",weight="500")
g.add_edge("STC","ParkingLot",weight="250")
g.add_edge("Phase3","ParkingLot",weight="350")
g.add_edge("Mada","ParkingLot",weight="700")
g.add_edge("J1","Mada",weight="200")

g.nodes["Sports_complex"]['pos']=(-8,4)
g.nodes["Siwaka"]['pos']=(-4,4)
g.nodes["Ph1A"]['pos']=(0,4)
g.nodes["Ph1B"]['pos']=(0,0)
g.nodes["STC"]['pos']=(0,-4)
g.nodes["Phase2"]['pos']=(4,0)
g.nodes["J1"]['pos']=(8,-4)
g.nodes["Mada"]['pos']=(8,0)
g.nodes["Phase3"]['pos']=(12,0)
g.nodes["ParkingLot"]['pos']=(8,-8 )

#store all the positions in a variable
node_pos = nx.get_node_attributes(g,'pos')
#call BFS to return set of all possible routes to the goal
route_bfs = BfsTraverser()
routes = route_bfs.BFS(g,"Sports_complex","ParkingLot")
print(route_bfs.visited)
route_list = route_bfs.visited
#color the nodes in the route_bfs
node_col = ['darkturquoise' if not node in route_list else 'peru' for node in g.nodes()]
peru_colored_edges = list(zip(route_list,route_list[1:]))
#color the edges as well
#print(peru_colored_edges)
edge_col = ['darkturquoise' if not edge in peru_colored_edges else 'peru' for edge in g.edges()]
arc_weight=nx.get_edge_attributes(g,'weight')
nx.draw_networkx(g, node_pos,node_color= node_col, node_size=450)
nx.draw_networkx_edges(g, node_pos,width=2,edge_color= edge_col)
#nx.draw_networkx_edge_labels(g, node_pos,edge_color= edge_col, edge_labels=arc_weight)

nx.draw_networkx_edge_labels(g, node_pos, edge_labels=arc_weight)
plt.axis('off')
plt.show()



