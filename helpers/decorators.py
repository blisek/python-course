from inspect import signature, _empty
from .exceptions import CastError


class cast_arguments:
    HANDLED_TYPES = {str, int, float}

    __slots__ = ['_func', '_mappings', '_required_args']

    def __init__(self, func):
        self._func = func
        self._mappings = []
        self._required_args = 0
        self.__init_mappers()

    def __call__(self, *args, **kwargs):
        mappings_len = len(self._mappings)
        args_len = len(args)
        if args_len < self._required_args:
            raise ValueError(f'unexpected arguments count! Expected {mappings_len}, got {args_len}')
        mappings = self._mappings
        mapped_args = []
        for i in range(args_len):
            dest_type = mappings[i][1]
            current_arg = args[i]
            current_arg_tp = type(current_arg)
            if dest_type is list and current_arg_tp is not list:
                mapped_args.append([current_arg])
            elif dest_type is tuple and current_arg_tp is not tuple:
                mapped_args.append((current_arg,))
            elif dest_type is None or current_arg_tp is dest_type:
                mapped_args.append(current_arg)
            elif dest_type in cast_arguments.HANDLED_TYPES:
                try:
                    casted = dest_type(current_arg)
                    mapped_args.append(casted)
                except ValueError as e:
                    raise CastError(f'cannot cast argument \'{mappings[i][0]}\'! Input value: {current_arg}') from e
            else:
                mapped_args.append(current_arg)  # TODO: zrobic lepsza obsluge
        self._func(*mapped_args)

    def __init_mappers(self):
        f_sig = signature(self._func)
        params = f_sig.parameters
        required_arg_count = 0
        for arg in params.keys():
            param = params[arg]
            param_name = param.name
            param_ann = param.annotation
            param_def = param.default

            if param_ann in cast_arguments.HANDLED_TYPES:
                self._mappings.append((param_name, param_ann))
            elif param_ann is _empty:
                self._mappings.append((param_name, None))
            else:
                self._mappings.append((param_name, param_ann))
            if param_def is not _empty:
                required_arg_count += 1
        self._required_args = required_arg_count
