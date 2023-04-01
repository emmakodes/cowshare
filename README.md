# cowshare

# How to set up the project locally on your system

0. Fork the repo to your GitHub account
![image](https://user-images.githubusercontent.com/122211702/225223055-92e2b168-6302-4c7e-92d3-b52ab58794f9.png)

1. Open your code editor(either visual studio code or pycharm)

2. Open the terminal

3. Clone the project by running the following command on the terminal(ensure you are connected to the internet)

 `git clone https://github.com/yourgithubusername/cowshare.git`

Instead of https://github.com/yourgithubusername/cowshare.git you copy the following from your GitHub account and use it  ![image](https://user-images.githubusercontent.com/122211702/225223448-dab70fd5-c56e-4547-81f3-4c1d39f92cf3.png) 

4. Change directory to the project by running the following command on the terminal

 `cd cowshare`

5. Create a virtual environment by running the following command:

 `python –m venv .myvenv`

6. Activate the virtual environment using the following command

 `.myvenv\Scripts\activate`


7. Run the following command on the terminal to install every package needed

 `pip install –r requirements.txt`

8. Run the following command to makemigrations and migrate

 `python manage.py makemigrations`

 `python manage.py migrate`


9. Start the development server

 `python manage.py runserver`

10. You can visit the admin panel
username: admin
password: admin
