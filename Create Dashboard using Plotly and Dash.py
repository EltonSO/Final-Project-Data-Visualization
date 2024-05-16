#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
#app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard", 
            style={'textAlign': 'center', 
            'color':'#503D36', 'font-size':24}),
    #May include style for title
    html.Div([#TASK 2.2: Add two dropdown menus
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}],
            value='Select Statistics', placeholder='Select a report type')
    ]),
    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value='Select Year'
        )),
    html.Div([#TASK 2.3: Add a division for output display
    html.Div(id='output-container', className='chart-grid', style={'display':'flex'})])
])
#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics': 
        return False
    else: 
        return True

#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), 
    Input(component_id='dropdown-statistics', component_property='value')
    ])

def update_output_container(selected_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Automobile sales fluctuation over recession period
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                                           title='Average Automobile Sales fluctuation over Recession Period'))

        # Plot 2: Average number of vehicles sold by vehicle type during recession period
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        chart2 = dcc.Graph(figure=px.line(average_sales, x='Vehicle_Type', y='Automobile_Sales',
                                           title="Average Automobile Sales by Vehicle type over Recession Period"))

        # Plot 3: Total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()
        labels = exp_rec.index
        sizes = exp_rec.values
        chart3 = dcc.Graph(figure=px.pie(values=sizes, names=labels,
                                          title='Total Expenditure share by Vehicle type during recessions'))

        # Plot 4: Effect of unemployment rate on vehicle type and sales during recession period
        unemp_rec = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        chart4 = dcc.Graph(figure=px.bar(unemp_rec, x='unemployment_rate', y='Automobile_Sales',
                                          color='Vehicle_Type',
                                          title='Effect of unemployment rate on vehicle type and sales'))

        return [html.Div(className='chart-item', children=[chart1, chart2]),
                html.Div(className='chart-item', children=[chart3, chart4])]

    elif selected_statistics == 'Yearly Statistics' and selected_year:
        yearly_data = data[data['Year'] == selected_year]

        # Plot 1: Yearly Automobile sales using line chart for the whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales', title='Yearly Automobile sales'))

        # Plot 2: Total Monthly Automobile sales using line chart
        tma = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        chart2 = dcc.Graph(figure=px.line(tma, x='Month', y='Automobile_Sales', title='Total Monthly Automobile sales'))

        # Plot 3: Average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                                          title='Average Vehicles Sold by Vehicle Type in the year {}'.format(
                                              selected_year)))

        # Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        sizes = exp_data['Advertising_Expenditure'].values
        labels = exp_data['Vehicle_Type'].values
        chart4 = dcc.Graph(figure=px.pie(values=sizes, names=labels,
                                          title='Total Advertisement Expenditure for each vehicle type'))

        return [html.Div(className='chart-item', children=[chart1, chart2]),
                html.Div(className='chart-item', children=[chart3, chart4])]

    else:
        return None


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

