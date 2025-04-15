SHELL=/bin/bash -o pipefail

# Default version if not specified
V2_SAMPLESHEET_PARSER_VERSION ?= 0.1.0

# Run tests
test:
	@pip install .[test]
	@PYTHONPATH=src/ pytest \
      --cov src/v2_samplesheet_parser \
      --capture=no | \
      tee coverage_report.txt

# Run build
build_package:
	@pip install .[build]
	@python3 -m build

# Install package
install:
	@pip install .

# Push to test pypi
push_test_pypi:
	@pip install .[deploy]
	@python3 -m twine upload --repository testpypi dist/* --verbose

# Install from test pypi
install_test_pypi:
	@pip install \
		--index-url https://test.pypi.org/simple/ \
		--extra-index-url https://pypi.org/simple/ \
		v2-samplesheet-parser==${V2_SAMPLESHEET_PARSER_VERSION}
	@python -c "from v2_samplesheet_parser import parse_samplesheet; print('Successfully imported parse_samplesheet')"

# Install to pypi
push_pypi:
	@pip install .[deploy]
	@python3 -m twine upload --repository pypi dist/* --verbose

# Install from pypi
install_pypi:
	@pip install \
		--index-url https://pypi.org/simple/ \
		v2-samplesheet-parser==${V2_SAMPLESHEET_PARSER_VERSION}
	@python -c "from v2_samplesheet_parser import parse_samplesheet; print('Successfully imported parse_samplesheet')"

# Clean build artifacts
clean:
	@rm -rf build/ dist/ *.egg-info
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

# Help target
help:
	@echo "Available targets:"
	@echo "  test              - Run tests with coverage"
	@echo "  build_package     - Build the package"
	@echo "  install           - Install the package locally"
	@echo "  push_test_pypi    - Push to test PyPI"
	@echo "  install_test_pypi - Install from test PyPI"
	@echo "  push_pypi         - Push to PyPI"
	@echo "  install_pypi      - Install from PyPI"
	@echo "  clean             - Clean build artifacts"
	@echo "  help              - Show this help message"
	@echo ""
	@echo "Usage examples:"
	@echo "  make test"
	@echo "  make build_package"
	@echo "  make push_test_pypi"
	@echo "  make install_test_pypi V2_SAMPLESHEET_PARSER_VERSION=0.1.0"
