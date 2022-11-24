import json
import seaborn as sns
import matplotlib.pyplot as plt


with open("KIRO-medium.json", "r") as read_file:
    data = json.load(read_file)


# PARAMETERS
parameters = data["parameters"]
buildingcosts = parameters["buildingCosts"]
productioncosts = parameters["productionCosts"]
routingcosts = parameters["routingCosts"]
capacitycost = parameters["capacityCost"]
capacities = parameters["capacities"]

# CLIENTS
clients = data["clients"]
nb_clients = len(clients)

# SITE-SITE DISTANCES
ss_distances = data["siteSiteDistances"]
nb_sites = len(ss_distances)

# SITE-CLIENT DISTANCES
sc_distances = data["siteClientDistances"]

# COST FUNCTION


def cost(p, d, auto, p_d, s_i):

    total_cost = 0

    # Building Costs
    for s in p:
        total_cost += buildingcosts["productionCenter"] + auto[s] * buildingcosts["automationPenalty"]

    total_cost += buildingcosts["distributionCenter"] * len(d)

    # Production Costs
    for i in range(nb_clients):
        if s_i[i] in p:
            total_cost += clients[i]["demand"] * (productioncosts["productionCenter"] - auto[s_i[i]] * productioncosts["automationBonus"])
        else:
            total_cost += clients[i]["demand"] * (productioncosts["productionCenter"] - auto[p_d[s_i[i]]] * productioncosts["automationBonus"] + productioncosts["distributionCenter"])

    # Routing Costs
    for i in range(nb_clients):
        if s_i[i] in p:
            total_cost += clients[i]["demand"] * routingcosts["secondary"] * sc_distances[s_i[i]][i]
        else:
            total_cost += clients[i]["demand"] * (routingcosts["primary"] * ss_distances[p_d[s_i[i]]][s_i[i]] + routingcosts["secondary"] * sc_distances[s_i[i]][i])

    # Capacity Costs
    for s in p:
        for i in range(nb_clients):
            if s_i[i] == s or (s_i[i] in d and p_d[s_i[i]]):
                total_cost += capacitycost * max(clients[i]["demand"] - capacities["productionCenter"] - auto[s] * capacities["automationBonus"], 0)

    return total_cost


# ENCODE FUNCTION

def encode_data(p, d, auto, p_d, s_i):

    answer = {
        "productionCenters": [],
        "distributionCenters": [],
        "clients": []
    }
    for s in p:
        s_dict = {
            "id": s+1,
            "automation": auto[s]
        }
        answer["productionCenters"].append(s_dict)

    for s in d:
        s_dict = {
            "id": s+1,
            "parent": p_d[s]+1
        }
        answer["distributionCenters"].append(s_dict)

    for i in range(nb_clients):
        i_dict = {
            "id": i+1,
            "parent": s_i[i]+1
        }
        answer["clients"].append(i_dict)

    return answer


"""
# TINY EXAMPLE

P = [0]
D = []
Auto = [0]
P_d = []
S_i = [0, 0, 0]

print(cost(P, D, Auto, P_d, S_i))

with open("answer_file.json", "w") as write_file:
    json.dump(encode_data(P, D, Auto, P_d, S_i), write_file, indent=4)
"""
