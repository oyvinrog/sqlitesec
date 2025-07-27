#!/usr/bin/env python3
"""
Unit tests for SqliteSec - SQLite database encryption/decryption library.
"""

import unittest
import os
from sqlitesec import SqliteSec


class TestSqliteSec(unittest.TestCase):
    """Test cases for SqliteSec functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Use a temporary database file for testing
        self.db_path = 'test.db'
        
        # Remove test database if it exists from previous runs
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            
        # 16-byte key for testing (AES-128)
        self.key = b'test_key_1234567890123456'
        self.sqlitesec = SqliteSec(self.key)

    def test_connection(self):
        """Test if the database connection is established and closed properly."""
        conn = self.sqlitesec.connect(self.db_path)
        self.assertIsNotNone(conn, "Database connection should not be None")
        
        # Close the connection
        self.sqlitesec.close(conn, self.db_path)
        
        # Check if file exists after closing (should be encrypted)
        self.assertTrue(os.path.exists(self.db_path), 
                       "Database file should exist after closing")

    def test_encryption_decryption(self):
        """Test if data is correctly encrypted and decrypted."""
        # Connect and insert test data
        conn = self.sqlitesec.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create a table and insert data
        cursor.execute('CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, data TEXT)')
        test_data = 'Hello, world!'
        cursor.execute('INSERT INTO test (data) VALUES (?)', (test_data,))
        conn.commit()
        self.sqlitesec.close(conn, self.db_path)
        
        # Reconnect and verify data persistence
        conn = self.sqlitesec.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT data FROM test WHERE id=1')
        result = cursor.fetchone()
        
        self.assertIsNotNone(result, "Query should return a result")
        fetched_data = result[0]
        print(f"Data fetched from database: {fetched_data}")
        
        self.assertEqual(fetched_data, test_data, 
                        "Fetched data should match the original data")
        self.sqlitesec.close(conn, self.db_path)

    def test_multiple_operations(self):
        """Test multiple database operations with encryption/decryption."""
        conn = self.sqlitesec.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table and insert multiple records
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)')
        test_users = [
            ('Alice', 'alice@example.com'),
            ('Bob', 'bob@example.com'),
            ('Charlie', 'charlie@example.com')
        ]
        
        cursor.executemany('INSERT INTO users (name, email) VALUES (?, ?)', test_users)
        conn.commit()
        self.sqlitesec.close(conn, self.db_path)
        
        # Reconnect and verify all data
        conn = self.sqlitesec.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT name, email FROM users ORDER BY id')
        results = cursor.fetchall()
        
        self.assertEqual(len(results), 3, "Should have 3 user records")
        for i, (name, email) in enumerate(results):
            expected_name, expected_email = test_users[i]
            self.assertEqual(name, expected_name, f"Name mismatch for user {i+1}")
            self.assertEqual(email, expected_email, f"Email mismatch for user {i+1}")
        
        self.sqlitesec.close(conn, self.db_path)

    def test_different_key_fails(self):
        """Test that using a different key fails to decrypt the database."""
        # Create database with original key
        conn = self.sqlitesec.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS secret (data TEXT)')
        cursor.execute('INSERT INTO secret (data) VALUES (?)', ('secret_data',))
        conn.commit()
        self.sqlitesec.close(conn, self.db_path)
        
        # Try to access with different key
        wrong_key = b'wrong_key_1234567890123456'
        wrong_sqlitesec = SqliteSec(wrong_key)
        
        # This should either fail to connect or return corrupted data
        try:
            conn = wrong_sqlitesec.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT data FROM secret')
            result = cursor.fetchone()
            
            # If we get here, the data should be corrupted or None
            if result is not None:
                self.assertNotEqual(result[0], 'secret_data', 
                                  "Wrong key should not decrypt correct data")
            
            wrong_sqlitesec.close(conn, self.db_path)
        except Exception:
            # It's acceptable for this to raise an exception
            pass

    def tearDown(self):
        """Clean up test fixtures after each test method."""
        # Remove the test database file if it exists
        if os.path.exists(self.db_path):
            os.remove(self.db_path)


def demonstrate_usage():
    """Demonstrate basic usage of SqliteSec."""
    print("\n" + "="*50)
    print("SqliteSec Usage Demonstration")
    print("="*50)
    
    # Clean up any existing test database
    if os.path.exists("demo.db"):
        os.remove("demo.db")

    key = b'demo_key_1234567890123456'
    sqs = SqliteSec(key)

    # Step 1: Create and populate database
    print("1. Creating and populating database...")
    conn = sqs.connect("demo.db")
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, message TEXT)')
    cursor.execute('INSERT INTO messages (message) VALUES (?)', ('Hei, verden!',))
    conn.commit()
    sqs.close(conn, "demo.db")
    print("   Database created and data inserted.")

    # Step 2: Read the data back
    print("2. Reading data from encrypted database...")
    conn = sqs.connect("demo.db")
    cursor = conn.cursor()
    cursor.execute('SELECT message FROM messages WHERE id=1')
    fetched_data = cursor.fetchone()[0]
    print(f"   Retrieved message: {fetched_data}")
    sqs.close(conn, "demo.db")
    
    # Clean up
    if os.path.exists("demo.db"):
        os.remove("demo.db")
    print("3. Demo completed and cleaned up.")
    print("="*50)


if __name__ == '__main__':
    # Run the demonstration first
    demonstrate_usage()
    
    # Then run the unit tests
    print("\nRunning unit tests...")
    unittest.main(verbosity=2) 