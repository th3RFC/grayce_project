# loading in raw data
import io
import requests
import pandas as pd
url = "https://raw.githubusercontent.com/th3RFC/grayce_project/main/aw_fb_data.csv"

# reading the downloaded content and turning it into a pandas dataframe
download = requests.get(url).content
dataset = pd.read_csv(io.StringIO(download.decode('utf-8')))
print(dataset.head())

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

# now finding average when picking just one activity
# removing all rows which are not self paced walk - justification: baseline fitness activity
dataset_clean_new = dataset_clean[~dataset_clean["activity"].str.contains("Running 7 METs|Lying|Running 5 METs|Running 3 METs|Sitting")]
print(dataset_clean_new)

# finding average per person for only self paced walk activity (excludes fact people perform some activities more than once compared to other people)
# resting heart rate
avg_heart_rate_new = dataset_clean_new.groupby(['person_id'])['resting_heart'].mean()
print(avg_heart_rate_new)

# average steps
avg_steps_new = dataset_clean_new.groupby(['person_id'])['steps'].mean()
print(avg_steps_new)

# average calories
avg_calories_new = dataset_clean_new.groupby(['person_id'])['calories'].mean()
print(avg_calories_new)

# average distance
avg_distance_new = dataset_clean_new.groupby(['person_id'])['distance'].mean()
print(avg_distance_new)

# merging averages into one dataset
# first merge
average_metrics_1_new = pd.merge(avg_heart_rate_new, avg_calories_new, how="left", on="person_id")
print(average_metrics_1_new)

# second merge
average_metrics2_new = pd.merge(average_metrics_1_new, avg_distance_new, how="left", on="person_id")
print(average_metrics2_new)

# third merge
average_metrics_new = pd.merge(average_metrics2_new, avg_steps_new, how="left", on="person_id")
print(average_metrics_new)

# exporting this dataset
average_metrics_new.to_csv(r'C:\Users\jade\OneDrive\Documents\Skills Club Project 1\grayce_project\Average Metrics - Self Pace Activity Only.csv', index=False)