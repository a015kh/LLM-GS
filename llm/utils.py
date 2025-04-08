from __future__ import annotations
import re

from prog_policies.base import dsl_nodes
from prog_policies.base import BaseDSL
from typing import List
import numpy as np

from .karel_prompt import KAREL_ACTION_DESC_LIST_DSL, KAREL_PERCEPTION_DESC_LIST_DSL
from .minigrid_prompt import MINIGRID_ACTION_DESC_LIST_DSL, MINIGRID_PERCEPTION_DESC_LIST_DSL

KAREL_ACTIONS = [a.split(":")[0] for a in KAREL_ACTION_DESC_LIST_DSL]
KAREL_PERCEPTIONS = [p.split(":")[0] for p in KAREL_PERCEPTION_DESC_LIST_DSL]
MINIGRID_ACTIONS = [a.split(":")[0] for a in MINIGRID_ACTION_DESC_LIST_DSL]
MINIGRID_PERCEPTIONS = [p.split(":")[0] for p in MINIGRID_PERCEPTION_DESC_LIST_DSL]
MINIGRID_OBJECTS = ["lava", "door", "ball", "box"]
MINIGRID_COLORS = ["red", "blue"]

INDENT = "    "
PROGRAM_FORMAT = "DEF run m( ", " m)"
WHILE_FORMAT = "WHILE c( ", " c) w( ", " w)"
IF_FORMAT = "IF c( ", " c) i( ", " i)"
IFELSE_FORMAT = "IFELSE c( ", " c) i( ", " i) ELSE e( ", " e)"
REPEAT_FORMAT = "REPEAT R=", " r( ", " r)"
CONDITION_FORMAT = "not c( ", " c)"
PERCEPTION_FORMAT = "h( ", " h)"

def count_indent(str: str) -> int:
    return str.count("    ")


def remove_one_indent(str: str) -> str:
    return str.replace("    ", "", 1)


def remove_brackets_and_colon(code: str) -> str:
    return code.replace("(", "").replace(")", "").replace(":", "")


def remove_quotes(code: str) -> str:
    return code.replace("\"", "").replace("'", "")

def convert_action(code: str) -> str:
    return " " + code.replace("(", "").replace(")", "") + " "

def convert_condition(code: str) -> str:
    
    code = remove_quotes(code)
    dsl_code = ""
    dsl_code = code.split(" ")[-1]
    
    if "front_object_type" in dsl_code:
        ot = dsl_code.split("(")[1].split(")")[0]
        dsl_code = f"front_object_type h( {ot} h)"
    elif "front_object_color" in dsl_code:
        color = dsl_code.split("(")[1].split(")")[0]
        dsl_code = f"front_object_color h( {color} h)"
    else:
        dsl_code = remove_brackets_and_colon(code.split(" ")[-1])
    
    if "not" in code:
        dsl_code = CONDITION_FORMAT[0] + dsl_code + CONDITION_FORMAT[1]
    else:
        dsl_code = dsl_code
    return dsl_code

def convert_expression(code: List[str]) -> str:
    # case 1: action
    # case 2: repeat
    # case 3: while
    # case 4: ifelse
    # case 5: if

    levels = np.array([count_indent(line) for line in code])
    expressions = np.where(levels == 0)[0]

    dsl_code = ""
    if len(code) == 1:  # case action
        dsl_code += convert_action(code[0])
    if "for" in code[0]:  # case repeat
        n = code[0].split(" ")[-1].split("(")[1].split(")")[0]
        dsl_code += REPEAT_FORMAT[0] + str(n) + REPEAT_FORMAT[1]
        code = [remove_one_indent(line) for line in code[1:]]
        dsl_code += convert(code)
        dsl_code += REPEAT_FORMAT[2]
    elif "while" in code[0]:  # case while
        dsl_code += WHILE_FORMAT[0]
        dsl_code += convert_condition(code[0])
        dsl_code += WHILE_FORMAT[1]
        code = [remove_one_indent(line) for line in code[1:]]
        dsl_code += convert(code)
        dsl_code += WHILE_FORMAT[2]
    elif "if" in code[0]:  # case if or ifelse
        is_else = len(expressions) == 2
        if is_else:
            dsl_code += IFELSE_FORMAT[0]
            dsl_code += convert_condition(code[0])
            dsl_code += IFELSE_FORMAT[1]
            else_index = expressions[1]
            dsl_code += convert(
                [remove_one_indent(line) for line in code[1:else_index]]
            )
            dsl_code += IFELSE_FORMAT[2]
            dsl_code += convert(
                [remove_one_indent(line) for line in code[else_index + 1 :]]
            )
            dsl_code += IFELSE_FORMAT[3]
        else:
            dsl_code += IF_FORMAT[0]
            dsl_code += convert_condition(code[0])
            dsl_code += IF_FORMAT[1]
            code = [remove_one_indent(line) for line in code[1:]]
            dsl_code += convert(code)
            dsl_code += IF_FORMAT[2]
    return " " + dsl_code + " "


def convert(code: List[str]):
    dsl_code = ""
    levels = np.array([count_indent(line) for line in code])
    expressions = np.where(levels == 0)[0]
    if len(expressions) == 1:
        dsl_code += convert_expression(code)
    else:
        for i in range(len(expressions) - 1):
            # check if the expression is if-else
            if "else" in code[expressions[i + 1]]:
                if i + 2 == len(expressions):
                    dsl_code += convert_expression(code[expressions[i] :])
                else:
                    dsl_code += convert_expression(
                        code[expressions[i] : expressions[i + 2]]
                    )
            else:
                dsl_code += convert_expression(
                    code[expressions[i] : expressions[i + 1]]
                )
        if "else" not in code[expressions[-1]]:
            dsl_code += convert_expression(code[expressions[-1] :])
    return dsl_code


def clear_reduntant_spaces(code: str) -> str:
    return " ".join(code.split())


def indent_python_to_str(code: str) -> str:
    code = code.strip("\n")
    code = code.split("\n")[1:]
    code = [remove_one_indent(line) for line in code]
    dsl_code = PROGRAM_FORMAT[0]
    dsl_code += clear_reduntant_spaces(convert(code))
    dsl_code += PROGRAM_FORMAT[1]
    return dsl_code


def parse_program_str_list(program_str_list: list[str], dsl: BaseDSL) -> list[dsl_nodes.Program]:
    program_list = []
    for program_str in program_str_list:
        try:
            program_list.append(dsl.parse_str_to_node(program_str))
        except:
            pass
    return program_list

def get_program_str_from_llm_response_python(llm_response, env_name="karel"):
    result = re.findall("```python.*?```", llm_response, flags=re.DOTALL)[0]
    result = result.replace("```python\n", "").replace("\n```", "")
    result = indent_python_to_str(result)
    result = get_program_str_from_llm_response_dsl(result, env_name=env_name)
    return result

def process_action_perception(result: str, env_name: str) -> str:
    if env_name == "karel":
        actions = KAREL_ACTIONS
        perceptions = KAREL_PERCEPTIONS
    elif env_name == "minigrid":
        actions = MINIGRID_ACTIONS
        perceptions = MINIGRID_PERCEPTIONS
    else:
        raise ValueError(f"Unknown environment name: {env_name}")

    for action in actions:
        result = result.replace(f"{action}()", action)
    
    for perception in perceptions:
        result = result.replace(f"{perception}()", perception)
    
    return result

def get_program_str_from_llm_response_dsl(llm_response, env_name="karel"):
    result = ' '.join(llm_response.split())
    result = process_action_perception(result, env_name)
    result = result.replace("\n", " ") \
                   .replace("(", " ( ") \
                   .replace(")", " ) ") \
                   .replace(";", "") \
                   .replace("\"", "") \
                   .replace("\'", "")
    
    for ot in MINIGRID_OBJECTS:
        result = result.replace(f"front_object_type({ot})", f"front_object_type h( {ot} h)")
    for color in MINIGRID_COLORS:
        result = result.replace(f"front_object_color({color})", f"front_object_color h( {color} h)")

    result = result.split()
    result = ' '.join(result).split()
    stack = []
    
    start = 0
    end = len(result)

    for index, word in enumerate(result):
        if word == 'DEF':
            start = index
        if word == '(':
            stack.append(result[index - 1])
        if word == ')':
            symbol = stack[-1]
            if result[index - 1] != symbol:
                result[index] = symbol + result[index]
            stack.pop()
            if symbol == 'm':
                end = index
                break

    result = result[start: end + 1]
    result = ' '.join(result).replace(" (", "(") \
                            .replace(" )", ")") \
                            .split()

    stack = []

    for index, word in enumerate(result):
        if word in ['WHILE', 'IF', 'IFELSE', 'not']:
            if result[index + 1] != 'c(':
                result[index] += ' c('
                stack.append('c(')
        elif word in ['front_object_type', 'front_object_color']:
            if result[index + 1] != 'h(':
                result[index] += ' h('
                stack.append('h(')
        elif word in ['c(', 'h(']:
            stack.append(word)
        else:
            if len(stack) != 0:
                last = stack.pop()
                if result[index + 1] != f"{last.replace('(', ')')}":
                    result[index] += f' {last.replace("(", ")")}'
                   
        if word in ['IF', 'IFELSE']:
            for i in range(index + 1, len(result)):
                if result[i] == 'i(':
                    stack.append('i(')
                elif result[i] == 'i)':
                    if 'i(' in stack:
                        stack.pop()
                        if 'i(' not in stack:
                            if result[i + 1] == 'ELSE':
                                result[index] = result[index].replace('IFELSE', 'IF')
                                result[index] = result[index].replace('IF', 'IFELSE')
                            else:
                                result[index] = result[index].replace('IFELSE', 'IF')
                            break
    
    result = filter(lambda x: x not in ['c', 'i', 'm', 'e', 'r', 'w', '```'], result)
    result = ' '.join(result)
    while True:
        previous_result = result
        result = result.replace("not c( markersPresent c)", "noMarkersPresent") \
                    .replace("not c( noMarkersPresent c)", "markersPresent") \
                    .replace("true", "True") \
                    .replace("false", "False") \
                    .replace("not c( False c)", "True") \
                    .replace("not c( True c)", "False") \
                    .replace("WHILE c( True c) w(", "REPEAT R=19 r(") \
                    .replace("WHILE c( False c) w(", "REPEAT R=0 r(")
        if previous_result == result:
            break
    
    stack = []
    result = result.split(' ')
    for index, word in enumerate(result):
        if '(' in word:
            stack.append(word)
        elif ')' in word:
            if len(stack) == 0:
                break
            result[index] = stack[-1].replace('(', ')')
            stack.pop()
        elif '=' in word:
            tmp = word.split('=')
            number = int(tmp[-1])
            tmp[-1] = str(min(max(0, number), 19))
            result[index] = '='.join(tmp)
    
    result = ' '.join(result)

    return result
