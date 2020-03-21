.PHONY: clean install

# Run all commands in a single shell
# See https://www.gnu.org/software/make/manual/html_node/One-Shell.html
SHELL := bash
.SHELLFLAGS := -ec
.ONESHELL:

VENV := venv

PACKAGE := directus

BLACK := python -m black --exclude ${VENV}
PYLINT := python -m pylint
MYPY := python -m mypy
PYTEST := python -m pytest -v

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
	${PYLINT} ${PACKAGE}
	@echo -e "\nChecking python typing\n"
	${MYPY} ${PACKAGE}

format: venv
	@source ${VENV}/bin/activate
	${BLACK} .

test: venv
	@source ${VENV}/bin/activate
	${PYTEST}
