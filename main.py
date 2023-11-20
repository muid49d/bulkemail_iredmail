import mysql.connector
import csv
import bcrypt

# Database credentials
host = "localhost"  # usually 'localhost' or an IP address
user = "vmailadmin"
password = "your_password"
database = "vmail"  # iRedMail uses 'vmail' by default

# Connect to the iRedMail database
cnx = mysql.connector.connect(host=host, user=user, password=password, database=database)
cursor = cnx.cursor()

# Path to your CSV file
csv_file_path = 'random_user_list_ticktok_top_user200.csv'

# Read the CSV file
with open(csv_file_path, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        email = row['email']
        plain_password = row['password']
        first_name = row['first_name']
        last_name = row['last_name']        


        # iRedMail uses the domain part to associate mailboxes, extract domain from email
        domain = email.split('@')[-1]

        # Encrypt the password using bcrypt
        encrypted_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # SQL command to insert the user
        # Note: The SQL fields (username, password, name, domain, etc.) should match your database schema
        sql = ("INSERT INTO mailbox (username, password, name, domain) "
               "VALUES (%s, %s, %s, %s)")
        values = (email, encrypted_password, f"{first_name} {last_name}", domain)

        # Execute the SQL command
        cursor.execute(sql, values)

# Commit changes and close the connection
cnx.commit()
cursor.close()
cnx.close()
