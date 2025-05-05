def create_query(table,columns: list):
    if(table == "Post"):
        conn = None
        try:
            conn = create_db_connection()
            cursor = conn.cursor(dictionary=True)
            users = ["Username", "Soc_Med", "Name", "Verified", "Country_Birth", "Country_Res", "Age", "Gender"]
            post = ["Username", "Soc_Med", "Time_Posted", "City", "State", "Country", "Multimedia", "Likes", "Dislikes", "Text", "Poster_OG", "Time_OG"]
            project = ["Name", "Manager", "Institute", "Start_Date", "End_Date"]
            record =["Project", "Text", "Fields", "Username", "Time_Posted", "Soc_Med"]
            
            query = """
                SELECT *
                FROM %s
                WHERE 1=1
                """
            parameters = []
            parameters.append(table)
            for i in range(0,columns.count):
                    if columns[i] != "":
                        if(table=="Users"):
                            parameters.append(users[i])
                        elif(table=="Post"):
                            parameters.append(post[i])
                        elif(table=="Project"):
                            parameters.append(project[i])
                        elif(table=="Record"):
                            parameters.append(record[i])
                        parameters.append(columns[i])
                        query+="AND %s = %s"

            cursor.execute(query, parameters)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Error querying posts: {e}")
            return []
        finally:
            if conn:
                conn.close()


        
    # elif(table == "User"):
    #     query = """
    #         SELECT *
    #         FROM User
    #         WHERE 1=1
    #         """
    #     if parameters[0] != "":
    #         query += "AND "
                
            
    # elif(table == "Project"):
    #     query = """
    #         SELECT *
    #         FROM Project
    #         WHERE 
    #         """
    # elif(table == "Record"):
    #     query = """
    #         SELECT *
    #         FROM Record
    #         WHERE 
    #         """
    
