import os
import psycopg2
from pymongo import MongoClient
from DatabaseTypeEnum import DatabaseTypeEnum

class DatabaseHelper:
    def __init__(self):

        self.connection = None
        self.client = None

        db_type_str = os.getenv("DB_TYPE", "").upper()

        if db_type_str == DatabaseTypeEnum.MONGODB.value :
            self.db_type = DatabaseTypeEnum.MONGODB
            self._connect_mongodb()
        elif db_type_str == DatabaseTypeEnum.POSTGRESQL.value:
            self.db_type = DatabaseTypeEnum.POSTGRESQL
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
        db_user = os.getenv("DB_USER","postgres")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "2003")
        db_name = os.getenv("DB_NAME", "HR-Database")

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

        if self.db_type == DatabaseTypeEnum.MONGODB and self.client:
            self.client.close()
        elif self.db_type == DatabaseTypeEnum.POSTGRESQL and self.connection:
            self.connection.close()
            self.connection = None
        print("🔌 Connection closed")


    def execute_mongo_query(self, collection_name, operation, data=None, filter_query=None, update_data=None):
        # Ensure the database type is MongoDB
        if self.db_type != DatabaseTypeEnum.MONGODB:
            raise Exception("❌ This operation is only supported for MongoDB.")

        # Check if the MongoDB connection is established
        if self.client is None or self.db is None:
            raise Exception("❌ MongoDB connection is not established.")

        try:
            # Access the collection
            collection = self.db[collection_name]

            # Supported operations
            if operation == "insert":
                # Insert one or multiple documents
                if isinstance(data, list):
                    result = collection.insert_many(data)
                    print(f"✅ Inserted {len(result.inserted_ids)} documents.")
                    return result.inserted_ids
                else:
                    result = collection.insert_one(data)
                    print(f"✅ Inserted document with ID: {result.inserted_id}.")
                    return result.inserted_id

            elif operation == "find":
                # Retrieve documents based on the filter query
                filter_query = filter_query or {}
                result = list(collection.find(filter_query))
                print(f"✅ Found {len(result)} documents.")
                return result

            elif operation == "update":
                # Update documents based on the filter query
                if not update_data:
                    raise ValueError("❌ 'update_data' must be provided for 'update' operation.")
                result = collection.update_many(filter_query, {"$set": update_data})
                print(f"✅ Updated {result.modified_count} documents.")
                return {"matched_count": result.matched_count, "modified_count": result.modified_count}

            elif operation == "delete":
                # Delete documents based on the filter query
                result = collection.delete_many(filter_query)
                print(f"✅ Deleted {result.deleted_count} documents.")
                return {"deleted_count": result.deleted_count}

            else:
                raise ValueError(f"❌ Unsupported operation: {operation}.")

        except Exception as e:
            print(f"❌ MongoDB operation failed: {e}")
            return None