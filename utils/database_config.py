import os
import psycopg2
from pymongo import MongoClient
from enum import Enum, auto

class DatabaseType(Enum):
    POSTGRESQL = auto()
    MONGODB = auto()

class DatabaseHelper:
    def __init__(self):

        self.connection = None
        self.client = None

        db_type_str = os.getenv("DB_TYPE", "").upper()

        if db_type_str == "MONGODB" :
            self.db_type = DatabaseType.MONGODB
            self._connect_mongodb()
        elif db_type_str == "POSTGRESQL" :
            self.db_type = DatabaseType.POSTGRESQL
            self._connect_postgresql()
        else:
            raise ValueError("❌ Could not detect database type. Please set `DB_TYPE`.")

    def _connect_mongodb(self):
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        try:
            self.client = MongoClient(mongo_uri)
            self.db = self.client.get_database()
            print(f"✅ Connected to MongoDB")
        except Exception as e:
            raise Exception(f"❌ MongoDB connection error: {e}")

    def _connect_postgresql(self):
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "2003")
        db_name = os.getenv("DB_NAME", "postgres")

        if not all([db_user, db_password, db_host, db_port, db_name]):
            raise ValueError("❌ Missing PostgreSQL configuration in environment variables.")

        try:
            self.connection = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            self.connection.autocommit = False
            print(f"✅ Connected to PostgreSQL [{db_name}]")
        except Exception as e:
            raise Exception(f"❌ PostgreSQL connection error: {e}")

    def execute_query(self, query, params=None, fetch=False):

        if self.connection is None:
            raise Exception("❌ No active database connection!")

        session = self.connection.cursor()
        try:
            session.execute(query, params or ())
            if fetch:
                return session.fetchall()
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"⚠️ Query execution failed: {e}")
            return []
        finally:
            session.close()

    def close(self):

        if self.db_type == DatabaseType.MONGODB and self.client:
            self.client.close()
        elif self.db_type == DatabaseType.POSTGRESQL and self.connection:
            self.connection.close()
            self.connection = None
        print("🔌 Connection closed")
