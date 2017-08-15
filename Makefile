# Use development settings for running django dev server.
export DJANGO_SETTINGS_MODULE=setting.settingsdev

# Initializes virtual environment with basic requirements.
prod:
	pip install -r requirements.txt
	cd frontend
	npm install --production
	cd ../

# Installs development requirements.
dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	cd frontend
	cnpm install
	cd ../

dev2:
	cd frontend
	cnpm install
	cd ../

# Runs development server.
# This step depends on `make dev`, however dependency is excluded to speed up dev server startup.
run:
	cd frontend
	npm run dev
	cd ../
	python ./manage runserver

# Creates migrations and migrates database.
# This step depends on `make dev`, however dependency is excluded to speed up dev server startup.
migrate:
	python manage.py makemigrations
	python manage.py migrate

# Builds files for distribution which will be placed in /static/dist
build: prod migrate
	cd frontend
	npm run build
	cd ../

# Cleans up folder by removing virtual environment, node modules and generated files.
clean:
	rm -rf frontend/node_modules
	rm -rf frontend/static/dist

# Run linter
lint:
	@npm run lint --silent
