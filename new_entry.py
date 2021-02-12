#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 14:13:43 2021

@author: jurjenvangenugten
"""

from mysql.connector import connect, Error
import json

with open('mysql_login.json') as json_file:
    credentials = json.load(json_file)["mysql_login"][0]
    
HOST=credentials['HOST']
DB_USER=credentials['DB_USER']
DB_PASS=credentials['DB_PASS']
DB_NAME=credentials['DB_NAME']

#add a specified row in a selected table
def new_entry():
    try:
        with connect(
            host=HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            autocommit=True
            ) as connection:
                with connection.cursor(buffered=True) as cursor:
                    #fetch tables from database
                    cursor.execute("SHOW TABLES")
                    for table in cursor:
                        print(table)
                    
                    #manually select table from options
                    create_query="SELECT * FROM {}"
                    selected_table = input("Which table? ")
                    cursor.execute(create_query.format(selected_table))
                    
                    #fetch columns from table and create a list
                    describe_query = "DESCRIBE {}"
                    cursor.execute(describe_query.format(selected_table))
                    meta = cursor.fetchall()
                    column_names = []
                    for row in meta:
                        column_names.append(row[0])
                    
                    #create query to insert values into selected table
                    entry_query = """INSERT INTO {}{} VALUES""".format(selected_table,tuple(column_names)).replace("'","")
                    values = []
                    max_value = -1
                    for column in column_names:
                        if "_id" in column and max_value == -1:
                            max_query = "SELECT MAX({}) FROM {}".format(column,selected_table)
                            cursor.execute(max_query)
                            max_value = cursor.fetchall()[0][0]
                            value = max_value + 1
                        else:
                            value = input("Give {}: ".format(column))
                        values.append(value)
                    entry_query = entry_query + str(tuple(values))
                    print(entry_query)
                    cursor.execute(entry_query)
                    
    except Error as e:
        print("error: ", e)