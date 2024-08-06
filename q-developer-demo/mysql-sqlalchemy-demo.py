import os
import ast
import boto3
from botocore.exceptions import ClientError
import sqlalchemy as db
from sqlalchemy.sql import text

# Global variables
secret_name = "rds!cluster-2d4c782c-f990-4538-a230-2984f61788f0"
db_host = 'aurora-mysql-5-7-instance-1.cykxuprqcxvu.us-east-1.rds.amazonaws.com'
db_port = '3306'
db_name = ''

# Function to retrieve secret from Secrets Manager
def get_secret(secret_name):

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-east-1'
    )

    # Retrieve the secret value
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        secret_value = get_secret_value_response['SecretString']
        secret_dict = ast.literal_eval(secret_value)
        return secret_dict
    except ClientError as e:
        print("Error occurred:", e)

# Function to connect to the database
def connect_to_db(db_username, db_password, db_host, db_port, db_name):
  
  # Construct the SQLAlchemy engine URL
  engine_url = db.engine.URL.create(
      drivername='mysql+pymysql',
      username=db_username,
      password=db_password,
      host=db_host,
      port=db_port,
      database=db_name
  )

  # Create the SQLAlchemy engine and connection
  engine = db.create_engine(engine_url)
  conn = engine.connect()
  return engine, conn


# Main function
def main():

  # Get the database credentials
  secret = get_secret(secret_name)
  
  # Extract the database credentials from the secret
  db_username = secret['username']
  db_password = secret['password']
  
  # Connect to the database
  engine, conn = connect_to_db(db_username, db_password, db_host, db_port, db_name)

  # Run SQL commands
  try:
      # List all databases
      print('Listing all databases:')
      tables = conn.execute(text('SHOW DATABASES;'))
      for table in tables:
          print(table[0])

      # Use the database
      conn.execute(text('USE q_dev_database;'))
      print('Using table q_dev_database.')

      # Create a new table
      items = conn.execute(text('''
          SELECT *
          FROM new_table
          LIMIT 10;
      '''))
      for item in items:
          print(item)

      '''
      # Insert some data into the new table
      conn.execute('INSERT INTO new_table (text_column) VALUES ('Hello'), ('World')')

      # Select the first 10 rows from the new table
      result = conn.execute('SELECT * FROM new_table LIMIT 10')
      print('\nFirst 10 rows from 'new_table':')
      for row in result:
          print(row)
      '''

  except db.exc.SQLAlchemyError as e:
      print('Error occurred:', e)

  finally:
      engine.dispose()


# Main function
if __name__ == "__main__":
    main()

