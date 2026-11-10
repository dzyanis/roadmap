STACKS := $(notdir $(patsubst %/,%,$(dir $(wildcard stacks/*/roadmap.xml))))
# Watch shared XML and directory changes, including additions or removals of includes.
SUBJECT_INPUTS := $(shell find subjects -type d -o -name '*.xml')
BUILD_TOOLS := $(wildcard tools/*.py) tools/build.sh Makefile
outputs = $(addprefix stacks/$(1)/data/roadmap.,dot svg png md)
stamp = stacks/$(1)/data/.roadmap-built

.PHONY: all golang $(STACKS)
all: $(STACKS)
golang: go

# Rebuild a stack if any member of its output set is missing.
define stack_rule
$(1): $(call stamp,$(1))
$(call stamp,$(1)): stacks/$(1)/roadmap.xml stacks/$(1)/materials.xml $(SUBJECT_INPUTS) $(BUILD_TOOLS) $(if $(filter-out $(wildcard $(call outputs,$(1))),$(call outputs,$(1))),force)
	sh tools/build.sh $(1)
	touch $$@
endef

$(foreach stack,$(STACKS),$(eval $(call stack_rule,$(stack))))

.PHONY: force clean
force:

clean:
	rm -f $(foreach stack,$(STACKS),$(call outputs,$(stack)) $(call stamp,$(stack)))

.PHONY: test
test:
	python3 -m unittest discover -s tests -v

.PHONY: check
check:
	python3 tools/validate.py
