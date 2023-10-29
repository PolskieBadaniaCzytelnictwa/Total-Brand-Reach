import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd

app = Dash(__name__)
server = app.server

pd.set_option('display.float_format', '{:.0f}'.format)

df = pd.read_excel('TBR_9m.xlsx')
tematyka = pd.read_excel('kat.xlsx')

tematyka_lista = tematyka['kat'].unique()
wskaźniki_lista = ['druk+e-wydania', 'www', 'TBR']
miesiące_lista = [1, 2, 3, 4, 5, 6, 7, 8, 9]

app = dash.Dash(__name__)

app.layout = html.Div([
    
    html.H1("Total Reach 2023"),
    
    html.P("Wybierz okres czasu (miesiące):"),
    
    dcc.RangeSlider(
        id='miesiace-slider',
        marks={i: str(i) for i in miesiące_lista},
        min=min(miesiące_lista),
        max=max(miesiące_lista),
        step=1,
        value=[min(miesiące_lista), max(miesiące_lista)]
    ),
    
      dcc.Checklist(
        id='tematyki-checkbox',
        options=[{'label': temat, 'value': temat} for temat in tematyka_lista],
        value=tematyka_lista,
        inline=False,
    ),

    dcc.Graph(
        id='table',
    )
])

@app.callback(
    Output('table', 'figure'),
    [Input('tematyki-checkbox', 'value'),
     Input('miesiace-slider', 'value')]
)
def update_figure(selected_tematyki, selected_miesiace):
    if not selected_tematyki:
        selected_tematyki = tematyka_lista

    wyniki = pd.DataFrame()
    
    for i in selected_tematyki:
        pisma_lista = tematyka[tematyka['kat'] == i]['tytuł'].to_list()
        for j in pisma_lista:
            for k in wskaźniki_lista:
                if k != 'TBR':
                    wyniki.loc[j, k] = df[(df['tytuł'] == j) & (df['wskaźnik'] == k) & (df['miesiąc'].between(selected_miesiace[0], selected_miesiace[1]))]['wynik'].mean()
                else:
                    wyniki.loc[j, k] = (1 - float(df[(df['tytuł'] == j) & (df['wskaźnik'] == 'współczytelnictwo')]['wynik'].iloc[0])) * wyniki.loc[j, 'druk+e-wydania'] + wyniki.loc[j, 'www']
    wyniki = wyniki[wyniki['www'] == wyniki['www']]
    wyniki = wyniki.fillna(0)
    wyniki = wyniki.sort_values('TBR', ascending=False)

    wyniki_sformatowane = wyniki.applymap(lambda x: '{:,.0f}'.format(x).replace(',', ' '))
    
    figure = {
        'data': [
            {
                'type': 'table',
                'header': {
                    'values': [''] + wyniki_sformatowane.columns.tolist()
                },
                'cells': {
                    'values': [wyniki_sformatowane.index] + [wyniki_sformatowane[col] for col in wyniki_sformatowane.columns[0:]]
                }
            }
        ]
    }

    return figure

if __name__ == '__main__':
    app.run_server()