---
name: test-case-generator
description: "Generate comprehensive test cases based on project code analysis. Use for: unit tests, integration tests, edge case identification, and test suite generation for various programming languages."
---

# Test Case Generator

This skill enables the automatic generation of test cases by analyzing project code, understanding its structure, functions, and potential edge cases.

## Core Workflow

To generate test cases for a project, follow these steps:

1. **Analyze Project Structure**: Examine the codebase to identify functions, classes, modules, and dependencies.
2. **Identify Testable Units**: Determine what needs testing (functions, methods, API endpoints, UI components).
3. **Generate Test Cases**:
    * **Unit Tests**: Test individual functions/methods with various inputs including edge cases.
    * **Integration Tests**: Test interactions between components.
    * **Edge Cases**: Identify boundary conditions, error scenarios, and unusual inputs.
    * **Parameterized Tests**: Generate tests with multiple input combinations.
4. **Implement Test Scripts**: Create test files in the appropriate framework (pytest, JUnit, Jest, etc.).
5. **Validate Tests**: Ensure generated tests are syntactically correct and runnable.
6. **Clean Up**: Remove any temporary analysis files.

## Bundled Resources

### Scripts
- `scripts/generate_tests.py`: A template script for analyzing code and generating test cases.

### References
- `references/testing_patterns.md`: Guide on testing patterns, frameworks, and best practices.

## Guidelines for Quality
- **Coverage**: Aim for high code coverage by testing all branches and edge cases.
- **Readability**: Generate clear, well-documented test cases with descriptive names.
- **Maintainability**: Structure tests to be easy to update when code changes.
- **Language Support**: Adapt to the project's programming language and testing framework.
- **Automation**: Generate tests that can be integrated into CI/CD pipelines.
