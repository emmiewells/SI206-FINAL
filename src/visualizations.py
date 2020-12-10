import plotly.graph_objects as go
import sqlite3

def main():

    # create a bar chart displaying the comparision of male and females deaths in the us.
    sex =['Male','Female']
    us_cases = [141640, 119883] #insert data from table
    colors = ['GreenYellow', 'MediumOrchid']
    fig = go.Figure(data=[go.Bar(x=sex, y=us_cases, marker_color=colors)])
    fig.show()

    # create a pie chart showing how COVID-19 deaths compares to pre-existing health conditions deaths.
    death_causes_list = ['COVID19_Deaths', 'Pneumonia_Deaths', 'Influenza_Deaths']
    amount_list = [261530, 257672, 6868]
    colors = ['light blue', 'yellow', 'DarkOrange']
    fig = go.Figure(data=[go.Pie(labels=death_causes_list, values=amount_list)]) #change colors
    fig.update_traces(hoverinfo='value', textinfo='label+percent', textfont_size=30,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.show()

    #create bubble chart for US states correlation to cases/deaths?
    conn=sqlite3.connect('covid.db')
    c= conn.cursor()
    query='SELECT State, Deaths FROM States'
    c.execute(query)
    x= c.fetchall()
    print(x)
    states = [i[0] for i in x]
    deaths = [i[1] for i in x]
    markers = [i for i in range(50,0,-1)]
    print(states)
    fig = go.Figure(data=[go.Scatter(
        x=[state for state in states], y =[death for death in deaths], 
        mode='markers',
        marker_size=[marker for marker in markers])
    ])
        
    fig.show() 


    
    
    #calculations-create a scatter plot of the age groups that have contracted covid-19 in the us.





    #covid_ages = []
    #new calculations graph
    #percentage of women died of covid vs men
    #deadliest age group

    #for all sexes, how many die of covid,influenza, pneumonia
    #women, how many die of covid,influenza, pneumonia
    #men, how many die of covid,influenza, pneumonia
    #bar plot for all sexes showing covid deaths for each age group, heigh of bar is coivd 19 deaths

    #us state table, which state was the deadliest for men, for women
    #which sex is most likely to die in __ state 

    #countries gender table, highest death for men vs women 

if __name__ == '__main__':
    main()
