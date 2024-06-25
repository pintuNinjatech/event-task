# Fever Providers API

### Technology Used
 
- Python 3.10.9
- Django
- Rest API
- Django Rest Framework
- SQLite Database
- Swagger (for API documentation)


### Steps to setup the project


* To update the dependencies of the project (i.e. packages)
```
make install-dependencies
```

* Migrate the changes to the database
```
make migrate
```

* To run the server in your machine
```
make run
```

* Fetch the data provider and store those in the database, make sure you run this command in another terminal
```
make load-data
```

### The API is developed as per the requrement, please check below information
#### Swagger documentation: ```https://localhost:PORT/swagger/```
#### Django Admin Panel: ```https://localhost:PORT/admin/``` Username: ```admin``` Password: ```admin```

## Project Flow
1) Django Project Structure

      Created a Django project with an events app.

      The events app includes all required APIs and the database structure.

2) Polling App

      The polling app is responsible for collecting data and storing it in the database.

      A Django management command is created to:

         Fetch data from an external URL.

         Parse the XML response.

         Store the data in the database.

3) Database Operations

   Use the APIs created in the events app for all database operations.

4) API Calls

   Used HTTPX, an HTTP client for Python 3, to make API calls.