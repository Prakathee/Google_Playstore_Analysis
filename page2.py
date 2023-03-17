import dash
import dash_bootstrap_components as dbc
from dash import dcc, callback
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import numpy as np

def get_page2_layout(df):
#replacing the Null Values in Released and Minimum Android using Forward fill method
    fill = ['Released']
    for x in fill:
        df[x].fillna(method = 'ffill', inplace = True)
        
    #replacing the Null Values in Rating and Rating Count using Forward Average of that column
    fill = ['Rating', 'Rating Count']
    for x in fill:
        mean = df[x].mean()
        df[x].fillna(mean, inplace = True)
        
    #removing rows with null values in all othercolumns, as they are very small

    df.dropna(subset = ['Size', 'Currency', 'Installs', 'Minimum Installs', 'App Name'],\
            inplace = True)

    #cleaning Installs Columns
    df['Installs'] = df['Installs'].str.split('+').str[0]    
    df['Installs'].replace(',','', regex = True, inplace = True) 
    df['Installs'] =df['Installs'].astype(np.int64)

    # Define layout
    layout = html.Div([
        html.H1("Ad Supported Vs Non Ad Supported", style={'fontSize': 30, 'fontWeight': 'bold'}),
        html.Label('Ad-Supported Apps: Select Yes or No'),
        dcc.Dropdown(
            id="ad-supported-dropdown",
            options=[
                {"label": "Yes", "value": True},
                {"label": "No", "value": False},
            ],
            value=True,
            placeholder="Select a value for Ad Supported",
            style={"width": "200px"}
        ),
        html.Div(children = [dcc.Graph(id="ratings-histogram", style = {'display':'inline-block'}),
                            dcc.Graph(id="installs-by-category", style = {'display':'inline-block'})]),  
        html.Div(children = [dcc.Graph(id="installs-by-rating-scatter", style = {'display':'inline-block'}),
                            dcc.Graph(id="free-vs-paid-pie", style = {'display':'inline-block'})]),
    ])

    # Define callbacks
    @callback(
        dash.dependencies.Output("ratings-histogram", "figure"),
        [dash.dependencies.Input("ad-supported-dropdown", "value")]
    )
    def update_ratings_histogram(ad_supported):
        filtered_df = df[df["Ad Supported"] == ad_supported]
        fig = px.histogram(filtered_df, x="Rating", nbins=20, title="App Ratings",
                        color_discrete_sequence=["#00cc96"])
        return fig

    @callback(
        dash.dependencies.Output("installs-by-category", "figure"),
        [dash.dependencies.Input("ad-supported-dropdown", "value")]
    )
    def update_installs_by_category(ad_supported):
        filtered_df = df[df["Ad Supported"] == ad_supported]
        grouped_df = filtered_df.groupby("Category", as_index=False)["Installs"].sum()
        fig = px.bar(grouped_df, x="Category", y="Installs", title="Installs by Category",
                    color_discrete_sequence=["#ef553b"])
        return fig

    @callback(
        dash.dependencies.Output("installs-by-rating-scatter", "figure"),
        [dash.dependencies.Input("ad-supported-dropdown", "value")]
    )
    def update_installs_by_rating(ad_supported):
        filtered_df = df[df["Ad Supported"] == ad_supported]
        fig = px.scatter(filtered_df, x="Rating", y="Installs", title="Installs by Rating",
                        color="Free", hover_name="App Name",
                        color_discrete_sequence=["#636efa", "#00cc96"])
        return fig

    @callback(
        dash.dependencies.Output("free-vs-paid-pie", "figure"),
        [dash.dependencies.Input("ad-supported-dropdown", "value")]
    )
    def update_free_vs_paid(ad_supported):
        filtered_df = df[df["Ad Supported"] == ad_supported]
        free_apps = filtered_df[filtered_df["Free"] == True]
        paid_apps = filtered_df[filtered_df["Free"] == False]
        labels = ["Free", "Paid"]
        values = [len(free_apps), len(paid_apps)]
        fig = px.pie(values=values, names=labels, title="Free vs Paid Apps",
                    color_discrete_sequence=["#ef553b", "#636efa"])
        return fig
    return layout
# Run app
if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)