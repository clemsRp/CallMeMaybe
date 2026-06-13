#!/usr/bin/env python3

import re
from llm_sdk.llm_sdk import Small_LLM_Model


def get_allowed_parts(
            llm: Small_LLM_Model,
            vocab: dict[str, int]
        ) -> dict[str, set[int]]:
    '''
    Return the allowed parts for the constrained decoding part

    Args:
        vocab: dict[str, int] = All the possible tokens
    Return:
        res: dict[str, set[int]] = The allowed parts
    '''
    res: dict[str, set[int]] = {}

    res["number"] = {
        llm.encode(word)[0].tolist()[0] for word in vocab.keys()
        if re.fullmatch('^[0-9-.,]+$', word)
    }

    res["integer"] = {
        llm.encode(word)[0].tolist()[0] for word in vocab.keys()
        if re.fullmatch('^[0-9-,]+$', word)
    }

    possible_str = '^[a-zA-Z0-9àâäéèêëïîôöùûüçÀÂÄÉÈÊËÏÎÔÖÙÛÜÇs.,!?\'"-]+$'
    res["string"] = {
        llm.encode(word)[0].tolist()[0] for word in vocab.keys()
        if re.fullmatch(possible_str, word)
    }

    return res


def get_allowed_fn_name(
            llm: Small_LLM_Model, vocab: dict[str, int],
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
    correct_funcs: list[str] = [
        func for func in func_names if func.startswith(current_fn_name)
    ]

    res: set[int] = {
        word for word in vocab.values() if any([
            func[len(current_fn_name):].startswith(llm.decode([word]))
            for func in correct_funcs
        ])
    }

    if not res:
        return set(range(len(vocab)))

    return res
