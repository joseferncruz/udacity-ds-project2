from collections import namedtuple
import calendar

# Constants
MONTHS = [month for month in calendar.month_name if month]
DAY_NAMES = list(calendar.day_name)


# FIGURE 1
def get_fig_one_data(data):
    """Return a namedTuple with data for figure one."""

    fig1_data = namedtuple('fig1', 'x y_2019 y_2020 y_2021')

    # subset data from clean dataset
    noise_year = data[~((data.year.isin([2021]))
                      & (data.month.isin([5])))].groupby(['year', 'month'])['complaint_type']\
                                                .count()\
                                                .reset_index()\
                                                .rename({'complaint_type': 'n_complains'}, axis=1)
  
    def return_month(idx):
        """Returns month from calendar module corresponding the dt.month index"""
        return calendar.month_name[idx]
    # map int to month names
    noise_year['month'] = noise_year.month.apply(lambda x: return_month(x))

    # get y-data
    complaints_2019 = noise_year[noise_year.year.isin([2019])].n_complains.tolist()
    complaints_2020 = noise_year[noise_year.year.isin([2020])].n_complains.tolist()
    complaints_2021 = noise_year[noise_year.year.isin([2021])].n_complains.tolist()

    # create an instance of named tuple with the data
    return fig1_data(MONTHS, complaints_2019, complaints_2020, complaints_2021)


# FIGURE 2
def get_fig_two_data(data):
    """Return a namedTuple with data for figure two."""
    
    # Create a named tuple to store the data
    fig2_data = namedtuple('fig2', 'x y_2019 y_2020')

    # subset data 
    noise_borough = data[data.year.isin([2019, 2020])].groupby(['year', 'borough'])['complaint_type']\
                                                      .count()\
                                                      .reset_index()\
                                                      .rename({'complaint_type': 'n_complains'}, axis=1)
    # get borough names
    borough = [borough.capitalize() for borough in noise_borough.borough.unique()]

    # get y-data
    complaints_2019 = noise_borough[noise_borough.year.isin([2019])].n_complains
    complaints_2020 = noise_borough[noise_borough.year.isin([2020])].n_complains

    # create and return an instance of named tuple with the data
    return fig2_data(borough, complaints_2019, complaints_2020)


# FIGURE 3 
def get_fig_three_data(data):
    """Return a namedTuple with data for figure three."""
    
    # set up the named tuple
    fig3_data = namedtuple('fig3', 'x y_2019 y_2020')

    # group by noise type
    noise_type = data[data.year.isin([2019, 2020])].groupby(['complaint_type', 'year'])['agency']\
                                                    .count()\
                                                    .reset_index()\
                                                    .rename({'agency': 'n_complains'}, axis=1)

    # # get the top 3 major sources in 2020
    top3_noise_type_2020 = noise_type[noise_type.year.isin([2020])].sort_values('n_complains', ascending=False)\
                                                                   .complaint_type[:3]

    # get the top 3 noise complaints
    top_noise_complaints = noise_type[noise_type.complaint_type.isin(top3_noise_type_2020)]

    # get the x
    complaint_type = top_noise_complaints.complaint_type.unique()

    # get the y 
    complaints_2019 = top_noise_complaints[top_noise_complaints.year.isin([2019])].n_complains
    complaints_2020 = top_noise_complaints[top_noise_complaints.year.isin([2020])].n_complains

    return fig3_data(complaint_type, complaints_2019, complaints_2020)

# FIGURE 4 
def get_fig_four_data(data):
    """Return a namedTuple with data for figure four."""

    # set up the named tuple
    namedTuple = namedtuple('weekday', ['y', 'x'])
    
    # subset data
    daily_noise = data[data.year.isin([2020])].groupby(['weekday', 'complaint_type'])['agency']\
                                                .count()\
                                                .reset_index()\
                                                .rename({'agency': 'n_complaints'}, axis=1)

    # discard Collection Truck Noise because number is negligable (n<=2)
    daily_noise = daily_noise[~daily_noise.complaint_type.isin(['Collection Truck Noise'])]

    # get total complains per type to normalize each day
    total_daily_complaints = daily_noise.groupby(['weekday'])['n_complaints'].sum().to_list()

    # store results
    result = dict()

    for complaint_type in daily_noise.complaint_type.unique():

        name_complaint = complaint_type
        
        # Get data for each weekday
        weekday = daily_noise[daily_noise.complaint_type.isin([complaint_type])].weekday.to_list()
        
        # Transform weekday index id to true name
        weekday_name = [calendar.day_name[i] for i in weekday]
        
        # Get a list with the number of complains normalized to total complains in each day
        number_complaints_norm = (daily_noise[daily_noise.complaint_type.isin([complaint_type])].n_complaints\
                            / total_daily_complaints * 100).apply(lambda x: round(x, 2)).to_list()
        
        # Add an instance of a named tuple with the data to a dict
        result[name_complaint] = namedTuple(weekday_name, number_complaints_norm)
    
    return result