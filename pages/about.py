import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H1(children='About the GUI webapp'),

    html.Div(children='''
        This page will be completed soon...
    '''),
    dcc.Graph(id='Logo'),

])