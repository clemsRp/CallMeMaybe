#!/usr/bin/env python3

from pydantic import BaseModel, Field
from typing import Literal


class Type(BaseModel):
    '''
    Pydantic class for the types

    Args:
        type: Literal["string", "number", "integer"] = The type
    Return:
        None
    '''
    type: Literal["string", "number", "integer"]


class Function(BaseModel):
    '''
    Pydantic class for the definition of one function

    Args:
        name: str = The name of the function
        description: str = The description of the function
        parameters: dict[str, Type] = The parameters of
            the function and their type
        returns: Type = The type of the returns
    Return:
        None
    '''
    name: str = Field(pattern=r"^fn_[a-z_]+$")
    description: str
    parameters: dict[str, Type]
    returns: Type


class Functions(BaseModel):
    '''
    Pydantic class for the function definitions

    Args:
        functions: list[Function] = The functions definition
    Return:
        None
    '''
    functions: list[Function]


class Prompt(BaseModel):
    '''
    Pydantic class for one prompt

    Args:
        prompt: str = The prompt
    Return:
        None
    '''
    prompt: str


class Prompts(BaseModel):
    '''
    Pydantic class for the prompts

    Args:
        prompts: list[Prompt] = The list of all the prompts
    Return:
        None
    '''
    prompts: list[Prompt]
