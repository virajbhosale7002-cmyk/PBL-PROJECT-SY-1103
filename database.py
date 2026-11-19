database.py
"""MySQL connection helper for Mentor-Mentee Management System."""
import mysql.connector
from mysql.connector import Error
def get_db_connection():
return mysql.connector.connect(
host="localhost",
user="root",
password="",
database="mentor_mentee_db",
