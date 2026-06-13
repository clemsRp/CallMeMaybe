#!/usr/bin/env python3

import pytest
import json
from typing import Any
from llm_sdk.llm_sdk import Small_LLM_Model
from src.constrained import get_allowed_parts, get_allowed_fn_name


@pytest.fixture(scope="session")
def real_llm() -> Small_LLM_Model:
    """
    Fixture providing a real Small_LLM_Model instance.

    Return:
        Small_LLM_Model = An initialized instance of the SDK model.
    """
    return Small_LLM_Model(model_name="Qwen/Qwen3-0.6B")


@pytest.fixture(scope="session")
def mock_vocab(real_llm: Small_LLM_Model) -> dict[str, int]:
    """
    Fixture providing a vocabulary aligned with the current src/constrained.py

    Args:
        real_llm: Small_LLM_Model = The LLM engine instance.
    Return:
        dict[str, int] = A dictionary mapping token strings to exact first IDs.
    """
    vocab_path: str = real_llm.get_path_to_vocab_file()
    vocab: dict[str, int] = json.load(open(vocab_path))

    return vocab


def encode(real_llm: Small_LLM_Model, text: str) -> Any:
    '''
    Encode the given text and return it

    Args:
        real_llm: Small_LLM_Model = The actual LLM engine fixture.
        text: str = The text to encode
    Return:
        None
    '''
    return real_llm.encode(text)[0].tolist()[0]


def test_get_allowed_parts_number(
            real_llm: Small_LLM_Model,
            mock_vocab: dict[str, int]
        ) -> None:
    """
    Test that the number mask only includes valid numeric tokens.

    Args:
        real_llm: Small_LLM_Model = The actual LLM engine fixture.
        mock_vocab: dict[str, int] = The mock vocabulary fixture.
    Return:
        None
    """
    res: dict[str, set[int]] = get_allowed_parts(real_llm, mock_vocab)

    assert "number" in res
    allowed: set[int] = res["number"]

    texts: list[str] = [
        "4242", "-5.0", "-45.2", "0", "1", "999999",
        "3.14159", "-0.001", "42", "-7", "123.4",
        "0.0", "1000", "-1000", "0"
    ]

    assert all([
        encode(real_llm, text) in allowed
        for text in texts
    ])


def test_get_allowed_parts_string(
            real_llm: Small_LLM_Model,
            mock_vocab: dict[str, int]
        ) -> None:
    """
    Test that the string mask correctly includes valid text tokens.

    Args:
        real_llm: Small_LLM_Model = The actual LLM engine fixture.
        mock_vocab: dict[str, int] = The mock vocabulary fixture.
    Return:
        None
    """
    res: dict[str, set[int]] = get_allowed_parts(real_llm, mock_vocab)

    assert "string" in res
    allowed: set[int] = res["string"]

    texts: list[str] = [
        "hello", "world", "Python", "test", "code",
        "bonjour", "café", "tête", "l'arbre", "c'est",
        "word!", "hello,", "yes.", "no?", '"quote"',
        "user_123", "version-2", "text...", "OK"
    ]

    assert all([
        encode(real_llm, text) in allowed
        for text in texts
    ])


def test_get_allowed_fn_name_match(
            real_llm: Small_LLM_Model,
            mock_vocab: dict[str, int]
        ) -> None:
    """
    Test the prefix matching logic for constraint masks on function names.

    Args:
        real_llm: Small_LLM_Model = The actual LLM engine fixture.
        mock_vocab: dict[str, int] = The mock vocabulary fixture.
    Return:
        None
    """
    func_names: list[str] = ["fn_add", "fn_add_numbers", "fn_greet"]

    allowed: set[int] = get_allowed_fn_name(
        llm=real_llm,
        vocab=mock_vocab,
        func_names=func_names,
        current_fn_name=""
    )
    assert encode(real_llm, "fn_add") in allowed
    assert encode(real_llm, "fn_greet") in allowed

    allowed_next: set[int] = get_allowed_fn_name(
        llm=real_llm,
        vocab=mock_vocab,
        func_names=func_names,
        current_fn_name="fn_add"
    )

    assert encode(real_llm, "_numbers") in allowed_next
    assert encode(real_llm, "fn_add_numbers") not in allowed_next


def test_get_allowed_fn_name_fallback(
            real_llm: Small_LLM_Model,
            mock_vocab: dict[str, int]
        ) -> None:
    """
    Test the safety fallback when no token matches the unexpected prefix.

    Args:
        real_llm: Small_LLM_Model = The actual LLM engine fixture.
        mock_vocab: dict[str, int] = The mock vocabulary fixture.
    Return:
        None
    """
    func_names: list[str] = ["fn_add"]
    allowed: set[int] = get_allowed_fn_name(
        llm=real_llm,
        vocab=mock_vocab,
        func_names=func_names,
        current_fn_name="impossible_prefix_xyz"
    )

    assert len(allowed) == len(mock_vocab)
