# Postfix Expression Solver

This Python script was created as part of a university exam. This script is a Postfix Expression Solver implementation capable of processing arithmetic, conditional, and looping expressions. It supports a series of predefined operations, allowing for variable handling, arithmetic operations, conditional logic, and even user-defined subroutines. The system uses a class-based structure to represent and evaluate each element of an expression.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Complete Example](#complete-example)
- [Modifications and Extensions](#modifications-and-extensions)

## Installation

To run this code, you only need Python 3.x. No additional libraries are required.

```bash
git clone https://github.com/JiacoDev/Postfix-Expression-Solver.git ./Postfix-expr-solver
cd ./Postfix-expr-solver
python3 Postfix_eval.py #use just this line if you want to run the code after you already downloaded the script
```

## Usage
### 1. Create and Evaluate expressions

To create an expression, use `Expression.from_program(text, dispatch)` with:
- `text`: a list of strings (Expression in postfix form)
- `dispatch`: a dictionary containing operators permitted to use

#### Example
```python
example = "2 3 + x * 6 5 - / abs 2 ** y 1/ + 1/"
e = Expression.from_program(example.split(), env)
#print(e)  # Prints the expression
result = e.evaluate({"x": 3, "y": 7})  # Evaluates the expression with x=3 and y=7
print(result)
```

### 2.Operators dictionary

Operators are defined in `env`. Currently, these are the implemented ones:
- Mathematical operations: `+`,`-`,`*`,`/`,`**`(Power),`%`(Modulus),`abs`,`1/`(Reciprocal)
- Logical operators: `=`,`!=`,`>`,`<`,`>=`,`<=`
- Assignment and memory: `alloc`,`valloc`,`setq`,`setv`
- Control flow: `if`,`while`,`for`,`prog2`,`prog3`,`prog4`
- Subroutines: `defsub`,`call`

### 3.Run Tests

In the code, there are test functions that helped to ensure that implemented operators work as intended.

## Complete Example

The following example demonstrates how to create an expression, evaluate it and display the result:

```python
# Define an expression
expression_text = "2 3 + x *"
expr = Expression.from_program(expression_text.split(), env)

# Evaluate the expression
result = expr.evaluate({"x": 5})
print(result)  # Expected output: 25
```

## Modifications and Extensions

You can extend the code by adding new operators by inheriting from `UnaryOp`,`BinaryOp`,`TernaryOp`,`QuaternaryOp` or other classes of appropriate arity and overriding the `evaluate` and `__str__` methods.
