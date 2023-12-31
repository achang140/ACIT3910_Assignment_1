import mysql.connector 

host = input("What host to connect to (localhost): ")
port = input("What port to connect to (3306): ")
user = input("What user to connect with (root): ")
password = input("What password to connect with: ")

try:
    db = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        auth_plugin="mysql_native_password"
    )

    if db.is_connected():
        print("Connected Successfully.")

        cursor = db.cursor()

        cursor.execute("SELECT VERSION()"); 
        mysql_version = cursor.fetchone()[0]
        print(f"('version', '{mysql_version}')")

        cursor.execute("USE dictionary;")

        input_word = input("What word do you want to add/change: ")

        cursor.execute("SELECT * FROM word WHERE word = %s", (input_word, )); 
        results = cursor.fetchall()

        if results:
            print(f'Found {input_word} in the database.')
            for row in results:
                print(row)
            
            input_change_word = input(f"Change '{input_word}' to: ")
            cursor.execute("UPDATE word SET word = %s WHERE word = %s", (input_change_word, input_word)); 
            db.commit()
            if cursor.rowcount > 0:
                print(f"Changed '{input_word}' to '{input_change_word}' in the database")
        else:
            print(f"The word '{input_word}' was not found... adding")
            cursor.execute("INSERT INTO word (word) VALUES (%s)", (input_word, )); 
            db.commit()
            if cursor.rowcount > 0:
                print(f"Added '{input_word}' to the database")

except mysql.connector.Error as err:
    if "Access denied for user" in str(err):
        print("Could not login to host with user/password provided.")
        print("Existing.")
    else:
        print(err)
    exit()

finally:
    if 'db' in locals() and db.is_connected():
        db.close()