#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 14:12:38 2021

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

#manually update all null values in selected table
def update_null():
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
                        
                    #check for empty cell and insert value
                    def update():
                        cursor.execute(create_query.format(selected_table))
                        update_query_total =""
                        for row in cursor:
                            row_id=row[0]
                            for cell,column in zip(list(row),column_names):
                                if cell != None and cell != "":
                                    pass
                                else:
                                    #skip if no value is entered
                                    value = input("Input %s for %s: " % (column, row_id))
                                    if value == "":
                                        continue
                                    
                                    update_query = """
                                    UPDATE 
                                        {}
                                    SET
                                        {}="{}"
                                    WHERE
                                        {}={};
                                    """.format(
                                        selected_table,     #table that needs update
                                        column,             #column that needs update
                                        value,              #new value
                                        column_names[0],    #where id_column
                                        row_id,             #row_id
                                        )
                                    update_query_total = update_query_total + update_query
                                    print(update_query_total)
                        return(update_query_total)
                    cursor.execute(update())
    except Error as e:
        print("error: ", e)
        
update_null()