#!/usr/bin/env python3

import argparse
from src.pipeline import execute_pipeline


def main() -> None:
    '''
    Main function of the project

    Args:
        None
    Return:
        None
    '''
    # Get the args
    arg_parser: argparse.ArgumentParser = (
        argparse.ArgumentParser(
            description="CallMeMaybe argument parser"
        )
    )

    arg_parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json",
        help="Define the path of the functions definition file"
    )
    arg_parser.add_argument(
        "--input",
        default="data/input/function_calling_tests.json",
        help="Define the path of the prompts file"
    )
    arg_parser.add_argument(
        "--output",
        default="data/output/function_calling_results.json",
        help="Define the path of the output file"
    )

    args = arg_parser.parse_args()

    execute_pipeline(args)


if __name__ == "__main__":

    main()
