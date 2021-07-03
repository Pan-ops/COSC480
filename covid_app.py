import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests
import plotly.express as px

#get the coronavirus information for the website worldometers
@st.cache
def get_current_covid_data():
    url = 'https://www.worldometers.info/coronavirus/'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')
    content = soup.find_all('div', class_='maincounter-number')
    covid_stat = []
    for number in content:
        covid_stat.append(number.text.replace('\n', '').strip())
    return covid_stat

#get current US covid data
@st.cache
def get_current_US_covid_data():
    url = 'https://www.worldometers.info/coronavirus/country/us/'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')
    content = soup.find_all('div', class_='maincounter-number')
    covid_stat = []
    for number in content:
        covid_stat.append(number.text.replace('\n', '').strip())
    return covid_stat

#get current NZ covid data
@st.cache
def get_current_NZ_covid_data():
    url = 'https://www.worldometers.info/coronavirus/country/new-zealand/'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')
    content =  soup.find_all('div', class_='maincounter-number')
    covid_stat = []
    for number in content:
        covid_stat.append(number.text.replace('\n', '').strip())
    return covid_stat

#get current China covid data
@st.cache
def get_current_CN_covid_data():
    url = 'https://www.worldometers.info/coronavirus/country/china/'
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')
    content = soup.find_all('div', class_='maincounter-number')
    covid_stat = []
    for number in content:
        covid_stat.append(number.text.replace('\n', '').strip())
    return covid_stat

NZ_current = get_current_NZ_covid_data()
CN_curent = get_current_CN_covid_data()
US_current = get_current_US_covid_data()
covid_current_stats = get_current_covid_data()
current_dict = {'New Zealand': NZ_current,
                'China': CN_curent,
                'United States': US_current}

#display the current covid data for selected country
def display_country_current_data(country):
    covid_current_stats = current_dict[country]
    col1, col2, col3 = st.beta_columns(3)
    col1.subheader('Coronavirus Cases')
    col1.write(f'''
    {covid_current_stats[0]} ''')
    col2.subheader('Deaths')
    col2.write(f'''
    {covid_current_stats[1]} ''')
    col3.subheader('Recovered')
    col3.write(f'''
    {covid_current_stats[1]} ''')


# display the currrent world covid-19 statistics
st.markdown('''
CURRENT COVID-19 CORONAVIRUS PANDENMIC WORLD STATISTICS''')
col1, col2, col3 = st.beta_columns(3)
col1.subheader('Coronavirus Cases')
col1.write(f'''
{covid_current_stats[0]} ''')
col2.subheader('Deaths')
col2.write(f'''
{covid_current_stats[1]} ''')
col3.subheader('Recovered')
col3.write(f'''
{covid_current_stats[1]} ''')



st.title('Covid-19 and Country Economy')
st.subheader('Data analysis for China, New Zealand and United States')

#plotiting the stock idexs

#plt.style.use('seaborn')
# reading in the data from previously processed

index_df = pd.read_csv('https://raw.githubusercontent.com/Pan-ops/COSC480/main/all_index.csv', index_col=0, parse_dates=True)
covid_df = pd.read_csv('https://raw.githubusercontent.com/Pan-ops/COSC480/main/covid_nz_china_us_data.csv', index_col=1, parse_dates=True)
emp_df = pd.read_csv('https://raw.githubusercontent.com/Pan-ops/COSC480/main/employment_data.csv', index_col=0)

# creating country selector
option = st.selectbox('Select following options for analysis',['Stock_Index', "Covid-19_Data","Employment Rate","Current Data"])

#plot individual country's index
def plot_index(country):
    country_grp = index_df.groupby(['location'])
    df = country_grp.get_group(country)['close']
    fig = px.line(df, title= f'{country} Stock Index')
    return st.plotly_chart(fig, use_container_width=True)

#functions for data normalization
def normalize_data(data):
    data = (data - data.min()) / (data.max() - data.min())
    return data

def plot_normalized_index():
    country_grp = index_df.groupby(['location'])
    countries = ["China", 'New Zealand',"United States"]
    df = dict()
    for country in countries:
        df[country] = normalize_data(country_grp.get_group(country)['close'])
    df = pd.DataFrame(df)
    fig = px.line(df)
    return st.plotly_chart(fig, use_container_width=True)

def show_close_index_table(country):
    country_grp = index_df.groupby(['location'])
    if st.button('Show Index Tables'):
        st.header('Table of stock index data')
        st.dataframe(country_grp.get_group(country))
        st.button('Close Index Table')


def plot_employment_rate():
    fig = px.bar(emp_df, barmode='group', labels={'index' : 'Country', 'value':'Employment Rate (%)', 'variable':'Year'})
    return st.plotly_chart(fig, use_container_width=True)

def plot_covid_data(country, data_options):
    country_grp = covid_df.groupby(["location"])
    df = dict()
    for data in data_options:
        df[data] = country_grp.get_group(country)[data]
    df = pd.DataFrame(df)
    fig = px.line(df, title = f'{country} Covid-19 Data', labels={'value':'Number of People'})
    return st.plotly_chart(fig, use_container_width=True)

def show_close_covid_table(country):
    country_grp = covid_df.groupby(["location"])
    if st.button('Show Covid Data Tables'):
        st.header('Table of Covid data')
        st.dataframe(country_grp.get_group(country))
        st.button('Close Covid Data Table')

def display_current_covid_data_table():
    df = pd.DataFrame(current_dict, index = ['Total Cases','Total Deaths','Recovered'])
    return st.dataframe(df)



def display_plot_base_on_option(option):
    if option == 'Stock_Index':
        st.header('Stock Index Data')
        col1, col2 = st.beta_columns(2)
        country = col1.radio('Country', ['New Zealand', 'China', "United States"])
        all_index = col2.checkbox('Normalized Index for Comparison')
        if all_index:
            plot_normalized_index()
        plot_index(country)
        show_close_index_table(country)
    elif option == 'Covid-19_Data':
        st.header('Covid-19 Data')
        col1, col2 = st.beta_columns(2)
        country = col1.radio('Country', ['New Zealand', 'China', "United States"])
        data_options = col2.multiselect('Data', ['total_cases', "total_deaths"], 'total_cases')
        plot_covid_data(country, data_options)
        display_country_current_data(country)
        show_close_covid_table(country)
    elif option == 'Employment Rate':
        plot_employment_rate()
    elif option == 'Current Data':
        display_current_covid_data_table()


display_plot_base_on_option(option)
