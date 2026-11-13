# Build and verification targets of Vértice, the bookstore software. The sast, sanitizers, valgrind
# and dast targets are the checks that the continuous integration pipeline runs.

CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -Isrc/include
RELEASE = -O2 -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=2 -fstack-protector-strong
SANITIZE = -O0 -g -fno-omit-frame-pointer -fsanitize=address,undefined -fno-sanitize-recover=all

SOURCES = src/Author.cpp src/Book.cpp src/Customer.cpp src/Invoice.cpp src/payment.cpp
HEADERS = $(wildcard src/include/*.h)

.PHONY: all sast sanitizers valgrind dast clean

# Builds the software and the unit tests with the regular flags
all: build/vertice build/tests

build/vertice: $(SOURCES) src/main.cpp $(HEADERS)
	@mkdir -p build
	$(CXX) $(CXXFLAGS) $(RELEASE) -o $@ $(SOURCES) src/main.cpp

build/tests: $(SOURCES) tests/unit/tests.cpp $(HEADERS)
	@mkdir -p build
	$(CXX) $(CXXFLAGS) $(RELEASE) -g -o $@ $(SOURCES) tests/unit/tests.cpp

build/tests-sanitizers: $(SOURCES) tests/unit/tests.cpp $(HEADERS)
	@mkdir -p build
	$(CXX) $(CXXFLAGS) $(SANITIZE) -o $@ $(SOURCES) tests/unit/tests.cpp

# SAST: Semgrep with the C++ rules in .semgrep
sast:
	semgrep scan --config .semgrep --error --metrics=off --disable-version-check src

# Dynamic analysis: each unit test runs in its own process, built with ASan and UBSan
sanitizers: build/tests-sanitizers
	@failed=0; for test in $$(build/tests-sanitizers --list); do \
		echo "== $$test"; build/tests-sanitizers $$test || failed=$$((failed + 1)); \
	done; echo "failed tests: $$failed"; test $$failed -eq 0

# Dynamic analysis: each unit test runs in its own process, under Valgrind
valgrind: build/tests
	@failed=0; for test in $$(build/tests --list); do \
		echo "== $$test"; valgrind --quiet --error-exitcode=1 build/tests $$test || failed=$$((failed + 1)); \
	done; echo "failed tests: $$failed"; test $$failed -eq 0

# DAST: hostile inputs against the regularly built binary, without looking at the source code
dast: build/vertice
	python3 tests/dast/hostile_cases.py build/vertice

clean:
	rm -rf build
