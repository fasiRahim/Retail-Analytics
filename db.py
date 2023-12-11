import streamlit as st
import plotly.express as px
import pandas as pd

st.header('Retail Sales Analytics Dashboard')
hide_st_style= '''
    <style>
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      header {visibility: hidden;}
      div.block-container{padding-top:1rem}
      button[title="View fullscreen"]{visibility: hidden;}
    </style>
'''
st.markdown(hide_st_style, unsafe_allow_html=True)

df=pd.read_csv('retails.csv', encoding='ISO-8859-1')





st.sidebar.image("retailanalytics.png", use_column_width=False)
st.sidebar.header('Dimensions: ')

# Years
year =st.sidebar.multiselect('Year',df['Year'].unique())
if not year:
    dfy=df.copy()
else:
    dfy = df[df['Year'].isin(year)]

# Quarters
qtr =st.sidebar.multiselect('Quarter',df['Quarter'].unique())
if not qtr:
    df1=dfy.copy()
else:
    df1 = dfy[dfy['Quarter'].isin(qtr)]

# Create for Gender
gender =st.sidebar.multiselect('Gender',df['Gender'].unique())
if not gender:
    df2=df1.copy()
else:
    df2 = df[df['Gender'].isin(gender)]
    
# Create for Category
category =st.sidebar.multiselect('Category',df['Category'].unique())
if not category:
    df3=df2.copy()
else:
    df3 = df2[df2['Category'].isin(category)]


mtb1, mtb2 = st.tabs(["📈 Dashboard", "🗃 About"])

with mtb1:
    # Content Section
    col1,col2 = st.columns(2)

    # Sales by Gender
    gender_df = df2.groupby(by = ['Gender'],as_index=False)['Sales'].sum()
    gender_Data = df2.groupby(by = ['Year','Gender'],as_index=False)['Sales'].sum()
    gender_Data = pd.pivot_table(data=gender_Data,values='Sales',
                                            index='Year',columns='Gender')
    with col1:
        with st.expander('Gender wise Sales'):
            # col1.subheader('Gender wise Sales')
            tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
            fig=px.pie(gender_df,values='Sales',names='Gender',hole=0.5)
            fig.update_traces(text=gender_df['Gender'],textposition='inside',showlegend=False)
            tab1.plotly_chart(fig,use_container_width=True,height=100)

            tab2.write(gender_Data)

    # Sales by Categrory
    category_df = df3.groupby(by = ['Category'],as_index=False)['Sales'].sum()
    category_Data=df3.groupby(by = ['Year','Category'],as_index=False)['Sales'].sum()
    category_Data = pd.pivot_table(data=category_Data,values='Sales',
                                            index='Category',columns='Year')
    with col2:
        with st.expander('Category wise Sales'):
            tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
            fig=px.pie(category_df,values='Sales',names='Category',hole=0.5)
            fig.update_traces(text=category_df['Category'],textposition='inside',showlegend=False)
            tab1.plotly_chart(fig,use_container_width=True,height=100)
            tab2.write(category_Data)

    with st.expander('Sales by Age Group'):
        sales_by_age_list=dfy.groupby(
            by=['Year','Age_Group'],as_index=False)['Sales'].sum()
        sales_by_age_chart =sales_by_age_list.groupby(by='Age_Group',as_index=False)['Sales'].sum()
        sales_by_age_list = pd.pivot_table(data=sales_by_age_list,values='Sales',
                                            index='Year',columns='Age_Group')
        
        tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])

        fig=px.bar(sales_by_age_chart,x='Age_Group',y='Sales',text=['${:,.2f}'.format(x) for x in sales_by_age_chart['Sales']],
                template='seaborn')
        tab1.plotly_chart(fig,use_container_width=True,height=100)
        tab2.write(sales_by_age_list)
            
    # SALES BY YEAR
    st.subheader('Period Wise Sales')
    tbYear, tbQuarter,tbMonths,tbDays = st.tabs(["Year", "Quarter","Months","Days"])

    sales_by_year = dfy.groupby(by = ['Year'],as_index=False)['Sales'].sum()
    tbYear.write(sales_by_year)

    # SALES BY QUARTER
    if qtr and gender:
        sales_by_quarter_list=df1[df1['Gender'].isin(gender) & df1['Quarter'].isin(qtr)].groupby(
            by=['Year','Gender','Quarter'],as_index=False)['Sales'].sum()
        sales_by_month_list = df1[df1['Gender'].isin(gender) & df1['Quarter'].isin(qtr)].groupby(
            by=['Year','Quarter','Month'],as_index=False)['Sales'].sum()
        sales_by_days_list = df1[df1['Gender'].isin(gender) & df1['Quarter'].isin(qtr)].groupby(
            by=['Year','Day'],as_index=False)['Sales'].sum()
    elif year and gender:
        sales_by_quarter_list=dfy[dfy['Gender'].isin(gender)].groupby(
            by=['Year','Gender','Quarter'],as_index=False)['Sales'].sum()
        sales_by_month_list=dfy[dfy['Gender'].isin(gender)].groupby(
            by=['Year','Month'],as_index=False)['Sales'].sum()
        sales_by_days_list=dfy[dfy['Gender'].isin(gender)].groupby(
            by=['Year','Day'],as_index=False)['Sales'].sum()
    elif gender:
        sales_by_quarter_list=dfy[dfy['Gender'].isin(gender)].groupby(
            by=['Gender','Quarter'],as_index=False)['Sales'].sum()
        sales_by_month_list=dfy[dfy['Gender'].isin(gender)].groupby(
            by=['Gender','Month'],as_index=False)['Sales'].sum()
        sales_by_days_list=dfy[dfy['Gender'].isin(gender)].groupby(
            by=['Year','Gender','Day'],as_index=False)['Sales'].sum()
    elif qtr:
        sales_by_quarter_list=dfy[dfy['Quarter'].isin(qtr)].groupby(
            by=['Year','Quarter'],as_index=False)['Sales'].sum()
        sales_by_month_list=dfy[dfy['Quarter'].isin(qtr)].groupby(
            by=['Year','Month'],as_index=False)['Sales'].sum()
        sales_by_days_list=dfy[dfy['Quarter'].isin(qtr)].groupby(
            by=['Year','Day'],as_index=False)['Sales'].sum()
    else:
        sales_by_quarter_list=dfy.groupby(
            by=['Year','Quarter'],as_index=False)['Sales'].sum()
        sales_by_month_list = dfy.groupby(
            by=['Year','Month'],as_index=False)['Sales'].sum()
        sales_by_days_list = dfy.groupby(
            by=['Year','Day'],as_index=False)['Sales'].sum()

    # Sales Graph and Data by Quarter
    Quarter_bc = sales_by_quarter_list.groupby(by='Quarter',as_index=False)['Sales'].sum()
    sales_by_quarter_list = pd.pivot_table(data=sales_by_quarter_list,values='Sales',
                                            index='Year',columns='Quarter')
    figQ=px.bar(Quarter_bc,x='Quarter',y='Sales',text=['${:,.2f}'.format(x) for x in Quarter_bc['Sales']],
                template='seaborn')
    with tbQuarter:
        with st.expander('Graph'):
            st.plotly_chart(figQ,use_container_width=True,height=100)
        with st.expander('Data'):
            st.write(sales_by_quarter_list)


    # Sales Graph and Data by Month
    Month_bc = sales_by_month_list.groupby(by='Month',as_index=False)['Sales'].sum()
    sales_by_month_list = pd.pivot_table(data=sales_by_month_list,values='Sales',
                                            index='Year',columns='Month')

    figM=px.bar(Month_bc,x='Month',y='Sales',text=['${:,.2f}'.format(x) for x in Month_bc['Sales']],
                template='seaborn')
    figM.update_xaxes(categoryorder='array', categoryarray= ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug','Sep','Oct','Nov','Dec'])

    with tbMonths:
        with st.expander('Graph'):
            st.plotly_chart(figM,use_container_width=True,height=100)
        with st.expander('Data'):
            st.write(sales_by_month_list)


    # Sales Graph and Data by Days
    Days_bc = sales_by_days_list.groupby(by='Day',as_index=False)['Sales'].sum()
    sales_by_days_list = pd.pivot_table(data=sales_by_days_list,values='Sales',
                                            index='Year',columns='Day')
    figD=px.bar(Days_bc,x='Day',y='Sales',text=['${:,.2f}'.format(x) for x in Days_bc['Sales']],
                template='seaborn')
    figD.update_xaxes(categoryorder='array', categoryarray= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    with tbDays:
        with st.expander('Graph'):
            st.plotly_chart(figD,use_container_width=True,height=100)
        with st.expander('Data'):
            st.write(sales_by_days_list)

with mtb2:
    st.write('Project Introduction will come here')

