import git.repo
import pandas as pd
import json
import os
from git import Repo
import mysql.connector
import logging
from mysql.connector import Error
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


#import matplotlib.pyplot as plt
#import plotly.express as px

# Define repository URL and path
repo_url = "https://github.com/PhonePe/pulse"
path = 'C:\\Users\\CGC\\Desktop\\MPK\\DS - GUVI\\Capstone -2 Phonepe Pulse'  # Replace with the actual path to the cloned repo

# Set Git executable path
os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = r'C:\Program Files\Git\bin\git.exe'

# Cloning Git hub 

try:
    if not os.path.exists(path):
        Repo.clone_from(repo_url,path)
        print("Repository Succesfully cloned")
    else:
        repo = Repo(path)
        print("Repository already exists")

    if repo.bare:
        print("Repositoty is bare")
    else:
        print(repo.git.status())
        origin = repo.remotes.origin
        origin.pull()
        print("Repository successfully updated")
except git.CommandError as e:
    print(f"Error occured: {e}")



# Connect with MY SQL Database 
class Database():
    def __init__(self):
         self.host = "localhost"
         self.port = 3306
         self.user = "root"
         self.password = "Pravin@05"
         self.database = None 
    def connect(self):
         try:          
             self.connection = mysql.connector.connect(
                 host = self.host,
                 user = self.user,
                 password = self.password,
                 database = self.database,
                 port = self.port 
         )
             self.cursor = self.connection.cursor()
             print("Its Connected")
         except mysql.connector.Error as err:
             print(f"Issues in Connection{err}")

    def close(self):
         if self.connection:
             self.connection.close()
             print("Connection Closed")

    def create_schema(self, schema_name):
         try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {schema_name}")
            self.connection.database = schema_name  
            print(f"Database '{schema_name}' selected or created successfully.")
         except mysql.connector.Error as e:
            print(f"Error: '{e}'")
    def select_database(self, schema_name):
        try:
            self.database = schema_name
            self.connection.database = schema_name
            print(f"Database '{schema_name}' selected.")
        except mysql.connector.Error as e:
            print(f"Error: '{e}'")
     
db = Database()
db.connect()
# Create the 'phonepe' schema   
db.create_schema('phonepe')
# Select the database
db.select_database('phonepe')


# define a agg_ins insurance method to collect data from json
def agg_ins_df(pat={'State':[], 'Year':[],'Quarter':[], 'Pay_Category':[], 'Count':[], 'Total_value':[]}):
    agg_ins = r"C:\\Users\\CGC\\Desktop\\MPK\\DS - GUVI\\Capstone 1- Youtube Data Harvesting\\New St app\\Capstone -2 Phonepe Pulse\\pulse\\data\\aggregated\\insurance\\country\\india\\state"
    agg_ins_p = os.listdir(agg_ins) # Path integreated
    for state in agg_ins_p:
        state_path = os.path.join(agg_ins, state)
        #print(f"Accessing state directory {state_path}")

        if os.path.isdir(state_path):
            agg_insyr = os.listdir(state_path)

            for year in agg_insyr:
                yr_path = os.path.join(state_path, year)
                #print(f"Accessing year directory {yr_path}")

                if os.path.isdir(yr_path):
                    ins_list = os.listdir(yr_path)

                    for file_name in ins_list:
                        if file_name.endswith('.json'):  # Check for JSON files
                            file_path = os.path.join(yr_path, file_name)
                            #print(f"Accessing file path {file_path}")

                            if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
                                try:
                                    with open(file_path, 'r') as file:
                                        data = json.load(file)

                                        # Extract relevant data from JSON
                                        transaction_data = data.get('data', {}).get('transactionData', [])
                                        for item in transaction_data:
                                            name = item.get('name', 'N/A')
                                            for payment in item.get('paymentInstruments', []):
                                                count = payment.get('count', 0)
                                                amount = payment.get('amount', 0)
                                                quarter = file_name.replace('.json','')
                                                pat['State'].append(state) 
                                                pat['Year'].append(year)
                                                pat['Quarter'].append(quarter)
                                                pat['Pay_Category'].append(name)
                                                pat['Count'].append(count)
                                                pat['Total_value'].append(amount)
                                except json.JSONDecodeError as e:
                                    print(f"JSON decoding failed: {e}")
        #                     else:None
        #                         #print(f"File {file_path} is not readable or does not exist")
        #         else: None
        #             #print(f"Year directory {yr_path} does not exist")
        # else: None
        #     #print(f"State directory {state_path} does not exist")

    return pd.DataFrame(pat)


# Method for aggregated Transaction
def agg_trans_df(pat={'State':[], 'Year':[],'Quarter':[], 'Pay_Category':[], 'Count':[], 'Total_value':[]}):
    agg_trans = r"C:\\Users\\CGC\\Desktop\\MPK\\DS - GUVI\\Capstone 1- Youtube Data Harvesting\\New St app\\Capstone -2 Phonepe Pulse\\pulse\\data\\aggregated\\transaction\\country\\india\state"
    agg_trs_p = os.listdir(agg_trans)

    for state in agg_trs_p:
        state_p = os.path.join(agg_trans,state)
        #print(f"Accessing state directory {state_p}")
        if os.path.isdir(state_p):
            agg_trsyr = os.listdir(state_p)

            for year in agg_trsyr:
                yr_path = os.path.join(state_p,year)
                #print(f"Accessing year directory{yr_path}")
                if os.path.isdir(yr_path):
                    trs_list = os.listdir(yr_path)
                    
                    for file_name in trs_list:
                        if file_name.endswith('.json'):
                            file_path = os.path.join(yr_path,file_name)
                            #print(f"Accessing file directpory {file_path}")
                            
                            if os.path.isfile(file_path) and os.access(file_path,os.R_OK):
                                try:
                                    with open(file_path, 'r') as file:
                                        data = json.load(file)
                                        for dt in data['data']['transactionData']:
                                            name = dt['name']
                                            for payment in dt['paymentInstruments']:
                                                count = payment['count']
                                                amount = payment['amount']
                                                quarter = file_name.replace('.json','')
                                                pat['State'].append(state)
                                                pat['Year'].append(year)
                                                pat['Quarter'].append(quarter)
                                                pat['Pay_Category'].append(name)
                                                pat['Count'].append(count)
                                                pat['Total_value'].append(amount)
                                except json.JSONDecodeError as e:
                                    print(f"JSON Decoding failed{e}")
            #                 else:
            #                     None
            #                     #print(f"Filepath is not Valid {file_path}")
            #             else:
            #                 None
            #         else:
            #             None
            #     else:
            #         None
            #         #print("State Path is not valid")
            # else:
            #     None
            #     #print("Aggregated path is not valid")
    return pd.DataFrame(pat)

# Method for  Aggregate User Folder 
def agg_users_df(pat={'State':[], 'Year':[],'Quarter':[], 'Brand':[], 'Count':[],'percentage':[]}):
    agg_user = r"C:\\Users\\CGC\\Desktop\\MPK\\DS - GUVI\\Capstone 1- Youtube Data Harvesting\\New St app\\Capstone -2 Phonepe Pulse\\pulse\\data\\aggregated\\user\\country\\india\state"
    agg_user_p = os.listdir(agg_user)

    for state in agg_user_p:
        state_p = os.path.join(agg_user, state)
        #print(f"Accessing state directory {state_p}")
        if os.path.isdir(state_p):
            agg_useryr = os.listdir(state_p)

            for year in agg_useryr:
                yr_path = os.path.join(state_p, year)
                #print(f"Accessing year directory {yr_path}")
                if os.path.isdir(yr_path):
                    usrs_list = os.listdir(yr_path)
                    
                    for file_name in usrs_list:
                        if file_name.endswith('.json'):
                            file_path = os.path.join(yr_path, file_name)
                            #print(f"Accessing file directory {file_path}")
                            
                            if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
                                try:
                                    with open(file_path, 'r') as file:
                                        data = json.load(file)
                                        #print(f"Loaded data from {file_path}")
                                        if data and data.get('data') and data['data'].get('usersByDevice'):
                                             for dts in data['data']['usersByDevice']:
                                                  brand = dts.get('brand','')
                                                  count = dts.get('count',0)
                                                  percen = dts.get('percentage',0)
                                                  quarter = file_name.replace('.json', '')
                                                  pat['State'].append(state)
                                                  pat['Year'].append(year)
                                                  pat['Quarter'].append(quarter)
                                                  pat['Brand'].append(brand)
                                                  pat['Count'].append(count)
                                                  pat['percentage'].append(percen)
                                        # else:
                                        #     None
                                            #print(f"No data found in {file_path}")
                                except json.JSONDecodeError as e:
                                    print(f"JSON Decoding failed for {file_path}: {e}")
                                except Exception as e:
                                    print(f"Error processing file {file_path}: {e}")
                            #else:
                                #print(f"File path is not valid or not readable: {file_path}")
                        #else:
                            #print(f"Skipping non-JSON file: {file_name}")
                #else:
                    #print(f"Year directory is not valid: {yr_path}")
        #else:
            #print(f"State directory is not valid: {state_p}")

    return pd.DataFrame(pat)


# Method to call a Map Insurance data extraction
def map_ins_df(
        pat = {'State':[], 'Year':[], 'Quarter':[],'District':[],'Count':[],'Amount':[]}):
        path = r"C:\\Users\\CGC\\Desktop\\MPK\\DS - GUVI\\Capstone 1- Youtube Data Harvesting\\New St app\\Capstone -2 Phonepe Pulse\\pulse\\data\\map\\insurance\\hover\\country\\india\\state"
        map_ins = os.listdir(path)

        for state in map_ins:
            state_p = os.path.join(path,state)

            if os.path.isdir(state_p):
                for year in os.listdir(state_p):
                    map_yr = os.path.join(state_p,year)

                    if os.path.isdir(map_yr):
                        for file_name in os.listdir(map_yr):
                            if file_name.endswith('.json'):
                                file_pa = os.path.join(map_yr,file_name)
                                #print(f"Accessing file path: {file_pa}")


                                if os.path.isfile(file_pa) and os.access(file_pa, os.R_OK):
                                    try:
                                        with open(file_pa,'r') as fil:
                                            dt = json.load(fil)
                                            if 'data' in dt and dt.get('data') and dt['data'].get('hoverDataList', []):
                                                 for dts in dt['data']['hoverDataList']:
                                                      name = dts.get('name',None)
                                                      for metric in dts.get('metric',[]):
                                                           count = metric.get('count', None)
                                                           amount = metric.get('amount', None)  
                                                           quarter = quarter = file_name.replace('.json', '')                                                                                                     
                                                           pat['State'].append(state)
                                                           pat['Year'].append(year)
                                                           pat['Quarter'].append(quarter)
                                                           pat['District'].append(name)
                                                           pat['Count'].append(count)
                                                           pat['Amount'].append(amount)

                                    except json.JSONDecodeError as e:
                                         print(f"JSON Decoding failed for {file_pa}: {e}")
                                    except Exception as e:
                                         print(f"Error processing file {file_pa}: {e}")
            #                     else: 
            #                         print(f"File path is not valid or not readable: {file_pa}")
            #                 else: None                                
            #         else: 
            #             print(f"File path is not valid or not readable: {map_yr}")
            # else: 
            #     print(f"File path is not valid or not readable: {state_p}")


        return pd.DataFrame(pat)


# Method to call a Map transaction data extraction
def map_trs_df(
        pat = {'State':[], 'Year':[], 'Quarter':[],'District':[],'Count':[],'Amount':[]}):
        path = r"C:\\Users\\CGC\\Desktop\\MPK\\DS - GUVI\\Capstone 1- Youtube Data Harvesting\\New St app\\Capstone -2 Phonepe Pulse\\pulse\\data\\map\\transaction\\hover\\country\\india\\state"
        map_trans = os.listdir(path)

        for state in map_trans :
            state_p = os.path.join(path,state)

            if os.path.isdir(state_p):
                for year in os.listdir(state_p):
                    map_yr = os.path.join(state_p,year)

                    if os.path.isdir(map_yr):
                        for file_name in os.listdir(map_yr):
                            if file_name.endswith('.json'):
                                file_pah = os.path.join(map_yr,file_name)
                                #print(f"Accessing file path: {file_pah}")


                                if os.path.isfile(file_pah) and os.access(file_pah, os.R_OK):
                                    try:
                                        with open(file_pah,'r') as fil:
                                            dt = json.load(fil)
                                            if 'data' in dt and dt.get('data') and dt['data'].get('hoverDataList', []):
                                                 for dts in dt['data']['hoverDataList']:
                                                      name = dts.get('name',None)
                                                      for metric in dts.get('metric',[]):
                                                           count = metric.get('count', None)
                                                           amount = metric.get('amount', None)  
                                                           quarter = quarter = file_name.replace('.json', '')                                                                                                     
                                                           pat['State'].append(state)
                                                           pat['Year'].append(year)
                                                           pat['Quarter'].append(quarter)
                                                           pat['District'].append(name)
                                                           pat['Count'].append(count)
                                                           pat['Amount'].append(amount)

                                    except json.JSONDecodeError as e:
                                         print(f"JSON Decoding failed for {file_pah}: {e}")
                                    except Exception as e:
                                         print(f"Error processing file {file_pah}: {e}")
            #                     else: 
            #                         print(f"File path is not valid or not readable: {file_pah}")
            #         else: 
            #             print(f"File path is not valid or not readable: {map_yr}")
            # else: 
            #     print(f"File path is not valid or not readable: {state_p}")

        return pd.DataFrame(pat)


# Method to call a Map Users data extraction
def map_usrs_df(
        pat = {'State':[], 'Year':[], 'Quarter':[],'District':[],'registeredUsers':[],'appOpens':[]}):
        path = r"C:\\Users\\CGC\\Desktop\\MPK\\DS - GUVI\\Capstone 1- Youtube Data Harvesting\\New St app\\Capstone -2 Phonepe Pulse\\pulse\\data\\map\\user\\hover\\country\\india\\state"
        map_users = os.listdir(path)

        for state in map_users :
            state_p = os.path.join(path,state)

            if os.path.isdir(state_p):
                for year in os.listdir(state_p):
                    map_yr = os.path.join(state_p,year)

                    if os.path.isdir(map_yr):
                        for file_name in os.listdir(map_yr):
                            if file_name.endswith('.json'):
                                file_pah = os.path.join(map_yr,file_name)
                                #print(f"Accessing file path: {file_pah}")


                                if os.path.isfile(file_pah) and os.access(file_pah, os.R_OK):
                                    try:
                                        with open(file_pah,'r') as fil:
                                            dt = json.load(fil)
                                            if 'data' in dt and dt.get('data') and dt['data'].get('hoverData', {}):
                                                 for district,data  in dt['data']['hoverData'].items():
                                                      regusrs = data.get('registeredUsers', None)
                                                      appopens = data.get('appOpens', None)
                                                      quarter = quarter = file_name.replace('.json', '')
                                                      pat['State'].append(state)
                                                      pat['Year'].append(year)
                                                      pat['Quarter'].append(quarter)
                                                      pat['District'].append(district)
                                                      pat['registeredUsers'].append(regusrs)
                                                      pat['appOpens'].append(appopens)

                                    except json.JSONDecodeError as e:
                                         print(f"JSON Decoding failed for {file_pah}: {e}")
                                    except Exception as e:
                                         print(f"Error processing file {file_pah}: {e}")
            #                     else: 
            #                         print(f"File path is not valid or not readable: {file_pah}")
            #         else: 
            #             print(f"File path is not valid or not readable: {map_yr}")
            # else: 
            #     print(f"File path is not valid or not readable: {state_p}")

        return pd.DataFrame(pat)

def top_ins_df(pat = {'State':[], 'Year':[], 'Quarter':[], 'EntityType':[], 'EntityName':[], 'Count':[], 'Amount':[]}
               ):

    path = r"C:\\Users\\CGC\\Desktop\\MPK\\DS - GUVI\\Capstone 1- Youtube Data Harvesting\\New St app\\Capstone -2 Phonepe Pulse\\pulse\\data\\top\\insurance\\country\\india\\state"
    top_trans = os.listdir(path)

    for state in top_trans:
        state_p = os.path.join(path, state)

        if os.path.isdir(state_p):
            for year in os.listdir(state_p):
                map_yr = os.path.join(state_p, year)

                if os.path.isdir(map_yr):
                    for file_name in os.listdir(map_yr):
                        if file_name.endswith('.json'):
                            file_path = os.path.join(map_yr, file_name)
                            #print(f"Accessing file path: {file_path}")

                            if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
                                try:
                                    with open(file_path, 'r') as fil:
                                        dt = json.load(fil)
                                        quarter = file_name.replace('.json', '')

                                        if 'data' in dt and dt.get('data'):
                                            # Processing states
                                            statess = dt['data'].get('states', [])
                                            if statess is not None:
                                                 for state_data in statess:
                                                     entity_name = state_data.get('entityName', None)
                                                     metric = state_data.get('metric', {})
                                                     count = metric.get('count', None)
                                                     amount = metric.get('amount', None)

                                                     pat['State'].append(state)
                                                     pat['Year'].append(year)
                                                     pat['Quarter'].append(quarter)
                                                     pat['EntityType'].append('states')
                                                     pat['EntityName'].append(entity_name)
                                                     pat['Count'].append(count)
                                                     pat['Amount'].append(amount)
                                            # else:
                                            #     print(f"No 'states' data found in {file_path}")


                                            # Processing districts
                                            districts = dt['data'].get('districts', [])
                                            if districts is not None:
                                                for district_data in districts:
                                                    entity_name = district_data.get('entityName', None)
                                                    metric = district_data.get('metric', {})
                                                    count = metric.get('count', None)
                                                    amount = metric.get('amount', None)

                                                    pat['State'].append(state)
                                                    pat['Year'].append(year)
                                                    pat['Quarter'].append(quarter)
                                                    pat['EntityType'].append('District')
                                                    pat['EntityName'].append(entity_name)
                                                    pat['Count'].append(count)
                                                    pat['Amount'].append(amount)
                                            # else:
                                            #     print(f"No 'Districts' data found in {file_path}")


                                            # Processing pincodes
                                            pincodes = dt['data'].get('pincodes', [])
                                            if pincodes is not None:
                                                for pincode_data in pincodes:
                                                    entity_name = pincode_data.get('entityName', None)
                                                    metric = pincode_data.get('metric', {})
                                                    count = metric.get('count', None)
                                                    amount = metric.get('amount', None)

                                                    pat['State'].append(state)
                                                    pat['Year'].append(year)
                                                    pat['Quarter'].append(quarter)
                                                    pat['EntityType'].append('Pincode')
                                                    pat['EntityName'].append(entity_name)
                                                    pat['Count'].append(count)
                                                    pat['Amount'].append(amount)

                                except json.JSONDecodeError as e:
                                    print(f"JSON Decoding failed for {file_path}: {e}")
                                except Exception as e:
                                    print(f"Error processing file {file_path}: {e}")
        #                     else:
        #                         print(f"File path is not valid or not readable: {file_path}")
        #         else:
        #             print(f"File path is not valid or not readable: {map_yr}")
        # else:
        #     print(f"File path is not valid or not readable: {state_p}")

    return pd.DataFrame(pat)

# Method for top trans users
def top_trans_df(pat= {'State':[], 'Year':[], 'Quarter':[], 'EntityType':[], 'EntityName':[], 'Count':[], 'Amount':[]}):

    path = r"C:\\Users\\CGC\\Desktop\\MPK\\DS - GUVI\\Capstone 1- Youtube Data Harvesting\\New St app\\Capstone -2 Phonepe Pulse\\pulse\\data\\top\\transaction\\country\\india\\state"
    top_trans = os.listdir(path)

    for state in top_trans:
        state_p = os.path.join(path, state)

        if os.path.isdir(state_p):
            for year in os.listdir(state_p):
                map_yr = os.path.join(state_p, year)

                if os.path.isdir(map_yr):
                    for file_name in os.listdir(map_yr):
                        if file_name.endswith('.json'):
                            file_path = os.path.join(map_yr, file_name)
                            #print(f"Accessing file path: {file_path}")

                            if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
                                try:
                                    with open(file_path, 'r') as fil:
                                        dt = json.load(fil)
                                        quarter = file_name.replace('.json', '')

                                        if 'data' in dt and dt.get('data'):
                                            # Processing states
                                            statess = dt['data'].get('states', [])
                                            if statess is not None:
                                                 for state_data in statess:
                                                     entity_name = state_data.get('entityName', None)
                                                     metric = state_data.get('metric', {})
                                                     count = metric.get('count', None)
                                                     amount = metric.get('amount', None)

                                                     pat['State'].append(state)
                                                     pat['Year'].append(year)
                                                     pat['Quarter'].append(quarter)
                                                     pat['EntityType'].append('states')
                                                     pat['EntityName'].append(entity_name)
                                                     pat['Count'].append(count)
                                                     pat['Amount'].append(amount)
                                            # else: 
                                            #     print(f"No 'states' data found in {file_path}")


                                            # Processing districts
                                            districts = dt['data'].get('districts', [])
                                            if districts is not None:
                                                for district_data in districts:
                                                    entity_name = district_data.get('entityName', None)
                                                    metric = district_data.get('metric', {})
                                                    count = metric.get('count', None)
                                                    amount = metric.get('amount', None)

                                                    pat['State'].append(state)
                                                    pat['Year'].append(year)
                                                    pat['Quarter'].append(quarter)
                                                    pat['EntityType'].append('District')
                                                    pat['EntityName'].append(entity_name)
                                                    pat['Count'].append(count)
                                                    pat['Amount'].append(amount)
                                            # else: 
                                            #     print(f"No 'Districts' data found in {file_path}")


                                            # Processing pincodes
                                            pincodes = dt['data'].get('pincodes', [])
                                            if pincodes is not None:
                                                for pincode_data in pincodes:
                                                    entity_name = pincode_data.get('entityName', None)
                                                    metric = pincode_data.get('metric', {})
                                                    count = metric.get('count', None)
                                                    amount = metric.get('amount', None)

                                                    pat['State'].append(state)
                                                    pat['Year'].append(year)
                                                    pat['Quarter'].append(quarter)
                                                    pat['EntityType'].append('Pincode')
                                                    pat['EntityName'].append(entity_name)
                                                    pat['Count'].append(count)
                                                    pat['Amount'].append(amount)

                                except json.JSONDecodeError as e:
                                    print(f"JSON Decoding failed for {file_path}: {e}")
                                except Exception as e:
                                    print(f"Error processing file {file_path}: {e}")
        #                     else:
        #                         print(f"File path is not valid or not readable: {file_path}")
        #         else:
        #             print(f"File path is not valid or not readable: {map_yr}")
        # else:
        #     print(f"File path is not valid or not readable: {state_p}")

    return pd.DataFrame(pat)

# Method for top users
def top_user_df(
        pat = {'State':[], 'Year':[], 'Quarter':[], 'EntityType':[],'EntityName':[], 'registeredUsers':[]}
        ):

    path = r"C:\\Users\\CGC\\Desktop\\MPK\\DS - GUVI\\Capstone 1- Youtube Data Harvesting\\New St app\\Capstone -2 Phonepe Pulse\\pulse\\data\\top\\user\\country\\india\\state"
    top_users = os.listdir(path)

    for state in top_users:
        state_p = os.path.join(path, state)

        if os.path.isdir(state_p):
            for year in os.listdir(state_p):
                map_yr = os.path.join(state_p, year)

                if os.path.isdir(map_yr):
                    for file_name in os.listdir(map_yr):
                        if file_name.endswith('.json'):
                            file_path = os.path.join(map_yr, file_name)
                            #print(f"Accessing file path: {file_path}")

                            if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
                                try:
                                    with open(file_path, 'r') as fil:
                                        dt = json.load(fil)
                                        quarter = file_name.replace('.json', '')

                                        if 'data' in dt and dt.get('data'):
                                            # Processing states
                                            statess = dt['data'].get('states', [])
                                            if statess is not None:
                                                 for state_data in statess:
                                                     entity_name = state_data.get('name', None)
                                                     RegdUsers = state_data.get('registeredUsers', None)

                                                     pat['State'].append(state)
                                                     pat['Year'].append(year)
                                                     pat['Quarter'].append(quarter)
                                                     pat['EntityType'].append('states')
                                                     pat['EntityName'].append(entity_name)
                                                     pat['registeredUsers'].append(RegdUsers)
                                    
                                            # else: 
                                            #     print(f"No 'states' data found in {file_path}")


                                            # Processing districts
                                            districts = dt['data'].get('districts', [])
                                            if districts is not None:
                                                for district_data in districts:
                                                    entity_name = district_data.get('name', None)
                                                    RegdUsers = district_data.get('registeredUsers', None)

                                                    pat['State'].append(state)
                                                    pat['Year'].append(year)
                                                    pat['Quarter'].append(quarter)
                                                    pat['EntityType'].append('District')
                                                    pat['EntityName'].append(entity_name)
                                                    pat['registeredUsers'].append(RegdUsers)
                                            # else: 
                                            #    print(f"No 'Districts' data found in {file_path}")


                                            # Processing pincodes
                                            pincodes = dt['data'].get('pincodes', [])
                                            if pincodes is not None:
                                                for pincode_data in pincodes:
                                                    entity_name = pincode_data.get('name', None)
                                                    RegdUsers = pincode_data.get('registeredUsers', None)

                                                    pat['State'].append(state)
                                                    pat['Year'].append(year)
                                                    pat['Quarter'].append(quarter)
                                                    pat['EntityType'].append('Pincode')
                                                    pat['EntityName'].append(entity_name)
                                                    pat['registeredUsers'].append(RegdUsers)

                                except json.JSONDecodeError as e:
                                    print(f"JSON Decoding failed for {file_path}: {e}")
                                except Exception as e:
                                    print(f"Error processing file {file_path}: {e}")
        #                     else:
        #                         print(f"File path is not valid or not readable: {file_path}")
        #         else:
        #             print(f"File path is not valid or not readable: {map_yr}")
        # else:
        #     print(f"File path is not valid or not readable: {state_p}")

    return pd.DataFrame(pat)

def create_table(table_name, df):
    try:
        columns = ', '.join([f"`{col}` VARCHAR(255)" for col in df.columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns});"
        return create_table_query
    except Exception as e:
        logging.error(f"Error creating table schema for {table_name}: {str(e)}")
        raise  # Reraise the exception after logging


# Insert DataFrame into SQL table
def insert_table(table_name, df):
    try:
        cols = ', '.join([f"`{col}`" for col in df.columns])
        placeholders = ', '.join(['%s'] * len(df.columns))
        insert_query = f"INSERT INTO `{table_name}` ({cols}) VALUES ({placeholders})"
        
        values = df.values.tolist()
        db.cursor.executemany(insert_query, values)
        db.connection.commit()
    except mysql.connector.Error as e:
        db.connection.rollback()  # Rollback in case of a MySQL error
        logging.error(f"Error inserting data into {table_name}: {str(e)}")
        raise  # Reraise the exception after logging
    except Exception as e:
        logging.error(f"General error while inserting data into {table_name}: {str(e)}")
        raise


# Store a Tables into MY SQL
def collect_all_tables ():
    agg_ins_table = agg_ins_df()
    agg_trans_table = agg_trans_df()
    agg_user_table = agg_users_df()
    map_ins_table = map_ins_df()
    map_trans_table = map_trs_df()
    map_user_table = map_usrs_df()
    top_ins_table = top_ins_df()
    top_trans_table = top_trans_df()
    top_user_table = top_user_df()
    return {
        'agg_ins_table': agg_ins_table,
        'agg_trans_table': agg_trans_table,
        'agg_user_table': agg_user_table,
        'map_ins_table': map_ins_table,
        'map_trans_table': map_trans_table,
        'map_user_table': map_user_table,
        'top_ins_table': top_ins_table,
        'top_trans_table': top_trans_table,
        'top_user_table': top_user_table
    }

# Store to MySQL Database
def store_db_to_sql():
    tables = collect_all_tables()
    stored_tables = []
    for table_name, df in tables.items():
        try:    
            # Create table schema
            create_table_query = create_table(table_name, df)
            db.cursor.execute(create_table_query)
            db.connection.commit()
            # Insert data
            insert_table(table_name, df)
            db.connection.commit()
            
            stored_tables.append(table_name)
            st.write(f"{table_name} were stored Succesfully")

        except mysql.connector.Error as e:
            db.connection.rollback()
            logging.error(f"MySQL error storing {table_name}: {str(e)}")
            print(f"Error storing {table_name}: {e}")
        
        except Exception as e:
            db.connection.rollback()
            logging.error(f"General error storing {table_name}: {str(e)}")
            st.write(f"Error storing {table_name}: {e}")

    return stored_tables

# Streamlit Page
#"C:\Users\CGC\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts\streamlit.exe" run phonepe.py
def main():
    st.sidebar.header(':violet[Dashboard]')

    option=st.sidebar.radio('Click a below wish to explore',['Home','Data Warehousing','Data Visualaization' ,'FAQs'])

    with st.sidebar:
            st.write("------")

    if option =='Home':
        st.title(":violet[Phonepe Pulse Data Visualization and Exploration:]")
        st.markdown("A User-Friendly Tool Using Streamlit and Plotly")
        st.header(":violet[Technologies Covered :]")
        st.markdown("""
                    - Github Cloning,
                    - Python,
                    - MySQL,
                    - Streamlit,
                    - Plotly.""")
        st.divider()
        st.subheader("Inspired From")
        st.markdown("[PhonePe](https://www.phonepe.com/pulse/explore/transaction/2022/4/)")
        st.subheader("Results:")
        st.markdown("""Users will be able to access the dashboard from a web browser and easily navigate
                     the different visualizations and facts and figures displayed. The dashboard will
                     provide valuable insights and information about the data in the Phonepe pulse
                     Github repository, making it a valuable tool for data analysis and decision-making.
                     Overall, the result of this project will be a comprehensive and user-friendly solution
                     for extracting, transforming, and visualizing data from the Phonepe pulse Github
                     repository.""")
        
    if option == 'Data Extraction':
        st.header('***:blue[Store Data into the Database]***', divider='rainbow')
        st.markdown("Clicking the 'Store Data into MYSQL' button will store data into SQL.")

        if st.button("Store Data into MYSQL"):
            with st.spinner('Storing Data in the Database...'):
                try:
                    result_message = store_db_to_sql()
                    if result_message:
                        st.write(f"Tables were stored Sucessfully:")
                    else:
                        st.write("No tables were stored.")
                   # Assuming `result_message` is a list of table names that were processed
                    if isinstance(result_message, list) and result_message:
                        if len(result_message)> 0 :
                            st.success("Tables were Stored Succesfully")
                            st.write(result_message)
                        else:
                            st.warning("Data already exists.")
                    else:
                        st.warning("No data were stored.")

                except KeyError as e:
                    st.error(f"Key Error: {e}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        st.divider()

    if option == 'Data Visualaization':
        st.title(':violet[Select a Category to view the Visualization]')

        # Create columns for side-by-side layout
        col1, col2, col3 = st.columns([3, 1, 1])  # Adjust the ratio as needed

        with col1:
            category = st.selectbox("Select a Category", ["Aggregated", "Map", "Top"])

        with col2:
            payment_type = st.selectbox("Select a Payment", ['Insurance', 'Transaction', 'Users'])
        
        with col3:
            Year = st.selectbox("Select a Year", ['2020', '2021', '2022', '2023', '2024'])
        
        search = st.button("Search")
        st.markdown('-----')
        
        if search:
            if search and category == 'Aggregated' and payment_type == 'Insurance' and Year in ['2020', '2021', '2022', '2023', '2024']:
                st.subheader(f':violet[Aggregated Insurance in {Year}]')
            
                # Query and process data
                agg_insdf = pd.read_sql(f"SELECT * FROM agg_ins_table WHERE Year = {Year}", con=db.connection)
                agg_insdf['State'] = agg_insdf['State'].str.replace('-', ' ').str.title()
                agg_insdf[['Total_value', 'Count']] = agg_insdf[['Total_value', 'Count']].apply(pd.to_numeric, errors='coerce')

                # Aggregate and round data
                summary = agg_insdf.groupby('Pay_Category').agg(Total_Count=('Count', 'sum'), Total_value=('Total_value', 'sum')).reset_index()
                # Calculate the Average Value and round it to 2 decimal places
                summary['Average_value'] = (summary['Total_value'] / summary['Total_Count']).round(2)

                # Format the total value and total count in millions
                total_value = (summary['Total_value'].sum() / 1000000).round(2)
                total_counts = (summary['Total_Count'].sum() / 1000000).round(2)

                # Calculate average and format it
                average = (total_value / total_counts).round(2)

                # Display metrics
                cl1, cl2   = st.columns(2)
                # Display the total value, total counts, and average value in metric widgets
                cl1.metric(label="Total Value (in Millions)", value=f"{total_value:,.2f}M")
                cl2.metric(label="Total Counts (in Millions)", value=f"{total_counts:,.2f}M")
                st.metric(label="Average Value per Count", value=f"{average:,.2f}")


                # Choropleth map
                geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                color_scales = {'2020': 'Reds', '2021': 'Blues', '2022': 'Rainbow', '2023': 'Greens', '2024': 'Viridis'}

                try:
                    fig = px.choropleth_mapbox(
                        agg_insdf, geojson=geojson_url, featureidkey='properties.ST_NM', locations='State',
                        color='Total_value', hover_name='Count', hover_data=['Pay_Category'], mapbox_style='carto-positron',
                        opacity=1, zoom=3.5, center={"lat": 22.9734, "lon": 78.6569}, width=1200, height=800,
                        color_continuous_scale=color_scales[str(Year)],
                        range_color=(agg_insdf['Total_value'].quantile(0.05), agg_insdf['Total_value'].quantile(0.95)),
                        title='Geo Visualization: Total Value by State in Aggregated Insurance'
                    )
                    st.plotly_chart(fig)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

                # Pie chart
                st.plotly_chart(px.pie(agg_insdf, values='Total_value', names='Quarter', title='Pie Chart for Aggregated Insurance', template='plotly_dark'))

            # Aggregated  Transactions
            if search and category == 'Aggregated' and payment_type == 'Transaction' and Year in ['2020', '2021', '2022', '2023', '2024']:
                st.subheader(f':violet[Aggregated Transactions in {Year}]')

            # Fetch and process data
                agg_trans = pd.read_sql(f"SELECT * FROM agg_trans_table WHERE Year = {Year}", con=db.connection)
                agg_trans['State'] = agg_trans['State'].str.replace('-', ' ').str.title()
                agg_trans[['Total_value', 'Count']] = agg_trans[['Total_value', 'Count']].apply(pd.to_numeric, errors='coerce')
                agg_trans['Total_value_Mn'] = (agg_trans['Total_value'] / 1e6).round(2)

                # Aggregate data and calculate metrics
                describe = agg_trans.groupby('Pay_Category').agg(Total_Count=('Count', 'sum'), Total_value=('Total_value', 'sum')).reset_index()
                describe['Average_value'] = (describe['Total_value'] / describe['Total_Count']).round(2)

                # Format the total value and total count in millions
                total_value = (describe['Total_value'].sum() / 1000000).round(2)
                total_counts = (describe['Total_Count'].sum() / 1000000).round(2)

                # Calculate average and format it
                average = (total_value / total_counts).round(2)

                # Display metrics
                cl1, cl2   = st.columns(2)
                # Display the total value, total counts, and average value in metric widgets
                cl1.metric(label="Total Value (in Millions)", value=f"{total_value:,.2f}M")
                cl2.metric(label="Total Counts (in Millions)", value=f"{total_counts:,.2f}M")
                st.metric(label="Average Value per Count", value=f"{average:,.2f}")

                # Choropleth map
                geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                try:
                    st.plotly_chart(px.choropleth_mapbox(agg_trans, geojson=geojson_url, locations='State', featureidkey='properties.ST_NM', color='Count',
                                                        hover_name='Total_value_Mn', mapbox_style='carto-positron', zoom=3.5,
                                                        range_color=(agg_trans['Count'].quantile(0.40), agg_trans['Count'].quantile(0.60)),
                                                        color_continuous_scale={'2020': 'Reds', '2021': 'Blues', '2022': 'Rainbow', '2023': 'Greens', '2024': 'Viridis'}[str(Year)],
                                                        center={"lat": 22.9734, "lon": 78.6569}, width=1200, height=800, title='Geo Visualization of Total Value by State'))
                except Exception as e:
                    st.error(f"Error: {e}")

                # Pie chart
                st.plotly_chart(px.pie(agg_trans, values='Count', names='Pay_Category', title='Pie Chart for Total Value'))

                
            
            # For Aggregated Users
            if search and category == 'Aggregated' and payment_type == 'Users' and Year in ['2020', '2021', '2022', '2023', '2024']:
                st.subheader(f':violet[Aggregated Users in {Year}]')

                # Query and process data
                agg_usr_df = pd.read_sql(f"SELECT * FROM agg_user_table WHERE Year = {Year}", con=db.connection)
                agg_usr_df['State'] = agg_usr_df['State'].str.replace('-', ' ').str.title()
                agg_usr_df['percentage'] = (pd.to_numeric(agg_usr_df['percentage'], errors='coerce') * 100).round(2).astype(str) + '%'
                agg_usr_df['Count'] = pd.to_numeric(agg_usr_df['Count'], errors='coerce')
                # Display unique brands and total counts
                unique_brands_df = agg_usr_df[['Brand', 'Count']].groupby('Brand', as_index=False).sum()
                st.write(unique_brands_df)

                # Calculate metrics
                total_count = agg_usr_df['Count'].sum()
                unique_brands = agg_usr_df['Brand'].nunique()
                counts = agg_usr_df['Count'].count()  # Total entries, not unique

                # Display metrics
                cl1, cl2 = st.columns(2)
                cl1.metric(label="Sum of Counts", value=f"{total_count:,.0f}")
                cl2.metric(label="Total Unique Brands", value=unique_brands)
                st.metric(label="Total Counts", value=counts)

                # Choropleth map
                try:
                    st.plotly_chart(px.choropleth_mapbox(
                        agg_usr_df, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM', locations='State', color='Count', hover_name='Brand', hover_data=['percentage'],
                        mapbox_style='carto-positron', zoom=3.5, range_color=(agg_usr_df['Count'].quantile(0.05), agg_usr_df['Count'].quantile(0.95)),
                        color_continuous_scale={'2020': 'Reds', '2021': 'Blues', '2022': 'Rainbow', '2023': 'Greens', '2024': 'Viridis'}[str(Year)],
                        center={"lat": 22.9734, "lon": 78.6569}, title='Geo Visualization of Total Value by State', width=1200, height=800
                    ).update_geos(fitbounds="locations", visible=False))
                except Exception as e:
                    st.error(f"An error occurred: {e}")

                # Pie chart
                st.plotly_chart(px.pie(agg_usr_df, values='Count', names='Brand', title='Pie Chart for Total Value'))

            # Create a Map in Insurance
            if  search and category == 'Map' and payment_type == 'Insurance' and Year in ['2020', '2021', '2022', '2023', '2024']:
                st.subheader(f':violet[Map Insurance in {Year}]')

                # Fetch and process data
                map_ins = pd.read_sql(f"SELECT * FROM map_ins_table WHERE Year = {Year}", con=db.connection)
                map_ins['State'] = map_ins['State'].str.replace('-', ' ').str.title()
                map_ins['District'] = map_ins['District'].str.replace('district', '', case=False)
                map_ins[['Amount', 'Count']] = map_ins[['Amount', 'Count']].apply(pd.to_numeric, errors='coerce')

                # Aggregate data and calculate metrics
                summary = map_ins.groupby('District').agg(Total_Count=('Count', 'sum'), Total_value=('Amount', 'sum')).reset_index()
                summary['Average_value'] = (summary['Total_value'] / summary['Total_Count']).round(2)

                # Format the total value and total count in millions
                total_value = (summary['Total_value'].sum() / 1000000).round(2)
                total_counts = (summary['Total_Count'].sum() / 1000000).round(2)
                Total_Districts = map_ins['District'].nunique()

                # Display metrics
                cl1, cl2   = st.columns(2)
                # Display the total value, total counts, and average value in metric widgets
                cl1.metric(label="Total Value (in Millions)", value=f"{total_value:,.2f}M")
                cl2.metric(label="Total Counts (in Millions)", value=f"{total_counts:,.2f}M")
                st.metric(label="Total No.of  Districts", value = Total_Districts)

                # Choropleth map
                geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                color_scales = {'2020': px.colors.sequential.Reds, '2021': px.colors.sequential.Blues,
                                '2022': px.colors.sequential.Rainbow, '2023': px.colors.sequential.Greens,
                                '2024': px.colors.sequential.Viridis}

                try:
                    fig = px.choropleth_mapbox(map_ins, geojson=geojson_url, featureidkey='properties.ST_NM', locations='State',
                                            color='Amount', hover_name='District', hover_data=['Count'], mapbox_style='carto-positron',
                                            zoom=3.5, range_color=(map_ins['Amount'].quantile(0.05), map_ins['Amount'].quantile(0.95)),
                                            color_continuous_scale=color_scales[Year], center={"lat": 22.9734, "lon": 78.6569},
                                            title=f'Geo Visualization of Total Value by State in {Year}', width=1200, height=800)
                    st.plotly_chart(fig)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

                # Subplots of bar charts by quarter
                fig = make_subplots(rows=2, cols=2, subplot_titles=[f"Bar Chart Q- {q}" for q in map_ins['Quarter'].unique()])

                for i, quarter in enumerate(map_ins['Quarter'].unique()):
                    fig.add_trace(px.bar(map_ins[map_ins['Quarter'] == quarter], x='District', y='Amount').data[0],
                                row=(i // 2) + 1, col=(i % 2) + 1)

                fig.update_layout(height=1000, width=1200, showlegend=False, title_text="Bar Charts of Amount by District for Each Quarter")
                st.plotly_chart(fig)

            # Map in transaction
            if search and category == 'Map' and payment_type == 'Transaction' and Year in ['2020', '2021', '2022', '2023', '2024']:
                st.subheader(f':violet[Map Transaction in {Year}]')

            # Fetch and clean data
                map_trans = pd.read_sql(f"SELECT * FROM map_trans_table WHERE Year = {Year}", con=db.connection)
                map_trans['State'] = map_trans['State'].str.replace('-', ' ').str.title()
                map_trans['District'] = map_trans['District'].str.replace('district', ' ', case=False)
                map_trans[['Amount', 'Count']] = map_trans[['Amount', 'Count']].apply(pd.to_numeric, errors='coerce')
                map_trans['Amount'] = (map_trans['Amount'] / 1e6).round(2)
                map_trans['Quarter'] = pd.qcut(map_trans['Amount'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
                
                # Create a list of quarters
                quarters = ['Q1', 'Q2', 'Q3', 'Q4']
                # Aggregate data and calculate metrics
                describe = map_trans.groupby('District').agg(Total_Count=('Count', 'sum'), Total_value=('Amount', 'sum')).reset_index()
                describe['Average_value'] = (describe['Total_value'] / describe['Total_Count']).round(2)

                # Format the total value and total count in millions
                total_value = (describe['Total_value'].sum() / 1000000).round(2)
                total_counts = (describe['Total_Count'].sum() / 1000000).round(2)
                Total_Districts = map_trans['District'].nunique()

                # Display metrics
                cl1, cl2   = st.columns(2)
                # Display the total value, total counts, and average value in metric widgets
                cl1.metric(label="Total Value (in Millions)", value=f"{total_value:,.2f}M")
                cl2.metric(label="Total Counts (in Millions)", value=f"{total_counts:,.2f}M")
                st.metric(label="Total No.of  Districts", value = Total_Districts)

                # Display District Total Values
                st.write(" Least 5 Districts with Amount:",  map_trans.groupby('District')['Amount'].sum().reset_index().sort_values(by='Amount', ascending=False).tail(5))

                # Display Choropleth Map
                st.plotly_chart(px.choropleth_mapbox(
                    map_trans, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM', locations='State', color='Amount', hover_data='Count',
                    mapbox_style='carto-positron', zoom=3.5, range_color=(map_trans['Amount'].quantile(0.40), map_trans['Amount'].quantile(0.60)),
                    color_continuous_scale=px.colors.sequential.Reds if Year == '2020' else px.colors.sequential.Blues,
                    center={"lat": 22.9734, "lon": 78.6569}, width=1200, height=800, title=f'Choropleth Map of Total Value - {Year}'
                ))

                # Create subplot figure
                fig = make_subplots(
                    rows=2, cols=2, 
                    subplot_titles=[f"Bar Chart - {quarter}" for quarter in quarters]
                )

                # Loop through quarters and create bar charts for each
                for i, quarter in enumerate(quarters):
                    row = (i // 2) + 1
                    col = (i % 2) + 1
                    # Filter data for the current quarter
                    quarter_data = map_trans[map_trans['Quarter'] == quarter]
                    # Create the bar chart for the current quarter
                    bar_chart = px.bar(quarter_data, x='District', y='Amount', title=f"{quarter} Amount by State")
                    # Add the bar chart to the subplot
                    fig.add_trace(bar_chart.data[0], row=row, col=col)

                # Update layout for better appearance
                fig.update_layout(height=800, width=1200, showlegend=False, title_text="Bar Charts of Amount by District for Each Quarter")
                # Display the subplots
                st.plotly_chart(fig)
    

            # Map Users page
            if search and category == 'Map' and payment_type == 'Users' and Year in ['2020', '2021', '2022', '2023', '2024']:
                st.subheader(f':violet[Map Users in {Year}]')

                # Fetch data
                map_users = pd.read_sql(f"SELECT * FROM map_user_table WHERE Year = {Year}", con=db.connection)
                map_users['State'] = map_users['State'].str.replace('-', ' ').str.title()
                map_users['District'] = map_users['District'].str.replace('district', '', case=False)
                map_users[['registeredUsers', 'appOpens']] = map_users[['registeredUsers', 'appOpens']].apply(pd.to_numeric, errors='coerce')
                map_users['Quarter'] = pd.qcut(map_users['registeredUsers'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])

                # Calculate and display metrics
                total_count = (map_users['appOpens'].sum() / 1_000_000).round(2)
                total_users = (map_users['registeredUsers'].sum() / 1_000_000).round(2)
                cl1, cl2 = st.columns(2)
                cl1.metric("App Opens (Millions)", f"{total_count:,.0f}M")
                cl2.metric("Registered Users (Millions)", f"{total_users:,.0f}M")
                st.metric("Districts", f"{map_users['District'].nunique()}")

                # Choropleth map
                try:
                    fig = px.choropleth_mapbox(
                        map_users, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM', locations='State', color='registeredUsers', hover_name='District',
                        hover_data=['appOpens'], mapbox_style='carto-positron', zoom=3.5,
                        range_color=(map_users['registeredUsers'].quantile(0.05), map_users['registeredUsers'].quantile(0.95)),
                        color_continuous_scale=px.colors.sequential.Reds, center={"lat": 22.9734, "lon": 78.6569}, width=1200, height=800
                    )
                    fig.update_geos(fitbounds="locations", visible=False)
                    st.plotly_chart(fig)
                except Exception as e:
                    st.error(f"Error: {e}")

                # Create subplot for scatter plots by quarter
                fig = make_subplots(rows=2, cols=2, subplot_titles=[f"Scatter - {q}" for q in ['Q1', 'Q2', 'Q3', 'Q4']])
                for i, quarter in enumerate(['Q1', 'Q2', 'Q3', 'Q4']):
                    row, col = divmod(i, 2)
                    quarter_data = map_users[map_users['Quarter'] == quarter]
                    scatter = px.scatter(quarter_data, x='District', y='registeredUsers', color='appOpens').data[0]
                    fig.add_trace(scatter, row=row + 1, col=col + 1)

                fig.update_layout(height=800, width=1200, showlegend=False, title_text="Scatter Plots by Quarter")
                st.plotly_chart(fig)


            # Create a Top in Insurance
            if search and category == 'Top' and payment_type == 'Insurance' and Year in ['2020', '2021', '2022', '2023', '2024']:
                st.subheader(f':violet[Top Insurance in {Year}]')

                # Fetch data
                query = f"SELECT * FROM top_ins_table WHERE Year = {Year}"
                top_ins = pd.read_sql(query, con=db.connection)
                top_ins['State'] = top_ins['State'].str.replace('-', ' ').str.title()
                top_ins[['Amount', 'Count']] = top_ins[['Amount', 'Count']].apply(pd.to_numeric, errors='coerce')

                # Aggregate data and calculate metrics
                summary = top_ins.groupby('EntityType').agg(Total_Count=('Count', 'sum'), Total_value=('Amount', 'sum')).reset_index()
                total_count, total_amount = (top_ins['Count'].sum() / 1_000_000).round(2), (top_ins['Amount'].sum() / 1_000_000).round(2)
                average = (total_amount / total_count).round(2)

                # Display metrics
                cl1, cl2 = st.columns(2)
                cl1.metric("Total Value (Millions)", f"{total_amount:,.2f}M")
                cl2.metric("Total Counts (Millions)", f"{total_count:,.2f}M")
                st.metric("Average Value", f"{average:,.2f}")

                # Choropleth map
                color_scales = {'2020': px.colors.sequential.Reds, '2021': px.colors.sequential.Blues, '2022': px.colors.sequential.Rainbow, '2023': px.colors.sequential.Greens, '2024': px.colors.sequential.Viridis}
                try:
                    fig = px.choropleth_mapbox(
                        top_ins, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM', locations='State', color='Amount', hover_name='EntityType', hover_data=['Count'],
                        mapbox_style='carto-positron', zoom=3.5, range_color=(top_ins['Amount'].quantile(0.05), top_ins['Amount'].quantile(0.95)),
                        color_continuous_scale=color_scales[str(Year)], center={"lat": 22.9734, "lon": 78.6569}, title='Geo Visualization of Total Value by State',
                        width=1200, height=800
                    )
                    fig.update_geos(fitbounds="locations", visible=False)
                    st.plotly_chart(fig)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

                # Bar chart
                st.plotly_chart(px.bar(top_ins, x='EntityName', y='Amount', color='EntityType', title="Amount by EntityName", labels={'Amount': 'Amount', 'EntityName': 'Entity Name'}))

            # Top in transaction # By SUb Plots
            if search and category == 'Top' and payment_type == 'Transaction' and Year in ['2020', '2021', '2022', '2023', '2024']:
                st.subheader(f':violet[Top Transaction in {Year}]')

                # Fetch and process data
                query = f"SELECT * FROM top_trans_table WHERE Year = {Year}"
                top_trans = pd.read_sql(query, con=db.connection)
                top_trans['State'] = top_trans['State'].str.replace('-', ' ').str.title()
                top_trans[['Amount', 'Count']] = top_trans[['Amount', 'Count']].apply(pd.to_numeric, errors='coerce')

                # Aggregate and calculate metrics
                total_count = (top_trans['Count'].sum() / 100_000_000).round(2)
                total_amount = (top_trans['Amount'].sum() / 100_000_000).round(2)
                average = (total_amount / total_count).round(2)

                # Display metrics
                cl1, cl2 = st.columns(2)
                cl1.metric("Total Value (Billions)", f"{total_amount:,.2f}B")
                cl2.metric("Total Counts (Billions)", f"{total_count:,.2f}B")
                st.metric("Average Value ", f"{average:,.2f}")
                # Choropleth map setup
                color_scales = {'2020': px.colors.sequential.Reds, '2021': px.colors.sequential.Blues, '2022': px.colors.sequential.Rainbow, '2023': px.colors.sequential.Greens, '2024': px.colors.sequential.Viridis}
                geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

                # Create and display choropleth map
                try:
                    fig = px.choropleth_mapbox(
                        top_trans, geojson=geojson_url, featureidkey='properties.ST_NM', locations='State',
                        color='Amount', hover_data=['Count'], hover_name='EntityType',
                        mapbox_style='carto-positron', zoom=3.5, range_color=(top_trans['Amount'].quantile(0.20), top_trans['Amount'].quantile(0.80)),
                        color_continuous_scale=color_scales[str(Year)], center={"lat": 22.9734, "lon": 78.6569},
                        title='Choropleth Map of Total Value by State', width=1200, height=800
                    )
                    fig.update_geos(fitbounds="locations", visible=False)
                    st.plotly_chart(fig)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

                # Bar chart for Amount by EntityName
                st.plotly_chart(px.bar(top_trans, x='EntityName', y='Amount', color='EntityType', title="Amount by EntityName", labels={'Amount': 'Amount', 'EntityName': 'Entity Name'}))
    
            # Top Users in github    
            if search and category == 'Top' and payment_type == 'Users' and Year in ['2020', '2021', '2022', '2023', '2024']:
                st.subheader(f':violet[Top Users in {Year}]')

                # Fetch and process data
                query = f"SELECT * FROM top_user_table WHERE Year = {Year}"
                top_users = pd.read_sql(query, con=db.connection)
                top_users['State'] = top_users['State'].str.replace('-', ' ').str.title()
                top_users['registeredUsers'] = pd.to_numeric(top_users['registeredUsers'], errors='coerce')

                # Calculate and display metrics
                total_users = (top_users['registeredUsers'].sum() / 1_000_000).round(2)
                cl1, cl2 = st.columns(2)
                cl1.metric("Registered Users (Millions)", f"{total_users:,.0f}M")
                cl2.metric("Total Entity Name Count", f"{top_users['EntityName'].nunique()}")

                st.write(top_users.head())

                # Choropleth map setup
                color_scales = {'2020': px.colors.sequential.Reds, '2021': px.colors.sequential.Blues, '2022': px.colors.sequential.Rainbow, '2023': px.colors.sequential.Greens, '2024': px.colors.sequential.Viridis}
                geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

                # Create and display choropleth map
                try:
                    fig = px.choropleth_mapbox(
                        top_users, geojson=geojson_url, featureidkey='properties.ST_NM', locations='State',
                        color='registeredUsers', hover_name='EntityType',
                        mapbox_style='carto-positron', zoom=3.5, 
                        range_color=(top_users['registeredUsers'].quantile(0.20), top_users['registeredUsers'].quantile(0.80)),
                        color_continuous_scale=color_scales[str(Year)], center={"lat": 22.9734, "lon": 78.6569},
                        title='Choropleth Map of Registered Users by State', width=1200, height=800
                    )
                    st.plotly_chart(fig)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

                # Bar plot for EntityName vs Registered Users
                st.plotly_chart(px.bar(top_users, x='EntityName', y='registeredUsers', color='EntityType', 
                                    title="Registered Users by EntityName", labels={'registeredUsers': 'Registered Users', 'EntityName': 'Entity Name'}))
        else:
            st.warning("Please ensure you select the correct combination of Category, Payment Type, and Year.")

    # Aggregated Insurance Table
    query = f"SELECT * FROM agg_ins_table "
    ag_ins_table  = pd.read_sql(query, con=db.connection)
    # Aggregated Transaction Table  
    query = f"SELECT * FROM agg_trans_table "
    ag_trans_table = pd.read_sql(query, con=db.connection)
    #Aggregated Users Table
    query = f"SELECT * FROM agg_user_table "
    ag_users_table  = pd.read_sql(query, con=db.connection)
    # Map Insurance Table
    query = f"SELECT * FROM map_ins_table "
    map_ins_table = pd.read_sql(query, con=db.connection)
    # Map Transcation Table
    query = f"SELECT * FROM map_trans_table "
    map_trans_table = pd.read_sql(query, con=db.connection)
    # Map Users Table
    query = f"SELECT * FROM map_user_table "
    map_user_table = pd.read_sql(query, con=db.connection)

    # Top Insuance Table
    query = f"SELECT * FROM top_ins_table "
    top_ins_table = pd.read_sql(query, con=db.connection)   
    # Top Transaction Table
    query = f"SELECT * FROM top_trans_table "
    top_trans_table = pd.read_sql(query, con=db.connection)  
    # Top Users Table
    query = f"SELECT * FROM top_user_table "
    top_user_table = pd.read_sql(query, con=db.connection)   
 
    # FAQ's
    if option == 'FAQs':
        st.balloons()
        st.header('Frequently Asked Questions in the Data')# List of FAQ questions
        questions = [
            "1. What is the Total Transactions Count Across States by Quarter?",
            "2. WWhat is the Top & Last 5 States of Total insurance amount by states",
            "3. What is the Trend of registered users over quarters for a selected state",
            "4. Subplots for the relationship between transaction count and value",
            "5. Which are the top 5 states in terms of total insurance count (Count)?",
            "6. What is the Total amount and Count in the Transactions by the year wise?",
            "7. What are the top 5  Brands in Aggretaed Users?",
            "8. Display the Map Category by the year wise?",
            "9. What is the total transaction amount (Amount) for each year?",
            "10. How much of Count has the across the all Category in the State wise?"
        ]

            # Multi-select option to choose questions
        selected_questions = st.multiselect(
            "Select a Question to view the Answer in Visuals", questions)
        if st.button("Run Selected Questions"):
            for quest in selected_questions:  # Loop through selected questions

                # Q1: Total Transactions Count Across States
                if quest == questions[0]:
                    df = pd.concat([ag_trans_table, map_trans_table, top_trans_table])
                    fig = px.bar(df, x='State', y='Count', color='Quarter',
                                title="Total Transactions Count Across States")
                    fig.update_layout(xaxis_title="State",
                                    yaxis_title="Transaction Count",
                                    xaxis_tickangle=-45,
                                    plot_bgcolor="rgba(0, 0, 0, 0)",
                                    paper_bgcolor="rgba(0, 0, 0, 0)")
                    st.plotly_chart(fig)

                # Q2: Total insurance Counts by State Wise
                elif quest == questions[1]: 
                    ins_df = pd.concat([ag_ins_table, map_ins_table,top_ins_table])
                    trans_df = pd.concat([ag_trans_table,map_trans_table,top_trans_table])
                    users_df = pd.concat([ag_users_table,map_user_table,top_user_table])
                    fig1 = px.line(ins_df,x ='State',y ='Count', color = 'Year', title = " Aggregated Line Chart for the State and Count by Year ")
                    fig2 = px.line(trans_df, x = 'State', y = 'Count', color= 'Year', title = " Map Line Chart for the State and Count by Year")
                    fig3 = px.line(users_df, x = 'State', y = 'Count', color= 'Year', title = " Top Line Chart for the State and Count by Year")
                    st.plotly_chart(fig1)
                    st.plotly_chart(fig2)
                    st.plotly_chart(fig3)                   
                # Q3: Trend of registered users over quarters for a selected state
                elif quest == questions[2]:
                    df = pd.concat([ag_users_table,map_user_table, top_user_table])
                    fig = px.scatter(df, x='State', y='registeredUsers', color='Quarter',
                                title="Trend of Registered Users Over Quarters")
                    st.plotly_chart(fig)

                # Q4: Subplots for the relationship between transaction count and value
                elif quest == questions[3]:
                    df = pd.concat([ag_trans_table, map_trans_table, top_trans_table])
                    fig = make_subplots(rows=1, cols=2, subplot_titles=("Transaction Count vs Transaction Value", "Count vs Amount by District"))
                    # Scatter plot 1
                    scatter1 = px.scatter(df, x='Count', y='Total_value', color='State')
                    # Add trace
                    fig.add_trace(go.Scatter(x=scatter1.data[0]['x'], y=scatter1.data[0]['y'], mode='markers', name='Count vs Total_value'),
                                row=1, col=1)
                    
                    # Scatter plot 2
                    scatter2 = px.scatter(df, x='Count', y='Amount', color='District')
                    # Add trace
                    fig.add_trace(go.Scatter(x=scatter2.data[0]['x'], y=scatter2.data[0]['y'], mode='markers', name='Count vs Amount'),
                                row=1, col=2)
                    
                    fig.update_layout(height=600, showlegend=False)
                    st.plotly_chart(fig)

                # Q5: Top 5 states by insurance count
                elif quest == questions[4]:
                    df = pd.concat([ag_ins_table,map_ins_table, top_ins_table] )
                    # Convert 'Count' column to numeric, coercing errors (non-numeric values will become NaN)
                    df['Count'] = pd.to_numeric(df['Count'], errors='coerce')
    
                    # Drop rows where 'Count' is NaN
                    df = df.dropna(subset=['Count'])

                    # Group by 'State', 'Quarter', and 'Year' to sum the 'Count' column
                    top_states = df.groupby(['State', 'Quarter', 'Year']).sum().nlargest(5, 'Count').reset_index()


                # Create a bar chart of the top 5 states by insurance count with Quarter as color and Year in hover
                    fig = px.bar(top_states, 
                                x='State', 
                                y='Count', 
                                color='Quarter', 
                                hover_data=['Year'],  # Include year in hover data
                                title="Top 5 States by Insurance Count",
                                labels={'Count':'Total Count', 'State':'State', 'Quarter':'Quarter', 'Year':'Year'})

                    # Update layout for better visual
                    fig.update_layout(
                        xaxis_tickangle=-45, 
                        plot_bgcolor="rgba(0, 0, 0, 0)",
                        paper_bgcolor="rgba(0, 0, 0, 0)",
                        xaxis_title="State",
                        yaxis_title="Transaction Count"
                    )
                    
                    # Display the chart in Streamlit
                    st.plotly_chart(fig)    

                # Q6: Distribution of app opens by district in a selected state
                elif quest == questions[5]:
                    df = pd.concat([map_user_table, ag_users_table, top_user_table])
                    fig = px.histogram(df, x='State', y='appOpens',
                                    title="Distribution of App Opens by State")
                    st.plotly_chart(fig)

                # Q7: Registered users across states in the most recent quarter
                elif quest == questions[6]:
                    df3 =  pd.concat([ag_users_table, map_user_table, top_user_table])
                    fig = px.bar(df3, x='State', y='registeredUsers', color = 'Year',
                                title="Registered Users Across States (Most Recent Quarter)")
                    st.plotly_chart(fig)

                # Q8: Sunburst chart for count of transactions by entity types
                elif quest == questions[7]:
                    fig = px.sunburst(ag_trans_table, path=['State', 'Category'], values='Count',
                                    title="Transactions by Entity Type")
                    st.plotly_chart(fig)
                # Q9: Line plot for total transaction amount for each year
                elif quest == questions[8]:
                    ag_trans_table['Year'] = pd.to_datetime(ag_trans_table['Quarter']).dt.year
                    total_by_year = ag_trans_table.groupby('Year').sum().reset_index()
                    fig = px.line(total_by_year, x='Year', y='Total_value',
                                title="Total Transaction Amount by Year")
                    st.plotly_chart(fig)

                # Q10: Pie chart for percentage of app opens by device brand
                elif quest == questions[9]:
                    selected_quarter = ag_trans_table[ag_trans_table['Quarter'] == 'Q1']  # Adjust for actual quarter selection
                    fig = px.pie(selected_quarter, names='Device', values='appOpens',
                                title="App Opens by Device Brand")
                    st.plotly_chart(fig)

if __name__ == "__main__":
    main() 


