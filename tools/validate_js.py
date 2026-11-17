import sys

def validate_javascript(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    n = len(code)
    i = 0
    line = 1
    col = 1
    
    # Stack stores:
    # ('{', line, col), ('(', line, col), ('[', line, col), ('${', line, col)
    paren_stack = []
    
    # State tracking
    # States: 'CODE', 'SINGLE', 'DOUBLE', 'TEMPLATE', 'REGEX', 'LINE_COMMENT', 'BLOCK_COMMENT'
    # For nested template literals, we can have a stack of template depths
    mode_stack = ['CODE']
    
    errors = []
    
    while i < n:
        c = code[i]
        cur_mode = mode_stack[-1]
        
        if c == '\n':
            line += 1
            col = 1
            i += 1
            continue
            
        if cur_mode == 'CODE':
            if c == '/' and i + 1 < n and code[i+1] == '/':
                # Line comment
                i += 2
                while i < n and code[i] != '\n':
                    i += 1
                continue
            elif c == '/' and i + 1 < n and code[i+1] == '*':
                # Block comment
                i += 2
                start_l = line
                while i + 1 < n and not (code[i] == '*' and code[i+1] == '/'):
                    if code[i] == '\n':
                        line += 1
                        col = 1
                    i += 1
                i += 2
                continue
            elif c == "'":
                mode_stack.append('SINGLE')
                i += 1
            elif c == '"':
                mode_stack.append('DOUBLE')
                i += 1
            elif c == '`':
                mode_stack.append('TEMPLATE')
                i += 1
            elif c in '({[':
                paren_stack.append((c, line, col))
                i += 1
            elif c in ')}]':
                if not paren_stack:
                    errors.append(f"Unexpected closing '{c}' at line {line}, col {col}")
                else:
                    top_char, top_line, top_col = paren_stack.pop()
                    if top_char == '${':
                        if c != '}':
                            errors.append(f"Mismatched bracket: opened '${{' at line {top_line}, col {top_col} but closed with '{c}' at line {line}, col {col}")
                        else:
                            # Popping '${' also exits the 'CODE' mode back to 'TEMPLATE'
                            if len(mode_stack) > 1 and mode_stack[-1] == 'CODE':
                                mode_stack.pop()
                    else:
                        expected = {'(': ')', '{': '}', '[': ']'}.get(top_char)
                        if expected != c:
                            errors.append(f"Mismatched bracket: opened '{top_char}' at line {top_line}, col {top_col} but closed with '{c}' at line {line}, col {col}")
                i += 1
            else:
                i += 1
                
        elif cur_mode in ('SINGLE', 'DOUBLE'):
            quote_char = "'" if cur_mode == 'SINGLE' else '"'
            if c == '\n':
                errors.append(f"Unterminated string literal at line {line}, col {col}")
                mode_stack.pop()
                line += 1
                col = 1
                i += 1
                continue
            elif c == '\\':
                i += 2
                col += 2
                continue
            elif c == quote_char:
                mode_stack.pop()
                i += 1
                col += 1
                continue
            else:
                i += 1
                col += 1
                continue
                
        elif cur_mode == 'TEMPLATE':
            if c == '\\':
                i += 2
            elif c == '`':
                mode_stack.pop()
                i += 1
            elif c == '$' and i + 1 < n and code[i+1] == '{':
                paren_stack.append(('${', line, col))
                mode_stack.append('CODE')
                i += 2
            else:
                i += 1
        col += 1

    if paren_stack:
        for p, l, c in paren_stack[-10:]:
            errors.append(f"Unclosed '{p}' opened at line {l}, col {c}")
            
    if len(mode_stack) > 1:
        errors.append(f"Unclosed string/template literal mode: {mode_stack[1:]}")
        
    print(f"Total lines: {line}")
    print(f"Errors count: {len(errors)}")
    for err in errors[:25]:
        print(f"  ❌ {err}")
    return len(errors) == 0

if __name__ == '__main__':
    validate_javascript('ui/app.js')
