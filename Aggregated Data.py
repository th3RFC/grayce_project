# loading in raw data
import pandas as pd
dataset = pd.read_csv(r'C:/Users/jade/OneDrive/Documents/Skills Club Project 1/aw_fb_data.csv')
print(dataset)

# giving participants unique id
# giving rows unique ID
dataset['person_id'] = pd.factorize(dataset.age+dataset.gender+dataset.height+dataset.weight)[0]
print(dataset)

# checking new dataset
print(dataset.head())
print(dataset.tail())

# cleaning dataset
dataset_clean = dataset.drop(['X1', 'entropy_heart', 'entropy_setps', 'corr_heart_steps', 'norm_heart', 'intensity_karvonen', 'sd_norm_heart'], axis=1)
print(dataset_clean)

# adding BMI column
# converting height to metres
dataset_clean['height_metres'] = dataset_clean['height']/100
dataset_clean['BMI'] = dataset_clean['weight']/(dataset_clean['height_metres']*2)

print(dataset_clean.head())

# finding average per person for each activity (without taking into count frequency of activity performed i.e., unweighted)
# resting heart rate
avg_heart_rate = dataset_clean.groupby(['person_id'])['resting_heart'].mean()
print(avg_heart_rate)

# average steps
avg_steps = dataset_clean.groupby(['person_id'])['steps'].mean()
print(avg_steps)

# average calories
avg_calories = dataset_clean.groupby(['person_id'])['calories'].mean()
print(avg_calories)

# average distance
avg_distance = dataset_clean.groupby(['person_id'])['distance'].mean()
print(avg_distance)

# merging averages into one dataset
# first merge
average_metrics_1 = pd.merge(avg_heart_rate, avg_calories, how="left", on="person_id")
print(average_metrics_1)

# second merge
average_metrics2 = pd.merge(average_metrics_1, avg_distance, how="left", on="person_id")
print(average_metrics2)

# third merge
average_metrics = pd.merge(average_metrics2, avg_steps, how="left", on="person_id")
print(average_metrics)

# now to find weighted average for final aggregated data

