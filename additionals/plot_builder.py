import pandas as pd
import plotly.express as px

df = pd.read_excel('ALLA.xlsx')
print(1)
dff = df['BCountry'].value_counts().reset_index()
print(dff)


fig = px.scatter_map(
    df,
    lat='Blat',
    lon='Blon',

)

#fig.show()
