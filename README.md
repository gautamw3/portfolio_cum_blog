My Portfolio Cum Blog Website
Welcome to my personal portfolio and blog website! This project showcases my work, shares my thoughts, and demonstrates my skills in full-stack web development.

Table of Contents
About
Features
Tech Stack
Getting Started
Project Structure
Contributing
License
Contact
About
This website serves as both my professional portfolio and a blogging platform. It highlights my projects, experience, and allows me to publish articles on topics I’m passionate about.

Features
Responsive, modern design
User authentication and profiles
Blog creation, editing, and commenting
Project showcase section
Interactive UI with AJAX features
Admin panel for content management
Tech Stack
Programming Language: Python
Framework: Django
Database: PostgreSQL
Frontend: Bootstrap, JavaScript, jQuery, SCSS/CSS, HTML
AJAX: For dynamic content updates
Others: Docker (optional for containerization), Shell scripting
Getting Started
To run this project locally, follow these steps:

Clone the repository

bash
git clone https://github.com/gautamw3/portfolio_cum_blog.git
cd portfolio_cum_blog
Create a virtual environment and activate it

bash
python3 -m venv venv
source venv/bin/activate
Install dependencies

bash
pip install -r requirements.txt
Configure the database

Update your database settings in settings.py with your PostgreSQL credentials.
Apply migrations

bash
python manage.py migrate
Run the development server

bash
python manage.py runserver
Access the site

Open http://localhost:8000 in your browser.
Project Structure
Code
portfolio_cum_blog/
│
├── blog/                # Blog app
├── portfolio/           # Portfolio app
├── static/              # Static files (CSS/JS/images)
├── templates/           # HTML templates
├── manage.py
├── requirements.txt
└── ...
Contributing
Contributions are welcome! Please open an issue or submit a pull request with improvements or suggestions.

License
This project is licensed under the MIT License.

Contact
GitHub: gautamw3
Email: your-email@example.com
