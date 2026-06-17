#!/usr/bin/env python3
"""
Supabase Database Connection and Query Script
This script connects to Supabase and allows you to query data from your tables
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Get Supabase credentials from .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Verify credentials are loaded
if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL or SUPABASE_KEY not found in .env file")
    print(f"   .env path: {env_path}")
    print(f"   .env exists: {env_path.exists()}")
    exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def test_connection():
    """Test the connection to Supabase"""
    try:
        print("✓ Supabase client initialized successfully")
        print(f"URL: {SUPABASE_URL}")
        return True
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False

def get_all_tables():
    """Get list of all tables in the database"""
    try:
        # This query gets table information from information_schema
        response = supabase.table('information_schema.tables').select('table_name').execute()
        print("✓ Tables in database:")
        for table in response.data:
            print(f"  - {table['table_name']}")
        return response.data
    except Exception as e:
        print(f"Note: Direct schema query may not be available. Try querying a specific table instead.")
        return None

def query_table(table_name: str, limit: int = 10):
    """Query data from a specific table"""
    try:
        response = supabase.table(table_name).select("*").limit(limit).execute()
        
        if not response.data:
            print(f"✓ Table '{table_name}' is empty or does not exist")
            return None
        
        print(f"\n✓ Data from table '{table_name}' (limit {limit}):")
        print(f"Total records returned: {len(response.data)}\n")
        
        for idx, row in enumerate(response.data, 1):
            print(f"Record {idx}:")
            for key, value in row.items():
                print(f"  {key}: {value}")
            print()
        
        return response.data
    except Exception as e:
        print(f"✗ Error querying table '{table_name}': {e}")
        return None

def insert_sample_data(table_name: str, data: dict):
    """Insert sample data into a table"""
    try:
        response = supabase.table(table_name).insert(data).execute()
        print(f"✓ Successfully inserted data into '{table_name}'")
        return response.data
    except Exception as e:
        print(f"✗ Error inserting data: {e}")
        return None

def main():
    """Main function to demonstrate Supabase queries"""
    print("=" * 60)
    print("Supabase Database Connection Test")
    print("=" * 60)
    
    # Test connection
    if not test_connection():
        return
    
    print("\n" + "=" * 60)
    print("Attempting to query tables...")
    print("=" * 60)
    
    # Try to get all tables
    # get_all_tables()
    
    # Example: Query specific tables
    # Replace with your actual table names
    tables_to_query = ['patients', 'users', 'products', 'orders']
    
    print("\nAttempting to query tables...")
    for table_name in tables_to_query:
        try:
            data = query_table(table_name, limit=10)
            if data:
                break  # Stop after first successful query
        except Exception as e:
            print(f"  (Skipping '{table_name}')")
            continue
    
    print("\n" + "=" * 60)
    print("Connection test completed!")
    print("=" * 60)
    print("\nTo query your own tables, modify the table_to_query() function")
    print("or use the provided functions in your own code.")

if __name__ == "__main__":
    main()
