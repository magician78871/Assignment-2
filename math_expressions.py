import ast
import operator
import tokenize
import re

# Create a sample input and output
sample_input = "3+5\n2+3*4\n-(3+4)\n--5\n(10-2)*3+-4/2\n3@5\n1/0\n"
sample_output = """Input: 3+5\nTree:(+3 5)\nTokens:[NUM:3][OP:+][NUM:5][END]\nResult: 8\nInput: 2+3*4\nTree:(+2 (*3 4))\nTokens:[NUM:2][OP:+][NUM:3][OP:*][NUM:4][END]\nResult: 14\nInput: -(3+4)\nTree:(neg (+3 4))\nTokens:[OP:-][LPAREN:(][NUM:3][OP:+][NUM:4][RPAREN:)][END]\nResult: -7\nInput: --5\nTree:(neg (neg 5))\nTokens:[OP:-][OP:-][NUM:5][END]\nResult: 5\nInput: (10-2)*3+-4/2\nTree:(+ (* (neg 10 2) 3) (/ (neg 4) 2))\nTokens:[LPAREN:(][NUM:10][OP:-][NUM:2][RPAREN:)][OP:*][NUM:3][OP:+][OP:-][NUM:4][OP:/][NUM:2][END]\nResult: 20.0\nInput: 3@5\nTree:(@3 5)\nTokens:[NUM:3][OP:@][NUM:5][END]\nResult: Error\nInput: 1/0\nTree:(/1 0)\nTokens:[NUM:1][OP:/][NUM:0][END]\nResult: Error\n"""

# Handle binary operators, unary negation and parenthesis (nested to depth)
OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '%': operator.mod,
    '^': operator.xor,
}

# Handle each level of operator precendence by its own function
operator_precedence = {
    '+': (1, 'Left'),
    '-': (1, 'Left'),
    '*': (2, 'Left'),
    '/': (2, 'Left'),
    '%': (2, 'Left'),
    'implicit_multiplication': (2, 'Left'),
    'unary_minus': (3, 'Prefix'),
    'unary_plus': (3, 'Prefix'),
    '^': (4, 'Right'),
}
# Does not support unary +; produce an error
if 'unary_plus' in operator_precedence:
    del operator_precedence['unary_plus']
else:
  print("Error")

# Tokenize math expressions from file
def tokenize_math_expression(expr):
  """
  Tokenizes mathematical expression into numbers, operators, parentheses.
  """
  tokens = re.findall(r'\d+\.?\d*|[+\-*/%^()]', expr) # Using this regex tokenizes 3 + 5' as ['3', '+', '5'], '-(3 + 4)' as ['-', '(', '3', '+', '4', ')'],
  # and '--5' as ['-', '-', '5'].
  print(tokens) # Display tokens
  return tokens

# Define precedence function and op_taken as parameter to return a single token
def precedence(op_token): 
  return operator_precedence.get(op_token, 0) # Calls the operator_precedence dictionary and return 0 for unknown/unhandled tokens

def unary_op_function(op_token): # Function looks up in the `UNARY_OPERATORS` dictionary.
# Was initially expr as a string but changed it to op_token to specify that a single token is returned
  return operator_precedence.get(op_token, None) # Returns 0 if none


# Expression tree correct for all cases from output file, including unary negation, parentheses, and operator precedence.
def extract_math_expressions(raw_content):
  """
  Extracts actual mathematical expressions (lines starting with 'Input: ')
  from the raw content string.
  """
  expressions_list = []
  for line in raw_content.splitlines():
      if line.startswith("Input: "):
          expressions_list.append(line.replace("Input: ", "").strip())
  return expressions_list


def tokenize(expression_str):
  """
  Tokenize the mathematical expression into [TYPE:value] format.
  Returns a string of tokens or [END:error].
  """

  # Define token pattens in a dictionary
  token_spec = [
      ("NUM", r'\d+\.\d+|\d+'), # Integer or decimal number
      ("OP", r'[+\-*/^@]'), # Arithmetic operators, added @ for MatMult
      ("LPAREN", r'\('), # Left parenthesis - Corrected escaping
      ("RPAREN", r'\)'), # Right parenthesis - Corrected escaping
      ("SKIP", r'\s+'), # Skip whitespace - Corrected escaping
      ("ERROR", r'.') # Any other character is an error
  ]

  tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
  get_token = re.compile(tok_regex).match

  tokens = []
  pos = 0
  while pos < len(expression_str):
    match = get_token(expression_str, pos)
    if not match:
      tokens.append({'type': 'ERROR', 'value': expression_str[pos:]})
      return tokens

    token_type = match.lastgroup
    value = match.group(token_type)

    if token_type == 'SKIP': # Handle whitespace explicitly by not adding it to tokens
      pass
    elif token_type == 'NUM':
      tokens.append({'type': 'NUM', 'value': float(value)})
    elif token_type == 'OP':
      tokens.append({'type': 'OP', 'value': value})
    elif token_type == 'LPAREN':
      tokens.append({'type': 'LPAREN', 'value': value})
    elif token_type == 'RPAREN':
      tokens.append({'type': 'RPAREN', 'value': value})
    elif token_type == 'ERROR':
      tokens.append({'type': 'ERROR', 'value': value})
      return tokens

    pos = match.end()

  tokens.append({'type': 'END', 'value': ''})
  return tokens


def parse_expression_to_ast(expression_str):
  """
  Parses a single mathematical expression string into an AST node.
  Returns the AST node or an error string if parsing fails.
  """
  try:
    # ast.parse with mode='eval' returns an Expression node, whose value is the actual AST.
    return ast.parse(expression_str, mode='eval').body
  except SyntaxError as e:
    return f"Syntax Error: {e}"
  except Exception as e:
    return f"Parsing Error: {e}"

def display_tree_with_negation(node):
  """
  Recursively generates a string representation of the AST,
  displaying unary negation as 'neg'.
  """
  ast_Constant = ast.Constant # Alias for ast.Constant
  ast_BinOp = ast.BinOp # Alias for ast.BinOp
  ast_UnaryOp = ast.UnaryOp # Alias for ast.UnaryOp
  ast_Expression = ast.Expression # Alias for ast.Expression
  ast_USub = ast.USub # Alias for ast.USub
  ast_Add = ast.Add # Alias for ast.Add
  ast_Sub = ast.Sub # Alias for ast.Sub
  ast_Mult = ast.Mult # Alias for ast.Mult
  ast_Div = ast.Div # Alias for ast.Div
  ast_MatMult = ast.MatMult # Alias for ast.MatMult


  if isinstance(node, ast_Constant):
    return str(node.value)
  elif isinstance(node, ast_BinOp):
    op_str = {
        ast_Add: '+', ast_Sub: '-', ast_Mult: '*',
        ast_Div: '/', ast_MatMult: '@'
    }.get(type(node.op), 'UNKNOWN_BIN_OP')
    left_str = display_tree_with_negation(node.left)
    right_str = display_tree_with_negation(node.right)
    return f"({op_str} {left_str} {right_str})"
  elif isinstance(node, ast_UnaryOp):
    if isinstance(node.op, ast_USub):
      operand_str = display_tree_with_negation(node.operand)
      return f"(neg {operand_str})"
    else:
      return f"(UNKNOWN_UNARY_OP {display_tree_with_negation(node.operand)})"
  elif isinstance(node, ast_Expression):
      return display_tree_with_negation(node.value) # Recurse on the value of the Expression node
  else:
    return f"ERROR: Unsupported node type {type(node).__name__}"


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

def main():
  # Read mathematical expressions from input.txt and output.txt (one per line)
  sample_input = "3 + 5\n2 + 3 * 4\n-(3 + 4)\n--5\n(10 - 2) * 3 + -4 / 2\n3 @ 5\n1 / 0\n"
  sample_output = """Input: 3+5\nTree:(+3 5)\nTokens:[NUM:3][OP:+][NUM:5][END]\nResult: 8\nInput: 2+3*4\nTree:(+2 (*3 4))\nTokens:[NUM:2][OP:+][NUM:3][OP:*][NUM:4][END]\nResult: 14\nInput: -(3+4)\nTree:(neg (+3 4))\nTokens:[OP:-][LPAREN:(][NUM:3][OP:+][NUM:4][RPAREN:)][END]\nResult: -7\nInput: --5\nTree:(neg (neg 5))\nTokens:[OP:-][OP:-][NUM:5][END]\nResult: 5\nInput: (10-2)*3+-4/2\nTree:(+ (* (- 10 2) 3) (/ (- 4) 2))\nTokens:[LPAREN:(][NUM:10][OP:-][NUM:2][RPAREN:)][OP:*][NUM:3][OP:+][OP:-][NUM:4][OP:/][NUM:2][END]\nResult: 20.0\nInput: 3@5\nTree:(@3 5)\nTokens:[NUM:3][OP:@][NUM:5][END]\nResult: Error\nInput: 1/0\nTree:(/1 0)\nTokens:[NUM:1][OP:/][NUM:0][END]\nResult: Error\n"""


  with open("input.txt", "w", encoding="utf-8") as f:
    f.write(sample_input)
  print(f"Sample text input: \n{sample_input}")


  # Display tokenized math expressions
  print("\n" + "="*20, "Tokenized Math Expressions from Input file", "="*20)
  with open("input.txt", "r", encoding="utf-8") as f:
    tokenized_expressions = []
    for line in f:
      line = line.strip()
      if not line: # Skip empty lines
          continue
      print() # Add space between token expressions
      print(f"Tokenized expression: {line}")
      
      # Call the function and assign to variable tokens_for_line
      tokens_for_line = tokenize_math_expression(line)
      tokenized_expressions.append(tokens_for_line)

    print("\n" + "="*20, "Sample Output as Input", "="*20)
    with open("output.txt", "w", encoding="utf-8") as f:
       f.write(sample_output)
    print("Sample output file as input")
    print(f"Input: \n{sample_output}")

    math_expressions_list = extract_math_expressions(sample_output)

    print("\n" + "="*20, "Extracted Expressions", "="*20)
    for i, expr in enumerate(math_expressions_list):
       print(f"{i+1}.{expr}")

    print("\n" + "="*20, "Trees", "="*20)
    for i, expr in enumerate(math_expressions_list):
       aparse = parse_expression_to_ast(expr)

       print(f"Original: '{expr}' ")
       if isinstance(aparse, str):
          print(f" Tree: {aparse}")
       else: 
          print(f" AST: {ast.dump(aparse)}")
          print(f" Custom Tree (with 'neg'): {display_tree_with_negation(aparse)}")
          print("-"*30)

    print("\n" + "="*20, 'Tokenizing' + '='*20)
    tokenized_expressions = []
    for i, expr in enumerate(math_expressions_list):
       tokens = tokenize(expr)
       tokenized_expressions.append(tokens)
       print()
       print(f" Tokens for '{expr}': {tokens}")

    print("\n" + "="*20, 'Results' + '='*20)
    aparser_results = parse_results(sample_output)
    print(f"Computed results output: \n{aparser_results.strip()}")
   
main() 











    

       
