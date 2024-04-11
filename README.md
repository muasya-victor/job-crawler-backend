Setting up project
1. Create Virtual Env read more [here](https://acceptance.co.ke/sections/software/deploy-django-application-with-postgres-ubuntu-20-04/#creating-a-virtual-environment)
2. Install packages from requirements.txt
    
   ```bash
    pip install -r requirements.txt
   ```
3. Make a copy of the env.example and enter your values
4. Create A secret key [here](https://djecrety.ir/) and paste it in the env file.
5. Run migrations
6. Create a super user 
7. Run the project

## WINDOWS SETUP
1. Initialize virtual environment
   ```bash
    python -m venv env
   ```
2. Activate Virtual Environment
   ```bash
    env\Scripts\Activate
   ```
3. Install requirements
   ```bash
    pip install -r requirements.txt
   ```
4. Make a copy of the env.example and enter your values
5. Create A secret key [here](https://djecrety.ir/) and paste it in the env file.
6. Update setup tools 
   ```bash 
      pip install --upgrade setuptools
   ```
7. Add themes for swagger and admin panel 
   ```bash 
      python manage.py collectstatic
   ```   
8. Run migrations
   ```bash
    python manage.py migrate
   ```
9. Run the project
   ```bash
    python manage.py runserver
   ```

## DEV NOTICE
Add all requirements in your environment to your requirements.txt everytime before you commit your changes
```bash 
   pip freeze > requirements.txt
```
