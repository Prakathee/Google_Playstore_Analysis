import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import callback, dcc, html
import pandas as pd
import plotly.express as px

from page1 import get_page1_layout
from page2 import get_page2_layout
from page3 import get_page3_layout

print(dcc.__version__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.Div("Analysis on Google Play Store Data", style={'fontSize':50, 'textAlign':'center'}),
    html.H3('Welcome to Google Play Store Data Analysis'),
    html.P(' '),
    html.P('Please Select a Page to Continue'),
    html.P(' '),
    dcc.Link('Page 1: Category Based Analysis', href='/page-1'),
    html.P(' '),
    dcc.Link('Page 2: Ad-Supported App Vs Non Ad-Supported Apps', href='/page-2'),
    html.P(' '),
    dcc.Link('Page 3: Analysis Based on Countries', href='/page-3'),
    html.P(' '),
    html.P(' '),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


df = pd.read_csv("Google-Playstore_110.csv")
page_1_layout = get_page1_layout(df)
page_2_layout = get_page2_layout(df)
page_3_layout = get_page3_layout(df)
# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    else:
        return ""


if __name__ == '__main__':
    app.run_server(debug=False,port=80,host = '0.0.0.0', use_reloader=False)
