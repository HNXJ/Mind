from dash.dependencies import Input, Output, State
from dash import Dash, dcc, html
from skimage import io


import plotly.graph_objects as go
import plotly.express as px


import markdown as md
import pandas as pd
import numpy as np
import scipy


app = Dash(__name__)
app.layout = html.Div(
    [
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Home', value='tab-1'),
        dcc.Tab(label='Figures', value='tab-2'),
        dcc.Tab(label='Results', value='tab-3'),
        dcc.Tab(label='Analysis', value='tab-4'),
    ],
    style={'color':'cyan',
               'width':'99vw',
               'height':50
        }),
    
    html.Div(id='tabs-content-1'),
    
    html.Div([
    html.Div([
        html.Label('File Path : '),
        dcc.Input(id='filepath', type='text', placeholder='Enter a valid path to your file',
                  style={'color':'b',
                             'width':'10vw',
                             'height':20,
                             'top':'300px',
                             'left':'30px',
                      }),
        html.Button('Load from this path', id='submit-val', n_clicks=0),
        html.Div(id='container-button-basic',
             children='Enter a value and press submit')
        ]),
        html.Label('Trial num : '),
        dcc.Input(id='trial', type="number", value=1,
                placeholder="Index of {}".format("trial"),
                style={'color':'b',
                           'width':'10vw',
                           'height':20,
                           'top':'300px',
                           'left':'30px'
                    }), # Temp
        html.Label('Channel  : '),
        dcc.Input(id='channel', type="number", value=1,
                placeholder="Index of {}".format("channel"),
                style={'color':'b',
                           'width':'10vw',
                           'height':20,
                           'top':'300px',
                           'left':'30px'
                    }) # Temp
        ])
    ]
)


@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('filepath', 'value')
)
def load_file(n_clicks, value):
    
    
    global d
    
    try:
        
        fp = str(value)
        d = scipy.io.loadmat(fp) 
        y = d['lfp']
        y = y.shape
        
        md1 = "$Sections : {}, Trials : {}, Channels : {}$".format(y[0], y[1], y[2])
        
        return html.Div([
            dcc.Markdown('''
                         
            ## File details :
        
            Converting to NWB lfp format :
            
            ''' + md1 + ''' 
            
            Check if dimensions and their order in the file are in <Section , Trial , Channel , Signal> format (Ignore this message if they are correct)
            
            '''
            , mathjax=True)
            ])
            
    except:
        
        return html.Div(["File not found or it is broken. enter a valid path."],
                        style={'color':'red',
                               'fontsize':'10px',
                            })
           
    
# @app.callback(
#     Output('container-button-basic', 'children'),
#     Input('submit-val', 'n_clicks'),
#     State('filepath', 'value')
# )
# def load_file_flagger(n_clicks, value):
    
#     return "Loading the file ..."

@app.callback(
    Output('tabs-content-1', 'children'),
    [Input('tabs', 'value'),
    Input('trial', 'value')]
)
def render_content(*args):
    
    try:
        
        tab = args[0]
        n = args[1]
    
    except:
        
        return
    
    if tab == 'tab-1':
        
        
        fig = go.Figure()
        
        for i in range(10):
            
            y1 = np.random.rand(100) + i
            x1 = np.linspace(0, 1, 100)
            df1 = pd.DataFrame(dict(x = x1, y = y1))
            fig.add_trace(go.Scatter(x = x1, y = y1))
            
        fig.update_layout(
            xaxis_title=r'$\sqrt{(n_\text{c}(t|{T_\text{early}}))}$',
            yaxis_title=r'$d, r \text{ (solar radius)}$',
            width=1740, height=740)
        
        md1 = "By HNXJ@GitHub, BastoslabVU.com".format(4, 7)
        
        return html.Div([
            dcc.Markdown('''
            # Electrophysiological analysis GUI :
        
            
            ''' + md1, mathjax=True),
        
            dcc.Graph(mathjax=True, figure=fig), #px.imshow(img_flowchart)
            ]
        )
    
    elif tab == 'tab-2':
        
        try:
            
            y = d['lfp']
            y = np.reshape(y[:, :, n], [y.shape[0], y.shape[1]])
            x = np.linspace(-1.5, 3, 4501)
            
        except:
            
            return html.Div([html.H3("Load file of your data before plotting.")])
            
        fig = go.Figure()
        
        for i in range(y.shape[1]):
            
            y1 = y[:, i] + 1.0 * i
            x1 = np.linspace(0, 1, y.shape[0])
            df1 = pd.DataFrame(dict(x = x1, y = y1))
            fig.add_trace(go.Scatter(x = x1, y = y1))
            
        fig.update_layout(
            yaxis_title=r'$\text{ Amplitude of signals }$',
            xaxis_title=r'$\text{ Time }$',
            width=1470, height=740)
        
        md1 = "By HNXJ@GitHub, {} p {}".format(4, 7)
        
        return html.Div([
            html.H3('Signal visualization'),
            dcc.Tabs(id='tabs2', value='tab-2-1', children=[
                dcc.Tab(label='LFPs', value='tab-2-1'),
                dcc.Tab(label='Spectrum', value='tab-2-2'),
                dcc.Tab(label='Spikes', value='tab-2-3'),
                dcc.Tab(label='Connectivity', value='tab-2-4'),
            ],
            style={'color':'brown',
                       'width':'99vw',
                       'height':25
                }),
            html.Div(id='tabs-content-2'),
            dcc.Markdown('''
            
            ''' + md1, mathjax=True),
        
            dcc.Graph(mathjax=True, figure=fig), #px.imshow(img_flowchart)
            ]
        )
    
    elif tab == 'tab-3':
        
        return html.Div([
            html.H3('Results'),
            dcc.Graph(
                figure=dict(
                    data=[dict(
                        x=[1, 2, 3],
                        y=[5, 10, 6],
                        type='bar'
                    )]
                )
            )
        ])
    
    elif tab == 'tab-4':
        
        return html.Div([
            html.H3('Analysis'),
            dcc.Graph(
                figure=dict(
                    data=[dict(
                        x=[1, 2, 3],
                        y=[5, -10, 6],
                        type='bar'
                    )]
                )
            )
        ])
    
    else:
        
        print("?")
        
        
@app.callback(
    Output('tabs-content-2', 'children'),
    [Input('tabs', 'value')]
)
def render_content(*args):
    
    try:
        
        tab = args[0]
    
    except:
        
        return
    
    if tab == 'tab-2-1':
        
        
        fig = go.Figure()
        
        for i in range(10):
            
            y1 = np.random.rand(100) + i
            x1 = np.linspace(0, 1, 100)
            df1 = pd.DataFrame(dict(x = x1, y = y1))
            fig.add_trace(go.Scatter(x = x1, y = y1))
            
        fig.update_layout(
            xaxis_title=r'$\sqrt{(n_\text{c}(t|{T_\text{early}}))}$',
            yaxis_title=r'$d, r \text{ (solar radius)}$',
            width=1740, height=740)
        
        md1 = "By HNXJ@GitHub, BastoslabVU.com".format(4, 7)
        
        return html.Div([
            dcc.Markdown('''
            # Electrophysiological analysis GUI :
        
            
            ''' + md1, mathjax=True),
        
            dcc.Graph(mathjax=True, figure=fig), #px.imshow(img_flowchart)
            ]
        )
    
    elif tab == 'tab-2-2':
        
        try:
            
            y = d['lfp']
            y = np.reshape(y[:, :, n], [y.shape[0], y.shape[1]])
            x = np.linspace(-1.5, 3, 4501)
            
        except:
            
            return html.Div([html.H3("Load file of your data before plotting.")])
            
        fig = go.Figure()
        
        for i in range(y.shape[1]):
            
            y1 = y[:, i] + 1.0 * i
            x1 = np.linspace(0, 1, y.shape[0])
            df1 = pd.DataFrame(dict(x = x1, y = y1))
            fig.add_trace(go.Scatter(x = x1, y = y1))
            
        fig.update_layout(
            yaxis_title=r'$\text{ Amplitude of signals }$',
            xaxis_title=r'$\text{ Time }$',
            width=1470, height=740)
        
        md1 = "By HNXJ@GitHub, {} p {}".format(4, 7)
        
        return html.Div([
            html.H3('Signal visualization'),
            dcc.Tabs(id='tabs', value='tab-1', children=[
                dcc.Tab(label='LFPs', value='tab-2-1'),
                dcc.Tab(label='Spectrum', value='tab-2-2'),
                dcc.Tab(label='Spikes', value='tab-2-3'),
                dcc.Tab(label='Connectivity', value='tab-2-4'),
            ],
            style={'color':'brown',
                       'width':'99vw',
                       'height':25
                }),
            dcc.Markdown('''
            
            ''' + md1, mathjax=True),
        
            dcc.Graph(mathjax=True, figure=fig), #px.imshow(img_flowchart)
            ]
        )
    
    elif tab == 'tab-2-3':
        
        return html.Div([
            html.H3('Results'),
            dcc.Graph(
                figure=dict(
                    data=[dict(
                        x=[1, 2, 3],
                        y=[5, 10, 6],
                        type='bar'
                    )]
                )
            )
        ])
    
    elif tab == 'tab-2-4':
        
        return html.Div([
            html.H3('Analysis'),
            dcc.Graph(
                figure=dict(
                    data=[dict(
                        x=[1, 2, 3],
                        y=[5, -10, 6],
                        type='bar'
                    )]
                )
            )
        ])
    
    else:
        
        print("?")
        
        
if __name__ == '__main__':
    
    app.run_server(debug=True)
    