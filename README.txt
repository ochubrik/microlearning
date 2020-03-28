sudo apt install python3-pip
sudo pip3 install virtualenv
virtualenv djangoenv
source djangoenv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser

python manage.py crontab add (not in win!)
registrate other user for test sending emails
in win case: python manage.py parse_articles, python manage.py email_sender
