# rescrapify

## Setting Up the Project on Windows

### Prerequisites
- Ensure that Python is installed on your system. If not, download and install Python from [python.org](https://www.python.org/).

### Setting Up Virtual Environment

1. Install virtualenv:
    ```bash
    pip install virtualenv
    ```

2. Create a new virtual environment:
    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:
    ```bash
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .\venv\Scripts\activate
    ```

### Initializing Dependencies and Running the Server

4. Install Django in the virtual environment:
    ```bash
    pip install Django
    ```

5. Fork the main repository and Clone your forked repository:
    ```bash
    git clone https://github.com/<your username>/rescrapify.git
    git remote -v 
    git pull origin main   
    ```

6. Navigate to the project directory:
    ```bash
    cd rescrapify
    ```

8. Install project dependencies:
    ```bash
    pip install -r requirements.txt
    ```

#### There's a need for initializing SECRET_KEY and .env.

1. Generate SECRET_KEY in python shell:
    ```bash
    from django.core.management.utils import get_random_secret_key
    print('SECRET_KEY=',get_random_secret_key())
    ```

2. Add SECRET_KEY in .env :
    
    ```bash
    SECRET_KEY= 2^y(*!7(n_(_v#o*+7w-_wt*@k(8m8l&9x-_cdbwube2%e6+4z
    EMAIL_HOST_USER = "rescrapify.demo.login@gmail.com"
    EMAIL_HOST_PASSWORD = "czyzipxusaoqvjxu" 
    RAZOR_PAY_KEY_ID = rzp_test_TqHFum4mPJRzWx
    RAZOR_PAY_KEY_SECRET = 7OC5Z3oqgEG4OjCcFs5LYtGK

    LINK =  http://127.0.0.1:8000/
    ```

9.  Make changes in the database using makemigrations:
    ```bash
    python manage.py makemigrations
    ```

10. Update the actual database:
    ```bash
    python manage.py migrate
    ```

11. Create a Superuser to access the admin panel
    ```bash
    python manage.py createsuperuser
    ```

12. Try running the server:
    ```bash
    python manage.py runserver
    ```


