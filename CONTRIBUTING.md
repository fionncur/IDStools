# Contributing Guidelines for IDStools

Thank you for your interest in contributing to IDStools. We welcome contributions from the fusion community to help each other. Please take a moment to review the following guidelines to ensure a smooth and productive collaboration.

## Getting Started

### Code of Conduct
Please read and adhere to ITER Code of Conduct. We expect all contributors to create a welcoming and inclusive community.

### Prerequisites
Before you start, ensure you have met the following requirements:
- Python 3.8+ is installed and available
- IMAS-Core module is loaded (Optional)

### Clone the repository
Clone the repository to your local machine:
```bash
git clone https://github.com/iter-organization/IDStools.git
cd IDStools
```

## Making Contributions
### Branching
Create a new branch for each contribution. Use a descriptive name for the branch.
To create a new branch and switch to it:

```bash
git checkout -b feature/your-feature-name
```

### Coding Guidelines
- Follow the coding style and conventions used in the project
- Follow SOLID principles while coding ([read more](https://www.freecodecamp.org/news/solid-principles-explained-in-plain-english/))

#### Code Organization
- Code is organized in three main packages: `compute`, `view`, and `domain`
- All calculation operations on IDS to get meaningful data are added to `compute`
- There is a distinct module in the `compute` and `view` packages for every IDS
- Each `Compute` class receives respective IDS object to operate on
- `domain` package is used when you have operations on 2 or more IDSs and need to return the result

#### Functions
- Define clear and meaningful function names (e.g., `getBResonance`, `getActivePfCoils`)
- Write functions to be generalized and reusable by other code
- Follow the `single responsibility principle` when writing functions
- Type hints for parameters and return types are mandatory
- Docstrings with examples are helpful for others to understand what the code does

#### Variable Naming
- Define clear and meaningful variable names (e.g., `b_total`, `profile_2d_index`)
- Use PascalCase for class names
- Use snake_case for variables and function names (following Python conventions)

### Script Naming Conventions
- Visualization scripts (console print or plots) start with `plot` prefix (e.g., `plotequilibrium`)
- IDS-related operations like copy, performance, size are prefixed with `ids` (e.g., `idscp`, `idsresample`)
- Database-related operations are prefixed with `db` (e.g., `dblist`)

#### Code Formatting
We use the [Black formatter](https://black.readthedocs.io/en/stable/) for consistent code formatting.

To format your code:
```bash
black -l 120 idstools
```

Append formatting-related commits to the `.git-blame-ignore-revs` file in the root of the repository.

Configure git to ignore formatting-related commits:
```bash
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

#### Pre-commit Hooks
Pre-commit hooks are used in the repository. To configure them:

1. Ensure pre-commit is installed:
```bash
pip install pre-commit
```

2. Install the hooks:
```bash
pre-commit install
```

More information: 
- [Black integrations](https://black.readthedocs.io/en/stable/integrations/source_version_control.html)
- [Pre-commit](https://pre-commit.com/#install)

#### Type Checking
Type checking is important to avoid runtime errors. Use [mypy](https://mypy.readthedocs.io/en/stable/getting_started.html) for static type checking:

```bash
pip install mypy
mypy idstools
```


### Testing
- Ensure your changes do not break existing functionality
- Write tests for new features or bug fixes, if applicable
- Run the project's test suite before submitting a pull request

```bash
pytest tests/
```

### Commit Messages
Write clear and concise commit messages that describe the purpose of your changes.
Use the present tense (`Add feature` not `Added feature`).
Reference issue numbers (e.g., `Fix IMAS-XXXX`) if relevant.

### Submitting Changes
#### Pull Request Guidelines
1. Create a pull request from your feature branch
2. Provide a clear description of the changes and why they are necessary
3. Reference any related issues
4. Engage in discussions and address feedback promptly

#### Code Review
- Be open to feedback and make necessary changes
- Respond to review comments in a timely manner
- Update your branch if requested

## Community

### Code of Conduct
ITER has a Code of Conduct to maintain a respectful and inclusive community. Please follow it in all interactions.

### Issue Tracking
- Check the issue tracker for open issues that need attention
- Create issues to report bugs or suggest enhancements
- Use appropriate labels and provide detailed descriptions

## Discussion
Join our community discussions to engage with other contributors:
- Participate in project-related discussions
- Share your insights and expertise
- Ask questions and help others

## Acknowledgment
Thank you for your contributions to the IDStools project! Your involvement helps advance fusion research and supports the broader scientific community.