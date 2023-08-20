# sql_validator

---

### What is it?
sql_validator is a CLI Python package that validates and format SQL(postgres) queries.

### Prerequisites
Before using this package make sure that you have a postgres database either on the local server or remote server, and have some data in it.

### Installation

To install this package, run the following command.

   ```python
   pip install git+https://github.com/Ahmad-Wahid/sql-validator
   ```

### Usage

1. Create an environment file `.env`, and update the following DB variables.

   ```text
   DB_NAME = database_name
   DB_USER = database_user
   DB_PASSWORD = database_password
   DB_HOST = ip_address
   DB_PORT = port
   ```

1. To run the validation script, there are two options. You can either pass a single query or file of multiple queries.
   
    - For passing a single query, run the following command. 
         
         ```python
         sql_validator --query "pass your query here"
         ```
    
    - For passing a file with `.sql` extension, run the following command.
      
         ```python
         sql_validator --file path/to/file-name.sql
         ```
         Make sure that, there is a semicolon at the end of every query.