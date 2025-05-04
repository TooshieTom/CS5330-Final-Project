import mysql.connector as mysql
import mysql.connector.errors
import os
import csv
from dotenv import load_dotenv



# Hey Dr. Lin, Here's my project. Output formats are matched pretty closely to what you asked outside of minimal spacing differences (and ordering for output5)
# I also did the extra part as a 5000 level student

    
# Functions here

# Functions
def makeTable(cursor):
    # Make player table
    cursor.execute("""
    CREATE TABLE if NOT EXISTS Player (
    ID CHAR(8) PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Rating FLOAT NOT NULL CHECK (Rating >= 0)
        );
    """)
    # Make Game table
    cursor.execute("""
    CREATE TABLE if NOT EXISTS Game (
    Date DATETIME NOT NULL,
    Time INT(4) NOT NULL,
    Acidic CHAR(8) NOT NULL,
    Alkaline CHAR(8) NOT NULL,
    AcScore INT CHECK (AcScore BETWEEN 0 AND 10),
    AkScore INT CHECK (AkScore BETWEEN 0 AND 10),
    AcRating FLOAT CHECK (AcRating >= 0),
    AkRating FLOAT CHECK (AkRating >= 0),
    PRIMARY KEY (Date, Time, Acidic),
    FOREIGN KEY (Acidic) REFERENCES Player(ID),
    FOREIGN KEY (Alkaline) REFERENCES Player(ID)
        );
    """)
    # Make Tournament Table
    cursor.execute("""CREATE TABLE if NOT EXISTS Tournament (
    Name VARCHAR(40) PRIMARY KEY,
    Organizer CHAR(8) NOT NULL,
    n INT CHECK (n >= 0)
        );
    """)


def clearTuples(cursor):
    makeTable(cursor)

    cursor.execute("DELETE FROM Game;")

    cursor.execute("DELETE FROM Player;")
    
    cursor.execute("DELETE FROM Tournament;")

def enterPlayer(ID, Name, Rating, cursor,l):
    try:
        cursor.execute("""
            INSERT INTO player (ID, Name, Rating) 
            VALUES (%s, %s, %s);
        """, (ID, Name, Rating))

    except mysql.connector.errors.Error as err:
        print(",".join(map(str, l)) + " Input Invalid")

def enterGamePartial(Date, Time, Acidic, Alkaline, cursor, l):
    try:
        # SQL INSERT query
        query = "INSERT INTO Game (Date, Time, Acidic, Alkaline) VALUES (%s, %s, %s, %s)"
        
        # Tuple of values to be inserted
        values = (Date, Time, Acidic, Alkaline)

        # Execute the query with the values
        cursor.execute(query, values)

    except mysql.connector.Error as err:
        print(",".join(map(str, l)) + " Input Invalid")

def enterGame(Date, Time, Acidic, Alkaline, AcScore, AkScore, AcRating, AkRating, cursor, l):
    try:
        # Have to check if either player is already playing a game
        # Combine date and time into a single datetime string
        datetime_str = f"{Date} {Time}"

        # SQL query to check for prior game with missing attribute
        query1 = """
        SELECT *
        FROM Game
        WHERE (Acidic = %s OR Alkaline = %s)
        AND (AcScore IS NULL OR AkScore IS NULL OR AcRating IS NULL OR AkRating IS NULL)
        AND CONCAT(Date, ' ', Time) < %s;
        """
        # SQL query to check for prior game with missing attribute
        query2 = """
        SELECT *
        FROM Game
        WHERE (Acidic = %s OR Alkaline = %s)
        AND (AcScore IS NULL OR AkScore IS NULL OR AcRating IS NULL OR AkRating IS NULL)
        AND CONCAT(Date, ' ', Time) < %s;
        """

        # Execute the query with the player's ID and new game datetime as parameters
        cursor.execute(query1, (Acidic, Acidic, datetime_str))
        Acidic_exists = cursor.fetchall()
        cursor.execute(query2, (Alkaline, Alkaline, datetime_str))
        Alkaline_exists = cursor.fetchall()
    
        # Fetch all results
        if Acidic_exists or Alkaline_exists:
            print(",".join(map(str, l)) + " Input Invalid")
            return
        else:
            # SQL INSERT query
            query = "INSERT INTO Game (Date, Time, Acidic, Alkaline, AcScore, AkScore, AcRating, AkRating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            
            # Tuple of values to be inserted
            values = (Date, Time, Acidic, Alkaline, AcScore, AkScore, AcRating, AkRating)

            # Execute the query with the values
            cursor.execute(query, values)

            # Update player ratings based on the game outcome and if its later than all other games in the current database
            cursor.execute("UPDATE Player SET Rating = %s WHERE ID = %s", (AcRating, Acidic))
            cursor.execute("UPDATE Player SET Rating = %s WHERE ID = %s", (AkRating, Alkaline))

    except mysql.connector.Error as err:
        print(",".join(map(str, l)) + " Input Invalid")


def enterResults(Date, Time, Acidic, Alkaline, AcScore, AkScore, AcRating, AkRating, cursor, l):
    try:
        # SQL INSERT query
        query = """
        UPDATE Game
        SET AcScore = %s, AkScore = %s, AcRating = %s, AkRating = %s
        WHERE Acidic = %s AND Time = %s;"""
        
        # Tuple of values to be inserted
        values = (AcScore, AkScore, AcRating, AkRating, Acidic, Time)

        # Execute the query with the values
        cursor.execute(query, values)

        # Update player ratings based on the game outcome
        cursor.execute("UPDATE Player SET Rating = %s WHERE ID = %s", (AcRating, Acidic))
        cursor.execute("UPDATE Player SET Rating = %s WHERE ID = %s", (AkRating, Alkaline))

    except mysql.connector.Error as err:
        print(",".join(map(str, l)) + " Input Invalid")

def enterTourney(Name, Organizer, n, cursor, l):
    try:
        # SQL INSERT query
        query = "INSERT INTO Tournament (Name, Organizer, n) VALUES (%s, %s, %s)"
        
        # Tuple of values to be inserted
        values = (Name, Organizer, n)

        # Execute the query with the values
        cursor.execute(query, values)

        # Create new temporary table to store games
        cursor.execute("""
        CREATE TEMPORARY TABLE CurrentTourney (
        Tourney_name VARCHAR(40),
        Date DATETIME NOT NULL,
        Time INT(4) NOT NULL,
        Acidic CHAR(8) NOT NULL,
        Alkaline CHAR(8) NOT NULL,
        AcScore INT CHECK (AcScore BETWEEN 0 AND 10),
        AkScore INT CHECK (AkScore BETWEEN 0 AND 10),
        PRIMARY KEY (Tourney_name, Date, Time, Acidic)
        );"""
        )

    except mysql.connector.Error as err:
        print(",".join(map(str, l)) + " Input Invalid")

def enterGameTourney(Tourney_name, Date, Time, Acidic, Alkaline, AcScore, AkScore, cursor, l):
    try:
        # SQL INSERT query
        query = "INSERT INTO CurrentTourney (Tourney_name, Date, Time, Acidic, Alkaline, AcScore, AkScore) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        
        # Tuple of values to be inserted
        values = (Tourney_name, Date, Time, Acidic, Alkaline, AcScore, AkScore)

        # Execute the query with the values
        cursor.execute(query, values)

    except mysql.connector.Error as err:
        print(",".join(map(str, l)) + " Input Invalid")

def getPlayer(ID, cursor):
    try:
        # Define your dynamic queries and their parameters
        queries = [
            ("SELECT COUNT(*) FROM Game WHERE (Alkaline = %s OR Acidic = %s) AND AkScore IS NOT NULL ", (ID,ID)), # Grab total games
            ("SELECT (SELECT COUNT(*) FROM Game WHERE Acidic = %s AND AcScore > AkScore) + (SELECT COUNT(*) FROM Game WHERE Alkaline = %s AND AkScore > AcScore) AS wins", (ID,ID)), # Combined wins query
            ("SELECT (SELECT COUNT(*) FROM Game WHERE Acidic = %s AND AkScore = AcScore) + (SELECT COUNT(*) FROM Game WHERE Alkaline = %s AND AcScore = AkScore) AS draws", (ID,ID)), # Grab Draws
            ("SELECT (SELECT COUNT(*) FROM Game WHERE Acidic = %s AND AkScore > AcScore) + (SELECT COUNT(*) FROM Game WHERE Alkaline = %s AND AcScore > AkScore) AS losses", (ID,ID)) # Combined losses query
        ]
        results = []
        # manually execute first query
        cursor.execute("SELECT Name, Rating FROM Player WHERE ID = %s", (ID,)) # Grab name and rating from Player table)
        temp = cursor.fetchone()
        results.append(temp[0])
        results.append(temp[1])

        for query, params in queries:        
            try:
                cursor.execute(query, params)  # Use the parameters in the query
                result = cursor.fetchone()  # Fetch the first row from the executed query
                
                if result:
                    # If the query is for a COUNT, it will return a tuple (count,)   
                    count = result[0]
                    results.append(count)  # Append the count to results
                else:
                    results.append(0)  # If no result is found, append 0 (for safety)
            except mysql.connector.Error as err:
                print("None")
                return []
            
        # Format the result as a string like "Alice,1520.00,10,5,3,2"
        formatted_result = "{},{},{},{},{},{}".format(results[0], results[1], results[2], results[3], results[4], results[5])
        # print(results)
        print(formatted_result)

    except mysql.connector.Error as err:
        print("None")

def getTourney(Tourney_name, cursor):
    try:
        query = "SELECT * FROM CurrentTourney WHERE Tourney_name = %s"
        cursor.execute(query, (Tourney_name,))

        rows = cursor.fetchall()

        for row in rows:
            # Extract date
            date_str = row[1].strftime("%Y/%m/%d")

            cursor.execute("SELECT Name FROM Player WHERE ID = %s", (row[3],))
            name1 = cursor.fetchone()
            cursor.execute("SELECT Name FROM Player WHERE ID = %s", (row[4],))
            name2 = cursor.fetchone()

            # Convert 1200 format to HH:MM
            time_int = row[2]
            time_str = f"{time_int // 100:02}:{time_int % 100:02}"  # Converts 1200 → "12:00", 915 → "09:15"

            # Reformat into desired output
            formatted_output = f"{date_str},{time_str},{name1[0]},{row[3]},{name2[0]},{row[4]},{row[5]},{row[6]}"
            print(formatted_output)
            # print(row)
        

    except mysql.connector.Error as err:
        print("None")
def getGames(ID, ID2, cursor):
    try:
        query = """SELECT * 
        FROM Game
        WHERE (Acidic = %s AND Alkaline = %s) 
        OR (Acidic = %s AND Alkaline = %s)
        ORDER BY Date ASC, Time ASC;"""
        cursor.execute(query, (ID, ID2, ID, ID2))

        rows = cursor.fetchall()

        cursor.execute("SELECT Name FROM Player WHERE ID = %s", (ID,))
        name1 = cursor.fetchone()
        cursor.execute("SELECT Name FROM Player WHERE ID = %s", (ID2,))
        name2 = cursor.fetchone()

        for row in rows:
            # Extract date
            date_str = row[0].strftime("%Y/%m/%d")

            # Convert 1200 format to HH:MM
            time_int = row[1]
            time_str = f"{time_int // 100:02}:{time_int % 100:02}"  # Converts 1200 → "12:00", 915 → "09:15"

            # Reformat into desired output
            formatted_output = f"{date_str},{time_str},{name1[0]},{row[2]},{name2[0]},{row[3]},{row[4]},{row[5]}"
            print(formatted_output)
            # print(row)
        


    except mysql.connector.Error as err:
        print("None")

def getLeaderboard(Date1, Date2, cursor):
    try:
        query = """
        SELECT 
        p.ID AS Player_ID,
        p.Name AS Player_Name,
        COUNT(g.Date) AS Games_Played,
        SUM(CASE 
            WHEN (g.Acidic = p.ID AND g.AcScore > g.AkScore) OR (g.Alkaline = p.ID AND g.AkScore > g.AcScore) THEN 1 
            ELSE 0 
        END) AS Wins,
        SUM(CASE 
            WHEN (g.Acidic = p.ID AND g.AcScore = g.AkScore) OR (g.Alkaline = p.ID AND g.AcScore = g.AkScore) THEN 1 
            ELSE 0 
        END) AS Draws,
        SUM(CASE 
            WHEN (g.Acidic = p.ID AND g.AcScore < g.AkScore) OR (g.Alkaline = p.ID AND g.AkScore < g.AcScore) THEN 1 
            ELSE 0 
        END) AS Losses,
        (2 * SUM(CASE 
            WHEN (g.Acidic = p.ID AND g.AcScore > g.AkScore) OR (g.Alkaline = p.ID AND g.AkScore > g.AcScore) THEN 1 
            ELSE 0 
        END) + 
        1 * SUM(CASE 
            WHEN (g.Acidic = p.ID AND g.AcScore = g.AkScore) OR (g.Alkaline = p.ID AND g.AcScore = g.AkScore) THEN 1 
            ELSE 0 
        END)) AS Points
        FROM 
            Player p
        JOIN 
            Game g 
            ON g.Acidic = p.ID OR g.Alkaline = p.ID
        WHERE 
            g.Date BETWEEN %s AND %s
        GROUP BY 
            p.ID
        ORDER BY 
            Points DESC;"""


        # Execute the query with the parameterized inputs
        cursor.execute(query, (Date1, Date2))

        # Fetch the results
        results = cursor.fetchall()

        for row in results:
            formatted_output = ','.join(map(str, row))
            print(formatted_output)

        


    except mysql.connector.Error as err:
        print("None")

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve values
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    try:
        # Establish connection
        conn = mysql.connector.connect(
            host="localhost",      # Change if needed
            user=db_user,  # Replace with your MySQL username
            password=db_password,  # Replace with your MySQL password
            database="dbprog",   # Replace with your database name
        )
    except mysql.connector.errors.Error as err:
        print(f"Database connection error: {err}")
        return

    # Create a cursor object
    cursor = conn.cursor()

    # Grab filename
    user_input = input("Enter the filename: ")
    try:
        # loop through each line of the file
        with open(user_input + ".txt", "r", newline="") as file:
            reader = csv.reader(file)
            inTourney = False
            gamesLeft = 0
            TourneyName= ""
            for row in reader:
                original_line = row
                Arr = []
                for item in row:
                    Arr.append(item)
                
                # print(Arr)
                # find correct statement
                if Arr[0] == 'e':
                    if not inTourney:
                        makeTable(cursor)
                elif Arr[0] == 'c':
                    if not inTourney:
                        clearTuples(cursor)
                elif Arr[0] == 'p':
                    enterPlayer(Arr[1],Arr[2],Arr[3], cursor, original_line)
                    conn.commit()
                elif Arr[0] == 'g':
                    if len(Arr) <= 5:
                        enterGamePartial(Arr[1],Arr[2],Arr[3],Arr[4], cursor, original_line)
                        conn.commit()
                    else:
                        enterGame(Arr[1],Arr[2],Arr[3],Arr[4],Arr[5],Arr[6],Arr[7],Arr[8], cursor, original_line)
                        conn.commit()

                    # check for tourney and update variables
                    if inTourney:
                        enterGameTourney(TourneyName, Arr[1],Arr[2],Arr[3],Arr[4],Arr[5],Arr[6], cursor, original_line)
                        gamesLeft = gamesLeft - 1
                        if gamesLeft == 0:
                            inTourney = False
                elif Arr[0] == 'r':
                    enterResults(Arr[1],Arr[2],Arr[3],Arr[4],Arr[5],Arr[6],Arr[7],Arr[8], cursor, original_line)
                    conn.commit()
                elif Arr[0] == 't':
                    if not inTourney:
                        enterTourney(Arr[1],Arr[2],Arr[3], cursor, original_line)
                        TourneyName = Arr[1]
                        inTourney = True
                        gamesLeft = int(Arr[3])
                        conn.commit()
                elif Arr[0] == 'P':
                    getPlayer(Arr[1], cursor)
                elif Arr[0] == 'T':
                    getTourney(Arr[1], cursor)
                elif Arr[0] == 'H':
                    getGames(Arr[1],Arr[2], cursor)
                elif Arr[0] == 'D':
                    getLeaderboard(Arr[1],Arr[2], cursor)
    except FileNotFoundError:
        print(f"File not found: {user_input}")
        return
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
        
