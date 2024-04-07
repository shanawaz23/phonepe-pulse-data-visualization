import streamlit as st 
from streamlit_option_menu import option_menu 
import psycopg2
import pandas as pd 
import plotly.express as px  
import requests
import json

#dataframe creation 

#sql connection
mydb=psycopg2.connect(host="localhost",
                    user="postgres",
                    password="nawaz.khan",
                    database="phonepe_data",
                    port="5432"
                    )
cursor=mydb.cursor()

#aggre_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1=cursor.fetchall()

Aggre_insurance=pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#aggre_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2=cursor.fetchall()

Aggre_transaction=pd.DataFrame(table2,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#aggre_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3=cursor.fetchall()

Aggre_user=pd.DataFrame(table3,columns=("States","Years","Quarter","Brands","Transaction_count","Percentage"))

#map_insurance_df
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4=cursor.fetchall()

Map_insurance=pd.DataFrame(table4,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

#map_transaction_df
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5=cursor.fetchall()

Map_transaction=pd.DataFrame(table5,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

#map_user_df
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()

Map_user=pd.DataFrame(table6,columns=("States","Years","Quarter","Districts","RegisteredUser","AppOpens"))

#top_insurance_df
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()

Top_insurance=pd.DataFrame(table7,columns=("States","Years","Quarter","pincodes","Transaction_count","Transaction_amount"))

#top_transaction_df
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8=cursor.fetchall()

Top_transaction=pd.DataFrame(table8,columns=("States","Years","Quarter","pincodes","Transaction_count","Transaction_amount"))

#top_user_df
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()

Top_user=pd.DataFrame(table9,columns=("States","Years","Quarter","pincodes","RegisteredUsers"))



def Transaction_amount_count_Y(df,year):               

    tacy=df[df["Years"] == year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()                                 
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount = px.bar(tacyg, x="Transaction_amount", y="States", title=f"{year} TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            orientation='h')
        fig_amount.update_layout(yaxis=dict(categoryorder='total ascending'))
        st.plotly_chart(fig_amount)
    with col2:

        fig_count = px.bar(tacyg, x="Transaction_count", y="States", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Mint, 
                        orientation='h')
        fig_count.update_layout(yaxis=dict(categoryorder='total ascending'))
        st.plotly_chart(fig_count)

    
    col1,col2=st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data_str = response.content.decode("utf-8")  # Decode the content
        states_name=[]
        data1 = json.loads(data_str)  # Load the decoded data
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="ylorbr",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].min()),
                                hover_name="States",title= f"{year} TRANSACTION AMOUNT",fitbounds="locations",
                                height= 650,width=600)
        fig_india_1.update_geos(visible=False)        
        st.plotly_chart(fig_india_1)           

    with col2:
        fig_india_2=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="ylorbr",
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].min()),
                                hover_name="States",title= f"{year} TRANSACTION COUNT",fitbounds="locations",
                                height= 650,width=600)
        fig_india_2.update_geos(visible=False)        
        st.plotly_chart(fig_india_2) 
    
    return tacy

def Transaction_amount_count_Y_Q(df,quarter):
    tacy=df[df["Quarter"] == quarter]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount = px.bar(tacyg, x="Transaction_amount", y="States", title=f"{quarter} QUATER TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,
                            orientation='h')
        fig_amount.update_layout(yaxis=dict(categoryorder='total ascending'))
        st.plotly_chart(fig_amount)
    with col2:

        fig_count = px.bar(tacyg, x="Transaction_count", y="States", title=f"{quarter} QUATER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Mint, 
                        orientation='h')
        fig_count.update_layout(yaxis=dict(categoryorder='total ascending'))
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data_str = response.content.decode("utf-8")  # Decode the content
        states_name=[]
        data1 = json.loads(data_str)  # Load the decoded data
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="ylorbr",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].min()),
                                hover_name="States",title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",fitbounds="locations",
                                height= 650,width=600)
        fig_india_1.update_geos(visible=False)        
        st.plotly_chart(fig_india_1)    
    with col2:      
        fig_india_2=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count",color_continuous_scale="ylorbr",
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].min()),
                                hover_name="States",title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",fitbounds="locations",
                                height= 650,width=600)
        fig_india_2.update_geos(visible=False)        
        st.plotly_chart(fig_india_2)  

    return tacy

def Aggregated_Tran_Transaction_type(df,state):

    tacy=df[df["States"] == state]
    tacy.reset_index(drop=True,inplace=True)


    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        fig_pie_1=px.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_amount",
                        width=600,title=f"{state.upper()} TRANSACTION AMOUNT", hole=0.5)
        st.plotly_chart(fig_pie_1)
    with col2:
        fig_pie_2=px.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_count",
                        width=600,title=f"{state.upper()} TRANSACTION COUNT", hole=0.5)
        st.plotly_chart(fig_pie_2)

#aggregated user analysis_1
def Aggre_user_plot_1(df,year):
    aguy=df[df["Years"]==year]
    aguy.reset_index(drop=True,inplace=True)

    aguyg=pd.DataFrame( aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyg,x="Brands", y="Transaction_count",title=f"BRANDS AND TRANSACTION COUNT {year}",
                    width=1000,color_discrete_sequence=px.colors.sequential.Redor_r,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

#Aggregated_user_analysis
def Aggre_user_plot_2(df,quarter):
    aguyq=df[df["Quarter"]==quarter]
    aguyq.reset_index(drop=True,inplace=True)


    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)
    fig_bar_1=px.bar(aguyqg,x="Brands", y="Transaction_count",title=f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.Redor_r,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq

#aggregated analysis 3 
def Aggre_user_plot_3(df,state):
    auyqs=df[df["States"] == state]
    auyqs.reset_index(drop=True,inplace=True)

    fig_line_1=px.line(auyqs,x="Brands",y="Transaction_count",hover_data="Percentage",
                    title=f"{state} BRANDS, TRANSACTION COUNT,PERCENTAGE",width=1000,markers=True)
    st.plotly_chart(fig_line_1)

def map_insure_plot_1(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(miysg, x= "Transaction_amount", y= "Districts",
                               height=600, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_1= px.bar(miysg, x= "Transaction_count", y= "Districts",
                               height= 600, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              color_discrete_sequence= px.colors.sequential.Mint)
        
        st.plotly_chart(fig_map_bar_1)

# map_user plot_1
def map_user_plot_1(df,year):
    muy=df[df["Years"]==year]
    muy.reset_index(drop=True,inplace=True)

    muyg=muy.groupby("States")[["RegisteredUser","AppOpens"]].sum()
    muyg.reset_index(inplace=True)
    fig_line_1=px.line(muyg,x="States",y=["RegisteredUser","AppOpens"],
                    title=f"{year} REGISTERED USER APPOPENS",width=1000,height=800,markers=True)

    fig_line_1.update_traces(fill='tozeroy',line_shape='spline')

    st.plotly_chart(fig_line_1)

    return muy

# map_user plot_1
def map_user_plot_2(df,quarter):
    muyq=df[df["Quarter"]==quarter]
    muyq.reset_index(drop=True,inplace=True)

    muyqg=muyq.groupby("States")[["RegisteredUser","AppOpens"]].sum()
    muyqg.reset_index(inplace=True)
    fig_line_1=px.line(muyqg,x="States",y=["RegisteredUser","AppOpens"],
                    title=f"{df['Years'].min()} YEARS {quarter} QUARTER REGISTER USER APPOPENS",width=1000,height=800,markers=True,
                    color_discrete_sequence=px.colors.sequential.Rainbow_r)

    fig_line_1.update_traces(fill='tozeroy',line_shape='spline')

    st.plotly_chart(fig_line_1)

    return muyq

def map_user_plot_3(df, state):
    muyqs= df[df["States"] == state]
    muyqs.reset_index(drop= True, inplace= True)
    muyqsg= muyqs.groupby("Districts")[["RegisteredUser", "AppOpens"]].sum()
    muyqsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_plot_1= px.bar(muyqsg, x= "RegisteredUser",y= "Districts",orientation="h",
                                    title= f"{state.upper()} REGISTERED USER",height=800,
                                    color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_user_plot_1)

    with col2:
        fig_map_user_plot_2= px.bar(muyqsg, x= "AppOpens", y= "Districts",orientation="h",
                                    title= f"{state.upper()} APPOPENS",height=800,
                                    color_discrete_sequence= px.colors.sequential.Mint)
        st.plotly_chart(fig_map_user_plot_2)

#top insurance plot 1
def Top_insurance_plot_1(df,state):
    tiy=df[df["States"]== state]
    tiy.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_top_insur_bar_1=px.bar(tiy, x="Quarter", y="Transaction_amount", hover_data="pincodes",
                                title="TRANSACTION AMOUNT",  height=650,width=600, color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_top_insur_bar_1)
    with col2:
        fig_top_insur_bar_2=px.bar(tiy, x="Quarter", y="Transaction_count", hover_data="pincodes",
                                title="TRANSACTION AMOUNT",  height=650,width=600, color_discrete_sequence=px.colors.sequential.Mint)
        st.plotly_chart(fig_top_insur_bar_2)

def top_user_plot_1(df,year):
    tuy=df[df["Years"]==year]
    tuy.reset_index(drop=True,inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)

    fig_top_plot_1=px.bar(tuyg,x= "States",y= "RegisteredUsers", color="Quarter",width=1000,height=800,
                        color_discrete_sequence=px.colors.sequential.Burgyl_r,hover_name="States",
                        title=f"{year} Registered users")
    st.plotly_chart(fig_top_plot_1)

    return tuy

#top user plot 2 
def top_user_plot_2(df,states):
    tuys=df[df["States"]==states]
    tuys.reset_index(drop=True,inplace=True)

    fig_top_plot_2=px.bar(tuys,x="Quarter", y="RegisteredUsers", title= "REGISTEREDUSERS,PINCODES,QUARTERS",
                        width=1000,height=800,color="RegisteredUsers",hover_data="pincodes",
                        color_continuous_scale=px.colors.sequential.matter)
    st.plotly_chart(fig_top_plot_2)

#sql connection
def option_chart_transaction_amount(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="nawaz.khan",
                        database="phonepe_data",
                        port="5432"
                        )
    cursor=mydb.cursor()

    #plot_1
    query1= f'''select states, SUM(transaction_amount) as transaction_amount
                from {table_name}
                group by states
                order by transaction_amount desc
                limit 10;'''
    
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("States","transaction_amount"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x="transaction_amount", y="States", title="TRANSACTION AMOUNT",hover_name="States",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600,
                                orientation='h')
        fig_amount.update_layout(yaxis=dict(categoryorder='total ascending'))
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''select states, SUM(transaction_amount) as transaction_amount
                from {table_name}
                group by states
                order by transaction_amount 
                limit 10;'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("States","transaction_amount"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="transaction_amount", y="States", title="TRANSACTION AMOUNT",hover_name="States",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600,
                                orientation='h')
        fig_amount_2.update_layout(yaxis=dict(categoryorder='total descending'))
        st.plotly_chart(fig_amount_2)

def avg_tran_amount(table_name):
    query3= f'''select states, avg(transaction_amount) as transaction_amount
                from {table_name}
                group by states
                order by transaction_amount;'''
    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("States","transaction_amount"))

    fig_amount_3 = px.bar(df_3, x="transaction_amount", y="States", title="TRANSACTION AMOUNT",hover_name="States",
                            color_discrete_sequence=px.colors.sequential.Redor_r,height=800,width=1000,
                            orientation='h')
    fig_amount_3.update_layout(yaxis=dict(categoryorder='total ascending'))
    st.plotly_chart(fig_amount_3)

#sql connection
def option_chart_transaction_count(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="nawaz.khan",
                        database="phonepe_data",
                        port="5432"
                        )
    cursor=mydb.cursor()

    #plot_1
    query1= f'''select states, SUM(transaction_count) as transaction_count
                from {table_name}
                group by states
                order by transaction_count desc
                limit 10;'''
    
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("States","transaction_count"))
    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x="transaction_count", y="States", title="TRANSACTION COUNT",hover_name="States",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600,
                                orientation='h')
        fig_amount.update_layout(yaxis=dict(categoryorder='total ascending'))
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''select states, SUM(transaction_count) as transaction_count
                from {table_name}
                group by states
                order by transaction_count 
                limit 10;'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("States","transaction_count"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="transaction_count", y="States", title="TRANSACTION COUNT",hover_name="States",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600,
                                orientation='h')
        fig_amount_2.update_layout(yaxis=dict(categoryorder='total descending'))
        st.plotly_chart(fig_amount_2)

def avg_tran_count(table_name):
    query3= f'''select states, avg(transaction_count) as transaction_count
                from {table_name}
                group by states
                order by transaction_count;'''
    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("States","transaction_count"))

    fig_amount_3 = px.bar(df_3, x="transaction_count", y="States", title="TRANSACTION COUNT",hover_name="States",
                            color_discrete_sequence=px.colors.sequential.Redor_r,height=800,width=1000,
                            orientation='h')
    fig_amount_3.update_layout(yaxis=dict(categoryorder='total ascending'))
    st.plotly_chart(fig_amount_3)
    

#sql connection
def option_chart_registered_user(table_name,state):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="nawaz.khan",
                        database="phonepe_data",
                        port="5432"
                        )
    cursor=mydb.cursor()

    #plot_1
    query1= f'''select districts,sum(registereduser) as registereduser
                    from {table_name}
                    where states='{state}'
                    group by districts 
                    order by registereduser desc
                    limit 10;'''
    
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("districts","registereduser"))
    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x="registereduser", y="districts", title="TOP 10 OF REGISTER USER",hover_name="districts",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600,
                                orientation='h')
        fig_amount.update_layout(yaxis=dict(categoryorder='total ascending'))
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''select districts,sum(registereduser) as registereduser
                    from {table_name}
                    where states='{state}'
                    group by districts 
                    order by registereduser 
                    limit 10'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("districts","registereduser"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="registereduser", y="districts", title="LAST 10 OF REGISTER USER",hover_name="districts",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600,
                                orientation='h')
        fig_amount_2.update_layout(yaxis=dict(categoryorder='total descending'))
        st.plotly_chart(fig_amount_2)

    #query_3
    query3= f'''select districts,avg(registereduser) as registereduser
                    from {table_name}
                    where states='{state}'
                    group by districts 
                    order by registereduser;'''
    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("districts","registereduser"))

    fig_amount_3 = px.bar(df_3, x="registereduser", y="districts", title="AVERAGE OF REGISTEREDUSER",hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Redor_r,height=800,width=1000,
                            orientation='h')
    fig_amount_3.update_layout(yaxis=dict(categoryorder='total ascending'))
    st.plotly_chart(fig_amount_3)

#sql connection
def option_chart_appopens(table_name,state):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="nawaz.khan",
                        database="phonepe_data",
                        port="5432"
                        )
    cursor=mydb.cursor()

    #plot_1
    query1= f'''select districts,sum(appopens) as appopens
                    from {table_name}
                    where states='{state}'
                    group by districts 
                    order by appopens desc
                    limit 10;'''
    
    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1,columns=("districts","appopens"))
    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x="appopens", y="districts", title="TOP 10 OF APPOPENS ",hover_name="districts",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600,
                                orientation='h')
        fig_amount.update_layout(yaxis=dict(categoryorder='total ascending'))
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''select districts,sum(appopens) as appopens
                    from {table_name}
                    where states='{state}'
                    group by districts 
                    order by appopens 
                    limit 10;'''
    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("districts","appopens"))
    with col2:
        fig_amount_2 = px.bar(df_2, x="appopens", y="districts", title="LAST 10 OF APPOPENS",hover_name="districts",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650,width=600,
                                orientation='h')
        fig_amount_2.update_layout(yaxis=dict(categoryorder='total descending'))
        st.plotly_chart(fig_amount_2)

    #query_3
    query3= f'''select districts,avg(appopens) as appopens
                    from {table_name}
                    where states='{state}'
                    group by districts 
                    order by appopens;'''
    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("districts","appopens"))

    fig_amount_3 = px.bar(df_3, x="appopens", y="districts", title="AVERAGE OF APPOPENS",hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Redor_r,height=800,width=1000,
                            orientation='h')
    fig_amount_3.update_layout(yaxis=dict(categoryorder='total ascending'))
    st.plotly_chart(fig_amount_3)


# streamlit part 

st.set_page_config(layout="wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")


    
select = option_menu(None , ["HOME", "DATA EXPLORATION", "TOP CHARTS"],
                     icons=['house','kanban','book'],
                     menu_icon="cast",default_index=0,
                     orientation='horizontal',                                    #this part suits further experimnet
                     styles={
                         "container":{"padding":"5!important","background-color":"#fa34xx"},
                         "icon":{"color":"orange","font-size":"25px"},
                         "nav-link":{"font-size":"16px","text-align":"left","margin":"0px","--hover-color":"#867"},
                         "nav-link-selected":{"background-color":"#02tt21"}
                        
                     })

if select =="HOME":
    pass

elif select == "DATA EXPLORATION":
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])
    
    with tab1:
        
        selected_methods = st.multiselect("Select the method", ["Insurance Analysis", "Transaction analysis", "User analysis"])

        if "Insurance Analysis" in selected_methods:
            col1,col2=st.columns(2)
            with col1:

            
                years=st.slider("select the year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            tac_Y=Transaction_amount_count_Y(Aggre_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                quaters=st.slider("select the Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y,quaters)

        elif "Transaction analysis" in selected_methods:
            col1,col2=st.columns(2)
            with col1:

            
                years=st.slider("select the year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_insurance["Years"].min())
            Aggre_tran_tac_Y=Transaction_amount_count_Y(Aggre_transaction,years)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states",Aggre_tran_tac_Y["States"].unique())

            Aggregated_Tran_Transaction_type(Aggre_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                quaters=st.slider("select the Quarter",Aggre_tran_tac_Y["Quarter"].min(),Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Aggre_tran_tac_Y,quaters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states_ty",Aggre_tran_tac_Y["States"].unique())

            Aggregated_Tran_Transaction_type(Aggre_tran_tac_Y_Q,states)

        elif "User analysis" in selected_methods:
            col1,col2=st.columns(2)
            with col1:

            
                years=st.slider("select the year",Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Y=Aggre_user_plot_1(Aggre_user,years)

            col1,col2=st.columns(2)
            with col1:
                
                quaters=st.slider("select the Quarter",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q=Aggre_user_plot_2(Aggre_user_Y,quaters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states",Aggre_user_Y_Q["States"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q,states)
            

    with tab2:
        method_map = st.multiselect("**Select the Analysis Method(MAP)**",["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])

        if "Map Insurance Analysis" in method_map:
            col1,col2= st.columns(2)
            with col1:
                years_m1= st.slider("**Select the Year_mi**", Map_insurance["Years"].min(), Map_insurance["Years"].max(),Map_insurance["Years"].min())

            df_map_insur_Y= Transaction_amount_count_Y(Map_insurance,years_m1)

            col1,col2= st.columns(2)
            with col1:
                state_m1= st.selectbox("Select the State_mi", df_map_insur_Y["States"].unique())

            map_insure_plot_1(df_map_insur_Y,state_m1)

            col1,col2=st.columns(2)
            with col1:
                quaters=st.slider("select the Quarter_mi",df_map_insur_Y["Quarter"].min(),df_map_insur_Y["Quarter"].max(),df_map_insur_Y["Quarter"].min())
            df_map_insur_Y_Q=Transaction_amount_count_Y_Q(df_map_insur_Y,quaters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states_ty",df_map_insur_Y_Q["States"].unique())

            map_insure_plot_1(df_map_insur_Y_Q,states)

        elif "Map Transaction Analysis" in method_map:
            col1,col2= st.columns(2)
            with col1:
                years_m1= st.slider("**Select the Year_mt**", Map_transaction["Years"].min(), Map_transaction["Years"].max(),Map_transaction["Years"].min())

            Map_tran_tac_Y= Transaction_amount_count_Y(Map_transaction,years_m1)

            col1,col2= st.columns(2)
            with col1:
                state_m1= st.selectbox("Select the State_mt", Map_tran_tac_Y["States"].unique())

            map_insure_plot_1(Map_tran_tac_Y,state_m1)

            col1,col2=st.columns(2)
            with col1:
                quaters=st.slider("select the Quarter_mt",Map_tran_tac_Y["Quarter"].min(),Map_tran_tac_Y["Quarter"].max(),Map_tran_tac_Y["Quarter"].min())
            Map_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Map_tran_tac_Y,quaters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states_mt",Map_tran_tac_Y_Q["States"].unique())

            map_insure_plot_1(Map_tran_tac_Y_Q,states)

        elif "Map User Analysis" in method_map:
            col1,col2= st.columns(2)
            with col1:
                year= st.slider("**Select the Year_mu**", Map_user["Years"].min(), Map_user["Years"].max(),Map_user["Years"].min())

            Map_user_Y= map_user_plot_1(Map_user,year)
            col1,col2=st.columns(2)
            
            with col1:
                quaters=st.slider("select the Quarter_mu",Map_user_Y["Quarter"].min(),Map_user_Y["Quarter"].max(),Map_user_Y["Quarter"].min())
            Map_user_Y_Q=map_user_plot_2(Map_user_Y,quaters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states_mus",Map_user_Y_Q["States"].unique())

            map_user_plot_3(Map_user_Y_Q,states)
             
    with tab3:
        method_top = st.multiselect("**Select the Analysis Method(TOP)**",["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])

        if "Top Insurance Analysis" in method_top:
            col1,col2= st.columns(2)
            with col1:
                years_t1= st.slider("**Select the Year_ti**", Top_insurance["Years"].min(), Top_insurance["Years"].max(),Top_insurance["Years"].min())
 
            df_top_insur_Y= Transaction_amount_count_Y(Top_insurance,years_t1)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states_ti",df_top_insur_Y["States"].unique())

            Top_insurance_plot_1(df_top_insur_Y,states)

        elif "Top Transaction Analysis" in method_top:
            col1,col2= st.columns(2)
            with col1:
                years_t1= st.slider("**Select the Year_tt**", Top_transaction["Years"].min(), Top_transaction["Years"].max(),Top_transaction["Years"].min())
 
            df_top_tran_Y= Transaction_amount_count_Y(Top_transaction,years_t1)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states_tt",df_top_tran_Y["States"].unique())

            Top_insurance_plot_1(df_top_tran_Y,states)

        elif "Top User Analysis" in method_top:
            col1,col2= st.columns(2)
            with col1:
                years_t1= st.slider("**Select the Year_tu**", Top_user["Years"].min(), Top_user["Years"].max(),Top_user["Years"].min())
            Top_user_Y=top_user_plot_1(Top_user,years_t1)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states_tu",Top_user_Y["States"].unique())

            top_user_plot_2(Top_user_Y,states)

elif select == "TOP CHARTS":
    question=st.selectbox("Select the option",["1.Highest and lowest Transaction amount of Aggregated Insurance",
                                               "2.Highest and lowest Transaction count of Aggregated transaction",
                                               "3.Average Transaction amount of Aggregated Insurance",
                                               "4.Highest and lowest Transaction amount of top Insurance",
                                               "5.Highest and lowest Transaction count of top transaction",
                                               "6.Average Transaction amount of top Insurance",
                                               "7.Highest and lowest Transaction amount of map Insurance",
                                               "8.Registered user of Map User",
                                               "9.App opens of Map User",
                                               "10.Registered user of Top User",
                                               ]) 
    if question    =="1.Highest and lowest Transaction amount of Aggregated Insurance":

        option_chart_transaction_amount("aggregated_insurance")
        
    elif question =="2.Highest and lowest Transaction count of Aggregated transaction":

        option_chart_transaction_count("aggregated_transaction")

    elif question =="3.Average Transaction amount of Aggregated Insurance":

        avg_tran_amount("aggregated_insurance")

    elif question =="4.Highest and lowest Transaction amount of top Insurance":

        option_chart_transaction_amount("top_insurance")

    elif question == "5.Highest and lowest Transaction count of top transaction":

        option_chart_transaction_count("top_transaction")

    elif question == "6.Average Transaction amount of top Insurance":

        avg_tran_amount("top_insurance")

    elif question == "7.Highest and lowest Transaction amount of map Insurance":

        option_chart_transaction_amount("map_insurance")

    elif question =="8.Registered user of Map User":
        states=st.selectbox("Choose the state",Map_user["States"].unique())

        option_chart_registered_user("map_user",states)

    elif question =="9.App opens of Map User":
        states=st.selectbox("Choose the state",Map_user["States"].unique())

        option_chart_appopens("map_user",states)



    






                     
