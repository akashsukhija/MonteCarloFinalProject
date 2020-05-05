import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
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

def calculate_traffic(h_multiplier, roadtype):
    car_stat = {}
    if h_multiplier == 0 and roadtype == "State":
        car_stat = {"h_param": 0,"autonomous":random.randint(100, 250), "no_of_cars": random.randint(1000, 2500)}
    elif roadtype == "State":
        car_stat = {"h_param": random.randint(0, h_multiplier),"autonomous":random.randint(100, 250), "no_of_cars": random.randint(1000, 2500)}
    elif h_multiplier == 0 and roadtype == "InterState":
        car_stat = {"h_param": 0, "autonomous":random.randint(100, 250), "no_of_cars": random.randint(1500, 5000)}
    elif roadtype == "InterState":
        car_stat = {"h_param": random.randint(h_multiplier - 50, h_multiplier * 3), "autonomous":random.randint(100, 250), "no_of_cars": random.randint(1500, 5000)}
    elif h_multiplier == 0 and roadtype == "City":
        car_stat = {"h_param": 0, "autonomous":random.randint(100, 250), "no_of_cars": random.randint(500, 2000)}
    else:
        car_stat = {"h_param": random.randint(0, h_multiplier - 50), "autonomous":random.randint(100, 250), "no_of_cars": random.randint(500, 2000)}
    return car_stat

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
        car_stat = calculate_traffic(h_multiplier,"State")
        distance = random.uniform(15, 25)
        d.add_edge(counties[i], counties[i - 1], weight=distance, type="State", car_stat=car_stat)
        d.add_edge(counties[i - 1], counties[i], weight=distance, type="State", car_stat=car_stat)
    distance = random.uniform(15, 25)
    car_stat = calculate_traffic(h_multiplier,"State")
    d.add_edge(counties[0], counties[i], weight=distance, type="State", car_stat=car_stat)
    d.add_edge(counties[i], counties[0], weight=distance, type="State", car_stat=car_stat)

    # InterState Roads
    for i in range(1, 10):
        distance = random.uniform(75, 100)
        car_stat = calculate_traffic(h_multiplier, "InterState")
        d.add_edge(counties[i * 3], counties[i * 3 - 3], weight=distance, type="InterState",car_stat=car_stat)
        d.add_edge(counties[(i * 3) - 3], counties[(i * 3)], weight=distance, type="InterState",car_stat=car_stat)

    for i in range(1, 9):
        distance = random.uniform(100, 125)
        car_stat = calculate_traffic(h_multiplier, "InterState")
        d.add_edge(counties[i * 4], counties[(i * 4) - 4], weight=distance, type="InterState", car_stat=car_stat)
        d.add_edge(counties[(i * 4) - 4], counties[(i * 4)], weight=distance, type="InterState", car_stat=car_stat)

    # City Roads
    for i in range(1, 7):
        distance = random.uniform(100, 125)
        car_stat = calculate_traffic(h_multiplier, "City")
        d.add_edge(counties[i * 5], counties[(i * 5) - 5 - i], weight=distance, type="city", car_stat=car_stat)
        d.add_edge(counties[(i * 5) - 5 - i], counties[(i * 5)], weight=distance, type="city", car_stat=car_stat)
    for i in range(1, 6):
        distance = random.uniform(150, 175)
        car_stat = calculate_traffic(h_multiplier, "City")
        d.add_edge(counties[i * 6], counties[(i * 6) - 6 - i], weight=distance, type="city", car_stat=car_stat)
        d.add_edge(counties[(i * 6) - 6 - i], counties[(i * 6)], weight=distance, type="city", car_stat=car_stat)
    return d


def initializemap(hypothesis):
  d = nx.DiGraph()
  #d = add_counties(d)
  d = create_map(d,hypothesis)
  return d


def accidents_per_edge(edgestat,hypothesis):
    if hypothesis == "alcohol":
        return (np.random.binomial(edgestat[next(iter(edgestat))], 0.033) + np.random.binomial(edgestat['autonomous'],0.02) + np.random.binomial(edgestat['no_of_cars'] - edgestat['autonomous'] - edgestat[next(iter(edgestat))], 0.03))
    elif hypothesis == "distraction":
        return (np.random.binomial(edgestat[next(iter(edgestat))], 0.0324) + np.random.binomial(edgestat['autonomous'],0.02) + np.random.binomial(edgestat['no_of_cars'] - edgestat['autonomous'] - edgestat[next(iter(edgestat))], 0.03))
    else:
        return (np.random.binomial(edgestat['autonomous'],0.02) + np.random.binomial(edgestat['no_of_cars'] - edgestat['autonomous'], 0.03))

#Assumption: If there are 100 vehicles, 10 collisions happen then out of those 10 collisions, 3 are due to alchohol
#and 7 due to other causes

def accidents_per_roadtype(d,hypothesis):
  cumulative_stat = {'State': 0,'InterState': 0 , 'City': 0}
  for i in range(0,len(d.edges(data=True))):
    if list(d.edges(data=True))[i][2]['type'] == 'State':
      cumulative_stat['State'] += accidents_per_edge((list(d.edges(data=True))[i])[2]['car_stat'],hypothesis)
    elif list(d.edges(data=True))[i][2]['type'] == 'InterState':
      cumulative_stat['InterState'] += accidents_per_edge((list(d.edges(data=True))[i])[2]['car_stat'],hypothesis)
    else:
      cumulative_stat['City'] += accidents_per_edge((list(d.edges(data=True))[i])[2]['car_stat'],hypothesis)
  return(cumulative_stat)


def route_display(d):
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
    nx.draw(d, pos=my_pos, with_labels=True, node_color='red', node_size=400, edge_color=edge_color, linewidths=1,
            font_size=15)
    plt.show()


# Main Function
if __name__ == "__main__":
    i = 0
    j = 0
    k = 0
    data1 = {}
    data2 = {}
    data3 = {}
    df_final1 = pd.DataFrame(columns=['State', 'InterState', 'City'])
    df_final2 = pd.DataFrame(columns=['State', 'InterState', 'City'])
    df_final3 = pd.DataFrame(columns=['State', 'InterState', 'City'])
    # d = initializemap("alcohol")

    print("Accidents on State,Interstate and City due to Alcohol")

    while i <= 999:
        d = initializemap("alcohol")
        data1 = accidents_per_roadtype(d, "alcohol")
        df = pd.DataFrame([data1], columns=data1.keys())
        df_final1 = pd.concat([df_final1, df])
        i = i + 1
    df_final1.agg({'State': ['min', 'max', 'median', 'skew'], 'InterState': ['min', 'max', 'median', 'mean'],
                   'City': ['min', 'max', 'median', 'mean']})
    df_final1.iloc[0:0]
    print(df_final1)

    route_display(d)
    # p = nx.get_edge_attributes(d,"car_stat")
    # print (p)
    print("Accidents on State,Interstate and City due to Distraction")

    while j <= 999:
        d = initializemap("distraction")
        data2 = accidents_per_roadtype(d, "distraction")
        df = pd.DataFrame([data2], columns=data2.keys())
        df_final2 = pd.concat([df_final2, df])
        j = j + 1
    df_final2.agg({'State': ['min', 'max', 'median', 'skew'], 'InterState': ['min', 'max', 'median', 'mean'],
                   'City': ['min', 'max', 'median', 'mean']})
    df_final2.iloc[0:0]
    print(df_final2)
    route_display(d)

    # q = nx.get_edge_attributes(d,"car_stat")
    # print (q)
    print("Accidents on State,Interstate and City due to Autonomous")
    while k <= 999:
        d = initializemap("autonomous")
        data3 = accidents_per_roadtype(d, "Autonomous")
        df = pd.DataFrame([data3], columns=data3.keys())
        df_final3 = pd.concat([df_final3, df])
        k = k + 1
    df_final3.agg({'State': ['min', 'max', 'median', 'skew'], 'InterState': ['min', 'max', 'median', 'mean'],
                   'City': ['min', 'max', 'median', 'mean']})
    df_final3.iloc[0:0]
    print(df_final3)
    route_display(d)

    # r = nx.get_edge_attributes(d,"car_stat")
    # print (r)

