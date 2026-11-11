# Roadmap keys include their category; directory names are stable public slugs.
ROADMAPS := $(patsubst roadmaps/%/roadmap.xml,%,$(wildcard roadmaps/*/*/roadmap.xml))
SUBJECT_INPUTS := $(shell find subjects -type d -o -name '*.xml')
BUILD_TOOLS := $(wildcard tools/*.py schemas/*.xsd schemas/*.json) tools/build.sh Makefile
outputs = $(addprefix generated/$(1)/roadmap.,dot svg png) generated/$(1)/guide.md generated/$(1)/graph.json
stamp = generated/$(1)/.roadmap-built

.PHONY: all
all: $(ROADMAPS)

define roadmap_rule
.PHONY: $(1) $(notdir $(1))
$(notdir $(1)): $(1)
$(1): $(call stamp,$(1))
$(call stamp,$(1)): roadmaps/$(1)/roadmap.xml roadmaps/$(1)/materials.xml $(SUBJECT_INPUTS) $(BUILD_TOOLS) $(if $(filter-out $(wildcard $(call outputs,$(1))),$(call outputs,$(1))),force)
	sh tools/build.sh $(1)
	touch $$@
endef

$(foreach roadmap,$(ROADMAPS),$(eval $(call roadmap_rule,$(roadmap))))

# Legacy commands retained for existing users and automation.
.PHONY: go golang java php python ruby devops cs
go golang: go-engineer
java: java-engineer
php: php-engineer
python: python-engineer
ruby: ruby-engineer
devops: devops-engineer
cs: data-structures-algorithms

.PHONY: force clean test check
force:

clean:
	rm -f $(foreach roadmap,$(ROADMAPS),$(call outputs,$(roadmap)) $(call stamp,$(roadmap)))

test:
	python3 -m unittest discover -s tests -v

check:
	python3 tools/validate.py
