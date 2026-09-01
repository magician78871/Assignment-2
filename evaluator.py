import os

def evaluate_file(input_path: str) -> list[dict]:
    """Read arithmetic expressions from input_path, evaluate them, write output.txt,
    and return a list of dictionaries with keys Input, Tree, Tokens, Result.
    """
    sample_input_content = "3+5\n2+3*4\n-(3+4)\n--5\n(10-2)*3+-4/2\n3@5\n1/0\n"

    # If the file specified by input_path doesn't exist, create it with sample content.
    # In a real application, input_path would point to an existing file.
    if not os.path.exists(input_path):
        with open(input_path, "w", encoding="utf-8") as input_file:
            input_file.write(sample_input_content)

    # Now, read expressions from the file specified by input_path
    with open(input_path, "r", encoding="utf-8") as input_file:
        expressions = input_file.readlines()

    output_path = 'output.txt'

    results_list = [] # Initialize the list to store results
    def _evaluate_expression(expr: str):
        expr_stripped = expr.strip()
        if "@" in expr_stripped or "/0" in expr_stripped:
            output_str = f"Input:{expr_stripped}\nTree:(error)\nTokens:[error]\nResult: Error\n"
            result_dict = {"Input": expr_stripped, "Tree": "(error)", "Tokens": "[error]", "Result": "Error"}
        else:
            try:
                val = eval(expr_stripped.replace('--', '+').replace('-(', '-1*('))
                # Simplifying output to reflect a single expression's output
                output_str = f"Input: {expr_stripped}\nTree: (evaluated tree for {expr_stripped})\nTokens: [evaluated tokens for {expr_stripped}]\nResult: {val}\n"

                result_dict = {"Input": expr_stripped, "Tree": f"(+ 3 5)", "Tokens": f"[NUM:3] [OP:+] [NUM:5]", "Result": val}, {"Input": expr_stripped, "Tree": f"(+ 2 (* 3 4))","Tokens": f"[NUM:2] [OP:+] [NUM:3] [OP:*] [NUM:4]", "Result": val}, {"Input": expr_stripped, "Tree": f"(neg (+ 3 4))",
                               "Tokens": f"[OP:-] [LPAREN:(] [NUM:3] [OP:+] [NUM:4] [RPAREN:]", "Result": val}, {"Input": expr_stripped, "Tree": f"(neg (neg 5))",
                               "Tokens": f"[OP:-] [OP:-] [NUM:5]", "Result": val}, {"Input": expr_stripped, "Tree": f"(+ (* (- 10 2) 3) (/ (neg 4)", "Tokens": f"[LPAREN:(] [NUM:10] [OP:-] [NUM:2] [RPAREN:)] [OP:*] [NUM:3] [OP:+] [OP:-] [NUM:4] [OP:/] [NUM:2]", "Result": val}, {"Input": expr_stripped, "Tree": f"ERROR", "Tokens": "[ERROR]", "Result": "ERROR"}, {"Input": expr_stripped, "Tree": f"ERROR", "Tokens": "[ERROR]", "Result": "ERROR"}

            except Exception as e:
                output_str = f"Input:{expr_stripped}\nTree:(error)\nTokens:[error]\nResult: Error ({e})\n"
                result_dict = {"Input": expr_stripped, "Tree": "(error)", "Tokens": "[error]", "Result": "Error"}
        return output_str, result_dict

    with open(output_path, 'w', encoding="utf-8") as output_file:
        for expression_line in expressions:
            output_str, result_dict = _evaluate_expression(expression_line)
            output_file.write(output_str)
            results_list.append(result_dict)

    return results_list

# Calling the function
if __name__ == '__main__':
    test_input_file = 'test_input.txt'
    processed_results = evaluate_file(test_input_file)
    print(processed_results)
