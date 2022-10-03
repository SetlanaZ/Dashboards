import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons

file = r'netflix.xlsx'

xl = pd.read_excel(file)

# собираем все жанры, убираем дублирующиеся ("TV Dramas == Dramas")
listed_in = [el.split(", ") for el in xl['listed_in'].tolist()]
all_genres = []
for el in listed_in:
    for i in el:
        if i == 'TV Shows' or i == 'TV Mysteries' or not i.startswith('TV '):
            all_genres.append(i)
        else:
            all_genres.append(i[3:])

# выбираем топ 5 жанров по всему миру
top_five = {}
for g in all_genres:
    if g not in top_five:
        top_five[g] = all_genres.count(g)

top_five = [[k, v] for k, v in top_five.items()]
top_five.sort(key=lambda x: x[1], reverse=True)
top_five = top_five[:5]

# удаляем все повторы
all_genres = set(all_genres)


lines = xl.to_dict(orient='record')

# словарь вида {"Страна": [жанры]}
genres = {}

# словарь вида {'Страна': [кол-во проектоов]} (для выборки топ 10 стран по количеству)
count_projects = {}

for line in lines:
    cntr = line['country']
    if cntr != 'Not Given':
        try:
            if cntr in genres:
                genres[cntr] = list(filter(lambda x: x in all_genres, genres[cntr] + line['listed_in'].split(', ')))
            else:
                genres[cntr] = line['listed_in'].split(', ')
            if cntr in count_projects:
                count_projects[cntr] += 1
            else:
                count_projects[cntr] = 1
        except Exception:
            pass

# те самые топ 10 стран по количеству проектов
countries = [[k, v] for k, v in count_projects.items()]
countries.sort(key=lambda x: x[1], reverse=True)
countries = countries[:10]


dfs = [{}, {},  {}, {}, {}, {}, {}, {}, {}, {}]

# словари по странам, {"Жанр": [кол-во проектов], "Жанр2": [кол-во проектов2]...}
for i in range(10):
    for el in genres[countries[i][0]]:
        if el in dfs[i]:
            dfs[i][el] += 1
        else:
            dfs[i][el] = 1
    dfs[i] = [[k, v] for k, v in dfs[i].items()]
    dfs[i].sort(key=lambda x: x[1], reverse=True)
    try:
        dfs[i] = dfs[i][:5]
    except Exception:
        pass

# объединяем все данные
data = {'All world': top_five}

for el in countries:
    data[el[0]] = dfs[countries.index(el)]

# график
fig, ax = plt.subplots(num="Genres")

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')

fig.patch.set_facecolor('black')
ax.patch.set_facecolor('black')

COLOR = 'white'
plt.rcParams['text.color'] = COLOR
plt.rcParams['axes.labelcolor'] = COLOR
plt.rcParams['xtick.color'] = COLOR
plt.rcParams['ytick.color'] = COLOR

fig.subplots_adjust(left=0.35)
fig.set_figwidth(8)
fig.set_figheight(8)

item = 'All world'

labels = [el[0] for el in data[item]]
values = np.array([el[1] for el in data[item]])

plt.title('Genres', color='White', size=16)
ax.bar(labels, values, color="#FF1493", error_kw={'ecolor': '0.4'}, alpha=0.6)
plt.xticks(rotation=15, ha='right', fontsize=8)
ax.tick_params(labelcolor='white')

p1 = ax.bar(np.arange(len(values)), values, width=0.5, alpha=0)
ax.bar_label(p1, padding=2)


rax = fig.add_axes([0.02, 0.51, 0.18, 0.4], facecolor='black')
radio = RadioButtons(rax, ([k for k in data.keys()]), activecolor='#ad005c')


def choose_country(c):
    global item, labels, values, rax, radio, fig
    item = c
    ax.clear()
    labels = [el[0] for el in data[item]]
    values = np.array([el[1] for el in data[item]])
    ax.bar(labels, values, color='#FF1493', error_kw={'ecolor': '0.4'}, alpha=0.6)
    p1 = ax.bar(np.arange(len(values)), values, width=0.5, alpha=0)
    ax.bar_label(p1, padding=2)
    ax.patch.set_facecolor('black')
    ax.tick_params(labelcolor='white')
    ax.tick_params(axis='x', labelrotation=15, labelsize=8)
    ax.set_title('Genres', size=16)
    plt.draw()

radio.on_clicked(choose_country)

plt.show()
