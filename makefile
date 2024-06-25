# Makefile

# Define the Python interpreter to use
PYTHON = python3

# Define the Django management command to run the server
MANAGE_CMD = manage.py

# Define the port to run the server on
PORT = 8000

# Activate vitual environment command
ACTIVATE_VENV := . venv/bin/activate

# Target to install Python dependencies
install-dependencies:
	@echo Installing dependencies of the project.
	$(PYTHON) -m pip install -r ../requirements.txt

# Target to run Django database migrations
migrate:
	@echo migrating the changes to Database.
	$(PYTHON) $(MANAGE_CMD) migrate

# Run the custom manage py command to load the data in the database
load-data:
	@echo Polling marketplace events API periodically and storing it in the database.
	$(PYTHON) $(MANAGE_CMD) poll_events

# Target to run the Django development server
run:
	@echo Running development server at 8000 PORT.
	$(PYTHON) $(MANAGE_CMD) runserver $(PORT)

# Show this help message
help:
	@echo "Available targets:"
	@echo "  install-dependencies        			- Install the dependencies in virtual environment"
	@echo "  migrate              				- Migrate the migrations to the database"
	@echo "  run              				- Run Django server"
	@echo "  load-data              			- Load data in the database"
	@echo "  help              				- Show this help message"
