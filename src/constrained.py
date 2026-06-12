#!/usr/bin/env python3

import re


def get_allowed_parts(vocab: dict[str, int]) -> dict[str, set[int]]:
    '''
    Return the allowed parts for the constrained decoding part

    Args:
        vocab: dict[str, int] = All the possible tokens
    Return:
        res: dict[str, set[int]] = The allowed parts
    '''
    res: dict[str, set[int]] = {}

    words = list(vocab.keys())

    res["number"] = {
        k for k in range(len(vocab)) if re.fullmatch('^[0-9-.,]+$', words[k])
    }

    possible_str = '^[a-zA-Z0-9àâäéèêëïîôöùûüçÀÂÄÉÈÊËÏÎÔÖÙÛÜÇs.,!?\'"-]+$'
    res["string"] = {
        k for k in range(len(vocab)) if re.fullmatch(possible_str, words[k])
    }

    return res


def get_allowed_fn_name(
            vocab: dict[str, int],
            func_names: list[str], current_fn_name: str
        ) -> set[int]:
    '''
    Return the allowed tokens for the fn_name

    Args:
        vocab: dict[str, int] = The vocab
        func_names: list[str] = The available functions
        current_fn_name: str = The current valu of the generated fn_name
    Return:
        None
    '''
    words: list[str] = list(vocab.keys())
    correct_funcs: list[str] = [
        func for func in func_names if func.startswith(current_fn_name)
    ]
    res: set[int] = {
        k for k in range(len(vocab)) if any([
            func[len(current_fn_name):].startswith(words[k])
            for func in correct_funcs
        ])
    }

    if not res:
        return set(range(len(vocab)))

    return res
