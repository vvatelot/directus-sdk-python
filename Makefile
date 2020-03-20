.PHONY: clean install

# Run all commands in a single shell
# See https://www.gnu.org/software/make/manual/html_node/One-Shell.html
.ONESHELL:

SHELL := bash
VENV := venv

BLACK := python3 -m black --exclude ${VENV}
PYLINT := python3 -m pylint

clean:
	@rm -rf -- ${VENV}

venv:
	@test -f ${VENV}/bin/activate || python3 -m venv ${VENV}
	@source ${VENV}/bin/activate
	@pip -q install wheel
	@pip -q install -r requirements-dev.txt

install: clean venv
	@echo "Activate the python virtual environement with 'source ${VENV}/bin/activate'"

lint: venv
	@source ${VENV}/bin/activate
	@echo -e "\nChecking python black\n"
	${BLACK} --check .
	@echo -e "\nChecking python lint\n"
	${PYLINT} directus_api

format: venv
	@source venv/bin/activate
	${BLACK} .
