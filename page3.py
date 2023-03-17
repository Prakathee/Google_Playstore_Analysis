import dash
import dash_bootstrap_components as dbc
from dash import dcc, callback
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

def get_page3_layout(df):
    currency_country_map = {
        'USD': 'United States',
        'XXX': 'Unknown',
        'CAD': 'Canada',
        'EUR': 'European Union',
        'INR': 'India',
        'VND': 'Vietnam',
        'GBP': 'United Kingdom',
        'BRL': 'Brazil',
        'KRW': 'South Korea',
        'TRY': 'Turkey',
        'RUB': 'Russia',
        'SGD': 'Singapore',
        'AUD': 'Australia',
        'PKR': 'Pakistan',
        'ZAR': 'South Africa'
    }

    df['Country'] = df['Currency'].map(currency_country_map)

    # convert the 'date' column to datetime type
    df['Released'] = pd.to_datetime(df['Released'])

    df['Year'] = pd.to_datetime(df['Released']).dt.year

    #country = df.groupby(["Country", "Year"], as_index = False).agg({'Maximum Installs':'sum', 'Category':'nunique' })
    country = df.groupby(["Country","Category", "Year"], as_index = False).agg({'Maximum Installs':'sum', 'Installs':'sum' })
    country['G_Country'] = country['Country'].apply(lambda x: 'United States' if x == 'United States' else 'Other')
    
    # Define the options for the dropdown
    years = country['Year'].unique()
    year_options = [{'label': year, 'value': year} for year in years]
    
    # Define the options for the dropdown
    countries = country['G_Country'].unique()
    country_options = [{'label': country, 'value': country} for country in countries]

# Define the layout
    layout = html.Div([
        html.H1("Analysis Based On Countries", style={'fontSize': 30, 'fontWeight': 'bold'}),
        html.Div([
            html.Div([
                html.Label('Select a year:'),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=year_options,
                    value=years[0],
                    placeholder='Select a year',
                    clearable=False,
                    style={'width': '200px', 'margin-bottom': '10px'}
                ),
                dcc.Graph(id='map-graph')
            ], style={'width': '50%', 'display': 'inline-block'}),
            html.Div([
                html.Label('Select a country:'),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=country_options,
                    value='United States',
                    placeholder='Select a country',
                    clearable=False,
                    style={'width': '200px', 'margin-bottom': '10px'}
                ),
                dcc.Graph(id='category-graph')
            ], style={'width': '50%', 'display': 'inline-block'})
        ]),
    ])


    # Define the callback to update the map and category graph based on user selection
    @callback(
        [dash.dependencies.Output('map-graph', 'figure'),
         dash.dependencies.Output('category-graph', 'figure')],
        [dash.dependencies.Input('year-dropdown', 'value'),
         dash.dependencies.Input('country-dropdown', 'value')]
    )
    def update_graphs(year, selected_country):
        # Filter the data based on the selected year for the map
        filtered_year = country[country['Year'] == year]

        map_fig = px.choropleth(filtered_year, 
                                locations='Country', 
                                locationmode="country names", 
                                color='Maximum Installs', 
                                hover_name='Country',
                                hover_data = ['Category'],
                                projection='natural earth',
                                color_continuous_scale=px.colors.sequential.Purp)
        map_fig.update_layout(title_text='Total Installs by Country and Year', 
                              title_x=0.5, 
                              geo=dict(showframe=False, 
                                       showcoastlines=True,
                                       showcountries=True,  # Show country borders
                                       countrycolor='rgb(204, 204, 204)',
                                       projection_type='equirectangular'),
                              margin=dict(l=0, r=0, t=30, b=0))

        # Filter the data based on both year and selected country for the bar graph
        filtered_data = country[(country['G_Country'] == selected_country) & (country['Year'] == year)]
        category_fig = px.bar(filtered_data, x='Category', y='Installs', color='Category', 
                               title=f'Total Installs by Category for {selected_country}')
        category_fig.update_layout(title_x=0.5)

        return map_fig, category_fig
    return layout

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)