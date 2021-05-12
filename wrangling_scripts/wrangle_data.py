import pandas as pd
import plotly.graph_objects as go
from collections import namedtuple
from wrangling_scripts.gen_fig_data import get_fig_one_data,\
                                           get_fig_two_data,\
                                           get_fig_three_data,\
                                           get_fig_four_data
import calendar
import json


# Constants
DATA = pd.read_csv('data/noise_data_clean.csv', index_col=0)


def return_figures():
    """Create 4 plotly visualizations for dashboard.

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """


    # FIGURE 1
    fig1_data = get_fig_one_data(DATA)

    graph_one = []
    graph_one.append(
      go.Scatter(x=fig1_data.x,
                 y=fig1_data.y_2019,
                 mode='lines',
                 name="2019")
    )

    graph_one.append(
      go.Scatter(x=fig1_data.x,
                 y=fig1_data.y_2020,
                 mode='lines',
                 name="2020")
    )
    graph_one.append(
      go.Scatter(x=fig1_data.x,
                 y=fig1_data.y_2021,
                 mode='lines',
                 name="2021")
    )
    layout_one = dict(title='<b>Noise complaints between January 2019 and April 2021<b>',
                      showlegend=True,
                      yaxis=dict(title='number of complaints'),)

    # FIGURE 2
    fig2_data = get_fig_two_data(DATA)

    graph_two = []

    graph_two.append(
      go.Bar(x=fig2_data.x,
             y=fig2_data.y_2019,
             name='2019'),
    )
    graph_two.append(
      go.Bar(x=fig2_data.x,
             y=fig2_data.y_2020,
             name='2020'),
    )

    layout_two = dict(title='<b>Noise complaints by borough<b>',
                      barmode='group',
                      yaxis=dict(title='number of complaints'),)

    # FIGURE 3
    fig3_data = get_fig_three_data(DATA)

    graph_three = []

    graph_three.append(
      go.Bar(x=fig3_data.x,
             y=fig3_data.y_2019,
             name='2019',)
    )
    graph_three.append(
      go.Bar(x=fig3_data.x,
             y=fig3_data.y_2020,
             name='2020',)
    )
    layout_three = dict(title='<b>Top 3 types of complaints<b>',
                        barmode='group',
                        xaxis=dict(title='type of complaint'),
                        yaxis = dict(title='number of complaints'),)

# FIGURE 4
    fig1_data = get_fig_four_data(DATA)

    graph_four = []

    for complaint_type in fig1_data.keys():

        graph_four.append(
          go.Bar(x=fig1_data.get(complaint_type).x,
                 y=fig1_data.get(complaint_type).y,
                 name=f'{complaint_type}',
                 orientation='h',)
        )

    layout_four = dict(title='<b>Daily types of complaints<b>',
                        barmode='stack',
                        xaxis=dict(title='percentage of total complaints'),)


    # Append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures
