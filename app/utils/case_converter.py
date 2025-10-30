

def camel_to_snake_case(camel_case_string: str) -> str:
    result = []
    for ind, char in enumerate(camel_case_string):
        if ind and char.isupper():
            nxt_idx = ind + 1
            flag = nxt_idx >= len(camel_case_string) or camel_case_string[nxt_idx].isupper()
            prev_char = camel_case_string[ind - 1]
            if prev_char.isupper() and flag:
                pass
            else:
                result.append('_')
        result.append(char.lower())
    return ''.join(result)