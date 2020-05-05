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
        h_multiplier = 10
    elif hypothesis == "distraction":
        h_multiplier = 15
    elif hypothesis == "autonomous":
        h_multiplier = 0
    d = add_routes(d,h_multiplier)
    return d

def calculate_traffic(h_multiplier, roadtype):
    car_stat = {}
    if h_multiplier == 0 and roadtype == "State":
        car_stat = {"h_param": 0,"autonomous":random.randint(10, 25), "no_of_cars": random.randint(100, 250)}
    elif roadtype == "State":
        car_stat = {"h_param": random.randint(0, h_multiplier),"autonomous":random.randint(10, 25), "no_of_cars": random.randint(100, 250)}
    elif h_multiplier == 0 and roadtype == "InterState":
        car_stat = {"h_param": 0, "autonomous":random.randint(10, 25), "no_of_cars": random.randint(150, 500)}
    elif roadtype == "InterState":
        car_stat = {"h_param": random.randint(h_multiplier - 5, h_multiplier * 3), "autonomous":random.randint(10, 25), "no_of_cars": random.randint(150, 500)}
    elif h_multiplier == 0 and roadtype == "City":
        car_stat = {"h_param": 0, "autonomous":random.randint(10, 25), "no_of_cars": random.randint(50, 200)}
    else:
        car_stat = {"h_param": random.randint(0, h_multiplier - 5), "autonomous":random.randint(10, 25), "no_of_cars": random.randint(50, 200)}
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

def run_experiment(hypothesis):
    data = {}
    df_final = pd.DataFrame(columns=['State', 'InterState', 'City'])

    for i in range(365):
        d = initializemap(hypothesis)
        data = accidents_per_roadtype(d, hypothesis)
        df = pd.DataFrame([data], columns=data.keys())
        df_final = pd.concat([df_final, df])

    alcohol_stats = df_final.agg(
        {'State': ['min', 'max', 'median', 'mean'], 'InterState': ['min', 'max', 'median', 'mean'],
         'City': ['min', 'max', 'median', 'mean']})

    df_final['Total'] = df_final['State'] + df_final['InterState'] + df_final['City']
    print(df_final)
    print(alcohol_stats)
    df_final.iloc[0:0]
    route_display(d)


# Main Function
if __name__ == "__main__":
    print("Accidents on State,Interstate and City due to Alcohol:")
    run_experiment("alcohol")

    print("Accidents on State,Interstate and City due to Distraction")
    run_experiment("distraction")

    print("Accidents on State,Interstate and City due to Autonomous")
    run_experiment("autonomous")

