from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import components as cmp
from utils import get_color

# Load and prepare data
data_path = 'data/elections_data.csv'
df = pd.read_csv(data_path)

winner_by_year_state = df.groupby(['year', 'state_po'])[['year', 'state_po', 'party_detailed', 'candidatevotes', 'totalvotes']].apply(
    lambda x: x.loc[x['candidatevotes'].idxmax()]).reset_index(drop=True)

# Format party column to be title case
winner_by_year_state['Winning Party'] = winner_by_year_state['party_detailed'].str.title()

winner_by_year_state['Votes'] = round(winner_by_year_state['candidatevotes'] / winner_by_year_state['totalvotes'], 4)
winner_by_year_state = winner_by_year_state[['year', 'state_po', 'Winning Party', 'Votes']]

min_year = df['year'].min()
max_year = df['year'].max()

# Initialize dash app and server
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Create components
year_range = range(min_year, max_year + 1, 4)
year_radio_items = cmp.create_radio_items('year_radio_items', year_range)
map_style = {'height': '90vh', 'width': '100%'}
map_chart = dcc.Graph(id='map-chart', style=map_style)
footer = cmp.create_footer()

app.layout = html.Div([
    dbc.Row([
        dbc.Col(html.H1(f'USA Elections {min_year} - {max_year}'), className='text-center p-2', xl=6, lg=12),
        dbc.Col(year_radio_items, className='px-4 py-3', xl=6, lg=12),
    ],style={
        'border-bottom': '1px solid #d1d1d1',
        'box-shadow': '0 -1px 5px rgba(0,0,0,0.1)'
    }),
    dbc.Row([
        dbc.Col(map_chart, width=12)
    ]),
    dbc.Row([
        dbc.Col(footer, width=12)
    ]),
], 
className='m-0',
style={'background-color': '#F5F5F5'}
)


# Define callback
@app.callback(
    Output('map-chart', 'figure'),
    Input('year_radio_items', 'value')
)
def update_choropleth_map(selected_year):
    selected_year = int(selected_year)
    filtered_df = winner_by_year_state[winner_by_year_state['year'] == selected_year]
    max_value = filtered_df['Votes'].max()
    
    filtered_df['color'] = filtered_df.apply(lambda row: get_color(row['Winning Party'], row['Votes'], max_value), axis=1)
    filtered_df['party_votes'] = filtered_df['Winning Party'] + '_' + filtered_df['Votes'].astype(str)
    
    fig = cmp.create_choropleth_map(filtered_df, selected_year)
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
