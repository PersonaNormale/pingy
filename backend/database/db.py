import mariadb
from dotenv import dotenv_values

class DataBase:
	# Init dove stabilisce una connessione con il server e crea il database con le tabelle
	def __init__(self, user, password, database, host, port):
		try:
			connection = mariadb.connect(
				user=user,
				password=password,
				database=database,
				host=host,
				port=port,
			)

			cursor = connection.cursor()

			cursor.execute("""
		  		--sql
				CREATE TABLE IF NOT EXISTS urls(
					id INT NOT NULL AUTO_INCREMENT,
		  			PRIMARY KEY(id),
					url VARCHAR(100) NOT NULL,
		  			timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
				);
			""")

			cursor.execute("""
		  		--sql
				CREATE TABLE IF NOT EXISTS pings(
					id INT NOT NULL AUTO_INCREMENT,
		  			PRIMARY KEY (id),
		  			url_id INT,
		  			FOREIGN KEY (url_id) REFERENCES urls(id),
		  			timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		  			response_time INT
				);
			""")

			connection.commit()
			connection.close()
		except mariadb.Error as e:
			print(f"An error occured with the database: {e}")

		try:
			self.connection = mariadb.connect(
				user=user,
				password=password,
				host=host,
				port=port,
				database="pingy_db"
			)
		except mariadb.Error as e:
			print(f"An error occured connecting to database: {e}")

	def add_url(self, url):
		try:
			cursor = self.connection.cursor()
			
			cursor.execute("INSERT INTO urls (url) VALUES (?)", (url,))

			self.connection.commit()

			cursor.close()
		except mariadb.Error as e:
			print(f"An error occured with database: {e}")

	def add_ping(self, url, time, response_time):
		try:
			cursor = self.connection.cursor()
			
			cursor.execute("SELECT id FROM urls WHERE url = ?", (url,))
			result = cursor.fetchone()

			if result is not None:
				url_id = result[0]

				cursor.execute("""
					--sql
					INSERT INTO pings (url_id, response_time, timestamp) VALUES (?,?,?);)
				""", (url_id, response_time, time))

				self.connection.commit()

				cursor.close()
		except mariadb.Error as e:
			print(f"An error occured with database: {e}")

	def remove_url(self, url):
		try:
			cursor = self.connection.cursor()
			
			cursor.execute("SELECT id FROM urls WHERE URL = ?", (url,))
			result = cursor.fetchone()

			if result is not None:
				url_id = result[0]
				query = """
					--sql
					DELETE FROM pings WHERE url_id = ?;
				"""
				
				cursor.execute(query, (url_id,))

				query = """
					--sql
					DELETE FROM urls WHERE url_id = ?;
				"""

				cursor.execute(query, (url_id,))

				self.connection.commit()

				cursor.close()
		except mariadb.Error as e:
			print(f"An error occured with database: {e}")

	def fetch_urls(self):
		try:
			cursor = self.connection.cursor()

			cursor.execute("SELECT url, timestamp FROM urls;")

			result = cursor.fetchall()

			cursor.close()

			return result
		except mariadb.Error as e:
			print(f"An error occured with database: {e}")

	def fetch_url_timestamp(self, url):
		try:
			cursor = self.connection.cursor()

			cursor.execute("SELECT timestamp FROM urls WHERE url = ?;", (url,))

			result = cursor.fetchone()

			cursor.close()

			return result[0]
		except mariadb.Error as e:
			print(f"An error occured with database: {e}")		

	def fetch_pings(self, url):
		try:
			cursor = self.connection.cursor()

			cursor.execute("SELECT id FROM urls WHERE url = ?;", (url,))

			result = cursor.fetchone()

			cursor.execute("SELECT timestamp, response_time FROM pings WHERE url_id = ?;" (url,))

			result = cursor.fetchall()

			cursor.close()

			return result
		except mariadb.Error as e:
			print(f"An error occured with database: {e}")	
