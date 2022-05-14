upbuild: build up

up:
	docker-compose -f local.yml up

build:
	docker-compose -f local.yml build

run:
	docker-compose -f local.yml run $(filter-out $@,$(MAKECMDGOALS))

restart:
	docker-compose -f local.yml restart $(filter-out $@,$(MAKECMDGOALS))

shell:
	docker-compose -f local.yml exec django /entrypoint python manage.py shell_plus

bash:
	docker-compose -f local.yml exec django /entrypoint sh

makemigrations:
	docker-compose -f local.yml run --rm django python manage.py makemigrations $(filter-out $@,$(MAKECMDGOALS))

migrate:
	docker-compose -f local.yml run --rm django python manage.py migrate $(filter-out $@,$(MAKECMDGOALS))

superuser:
	docker-compose -f local.yml run --rm django python manage.py createsuperuser $(filter-out $@,$(MAKECMDGOALS))

makemessages:
	docker-compose -f local.yml run --rm django python manage.py makemessages --no-location -l ar

compilemessages:
	docker-compose -f local.yml run --rm django python manage.py compilemessages

urls:
	docker-compose -f local.yml run django python manage.py show_urls

logs:
	docker-compose -f local.yml logs -f $(filter-out $@,$(MAKECMDGOALS))

test:
	docker-compose -f local.yml run --service-ports --rm -e DEBUGGER=True -e DJANGO_SETTINGS_MODULE=config.settings.test django python manage.py test $(filter-out $@,$(MAKECMDGOALS))

test_local:
	docker-compose -f local.yml exec -e DJANGO_SETTINGS_MODULE=config.settings.test django /entrypoint python manage.py test $(filter-out $@,$(MAKECMDGOALS))

debug:
	docker-compose -f local.yml run --service-ports --rm $(filter-out $@,$(MAKECMDGOALS))

down:
	docker-compose -f local.yml down $(filter-out $@,$(MAKECMDGOALS))

destroy:
	docker-compose -f local.yml down -v


rm_pyc:
	find . -name '__pycache__' -name '*.pyc' | xargs rm -rf
