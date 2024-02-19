# Helper scripts organized in Makefile for easy execution
clear_coverage:
	rm -rf ./coverage/*
	rm -f ./coverage/.coverage

generate_coverage_report:
	coverage run --branch -m pytest ./src/VendingMachine.py ./src/test_vendingmachine.py
	coverage html
