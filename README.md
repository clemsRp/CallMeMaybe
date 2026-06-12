*This project has been created as part of the 42 curriculum by crappo*

# Call Me Maybe

## Description

This project aims to implement a constrained decoding system for reliable function calling in Large Language Models (LLMs).

The main objective is to ensure that model outputs strictly follow a predefined structured format (such as a JSON schema) while maintaining accuracy, performance, and reliability.

In this project, we designed and implemented a decoding mechanism that dynamically restricts token generation to prevent malformed outputs and hallucinated function calls.

### Key Objectives

- Implement constrained decoding
- Guarantee structured output compliance
- Improve reliability of function calls
- Analyze performance trade-offs
- Ensure robustness through testing

---

## Instructions

### Requirements

- Programming Language: [e.g., Python 3.11]
- Package Manager: uv and pip
- Dependencies: Listed in `pyproject.toml`

### Installation

    git clone <repository_url>
    cd <project_name>
    make install
	uv sync

### Execution

    make run OR uv run python -m src --> Default files

	OR

	uv run python -m src [--input <input_file>] [--output <output_file>] --> Adapted files

---

## Algorithm Explanation

>For constrained decoding, we create 4 sets (int, float, str and fn_name) to decrease the number of token possible at each call to the LLM. So we search the max inside a set of 20 000/30 000 tokens instead of 150 000.

## Design Decisions

>Instead of asking the LLM for the entire JSON response to write, we pre-fill fields so that it only completes what is adaptive based on the prompt. Once it has given us the fn_name to use, we look at the arguments that this function takes and their type. We can then pre-fill the argument keys and choose the regex for the argument value.

---

## Performance Analysis

### Accuracy

>Thanks to the constrained decoding, the accuracy of the LLM response is very good. We must be near to 100% accurate, as it may make mistakes, most particularely with the regex for numbers only.

### Speed

>The execution speed of my program is very good, it's around a minute generally.

### Reliability

>Thanks to constrained decoding, JSON reliability is 100%. We will never have poorly formatted or incorrect JSON.

---

## Challenges Faced

>At first, I had a lot of trouble understanding what constrained decoding was. I thought that all I had to do was provide a lot of context for the LLM to give me the right format. So I looked online and got help from AI to understand what was required.

---

## Testing Strategy

We validated the implementation using multiple testing layers:

### Integration Tests

- End-to-end function calling scenarios
- Realistic prompts
- Edge case handling
- Error case simulations

### Manual Testing

- Boundary condition scenarios
- Invalid input simulations
- Unexpected user behavior

Testing focused on correctness, robustness, and consistency.

---

## Example Usage

	# Basic execution
	make run

	# Adapted file paths execution
	-	uv run python -m src --input data/input/function_calling_tests.json
	-	uv run python -m src --output data/output/function_calling_results.json
	-	uv run python -m src --input data/input/function_calling_tests.json --output data/output/function_calling_results.json


Expected output:

	[
    	{
    	    "prompt": "What is the sum of 40 and 2?",
    	    "fn_name": "fn_add_numbers",
    	    "args": {"a": 40.0, "b": 2.0}
    	}
	]

---

## Resources

### AI Usage Disclosure

AI tools were used for:

- Understanding constrained decoding theory
- Brainstorming implementation strategies
- Improving documentation clarity
- Debugging conceptual issues
