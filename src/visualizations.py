import plotly.graph_objects as go
import json


def main():

    # create a bar chart displaying the comparision of male and females cases in the us.
    sex=['Male','Female']
    fig = go.Figure([go.Bar(x=sex, y=cases)])
    fig.show()

    # create a pie chart showing how COVID-19 deaths compares to pre-existing health conditions deaths.

    # create a scatter plot of the age groups that have contracted covid-19.

    pass

# import plotly.graph_objects as go 
# label_list = ['240213',  ]
# value_list = [100, 200]
# fig = go.Figure(data=[go.Pie(labels=label_list, values=value_list)])
# fig.show()
if __name__ == '__main__':
    main()
