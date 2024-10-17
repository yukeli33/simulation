from ctypes import util
import math
import numpy as np
import networkx as nx
import numpy.random
# from collection import Counter
from collections import Counter
import tqdm 
# value of utility when safe versus unsafe.
U_1 = 5
U_0 = -5

# construct the edges for node G
def construct_edges(G,edges_w):
    for edge in edges_w:
        G.add_edge(edge[0],edge[1],rel = edge[2], rel_w = edge[3])
    return G

# initialize the graph G with power 
def initialize_graph(G=None, power=None,opinion= [],loc = []):
    for i in range(len(power)):
        G.add_node(i,power=0,status=0,d = np.zeros(len(power)), opinion = 0,loc = 0)
        G.nodes[i]['power'] = power[i]
        G.nodes[i]['d'][i] = power[i]
        if len(opinion)>0:
            # print(opinion[i])
            G.nodes[i]['opinion'] = opinion[i]
            # print('yes')
        if len(loc)>0:
            G.nodes[i]['loc'] = loc[i]
        i+=1
    return G

# calculate the support and threat of G
def cal_state(G,node):
    neighbors = list(nx.neighbors(G,node))
    support = 0
    threat = 0
    support +=  G.nodes[node]['d'][node]
    for n in neighbors:
        if G[n][node]['rel']>0:
            support += G.nodes[n]['d'][node]
        elif G[n][node]['rel']<0:
            support+= G.nodes[node]['d'][n]
            threat +=G.nodes[n]['d'][node]
    return support,threat

# update the status of G
def update_status(G):
    for node in G.nodes:
        s,t = cal_state(G,node)
        diff = (s-t)
        if diff>0:
            G.nodes[node]['status']= 1
        elif diff == 0:
            G.nodes[node]['status']= 0
        else:
            G.nodes[node]['status']= -1
    return G

# calculate the utility of node n
def cal_utility(G,n):
    # status = G[n]['status']
    neighbors = list(nx.neighbors(G,n))
    utility = 0
    if G.nodes[n]['status'] <0:
        utility = U_0
    else:
        for node in neighbors:
            if  G[n][node]['rel']>0:
                if G.nodes[node]['status']>=0:
                    utility += U_1*G[n][node]['rel_w']
                # else: utility += U_0
            elif  G[n][node]['rel']<0:
                if G.nodes[node]['status']<=0:
                    utility += U_1*G[n][node]['rel_w']
                # else: utility += U_0
    return utility

# generate new power distribution for node n
def generate_d(G,n):
    neighbors = list(nx.neighbors(G,n))
    distri = np.random.dirichlet(np.ones(len(neighbors)+1),size=(1))
    G.nodes[n]['d'] = np.zeros(len(G.nodes[n]['d']))
    for i in range(len(neighbors)):
        node = neighbors[i]
        G.nodes[n]['d'][node] = distri[0][i]*G.nodes[n]['power']
    G.nodes[n]['d'][n] = distri[0][len(neighbors)]*G.nodes[n]['power']
    return G



# steps Total number of updating steps
def power_allocation(G, steps = 500):
    equilibrium = []
    # flag for updating
    update = False

    G_n = G.copy()
    for t in range(steps):
        for node in G.nodes:
            # sample a new power distribution for node 
            G_n = generate_d(G_n,node)
            G_n = update_status(G_n)
            utility_n = cal_utility(G_n,node)
            utility = cal_utility(G,node)
            # if the utility get larger, update the graph
            if utility_n-utility>0.01:
                update=True
                G = G_n
            G_n = G.copy()
        if update == True:
            update = False
            continue
        else: 
            equilibrium.append(tuple(nx.get_node_attributes(G, 'status').values()))
    # for u in equilibrium:
    #     values = np.array(list(u.values()))
        #print('The equilibrium is ' + str(values) + ' safe pecent %.2f, unsafe pecent %.2f'%(sum(values==1)/len(values),(sum(values==-1)/len(values))))
    return equilibrium
        # print('The percentage of safe countries: ' + str(sum(values==1)/len(values)))
    # print('The percentage of unsafe countries: ' + str(sum(values==-1)/len(values)))
    # print('\n')
    # i+=1 
# neighbors = list(nx.neighbors(G,0))
# for n in neighbors:
#     if G[n][0]['rel']>0:
#         print(n)

# a = np.random.dirichlet(np.ones(2),size=(1))
# print(a)

# edges = [(0,1,-1,1),(0,3,1,1),(0,4,-1,1),(1,3,-1,1),(1,4,1,1),(2,3,-1,1),(2,4,-1,1),(2,5,-1,1),(3,4,1,1),(3,5,-1,1)]
# G = initialize_graph(G,power)
# G = construct_edges(G,edges)
# G = update_status(G)

