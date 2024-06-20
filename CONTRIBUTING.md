# Contributing Guidelines for IDStools
Thank you for your interest in contributing to IDStools. We welcome contributions from the fusion community to help each other . Please take a moment to review the following guidelines to ensure a smooth and productive collaboration.

## Getting Started

### Code of Conduct
Please read and adhere to ITER Code of Conduct. We expect all contributors to create a welcoming and inclusive community.

### Prerequisites
Before you start, ensure you have met the following requirements:
*   IMAS module is loaded
*   Python 3+ is loaded


### Clone the repository
Clone repository to your local machine.
```
git clone ssh://git@git.iter.org/imas/idstools.git
```

## Making Contributions
### Branching
Create a new branch for each contribution. Use a descriptive name for the branch.
To create a new branch and switch to it:

```
git checkout -b feature/your-feature
```

### Coding Guidelines
 - Follow the coding style and conventions used in the project.
 - Follow SOLID principles while coding [read more](https://www.freecodecamp.org/news/solid-principles-explained-in-plain-english/)


#### Code organization
 - Code is organized in two main packages, `compute` and `view`
 - All calculation operations on IDS to get meaningful data are added to `compute`
 - There is a distinct module in the `compute` and `view` packages for every IDS.
 - Each `Compute` class receives respective ids object to operate on
 - `domain` package is used if you have operations on 2 or more idses and need return the result

#### Functions
 - Define clear and meaningful function names `getBResonance`, `getActivePfCoils`
 - While writing functions always remember to make it generalized and can be used later by other codes
 - Follow `single responsibility principle` while writing functions
 - `typehint` for parameters and return types is mandatory
 - `docstring` with example will be useful for others to understand what code is doing

#### Variable Naming
Define clear and meaningful variable names `bTotal`, `profile2dIndex`
*   Use PascalCase for class names
*   Use camelCase for variables, function names

### Scripts Naming
*   Visualization scripts (console print or plots) starts with `view` prefix e.g. `plotequilibrium`
*   ids related operations like copy, performance, size prefix with `ids` e.g. `idscp`, `idsresample`
*   database related operations prefix with `db` e.g. dblist

#### Formatting
Use black formatter https://black.readthedocs.io/en/stable/

#### Type checking
It is very important to type check variables to avoid last minute surprises. To check your code for static type checking you can use mypy.
https://mypy.readthedocs.io/en/stable/getting_started.html


### Testing
Ensure your changes do not break existing functionality.
Write tests for new features or bug fixes, if applicable.
if new scripts are written then it should be added in tests\testscripts.sh, This script  is used in CI for testing regression
Run the project's test suite before submitting a pull request.

### Commit Messages
Write clear and concise commit messages that describe the purpose of your changes.
Use the present tense (`Add feature` not `Added feature`).
Reference issue numbers (e.g., `Fix IMAS-XXXX`) if relevant.

### Submitting Changes
#### Pull Request Guidelines
Create a pull request.
Provide a clear description of the changes and why they are necessary.
Engage in discussions and address feedback promptly.

#### Code Review
Be open to feedback and make necessary changes.

## Community
### Code of Conduct
ITER has Code of Conduct to maintain a respectful and inclusive community. Please follow it.

### Issue Tracking
Check the issue tracker for open issues that need attention.
Create issues to report bugs or suggest enhancements.

## Discussion
Join our Discussion Forum here to engage with the community.
Participate in project-related discussions and share your insights.

## Acknowledgment
Thank you for your contributions to IDStools project!