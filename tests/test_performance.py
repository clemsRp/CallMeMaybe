#!/usr/bin/env python3

import pytest
import time
import json
from typing import Any
from llm_sdk.llm_sdk import Small_LLM_Model
from src.constrained import get_allowed_parts
from src.context import get_context_fn_name
from src.pipeline import get_output_content


@pytest.fixture(scope="session")
def real_llm() -> Small_LLM_Model:
    """
    Fixture providing a shared real Small_LLM_Model instance.

    Return:
        Small_LLM_Model = An active instance of the model runner.
    """
    return Small_LLM_Model(model_name="Qwen/Qwen3-0.6B")


@pytest.fixture(scope="session")
def performance_environment(
    real_llm: Small_LLM_Model
) -> dict[str, Any]:
    """
    Prepares a clean environment layout to execute
    baseline performance benchmarks.

    Args:
        real_llm: Small_LLM_Model = The shared LLM instance fixture.
    Return:
        dict[str, Any] = Dictionary containing pipeline-ready elements.
    """
    vocab_path: str = real_llm.get_path_to_vocab_file()
    vocab: dict[str, int] = json.load(open(vocab_path))
    words: list[int] = list(vocab.values())
    allowed_parts: dict[str, set[int]] = get_allowed_parts(real_llm, vocab)

    funcs_raw = (
        '[\n'
        '  {\n'
        '    "name": "fn_add",\n'
        '    "description": "Compute sum",\n'
        '    "parameters": {\n'
        '      "a": {"type": "number"}\n'
        '    },\n'
        '    "returns": {"type": "number"}\n'
        '  }\n'
        ']'
    )

    # Creating a simple mock class to reflect a structural Prompt object
    class MockPrompt:
        def __init__(self, text: str) -> None:
            self.prompt = text

    params = {"prompts": [MockPrompt("Add 5 and 3")]}
    context = get_context_fn_name("fn_add")

    return {
        "llm": real_llm,
        "vocab": vocab,
        "words": words,
        "allowed_parts": allowed_parts,
        "funcs": funcs_raw,
        "context": context,
        "params": params
    }


def test_pipeline_execution_speed(
    performance_environment: dict[str, Any]
) -> None:
    """
    Assert that processing a regular prompt
    stays within performance thresholds.

    Args:
        performance_environment: dict[str, Any] = Environment details fixture.
    Return:
        None
    """
    env = performance_environment

    start_time = time.perf_counter()

    # Triggering execution flow for a standard input query
    _ = get_output_content(
        params=env["params"],
        llm=env["llm"],
        vocab=env["vocab"],
        words=env["words"],
        allowed_parts=env["allowed_parts"],
        funcs=env["funcs"],
        context=env["context"]
    )

    end_time = time.perf_counter()
    execution_duration = end_time - start_time

    # Output metric details in terminal using standard capture (pytest -s)
    print(f"\n[BENCHMARK] Token generation latency: {execution_duration:.4f}s")

    # Hard threshold limit set to 15.0 seconds maximum for processing a prompt
    assert execution_duration < 15.0
