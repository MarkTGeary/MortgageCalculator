import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from collections import defaultdict
import numpy as np
import json
import os

current_dir = os.path.dirname(__file__)
csv_filename = 'HSA06.20250102T160128.csv'
file_path = os.path.join(current_dir, csv_filename)

#Clean the data from the dataset and convert it to a dictionary
def csv_to_grouped_dict(file_path):
    grouped_data = defaultdict(lambda: defaultdict(list))
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                year = int(row['Year'])
                value = int(row['VALUE'])
                area = row['Area']
            except:
                print("Value Invalid. Removing value from dictionary")
            grouped_data[area]['Year'].append(year)
            grouped_data[area]['VALUE'].append(value)
    return grouped_data

#Code to make the graph
def format_yaxis(value, tick_number):
    return f'{value / 1000:.0f}'

def plot_grouped_data(grouped_data):
    plt.figure(figsize=(12, 8))
    
    for area, data in grouped_data.items():
        plt.plot(data['Year'], data['VALUE'], marker='o', label=area)
    
    plt.xlabel('Year')
    plt.ylabel("€ (000's)")
    plt.title('Housing Prices By Year By Area')
    plt.grid(True)
    plt.legend(title='Area', loc='upper left')
    
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_yaxis))
    plt.savefig('Artefact/Images/HousingPriceGraph.png', dpi=300, bbox_inches='tight')
    plt.show()

grouped_data = csv_to_grouped_dict(file_path)
plot_grouped_data(grouped_data)

#Calculate the average inflation per year
def calculate_slopes(grouped_data):
    slopes = {}
    for area, data in grouped_data.items():
        years = np.array(data['Year'])
        values = np.array(data['VALUE'])
        if len(years) > 1:  
            slope = np.polyfit(years, values, 1).tolist()  
            slopes[area] = slope
    return slopes

slopes = calculate_slopes(grouped_data)

os.makedirs('Artefact', exist_ok=True)  
output_json_path = 'Artefact/inflation.json'
with open(output_json_path, 'w') as json_file:
    json.dump(slopes, json_file, indent=4)