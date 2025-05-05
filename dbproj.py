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


def query_posts(Username=None, Soc_Med=None, Time_Posted=None, City=None, State=None, Country=None, Likes=None, Dislikes=None, Poster_OG=None, Time_OG=None,
                Name=None, Verified=None, Country_Birth=None, Country_Res=None, Age=None, Gender=None,
                Time_Posted_Oldest=None, Time_Posted_Youngest=None):
    conn = None
    try:
        conn = create_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT p.Username, p.Soc_Med, p.Time_Posted, 
               u.Name
        FROM Post p
        JOIN `User` u ON p.Username = u.Username AND p.Soc_Med = u.Soc_Med
        WHERE 1=1
        """

        params = []
        if Username:
            query += " AND p.Username = %s"
            params.append(Username)
        if Soc_Med:
            query += " AND p.Soc_Med = %s"
            params.append(Soc_Med)
        if Time_Posted:
            query += " AND p.Time_Posted = %s"
            params.append(Time_Posted)

        if Time_Posted_Youngest:
            query += " AND p.Time_Posted <= %s"
            params.append(Time_Posted_Youngest)
        if Time_Posted_Oldest:
            query += " AND p.Time_Posted >= %s"
            params.append(Time_Posted_Oldest)

        if City:
            query += " AND p.City = %s"
            params.append(City)
        if State:
            query += " AND p.State = %s"
            params.append(State)
        if Country:
            query += " AND p.Country = %s"
            params.append(Country)
        if Likes:
            query += " AND p.Likes = %s"
            params.append(Likes)
        if Dislikes:
            query += " AND p.Dislikes = %s"
            params.append(Dislikes)
        if Poster_OG:
            query += " AND p.Poster_OG = %s"
            params.append(Poster_OG)
        if Time_OG:
            query += " AND p.Time_OG = %s"
            params.append(Time_OG)
        if Name:
            query += " AND u.Name = %s"
            params.append(Name)
        if Verified is not None:
            query += " AND u.Verified = %s"
            params.append(Verified)
        if Country_Birth:
            query += " AND u.Country_Birth = %s"
            params.append(Country_Birth)
        if Country_Res:
            query += " AND u.Country_Res = %s"
            params.append(Country_Res)
        if Age:
            query += " AND u.Age = %s"
            params.append(Age)
        if Gender:
            query += " AND u.Gender = %s"
            params.append(Gender)

        query += " GROUP BY p.Text, p.Username, p.Soc_Med, p.Time_Posted, u.Name"

        cursor.execute(query, params)
        results = cursor.fetchall()
        return results

    except Exception as e:
        print(f"Error querying posts: {e}")
        return []
    finally:
        if conn:
            conn.close()
def assign_fields(Project, Username, Time_Posted, Soc_Med, Fields):
    try:
        conn = create_db_connection()
        cursor = conn.cursor()

        update_query = """
        UPDATE Record
        SET Fields = %s
        WHERE Project = %s AND Username = %s AND Time_Posted = %s AND Soc_Med = %s
        """

        cursor.execute(update_query, (Fields, Project, Username, Time_Posted, Soc_Med))
        conn.commit()

        if cursor.rowcount == 0:
            print("No matching record found to update.")
            return False
        else:
            print("Fields updated successfully.")
            return True

    except Exception as e:
        print(f"Error updating fields: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

# TO DO LIST as per our discussion may 3rd (I removed the stuff i finished and checkmarked it on discord)
# make_record(Project_Name,Username, Time_Posted, Soc_Med, Fields) to create a record
# For Queries --- SELECT FROM and WHERE each have a text field that they enter into
# Library- faker to populate and test database (DATA BASE TEST)
# Dropdown for FROM which lists tables
# dropdown for the column
#       equals, <=, <, >, >=, !=
# AND button/checkmark, add another column option
# TEST THIS