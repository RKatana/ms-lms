server:
	python manage.py runserver

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

collecstatic:
	python manage.py collecstatic

superuser:
	python manage.py createsuperuser --username ${name}

fixture:
	python manage.py dumpdata ${app} --indent=2 --output=moringaschool/fixtures/models.json

loaddata:
	python manage.py loaddata models.json

shell:
	python manage.py shell