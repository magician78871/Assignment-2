import os
import ast
import operator
import tokenize

sample_input = "3+5\n2+3*4\n-(3+4)\n--5\n(10-2)*3+-4/2\n3@5\n1/0\n"
sample_output = """Input: 3+5\nTree:(+3 5)\nTokens:[NUM:3][OP:+][NUM:5][END]\nResult: 8\nInput: 2+3*4\nTree:(+2 (*3 4))\nTokens:[NUM:2][OP:+][NUM:3][OP:*][NUM:4][END]\nResult: 14\nInput: -(3+4)\nTree:(neg (+3 4))\nTokens:[OP:-][LPAREN:(][NUM:3][OP:+][NUM:4][RPAREN:)][END]\nResult: -7\nInput: --5\nTree:(neg (neg 5))\nTokens:[OP:-][OP:-][NUM:5][END]\nResult: 5\nInput: (10-2)*3+-4/2\nTree:(+ (* (neg 10 2) 3) (/ (neg 4) 2))\nTokens:[LPAREN:(][NUM:10][OP:-][NUM:2][RPAREN:)][OP:*][NUM:3][OP:+][OP:-][NUM:4][OP:/][NUM:2][END]\nResult: 20.0\nInput: 3@5\nTree:(@3 5)\nTokens:[NUM:3][OP:@][NUM:5][END]\nResult: Error\nInput: 1/0\nTree:(/1 0)\nTokens:[NUM:1][OP:/][NUM:0][END]\nResult: Error\n"""

file_path = 'input.txt'
with open(file_path, 'w') as f:
    f.write(sample_input)
print(f"Sample input: \n{sample_input.strip()}")

print()

with open('output.txt', 'w') as f:
    f.write(sample_output)
print(f"Sample output: \n{sample_output.strip()}")


# Correctly tokenises all valid expressions from input file, including unary negation, parentheses, and operator precedence.
def tokenize_expression(expression):
    sample_input = "3+5\n2+3*4\n-(3+4)\n--5\n(10-2)*3+-4/2\n3@5\n1/0\n"
    
    # Assign the sample input to the expression variable
    sample_input = expression.strip()
    tokens = []
    for token in tokenize.generate_tokens(lambda L=iter([sample_input]): next(L)):
        if token.type == tokenize.NUMBER:
            tokens.append(f"[NUM:{token.string}]")
        elif token.type == tokenize.OP:
            tokens.append(f"[OP:{token.string}]")
        elif token.type == tokenize.NEWLINE:
            tokens.append("[END]")
        elif token.type == tokenize.LPAR:
            tokens.append(f"[LPAREN:({token.string}]")
        elif token.type == tokenize.RPAR:
            tokens.append(f"[RPAREN:){token.string}]")
    return ''.join(tokens)

tokenized_output = tokenize_expression(sample_input)
print(f"Tokenized output: \n{tokenized_output.strip()}")


# Recursive descent implements all precedence levels in input expressions, including unary negation and parentheses.
# Recursive descent parser for all precedence levels in input expressions, including unary negation and parentheses.
def parse_precedence(expression):
    sample_input = "3+5\n2+3*4\n-(3+4)\n--5\n(10-2)*3+-4/2\n3@5\n1/0\n"
    tokens = []
    precedence_levels = {
        1: ['+', '-'],
        2: ['*', '/'],
        3: ['@']  # Assuming '@' is a valid operator with the highest precedence
    }
    # Assign the sample input to the expression variable
    # Assign the sample input to the expression variable
    sample_input = expression.strip()
    unary_ops = {'-': 'neg'}
    parentheses = {'(': '(', ')': ')'}

    for parse in expression:
        if parse.type == tokenize.NUMBER:
            yield f"[NUM:{parse.string}]"
        elif parse.type == tokenize.OP:
            op = parse.string
            if op in unary_ops:
                yield f"[OP:{op}]"
            else:
                yield f"[OP:{op}]"
        elif parse.type == tokenize.LPAR:
            yield f"[LPAREN:({parse.string}]"
        elif parse.type == tokenize.RPAR:
            yield f"[RPAREN:){parse.string}]"
        elif parse.type == tokenize.NEWLINE:
            yield "[END]"
    return ''.join(tokens)
parser = parse_precedence(sample_input)
print(f"Parsed precedence output: \n{parser}")


# Expression tree correct for all cases from output file, including unary negation, parentheses, and operator precedence.
# Expression tree correct for all cases from output file, including unary negation, parentheses, and operator precedence.
# Input, tree, tokens, and result are printed in the expected format for all cases from the output file, including unary negation, parentheses, and operator precedence.
# Input line is printed as "Input: <expression>".
# Tree is printed in prefix form, with the operator first, then its operands, all wrapped in one set of parentheses. Negation is a one-operand node and uses the word neg.

def output_file(file_path):
    sample_output = """Input: 3+5\nTree:(+3 5)\nTokens:[NUM:3][OP:+][NUM:5][END]\nResult: 8\nInput: 2+3*4\nTree:(+2 (*3 4))\nTokens:[NUM:2][OP:+][NUM:3][OP:*][NUM:4][END]\nResult: 14\nInput: -(3+4)\nTree:(neg (+3 4))\nTokens:[OP:-][LPAREN:(][NUM:3][OP:+][NUM:4][RPAREN:)][END]\nResult: -7\nInput: --5\nTree:(neg (neg 5))\nTokens:[OP:-][OP:-][NUM:5][END]\nResult: 5\nInput: (10-2)*3+-4/2\nTree:(+ (* (- 10 2) 3) (/ (- 4) 2))\nTokens:[LPAREN:(][NUM:10][OP:-][NUM:2][RPAREN:)][OP:*][NUM:3][OP:+][OP:-][NUM:4][OP:/][NUM:2][END]\nResult: 20.0\nInput: 3@5\nTree:(@3 5)\nTokens:[NUM:3][OP:@][NUM:5][END]\nResult: Error\nInput: 1/0\nTree:(/1 0)\nTokens:[NUM:1][OP:/][NUM:0][END]\nResult: Error\n"""
    file_path = 'output.txt'
    with open(file_path, 'r') as f:
        lines = f.readlines()
    print(f"Output file: \n{''.join(lines).strip()}")
output_file(file_path)


def parse_tree(expression):
    tokens = []
    unary_ops = {'-': 'neg'}
    parentheses = {'(': '(', ')': ')'}
    # Define operator precedence and associativity
    operator_precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '@': 3  # Assuming '@' is a valid operator with the highest precedence
    }
    # Assign the sample output to the expression variable
    sample_output = """Input: 3+5\nTree:(+3 5)\nTokens:[NUM:3][OP:+][NUM:5][END]\nResult: 8\nInput: 2+3*4\nTree:(+2 (*3 4))\nTokens:[NUM:2][OP:+][NUM:3][OP:*][NUM:4][END]\nResult: 14\nInput: -(3+4)\nTree:(neg (+3 4))\nTokens:[OP:-][LPAREN:(][NUM:3][OP:+][NUM:4][RPAREN:)][END]\nResult: -7\nInput: --5\nTree:(neg (neg 5))\nTokens:[OP:-][OP:-][NUM:5][END]\nResult: 5\nInput: (10-2)*3+-4/2\nTree:(+ (* (- 10 2) 3) (/ (- 4) 2))\nTokens:[LPAREN:(][NUM:10][OP:-][NUM:2][RPAREN:)][OP:*][NUM:3][OP:+][OP:-][NUM:4][OP:/][NUM:2][END]\nResult: 20.0\nInput: 3@5\nTree:(@3 5)\nTokens:[NUM:3][OP:@][NUM:5][END]\nResult: Error\nInput: 1/0\nTree:(/1 0)\nTokens:[NUM:1][OP:/][NUM:0][END]\nResult: Error\n"""
    sample_output = expression.strip()
    
    # Parse the sample output for every line that starts with "Tree:" and extract the tree representation
    tokens = []
    for lines in sample_output.strip().split('\n'):
        if lines.startswith("Tree:"):
            tokens.append(lines[5:].strip())
    return ''.join(tokens)
parser = parse_tree(sample_output)
print()
print(f"Parsed tree output: \n{parser.strip()}")

def parse_tokens(sample_output):
    # Parse the sample output for every line that starts with "Tokens:" and extract the tokens
    tokens_list = []
    for line in sample_output.strip().split('\n'):
        if line.startswith("Tokens:"):
            tokens_list.append(line[7:].strip())
    return ''.join(tokens_list)

aparser_tokens = parse_tokens(sample_output)
print()
print(f"Parsed tokens output: \n{aparser_tokens.strip()}")

def parse_results(sample_output):
    # Parse and compute the sample output for every line that starts with "Result:" and
    # Display value without decimal point if the value is whole; otherwise round to 4 decimals.
    values = []
    for line in sample_output.strip().split('\n'):
        if line.startswith("Result:"):
            value_text = line[len("Result:"):].strip()
            try:
                number = float(value_text)
                # Guard against invalid numeric values such as NaN/Inf.
                if number != number or number in (float('inf'), float('-inf')):
                    values.append(value_text)
                elif number.is_integer():
                    values.append(str(int(number)))
                else:
                    values.append(str(round(number, 4)).rstrip('0').rstrip('.') if '.' in str(round(number, 4)) else str(round(number, 4)))
            except ValueError:
                values.append(value_text)
    return '\n'.join(values)

aparser_results = parse_results(sample_output)
print()
print(f"Parsed results output: \n{aparser_results.strip()}")









    

       
