# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX launch data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create options for the dropdown menu
all_sites = [{'label': 'All Sites', 'value': 'ALL'}]
launch_sites = [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]

# Concatenate all_sites and launch_sites options
dropdown_options = all_sites + launch_sites

# Set up the app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=dropdown_options,
        value='ALL',  # Default value is 'ALL'
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    
    html.Br(),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    
])

# Callback function to update success-pie-chart based on dropdown selection
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        filtered_df = spacex_df.copy()
        title = 'Success Rate for All Launch Sites'
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        title = f'Success Rate for {selected_site}'
    
    success_counts = filtered_df['class'].value_counts()
    fig = px.pie(success_counts, values=success_counts.values, names=success_counts.index,
                 title=title, hole=0.3)
    
    return fig

# Callback function to update success-payload-scatter-chart based on dropdown and range slider selection
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df.copy()
        title = 'Payload Success Rate for All Launch Sites'
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        title = f'Payload Success Rate for {selected_site}'
    
    low, high = payload_range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= low) & (filtered_df['Payload Mass (kg)'] <= high)]
    
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version',
                     title=title, marginal_y='violin', trendline='ols')
    
    return fig

# Add a RangeSlider to select payload
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=dropdown_options,
        value='ALL',  # Default value is 'ALL'
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    
    # TASK 3: Add a RangeSlider to Select Payload
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        value=[min_payload, max_payload],
        marks={min_payload: str(min_payload), max_payload: str(max_payload)}
    ),
    
    html.Br(),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    
])

# Callback function to update success-payload-scatter-chart based on dropdown and range slider selection
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df.copy()
        title = 'Payload Success Rate for All Launch Sites'
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        title = f'Payload Success Rate for {selected_site}'
    
    low, high = payload_range
    filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= low) & (filtered_df['Payload Mass (kg)'] <= high)]
    
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version',
                     title=title, marginal_y='violin', trendline='ols')
    
    return fig



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
    


