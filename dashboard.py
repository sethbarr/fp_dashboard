import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_daq as daq

# Import helper functions
from dashboard_helpers import parse_pop_sizes, perform_calculations, create_plot, prepare_combined_data

# Initialize the Dash app
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

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("Budget Impact Analysis of DMPA-SC Introduction in South Africa Over 4 Years"),
        
        html.Div([
            html.P("This model evaluates the efficiency gains of introducing DMPA-SC for self injection resulting from transitioning users from DMPA-IM and NET-EN to DMPA-SC over a period of 4 years. "
                   "Input initial injectables user population sizes, annual method specific visit costs, annual method specific product costs, and yearly conversion rates. The model uses hypothetical product costs and is for exploratory purposes only."),
            html.H3("Starting Population Sizes"),
            html.Div([
                html.Div([
                    html.Label("NET-EN Starting Population"),
                    dcc.Input(id='neten-start-pop', type='number', value=552108)
                ], className='input-group'),
                html.Div([
                    html.Label("DMPA-IM Starting Population"),
                    dcc.Input(id='dmpim-start-pop', type='number', value=1701061)
                ], className='input-group'),
            ]),
        ], className='container'),
        
        html.Div([
            html.H3("Annual Costs per User (Rand)"),
            html.P("Specify the cost per visit (this should be the same for each intervention), the number of annual visits required for each intervention, and the annual method specific costs per user for each type of intervention. If the new intervention (DMPSA-SC) will require more intensive first visits use the multiplier option (default value 2) which will increase the cost for the first visit of the year to account for a longer first visit."),
            html.Div([
                html.Div([
                    html.Label("Cost per Visit"),
                    dcc.Input(id='visit-cost', type='number', value=329)
                ], className='input-group'),
                html.Div([
                    html.Label("NET-EN Number of Visits"),
                    dcc.Input(id='neten-visits', type='number', value=6)
                ], className='input-group'),
                html.Div([
                    html.Label("NET-EN Product Cost (6 Units/Year)"),
                    dcc.Input(id='neten-product-cost', type='number', value=143.52)
                ], className='input-group'),
                html.Div([
                    html.Label("DMPA-IM Number of Visits"),
                    dcc.Input(id='dmpim-visits', type='number', value=4)
                ], className='input-group'),
                html.Div([
                    html.Label("DMPA-IM Product Cost (4 Units/Year)"),
                    dcc.Input(id='dmpim-product-cost', type='number', value=63.4)
                ], className='input-group'),
                html.Div([
                    html.Label("DMPA-SC Number of Visits"),
                    dcc.Input(id='dmpsc-visits', type='number', value=2)
                ], className='input-group'),
                html.Div([
                    html.Label("DMPA-SC First Visit Multiplier"),
                    dcc.Input(id='dmpsc-first-visit-multiplier', type='number', value=2)
                ], className='input-group'),
                html.Div([
                    html.Label("DMPA-SC Product Cost (4 Units/Year)"),
                    dcc.Input(id='dmpsc-product-cost', type='number', value=116)
                ], className='input-group'),
            ])
        ], className='container'),
        
        html.Div([
            html.H3("Yearly Market Share Conversion"),
            html.P("Specify the yearly market share conversions from NET-EN and DMPA-IM to DMPA-SC."),
            html.Div([
                html.H4("NET-EN to DMPA-SC Market Share Conversion (%)"),
                html.Div([
                    html.Div([
                        html.Label("Year 1"),
                        dcc.Input(id='neten-conv-rate-1', type='number', value=25)
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
            ]),
            html.Div([
                html.H4("DMPA-IM to DMPA-SC Market Share Conversion (%)"),
                html.Div([
                    html.Div([
                        html.Label("Year 1"),
                        dcc.Input(id='dmpim-conv-rate-1', type='number', value=10) #15.8417599
                    ], className='input-group'),
                    html.Div([
                        html.Label("Year 2"),
                        dcc.Input(id='dmpim-conv-rate-2', type='number', value=15)
                    ], className='input-group'),
                    html.Div([
                        html.Label("Year 3"),
                        dcc.Input(id='dmpim-conv-rate-3', type='number', value=20)
                    ], className='input-group'),
                    html.Div([
                        html.Label("Year 4"),
                        dcc.Input(id='dmpim-conv-rate-4', type='number', value=25)
                    ], className='input-group'),
                ])
            ])
        ], className='container'),
        
        html.Div([
            html.H3("Manually Defined Population Sizes (Optional)"),
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
                        value=dict(hex='#003f5c')
                    )
                ], className='input-group'),
                html.Div([
                    html.Label("DMPIM Color"),
                    daq.ColorPicker(
                        id='dmpim-color',
                        value=dict(hex='#7a5195')
                    )
                ], className='input-group'),
                html.Div([
                    html.Label("DMPSC Color"),
                    daq.ColorPicker(
                        id='dmpsc-color',
                        value=dict(hex='#ef5675')
                    )
                ], className='input-group'),
                html.Div([
                    html.Label("Efficiency Gain Color"),
                    daq.ColorPicker(
                        id='cost-saving-color',
                        value=dict(hex='#ffa600')
                    )
                ], className='input-group')
            ])
        ], className='container'),
        
        html.Button('Update Plot', id='submit-button', n_clicks=0),
        html.Button('Export CSV', id='export-button', n_clicks=0),

        dcc.Download(id="download-dataframe-csv"),

        dcc.Graph(id='stacked-bar-plot'),

        html.H3("Combined Data"),
        dash_table.DataTable(
            id='combined-data-table',
            columns=[],
            data=[],
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '5px'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
        )
    ], className='container')
])

# Callback functions
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
     Output('download-dataframe-csv', 'data'),
     Output('combined-data-table', 'data'),
     Output('combined-data-table', 'columns')],
    [Input('submit-button', 'n_clicks'),
     Input('export-button', 'n_clicks')],
    [State('neten-start-pop', 'value'),
     State('dmpim-start-pop', 'value'),
     State('visit-cost', 'value'),
     State('neten-visits', 'value'),
     State('neten-product-cost', 'value'),
     State('dmpim-visits', 'value'),
     State('dmpim-product-cost', 'value'),
     State('dmpsc-visits', 'value'),
     State('dmpsc-first-visit-multiplier', 'value'),
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

def update_graph(submit_n_clicks, export_n_clicks, *args):
    # Prepare input data
    inputs = {
        'start_pops': args[:2],
        'cost_per_visit': args[2],
        'neten_costs': args[3:5],
        'dmpim_costs': args[5:7],
        'dmpsc_costs': [args[7], args[9]],
        'dmpsc_first_visit_multiplier': args[8],
        'dmpim_conv_rates': args[10:14],
        'neten_conv_rates': args[14:18],
        'user_pop_sizes': [parse_pop_sizes(pop_size) for pop_size in args[18:22]],
        'colors': {k: v['hex'] for k, v in zip(['neten', 'dmpim', 'dmpsc', 'efficiency_gain'], args[22:])}
    }

    # Perform calculations
    results = perform_calculations(inputs)

    # Prepare data for plotting and tables
    df = pd.DataFrame({
        'NET-EN Product': results['costs']['neten_product'],
        'NET-EN Visit': results['costs']['neten_visit'],
        'DMPA-IM Product': results['costs']['dmpim_product'],
        'DMPA-IM Visit': results['costs']['dmpim_visit'],
        'DMPA-SC Product': results['costs']['dmpsc_product'],
        'DMPA-SC Visit': results['costs']['dmpsc_visit'],
        'Total Costs': results['total_costs'],
        'Efficiency gain': results['efficiency_gains']
    })

    # Convert costs to billions
    df = df / 1e9

    # Create the plot
    fig = create_plot(df, inputs['colors'])

    # Prepare the combined data table
    df_combined = prepare_combined_data(results, inputs)

    # Prepare CSV data
    csv_data = dcc.send_data_frame(df_combined.to_csv, "user_population_and_costs.csv", index=False)

    # Prepare table data
    table_columns = [{"name": i, "id": i} for i in df_combined.columns]
    table_data = df_combined.to_dict('records')

    if export_n_clicks > 0:
        return fig, csv_data, table_data, table_columns
    else:
        return fig, None, table_data, table_columns

if __name__ == '__main__':
    app.run_server(debug=True)
