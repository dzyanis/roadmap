.PHONY: all
all: golang java php python
	@echo "Done"

.PHONY: golang
golang:
	@echo "start golang"
	sh tools/build.sh go
	@echo "finish golang"

.PHONY: java
java:
	@echo "start java"
	sh tools/build.sh java
	@echo "finish java"

.PHONY: php
php:
	@echo "start php"
	sh tools/build.sh php
	@echo "finish php"


.PHONY: python
python:
	@echo "start python"
	sh tools/build.sh python
	@echo "finish python"