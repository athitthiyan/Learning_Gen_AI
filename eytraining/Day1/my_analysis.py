import pandas as pd
import numpy as np
import seaborn as sns

print("Pandas version:", pd.__version__)

# Part 1 : Loading Data & Inspecting using titanic dataset

df = sns.load_dataset('titanic')

print('Shape', df.shape)
print(df.head())

# Part 2 - Handling missing values

# Strategy 1 : Dropping rows where any column is null
print('Before dropna():', df.shape)

df_dropped = df.dropna()

print('After dropna():', df_dropped.shape)

# Strategy 2: Drop only if specific column is null
df_dropped2 = df.dropna(subset=['age', 'embarked'])

print('After dropna(subset=[age, embarked]):', df_dropped2.shape)

# Strategy 3: Fill missing values

df2 = df.copy()   # never mutate the original while exploring

df2['age'] = df2['age'].fillna(df2['age'].mean())
df2['embarked'] = df2['embarked'].fillna(df2['embarked'].mode()[0])

# Drop 'deck' - too many missing values to be useful
df2 = df2.drop(columns=['deck'])

print('Missing after cleaning')
print(df2.isnull().sum())

survivours_young = df2.query('survived == 1 and age < 18')

print(len(survivours_young))
print(survivours_young.head())

# 1. How many unique values does the 'embarked' column have?
# 2. What is the most common passenger class (pclass)

print(df2['embarked'].nunique())
print(df['embarked'].unique())

# 1. Find all male passengers who paid a fare above 200 and survived.
# 2. Using .iloc, extract rows 100 to 109 and the last 3 columns.

male_survivour = df2.query(
    "sex == 'male' and fare > 200 and survived == 1"
)

print(male_survivour)

print(df2.iloc[100:110, -3:])

# Groupby analysis

survival_status = (
    df2.groupby(['pclass', 'sex'])['survived']
    .agg(['mean', 'count'])
    .rename(columns={
        'mean': 'survival_rate',
        'count': 'total_count'
    })
    .sort_values(by='survival_rate', ascending=False)
)

print(survival_status)

# Aggregation summary

class_summary = df2.groupby('pclass').agg(
    avg_age=('age', 'mean'),
    avg_fare=('fare', 'mean'),
    survived=('survived', 'count'),
    n=('survived', 'sum')
)

print(class_summary)

# Pivot table

pt = df2.pivot_table(
    values='survived',
    index='pclass',
    columns='sex',
    aggfunc='mean'
)

print(pt)

pt1 = df2.pivot_table(
    values='survived',
    index='pclass',
    columns='sex',
    aggfunc='mean'
)

print(pt1)

# Average fare

avg_fare = df2.pivot_table(
    values='fare',
    index='embarked',
    aggfunc='mean'
)

print("Average Fare by Embarkation Port")
print(avg_fare)

# Survivors per class

survivours_per_clss = df2[df2['survived'] == 1].pivot_table(
    values='survived',
    index='pclass',
    aggfunc='count'
).sort_values(by='survived', ascending=False)

print("Survivors per class")
print(survivours_per_clss)

# Empty DataFrame

class_info = pd.DataFrame([])

# Port lookup table

port_lookup = pd.DataFrame({
    'embarked': ['C', 'Q', 'S'],
    'port_name': ['Cherbourg', 'Queenstown', 'Southampton']
})

print(port_lookup)

# Merge example

df_merged = pd.merge(
    df2,
    port_lookup,
    on='embarked',
    how='left'
)

print(df_merged[['embarked', 'port_name']].head())

# Age grouping using pd.cut()

df2['age_group'] = pd.cut(
    df2['age'],
    bins=[0, 18, 50, 100],
    labels=['child', 'adult', 'senior']
)

print(df2['age_group'])

print(
    df2.groupby('age_group', observed=True)['survived']
    .mean()
    .round(3)
)