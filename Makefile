.PHONY : build test publish
.DEFAULT_GOAL := build

build:
	poetry build

tests:
	poetry run pytest

publish:
	poetry publish



