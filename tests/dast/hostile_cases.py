#!/usr/bin/env python3
"""DAST for Vértice, the bookstore software: runs the binary with hostile inputs and watches how it
behaves, without looking at the source code. Each case describes the input and what
the program is expected to do.

Usage: python3 tests/dast/hostile_cases.py build/vertice
"""
import subprocess
import sys

# Commands that set up a valid session before each attack.
SETUP = (
    "customer 7 10 Ana Souza\n"
    "author 1 M Machado de Assis\n"
    "book 1 1 39.90 Dom Casmurro\n"
)

# Each case has a name, the commands sent and the expectation:
# "no_crash" only requires the program to finish normally, and
# "reject" also requires the answer to the last command to start with "Error".
CASES = [
    ("5,000-character title", SETUP + "book 2 1 10.00 " + "A" * 5000 + "\ninvoice\n", "no_crash"),
    ("negative quantity", SETUP + "add 1 -5\n", "reject"),
    ("zero quantity", SETUP + "add 1 0\n", "reject"),
    ("eleventh book in a full invoice", SETUP + "add 1 1\n" + "".join("book %d 1 10.00 Book %d\nadd %d 1\n" % (n, n, n) for n in range(2, 12)), "reject"),
    ("text instead of a quantity", SETUP + "add 1 five\n", "reject"),
    ("quantity larger than an int", SETUP + "add 1 99999999999999999999\n", "reject"),
    ("book that does not exist", SETUP + "add 42 1\n", "reject"),
    ("unknown command", SETUP + "delete everything\n", "reject"),
]


def run(binary, commands):
    """Runs the binary with the given input and returns the exit code and the answers."""
    result = subprocess.run([binary], input=commands, capture_output=True, text=True, timeout=10)
    return result.returncode, result.stdout.splitlines()


def evaluate(binary, commands, expectation):
    """Evaluates one case and returns a failure message, or None when the program behaved well."""
    try:
        code, answers = run(binary, commands)
    except subprocess.TimeoutExpired:
        return "the program did not finish within 10 seconds"

    if code < 0 or code > 128:
        return "the program crashed (exit code %d)" % code

    if code != 0:
        return "the program ended with an error (exit code %d)" % code

    if expectation == "reject" and (not answers or not answers[-1].startswith("Error")):
        last = answers[-1] if answers else "(none)"
        return "the hostile command was accepted (answer: %s)" % last

    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 tests/dast/hostile_cases.py <Vértice binary>")
        return 2

    failures = 0

    for name, commands, expectation in CASES:
        reason = evaluate(sys.argv[1], commands, expectation)

        if reason is None:
            print("[ok] %s" % name)
        else:
            print("[FAILED] %s: %s" % (name, reason))
            failures += 1

    print("%d of %d hostile cases failed" % (failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
