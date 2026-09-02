import os


#===========================================
# Master Function
#===========================================
def evaluate_file(input_path: str) -> list[dict]:

    f = open(input_path, 'r')
    lines = f.read().splitlines()

    results = []
    blocks = []

    for line in lines:
        expr_str = line

        # tokenise
        tokens = tokenize(expr_str)
        if tokens is None:
            res = {
                "input": expr_str,
                "tree": "ERROR",
                "tokens": "ERROR",
                "result": "ERROR"
            }
            results.append(res)
            blocks.append(format_block(res))
            continue

        tokens_str = format_tokens(tokens)

        # parse
        try:
            tree = parse(tokens)
        except ValueError:
            res = {
                "input": expr_str,
                "tree": "ERROR",
                "tokens": tokens_str,
                "result": "ERROR"
            }
            results.append(res)
            blocks.append(format_block(res))
            continue

        tree_str = format_tree(tree)

        # evaluate
        try:
            result_val = evaluate_tree(tree)
        except (ZeroDivisionError, OverflowError, ValueError):
            result_val = "ERROR"

        res = {
            "input": expr_str,
            "tree": tree_str,
            "tokens": tokens_str,
            "result": result_val
        }
        results.append(res)
        blocks.append(format_block(res))

    # write output file
    output_path = os.path.join(os.path.dirname(input_path), "output.txt")
    with open(output_path, 'w') as f:
        f.write("\n\n".join(blocks) + "\n")

    return results

#===========================================
# Tokeniser
#===========================================
def tokenize(expr):
    tokens = []
    i = 0
    n = len(expr)
    while i < n:
        c = expr[i]
        if c.isspace():     # skip spaces
            i += 1
            continue
        if c.isdigit():     # numbers
            num = c
            i += 1
            while i < n and expr[i].isdigit():
                num += expr[i]
                i += 1
            if i < n and expr[i] == '.':        # numbers with decimal
                if i + 1 < n and expr[i + 1].isdigit():
                    num += '.'
                    i += 1
                    while i < n and expr[i].isdigit():
                        num += expr[i]
                        i += 1
                else:       # for invalid 
                    return None     
            tokens.append(("NUM", num))
            continue
        if c in "+-*/%^":       # operators
            tokens.append(("OP", c))
            i += 1
            continue
        if c == '(':        # L parenthesis
            tokens.append(("LPAREN", c))
            i += 1
            continue
        if c == ')':        # R parenthesis
            tokens.append(("RPAREN", c))
            i += 1
            continue
        return None     # for invalid
    tokens.append(("END", ""))      # add an "END" token
    return tokens


def format_tokens(tokens):      # returns list of "[typ:val]" items eg. [NUM:3]
    parts = []
    for typ, val in tokens:
        if typ == "END":
            parts.append("[END]")
        else:
            parts.append(f"[{typ}:{val}]")
    return " ".join(parts)

#===========================================
# Recursive Descent Parser
#===========================================
def parse(tokens):
    pos = [0]

    # check token
    def peek():     
        return tokens[pos[0]]

    # move to next token
    def consume():      
        tok = tokens[pos[0]]
        pos[0] += 1
        return tok

    # numbers and parentheses
    def parse_primary():
        tok = peek()
        if tok[0] == "NUM":
            consume()
            return float(tok[1])
        elif tok[0] == "LPAREN":
            consume()
            expr = parse_expression()       # parse inside expression
            if peek()[0] != "RPAREN":
                raise ValueError("Expected closing parenthesis")
            consume()
            return expr
        else:
            raise ValueError("Unexpected token in primary")

    # exponents - level 4
    def parse_exponent():
        left = parse_primary()
        if peek()[0] == "OP" and peek()[1] == "^":
            consume()
            right = parse_unary()   # right side can be unary (eg. 2^-2)
            return ("^", left, right)
        return left

    # unary minus - level 3
    def parse_unary():
        if peek()[0] == "OP" and peek()[1] == "-":
            consume()
            operand = parse_unary()
            return ("neg", operand)
        return parse_exponent()

    # multiply|divide - level 2
    def parse_term():
        left = parse_unary()
        while True:
            if peek()[0] == "OP" and peek()[1] in ("*", "/", "%"):      # explicit * / %
                op = consume()[1]
                right = parse_unary()
                left = (op, left, right)
            elif peek()[0] == "LPAREN":     # implicit multiplication when an opening parenthesis follows
                right = parse_unary()
                left = ("*", left, right)
            else:
                break
        return left

    # plus|minus - level 1
    def parse_expression():
        left = parse_term()
        while peek()[0] == "OP" and peek()[1] in ("+", "-"):
            op = consume()[1]
            right = parse_term()
            left = (op, left, right)
        return left

    tree = parse_expression()
    if peek()[0] != "END":
        raise ValueError("Extra tokens after expression")
    return tree

# formats tree into (+ 2 (* 3 4)) notation
def format_tree(tree):
    if isinstance(tree, float):
        if tree.is_integer():
            return str(int(tree))
        return str(tree)
    elif isinstance(tree, tuple):
        if len(tree) == 2 and tree[0] == "neg":
            return f"(neg {format_tree(tree[1])})"
        elif len(tree) == 3:
            op, left, right = tree
            return f"({op} {format_tree(left)} {format_tree(right)})"
    raise ValueError("Invalid tree")

# calculates numerical value of tree 
def evaluate_tree(tree):
    if isinstance(tree, float):
        return tree
    elif isinstance(tree, tuple):       
        if len(tree) == 2 and tree[0] == "neg":
            return -evaluate_tree(tree[1])
        elif len(tree) == 3:
            op, left, right = tree
            lval = evaluate_tree(left)
            rval = evaluate_tree(right)
            if op == "+":
                return lval + rval
            elif op == "-":
                return lval - rval
            elif op == "*":
                return lval * rval
            elif op == "/":
                if rval == 0:
                    raise ZeroDivisionError("Division by zero")
                return lval / rval
            elif op == "%":
                if rval == 0:
                    raise ZeroDivisionError("Modulo by zero")
                return lval % rval
            elif op == "^":
                return lval ** rval
            else:
                raise ValueError("Unknown operator")
    raise ValueError("Invalid tree")

# format results
def format_block(res):
    result_display = res["result"]
    if isinstance(result_display, float):
        if result_display.is_integer():
            result_display = str(int(result_display))
        else:
            result_display = f"{result_display:.4f}"
    else:
        result_display = str(result_display)

    # return list of dictionaries
    return "\n".join([
        f"Input: {res['input']}",
        f"Tree: {res['tree']}",
        f"Tokens: {res['tokens']}",
        f"Result: {result_display}"
    ])


# TO BE DELETED
evaluate_file("input.txt")
print(evaluate_file("input.txt"))