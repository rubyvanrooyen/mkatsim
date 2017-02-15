# Makefile -- python with virtualenv

PACKAGE = .

ifeq ($(wildcard venv),)
$(info `venv/' does not exist .. please run `./build-aux/bootstrap' first.)
endif

## control verbosity -- `make V=1` to see verbose output, or
##                   -- `make V=2` for increased verbosity
ifeq ($(V),2)
PYTESTFLAGS ?= -s
VERBOSE = -vv
else ifeq ($(V),1)
VERBOSE = -v
else
VERBOSE =
endif

SHELL = /bin/sh

BINDIR = ./venv/bin
FLAKE8 = $(BINDIR)/flake8 $(VERBOSE) $(FLAKE8FLAGS)
PYTEST = $(BINDIR)/py.test $(VERBOSE) $(PYTESTFLAGS)

.PHONY: all
all:

.PHONY: check
check:
	$(PYTEST)

.PHONY: cov
cov:
	$(PYTEST) --cov

.PHONY: clean
clean:
	$(RM) -- *.pyc
	find $(PACKAGE) tests/ -name '*.pyc' -delete

.PHONY: distclean
distclean: clean
	$(RM) -r .cache
	$(RM) .coverage
	$(RM) tags
	find . -name '__pycache__' -exec $(RM) -r "{}" +

.PHONY: help
help:
	@echo "Makefile targets:"
	@echo
	@echo "  all        trigger the default task (*)"
	@echo "  check      run software tests (+)"
	@echo "  clean      make clean"
	@echo "  cov        check test code coverage (+)"
	@echo "  distclean  make really clean"
	@echo "  help       display this text"
	@echo "  lint       run lint checks (+)"
	@echo "  tags       create ctags tags file"
	@echo
	@echo "    *  default Make target"
	@echo "     ++  adding \`V=1' gives verbose output"
	@echo "     ++  using \`V=2' increases the verbosity"

.PHONY: lint
lint:
	$(FLAKE8)

.PHONY: tags
tags:
	ctags \
    --exclude=venv \
    --exclude=__pycache__ \
    --exclude=.cache \
    --exclude=_attic \
    --python-kinds=-i \
    --recurse

# -fin-
