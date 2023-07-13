setup:
	pipenv sync --dev

run_server:
	cd ChatServer && python ChatServer.py

run_client:
	cd ChatClient && python ClientHandling.py

run_program: setup run_server run_client