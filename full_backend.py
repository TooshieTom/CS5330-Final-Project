import mysql.connector as mysql
import mysql.connector.errors
import os
import csv
from dotenv import load_dotenv
import json
from collections import defaultdict
import os
import mysql.connector
from mysql.connector import Error
from typing import Optional

    
# Functions here

# Functions
def makeTable(cursor):
    # Make User table
    cursor.execute("""
    CREATE TABLE if NOT EXISTS User (
       Username VARCHAR(40) NOT NULL,
       Soc_Med VARCHAR(50) NOT NULL,
       Name VARCHAR(100),
       Verified BOOLEAN,
       Country_Birth VARCHAR(50),
       Country_Res VARCHAR(50),
       Age INT CHECK (Age >= 0 AND Age <= 200),
       Gender VARCHAR(20),
       PRIMARY KEY (Username, Soc_Med)
    );
    """)
    # Make Post table
    cursor.execute("""
    CREATE TABLE if NOT EXISTS Post (
       Username VARCHAR(40) NOT NULL,
       Soc_Med VARCHAR(50) NOT NULL,
       Time_Posted TIMESTAMP,
       City VARCHAR(50),
       State VARCHAR(50),
       Country VARCHAR(50),
       Multimedia VARCHAR(50),
       Name_F VARCHAR(50),
       Name_L VARCHAR(50),
       Likes INT CHECK (Likes >= 0),
       Dislikes INT CHECK (Dislikes >= 0),
       Text TEXT,
       Poster_OG VARCHAR(40),
       Time_OG TIMESTAMP,
	    PRIMARY KEY(Username,Soc_Med,Time_Posted),
        FOREIGN KEY (Username, Soc_Med) REFERENCES User(Username, Soc_Med)
    );
    """)
    # Make Project Table
    cursor.execute("""
    CREATE TABLE if NOT EXISTS Project (
       Name VARCHAR(100) PRIMARY KEY,
       Manager VARCHAR(100),
       Institute VARCHAR(100),
       Start_Date DATE,
       End_Date DATE
   );

    """)
    # Make Record Table
    cursor.execute("""
    CREATE TABLE if NOT EXISTS Record (
       Project VARCHAR(100) NOT NULL,
       Text TEXT,
       Fields JSON,
       Username VARCHAR(40) NOT NULL,
       Time_Posted DATE NOT NULL,
       Soc_Med VARCHAR(50) NOT NULL,
        PRIMARY KEY(Project,Username,Soc_Med,Time_Posted),
       FOREIGN KEY (Project) REFERENCES Project(Name)
   );
    """)



def clearTuples():
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve values
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    try:
        # Establish connection
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user=db_user,
            password=db_password,
            database="postdb",
            connection_timeout=5,  # force error if hangs
            auth_plugin="caching_sha2_password",
            use_pure=True
        )
        # Create a cursor object
        cursor = conn.cursor()
        makeTable(cursor)

        cursor.execute("DELETE FROM User;")

        cursor.execute("DELETE FROM Post;")
        
        cursor.execute("DELETE FROM Project;")

        cursor.execute("DELETE FROM Record;")


    except mysql.connector.Error as err:
        print("Input Invalid")
        return 1
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return
    finally:
        # Close the cursor
        if cursor is not None: 
            try:
                cursor.close()  
            except Exception as e:
                print(f"Unexpected error while closing cursor: {e}")
        # Close the connection
        if conn is not None:
            try:
                conn.close()  
                # print("Database connection closed.")
            except Exception as e:
                print(f"Unexpected error while closing connection: {e}")


def enterTuple(inputs):
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve values
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    try:
        # Establish connection
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user=db_user,
            password=db_password,
            database="postdb",
            connection_timeout=5,  # force error if hangs
            auth_plugin="caching_sha2_password",
            use_pure=True
        )

        # Create a cursor object
        cursor = conn.cursor()

        # Do pre-processing
        query = "INSERT INTO "
        num_inputs = 0
        parameters = []
        # Need to convert into parameterized query, and then execute
        if len(inputs) == 8:
            # User input
            query += "`user` ("
            for i in range(len(inputs)):
                value = inputs[i]
                # update query depending on values
                if value == "":
                    continue
                elif i == 0:
                    query += "username, "
                elif i == 1:
                    query += "soc_med, "
                elif i == 2:
                    query += "name, "
                elif i == 3:
                    query += "verified, "
                elif i == 4:
                    query += "country_birth, "
                elif i == 5:
                    query += "country_res, "
                elif i == 6:
                    query += "age, "
                elif i == 7:
                    query += "gender, "
                num_inputs += 1
                parameters.append(inputs[i])

        elif len(inputs) == 5:
            # Project
            query += "project ("
            for i in range(len(inputs)):
                value = inputs[i]
                # update query depending on values
                if value == "":
                    continue
                elif i == 0:
                    query += "name, "
                elif i == 1:
                    query += "manager, "
                elif i == 2:
                    query += "institute, "
                elif i == 3:
                    query += "start_date, "
                elif i == 4:
                    query += "end_date, "
                num_inputs += 1
                parameters.append(inputs[i])
        elif len(inputs) == 6:
            # Record
            query += "record ("
            for i in range(len(inputs)):
                value = inputs[i]
                # update query depending on values
                if value == "":
                    continue
                elif i == 0:
                    query += "project, "
                elif i == 1:
                    query += "text, "
                elif i == 2:
                    query += "fields, "
                elif i == 3:
                    query += "username, "
                elif i == 4:
                    query += "time_posted, "
                elif i == 5:
                    query += "soc_med, "
                num_inputs += 1
                parameters.append(inputs[i])
        else:
            # Post
            query += "post ("
            for i in range(len(inputs)):
                value = inputs[i]
                # update query depending on values
                if value == "":
                    continue
                elif i == 0:
                    query += "username, "
                elif i == 1:
                    query += "soc_med, "
                elif i == 2:
                    query += "time_posted, "
                elif i == 3:
                    query += "city, "
                elif i == 4:
                    query += "state, "
                elif i == 5:
                    query += "country, "
                elif i == 6:
                    query += "multimedia, "
                elif i == 7:
                    query += "name_f, "
                elif i == 8:
                    query += "name_l, "
                elif i == 9:
                    query += "likes, "
                elif i == 10:
                    query += "dislikes, "
                elif i == 11:
                    query += "text, "
                elif i == 12:
                    query += "poster_og, "
                elif i == 13:
                    query += "date_og, "
                num_inputs += 1
                parameters.append(inputs[i])


        query = query[:-2]
        query += ") VALUES ("
        
        for i in range(num_inputs):
            query += "%s, "
        query = query[:-2]
        query += ")"

        print(query)
        print(parameters)

        cursor.execute(query,parameters)
        conn.commit()



    except mysql.connector.Error as err:
        print("Input Invalid")
        return 1
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return
    finally:
        # Close the cursor
        if cursor is not None: 
            try:
                cursor.close()  
            except Exception as e:
                print(f"Unexpected error while closing cursor: {e}")
        # Close the connection
        if conn is not None:
            try:
                conn.close()  
                # print("Database connection closed.")
            except Exception as e:
                print(f"Unexpected error while closing connection: {e}")

def query_post(table,columns: list):
        load_dotenv()

        # Retrieve values
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        try:
            # Establish connection
            conn = mysql.connector.connect(
                host="127.0.0.1",
                user=db_user,
                password=db_password,
                database="postdb",
                connection_timeout=5,  # force error if hangs
                auth_plugin="caching_sha2_password",
                use_pure=True
            )

            # Create a cursor object
            cursor = conn.cursor()
            query = ""
            if table == "User":
                query = """
                    SELECT *
                    FROM User
                    WHERE 1=1
                    """
            elif table == "Post":
                query = """
                    SELECT *
                    FROM Post
                    WHERE 1=1
                    """
            elif table == "Project":
                query = """
                    SELECT *
                    FROM Project
                    WHERE 1=1
                    """
            elif table == "Record":
                query = """
                    SELECT *
                    FROM Record
                    WHERE 1=1
                    """
            else:
                print(f"{table} is an invalid table")
            parameters = []
            # parameters.append(table)
            if(len(columns)%3==0):
                for i in range(0,len(columns)//3):
                    if(columns[3*i+1]=="<"):
                        query+= "%s < %s"
                    elif(columns[3*i+1]==">"):
                        query+= "%s > %s"
                    elif(columns[3*i+1]=="=="):
                        query+= "%s == %s"
                    elif(columns[3*i+1]==">="):
                        query+= "%s >= %s"
                    elif(columns[3*i+1]=="<="):
                        query+= "%s > %s"
                    elif(columns[3*i+1]=="!="):
                        query+= "%s > %s"
                    else:
                        print("{columns[3*i+1]} is an invalid operator.")
                    parameters.append(columns[i*3])
                    parameters.append(columns[3*i+2])
            else:
                print("Error: Weird amount of items in the column list")

            cursor.execute(query, parameters)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Error querying posts: {e}")
            return []
        finally:
            if conn:
                conn.close()
def query_projects(table, project_name):
    load_dotenv()

        # Retrieve values
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    try:
            # Establish connection
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user=db_user,
            password=db_password,
            database="postdb",
            connection_timeout=5,  # force error if hangs
            auth_plugin="caching_sha2_password",
            use_pure=True
        )

            # Create a cursor object
        cursor = conn.cursor()

        # cursor.execute("""
        #     SELECT * FROM %s WHERE Project_Name = %s
        # """, (table,project_name,))
        cursor.execute("""
            SELECT * FROM Record WHERE Project_Name = %s
        """, (project_name,))
        records = cursor.fetchall()

        if not records:
            return {
                "message": f"No posts found for project '{project_name}'.",
                "posts": [],
                "field_coverage": {}
            }

        posts = []
        field_counts = defaultdict(int)

        for record in records:

            raw_fields = record.get('Fields')
            try:
                fields = json.loads(raw_fields) if isinstance(raw_fields, str) else raw_fields
            except Exception as e:
                print(f"Error parsing fields for record {record.get('ID', 'unknown')}: {e}")
                fields = {}

            for key in fields:
                field_counts[key] += 1

            post_entry = {
                "Record_Identifier": {
                    "Project": record.get("Project"),
                    "Username": record.get("Username"),
                    "Time_Posted": str(record.get("Time_Posted")), 
                    "Soc_Med": record.get("Soc_Med")
                },
                "Fields": fields
            }

            posts.append(post_entry)

        total_posts = len(posts)


        field_coverage = {
            field: round((count / total_posts) * 100, 2)
            for field, count in field_counts.items()
        }

        return {
            "project": project_name,
            "posts": posts,
            "field_coverage": field_coverage
        }

    except Exception as e:
        print(f"Error querying project data: {e}")
        return {
            "error": str(e),
            "posts": [],
            "field_coverage": {}
        }
    finally:
        if conn:
            conn.close()



def main():
    # clearTuples()
    input = ['Pooper', 'Scooper', '1970-02-01 00:00:01', '', '', '','','','','-1','','','']
    # enterTuple(input)

main()



# Query post and project
    # Post: query by social media and username, between times, certain first/last name
        