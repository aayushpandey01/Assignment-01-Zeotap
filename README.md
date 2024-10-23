Rule Engine with AST-

Overview:-

This project implements a rule engine application that uses an Abstract Syntax Tree (AST) to determine user eligibility based on various attributes such as age, department, income, and spend. The system supports dynamic creation, combination, and modification of rules.

Features:-

Define rules using an AST structure.
Store rules in an SQLite database.
Create and combine rules.
Evaluate rules against user data.
Error handling for invalid rule strings or data formats.
Modify existing rules.

Prerequisites:-

Python 3.6+
SQLite

Installation-

1. Clone the repository:
   
   git clone <repository_url>
cd rule-engine-with-ast

3. Create and activate a virtual environment (optional but recommended):
   
   python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

5. Install required packages:
   
   pip install -r requirements.txt

Database Setup:-

1. Initialize the SQLite database:
   python init_db.py
