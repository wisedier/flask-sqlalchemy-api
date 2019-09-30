# Flask-SQLAlchemy
This project was created to demonstrate how to set up and organize an API server project using:

- [**FLASK**](https://palletsprojects.com/p/flask/)
- [**SQLAlchemy**](https://www.sqlalchemy.org)

## Setup

At first, you have to install a database server. In this project, I used PostgreSQL. If you want to change it from PostgreSQL to other one, 
remove a line contains `psycopg2-binary` from [*requirements.txt*](/requirements.txt) and update [*SQLALCHEMY_DATABASE_URL*](/api/config/secret.py).  
```bash
createuser -h 127.0.0.1 -d -P api
createdb -O api api
psql -h 127.0.0.1 -U api -W
```

After setup database, install required Python packages and run the server. Server will listening at [127.0.0.1:5000](http://127.0.0.1:5000)

```bash
pip install -r api/requirements.txt
python api/manage.py initdb
python api/manage.py run
```

You can check Swagger UI for API documentation at http://127.0.0.1:5000/docs

## Notes
- Update [**SECRET**](/api/config/secret.py) value
- Add [**secret.py**](/api/config/secret.py) to [**.gitignore**](.gitignore)
- In order to use [**uWSGI**](http://projects.unbit.it/uwsgi), you can use [**wsgi.py**](/api/app/wsgi.py) as a callable app module

The above listings are IMPORTANT for security if your service based on this project will be exposed to external connections.
