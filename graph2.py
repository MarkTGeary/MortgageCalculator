import csv
import matplotlib.pyplot as plt
import os

current_dir = os.path.dirname(__file__)

csv_filename = 'NAQ03.20250104T140139.csv'
file_path = os.path.join(current_dir, csv_filename)


#Clean the data and convert to dictionary
gnp_data = {}

try:
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            year = row['Quarter'][:4]  
            value = float(row['VALUE'])  
            gnp_data[year] = value
except FileNotFoundError:
    print("File not found:")

years = list(map(int, gnp_data.keys()))  
values = list(gnp_data.values())
#Code to make graph
plt.figure(figsize=(10, 6))
plt.bar(years, values, color='blue', alpha=0.7, label='GNP (in Euro Million)')

plt.title("Irish GNP at Current Market Prices (1995-2023)")
plt.xlabel("Year")
plt.ylabel("GNP €(000,000's)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=45)  
plt.legend()
plt.savefig('Artefact/Images/gnpGraph.png', dpi=300, bbox_inches='tight')
plt.show()
