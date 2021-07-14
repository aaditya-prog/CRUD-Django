**Hi there, I'm [Aaditya Dulal](https://aadityadulal.com/)**

This is the first real project I've worked on and published on GitHub, It is
a simple CRUD application created using the powerful python framework, django.
Using the application, basic CRUD operations can be carried out.
User authentication system has also been managed in the application.
You must register and verify your email to login into the system. Also, only
admins will have access to the user management templates i.e., (add, update and delete users).
The normal users can perform crud operations on products and categories only.

So, if you are interested to take a look and run the project locally, follow the
guidelines below.

To run the project, you must have python installed on your system. Download the latest version of
python from the [Download Python](https://www.python.org/downloads/) page.

For packaging and dependency management of the application, python poetry has
been used. So, the second step is to install poetry on your system.

>Install poetry using the command `pip install poetry`. If you are facing
any problems installing and using poetry, read the docs here. [Poetry Docs](https://python-poetry.org/docs/)

>Clone the repository or download it manually.
Inside the root directory of the project, there is an .env_example file.
Rename it to .env and change the database and email configurations.

>The default database used in the project is postgreSQL. If you wish to use any
other database, change the database settings manually. Visit the official django
documentation for the guide. [Django Database Settings](https://docs.djangoproject.com/en/3.2/ref/settings/#databases)

You don't need to run the project in a virtual environment as poetry will automatically create a
virtual environment on your system. Now go to your terminal, type `poetry run python manage.py check`.
If you don't see any errors, you can run the server by typing `poetry run python manage.py runserver`.

You should be good to go now. I'd be glad to help you and
receive your feedbacks on the project:heart:

artdityadulal@gmail.com