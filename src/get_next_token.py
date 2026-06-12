#!/usr/bin/env python3

from llm_sdk.llm_sdk import Small_LLM_Model


def get_next_token(
            llm: Small_LLM_Model, words: list[int],
            prompt: list[int], allowed: set[int]
        ) -> list[int]:
    '''
    Return the most probable token use at the end of the prompt

    Args:
        llm: Small_LLM_Model = The LLM model use
        vocab: dict[str, int] = The dictionary of the words and their token
        words: list[int] = All the possible tokens
        prompt: str = The prompt send to the LLM
        allowed: set[int] = The authorized tokens depending on the arg_type
        arg_type: str = The type of the needed argument
    Return:
        token: int = The next token to add to the prompt and the LLM response
    '''
    logits = llm.get_logits_from_input_ids(prompt)
    index = max(allowed, key=lambda i: logits[i])
    res = words[index]
    return [res]
