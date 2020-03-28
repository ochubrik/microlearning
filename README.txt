sudo apt install python3-pip
sudo pip3 install virtualenv
virtualenv djangoenv
source djangoenv/bin/activate
in win case: djangoenv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser

In file olgaproject/settings.py add EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
Registrate other user for test sending emails

python manage.py crontab add (not in win!)
in win case: python manage.py parse_articles, python manage.py email_sender
