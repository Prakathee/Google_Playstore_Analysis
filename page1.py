import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import callback, dcc, html
import pandas as pd
import plotly.express as px


def get_page1_layout(df):

    page_1_layout = dbc.Container([
    html.H1('Analysis on App Categories', style={'fontSize': 30, 'fontWeight': 'bold'}),
    html.Label('Select Category', style={'fontWeight': 'bold'}),
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': c, 'value': c} for c in df['Category'].unique()],
        value='Adventure',
        style={"width": "200px"}
    ),
    html.Div(children = [dcc.Graph(id="installs-graph", style = {'display':'inline-block'}),
                        dcc.Graph(id="content-rating-graph", style = {'display':'inline-block'})]),
    html.Div(children = [dcc.Graph(id="ad-supported-graph", style = {'display':'inline-block'}),
                        dcc.Graph(id="size-graph", style = {'display':'inline-block'})]),
    html.Div(children = [dcc.Graph(id="content-rating-pie", style = {'display':'inline-block'}),
                        dcc.Graph(id="editors-choice-hist", style = {'display':'inline-block'})]),
    html.Div(children = [dcc.Graph(id="currency-bar", style = {'display':'inline-block'}),
                        dcc.Graph(id="max-installs-rating-scatter", style = {'display':'inline-block'})]),
    ], fluid=True)
    # Define callbacks
    @callback(
        [dash.dependencies.Output('installs-graph', 'figure'),
        dash.dependencies.Output('content-rating-graph', 'figure'),
        dash.dependencies.Output('ad-supported-graph', 'figure'),
        dash.dependencies.Output('size-graph', 'figure'),
        dash.dependencies.Output('content-rating-pie', 'figure'),
        dash.dependencies.Output('editors-choice-hist', 'figure'),
        dash.dependencies.Output('currency-bar', 'figure'),
        dash.dependencies.Output('max-installs-rating-scatter', 'figure')],
        [dash.dependencies.Input('category-dropdown', 'value')])
    def update_graphs(selected_category):
        filtered_df = df[df['Category'] == selected_category]
        
        # Installs graph
        fig1 = px.scatter(filtered_df, x='Rating', y='Installs', color='Free', hover_data=['App Name'])
        fig1.update_layout(title='Installs vs Rating')
        
        # Content rating graph
        fig2 = px.violin(filtered_df, x='Content Rating', y='Rating')
        fig2.update_layout(title='Rating vs Content Rating')
        
        # Ad supported graph
        fig3 = px.pie(filtered_df, names='Ad Supported')
        fig3.update_layout(title='Ad Supported Apps')
        
        # Size graph
        fig4 = px.histogram(filtered_df, x='Size')
        fig4.update_layout(title='Size Distribution')
        
        # Content rating pie chart
        fig5 = px.pie(filtered_df, names='Content Rating')
        fig5.update_layout(title='Content Rating Distribution')
        
        # Editor's choice histogram
        fig6 = px.histogram(filtered_df, x='Editors Choice', color='Ad Supported', barmode='group')
        fig6.update_layout(title='Editor\'s Choice Distribution', yaxis_title='Count', legend_title='Ad Supported')
        #fig6.update_traces(text=fig6['data'][0].y, texttemplate= '%{text:.2s}', textposition='auto')

        # Currency and price distribution graph (as bar plot)
        fig7 = px.bar(filtered_df, x='Currency', y='Price', hover_data=['App Name'])
        fig7.update_layout(title='Currency and Price Distribution', xaxis_title='Currency', yaxis_title='Price', legend_title='Currency')
        
        # New scatter plot
        fig8 = px.scatter(filtered_df, x="Maximum Installs", y="Rating Count", color="Content Rating", title="Content Rating and Maximum installations ")
        fig8.update_layout(xaxis_title="Maximum Installs", yaxis_title="Rating Count")
        
        return fig1, fig2, fig3, fig4, fig6, fig5, fig7, fig8
    return page_1_layout