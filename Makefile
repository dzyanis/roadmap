.PHONY: all
all: golang java ruby php
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

.PHONY: ruby
ruby:
	@echo "start ruby"
	sh tools/build.sh ruby
	@echo "finish ruby"

.PHONY: php
php:
	@echo "start php"
	sh tools/build.sh php
	@echo "finish php"