#!/usr/bin/env python3

import argparse
import json
from typing import Any
from llm_sdk.llm_sdk import Small_LLM_Model
from src.constrained import get_allowed_parts
from src.parser import get_params
from src.context import get_context_fn_name
from src.output import write_output, get_output_content


def execute_pipeline(args: argparse.ArgumentParser) -> None:
    '''
    Execute the project main pipeline

    Args:
        args: argparse.ArgumentParser = The arguments
    Return:
        None
    '''
    # Init LLM, context and get all vocabulary
    llm: Small_LLM_Model = Small_LLM_Model(model_name=args.model)
    vocab_path: str = llm.get_path_to_vocab_file()
    vocab: dict[str, int] = json.load(open(vocab_path))
    words: list[int] = list(vocab.values())

    # Init the params and the allowed_parts
    params: dict[str, Any] = get_params(
        args.functions_definition,
        args.input
    )
    funcs: str = json.dumps(
        [f.model_dump() for f in params["functions"]],
        indent=2, ensure_ascii=False
    )
    func_names: list[str] = [f.name for f in params["functions"]]
    context_funcs: str = ", ".join(func_names)
    context: str = get_context_fn_name(context_funcs)
    allowed_parts: dict[str, set[int]] = get_allowed_parts(llm, vocab)

    # Init then fill the output_content
    output_content: str = get_output_content(
        params, llm, vocab, words, allowed_parts, funcs, context
    )

    # Write the output_content in the output file
    write_output(args.output, output_content)
