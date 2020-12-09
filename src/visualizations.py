import plotly.graph_objects as go
import json


def main():

    # create a bar chart displaying the comparision of male and females cases in the us.
    sex =['Male','Female']
    us_cases = [130005, 110202] #insert data from table
    fig = go.Figure(data=[go.Bar(x=sex, y=us_cases)])
    fig.show()

    # create a pie chart showing how COVID-19 deaths compares to pre-existing health conditions deaths.
    death_causes_list = ['COVID19_Deaths', 'Pneumonia_Deaths', 'Influenza_Deaths']
    amount_list = [240213, 242296, 6829]
    fig = go.Figure(data=[go.Pie(labels=death_causes_list, values=amount_list)]) #change colors
    fig.show()

    # create a scatter plot of the age groups that have contracted covid-19 in the us .
    #covid_ages = []




if __name__ == '__main__':
    main()
