"""
Example usage of Supabase database connection
This file shows how to use the database module in your application
"""

from supabase_db import db

def example_basic_queries():
    """Basic query examples"""
    
    # Example 1: Select all records from a table
    # users = db.select('users', limit=10)
    # print("All users:", users)
    
    # Example 2: Select specific columns
    # users = db.select('users', columns='id,name,email', limit=5)
    # print("User IDs and names:", users)
    
    # Example 3: Select with WHERE clause
    # user = db.select_where('users', 'id', 1)
    # print("User with ID 1:", user)
    
    # Example 4: Insert a record
    # new_user = db.insert('users', {
    #     'name': 'John Doe',
    #     'email': 'john@example.com',
    #     'age': 30
    # })
    # print("Inserted user:", new_user)
    
    # Example 5: Insert multiple records
    # users_data = [
    #     {'name': 'Alice', 'email': 'alice@example.com', 'age': 25},
    #     {'name': 'Bob', 'email': 'bob@example.com', 'age': 28},
    # ]
    # inserted = db.insert_many('users', users_data)
    # print("Inserted records:", inserted)
    
    # Example 6: Update a record
    # updated = db.update('users', {'age': 31}, 'id', 1)
    # print("Updated user:", updated)
    
    # Example 7: Delete a record
    # deleted = db.delete('users', 'id', 1)
    # print("Deleted:", deleted)
    
    pass

def test_table(table_name: str):
    """Test a specific table by querying first 5 records"""
    print(f"\nQuerying table: {table_name}")
    print("-" * 50)
    
    data = db.select(table_name, limit=5)
    
    if data:
        print(f"✓ Found {len(data)} record(s)")
        for idx, record in enumerate(data, 1):
            print(f"\nRecord {idx}:")
            for key, value in record.items():
                print(f"  {key}: {value}")
    else:
        print(f"✗ Table '{table_name}' is empty or doesn't exist")

if __name__ == "__main__":
    print("=" * 50)
    print("Supabase Database Examples")
    print("=" * 50)
    
    # Uncomment the table names you want to test
    # test_table('users')
    # test_table('products')
    # test_table('orders')
    
    # Or run the examples above
    example_basic_queries()
    
    print("\n✓ Ready to use! Uncomment examples to test your tables.")
