import plotly.graph_objects
# import plotly.express as px
# import json


def main():

#     # create a bar chart displaying the comparision of male and females cases in the us.

#     # create a pie chart showing how COVID-19 deaths compares to pre-existing health conditions deaths.

#     # create a scatter plot of the age groups that have contracted covid-19.

#     pass

# import plotly.graph_objects as go 
# death_causes_list = ['COVID19_Deaths', 'Pneumonia_Deaths', 'Influenza_Deaths']
# amount_list = [240213, 242296, 6829]
# fig = go.Figure(data=[go.Pie(labels=death_causes_list, values=amount_list)])
# fig.show()

# import plotly.express as px
# age_group = ('Under 1 year', '0-17 years', '1-4 years', '5-14 years', '15-24 years', '18-29 years', '25-34 years', '30-49 years', '35-44 years', '45-54 years', '50-64 years', '55-64 years', '65-74 years', '75-84 years', '85 years and over')
# Covid19_Deaths = 

# if __name__ == '__main__':
#     main()

    # create a bar chart displaying the comparision of male and females cases in the us.
    sex =['Male','Female']
    us_cases = [130005, 110202] #insert data from table
    fig = go.Figure(data=[go.Bar(x=sex, y=us_cases)])
    fig.show()

    # create a pie chart showing how COVID-19 deaths compares to pre-existing health conditions deaths.
    death_causes_list = ['COVID19_Deaths', 'Pneumonia_Deaths', 'Influenza_Deaths']
    amount_list = [240213, 242296, 6829]
    fig = go.Figure(data=[go.Pie(labels=death_causes_list, values=amount_list)])
    fig.show()

    # create a scatter plot of the age groups that have contracted covid-19.
    #covid_ages = []




if __name__ == '__main__':
    main()

