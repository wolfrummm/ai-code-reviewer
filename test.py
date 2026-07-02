# test.py
import os

def get_user(id):
    query = "SELECT * FROM users WHERE id = " + id  # SQL injection vulnerability
    return query

password = "admin123"  # hardcoded credential

def divide(a, b):
    return a/b  # no zero division check

data = []
for i in range(1000000):
    data.append(i)  # memory inefficient