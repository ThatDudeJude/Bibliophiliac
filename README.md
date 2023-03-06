# Bibliophiliac

A simple web-based book review app for book lovers that allows users to search for book information, review data, and add their own reviews. 

### Development Process
This project's frontend was built using pure CSS and Javascript (no styling framework) and the backend uses the python-based flask microframework that interacts with a database. The backend logic utilizes sqlachemy's ORM to interact with a postgresql database. For book description data, cover images, and ratings data, the [google books api](https://www.developers.google.com/books/docs/v1/using) repository is utilized in the app.

### Technology used
|Technology   |   Version |   Utility                      |
|-------------|-----------|--------------------------------|
|Flask        | v2.0.2    |Web microframework for Python web development
|SQLAlchemy   |v1.4.25    |Provides the ORM interface for interacting with databases
|Postgres     |v14.0      | SQL based Relational Database Management System (RDMS) for handling app data
|Psycopg2     |v2.9.1     | PostgreSQL database adapter for the Python-based web app
| Pytest       |v6.2.5    | Testing library for building and running the unit tests
|Google books api service | v1 | Provides access to book data ([more info here](https://www.developers.google.com/books/docs/v1/using))

## Installation and Setup

Installation instructions for Mac and Ubuntu based machines

1. Launch your terminal.
2. Create a new folder for your clone and navigate to it.   
3. Clone this github repository i.e. https://github.com/ThatDudeJude/Bibliophiliac into your folder.
4. Check that [python](https://www.python.org) version v3.8+ and pip is installed in your computer. If not install it.
5. Install a postgres server for your OS ([more info here](https://www.postgres.org/download)) if not installed. For windows users, you can add psql.exe to path.
6. Generate your google books api key [here](https://www.developers.google.com/books/docs/v1/using).
7. Now create a new virtual environment and activate it. For Linux and Mac OS run ``python3 -m venv venv && ./venv/bin/activate`` . For Windows cmd.exe run ``c:\>c:\Python38\python -m venv venv && venv/SCRIPTS/activate.bat`` . 
8.  Install all the required libraries. 
```
   python3 -m pip install -r requirements.txt
```
9. Open a new terminal and create two databases, one for testing and one for development purposes. First you need to login and obtain your hostname
For Mac and Linux users, run :
```    
    sudo su postgres
    psql postgres
    \! hostname
```

For Windows users, run:
```
    psql -U postgres    
    \! hostname
```

Now create a role and assign the privileges necessary for running the app's database
```    
    CREATE USER bibliophiliac WITH PASSWORD 'bibliophiliac_password';
    CREATE DATABASE bibliophiliac_db;    
    CREATE DATABASE test_bibliophiliac_db;    
    GRANT ALL PRIVILEGES ON DATABASE bibliophiliac_db TO bibliophiliac;
    GRANT ALL PRIVILEGES ON DATABASE test_bibliophiliac_db TO bibliophiliac;
    \connect bibliophiliac_db
    \conninfo
    \connect test_bibliophiliac_db
    \conninfo
    \q
```

   
Next, set the environment variables using information from hostname, the bibliophiliac password, and both databases from their `\conninfo` output.
```
    DATABASE_URL=postgres://USERNAME:PASSWORD@HOSTNAME:PORT/bibliophiliac_db
    TEST_DATABASE_URL=postgres://USERNAME:PASSWORD@HOSTNAME:PORT/test_bibliophiliac_db
```
10.  Before running the development server, set the environment variables for SECRET_KEY, BOOKS_API_KEY, and the necessary Flask-related variables. To generate a secret key, type in ``python3 -c "import secrets; print(secrets.token_urlsafe());" `` and use the output as the secret key.
```
    SECRET_KEY=[secret_key]    
    BOOKS_API_KEY=[google_books_api_key]
    FLASK_APP=bibliophiliac
    FLASK_ENV=development    
```
Once set, now run ``flask initialize-database && flask run``. Navigate to http://127.0.0.1:5000/ to view the application.

## Tests

To run the tests make sure to press Ctrl + C to stop the live server first. Then install the bibliophiliac library first and then run the tests using the following commands:
```
    python3 -m pip install -e .
    pytest tests
```
To uninstall bibliophiliac after the test, run
```
    python3 -m pip uninstall bibliophiliac
```

## Screenshots and visuals
* Login
![Login Page](/bibliophiliac/static/imgs/Login_Page.png)
  
* Search
![Book Search Results](/bibliophiliac/static/imgs/Search_Results.gif)  
* Add Review
![Adding a Review](/bibliophiliac/static/imgs/Add_Book_Review.gif)
* Update Profile
![Updating Profile](/bibliophiliac/static/imgs/Change_Profile_Name.gif)

## Contributing
Want to contribute? See contributing guidelines [here](/CONTRIBUTING.md).

## Codebeat

[![codebeat badge](https://codebeat.co/badges/be4f9790-dc54-416a-82cf-d856f84ccf2a)](https://codebeat.co/projects/github-com-thatdudejude-bibliophiliac-profile_branch_final)

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENCE.txt)