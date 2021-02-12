#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 14:15:17 2021

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

#delete a specified row in a selected table
def delete_entry():
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
                    
                    #create query for deletion
                    delete_query="DELETE FROM {} WHERE {} = {};".format(selected_table,column_names[0],input("Which id do you want to delete? "))
                    cursor.execute(delete_query)
                    
    except Error as e:
        print("error: ", e)