import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash_daq as daq

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
        html.H1("Budget Impact Analysis of DMPA-SC Introduction in South Africa Over 4 Years"),
        
        html.Div([
            html.P("This model evaluates the efficiency gains of introducing DMPA-SC for self injection resulting from transitioning users from DMPA-IM and NET-EN to DMPA-SC over a period of 4 years. "
                   "Input initial injectables user population sizes, annual method specific visit costs, annual method specific product costs, and yearly conversion rates. The model assumes linear progression and does not account for external factors."),
            html.H3("Starting Population Sizes"),
            html.Div([
                html.Div([
                    html.Label("NET-EN Starting Population"),
                    dcc.Input(id='neten-start-pop', type='number', value=500000)
                ], className='input-group'),
                html.Div([
                    html.Label("DMPA-IM Starting Population"),
                    dcc.Input(id='dmpim-start-pop', type='number', value=1700000)
                ], className='input-group'),
                html.Div([
                    html.Label("DMPA-SC Starting Population"),
                    dcc.Input(id='dmpsc-start-pop', type='number', value=0)
                ], className='input-group'),
            ]),
        ], className='container'),
        
        html.Div([
            html.H3("Annual Costs per User (Rand)"),
            html.P("Specify the annual method specific costs per user for each type of intervention."),
            html.Div([
                html.Div([
                    html.Label("NET-EN Visit Cost"),
                    dcc.Input(id='neten-visit-cost', type='number', value=1974)
                ], className='input-group'),
                html.Div([
                    html.Label("NET-EN Product Cost"),
                    dcc.Input(id='neten-product-cost', type='number', value=144)
                ], className='input-group'),
                html.Div([
                    html.Label("DMPA-IM Visit Cost"),
                    dcc.Input(id='dmpim-visit-cost', type='number', value=1316)
                ], className='input-group'),
                html.Div([
                    html.Label("DMPA-IM Product Cost"),
                    dcc.Input(id='dmpim-product-cost', type='number', value=63)
                ], className='input-group'),
                html.Div([
                    html.Label("DMPA-SC Visit Cost"),
                    dcc.Input(id='dmpsc-visit-cost', type='number', value=658)
                ], className='input-group'),
                html.Div([
                    html.Label("DMPA-SC Product Cost"),
                    dcc.Input(id='dmpsc-product-cost', type='number', value=116)
                ], className='input-group'),
            ])
        ], className='container'),
        
        html.Div([
            html.H3("Conversion Rates"),
            html.P("Specify the conversion rates from DMPA-IM and NET-EN to DMPA-SC for each year."),
            html.Div([
                html.H4("DMPA-IM to DMPA-SC Conversion Rates (%)"),
                html.Div([
                    html.Div([
                        html.Label("Year 1"),
                        dcc.Input(id='dmpim-conv-rate-1', type='number', value=25)
                    ], className='input-group'),
                    html.Div([
                        html.Label("Year 2"),
                        dcc.Input(id='dmpim-conv-rate-2', type='number', value=35)
                    ], className='input-group'),
                    html.Div([
                        html.Label("Year 3"),
                        dcc.Input(id='dmpim-conv-rate-3', type='number', value=40)
                    ], className='input-group'),
                    html.Div([
                        html.Label("Year 4"),
                        dcc.Input(id='dmpim-conv-rate-4', type='number', value=45)
                    ], className='input-group'),
                ])
            ]),
            html.Div([
                html.H4("NET-EN to DMPA-SC Conversion Rates (%)"),
                html.Div([
                    html.Div([
                        html.Label("Year 1"),
                        dcc.Input(id='neten-conv-rate-1', type='number', value=16)
                    ], className='input-group'),
                    html.Div([
                        html.Label("Year 2"),
                        dcc.Input(id='neten-conv-rate-2', type='number', value=35)
                    ], className='input-group'),
                    html.Div([
                        html.Label("Year 3"),
                        dcc.Input(id='neten-conv-rate-3', type='number', value=50)
                    ], className='input-group'),
                    html.Div([
                        html.Label("Year 4"),
                        dcc.Input(id='neten-conv-rate-4', type='number', value=65)
                    ], className='input-group'),
                ])
            ])
        ], className='container'),
        
        html.Div([
    html.H3("Manually defined Population Sizes (Optional)"),
    html.P("Optionally, specify the injectables user population sizes for each year if you want to override the model's calculations."),
    html.Button('Show/Hide Population Sizes', id='pop-size-button', n_clicks=0),
    html.Div(id='pop-size-div', style={'display': 'none'}, children=[
        html.Div([
            html.Label("Year 1 Population Sizes (NET-EN, DMPA-IM, DMPA-SC)"),
            dcc.Input(id='pop-sizes-year-1', type='text', placeholder='e.g., 450000, 1600000, 50000')
        ], className='input-group'),
        html.Div([
            html.Label("Year 2 Population Sizes (NET-EN, DMPA-IM, DMPA-SC)"),
            dcc.Input(id='pop-sizes-year-2', type='text', placeholder='e.g., 400000, 1500000, 100000')
        ], className='input-group'),
        html.Div([
            html.Label("Year 3 Population Sizes (NET-EN, DMPA-IM, DMPA-SC)"),
            dcc.Input(id='pop-sizes-year-3', type='text', placeholder='e.g., 350000, 1400000, 150000')
        ], className='input-group'),
        html.Div([
            html.Label("Year 4 Population Sizes (NET-EN, DMPA-IM, DMPA-SC)"),
            dcc.Input(id='pop-sizes-year-4', type='text', placeholder='e.g., 300000, 1300000, 200000')
        ], className='input-group'),
    ])
        ], className='container'),
        
        html.Div([
            html.H3("Color Palette Picker (Optional)"),
            html.P("Select the colors for the different categories in the graph."),
            html.Button('Show/Hide Color Pickers', id='color-picker-button', n_clicks=0),
            html.Div(id='color-picker-div', style={'display': 'none'}, children=[
                html.Div([
                    html.Label("NETEN Color"),
                    daq.ColorPicker(
                        id='neten-color',
                        value=dict(hex='#003f5c')  # Orange
                    )
                ], className='input-group'),
                html.Div([
                    html.Label("DMPIM Color"),
                    daq.ColorPicker(
                        id='dmpim-color',
                        value=dict(hex='#7a5195')  # Blue
                    )
                ], className='input-group'),
                html.Div([
                    html.Label("DMPSC Color"),
                    daq.ColorPicker(
                        id='dmpsc-color',
                        value=dict(hex='#ef5675')  # Green
                    )
                ], className='input-group'),
                html.Div([
                    html.Label("Efficiency Gain Color"),
                    daq.ColorPicker(
                        id='cost-saving-color',
                        value=dict(hex='#ffa600')  # Grey
                    )
                ], className='input-group')
            ])
        ], className='container'),
        
        html.Button('Update Plot', id='submit-button', n_clicks=0),
        html.Button('Export CSV', id='export-button', n_clicks=0),

        dcc.Download(id="download-dataframe-csv"),

        dcc.Graph(id='stacked-bar-plot')
    ], className='container')
])

def parse_pop_sizes(pop_sizes_str):
    if pop_sizes_str:
        try:
            return [int(x.strip()) for x in pop_sizes_str.split(',')]
        except ValueError:
            return None
    return None

def convert(n_source, n_sink, Conv):
    efflux = n_source * Conv
    n_source -= efflux
    n_sink += efflux
    return n_source, n_sink

# Add this callback function
@app.callback(
    Output('pop-size-div', 'style'),
    Input('pop-size-button', 'n_clicks'),
    State('pop-size-div', 'style')
)
def toggle_pop_size(n_clicks, style):
    if n_clicks % 2 == 1:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('color-picker-div', 'style'),
    Input('color-picker-button', 'n_clicks'),
    State('color-picker-div', 'style')
)
def toggle_color_picker(n_clicks, style):
    if n_clicks % 2 == 1:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    [Output('stacked-bar-plot', 'figure'),
     Output('download-dataframe-csv', 'data')],
    [Input('submit-button', 'n_clicks'),
     Input('export-button', 'n_clicks')],
    [State('neten-start-pop', 'value'),
     State('dmpim-start-pop', 'value'),
     State('dmpsc-start-pop', 'value'),
     State('neten-visit-cost', 'value'),
     State('neten-product-cost', 'value'),
     State('dmpim-visit-cost', 'value'),
     State('dmpim-product-cost', 'value'),
     State('dmpsc-visit-cost', 'value'),
     State('dmpsc-product-cost', 'value'),
     State('dmpim-conv-rate-1', 'value'),
     State('dmpim-conv-rate-2', 'value'),
     State('dmpim-conv-rate-3', 'value'),
     State('dmpim-conv-rate-4', 'value'),
     State('neten-conv-rate-1', 'value'),
     State('neten-conv-rate-2', 'value'),
     State('neten-conv-rate-3', 'value'),
     State('neten-conv-rate-4', 'value'),
     State('pop-sizes-year-1', 'value'),
     State('pop-sizes-year-2', 'value'),
     State('pop-sizes-year-3', 'value'),
     State('pop-sizes-year-4', 'value'),
     State('neten-color', 'value'),
     State('dmpim-color', 'value'),
     State('dmpsc-color', 'value'),
     State('cost-saving-color', 'value')]
)
def update_graph(submit_n_clicks, export_n_clicks, 
                 neten_start_pop, dmpim_start_pop, 
                 dmpsc_start_pop, 
                 neten_visit_cost, neten_product_cost, 
                 dmpim_visit_cost, 
                 dmpim_product_cost, dmpsc_visit_cost, 
                 dmpsc_product_cost,
                 dmpim_conv_rate_1, dmpim_conv_rate_2, 
                 dmpim_conv_rate_3, dmpim_conv_rate_4, 
                 neten_conv_rate_1, neten_conv_rate_2, 
                 neten_conv_rate_3, neten_conv_rate_4, 
                 pop_sizes_year_1, pop_sizes_year_2, 
                 pop_sizes_year_3, pop_sizes_year_4,
                 neten_color, dmpim_color, 
                 dmpsc_color, cost_saving_color):
    
    dmpim_conv_rates = [dmpim_conv_rate_1, dmpim_conv_rate_2, dmpim_conv_rate_3, dmpim_conv_rate_4]
    neten_conv_rates = [neten_conv_rate_1, neten_conv_rate_2, neten_conv_rate_3, neten_conv_rate_4]
    user_pop_sizes = [parse_pop_sizes(pop_sizes_year_1), parse_pop_sizes(pop_sizes_year_2), 
                      parse_pop_sizes(pop_sizes_year_3), parse_pop_sizes(pop_sizes_year_4)]
    
    n_neten, n_dmpim, n_dmpsc = neten_start_pop, dmpim_start_pop, dmpsc_start_pop
    
    # convert pct to proportion
    dmpim_Conv = [rate / 100 for rate in dmpim_conv_rates]
    neten_Conv = [rate / 100 for rate in neten_conv_rates]
    years = 4

    dmpim, dmpsc, neten = [n_dmpim], [n_dmpsc], [n_neten]

    for i in range(years):
        if user_pop_sizes[i] is not None:
            n_neten, n_dmpim, n_dmpsc = user_pop_sizes[i]
        else:
            n_dmpim, n_dmpsc = convert(n_dmpim, n_dmpsc, dmpim_Conv[i])
            n_neten, n_dmpsc = convert(n_neten, n_dmpsc, neten_Conv[i])
        
        dmpim.append(n_dmpim)
        neten.append(n_neten)
        dmpsc.append(n_dmpsc)

    dmpim_visit_costs = [d * dmpim_visit_cost for d in dmpim]
    dmpsc_visit_costs = [d * dmpsc_visit_cost for d in dmpsc]
    neten_visit_costs = [n * neten_visit_cost for n in neten]

    dmpim_product_costs = [d * dmpim_product_cost for d in dmpim]
    neten_product_costs = [n * neten_product_cost for n in neten]
    dmpsc_product_costs = [d * dmpsc_product_cost for d in dmpsc]

    baselinecost = sum(x[0] for x in [dmpim_visit_costs, dmpim_product_costs, neten_visit_costs, neten_product_costs, dmpsc_visit_costs, dmpsc_product_costs]) # adding sc costs in case there is a baseline with sc
    tot_costs = [sum(x) for x in zip(dmpim_visit_costs, dmpim_product_costs, 
                                     dmpsc_visit_costs, dmpsc_product_costs, 
                                     neten_visit_costs, neten_product_costs)]
    baseline_diff = [x - baselinecost for x in tot_costs]

    df = pd.DataFrame({
        'NET-EN Product': neten_product_costs,
        'NET-EN Visit': neten_visit_costs,
        'DMPA-IM Product': dmpim_product_costs,
        'DMPA-IM Visit': dmpim_visit_costs,
        'DMPA-SC Product': dmpsc_product_costs,
        'DMPA-SC Visit': dmpsc_visit_costs,
        'Efficiency gain': np.abs(baseline_diff)
    })
    
    df_users = pd.DataFrame({
        'Year': ['Baseline (Year 1-4)', 'Intervention Year 1', 'Intervention Year 2', 'Intervention Year 3', 'Intervention Year 4'],
        'NET-EN': neten,
        'DMPA-IM': dmpim,
        'DMPA-SC': dmpsc,
    })

    # Divide all costs by 1 billion
    for column in df.columns:
        df[column] = df[column] / 1e9

    # Picker colors
    colors = {
        'NET-EN': neten_color['hex'],
        'DMPA-IM': dmpim_color['hex'],
        'DMPA-SC': dmpsc_color['hex'],
        'Efficiency gain': cost_saving_color['hex']
    }

    fig = go.Figure()

    x_labels = ['Baseline<br>(Years 1-4)', 'Intervention<br>Year 1', 'Intervention<br>Year 2', 'Intervention<br>Year 3', 'Intervention<br>Year 4']

    for column in df.columns:
        if 'Visit' in column:
            fig.add_trace(go.Bar(x=x_labels, y=df[column], name=column, 
                                 marker_color=colors[column.split()[0]], opacity=0.65))
        elif 'Product' in column:
            fig.add_trace(go.Bar(x=x_labels, y=df[column], name=column, 
                                 marker_color=colors[column.split()[0]], opacity=1))
        else:  # Efficiency gain
            fig.add_trace(go.Bar(x=x_labels, y=df[column], name=column, 
                                 marker_color=colors[column], opacity=1))

    fig.update_layout(
        barmode='stack',
        title=f'Budget impact analysis of DMPA-SC for self injection introduction in South Africa over 4 years with specified conversion rates from DMPA-IM and NET-EN to DMPA-SC',
        xaxis_title='Year',
        yaxis_title='Costs in Billions of Rand',
        yaxis=dict(tickformat=".2f"),
        legend=dict(x=1.05, y=1, bordercolor="Black", borderwidth=2)
    )

# make output df for csv
    df_costs = pd.DataFrame({
        'Year': ['Baseline (Years 1-4)', 'Intervention Year 1', 'Intervention Year 2', 'Intervention Year 3', 'Intervention Year 4'],
        'NET-EN Product': neten_product_costs,
        'NET-EN Visit': neten_visit_costs,
        'DMPA-IM Product': dmpim_product_costs,
        'DMPA-IM Visit': dmpim_visit_costs,
        'DMPA-SC Product': dmpsc_product_costs,
        'DMPA-SC Visit': dmpsc_visit_costs,
        'Efficiency gain': np.abs(baseline_diff)
    })
    
    df_combined = pd.merge(df_users, df_costs, on='Year')
    
    # add a column that combines NET-EN and DMPA-IM for visit, and for product
    df_combined['NET-EN Visit + DMPA-IM Visit'] = df_combined['NET-EN Visit'] + df_combined['DMPA-IM Visit']
    df_combined['NET-EN Product + DMPA-IM Product'] = df_combined['NET-EN Product'] + df_combined['DMPA-IM Product']


    csv_data = dcc.send_data_frame(df_combined.to_csv, "user_population_and_costs.csv", index=False)

    if export_n_clicks > 0:
        return fig, csv_data
    else:
        return fig, None

if __name__ == '__main__':
    app.run_server(debug=True)
