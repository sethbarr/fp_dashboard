vimport dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np

app = dash.Dash(__name__)
server = app.server

# Custom CSS for better styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f0f0f0;
            }
            .container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #2c3e50;
                text-align: center;
            }
            h3 {
                color: #34495e;
                border-bottom: 2px solid #ecf0f1;
                padding-bottom: 10px;
            }
            .input-container {
                display: flex;
                justify-content: space-between;
            }
            .input-group {
                margin-bottom: 15px;
            }
            .input-group label {
                display: inline-block;
                width: 180px;
                text-align: right;
                margin-right: 15px;
                color: #7f8c8d;
            }
            .input-group input {
                width: 120px;
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            button {
                display: block;
                margin: 20px auto;
                padding: 10px 20px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #2980b9;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div([
    html.Div([
        html.H1("Scenario 3: Change in costs over 4 years from IM and NETEN to SC"),
        
        html.Div([
            html.Div([
                html.H3("Annual Costs per User"),
                html.Div([
                    html.Div([
                        html.Label("NETEN Visit Cost"),
                        dcc.Input(id='neten-visit-cost', type='number', value=1974)
                    ], className='input-group'),
                    html.Div([
                        html.Label("NETEN Product Cost"),
                        dcc.Input(id='neten-product-cost', type='number', value=24)
                    ], className='input-group'),
                    html.Div([
                        html.Label("DMPIM Visit Cost"),
                        dcc.Input(id='dmpim-visit-cost', type='number', value=1316)
                    ], className='input-group'),
                    html.Div([
                        html.Label("DMPIM Product Cost"),
                        dcc.Input(id='dmpim-product-cost', type='number', value=16)
                    ], className='input-group'),
                    html.Div([
                        html.Label("DMPSC Visit Cost"),
                        dcc.Input(id='dmpsc-visit-cost', type='number', value=658)
                    ], className='input-group'),
                    html.Div([
                        html.Label("DMPSC Product Cost"),
                        dcc.Input(id='dmpsc-product-cost', type='number', value=116)
                    ], className='input-group'),
                ])
            ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

            html.Div([
                html.H3("Conversion Rates (%)"),
                html.Div([
                    html.Div([
                        html.Label("Year 1"),
                        dcc.Input(id='conv-rate-1', type='number', value=25)
                    ], className='input-group'),
                    html.Div([
                        html.Label("Year 2"),
                        dcc.Input(id='conv-rate-2', type='number', value=35)
                    ], className='input-group'),
                    html.Div([
                        html.Label("Year 3"),
                        dcc.Input(id='conv-rate-3', type='number', value=40)
                    ], className='input-group'),
                    html.Div([
                        html.Label("Year 4"),
                        dcc.Input(id='conv-rate-4', type='number', value=45)
                    ], className='input-group'),
                ])
            ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
        ], className='input-container'),
        
        html.Button('Update Plot', id='submit-button', n_clicks=0),
        
        dcc.Graph(id='stacked-bar-plot')
    ], className='container')
])

def convert(n_source, n_sink, Conv):
    efflux = n_source * Conv
    n_source = n_source - efflux
    n_sink = n_sink + efflux
    return n_source, n_sink

@app.callback(
    Output('stacked-bar-plot', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('neten-visit-cost', 'value'),
     State('neten-product-cost', 'value'),
     State('dmpim-visit-cost', 'value'),
     State('dmpim-product-cost', 'value'),
     State('dmpsc-visit-cost', 'value'),
     State('dmpsc-product-cost', 'value'),
     State('conv-rate-1', 'value'),
     State('conv-rate-2', 'value'),
     State('conv-rate-3', 'value'),
     State('conv-rate-4', 'value')]
)
def update_graph(n_clicks, neten_visit_cost, neten_product_cost, 
                 dmpim_visit_cost, dmpim_product_cost, 
                 dmpsc_visit_cost, dmpsc_product_cost, 
                 *conv_rates):
    
    # Hardcoded initial user numbers
    n_neten, n_dmpim, n_dmpsc = 500000, 1700000, 0
    
    Conv_slow = [rate/100 for rate in conv_rates]
    years = 4

    dmpim, dmpsc, neten = [n_dmpim], [n_dmpsc], [n_neten]

    for i in range(years):
        n_dmpim, n_dmpsc = convert(n_dmpim, n_dmpsc, Conv_slow[i])
        n_neten, n_dmpsc = convert(n_neten, n_dmpsc, Conv_slow[i])
        
        dmpim.append(n_dmpim)
        neten.append(n_neten)
        dmpsc.append(n_dmpsc)

    dmpim_visit_costs = [d * dmpim_visit_cost for d in dmpim]
    dmpsc_visit_costs = [d * dmpsc_visit_cost for d in dmpsc]
    neten_visit_costs = [n * neten_visit_cost for n in neten]

    dmpim_product_costs = [d * dmpim_product_cost for d in dmpim]
    neten_product_costs = [n * neten_product_cost for n in neten]
    dmpsc_product_costs = [d * dmpsc_product_cost for d in dmpsc]

    baselinecost = sum(x[0] for x in [dmpim_visit_costs, dmpim_product_costs, neten_visit_costs, neten_product_costs])
    tot_costs = [sum(x) for x in zip(dmpim_visit_costs,      dmpim_product_costs, 
                                     dmpsc_visit_costs, dmpsc_product_costs, 
                                     neten_visit_costs, neten_product_costs)]
    baseline_diff = [x - baselinecost for x in tot_costs]

    df = pd.DataFrame({
        'NETEN Product': neten_product_costs,
        'NETEN Visit': neten_visit_costs,
        'DMPIM Product': dmpim_product_costs,
        'DMPIM Visit': dmpim_visit_costs,
        'DMPSC Product': dmpsc_product_costs,
        'DMPSC Visit': dmpsc_visit_costs,
        'Cost saving': np.abs(baseline_diff)
    })
    
    # Divide all costs by 1 billion
    for column in df.columns:
        df[column] = df[column] / 1e9

    colors = {
        'NETEN': 'orange',
        'DMPIM': 'blue',
        'DMPSC': 'green',
        'Cost saving': 'grey'
    }

    fig = go.Figure()

    for column in df.columns:
        if 'Visit' in column:
            fig.add_trace(go.Bar(x=['Baseline', 'Year 1', 'Year 2', 'Year 3', 'Year 4'], y=df[column], name=column, 
                                 marker_color=colors[column.split()[0]], opacity=1))
        elif 'Product' in column:
            fig.add_trace(go.Bar(x=['Baseline', 'Year 1', 'Year 2', 'Year 3', 'Year 4'], y=df[column], name=column, 
                                 marker_color=colors[column.split()[0]], opacity=0.5))
        else:  # Cost saving
            fig.add_trace(go.Bar(x=['Baseline', 'Year 1', 'Year 2', 'Year 3', 'Year 4'], y=df[column], name=column, 
                                 marker_color=colors[column], opacity=0.5))

    fig.update_layout(
        barmode='stack',
        title=f'Scenario 3: change in costs over 4 years from IM and NETEN to SC (slow uptake: {", ".join([f"{rate}%" for rate in conv_rates])})',
        xaxis_title='Year',
        yaxis_title='Costs in Billions of Rand',
        yaxis=dict(tickformat=".2f"),
        legend=dict(x=1.05, y=1, bordercolor="Black", borderwidth=2)
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
