import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
random.seed(10)


def create_map(d, hypothesis):
    '''
    The function is to create an if else ladder for iterating through different types of hypothesis parameters 'alcohol', 'distraction' and 'autonomous'.
    There h_multiplier multiplies with the number of cars. The multiplier for alcohol is 10 and with distraction is 15 because according to statistics obtained
    from 'Illinois Department of Transportation' and 'Illinois Tollway' and a few assumptions made for autonomous vehicles to reach a conclusion.

    :param d: Represents the Digraph Created for Testing a Hypothesis
    :param hypothesis: Hypothesis is the type of hypothesis under test (Alcohol, Distraction, Autonomous only)
    :return: The function returns a network graph with the hypothesis multiplier value depending upon the hypothesis.
    >>> d = nx.DiGraph()
    >>> len(create_map(d,"alcohol"))
    42
    '''
    if hypothesis == "alcohol":
        h_multiplier = 10
    elif hypothesis == "distraction":
        h_multiplier = 15
    elif hypothesis == "autonomous":
        h_multiplier = 0
    d = add_routes(d,h_multiplier)
    return d

def calculate_traffic(h_multiplier, roadtype):
    '''
    As part of this function, we assign traffic to each type of route and the number of cars satisfying the hypothesis parameter.
    For an InterState Type Road we have assumed the maximum traffic, followed by State Type Road and then to the City Roads.
    The cars satisfying the hypothesis parameter are also adjusted according to the type of road.

    :param h_multiplier: The h_multiplier variable is chosen in the create_map function it may vary according to the hypothesis under test
    :param roadtype: roadtype is variable which represents the different types of variables
    :return: A dictionary called car_stat is returned by the function
    >>> calculate_traffic(10,"State")
    {'h_param': 0, 'autonomous': 21, 'no_of_cars': 122}
    >>> calculate_traffic(0,"InterState")
    {'h_param': 0, 'autonomous': 22, 'no_of_cars': 374}
    '''
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
    """
    :param d: Represents the Digraph Created for Testing a Hypothesis
    :param h_multiplier: The h_multiplier variable is chosen in the create_map function it may vary according to the hypothesis under test
    :return: Returns a network digraph with added edges and attributes.
    >>> t = nx.DiGraph()
    >>> len(add_routes(t,10))
    42
    """
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
    '''
    As part of the initialize map function we have used a Network DiGraph as our principle data structure to create
    The edges the represent the following attributes types of routes, the amount of traffic, number of cars with the
    hypothesis parameter. For example, cars in which drivers are under influence of alcohol or are distracted driving
    or cars which are autonomous.

    :param hypothesis: Hypothesis represents the hypothesis under test which may be 'alchohol' or any of the three hypothesis.
    :return: The function returns a created map with all the routes added
    '''
    d = nx.DiGraph()
    # d = add_counties(d)
    d = create_map(d, hypothesis)
    return d


def accidents_per_edge(edgestat,hypothesis):
    """
    In this function we calculate the accidents happening per edge or per route depending upon the type of
    hypothesis. The formula is based upon facts and figures obtained from 'Illinois Department of Transportation' and
    'Illinois Tollway' and a few assumptions made for autonomous vehicles to reach the conclusion for the hypothesis.

    :param edgestat: edgestat is a dictionary which is being passed, this dictionary is the output of the assign_traffic function
    :param hypothesis:Hypothesis represents the hypothesis under test which may be 'alcohol' or any of the three hypothesis.
    :return: The function returns a randomly generated number (samples from a parameterized binomial distribution)

    >>> type(accidents_per_edge({'h_param': 9, 'autonomous': 11, 'no_of_cars': 209},'alcohol'))
    <class 'int'>
    """
    if hypothesis == "alcohol":
        return (np.random.binomial(edgestat[next(iter(edgestat))], 0.033) + np.random.binomial(edgestat['autonomous'],0.02) + np.random.binomial(edgestat['no_of_cars'] - edgestat['autonomous'] - edgestat[next(iter(edgestat))], 0.03))
    elif hypothesis == "distraction":
        return (np.random.binomial(edgestat[next(iter(edgestat))], 0.0324) + np.random.binomial(edgestat['autonomous'],0.02) + np.random.binomial(edgestat['no_of_cars'] - edgestat['autonomous'] - edgestat[next(iter(edgestat))], 0.03))
    else:
        return (np.random.binomial(edgestat['autonomous'],0.02) + np.random.binomial(edgestat['no_of_cars'] - edgestat['autonomous'], 0.03))

#Assumption: If there are 100 vehicles, 10 collisions happen then out of those 10 collisions, 3 are due to alchohol
#and 7 due to other causes

def accidents_per_roadtype(d,hypothesis):
    """
    In this function we have calculated and stored the total number of accidents happening per road type.

    :param d: Represents the Digraph Created for Testing a Hypothesis
    :param hypothesis: Hypothesis represents the hypothesis under test which may be 'alcohol' or any of the three hypothesis.
    :return: All values of accidents are stored in a dictionary called cumulative_stat.
    """
    cumulative_stat = {'State': 0, 'InterState': 0, 'City': 0}
    for i in range(0, len(d.edges(data=True))):
        if list(d.edges(data=True))[i][2]['type'] == 'State':
            cumulative_stat['State'] += accidents_per_edge((list(d.edges(data=True))[i])[2]['car_stat'], hypothesis)
        elif list(d.edges(data=True))[i][2]['type'] == 'InterState':
            cumulative_stat['InterState'] += accidents_per_edge((list(d.edges(data=True))[i])[2]['car_stat'],
                                                                hypothesis)
        else:
            cumulative_stat['City'] += accidents_per_edge((list(d.edges(data=True))[i])[2]['car_stat'], hypothesis)
    return (cumulative_stat)


def route_display(d):
    '''
    In this function we are displaying or visualizing the networkx graph created for the hypothesis under test.
    :param d: Represents the Digraph Created for Testing a Hypothesis
    :return: The function returns no value but prints the networkx graph plot
    '''
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
    """
    The run experiment function runs the hypothesis for a specific time period. In our case '182' represents the
    number of days for which the experiment is running. These results are stored in a pandas dataframe in the
    columns 'State', Interstate' and 'City'. The functions helps to calculate the minimum value, maximum value,
    median and mean of the dataframe
    :param hypothesis: hypothesis: Hypothesis represents the hypothesis under test which may be
    'alcohol' or any of the three hypothesis.
    :return: List consisting of total number of accidents.
    """
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
    #route_display(d)
    return list(df_final['Total'])


# Main Function
if __name__ == "__main__":
    no_of_days = list(range(1,366))
    print("Accidents on State,Interstate and City due to Alcohol:")
    alcohol = run_experiment("alcohol")

    print("Accidents on State,Interstate and City due to Distraction")
    distraction = run_experiment("distraction")

    print("Accidents on State,Interstate and City due to Autonomous")
    autonomous = run_experiment("autonomous")

    plt.plot(no_of_days,alcohol, label = "Alcohol")
    plt.plot(no_of_days, distraction,label = "Distraction")
    plt.plot(no_of_days, autonomous , label = "Autonomous")
    plt.xlabel("Days")
    plt.ylabel("Accidents")
    plt.legend()
    plt.show()

