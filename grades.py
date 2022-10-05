import pandas as pd
import matplotlib.pyplot as plt

data_set = pd.read_csv(r"C:\Users\User\Desktop\StudentsPerformance.csv")
data_set.head()

data_set['id'] = [i for i in range(data_set.shape[0])]

boys = data_set.loc[data_set['gender'] == 'male']
girls = data_set.loc[data_set['gender'] == 'female']


# math
boys_m = boys.groupby(['math score'])['id'].count().reset_index(name='count')

girls_m = girls.groupby(['math score'])['id'].count().reset_index(name='count')


fig, ([ax1, ax2, ax3], [ax11, ax22, ax33]) = plt.subplots(nrows=2, ncols=3, figsize=(12, 9), num='Students statistic')
plt.subplots_adjust(wspace=0.4, hspace=0.4)
fig.suptitle('Students statistic', fontweight='bold', size=16)


columns = boys_m['math score']
rows = boys_m['count']
ax1.bar(columns, rows, color="blue", alpha=0.6, label='male')

columns = girls_m['math score']
rows = girls_m['count']
ax1.bar(columns, rows, color="red", alpha=0.6, label='female')

ax1.set_xlabel('math score', fontweight='bold', fontsize=12)
ax1.set_ylabel('count', fontweight='bold', fontsize=12)
ax1.legend()

# reading
boys_r = boys.groupby(['reading score'])['id'].count().reset_index(name='count')
girls_r = girls.groupby(['reading score'])['id'].count().reset_index(name='count')


columns = boys_r['reading score']
rows = boys_r['count']
ax2.bar(columns, rows, color="blue", alpha=0.6, label='male')

columns = girls_r['reading score']
rows = girls_r['count']
ax2.bar(columns, rows, color="red", alpha=0.6, label='female')

ax2.set_xlabel('reading score', fontweight='bold', fontsize=12)
ax2.set_ylabel('count', fontweight='bold', fontsize=12)
ax2.legend()

# writing
boys_w = boys.groupby(['writing score'])['id'].count().reset_index(name='count')

girls_w = girls.groupby(['writing score'])['id'].count().reset_index(name='count')


columns = boys_w['writing score']
rows = boys_w['count']
ax3.bar(columns, rows, color="blue", alpha=0.6, label='male')


columns = girls_w['writing score']
rows = girls_w['count']
ax3.bar(columns, rows, color="red", alpha=0.6, label='female')

ax3.set_xlabel('writing score', fontweight='bold', fontsize=12)
ax3.set_ylabel('count', fontweight='bold', fontsize=12)
ax3.legend()


# average score by gender
counts = data_set['gender'].value_counts().to_dict()
average = data_set[['gender', 'math score', 'reading score', 'writing score']].groupby(['gender']).mean().round(1).T

average.plot(kind='bar', rot=20, color=['r', 'b'], alpha=0.6, ax=ax11)
ax11.set_ylabel('AVG score', fontweight='bold', fontsize=12)

ax11.legend(title='')


# race + subject score
races = data_set[['race/ethnicity', 'math score', 'reading score', 'writing score']].groupby(['race/ethnicity']).mean()

ax22.scatter([range(1, 6)], races['math score'], color="#191970", label='math', alpha=0.6)
ax22.scatter([range(1, 6)], races['reading score'], color="#FFD700", label='reading', alpha=0.6)
ax22.scatter([range(1, 6)], races['writing score'], color="#C71585", label='writing', alpha=0.6)

ax22.set_xticks([1, 2, 3, 4, 5], ['group A', 'group B', 'group C', 'group D', 'group E'], rotation=20)
ax22.set_ylabel('AVG score', fontweight='bold', fontsize=12)

ax22.legend()

# parents' education
parents = data_set[['parental level of education', 'math score', 'reading score', 'writing score']].groupby(['parental level of education']).mean()

parents.plot(kind='bar', rot=25, color=['#191970', '#FFD700', '#C71585'], alpha=0.6, ax=ax33)
ax33.set_ylabel('AVG Score', fontweight='bold', fontsize=12)
ax33.set_xlabel('')
ax33.tick_params(axis='x', labelsize=8)


plt.show()


