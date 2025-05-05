import mysql.connector as mysql
import mysql.connector.errors
import os
import csv
from dotenv import load_dotenv

    
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
       Fields TEXT,
       Username VARCHAR(40) NOT NULL,
       Time_Posted TIMESTAMP NOT NULL,
       Soc_Med VARCHAR(50) NOT NULL,
        PRIMARY KEY(Project,Username,Soc_Med,Time_Posted),
       FOREIGN KEY (Project) REFERENCES Project(Name)
   );
    """)



def clearTuples(cursor):
    makeTable(cursor)

    cursor.execute("DELETE FROM User;")

    cursor.execute("DELETE FROM Post;")
    
    cursor.execute("DELETE FROM Project;")

    cursor.execute("DELETE FROM Record;")


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
        query = "INSERT INTO "
        num_inputs = 0
        # Need to convert into parameterized query, and then execute
        if len(inputs) == 8:
            # User input
            query += "user ("
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

            query = query[:-2]
            query += ") VALUES ("
            
            for i in range(num_inputs):
                query += "%s, "
            query = query[:-2]
            query += ")"

            print(query)


                


        if len(inputs) == 5:
            # Project
            query += "project "
        if len(inputs) == 6:
            # Record
            query += "record "
        else:
            # Post
            query += "post "

    except mysql.connector.Error as err:
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


def main():
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

        clearTuples(cursor)

        input = ["TooshieTom","Twitter","","","","","",""]
        enterTuple(input,cursor)




           
    except mysql.connector.errors.Error as err:
        print(f"Database error while processing commands: {err}")
        return
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

main()



# Query post and project
    # Post, query by social media, between times, 
        
