from langchain_community.utilities.sql_database import SQLDatabase

db = SQLDatabase.from_uri(database_uri='mysql+pymysql://root:root@localhost:3306/hospital_db')
