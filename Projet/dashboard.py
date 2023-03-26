import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import datetime
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,  # 5 minutes in milliseconds
        n_intervals=0
    ),
    dcc.Graph(id='kering-graph'),
    html.H3('Daily Report'),
    html.Div(id='daily-report')
])

@app.callback(
    Output('kering-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    df = pd.read_csv('kering_price.csv', names=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    fig = px.line(df, x='timestamp', y='price', title='Kering Price Over Time')
    return fig

@app.callback(
    Output('daily-report', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_daily_report(n):
    now = datetime.datetime.now()

    if now.hour != 20:
        return "Daily report updates at 8 PM."

    df = pd.read_csv('kering_price.csv', names=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    today = now.date()
    today_data = df[df['timestamp'].dt.date == today]

    if today_data.empty:
        return "No data available for today."

    open_price = today_data.iloc[0]['price']
    close_price = today_data.iloc[-1]['price']
    price_change = close_price - open_price
    daily_volatility = np.std(today_data['price'].pct_change().dropna())

    report = html.Div([
        html.P(f"Open Price: {open_price}"),
        html.P(f"Close Price: {close_price}"),
        html.P(f"Price Change: {price_change}"),
        html.P(f"Daily Volatility: {daily_volatility:.4f}"),
    ])

    return report

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0')
