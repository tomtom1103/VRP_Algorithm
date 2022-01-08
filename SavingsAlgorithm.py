import json
import util
import operator

with open('data_original.json') as inputFile:
    data = json.load(inputFile)

noOfCustomers = len(data["nodes"])
customerPosDemand = dict()
vehicleCap = data["vehicleCapacity"][0]["1"]
# print vehicleCap
for i in range(noOfCustomers):
    customerPosDemand[data["nodes"][i]["x"], data["nodes"][i]["y"]] = data["nodes"][i]["demand"]
print(customerPosDemand)

def computeSaving(depot, i, j):
    iDepot = util.euclideanDistance(i, depot)
    jDepot = util.euclideanDistance(depot, j)
    ijDist = util.euclideanDistance(i, j)

    return (iDepot + jDepot - ijDist)

savings = dict()
customerPositions = list(customerPosDemand.keys())

pointsLen = len(customerPositions)
depot = (data["depot"]["x"], data["depot"]["y"])

def allCustomersConsidered(customerServed):
    for val in customerServed.values():
        if val == False:
            return False
    return True

# Step 1
distanceDict = dict()
for i in range(pointsLen):
    for j in range(i + 1, pointsLen):
        distanceDict[(customerPositions[i], customerPositions[j])] = util.euclideanDistance(customerPositions[i], customerPositions[j])

# Step 2
for i in range(pointsLen):
    for j in range(i + 1, pointsLen):
        savings[(customerPositions[i], customerPositions[j])] = computeSaving(depot, customerPositions[i], customerPositions[j])
savings = sorted(savings.items(), key=operator.itemgetter(1), reverse=True)
l = len(savings)
cust_pairs = list()
for i in range(l):
    cust_pairs.append(savings[i][0])

# initially none of the customers have been isServed
customerServed = dict()
for c in customerPositions:
    customerServed[c] = False

# Step 3
def inPrevious(new, existing):
    start = existing[0]
    end = existing[len(existing) - 1]
    if new == start:
        return 1
    elif new == end:
        return 0
    else:
        return -1

def capacityValid(existing, new):
    totalCap = customerPosDemand[new]
    for c in existing:
        totalCap += customerPosDemand[c]

    return totalCap <= vehicleCap

def isServed(c):
    return customerServed[c]

def hasBeenServed(c):
    customerServed[c] = True

routes = dict()
l = len(cust_pairs)
i = 0
idx = -1
truck = [0, 0, 0, 0, 0]

while (not (allCustomersConsidered(customerServed))):
    # choosing the maximum savings customers who are unserved
    for c in cust_pairs:
        if (isServed(c[0]) == False and isServed(c[1]) == False):
            hasBeenServed(c[0])
            hasBeenServed(c[1])
            idx += 1
            routes[idx] = ([c[0], c[1]])
            break

    # finding a customer that is either at the start or end of previous route
    for c in cust_pairs:
        res = inPrevious(c[0], routes[idx])
        if res == 0 and capacityValid(routes[idx], c[1]) and (isServed(c[1]) == False):
            if c[1] == (13, 7):
                print(customerServed[c[1]])
            hasBeenServed(c[1])
            routes[idx].append(c[1])
        elif res == 1 and capacityValid(routes[idx], c[1]) and (isServed(c[1]) == False):
            if c[1] == (13, 7):
                print(customerServed[c[1]])
            hasBeenServed(c[1])
            routes[idx].insert(0, c[1])

        else:
            res = inPrevious(c[1], routes[idx])
            if res == 0 and capacityValid(routes[idx], c[0]) and (isServed(c[0]) == False):
                if c[0] == (13, 7):
                    print(customerServed[c[0]])
                hasBeenServed(c[0])
                routes[idx].append(c[0])
            elif res == 1 and capacityValid(routes[idx], c[0]) and (isServed(c[0]) == False):
                if c[0] == (13, 7):
                    print(customerServed[c[0]])
                hasBeenServed(c[0])
                routes[idx].insert(0, c[0])

for point in customerPosDemand.keys():
    print(f'point1: {point}')

for r in routes.values():
    for point in r:
        print(f'point2: {point}')

# printing each truck load
for r in routes.values():
    cap = 0
    for points in r:
        cap += customerPosDemand[points]
    print(f'cap: {cap}')

# adding depot at ends
for r in routes.values():
    util.addDepotAtEnds(depot, r)

totalDist = 0
for k, v in routes.items():
    totalDist += util.calculateRouteCost(v)
    print(k, "-", v)
print(f'totaldist: {totalDist}')
