#!/usr/bin/env python3

import argparse
import json
import time
from typing import Any
from pathlib import Path
from llm_sdk.llm_sdk import Small_LLM_Model
from src.constrained import get_allowed_parts
from src.parser import get_params
from src.context import get_context_fn_name
from src.get_llm_response import get_response
from src.models import Prompt

RESET = "\033[0m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"


def execute_pipeline(args: argparse.Namespace) -> None:
    '''
    Execute the project main pipeline

    Args:
        args: argparse.ArgumentParser = The arguments
    Return:
        None
    '''
    # Init the params and the allowed_parts
    params: dict[str, Any] = get_params(
        args.functions_definition,
        args.input
    )

    # Init LLM, context and get all vocabulary
    llm: Small_LLM_Model = Small_LLM_Model(model_name=args.model)

    try:
        vocab_path: str = llm.get_path_to_vocab_file()
        with open(vocab_path, "r", encoding="utf-8") as f:
            vocab: dict[str, int] = json.load(f)

    except Exception as e:
        from src.parser import handle_error
        handle_error(
            "Model Vocabulary Error",
            f"An error occured while reading the vocabulary: {e}"
        )

    words: list[int] = list(vocab.values())

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


def get_output_content(
            params: dict[str, Any], llm: Small_LLM_Model,
            vocab: dict[str, int], words: list[int],
            allowed_parts: dict[str, set[int]],
            funcs: str, context: str
        ) -> str:
    '''
    Return the content to write inside the output file

    Args:
        None
    Return:
        content: str = the content to write inside the output file
    '''
    output_content: str = ""
    output_content += "[\n"

    start_time: float = time.time()

    print()

    for k in range(len(params["prompts"])):
        # Update the output_content for each prompt
        prompt: Prompt = params["prompts"][k]

        cur_time: float = round(time.time() - start_time, 2)

        print(f"{CYAN}Prompt: {k + 1}/{len(params['prompts'])}{RESET}")
        print(f"{GREEN}-> '{prompt.prompt}': {YELLOW}{cur_time}s{RESET}\n")
        res: str = get_response(
            llm, vocab, words, allowed_parts,
            json.loads(funcs), context, prompt.prompt
        )

        output_content += res

        if k != len(params["prompts"]) - 1:
            output_content += ","

        print("\n")

        output_content += "\n"
    output_content += "]"

    return output_content


def write_output(output_file: str, output_content: str) -> None:
    '''
    Write the output datas inside the ouput file

    Args:
        output_file: str = The path of the output file
        output_content: str = The content to write inside the output file
    Return:
        None
    '''
    file_path: Path = Path(output_file)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(output_content)
