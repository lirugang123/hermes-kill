# Contributing to Hermes Kill

First off, thanks for taking the time to contribute! 🎉

## Code of Conduct

- Be respectful and inclusive
- Exercise empathy and kindness
- Give constructive feedback
- Focus on what is best for the community

## Getting Started

### Prerequisites

- Python 3.11+
- Git
- Node.js 18+ (optional)
- Docker (optional)

### Installation

```bash
# Clone the repository
git clone git@github.com:lirugang123/hermes-kill.git
cd hermes-kill

# Install Python dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

## Contributing Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat: add web crawler tool
fix: resolve timeout issue in scraper
docs: update API documentation
refactor: improve error handling
test: add unit tests for utils
```

## Project Structure

```
hermes-kill/
├── scripts/              # Utility scripts
├── examples/             # Code examples
├── docs/                 # Documentation
├── tests/                # Test files
├── config/               # Configuration files
├── .github/workflows/    # CI/CD workflows
├── web-crawler-toolkit/  # Main skill
└── README.md
```

## Development Guidelines

### Python Code Style

- Follow [PEP 8](https://pep8.org/)
- Use type hints
- Add docstrings
- Maximum line length: 88 characters

### Testing

- Write tests for new features
- Maintain test coverage > 80%
- Run tests before submitting PR

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test
pytest tests/test_scraper.py -v
```

### Documentation

- Update README.md for significant changes
- Add docstrings to functions
- Update API documentation

## Reporting Bugs

Use GitHub Issues to report bugs. Include:

- Clear description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details

## Requesting Features

Use GitHub Issues to request features. Include:

- Feature description
- Use case
- Proposed solution
- Alternatives considered

## Pull Request Process

1. Update documentation
2. Add or update tests
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Release Process

1. Update version in package.json/setup.py
2. Update CHANGELOG.md
3. Create git tag
4. Build and upload release artifacts
5. Publish release on GitHub

## Contact

- GitHub: [@lirugang123](https://github.com/lirugang123)
- Email: lirugang123@qq.com
