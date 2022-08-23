# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                options=[{'label':html.Div(['All Sites'],style={'font-size':30}),'value':'ALL'}]+[{'label': html.Div([launch_site],style={'font-size':30}), 'value': launch_site} for launch_site in set(spacex_df['Launch Site'])],
                                value='ALL', placeholder="Select/Search for the launch site here", searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
								html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):", style={'width':'80%', 'padding':'3px', 'fontSize':'20px', 'text-align-last':'left'}),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000, marks={i:str(i) for i in range(0,10100,500)}, value=[min_payload, max_payload]),
                                html.Br(),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        filtered_df = spacex_df['class'].groupby(spacex_df['Launch Site']).sum()
        fig = px.pie(filtered_df, values = 'class', 
        names=filtered_df.index,
        color=filtered_df.index)
        fig.update_layout(font={'size': 25, 'family':'Times New Roman'}, title={'text': 'Sites of Falcon 9 Successful Launches', 'font': {'size': 30, 'family':'Times New Roman'}})
        return fig
    else:
        spacex_df['Landing Outcome'] = spacex_df['class'].apply(lambda x: 'Success' if x==1 else 'Failure')
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        filtered_df = filtered_df['Landing Outcome'].value_counts()
        fig = px.pie(filtered_df, values='Landing Outcome', 
        names=filtered_df.index,
        color=filtered_df.index,
        color_discrete_map={'Success':'blue', 'Failure':'red'})
        fig.update_layout(font={'size': 25, 'family':'Times New Roman'}, title={'text': 'Falcon 9 Launch Outcomes at ' + entered_site, 'font': {'size': 30, 'family':'Times New Roman'}})
        return fig
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
			  Input(component_id='payload-slider', component_property='value'))

def get_scatter_plot(entered_site, payload_slider):
    if entered_site=='ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>=payload_slider[0]) & (spacex_df['Payload Mass (kg)']<=payload_slider[1])]
        fig2 = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', labels={'Payload Mass (kg)':'Payload Mass (kg)', 'class':'Launch Outcome'})
        fig2.update_layout(font={'size': 20, 'family':'Times New Roman'}, title={'text': 'Launch success and payload mass at all sites', 'font': {'size': 30, 'family':'Times New Roman'}})
        return fig2
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site']==entered_site) & (spacex_df['Payload Mass (kg)']>=payload_slider[0]) & (spacex_df['Payload Mass (kg)']<=payload_slider[1])]
        fig2 = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', labels={'Payload Mass (kg)':'Payload Mass (kg)', 'class':'Launch Outcome'})
        fig2.update_layout(font={'size': 20, 'family':'Times New Roman'}, title={'text': 'Launch success and payload mass at ' + entered_site, 'font': {'size': 30, 'family':'Times New Roman'}})
        return fig2

# Run the app
if __name__ == '__main__':
    app.run_server()
	
	
# Which site has the largest successful launches? KSC LC-39A
# Which site has the highest launch success rate? KSC LC-39A
# Which payload range(s) has the highest launch success rate? 2700 - 3150 kg and 4900 - 5200 kg
# Which payload range(s) has the lowest launch success rate? 5350 - 6800 kg
# Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest launch success rate? FT (15/23)
