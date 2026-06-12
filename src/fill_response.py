#!/usr/bin/env python3

from llm_sdk.llm_sdk import Small_LLM_Model
from src.get_next_token import get_next_token
from src.constrained import get_allowed_fn_name


def get_fn_name(
            llm: Small_LLM_Model, vocab: dict[str, int],
            words: list[int], final_prompt: str, func_names: list[str]
        ) -> str:
    '''
    Return the LLM response for the fn_name

    Args:
        llm: Small_LLM_Model = The LLM model used
        vocab: dict[str, int] = The available vocabulary
        final_prompt: str = The prompt the LLM will answer
        allowed: set[int] = Authorized tokens
    Return:
        res: str = The fn_name
    '''
    res: str = ""
    prompt: str = final_prompt
    while '"' not in res:
        # Update res with the fn_name
        allowed: set[int] = get_allowed_fn_name(vocab, func_names, res)
        llm_prompt: list[int] = llm.encode(prompt)[0].tolist()
        res += llm.decode(get_next_token(
            llm, words, llm_prompt, allowed
        ))
        prompt = final_prompt + res

    if res[-2] != ",":
        res = res[:-1] + "," + res[-1]

    return res


def get_arg(
            llm: Small_LLM_Model, vocab: dict[str, int],
            words: list[int], final_prompt: str,
            arg_type: str, allowed_parts: dict[str, set[int]]
        ) -> str:
    '''
    Return the next argument

    Args:
        llm: Small_LLM_Model = The LLM model used
        vocab: dict[str, int] = The available vocabulary
        final_prompt: str = The prompt send to the LLM
        arg_type: str = The type of the next argument
        allowed_parts: dict[str, set[int]] = Authorized tokens
    Return:
        res: str = The next argument
    '''
    res: str = ""
    allowed: set[int] = allowed_parts[arg_type["type"]]

    current_prompt = final_prompt

    if arg_type["type"] == "string":
        res += '"'
        current_prompt += '"'

    while True:
        llm_prompt: list[int] = llm.encode(current_prompt)[0].tolist()
        token_decoded = llm.decode(get_next_token(
            llm, words, llm_prompt, allowed
        ))

        if not token_decoded:
            break

        res += token_decoded
        current_prompt += token_decoded

        if arg_type["type"] == "string" and '"' in token_decoded:
            break

        if arg_type["type"] == "number" and \
                (',' in token_decoded or '}' in token_decoded):
            break

    res = res.strip()

    if arg_type["type"] == "string":
        if not res.startswith('"'):
            res = '"' + res
        if res.count('"') == 1:
            res += '"'
        elif res.count('"') > 2:
            cleaned = res.replace('"', '')
            res = f'"{cleaned}"'
    else:
        import re
        res = re.sub(r'[^0-9.-]', '', res)

    if not res.startswith(" "):
        res = " " + res

    return res


def get_args(
            llm: Small_LLM_Model, vocab: dict[str, int], words: list[int],
            args_types: dict[str, str], final_prompt: str,
            allowed_parts: dict[str, set[int]]
        ) -> str:
    '''
    Return the LLM response for the args

    Args:
        llm: Small_LLM_Model = The LLM model used
        vocab: dict[str, int] = The available vocabulary
        args_types: dict[str, str] = Inofrmations about args
        final_prompt: str = The prompt the LLM will answer
        allowed_parts: Dict[str, set[int]] = Authorized tokens
    Return:
        res: str = The args
    '''
    res: str = ""
    for (arg, arg_type) in args_types.items():
        # Update res with the args keys
        res += f'"{arg}":'
        prompt: str = final_prompt + res
        arg_res: str = get_arg(
            llm, vocab, words, prompt, arg_type, allowed_parts
        )

        if arg_type["type"] == "number" and "." not in arg_res:
            arg_res += ".0"

        res += arg_res
        if res[-1] == ",":
            res += " "
        elif res[-2:] != ", ":
            res += ", "

    res = res[:-2]

    if res != "" and res[-1] == ",":
        res = res[:-1]
    if "}" not in res:
        res += "}"

    return res
