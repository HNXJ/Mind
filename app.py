import scipy
import numpy as np
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State


import plotly.express as px


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
    html.H5('FilePath'),
    dcc.Input(id='input-on-submit', type='text', name='a'),
    html.Div([
        html.Button('Submit', id='submit-val', n_clicks=0),
        html.Div(id='container-button-basic',
             children='Enter a value and press submit')
        ],
        style={'display':'none'}),
    
        dcc.Input(id='trial', type="number", value=1,
                placeholder="Index of {}".format("trial"),
                style={'color':'b',
                           'width':'10vw',
                           'height':20,
                           'top':'300px',
                           'left':'30px'
                    }), # Temp
        dcc.Input(id='channel', type="number", value=1,
                placeholder="Index of {}".format("channel"),
                style={'color':'b',
                           'width':'10vw',
                           'height':20,
                           'top':'300px',
                           'left':'30px'
                    }) # Temp
        
    ]
)


@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')
)
def update_output(n_clicks, value):
    return value


@app.callback(
    Output('tabs-content-1', 'children'),
    [Input('tabs', 'value'),
    Input('trial', 'value'),
    Input('channel', 'value')]
)
def render_content(*args):
    
    try:
        
        tab = args[0]
        n = args[1]
        m = args[2]
    
    except:
        
        return
    
    if tab == 'tab-1':
        
        fig = px.line(x=[1, 2, 3, 4], y=[1, 4, 9, 16], title=r'$\alpha_{1c} = 352 \pm 11 \text{ km s}^{-1}$')
        fig.update_layout(
            xaxis_title=r'$\sqrt{(n_\text{c}(t|{T_\text{early}}))}$',
            yaxis_title=r'$d, r \text{ (solar radius)}$')
        
        return html.Div([
            dcc.Markdown('''
            ## LaTeX in a Markdown component:
        
            This example uses the block delimiter:
            $$
            \\frac{1}{(\\sqrt{\\phi \\sqrt{5}}-\\phi) e^{\\frac25 \\pi}} =
            1+\\frac{e^{-2\\pi}} {1+\\frac{e^{-4\\pi}} {1+\\frac{e^{-6\\pi}}
            {1+\\frac{e^{-8\\pi}} {1+\\ldots} } } }
            $$
        
            This example uses the inline delimiter:
            $E^2=m^2c^4+p^2c^2$
        
            ## LaTeX in a Graph component:
        
            ''', mathjax=True),
        
            dcc.Graph(mathjax=True, figure=fig),
            ]
        )
    
    elif tab == 'tab-2':
        
        try:
            
            y = d['lfp']
            y = np.reshape(y[:, :, n], [y.shape[0], y.shape[1]])
            x = np.linspace(-1.5, 3, 4501)
            
        except:
            
            pass
            
        return html.Div([
            html.H3('Plot signals'),
            dcc.Graph(
                figure=dict(
                    data=
                    [dict(
                        x=x,
                        y=y[:, m],
                        type='scatter'
                        )
                    ],
                    layout=dict(
                        title="Plot Title",
                        xaxis_title="X Axis Title",
                        yaxis_title="Y Axis Title",
                        legend_title="Legend Title")
                    )
                )
        ])
    
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
        
        

if __name__ == '__main__':
    
    d = scipy.io.loadmat("data.mat")
    app.run_server(debug=True)
    