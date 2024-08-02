1. Project Overview

   - Project Name: Blog Web App.
   - Description: The Django Blog Project is a simple yet powerful blogging platform built using the Django web framework. It provides essential blogging features such as creating, editing, and deleting posts, as well as user authentication and commenting..
   - Purpose: Its main purpose is to perform basic crud operations of a blog.
   - Link to Demo: My github link ( https://github.com/thinkingtek/django-blog.git )

2. Installation

   - Clone the repository:
     git clone https://github.com/thinkingtek/django-blog.git

   - Change directory:
     cd yourproject

   - Create a virtual environment
     python -m venv env
   - Activate the virtual environment
     .\env\Scripts\activate (for windows)
     source env/bin/activate (for Mac)

   - Install dependencies:
     pip install -r reqs.txt

   - Set up the database:
     python manage.py migrate

3. Usage

   - Run "python manage.py runserver" to run the project

4. Instructions

   - After running migrations, then add post categories through the Django admin (morals, relations,politics,economics,tech, etc) before adding posts.
   

5. Features

   - It as a responsive design, for both mobile and destop screens.
   - User creation, authentication, password reset and more.
   - Contact form page for users to communicate or send emails to the company
   - small letter case is enforced for email with JS in the signup form
   - Registered users can perform crud operations, like and comment on posts and add to favourite
   - Superuser can set posts as editors pick in the Django admin 
   - Feature to like social media handle
   - Unit testing can be added later

6. Testing

   - "python manage.py test"

7. Created Accounts
   NOTE: Emails from the .env file are not fuctional

   -------- ACCOUNTS -----------
   username: testuser
   email: testuser@gmail.com
   password: mypass123

   username: superuser (django admin access)
   email: superuser@gmail.com
   password: mypass123

   testuserpass (password for all ordinary user accounts)
