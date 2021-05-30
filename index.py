import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_table as dt
import pathlib


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("./data").resolve()

data = pd.read_csv(DATA_PATH.joinpath('gapminderDataFiveYear.csv'))

year_list = list(data['year'].unique())

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.H5('World Countries Information', className = 'title_text'),
            ])
        ], className = "title_container twelve columns")
    ], className = "row flex-display"),

    html.Div([
        html.Div([
            html.Div([
             html.P('Select Continent:', className = 'fix_label', style = {'color': 'black'}),
             html.P('Select Country:', className = 'fix_label', style = {'color': 'black'}),
                     ], className = 'adjust_title'),
            html.Div([
            dcc.Dropdown(id = 'select_continent',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         value = 'Asia',
                         placeholder = 'Select Continent',
                         options = [{'label': c, 'value': c}
                                    for c in data['continent'].unique()], className = 'dcc_compon'),


            dcc.Dropdown(id = 'select_countries',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         placeholder = 'Select Country',
                         options = [], className = 'dcc_compon'),
              ], className = 'adjust_drop_down_lists'),

            html.P('Year', className = 'fix_label', style = {'color': 'black'}),
            dcc.RangeSlider(id = 'select_years',
                            min = year_list[0],
                            max = year_list[-1],
                            step = None,
                            updatemode='drag',
                            value = [year_list[3], year_list[-2]],
                            marks = {str(yr): str(yr) for yr in year_list},
                            className = 'dcc_compon'),

        ], className = "create_container2 six columns", style = {'margin-bottom': '10px', "margin-top": "10px"}),

        html.Div([
         html.Div([
            html.Div(id = 'text1'),
            html.Div(id = 'text2'),
            html.Div(id = 'text3'),
                ], className = 'adjust_inline')
        ], className = "create_container2 six columns", style = {'margin-bottom': '10px', "margin-top": "10px"}),

    ], className = "row flex-display"),

    html.Div([
        html.Div([
            dcc.RadioItems(id = 'radio_items',
                           labelStyle = {"display": "inline-block"},
                           options = [{'label': 'Life Expectancy', 'value': 'life_expectancy'},
                                      {'label': 'Population', 'value': 'population'},
                                      {'label': 'gdpPercap', 'value': 'gdp_Per_cap'}],
                           value = 'life_expectancy',
                           style = {'text-align': 'center', 'color': 'black'},
                           className = 'dcc_compon'),
            dcc.Graph(id = 'line_chart',
                      config = {'displayModeBar': 'hover'}),

        ], className = 'create_container2 six columns'),

        html.Div([
            dt.DataTable(id = 'my_datatable',
                         columns = [{'name': i, 'id': i} for i in
                                    data.loc[:, ['country', 'year', 'pop',
                                                 'continent', 'lifeExp', 'gdpPercap']]],
                         sort_action = "native",
                         style_table = {"overflowX": "auto"},
                         sort_mode = "multi",
                         virtualization = True,
                         style_cell = {'textAlign': 'left',
                                       'min-width': '100px',
                                       'backgroundColor': '#F2F2F2',
                                       },
                         style_as_list_view = False,
                         style_header = {
                             'backgroundColor': '#9A38D5',
                             'fontWeight': 'bold',
                             'font': 'Lato, sans-serif',
                             'color': 'white',
                             'border': '1px solid #9A38D5'
                         },
                         style_data = {'textOverflow': 'hidden', 'color': 'black',
                                       'border': '1px solid orange'},
                         fixed_rows = {'headers': True},
                         )

        ], className = 'create_container2 six columns'),

    ], className = "row flex-display"),

], id= "mainContainer", style={"display": "flex", "flex-direction": "column"})

@app.callback(
    Output('select_countries', 'options'),
    Input('select_continent', 'value'))
def get_country_options(select_continent):
    data1 = data[data['continent'] == select_continent]
    return [{'label': i, 'value': i} for i in data1['country'].unique()]


@app.callback(
    Output('select_countries', 'value'),
    Input('select_countries', 'options'))
def get_country_value(select_countries):
    return [k['value'] for k in select_countries][0]


@app.callback(Output('text1', 'children'),
              [Input('select_continent', 'value')],
              [Input('select_years', 'value')])

def update_text(select_continent, select_years):
    data1 = data.groupby(['country', 'year', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()
    data2 = data1[(data1['continent'] == select_continent) & (data1['year'] >= select_years[0]) & (data1['year'] <= select_years[1])].nlargest(1, columns = ['pop'])
    data_continent = data2['continent'].iloc[0]
    top_year = data2['year'].iloc[0]
    top_country = data2['country'].iloc[0]
    top_pop = data2['pop'].iloc[0]

    return [

               html.H6('Top country by population in' + ' ' + data_continent,
                       style = {'textAlign': 'center',
                                'line-height': '1',
                                'color': '#006fe6'}
                       ),
               html.P('Year:' + '  ' + '{0:.0f}'.format(top_year),
                      style = {'textAlign': 'center',
                               'color': 'black',
                               'fontSize': 15,
                               'margin-top': '-3px'
                               }
                      ),
               html.P('Country:' + '  ' + top_country,
                      style = {'textAlign': 'center',
                               'color': 'black',
                               'fontSize': 15,
                               'margin-top': '-10px'
                               }
                      ),
               html.P('Population:' + '  ' + '{0:,.0f}'.format(top_pop),
                      style = {'textAlign': 'center',
                               'color': 'black',
                               'fontSize': 15,
                               'margin-top': '-10px'
                               }
                      ),


    ]

@app.callback(Output('text2', 'children'),
              [Input('select_continent', 'value')],
              [Input('select_years', 'value')])

def update_text(select_continent, select_years):
    data1 = data.groupby(['country', 'year', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()
    data2 = data1[(data1['continent'] == select_continent) & (data1['year'] >= select_years[0]) & (data1['year'] <= select_years[1])].nlargest(1, columns = ['lifeExp'])
    data_continent = data2['continent'].iloc[0]
    top_year = data2['year'].iloc[0]
    top_country = data2['country'].iloc[0]
    top_lifeexp = data2['lifeExp'].iloc[0]

    return [

               html.H6('Top country by life expectancy in' + ' ' + data_continent,
                       style = {'textAlign': 'center',
                                'line-height': '1',
                                'color': '#006fe6'}
                       ),
               html.P('Year:' + '  ' + '{0:.0f}'.format(top_year),
                      style = {'textAlign': 'center',
                               'color': 'black',
                               'fontSize': 15,
                               'margin-top': '-3px'
                               }
                      ),
               html.P('Country:' + '  ' + top_country,
                      style = {'textAlign': 'center',
                               'color': 'black',
                               'fontSize': 15,
                               'margin-top': '-10px'
                               }
                      ),
               html.P('Life Expectancy:' + '  ' + '{0:,.0f}'.format(top_lifeexp),
                      style = {'textAlign': 'center',
                               'color': 'black',
                               'fontSize': 15,
                               'margin-top': '-10px'
                               }
                      ),


    ]

@app.callback(Output('text3', 'children'),
              [Input('select_continent', 'value')],
              [Input('select_years', 'value')])

def update_text(select_continent, select_years):
    data1 = data.groupby(['country', 'year', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()
    data2 = data1[(data1['continent'] == select_continent) & (data1['year'] >= select_years[0]) & (data1['year'] <= select_years[1])].nlargest(1, columns = ['gdpPercap'])
    data_continent = data2['continent'].iloc[0]
    top_year = data2['year'].iloc[0]
    top_country = data2['country'].iloc[0]
    top_gdppercap = data2['gdpPercap'].iloc[0]

    return [

               html.H6('Top country by gdpPercap in' + ' ' + data_continent,
                       style = {'textAlign': 'center',
                                'line-height': '1',
                                'color': '#006fe6'}
                       ),
               html.P('Year:' + '  ' + '{0:.0f}'.format(top_year),
                      style = {'textAlign': 'center',
                               'color': 'black',
                               'fontSize': 15,
                               'margin-top': '-3px'
                               }
                      ),
               html.P('Country:' + '  ' + top_country,
                      style = {'textAlign': 'center',
                               'color': 'black',
                               'fontSize': 15,
                               'margin-top': '-10px'
                               }
                      ),
               html.P('gdpPercap:' + '  ' + '{0:,.0f}'.format(top_gdppercap),
                      style = {'textAlign': 'center',
                               'color': 'black',
                               'fontSize': 15,
                               'margin-top': '-10px'
                               }
                      ),


    ]



@app.callback(Output('line_chart', 'figure'),
              [Input('select_continent', 'value')],
              [Input('select_countries', 'value')],
              [Input('select_years', 'value')],
              [Input('radio_items', 'value')])

def update_graph(select_continent, select_countries, select_years, radio_items):
    data1 = data.groupby(['country', 'year', 'continent'])[['pop', 'lifeExp', 'gdpPercap']].sum().reset_index()
    data2 = data1[(data1['continent'] == select_continent) & (data1['country'] == select_countries) &
                  (data1['year'] >= select_years[0]) & (data1['year'] <= select_years[1])]

    if radio_items == 'life_expectancy':

     return {
        'data':[
            go.Scatter(
                x = data2['year'],
                y = data2['lifeExp'],
                mode = 'text + markers + lines',
                text = data2['lifeExp'],
                texttemplate = '%{text:.0f}',
                textposition = 'bottom right',
                line = dict(width = 3, color = '#38D56F'),
                marker = dict(size = 10, symbol = 'circle', color = '#38D56F',
                              line = dict(color = '#38D56F', width = 2)
                              ),
                textfont = dict(
                    family = "sans-serif",
                    size = 12,
                    color = 'black'),

                hoverinfo = 'text',
                hovertext =
                '<b>Country</b>: ' + data2['country'].astype(str) + '<br>' +
                '<b>Year</b>: ' + data2['year'].astype(str) + '<br>' +
                '<b>Continent</b>: ' + data2['continent'].astype(str) + '<br>' +
                '<b>Life Expectancy</b>: ' + [f'{x:,.3f}' for x in data2['lifeExp']] + '<br>'

            )],


        'layout': go.Layout(
             plot_bgcolor='#F2F2F2',
             paper_bgcolor='#F2F2F2',
             title={
                'text': '<b>Life expectancy' + ' ' + ' to '.join([str(y) for y in select_years]),

                'y': 0.99,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': '#38D56F',
                        'size': 17},

             hovermode='closest',
             margin = dict(t = 15, r = 0),

             xaxis = dict(title = '<b>Years</b>',
                          visible = True,
                          color = 'black',
                          showline = True,
                          showgrid = False,
                          showticklabels = True,
                          linecolor = 'black',
                          linewidth = 1,
                          ticks = 'outside',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'black')

                         ),

             yaxis = dict(title = '<b>Life Expectancy</b>',
                          visible = True,
                          color = 'black',
                          showline = False,
                          showgrid = True,
                          showticklabels = True,
                          linecolor = 'black',
                          linewidth = 1,
                          ticks = '',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'black')

                         ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},

            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'white'),

        )

    }

    elif radio_items == 'population':

     return {
        'data':[
            go.Scatter(
                x = data2['year'],
                y = data2['pop'],
                mode = 'text + markers + lines',
                text = data2['pop'],
                texttemplate = '%{text:,.2s}',
                textposition = 'top center',
                line = dict(width = 3, color = '#9A38D5'),
                marker = dict(size = 10, symbol = 'circle', color = '#9A38D5',
                              line = dict(color = '#9A38D5', width = 2)
                              ),
                textfont = dict(
                    family = "sans-serif",
                    size = 12,
                    color = 'black'),

                hoverinfo = 'text',
                hovertext =
                '<b>Country</b>: ' + data2['country'].astype(str) + '<br>' +
                '<b>Year</b>: ' + data2['year'].astype(str) + '<br>' +
                '<b>Continent</b>: ' + data2['continent'].astype(str) + '<br>' +
                '<b>Population</b>: ' + [f'{x:,.0f}' for x in data2['pop']] + '<br>'

            )],


        'layout': go.Layout(
             plot_bgcolor='#F2F2F2',
             paper_bgcolor='#F2F2F2',
             title={
                'text': '<b>Population' + ' ' + ' to '.join([str(y) for y in select_years]),

                'y': 0.99,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': '#9A38D5',
                        'size': 17},

             hovermode='closest',
             margin = dict(t = 15, r = 0),

             xaxis = dict(title = '<b>Years</b>',
                          visible = True,
                          color = 'black',
                          showline = True,
                          showgrid = False,
                          showticklabels = True,
                          linecolor = 'black',
                          linewidth = 1,
                          ticks = 'outside',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'black')

                         ),

             yaxis = dict(title = '<b>Population</b>',
                          visible = True,
                          color = 'black',
                          showline = False,
                          showgrid = True,
                          showticklabels = True,
                          linecolor = 'black',
                          linewidth = 1,
                          ticks = '',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'black')

                         ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},

            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'white'),

        )

    }

    elif radio_items == 'gdp_Per_cap':

     return {
        'data':[
            go.Scatter(
                x = data2['year'],
                y = data2['gdpPercap'],
                mode = 'text + markers + lines',
                text = data2['gdpPercap'],
                texttemplate = '%{text:,.0f}',
                textposition = 'bottom right',
                line = dict(width = 3, color = '#FFA07A'),
                marker = dict(size = 10, symbol = 'circle', color = '#FFA07A',
                              line = dict(color = '#FFA07A', width = 2)
                              ),
                textfont = dict(
                    family = "sans-serif",
                    size = 12,
                    color = 'black'),

                hoverinfo = 'text',
                hovertext =
                '<b>Country</b>: ' + data2['country'].astype(str) + '<br>' +
                '<b>Year</b>: ' + data2['year'].astype(str) + '<br>' +
                '<b>Continent</b>: ' + data2['continent'].astype(str) + '<br>' +
                '<b>gdpPercap</b>: ' + [f'{x:,.6f}' for x in data2['gdpPercap']] + '<br>'

            )],


        'layout': go.Layout(
             plot_bgcolor='#F2F2F2',
             paper_bgcolor='#F2F2F2',
             title={
                'text': '<b>gdpPercap' + ' ' + ' to '.join([str(y) for y in select_years]),

                'y': 1,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': '#FFA07A',
                        'size': 17},

             hovermode='closest',
             margin = dict(t = 15, r = 0),

             xaxis = dict(title = '<b>Years</b>',
                          visible = True,
                          color = 'black',
                          showline = True,
                          showgrid = False,
                          showticklabels = True,
                          linecolor = 'black',
                          linewidth = 1,
                          ticks = 'outside',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'black')

                         ),

             yaxis = dict(title = '<b>gdpPercap</b>',
                          visible = True,
                          color = 'black',
                          showline = False,
                          showgrid = True,
                          showticklabels = True,
                          linecolor = 'black',
                          linewidth = 1,
                          ticks = '',
                          tickfont = dict(
                             family = 'Arial',
                             size = 12,
                             color = 'black')

                         ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},

            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'white'),

        )

    }

@app.callback(Output('my_datatable', 'data'),
              [Input('select_continent', 'value')],
              [Input('select_countries', 'value')],
              [Input('select_years', 'value')])
def display_table(select_continent, select_countries, select_years):
    data_table = data[(data['continent'] == select_continent) & (data['country'] == select_countries) &
                      (data['year'] >= select_years[0]) & (data['year'] <= select_years[1])]
    return data_table.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)