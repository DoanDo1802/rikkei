"""
Supabase Database Utility Module
Provides a simple interface for database operations
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class SupabaseDB:
    """Database connection wrapper for Supabase"""
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client: Client = create_client(self.url, self.key)
    
    def select(self, table: str, columns: str = "*", limit: int = 100):
        """
        Select data from a table
        
        Args:
            table: Table name
            columns: Columns to select (default: "*" for all)
            limit: Maximum number of rows (default: 100)
        
        Returns:
            List of rows or None if error
        """
        try:
            response = self.client.table(table).select(columns).limit(limit).execute()
            return response.data
        except Exception as e:
            print(f"Error selecting from {table}: {e}")
            return None
    
    def select_where(self, table: str, column: str, value, columns: str = "*"):
        """
        Select data with a WHERE clause
        
        Args:
            table: Table name
            column: Column to filter by
            value: Value to match
            columns: Columns to select (default: "*" for all)
        
        Returns:
            List of matching rows or None if error
        """
        try:
            response = self.client.table(table).select(columns).eq(column, value).execute()
            return response.data
        except Exception as e:
            print(f"Error querying {table}: {e}")
            return None
    
    def insert(self, table: str, data: dict):
        """
        Insert a single row
        
        Args:
            table: Table name
            data: Dictionary of column-value pairs
        
        Returns:
            Inserted row or None if error
        """
        try:
            response = self.client.table(table).insert(data).execute()
            return response.data
        except Exception as e:
            print(f"Error inserting into {table}: {e}")
            return None
    
    def insert_many(self, table: str, data: list):
        """
        Insert multiple rows
        
        Args:
            table: Table name
            data: List of dictionaries
        
        Returns:
            Inserted rows or None if error
        """
        try:
            response = self.client.table(table).insert(data).execute()
            return response.data
        except Exception as e:
            print(f"Error inserting into {table}: {e}")
            return None
    
    def update(self, table: str, data: dict, filter_column: str, filter_value):
        """
        Update rows
        
        Args:
            table: Table name
            data: Dictionary of columns to update
            filter_column: Column to filter by
            filter_value: Value to match
        
        Returns:
            Updated rows or None if error
        """
        try:
            response = self.client.table(table).update(data).eq(filter_column, filter_value).execute()
            return response.data
        except Exception as e:
            print(f"Error updating {table}: {e}")
            return None
    
    def delete(self, table: str, filter_column: str, filter_value):
        """
        Delete rows
        
        Args:
            table: Table name
            filter_column: Column to filter by
            filter_value: Value to match
        
        Returns:
            Result or None if error
        """
        try:
            response = self.client.table(table).delete().eq(filter_column, filter_value).execute()
            return response.data
        except Exception as e:
            print(f"Error deleting from {table}: {e}")
            return None

# Initialize global database instance
db = SupabaseDB()

# Example usage
if __name__ == "__main__":
    # Test connection
    print("Testing Supabase connection...")
    
    # Example: Get all users (replace 'users' with your table name)
    # users = db.select('users', limit=10)
    # if users:
    #     print(f"Found {len(users)} users:")
    #     for user in users:
    #         print(user)
    
    print("✓ Database utility module loaded successfully")
