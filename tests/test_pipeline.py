#!/usr/bin/env python3

import json
import os
from typing import Any
import pytest
from llm_sdk.llm_sdk import Small_LLM_Model
from src.get_llm_response import get_response


@pytest.mark.skipif(
    not os.getenv("RUN_INTEGRATION_TESTS"),
    reason="Heavy test requiring local Hugging Face model download"
)
def test_end_to_end_json_generation() -> None:
    """
    Verify that the constrained decoding pipeline
    produces a valid JSON structure.

    Return:
        None
    """
    # Initialize the default lightweight model used for standard execution
    model_name: str = "Qwen/Qwen2.5-0.5B-Instruct"
    llm: Small_LLM_Model = Small_LLM_Model(model_name=model_name)

    # Extract required structural metadata mappings from the tokenizer pipeline
    vocab_path: str = llm.get_path_to_vocab_file()
    with open(vocab_path, "r", encoding="utf-8") as f:
        vocab: dict[str, int] = json.load(f)

    words: list[int] = list(vocab.values())

    # Mock dynamic functions definitions for tool calling validation
    mock_functions: list[dict[str, Any]] = [
        {
            "name": "fn_add_numbers",
            "description": "Add two numbers Together",
            "parameters": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            }
        }
    ]

    prompt: str = "Can you add 15 and 30 for me?"

    # Execute the core constraint pipeline to generate structural output text
    generated_output: str = get_response(
        llm=llm,
        vocab=vocab,
        words=words,
        prompt=prompt,
        functions=mock_functions
    )

    assert generated_output is not None
    assert "fn_add_numbers" in generated_output

    # Attempt parsing validation to guarantee structural integrity of the JSON
    try:
        data: dict[str, Any] = json.loads(generated_output)
        assert "parameters" in data
        assert "a" in data["parameters"]
        assert "b" in data["parameters"]
    except json.JSONDecodeError:
        pytest.fail("The constrained output string is not a valid JSON object")
