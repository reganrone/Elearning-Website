# CS396 Project

## Description

This project builds an online learning system to help educate students. It allows teachers to monitor students activities and create lessons/quizzes for students to study and practice. This online learning system allows students to study and practice lessons/quizzes that teachers create and also allows them to create discussion posts. 

## Installation

To install this project, follow these steps:

1. Download Python and Django 
2. Install Python by creating a virtual environment
    "conda create --name CS396"
3. Activate your virtual environment
    "conda activate CS396"
4. Install Django
    "conda install -c conda-forge django"
5. Create a project
    "Django-admin startproject mysite"
    "cd mysite"
6. Run the server
    "python manage.py runserver" 
7. Your project is now running locally. Access it in your web browser at http://localhost:8000/.

## Usage

Creating an account: 
1. Open your web browser and navigate to the projects homepage. 
2. Click on the "Log in" or "Sign up" button. 
3. Fill in the required registration information such as username and password. 
4. Click the "Sign up" button to create an account. 

Logging in: 
1. Open your web browser and navigate to the project's homepage.
2. Click on the "Log In" button.
3. Enter your username and password.
4. Select either the teacher or student role
5. Click the "Log In" button to access your account.

Navigation for teachers: 
1. Once you sign in, you are directed to the teachers homepage
2. The teachers homepage has different links for each action.
3. Click on create lesson to create a lesson, create quiz to create a quiz, view grades to view grades, record grades to record a grade and so on.
4. Redirect to the homepage at any time by clicking the back to home link
5. Log out by clocking log out. 

Navigation for students: 
1. Once you sign in, you are directed to the students homepage
2. The students homepage has different links for each action.
3. Click on view lessons to view a lesson, view quizzes to view a quiz, create discussion post to create a discussion post and so on.
4. Redirect to the homepage at any time by clicking the back to home link
5. Log out by clocking log out. 

## Contributing

I welcome contributions from the community! If you'd like to contribute to this project, please follow these guidelines:

### Reporting Issues

When reporting issues, please include as much detail as possible, including:

- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Any error messages

### Making Code Contributions

If you'd like to contribute code changes, please follow these steps:

1. Fork the repository to your GitHub account.

2. Create a new branch for your changes:


## Acknowledgments

I would like to express my gratitude to the following resources that have inspired, guided, or contributed to this project:

- [Django Tutorial]: This tutorial was used in the first stages of this project as a guide for getting me started. 
