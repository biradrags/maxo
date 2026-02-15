# Cross-platform shell configuration
# Use PowerShell on Windows (higher precedence than shell setting)

set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

# Use sh on Unix-like systems

set shell := ["sh", "-c"]

lint:
    ruff check
    codespell src examples
    bandit src -r
    slotscheck src

static:
    mypy

test:
    pytest --cov src

test-all:
    nox

all:
    just lint
    just static
    just test-all
