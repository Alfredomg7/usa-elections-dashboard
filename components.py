from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px

def create_radio_items(id, options):
    radio_items = dbc.RadioItems(
        id=id,
        options=[
            {'label': option, 'value': option} for option in options
        ],
        value=options[0],
        inline=True,
    )
    return radio_items

def create_choropleth_map(df, selected_year):
    color_mapping = {combo: color for combo, color in zip(df['party_votes'], df['color'])}

    fig = px.choropleth(
        df,
        locations='state_po',
        locationmode='USA-states',
        color='party_votes',
        color_discrete_map=color_mapping,
        hover_name='state_po',
        hover_data={'state_po': False, 'party_votes': False, 'Winning Party': True,'Votes': True},
        title=f'Winning Party by State in {selected_year}',
        scope='usa',
    )

    fig.update_traces(
        showlegend=False,
        hovertemplate=fig.data[0].hovertemplate.replace(
        '%{customdata[3]}', '%{customdata[3]:.1%}')
        )
    
    fig.update_layout(
        title_font_size=28,
        title_font_family='sans-serif',
        title_x=0.5,
        paper_bgcolor='#f9f9f9',
        plot_bgcolor='#f9f9f9',
    )

    return fig

def create_footer():
    footer = html.Footer(
                [
                    html.Div(
                    [
                        html.A('Source Code', href='https://github.com/Alfredomg7/usa-elections-dashboard', target='_blank', className='link-primary link-underline-opacity-0'),
                        html.Span(' | '),
                        html.A('Dataset Source', href='https://github.com/plotly/Figure-Friday/tree/main/2024/week-33', target='_blank', className='link-primary link-underline-opacity-0')
                    ],
                    className='text-center py-2 fs-5',
                    style={
                        'position': 'fixed',
                        'bottom': '0',
                        'background-color': '#F5F5F5',
                        'border-top': '1px solid #d1d1d1',
                        'width': '100%',
                        'box-shadow': '0 -1px 5px rgba(0,0,0,0.1)',
                        'z-index': '1000'
                        }
                    )
                ]
            ),
    return footer
