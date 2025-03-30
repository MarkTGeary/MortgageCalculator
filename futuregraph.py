import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import pearsonr

# Get current directory for file paths
current_dir = os.path.dirname(__file__)

# Read the housing prices data
housing_file = os.path.join(current_dir, 'HSA06.20250102T160128.csv')
housing_data = pd.read_csv(housing_file)

# Filter for National New House Prices
national_data = housing_data[
    (housing_data['Statistic Label'] == 'New House Prices') & 
    (housing_data['Area'] == 'National')
]
national_data = national_data.rename(columns={'VALUE': 'House_Price'})

# Read GNP data
gnp_file = os.path.join(current_dir, 'NAQ03.20250104T140139.csv')
gnp_data = pd.read_csv(gnp_file)
gnp_data['Year'] = gnp_data['Quarter'].str[:4].astype(int)
gnp_yearly = gnp_data[gnp_data['Quarter'].str.endswith('Q4')].rename(columns={'VALUE': 'GNP'})

# Ensure correct data types
national_data['Year'] = national_data['Year'].astype(int)
national_data['House_Price'] = national_data['House_Price'].astype(float)

# Merge the datasets
merged_data = pd.merge(national_data[['Year', 'House_Price']], 
                       gnp_yearly[['Year', 'GNP']], 
                       on='Year', how='inner')

# Drop any rows with missing values
merged_data = merged_data.dropna()



# Calculate correlations
correlation_matrix = merged_data[['House_Price', 'GNP']].corr()


plt.figure(figsize=(16, 10))
# 1. Time series of variables (normalized for comparison)
plt.subplot(2, 2, 1)
normalized_data = merged_data.copy()
for column in ['House_Price', 'GNP']:
    normalized_data[column] = (merged_data[column] - merged_data[column].min()) / \
                             (merged_data[column].max() - merged_data[column].min())

ax1 = normalized_data.plot(x='Year', y=['House_Price', 'GNP'], 
                    ax=plt.gca(), marker='o')
plt.title('Normalized Trends Over Time', fontsize=12)
plt.xlabel('Year', fontsize=10)
plt.ylabel('Normalized Value', fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 2. Correlation Matrix
plt.subplot(2, 2, 2)
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, 
           square=True, linewidths=.5, cbar_kws={"shrink": .8})
plt.title('Correlation Matrix', fontsize=12)

# 3. House Price vs GNP scatter plot
plt.subplot(2, 2, 3)
ax3 = plt.scatter(merged_data['GNP'], merged_data['House_Price'], alpha=0.7)
plt.title('House Price vs GNP', fontsize=12)
plt.xlabel('GNP', fontsize=10)
plt.ylabel('House Price (€)', fontsize=10)
plt.grid(True, alpha=0.3)

plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
plt.gca().get_yaxis().get_major_formatter().set_scientific(False)
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
plt.gca().get_xaxis().get_major_formatter().set_scientific(False)

# Calculate Pearson correlation and p-value
corr_gnp, p_value_gnp = pearsonr(merged_data['GNP'], merged_data['House_Price'])
plt.annotate(f'Correlation: {corr_gnp:.2f}\np-value: {p_value_gnp:.4f}', 
             xy=(0.05, 0.95), xycoords='axes fraction', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

plt.tight_layout()
plt.savefig(os.path.join(current_dir, 'housing_correlations.png'), dpi=300)
plt.show()

# Create a simple prediction model based on the last value and average growth
last_house_price = merged_data['House_Price'].iloc[-1]
last_year = merged_data['Year'].iloc[-1]

# Calculate average annual house price growth rate
growth_rate = (merged_data['House_Price'].iloc[-1] / merged_data['House_Price'].iloc[0]) ** \
              (1/(len(merged_data)-1)) - 1

# Generate forecast to 2040
future_years = np.arange(last_year + 1, 2041)
forecast_years = len(future_years)
forecast = [last_house_price * (1 + growth_rate)**i for i in range(1, forecast_years + 1)]

# Create Moderate Inflation Values
moderate_growth_rate = growth_rate * 0.9  # 10% lower growth rate
forecast_moderate = [last_house_price * (1 + moderate_growth_rate)**i for i in range(1, forecast_years + 1)]

# Create Low Inflation Values
pessimistic_growth_rate = growth_rate * 0.7  
forecast_pessimistic = [last_house_price * (1 + pessimistic_growth_rate)**i for i in range(1, forecast_years + 1)]

# Plot historical and estimated future house prices
plt.figure(figsize=(12, 5))  
plt.plot(merged_data['Year'], merged_data['House_Price'], 'o-', color='black', linewidth=2,
         label='Historical House Prices')
plt.plot(future_years, forecast, 's--', color='green', label='High Inflation Forecast')
plt.plot(future_years, forecast_moderate, 'o--', color='blue', label='Moderate Inflation Forecast')
plt.plot(future_years, forecast_pessimistic, 'x--', color='red', label='Low Inflation Forecast')

plt.xlabel('Year', fontsize=12)
plt.ylabel('House Price (€)', fontsize=12)
plt.title('House Price Forecast to 2040', fontsize=14)
plt.legend(loc='upper left')
plt.grid(True, alpha=0.3)

# Force regular number format instead of scientific notation
plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
plt.gca().get_yaxis().get_major_formatter().set_scientific(False)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

# Add annotations for key years (2025, 2030, 2035, 2040)
key_years = [2025, 2030, 2035, 2040]
for year in key_years:
    if year >= last_year:
        year_index = np.where(future_years == year)[0][0]
        price = forecast[year_index]
        plt.annotate(f'€{price:,.0f}', 
                    xy=(year, price), xytext=(5, 10),
                    textcoords='offset points', fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="green", alpha=0.7))

plt.tight_layout()
plt.savefig(os.path.join(current_dir, 'house_price_forecast_2040.png'), dpi=300)
plt.show()

# Print key statistics and forecast
print("\nKey Statistics:")
print(f"Last recorded year: {last_year}")
print(f"Last house price: €{last_house_price:,.2f}")
print(f"Average annual growth rate: {growth_rate:.2%}")
print(f"Moderate Inflation Rate: {moderate_growth_rate:.2%}")
print(f"Low Inflation Rate: {pessimistic_growth_rate:.2%}")

print("\nForecast for Key Years:")
for year in key_years:
    if year >= last_year:
        year_index = np.where(future_years == year)[0][0]
        print(f"\nYear {year}:")
        print(f"  High Inflation: €{forecast[year_index]:,.2f}")
        print(f"  Moderate: €{forecast_moderate[year_index]:,.2f}")
        print(f"  Low Inflation: €{forecast_pessimistic[year_index]:,.2f}")