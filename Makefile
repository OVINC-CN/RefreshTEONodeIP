pylint:
	scripts/pylint.sh

pre-commit:
	scripts/pre-commit.sh

lint: pre-commit pylint

init:
	scripts/init.sh

init-dev:
	scripts/init-dev.sh
