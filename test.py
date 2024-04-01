import pandas as pd
import matplotlib.pyplot as plt

# Load the weather data from the CSV file
weather_data = pd.read_csv("F:/64.csv")

# Calculate accumulated precipitation for each year
accumulated_precipitation = {}
for year in range(1981, 2020):
    year_data = weather_data[weather_data['YEAR'] == year]
    accumulated_precipitation[year] = year_data['PREC'].cumsum()

# Find onset and end dates for each year
onset_dates = {}
end_dates = {}
for year in range(1981, 2020):
    year_data = weather_data[weather_data['YEAR'] == year]
    for month in range(1, 13):
        month_data = year_data[year_data['MONTH'] == month]
        if month_data['PREC'].sum() >= 51:
            onset_date = month_data[month_data['PREC'].cumsum() >= 51].iloc[0]
            onset_dates[year] = pd.to_datetime(f"{int(onset_date['YEAR'])}-{int(onset_date['MONTH'])}-{int(onset_date['DAY'])}")
            break

    reversed_year_data = year_data[::-1]
    for month in range(12, 0, -1):
        month_data = year_data[year_data['MONTH'] == month]
        if month_data['PREC'].sum() >= 51:
            end_date = month_data[month_data['PREC'].cumsum() >= 51].iloc[0]
            end_dates[year] = pd.to_datetime(f"{int(end_date['YEAR'])}-{int(end_date['MONTH'])}-{int(end_date['DAY'])}")
            break


# Calculate duration of the rainy season for each year
duration = {year: (end_dates[year] - onset_dates[year]).days + 1 for year in onset_dates}

# Print results
for year in onset_dates:
    print(f"Year: {year}, Onset Date: {onset_dates[year].strftime('%Y-%m-%d')}, End Date: {end_dates[year].strftime('%Y-%m-%d')}, Duration: {duration[year]} days")

# Create lists of years and onset/end days
years = list(onset_dates.keys())
onset_days = [onset_dates[year].dayofyear for year in years]
end_days = [end_dates[year].dayofyear for year in years]

# Plot the onset and end dates
plt.figure(figsize=(10, 6))
plt.plot(years, onset_days, marker='o', linestyle='-', color='b', label='Onset Date')
plt.plot(years, end_days, marker='s', linestyle='-', color='r', label='End Date')
plt.title('Rainy Season Onset and End Dates (1981-2019)')
plt.xlabel('Year')
plt.ylabel('Day of Year')
plt.legend()
plt.grid(True)
plt.xticks(range(1981, 2020, 2))  # Show ticks every 2 years
plt.tight_layout()
plt.show()
