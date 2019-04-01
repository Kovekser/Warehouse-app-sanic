.PHONY: test
test:
	@echo 'test run'


.PHONY: setup
setup:
	sudo pip install virtualenv
	virtualenv -p python3.7 venv
	pip install -r requirements/requirements.txt



.PHONY: liq_migrate
liq_migrate:
	./migrations/liquibase --url=jdbc:postgresql://localhost/warehouse \
	--driver=org.postgresql.Driver \
	--classpath=./migrations/jdbcdrivers/postgresql-42.2.5.jar \
	--username=admin \
	--password=686314 \
	--changeLogFile=/migrations/changelog.xml migrate

.PHONY: run_app
run_app:
	python manage.py