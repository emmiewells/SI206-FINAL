import plotly.graph_objects as go
import sqlite3

def main():
    """this will generate visualizations of the data we fetched from the database
    """

    # create a bar chart displaying the comparision of male and females deaths in the us.
    sex =['Male','Female']
    us_cases = [141640, 119883] #insert data from table
    colors = ['GreenYellow', 'MediumOrchid']
    fig = go.Figure(data=[go.Bar(x=sex, y=us_cases, marker_color=colors)])
    title_str = "Male and Female COVID-19 Cases in the US"
    fig.update_layout(title = title_str)
    fig.show()

    # create a pie chart showing how COVID-19 deaths compares to pre-existing health conditions deaths.
    death_causes_list = ['COVID19_Deaths', 'Pneumonia_Deaths', 'Influenza_Deaths']
    amount_list = [261530, 257672, 6868]
    colors = ['DarkOrange', 'yellow', 'DeepPink']
    fig = go.Figure(data=[go.Pie(labels=death_causes_list, values=amount_list)]) #change colors
    title_str = "Pre-existing health conditions and COVID-19 Deaths"
    fig.update_traces(hoverinfo='value', textinfo='label+percent', textfont_size=30,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.update_layout(title = title_str)
    fig.show()

    # create bubble chart for US states correlation to deaths
    conn=sqlite3.connect('covid.db')
    c= conn.cursor()
    query='SELECT State, Deaths FROM States'
    c.execute(query)
    x= c.fetchall()
    # print(x)
    states = [i[0] for i in x]
    deaths = [i[1] for i in x]
    markers = [i for i in range(56,0,-1)]
    # print(states)
    fig = go.Figure(data=[go.Scatter(
        x=[state for state in states], y =[death for death in deaths], 
        mode='markers',
        marker_size=[marker for marker in markers])
    ])
    title_str = "Covid-19 Deaths by US State"
    fig.update_layout(title = title_str)
    fig.show() 
    
    # bubble chart showing global COVID data by country
    query = 'SELECT Country, TotalDeaths FROM Countries'
    c.execute(query)
    x = c.fetchall()
    # print(x)
    countries = [i[0] for i in x]
    deaths = [i[1] for i in x]
    markers = [i for i in range(150, 0, -1)]
    # print(states)
    fig = go.Figure(data=[go.Scatter(
        x=countries, y=deaths,
        mode='markers',
        marker_size=[marker for marker in markers])
    ])
    title_str = "Global COVID-19 data by Country"
    fig.update_layout(title = title_str)
    fig.show()

    #calculations-create a line chart plot of the age groups that have contracted covid-19 in the us:
    #y amount of deaths, x age groups and then two lines displaying sex

    query = '''SELECT AgeGroup, FemaleDeaths, MaleDeaths FROM CountriesAgeSex WHERE Country = 'Mexico';'''
    c.execute(query)

    data = c.fetchall()
    age_groups = [i[0] for i in data]
    female_deaths = [i[1] for i in data]
    male_deaths = [i[2] for i in data]
    deaths = [i for i in range(10000)]
    
    fig = go.Figure(data=go.Scatter(x=age_groups,y=female_deaths))
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=age_groups, y=female_deaths, mode='lines'))
    fig.add_trace(go.Scatter(x=age_groups, y=male_deaths, mode='lines'))
    title_str ="Male and Female COVID-19 Deaths by Age for Mexico"
    fig.update_layout(title = title_str)
    # fig = px.line(x=age_groups, y)

    # fig.add_trace(data=go.Scatter(x=age_groups, y=male_deaths))
    fig.show()



    #Percentage by Deaths by Case per state, all sex and all ages (pie chart)
    #Make list of COVID-19 deaths where the sex is all sexes/all ages and add up those states to get 100

    query = "SELECT COVID19Deaths, State FROM USAStateGender WHERE Sex = 'All Sexes'"
    c.execute(query)
    x = c.fetchall()
    #print(x)
    covid_deaths = [i[0] for i in x]
    #print(covid_deaths)
    deaths_sum = sum(covid_deaths)
    print(deaths_sum)
    us_states = [i[1] for i in x] 
    print(us_states)

    labels = us_states
    values = covid_deaths
    fig =go.Figure(data=[go.Pie(labels=labels, values=values)])
    title_str ="COVID-19 Deaths by State including all Sexes and Ages"
    fig.update_layout(title = title_str)
    fig.show()


if __name__ == '__main__':
    main()
