import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)


from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from dateutil.utils import today


#Data Fetching
print("Adatbetöltés megkezdése....")

print("ALLA.xlsx betöltése")
authorCSV = pd.read_excel('Data/ALLA.xlsx')

authorCSV['BornYear'] = pd.to_datetime(authorCSV['BornYear'], format = '%Y-%m-%d', errors = 'coerce')
authorCSV['DiedYear'] = pd.to_datetime(authorCSV['DiedYear'], format = '%Y-%m-%d', errors = 'coerce')

print("ALLA.xlsx betöltve, adatai (BornYear, DiedYear) formátolva")
print()
print(authorCSV)
print()
print("Works HU.xlsx betöltése")
worksXLSX = pd.read_excel('Data/Works HU.xlsx')
worksXLSX['Year'] = pd.to_datetime(worksXLSX['Year'], format = '%Y', errors = 'coerce')
print("Works HU.xlsx betöltve, adatai (Year) formátolva")
print()
print(worksXLSX)
print()

colors = {
    'backround': '#000',
    'text': 'lightcyan'
}
print("Az oldal színkönyvtára betöltve!")
print()
print("Térképek betöltése")


authors_born_graph = px.scatter_map(
    authorCSV,
    lat='Blat',
    lon='Blon',
    hover_name='Name',
    hover_data=['BCountry','BornCity'],
    color='Irodalom',
    zoom=2,
    title="Szarmazas"
)
authors_born_graph.update_layout(
    map_style='dark',
    plot_bgcolor=colors['backround'],
    paper_bgcolor=colors['backround'],
    font_color=colors['text'])
print("authors_born_graph ...ok")

filtereddf=(authorCSV['Kor'].value_counts(dropna=False).reset_index())

EtapPie = px.pie(filtereddf,
             values = 'count',
             names = 'Kor',
             title='Érettségire melyik irodalmi korból van a legtöbb?',
             hole=0.5,
             color_discrete_sequence=px.colors.sequential.Blues,)
EtapPie.update_layout(template='plotly_dark',
                      paper_bgcolor=colors['backround'],
                      font_color=colors['text']
                      )
print("EtapPie ...ok")

filteredworks = (worksXLSX['Műfaj'].value_counts(dropna=True).reset_index())

WorksMufaj = px.bar(filteredworks,
             x = 'Műfaj',
             y = 'count',
             color = 'Műfaj',)
WorksMufaj.update_layout(template='plotly_dark',
                         paper_bgcolor=colors['backround'],
                         font_color=colors['text']
                         )
print("WorksMufaj ...ok")

fflire = worksXLSX.loc[worksXLSX['Műfaj']=='Líra',['Title','Type']]
fflira = (fflire['Type'].value_counts(dropna=True).reset_index())


LiraHistrogram = px.histogram(fflira,
             y='count',
             x = 'Type',
             labels='Type')
LiraHistrogram.update_layout(template='plotly_dark',
                             paper_bgcolor=colors['backround'],
                             font_color=colors['text']
                             )
print("LiraHistogram ...ok")

AC = (authorCSV['BCountry'].value_counts(dropna=True).reset_index())

ACountry = px.bar(AC,
                  x = 'BCountry',
                  y = 'count',
                  labels = 'BCountry',
                  title="Ország toplista",
                  subtitle="Mennyi író/költő származik az adott országból")
ACountry.update_layout(template='plotly_dark',
                       paper_bgcolor=colors['backround'],
                       font_color=colors['text'])
print("ACountry ...ok")

WorksMap = px.scatter_map(worksXLSX,
                     lat = 'Latitude',
                     lon = 'Longitude',
                     hover_name='Title',
                     hover_data=[],
                     color='Műfaj',
                     height=800,
                     width=900,
                     title="Magyar művek megírásának helye ** folyamatban a bővítés **",
                     zoom=5)
WorksMap.update_layout(map_style='dark',
                       template='plotly_dark',
                       paper_bgcolor=colors['backround'],
                       font_color=colors['text']
                       )
print("WorksMap ...ok")

print()
print("Graphok betöltve!")
print()



print("App indítása")
app = Dash(__name__)
app.title = "Irodalmi Overview"

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div( children=[
    html.Title("IA"),
    html.H1("Irodalmi Áttekintő",
            ),
    html.Br(),
    html.Div([
        dcc.Dropdown(
            id='literature',
            options=[{'label': name, 'value': name} for name in sorted(authorCSV['Irodalom'].dropna().unique())],
            value=[authorCSV['Irodalom'].dropna().iloc[0]] if not authorCSV['Irodalom'].dropna().empty else [],
            multi=True,
            clearable=True,
            persistence=True,
            persistence_type='local',
            placeholder='Select a literature',
            ),

        dcc.Dropdown(
            id = 'etaps',
            options = [{'label': meno, 'value': meno} for meno in sorted(authorCSV['Kor'].dropna().unique())],
            value=[authorCSV['Kor'].dropna().iloc[0]] if not authorCSV['Kor'].dropna().empty else [],
            multi=True,
            clearable=True,
            persistence=True,
            persistence_type='local',
            placeholder='Select a Etap',
            ),
    ]),
    html.Br(),
    html.Div(id='output_container',
             children=[],
             className="output-choice"),
    html.Br(),
    html.H2("Költők/írók származása térképen megmutatva",
            ),
    html.Div([
            dcc.RadioItems(inline=True,
                           id='abd',
                           options=[
                               {'label': 'Született', 'value': 'Born'},
                               {'label':'Elhunyt','value':'Died'}
                           ],
                           value='Born',
                           labelStyle={'display': 'inline-block', 'margin-right': '12px'},
                           className='radioitems',
                           style={'display': 'inline-block', 'color': 'lightcyan'},),
            dcc.Graph(
                id='Authors_born_graph',
                figure = authors_born_graph,
                className='ABG-graph-container',
                style = {'height': '80vh',
                         'color': colors['text']},
            ),
            dcc.Graph(
                id='Author_country_graph',
                figure= ACountry,
                className='ABG-graph-container',
                style = {'height': '50vh',
                         'color': colors['text']},
            )
    ], style={'padding': 10}),
    html.Br(),
    html.H2("Gant graph és érintett országok",),
    html.Div([
        html.Div([
            dcc.Graph(id='Authors',
                      figure={},
                      style={'height': '80vh',
                             'palette': 'muted',
                             'font-family': 'Quicksand'}),
        ], style={'padding':10, 'flex':1}),
        html.Div([
            dcc.Graph(id='nationality-map',
                      figure={},
                      style={'height': '80vh',
                             'color': colors['text'] },),
        ], style={'padding':10, 'flex':1}),
    ], style={'display':'flex', 'padding':10}),
    html.Br(),
html.H2("Statisztika & Map",
        ),
    html.Div([
        html.Div([
            dcc.Graph(id='Etapcount',
                      figure=EtapPie,
                      style={'height': '40vh',
                             'color': colors['text'] },),
            dcc.Graph(id='Liracount',
                      figure=LiraHistrogram,
                      style={'height': '30vh',
                             'color': colors['text'] },),
        ], style={'padding':10, 'flex':1}),
        html.Div([
            html.P("Sajnos sok időt igényel, nem minden mű van rendesen dokumentálva. "
                              "Ha esetleg találsz/ismersz egy jó adatbázist/osldalt, amely rendelkezik ilyen információkkal, "
                              "kérlek oszd meg velem! :))"),
            dcc.Graph(id='WorksMap',
                      figure=WorksMap,
                      style={'height': '80vh',
                             'color': colors['text'] },),
        ], style={'padding':10, 'flex':1}),

    ],style={'padding':10, 'display':'flex'}),

    html.Br(),
    html.Br(),
    html.Br(),

    html.H6(f"Készítette: Kiss Christopher. Minden jog fenntartva {today()}",
            ),

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='Authors', component_property='figure')],
    [Input(component_id='literature', component_property='value'),
     Input(component_id='etaps', component_property='value'),]
)

def update_graph(option_slctd, etap_choice):
    print("update_graph hívva",option_slctd,"&", etap_choice, "paraméterekkel")

    dff = authorCSV[
        authorCSV['Irodalom'].isin(option_slctd) &
        authorCSV['Kor'].isin(etap_choice)
        ].copy()
    print("dff létrehozva")

    container = (
        f"Választott irodalom: {', '.join(option_slctd)}; "
        f"Kor: {', '.join(etap_choice)}; "
        f"Találatok: {len(dff)}"
    )

    dff = dff.dropna(subset=['BornYear'])
    #dff['DiedYear'] = dff['DiedYear'].fillna(pd.Timestamp.today())

    # Plotly Express
    fig = px.timeline(
        dff.sort_values('Irodalom',ascending=False).reset_index(drop=True),
        x_start="BornYear",
        x_end="DiedYear",
        y="Name",
        text="Alkor",
        color = "Irodalom",
        title = "Mettől-meddig élt",
        hover_name="Name",

    )
    fig.update_yaxes(autorange="reversed")  # Gantt charts usually reverse Y-axis
    fig.update_layout(template='plotly_dark',
                      font_color=colors['text'],
                      paper_bgcolor=colors['backround'])

    print("update_graph fig létrehozva")

    return container, fig

@app.callback(
    Output(component_id='nationality-map', component_property='figure'),
    [Input(component_id='etaps', component_property='value'),
     Input(component_id='literature', component_property='value'),])

def update_nationlitymap(etap_choice, option_slctd):
    print("update_nationality hívva", option_slctd, "&", etap_choice, "paraméterekkel")
    if not option_slctd or not etap_choice:
        return "Válassz irodalmat és korszakot!"

    filtered_df = authorCSV[
        authorCSV['Kor'].isin(etap_choice) &
        authorCSV['Irodalom'].isin(option_slctd)
        ].copy()

    fig = px.choropleth(
        filtered_df.sort_values('BornYear'),
        locations='BCountry',
        locationmode='country names',
        color='BCountry',
        title = "Ország szerinti szétosztás",
        projection='miller',

    )
    fig.update_layout(template='plotly_dark',
                      font_color = colors['text'],
                      paper_bgcolor=colors['backround'])
    print("update_nationlitymap fig létrehozva")
    return fig

@app.callback(Output('Authors_born_graph', 'figure'),
              Input('abd','value'))
def update_authors_born_graph(choice):
    print("update_authors_born_graph hívva", choice, "paraméterrel")
    if choice == 'Died':
        fig = px.scatter_map(
            authorCSV,
            lat = 'Dlat',
            lon = 'Dlon',
            hover_name = 'Name',
            hover_data=['DCountry','DiedCity', 'Irodalom', 'Alkor'],
            color = 'BCountry',
            title = "Elhalálozás",
            zoom = 2
        )
    else:
        fig = px.scatter_map(
            authorCSV,
            lat='Blat',
            lon='Blon',
            hover_name='Name',
            hover_data=['BCountry', 'BornCity', 'Irodalom', 'Alkor'],
            color='BCountry',
            title="Származás",
            zoom = 2,
        )

    fig.update_layout(map_style='dark',
                      font_color='lightcyan',
                      paper_bgcolor='#000')
    print("update_authors_born_graph fig létrehozva")
    return fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)