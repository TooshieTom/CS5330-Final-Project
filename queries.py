import json
from collections import defaultdict
import os
import mysql.connector
from mysql.connector import Error
from typing import Optional


def create_db_connection() -> Optional[mysql.connector.connection.MySQLConnection]:
    connection = None

    config = {
        'host': os.getenv("DB_HOST", "localhost"),
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"),
        'database': 'dbprog',
        'port': int(os.getenv("DB_PORT", "3306")),
        'raise_on_warnings': True,
        'buffered': True,
        'connection_timeout': 10
    }

    try:
        # print("Connecting to mysqldatabase database...")
        connection = mysql.connector.connect(**config)
        # print("Connection established successfully.")
        return connection

    except Error as e:
        print("Error connecting to MySQL ", e)
        if connection and connection.is_connected():
            connection.close()
        return None
    except Exception as e:
        print("Unexpected error: ", e)
        if connection and connection.is_connected():
            connection.close()
        return None


# user table
def create_tables():
    conn = None
    try:
        conn = create_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE `User` (
            Username VARCHAR(40) NOT NULL,
            Soc_Med VARCHAR(50) NOT NULL,
            Name VARCHAR(100),
            Verified BOOLEAN,
            Country_Birth VARCHAR(50),
            Country_Res VARCHAR(50),
            Age INT CHECK (Age BETWEEN 0 AND 125),
            Gender VARCHAR(20),
            PRIMARY KEY (Username, Soc_Med)
        );''')

        # Create post Table
        # time_posted is the time that post was made. The Time_OG is the time that the orignal post was made. If the time_posted and the time_OG are the same its a new post. If they're different its a repost
        cursor.execute('''
        CREATE TABLE Post (
            Username VARCHAR(40) NOT NULL,
            Soc_Med VARCHAR(50) NOT NULL,
            Time_Posted TIMESTAMP NOT NULL,
            City VARCHAR(50),
            State VARCHAR(50),
            Country VARCHAR(50),
            Multimedia VARCHAR(50),
            Likes INT CHECK (Likes >= 0),
            Dislikes INT CHECK (Dislikes >= 0),
            Text TEXT,
            Poster_OG VARCHAR(40),
            Time_OG TIMESTAMP,
            PRIMARY KEY(Username, Soc_Med, Time_Posted),
            FOREIGN KEY (Username, Soc_Med) REFERENCES `User`(Username, Soc_Med)
        );''')

        # create project table
        cursor.execute('''
        CREATE TABLE Project (
            Name VARCHAR(100) NOT NULL, 
            Manager VARCHAR(100),
            Institute VARCHAR(100),
            Start_Date DATE,
            End_Date DATE,
            PRIMARY KEY(Name)
        );''')

        # create Table Record
        cursor.execute('''
        CREATE TABLE Record (
            Project VARCHAR(100) NOT NULL,
            Text TEXT,
            Fields TEXT,
            Username VARCHAR(40),
            Time_Posted TIMESTAMP,
            Soc_Med VARCHAR(50),
            PRIMARY KEY(Project, Username, Time_Posted, Soc_Med),
            FOREIGN KEY (Project) REFERENCES Project(Name)
        );''')

        conn.commit()
        return True
    except Exception as e:
        print(f"Error {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def query_post(table,columns: list):
        conn = None
        try:
            conn = create_db_connection()
            cursor = conn.cursor(dictionary=True)
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

    conn = None
    try:
        conn = create_db_connection()
        cursor = conn.cursor(dictionary=True)

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
