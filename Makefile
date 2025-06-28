PYTHON = python
PYTEST = pytest
BLACK = black
ISORT = isort
FLAKE8 = flake8

SRC_DIR = app/

.PHONY: lint test

lint:
	@echo "=== Start ISORT check ==="
	$(ISORT) --check $(SRC_DIR)
	@echo "======== SUCCESS ========"
	@echo "=== Start BLACK check ==="
	$(BLACK) --check $(SRC_DIR)
	@echo "======== SUCCESS ========"
	@echo "=== Start FLAKE8 check =="
	$(FLAKE8) $(SRC_DIR)
	@echo "======== SUCCESS ========"

test:
	@echo "====== Start TESTS ======"
	$(PYTEST) -v
	@echo "======== SUCCESS ========"