import pytest
from llm_sdk.llm_sdk import Small_LLM_Model
from src.constrained import get_allowed_parts, get_allowed_fn_name


@pytest.fixture
def real_llm() -> Small_LLM_Model:
    """
    Fixture providing a real Small_LLM_Model instance.

    Return:
        Small_LLM_Model = An initialized instance of the SDK model.
    """
    return Small_LLM_Model(model_name="Qwen/Qwen3-0.6B")


@pytest.fixture
def mock_vocab() -> dict[str, int]:
    """
    Fixture providing a minimal mock vocabulary for testing constraints.

    Return:
        dict[str, int] = A small dictionary mapping token strings to IDs.
    """
    return {
        "fn_add": 0,
        "fn_greet": 1,
        "fn_add_numbers": 2,
        "123": 3,
        "-45.2": 4,
        "hello": 5,
        "Ġworld": 6,
        "Ġ12": 7,
        "bad_token!": 8,
        '"': 9,
        ",": 10
    }


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
    allowed_indices: set[int] = res["number"]

    assert mock_vocab["123"] in allowed_indices
    assert mock_vocab["-45.2"] in allowed_indices
    assert mock_vocab["Ġ12"] in allowed_indices

    assert mock_vocab["hello"] not in allowed_indices
    assert mock_vocab["bad_token!"] not in allowed_indices


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
    allowed_indices: set[int] = res["string"]

    assert mock_vocab["hello"] in allowed_indices
    assert mock_vocab["Ġworld"] in allowed_indices
    assert mock_vocab["bad_token!"] not in allowed_indices


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
    assert mock_vocab["fn_add"] in allowed
    assert mock_vocab["fn_greet"] in allowed

    allowed_next: set[int] = get_allowed_fn_name(
        llm=real_llm,
        vocab=mock_vocab,
        func_names=func_names,
        current_fn_name="fn_add"
    )
    assert (
        mock_vocab["fn_add_numbers"] in allowed_next
        or mock_vocab[","] in allowed_next
    )
    assert mock_vocab["fn_greet"] not in allowed_next


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
