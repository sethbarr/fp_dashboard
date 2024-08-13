# dashboard_helpers.py

import pandas as pd
import plotly.graph_objs as go
import numpy as np

def parse_pop_sizes(pop_sizes_str):
    """Parse population sizes from a string input."""
    if pop_sizes_str:
        try:
            return [int(x.strip()) for x in pop_sizes_str.split(',')]
        except ValueError:
            return None
    return None

def convert_population(source_pop, sink_pop, conversion_rate):
    """Calculate population conversion."""
    converted = int(source_pop * conversion_rate)
    source_pop -= converted
    sink_pop += converted
    return source_pop, sink_pop

def calculate_costs(population, visit_cost, product_cost):
    """Calculate visit and product costs for a given population."""
    return population * visit_cost, population * product_cost


def perform_calculations(inputs):
    """Perform main calculations for the dashboard."""
    neten_start_pop, dmpim_start_pop, dmpsc_start_pop = inputs['start_pops']
    neten_visit_cost, neten_product_cost = inputs['neten_costs']
    dmpim_visit_cost, dmpim_product_cost = inputs['dmpim_costs']
    dmpsc_visit_cost, dmpsc_product_cost = inputs['dmpsc_costs']
    dmpim_conv_rates = inputs['dmpim_conv_rates']
    neten_conv_rates = inputs['neten_conv_rates']
    user_pop_sizes = inputs['user_pop_sizes']

    # Initialize populations
    n_neten, n_dmpim, n_dmpsc = neten_start_pop, dmpim_start_pop, dmpsc_start_pop
    total_start_pop = n_neten + n_dmpim + n_dmpsc

    # Convert rates to decimals
    dmpim_conv_rates = [rate / 100 for rate in dmpim_conv_rates]
    neten_conv_rates = [rate / 100 for rate in neten_conv_rates]

    years = 4
    dmpim, dmpsc, neten = [n_dmpim], [n_dmpsc], [n_neten]

    # Manual NET-EN population sizes (as provided)
    manual_neten_pop_sizes = [552108, 557630, 563206, 568838]

    for i in range(years):
        if user_pop_sizes[i] is not None:
            n_neten, n_dmpim, n_dmpsc = user_pop_sizes[i]
        elif neten_start_pop > 0:
                        # Calculate populations based on conversion rates
            n_dmpim = int(dmpim_start_pop * (1 - dmpim_conv_rates[i]))
            n_neten = int(manual_neten_pop_sizes[i] * (1 - neten_conv_rates[i]))
            n_dmpsc = int(dmpim_start_pop * dmpim_conv_rates[i]) + int(manual_neten_pop_sizes[i] * neten_conv_rates[i])
        elif neten_start_pop == 0:
        # else:
            # Calculate populations based on conversion rates
            n_dmpim = int(dmpim_start_pop * (1 - dmpim_conv_rates[i]))
            n_neten = 0
            n_dmpsc = int(dmpim_start_pop * dmpim_conv_rates[i]) 

        dmpim.append(n_dmpim)
        neten.append(n_neten)
        dmpsc.append(n_dmpsc)

    # Calculate costs
    dmpim_visit_costs = [d * dmpim_visit_cost for d in dmpim]
    dmpsc_visit_costs = [d * dmpsc_visit_cost for d in dmpsc]
    neten_visit_costs = [n * neten_visit_cost if n > 0 else 0 for n in neten]

    dmpim_product_costs = [d * dmpim_product_cost for d in dmpim]
    dmpsc_product_costs = [d * dmpsc_product_cost for d in dmpsc]
    neten_product_costs = [n * neten_product_cost if n > 0 else 0 for n in neten]

    # Calculate total costs
    total_costs = [sum(x) for x in zip(dmpim_visit_costs, dmpim_product_costs,
                                       dmpsc_visit_costs, dmpsc_product_costs,
                                       neten_visit_costs, neten_product_costs)]
    print("Total costs:")
    print(total_costs)

    # Calculate baseline costs (now accounting for NET-EN population variations)
    if dmpim_start_pop > 0:
        # If NET-EN starting population is provided, calculate baseline costs
        # baseline_dmpim_costs = [dmpim_start_pop] + [552108, 557630, 563206, 568838]
        baseline_dmpim_costs = [dmpim_start_pop * (dmpim_visit_cost + dmpim_product_cost)] * (years + 1)
    else:
        # If no NET-EN starting population, fill with zeros
        baseline_dmpim_costs = [0] * (years + 1)

    # baseline_dmpim_costs = [dmpim_start_pop * (dmpim_visit_cost + dmpim_product_cost)] * (years + 1)
    baseline_dmpsc_costs = [dmpsc_start_pop * (dmpsc_visit_cost + dmpsc_product_cost)] * (years + 1)
    # Check if user supplied a starting value for NET-EN
    if neten_start_pop > 0:
        # If NET-EN starting population is provided, calculate baseline costs
        neten_populations = [neten_start_pop] + [552108, 557630, 563206, 568838]
        baseline_neten_costs = [n * (neten_visit_cost + neten_product_cost) for n in neten_populations]
    else:
        # If no NET-EN starting population, fill with zeros
        baseline_neten_costs = [0] * (years + 1)
    # baseline_neten_costs = [n * (neten_visit_cost + neten_product_cost) if n > 0 else 0 for n in manual_neten_pop_sizes]
    print("Neten baseline costs:")
    print(baseline_neten_costs)

    baseline_costs = [sum(x) for x in zip(baseline_dmpim_costs, baseline_dmpsc_costs, baseline_neten_costs)]
    
    # initial baseline costs should be the same for baseline yr and year 1
    # baseline_costs.insert(0, baseline_costs[0])
    
    print("Baseline costs:")
    print(baseline_costs)

    # Calculate efficiency gains
    efficiency_gains = []
    print("\nCalculating efficiency gains:")
    for year, (baseline, total) in enumerate(zip(baseline_costs, total_costs)):
        gain = baseline - total
        print(f"Year {year+1}: Baseline {baseline} - Total {total} = Gain {gain}")
        efficiency_gains.append(gain)

    print("\nFinal efficiency gains:")
    print(efficiency_gains)

    # # Calculate efficiency gains
    # efficiency_gains = [b - t for b, t in zip(baseline_costs, total_costs)]

    # Ensure all arrays have the same length (5 elements: baseline + 4 years)
    def pad_array(arr, target_length=5):
        return [arr[0]] * (target_length - len(arr)) + arr if len(arr) < target_length else arr

    return {
        'populations': {
            'neten': pad_array(neten),
            'dmpim': pad_array(dmpim),
            'dmpsc': pad_array(dmpsc)
        },
        'costs': {
            'neten_visit': pad_array(neten_visit_costs),
            'neten_product': pad_array(neten_product_costs),
            'dmpim_visit': pad_array(dmpim_visit_costs),
            'dmpim_product': pad_array(dmpim_product_costs),
            'dmpsc_visit': pad_array(dmpsc_visit_costs),
            'dmpsc_product': pad_array(dmpsc_product_costs),
        },
        'total_costs': pad_array(total_costs),
        'baseline_costs': pad_array(baseline_costs),
        'efficiency_gains': pad_array(efficiency_gains)
    }
    
def create_plot(df, colors):
    """Create the main plot for the dashboard."""
    fig = go.Figure()

    x_labels = ['Baseline<br>(Years 1-4)', 'Intervention<br>Year 1', 'Intervention<br>Year 2', 'Intervention<br>Year 3', 'Intervention<br>Year 4']

    # Create a mapping between column prefixes and color keys
    color_mapping = {
        'NET-EN': 'neten',
        'DMPA-IM': 'dmpim',
        'DMPA-SC': 'dmpsc',
        'Efficiency': 'efficiency_gain'
    }

    for column in df.columns:
        prefix = column.split()[0]
        if prefix in color_mapping:
            color_key = color_mapping[prefix]
            if 'Visit' in column:
                fig.add_trace(go.Bar(x=x_labels, y=df[column], name=column, 
                                     marker_color=colors.get(color_key, '#808080'), opacity=0.65))
            elif 'Product' in column:
                fig.add_trace(go.Bar(x=x_labels, y=df[column], name=column, 
                                     marker_color=colors.get(color_key, '#808080'), opacity=1))
            else:  # Efficiency gain
                fig.add_trace(go.Bar(x=x_labels, y=df[column], name=column, 
                                     marker_color=colors.get(color_key, '#808080'), opacity=1))

    fig.update_layout(
        barmode='stack',
        title='Budget impact analysis of DMPA-SC for self injection introduction in South Africa<br>over 4 years with specified conversion rates from DMPA-IM and NET-EN to DMPA-SC',
        xaxis_title='Year',
        yaxis_title='Costs in Billions of Rand',
        yaxis=dict(tickformat=".2f"),
        legend=dict(x=1.05, y=1)
    )

    return fig


def prepare_combined_data(results, inputs):
    """Prepare combined data for the dashboard table."""
    years = ['Baseline (Year 1-4)', 'Intervention Year 1', 'Intervention Year 2', 'Intervention Year 3', 'Intervention Year 4']
    
    df_users = pd.DataFrame({
        'Year': years,
        'NET-EN Users': results['populations']['neten'],
        'DMPA-IM Users': results['populations']['dmpim'],
        'DMPA-SC Users': results['populations']['dmpsc'],
        'NET-EN + DMPA-IM Users': [sum(x) for x in zip(results['populations']['neten'], results['populations']['dmpim'])],
    })
    
    # Ensure all cost arrays have the same length
    def pad_array(arr, target_length=5):
        return [arr[0]] * (target_length - len(arr)) + arr if len(arr) < target_length else arr

    baseline_costs = pad_array(results['baseline_costs'])
    
    df_costs = pd.DataFrame({
        'Year': years,
        'NET-EN Product': results['costs']['neten_product'],
        'NET-EN Visit': results['costs']['neten_visit'],
        'DMPA-IM Product': results['costs']['dmpim_product'],
        'DMPA-IM Visit': results['costs']['dmpim_visit'],
        'DMPA-SC Product': results['costs']['dmpsc_product'],
        'DMPA-SC Visit': results['costs']['dmpsc_visit'],
        'Total Costs': results['total_costs'],
        'Total Baseline Costs': baseline_costs,
        'Efficiency gain': results['efficiency_gains']
    })
    
    df_combined = pd.merge(df_users, df_costs, on='Year')
    
    df_combined['NET-EN Visit + DMPA-IM Visit'] = df_combined['NET-EN Visit'] + df_combined['DMPA-IM Visit']
    df_combined['NET-EN Product + DMPA-IM Product'] = df_combined['NET-EN Product'] + df_combined['DMPA-IM Product']
    
    df_combined = df_combined[['Year', 'NET-EN + DMPA-IM Users', 'NET-EN Users', 'DMPA-IM Users', 'DMPA-SC Users', 
                               'NET-EN Visit + DMPA-IM Visit', 'NET-EN Visit', 'DMPA-IM Visit', 'DMPA-SC Visit',
                               'NET-EN Product + DMPA-IM Product', 'NET-EN Product', 'DMPA-IM Product', 'DMPA-SC Product', 
                               'Total Costs', 'Total Baseline Costs', 'Efficiency gain']]
    # Round all numeric columns to 2 decimal places
    numeric_columns = df_combined.select_dtypes(include=[np.number]).columns
    df_combined[numeric_columns] = df_combined[numeric_columns].round(2)
    
    return df_combined