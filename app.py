from dash.dependencies import Input, Output, State
from dash import Dash, dcc, html
from skimage import io


import plotly.graph_objects as go
import plotly.express as px


import markdown as md
import pandas as pd
import numpy as np
import scipy


app = Dash(__name__, suppress_callback_exceptions=True)
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
    html.H5('By HNXJ@GitHub (Hamed Nejat)')
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
        render_content2('tab-2-1')
        
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
    [Input('tabs', 'value')]
)
def render_content1(*args):
    
    try:
        
        tab = args[0]
    
    except:
        
        return
    
    print(tab)
    
    if tab == 'tab-1':
        
        
        __img = io.imread('blvu.png')

        __fig = px.imshow(__img, color_continuous_scale='gray')
        __fig.update_layout(coloraxis_showscale=False)
        __fig.update_xaxes(showticklabels=False)
        __fig.update_yaxes(showticklabels=False)
        
        md1 = "".format()
        
        return html.Div([
            dcc.Graph(figure=__fig),
            dcc.Markdown('''
            # Electrophysiological analysis app's GUI
            
            ''' + md1, mathjax=True),
            ]
        )
    
    elif tab == 'tab-2':
        
        return html.Div([
            html.H3('Figures'),
            dcc.Tabs(id='tabs2', value='tab-2-1', children=[
                dcc.Tab(label='LFPs', value='tab-2-1'),
                dcc.Tab(label='Spectrum', value='tab-2-2'),
                dcc.Tab(label='Spikes', value='tab-2-3'),
            ],
            style={'color':'brown',
                       'width':'99vw',
                       'height':50
                }),
            html.Div(id='tabs-content-2'),
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
                     children='Enter a value and press submit'),
            html.Div(id='container-button-basic',
                 children='Enter a value and press submit')
            ]),
            dcc.Markdown('''
            
            ''', mathjax=True),
            ]
        )
    
    elif tab == 'tab-3':
        
        return html.Div([
            html.H3('Results (TODO)'),
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
            html.H3('Analysis (TODO)'),
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
    [Input('tabs2', 'value')]
)
def render_content2(*args):
    
    try:
        
        tab = args[0]
    
    except:
        
        return
    
    if tab == 'tab-2-1':
        
        try:
            
            y = d['lfp']
            y = np.reshape(y[:, :, 1], [y.shape[0], y.shape[1]])
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
        
        md1 = "".format(4, 7)
        
        return html.Div([
            html.H3('Signal visualization'),
            dcc.Markdown('''
            
            ''' + md1, mathjax=True),
        
            dcc.Graph(mathjax=True, figure=fig),
            ]
        )
    
    elif tab == 'tab-2-2':
        
        try:
            
            y = d['lfp']
            y = np.reshape(y[:, :, 1], [y.shape[0], y.shape[1]])
            x = np.linspace(-1.5, 3, 4501)
            
        except:
            
            return html.Div([html.H3("Load file of your data before plotting.")])
            
        __wdt = np.arange(7)
        _f, _t, __psd = scipy.signal.spectrogram(y[:, 1], 1000, nfft=1000, nperseg=100)
        fmax_ = 100
        fig = px.imshow(img=__psd[40:fmax_, :], x=_t*1000, y=_f[40:fmax_], aspect='auto')
        print(__psd.shape)
        fig.update_layout(
            yaxis_title=r'$\text{ Frequency }$',
            xaxis_title=r'$\text{ Time }$',
            width=1470, height=740)
        
        return html.Div([
            html.H3('Spectrum'),
            dcc.Markdown('''
            
            ''', mathjax=True),
        
            dcc.Graph(mathjax=True, figure=fig),
            ]
        )
    
    elif tab == 'tab-2-3':
        
        # try: TODO : UNCOMMENT
            
        #     y = d['lfp']
        #     y = np.reshape(y[:, :, 1], [y.shape[0], y.shape[1]])
        #     x = np.linspace(-1.5, 3, 4501)
            
        # except:
            
        #     return html.Div([html.H3("Load file of your data before plotting.")])
            
        __wdt = np.arange(7)
        __psd = np.random.rand(100, 400) > 0.91
        fig = px.imshow(__psd)
        md1 = "".format(4, 7)
        
        return html.Div([
            html.H3('Spikes'),
            dcc.Markdown('''
            
            ''' + md1, mathjax=True),
        
            dcc.Graph(mathjax=True, figure=fig),
            ]
        )
    
    else:
        
        print("?")
        
        
if __name__ == '__main__':
    
    app.run_server(debug=True)
    