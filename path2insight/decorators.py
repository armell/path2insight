from functools import wraps

from path2insight.utils import is_list_like, PATH_OBJECT_TYPES


def iter_advanced(func):

    @wraps(func)
    def func_wrapper(first_arg, *args, **kwargs):

        if isinstance(first_arg, PATH_OBJECT_TYPES):
            result = func([first_arg], *args, **kwargs)

            # if the result is a list-like object with one value, than return
            # the unlisted value.
            if is_list_like(result) and len(result) == 1:
                return result[0]
            else:
                return result
        else:
            # expecting an iterable
            return func(first_arg, *args, **kwargs)

    return func_wrapper


def iter_advanced_method(func):

    @wraps(func)
    def func_wrapper(self, first_arg, *args, **kwargs):

        if isinstance(first_arg, PATH_OBJECT_TYPES):
            result = func(self, [first_arg], *args, **kwargs)

            # if the result is a list-like object with one value, than return
            # the unlisted value.
            if is_list_like(result) and len(result) == 1:
                return result[0]
            else:
                return result
        else:
            # expecting an iterable
            return func(self, first_arg, *args, **kwargs)

    return func_wrapper


def iter_advanced_2d(func):

    @wraps(func)
    def func_wrapper(first_arg=None, second_arg=None, *args, **kwargs):

        if isinstance(first_arg, PATH_OBJECT_TYPES):
            first_arg = [first_arg]
        if isinstance(second_arg, PATH_OBJECT_TYPES):
            second_arg = [second_arg]

        result = func(first_arg, second_arg, *args, **kwargs)

        # if the result is a list-like object with one value, than return
        # the unlisted value.
        if is_list_like(result) and len(result) == 1:
            return result[0]
        else:
            return result

    return func_wrapper
