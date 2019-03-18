import typing as tp
import re
from .exceptions import InputNotProvidedError


class DataProvider:

    __slots__ = ['_input_method', '_default_prompt']

    INTEGER_REGEX = re.compile(r'^[+-]?\d+$')
    FLOAT_REGEX = re.compile(r'^[+-]?\d*(?:\.\d*)?$')

    def __init__(self, input_method: tp.Callable[[str], str], default_prompt: str = 'Input: '):
        if not input_method:
            raise ValueError('input_method is None')
        if not default_prompt:
            raise ValueError('default_prompt can\'t be None')
        self._input_method = input_method
        self._default_prompt = default_prompt

    def get_non_empty_string(self, prompt: str = None, retry: bool = True):
        while True:
            s = None
            try:
                s = self._input_method(prompt if prompt is not None else self._default_prompt)
            except (Exception, KeyboardInterrupt) as ex:
                raise InputNotProvidedError() from ex
            if not s:
                if retry:
                    continue
                else:
                    raise InputNotProvidedError()
            else:
                return s

    def get_int(self, prompt: str = None, retry: bool = True):
        while True:
            s = self.get_non_empty_string(prompt, retry)

