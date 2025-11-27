import pandas as pd
import plotly.express as px


spis = pd.read_excel("SlovakAuthors.xlsx")
print(1)
spis['BornYear'] = pd.to_datetime(spis['BornYear'], format='%Y-%m-%d', errors='coerce')
print(2)
spis['DiedYear'] = pd.to_datetime(spis['DiedYear'], format='%Y-%m-%d', errors='coerce')
print(3)


print(spis)

f2 = px.scatter_map(spis, lat='Blat', lon='Blon', color='Kor', hover_name='Name')
f2.show()
f3 = px.scatter_map(spis, lat='Dlat', lon='Dlon', color='Kor', hover_name='Name')
f3.show()

#fig=px.timeline(etapy.sort_values(by='BornYear', ascending=True), x_start='BornYear', x_end='DiedYear', y='Name', color='Column1',)
#fig.show()
