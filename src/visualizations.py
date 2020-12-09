import plotly.graph_objects as go
import json


def main():

    # create a bar chart displaying the comparision of male and females cases in the us.
    sex=['Male','Female']
    fig = go.Figure([go.Bar(x=sex, y=cases)])
    fig.show()

    # create a pie chart showing how COVID-19 deaths compares to pre-existing health conditions deaths.
    death_causes_list = ['COVID19_Deaths', 'Pneumonia_Deaths', 'Influenza_Deaths']
    amount_list = [240213, 242296, 6829]
    fig = go.Figure(data=[go.Pie(labels=death_causes_list, values=amount_list)])
    fig.show()

    # create a scatter plot of the age groups that have contracted covid-19.



if __name__ == '__main__':
    main()
