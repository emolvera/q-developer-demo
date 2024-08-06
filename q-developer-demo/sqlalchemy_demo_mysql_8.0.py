import os
import ast
import boto3
from botocore.exceptions import ClientError
import sqlalchemy as db
from sqlalchemy.sql import text

# Global variables
from variables import secret_name_8_0 as secret_name, db_host_8_0 as db_host, db_port, db_name

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

	# Try SQL commands
	try:
		# Drop table if exists
		sql = '''
				DROP TABLE IF EXISTS demo_table;
		'''
		result = conn.execute(text(sql))

		# List all tables in database
		sql = '''
				SHOW TABLES;
		'''
		result = conn.execute(text(sql))

		print('\nListing all tables in database...')
		for table in result:
				print(table[0])

		# Create table
		print('\nCreating table...')
		sql = '''
				CREATE TABLE IF NOT EXISTS `demo_table` (
						`id` INT(11) NOT NULL AUTO_INCREMENT,
						`item` VARCHAR(45) DEFAULT NULL,
						`date` DATE DEFAULT NULL,
						PRIMARY KEY (`id`)
				) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8mb4 COLLATE=utf8mb4_general_ci;
		'''
		result = conn.execute(text(sql))

		# Insert zero date items in table
		sql = '''
				INSERT INTO demo_table (item, date)
				VALUES ('item_1', NULL)
						, ('item_2', NULL)
						, ('item_3', NULL);
		'''
		result = conn.execute(text(sql))

		# Preview table
		sql = '''
				SELECT *
				FROM demo_table
				LIMIT 10;
		'''
		result = conn.execute(text(sql))

		print('\nPreviewing table...')
		for item in result:
				print(item)

		# Select items where date is empty
		sql = '''
				SELECT id, item
				FROM demo_table
				WHERE date IS NULL;
		'''
		result = conn.execute(text(sql))

		print('\nListing items where date is empty...')
		for item in result:
				print(item)

		# Show warnings
		sql = '''
				SHOW WARNINGS;
		'''
		result = conn.execute(text(sql))
		print('\nWarnings...', result.fetchall())

	# Catch errors
	except db.exc.SQLAlchemyError as e:
		print('\nError occurred:', e)

	finally:
		engine.dispose()


# Main function
if __name__ == "__main__":
    main()
