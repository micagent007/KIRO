import json


with open("tiny1.json", "r") as read_file:
    data = json.load(read_file)


# PARAMETERS
parameters = data["parameters"]
jobs = data["jobs"]
tasks = data["tasks"]
J = len(jobs)
I = len(tasks)
size = parameters["size"]
costs = parameters["costs"]
release_date = [jobs[j]["release_date"] for j in range(J)]
due_date = [jobs[j]["due_date"] for j in range(J)]
weight = [jobs[j]["weight"] for j in range(J)]
sequence = [jobs[j]["sequence"] for j in range(J)]


# COST FUNCTION

alpha = costs["unit_penalty"]
beta = costs["tardiness"]


def cost(b):

    total_cost = 0

    for j in range(J):
        cj = b[sequence[j][-1]-1] + tasks[sequence[j][-1]-1]["processing_time"]
        tj = max(0, cj - due_date[j])
        if cj > due_date[j]:
            uj = 1
        else:
            uj = 0
        total_cost += weight[j] * (cj + alpha * uj + beta * tj)

    return total_cost


# ENCODE FUNCTION

def encode_data(b, m, o):

    answer = []

    for i in range(I):
        task_i = {
            "task": i+1,
            "start": b[i],
            "machine": m[i],
            "operator": o[i]
        }
        answer.append(task_i)

    return answer


#CHECK FUNCTION


def check(b, m, o):
    check = True
    for j in range(J):
        check = check and (b[sequence[j][0]-1] >= release_date[j])
        for i in range(len(sequence[j])-1):
            check = check and (b[sequence[j][i+1]-1] >= b[sequence[j][i]-1] + tasks[sequence[j][i]-1]["processing_time"])
    
    for i in range(I):
        for j in range(i+1, I):
            if m[i] == m[j] or o[i] == o[j]:
                check = check and (b[i] >= b[j] + tasks[j]["processing_time"]) and (b[i] + tasks[i]["processing_time"] <= b[j])
    return check


B = [0, 8, 14]
M = [2, 1, 1]
O = [1, 1, 1]

print(cost(B))

if check(B, M, O):
    print("JE TENCULE")

with open("answer_file.json", "w") as write_file:
    json.dump(encode_data(B, M, O), write_file, indent=4)
