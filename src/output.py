#!/usr/bin/env python3

import json
from pathlib import Path
from typing import Any
from llm_sdk.llm_sdk import Small_LLM_Model
from src.get_llm_response import get_response

RESET = "\033[0m"
CYAN = "\033[36m"
GREEN = "\033[32m"


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

    print()

    for k in range(len(params["prompts"])):
        # Update the output_content for each prompt
        prompt: dict[str, str] = params["prompts"][k]

        print(f"{CYAN}Prompt: {k + 1}/{len(params["prompts"])}{RESET}")
        print(f"{GREEN}-> '{prompt.prompt}':\n{RESET}")
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
