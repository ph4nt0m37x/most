# Most
A collaboration application made in Django.
## Requirements
- Python 3.12
- Django
- Docker (optional)

## Run locally

- Install python.
- Make a local venv (virtual environment) and install all requirements. Another option is to open the project in a python IDE and configure a venv and interpreter there.
- Locate to the directory with the [manage.py](manage.py) file.
- Run the commands in terminal.
```cmd
> python manage.py makemigrations
> python manage.py migrate
> python manage.py runserver
```
- For creating an admin user, stop the application and run the commands.
```cmd
> python manage.py createsuperuser
> python manage.py runserver
```
- The application is available at http://127.0.0.1:8000/
- The admin panel is available at http://127.0.0.1:8000/admin. Login using the previously created credentials.

<sub>Note: When running localy the database will be empty.</sub>

## Run with Docker
- Install Docker.
- Run the command in terminal.
```cmd
> docker run -d -p "8000:8000" stojchevska/most:latest
```
- The application is available at http://localhost:8000

<sub>Note: The application includes example profiles. Admin panel is not available.</sub>

## Hosted on Azure
- Link to the hosted application https://most-e8dxaxgxd5dwc6d3.germanywestcentral-01.azurewebsites.net

<sub>Note: The application includes example profiles. Admin panel is not available.</sub>
