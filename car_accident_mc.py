import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
random.seed(10)


def create_map(d, hypothesis):
    # car_stat = {"no_of_cars" : 1000, "h_param": 50}
    # State Roads
    if hypothesis == "alcohol":
        h_multiplier = 100
    elif hypothesis == "distraction":
        h_multiplier = 150
    elif hypothesis == "autonomous":
        h_multiplier = 0
    d = add_routes(d,h_multiplier)
    return d

def add_routes(d,h_multiplier):
    random.seed(10)
    counties = ['Adams', 'Alexander', 'Bond', 'Boone', 'Brown', 'Bureau', 'Calhoun', 'Carroll', 'Cass', 'Champaign',
                'Christian', 'Clark', 'Clay', 'Clinton', 'Coles', 'Cook', 'Crawford', 'Cumberland', 'DeKalb', 'De Witt',
                'Douglas', 'Dupage',
                'Edgar', 'Edwards', 'Effingham',
                'Fayette', 'Ford', 'Franklin', 'Fulton', 'Gallatin', 'Greene', 'Grundy', 'Hamilton', 'Hancock',
                'Hardin', 'Henderson', 'Henry', 'Iroquois', 'Jackson',
                'Jasper', 'Jefferson', 'Jersey', 'Jo Daviess', 'Johnson', 'Kane', 'Kankakee', 'Kendall', 'Knox', 'Lake',
                'LaSalle', 'Lawrence', 'Lee', 'Livingston', 'Logan',
                'Macon', 'Macoupin', 'Madison', 'Marion', 'Marshall', 'Mason', 'Massac', 'McDonough', 'McHenry',
                'McLean', 'Menard', 'Mercer', 'Monroe', 'Montgomery', 'Morgan',
                'Moultrie', 'Ogle', 'Peoria', 'Perry', 'Piatt', 'Pike', 'Pope', 'Pulaski', 'Putnam', 'Randolph',
                'Richland', 'Rock Island', 'Saline', 'Sangamon', 'Schuyler',
                'Scott', 'Shelby', 'St. Clair', 'Stark', 'Stephenson', 'Tazewell', 'Union', 'Vermilion', 'Wabash',
                'Warren', 'Washington', 'Wayne', 'White', 'Whiteside', 'Will',
                'Williamson', 'Winnebago', 'Woodford']
    counties = counties[:42]
    for i in range(1, len(counties)):
        distance = random.uniform(15, 25)
        if h_multiplier == 0:
            state_car_stat = {"h_param": 0, "no_of_cars": random.randint(1000, 2500)}
        else:
            state_car_stat = {"h_param": random.randint(0, h_multiplier), "no_of_cars": random.randint(1000, 2500)}
        d.add_edge(counties[i], counties[i - 1], weight=distance, type="State", car_stat=state_car_stat)
        d.add_edge(counties[i - 1], counties[i], weight=distance, type="State", car_stat=state_car_stat)
    distance = random.uniform(15, 25)
    if h_multiplier == 0:
        state_car_stat = {"h_param": 0, "no_of_cars": random.randint(1000, 2500)}
    else:
        state_car_stat = {"h_param": random.randint(0, h_multiplier), "no_of_cars": random.randint(1000, 2500)}
    d.add_edge(counties[0], counties[i], weight=distance, type="State", car_stat=state_car_stat)
    d.add_edge(counties[i], counties[0], weight=distance, type="State", car_stat=state_car_stat)

    # InterState Roads
    for i in range(1, 10):
        distance = random.uniform(75, 100)
        if h_multiplier == 0:
            interstate_car_stat = {"h_param": 0,"no_of_cars": random.randint(1500, 5000)}
        else:
            interstate_car_stat = {"h_param": random.randint(h_multiplier - 50, h_multiplier * 3), "no_of_cars": random.randint(1500, 5000)}
        d.add_edge(counties[i * 3], counties[i * 3 - 3], weight=distance, type="InterState",car_stat=interstate_car_stat)
        d.add_edge(counties[(i * 3) - 3], counties[(i * 3)], weight=distance, type="InterState",car_stat=interstate_car_stat)

    for i in range(1, 9):
        distance = random.uniform(100, 125)
        if h_multiplier == 0:
            interstate_car_stat = {"h_param": 0, "no_of_cars": random.randint(1500, 5000)}
        else:
            interstate_car_stat = {"h_param": random.randint(h_multiplier - 50, h_multiplier * 3), "no_of_cars": random.randint(1500, 5000)}
        d.add_edge(counties[i * 4], counties[(i * 4) - 4], weight=distance, type="InterState", car_stat=interstate_car_stat)
        d.add_edge(counties[(i * 4) - 4], counties[(i * 4)], weight=distance, type="InterState", car_stat=interstate_car_stat)

    # City Roads
    for i in range(1, 7):
        distance = random.uniform(100, 125)
        if h_multiplier == 0:
            city_car_stat = {"h_param": 0, "no_of_cars": random.randint(500, 2000)}
        else:
            city_car_stat = {"h_param": random.randint(0, h_multiplier - 50), "no_of_cars": random.randint(500, 2000)}
        d.add_edge(counties[i * 5], counties[(i * 5) - 5 - i], weight=distance, type="city", car_stat=city_car_stat)
        d.add_edge(counties[(i * 5) - 5 - i], counties[(i * 5)], weight=distance, type="city", car_stat=city_car_stat)
    for i in range(1, 6):
        distance = random.uniform(150, 175)
        if h_multiplier == 0:
            city_car_stat = {"h_param": 0, "no_of_cars": random.randint(500, 2000)}
        else:
            city_car_stat = {"h_param": random.randint(0, h_multiplier - 50), "no_of_cars": random.randint(500, 2000)}
        d.add_edge(counties[i * 6], counties[(i * 6) - 6 - i], weight=distance, type="city", car_stat=city_car_stat)
        d.add_edge(counties[(i * 6) - 6 - i], counties[(i * 6)], weight=distance, type="city", car_stat=city_car_stat)
    return d



# First Function
def initializemap(hypothesis):
  d = nx.DiGraph()
  #d = add_counties(d)
  d = create_map(d,hypothesis)
  return d

#Fifth Function
def accidents_per_edge(edgestat,hypothesis):
    if hypothesis == "alcohol":
        return (np.random.binomial(edgestat[next(iter(edgestat))], 0.033) + np.random.binomial(edgestat['no_of_cars'] - edgestat[next(iter(edgestat))], 0.03))
    elif hypothesis == "distraction":
        return (np.random.binomial(edgestat[next(iter(edgestat))], 0.0324) + np.random.binomial(edgestat['no_of_cars'] - edgestat[next(iter(edgestat))], 0.03))
    else:
        return (np.random.binomial(0, 0.1) + np.random.binomial(edgestat['no_of_cars'], 0.03))

#Assumption: If there are 100 vehicles, 10 collisions happen then out of those 10 collisions, 3 are due to alchohol
#and 7 due to other causes

#Fourth Function
def accidents_per_roadtype(d,hypothesis):
  cumulative_stat = {'State': 0,'InterState': 0 , 'City': 0}
  for i in range(0,len(d.edges(data=True))):
    if list(d.edges(data=True))[i][2]['type'] == 'State':
      cumulative_stat['State'] += accidents_per_edge((list(d.edges(data=True))[i])[2]['car_stat'],hypothesis)
    elif list(d.edges(data=True))[i][2]['type'] == 'InterState':
      cumulative_stat['InterState'] += accidents_per_edge((list(d.edges(data=True))[i])[2]['car_stat'],hypothesis)
    else:
      cumulative_stat['City'] += accidents_per_edge((list(d.edges(data=True))[i])[2]['car_stat'],hypothesis)
  print(cumulative_stat)


#Main Function
if __name__ == "__main__":
    d = initializemap("alcohol")
    my_pos = nx.spring_layout(d, seed=50)
    edge_color = []
    mapdict = (nx.get_edge_attributes(d, "type"))
    for key in mapdict:
        if mapdict[key] == "InterState":
            edge_color.append("green")
        elif mapdict[key] == "city":
            edge_color.append("orange")
        else:
            edge_color.append("blue")
    nx.draw(d, pos=my_pos, with_labels=True, node_color='red', node_size=400, edge_color=edge_color, linewidths=1, font_size=15)
    plt.show()
    print("Accidents on State,Interstate and City due to Alcohol")
    d = initializemap("alcohol")
    accidents_per_roadtype(d, "alcohol")
    # p = nx.get_edge_attributes(d,"car_stat")
    # print (p)
    print("Accidents on State,Interstate and City due to Distraction")
    d = initializemap("distraction")
    accidents_per_roadtype(d, "distraction")
    # q = nx.get_edge_attributes(d,"car_stat")
    # print (q)
    print("Accidents on State,Interstate and City due to Neutral")
    d = initializemap("autonomous")
    accidents_per_roadtype(d, "Autonomous")
    # r = nx.get_edge_attributes(d,"car_stat")
    # print (r)

