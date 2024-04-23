import psycopg2

def create_connection():
    try:
        connection = psycopg2.connect(
            dbname="chatApp",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432" 
        )
        print("Connected to database!")
        return connection
    except psycopg2.Error as e:
        print("Unable to connect to the database:", e)
        return None

def connect_users(chat_id, sender, recipient, connection):
    cursor = connection.cursor()
    sender, recipient = sorted([sender, recipient])
    
    cursor.execute("SELECT COUNT(*) FROM user_relation WHERE sender = %s AND recipient = %s AND conn_id = %s", (sender, recipient, chat_id))
    count = cursor.fetchone()[0]
    
    if count == 0:
        cursor.execute("INSERT INTO user_relation (sender, recipient, conn_id) VALUES (%s, %s, %s)", (sender, recipient, chat_id))
        print("New connection created successfully")
    else:
        print("Connection already exists")


def insert_message(chat_id, sender, recipient, timestamp, content):
    try:
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO chat (chat_id, sender, recipient, timestamp, status, content) VALUES (%s, %s, %s, %s, %s, %s)", (chat_id, sender, recipient, timestamp, False, content))

        cursor.execute("SELECT COUNT(*) FROM user_relation WHERE sender = %s AND recipient = %s AND conn_id = %s", (sender, recipient, chat_id))
        count = cursor.fetchone()[0]
        
        if count == 0:
            connect_users(chat_id, sender, recipient, connection)
        
        connection.commit()
        print("Message inserted successfully!")
    except psycopg2.Error as error:
        connection.rollback()
        print("Error inserting message:", error)
    finally:
        cursor.close()


def add_user(user_id, username):
    try:
        cursor = connection.cursor()

        cursor.execute("INSERT INTO persons (user_id, username) VALUES (%s, %s)", (user_id, username))
        
        connection.commit()
        print("User added successfully!")
    except psycopg2.Error as error:
        connection.rollback()
        print("Error adding user:", error)
    finally:
        cursor.close()

def user_exists(username):
    try:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM persons WHERE username = %s", (username,))
        count = cursor.fetchone()[0]

        return count > 0
    except psycopg2.Error as error:
        print("Error checking user existence:", error)
        return False
    finally:
        cursor.close()

def print_by_chat_id(chat_id, order):
    try:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM chat WHERE chat_id = %s ORDER BY timestamp " + order, (chat_id,))
        
        rows = cursor.fetchall()

        if rows:
            print("Messages for chat_id", chat_id)
            for row in rows:
                print(row)
        else:
            print("No messages found for chat_id", chat_id)

    except psycopg2.Error as error:
        print("Error retrieving messages:", error)
    finally:
        cursor.close()
def delete_account(username):
    try:
        cursor = connection.cursor()

        cursor.execute("DELETE FROM chat WHERE sender = %s OR recipient = %s", (username, username))

        cursor.execute("DELETE FROM user_relation WHERE sender = %s OR recipient = %s", (username, username))

        cursor.execute("DELETE FROM persons WHERE username = %s", (username,))

        connection.commit()
        print("Account for user", username, "deleted successfully!")
    except psycopg2.Error as error:
        connection.rollback()
        print("Error deleting account:", error)
    finally:
        cursor.close()


def delete_contact(chat_id):
    try:
        cursor = connection.cursor()

        cursor.execute("SELECT sender, recipient FROM chat WHERE chat_id = %s", (chat_id,))
        sender, recipient = cursor.fetchone()

        cursor.execute("DELETE FROM chat WHERE chat_id = %s", (chat_id,))
        cursor.execute("DELETE FROM user_relation WHERE sender = %s AND recipient = %s", (sender, recipient))
        connection.commit()
        print("Messages for chat_id", chat_id, "deleted successfully!")
    except psycopg2.Error as error:
        connection.rollback()
        print("Error deleting messages:", error)
    finally:
        cursor.close()

def update_status(chat_id, timestamp):
    try:
        cursor = connection.cursor()

        cursor.execute("UPDATE chat SET status = %s WHERE chat_id = %s AND timestamp = %s", (True, chat_id, timestamp))
        
        connection.commit()
        print("Status updated successfully for chat_id", chat_id, "and timestamp", timestamp)
    except psycopg2.Error as error:
        connection.rollback()
        print("Error updating status:", error)
    finally:
        cursor.close()




connection = create_connection()
if connection:
    delete_contact("00001")
    
    connection.close()
