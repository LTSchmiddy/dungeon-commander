"""
Python Anonymous Functions Library
Created by LT_Schmiddy (Alex Schmid) on 9/25/2020
"""

import inspect
import textwrap
from types import CodeType, FunctionType

# code_class = type(compile("", "<string>", 'exec'))
from typing import Any


def _get_exec_name(
    frame_info: inspect.FrameInfo, prefix: str = "anon_func.rexec"
) -> str:
    return (
        f"<{prefix} (execution) @ function `{frame_info.function}`,"
        f" file '{frame_info.filename}', line {frame_info.lineno}>"
    )


def _get_r_eval_name(
    frame_info: inspect.FrameInfo, prefix: str = "anon_func.rexec"
) -> str:
    return (
        f"<{prefix} (return evaluation) @ function `{frame_info.function}`,"
        f" file '{frame_info.filename}', line {frame_info.lineno}>"
    )


def rexec(
    p_code: (str, CodeType, None) = None,
    p_return: (str, CodeType, None) = None,
    use_globals: (dict, None) = None,
    use_locals: (dict, None) = None,
    prefix: str = "anon_func.rexec",
    dedent: bool = True,
) -> Any:
    """
    Indented to work like the `exec()` builtin, but able to return a value.
    Accepts strings or code objects like those returned from `compile()`.
    By default, it uses the globals and locals from the calling stack-frame.
    Useful for squeezing extra statements into a lambda function.

    Since return statements in `exec()` do not recognize when they are inside a function,
    this is not a viable method for returning a value. Instead, after the exec code finishes
    running, `eval(p_return)` is used on the same namespace to get a value to return.

    `p_code` and `p_return` are both allowed to be blank or None. If p_code is blank, it is simply
    ignored and only `p_return` is evaluated. If `p_return` is blank, None is returned.

    The `prefix` parameter is fed into the beginning of the `filename` parameter of the `compile()`
    builtin, and is very useful for debugging and picking through traceback messages.

    The parameters `use_globals` and `use_locals` allow you to specify dicts of globals and locals
    to use instead of the default (Similar to the `__globals` and `__locals` parameter in `exec()`).

    :param p_code: The code to execute.
    :param p_return: An evaluation to run, the result of which will be returned.
    :param prefix: A prefix for the filename string of the code you're running.
    :param use_globals: Manually specify global variables to use.
    :param use_locals: Manually specify local variables to use.
    :param dedent: If p_code is a string, should it be de-indented before execution?
    :return: The returned value from `p_return`.
    """
    # Gets the frame for the function call.
    # Since this code is inside a function, `frames` will always have at least 2 members.
    frame_info = inspect.stack()[1]

    if use_globals is None:
        use_globals = frame_info.frame.f_globals
    if use_locals is None:
        use_locals = frame_info.frame.f_locals

    # print(f"{use_locals}")
    # Handle function execution:

    if p_code is not None:
        # Did the execution code come pre-compiled?
        if isinstance(p_code, CodeType):
            exec(p_code, use_globals, use_locals)
        # Did we get a source code string?
        elif isinstance(p_code, str) and p_code.strip() != "":
            if dedent:
                p_code = textwrap.dedent(p_code)

            exec(
                compile(p_code, _get_exec_name(frame_info, prefix), "exec"),
                use_globals,
                use_locals,
            )

    # Are we supposed to try to return something?
    if p_return is None:
        return None

    # Generate return evaluation filename string:

    # Did the return code come pre-compiled?
    if isinstance(p_return, CodeType):
        return eval(p_return, frame_info.frame.f_globals, frame_info.frame.f_locals)
    # Did we get a source code string?
    elif isinstance(p_return, str) and p_return.strip() != "":
        return eval(
            compile(p_return, _get_r_eval_name(frame_info, prefix), "eval"),
            use_globals,
            use_locals,
        )

    return None

def tget(p_expression: Any, r_true=None, r_false=None, do_conversion: bool=True)->Any:
    """
    Designed to function like the ternary operator (`?`) in c-based languages.
    For best results, you can simply enter an expression that evaluates to a boolean
    (such as `x==5`) or another type that can be converted to a boolean with bool(`bool`).
    By default, this type conversion is done automatically, to replicate the concept of 'truthiness'
    in `if` statements.

    Unlike some other methods in this module, passing a string into `p_expression` will not evaluate it as code.
    Enter your evaluation as Python code directly. Technically, the expression will be processed before
    it's passed to this function.

    :param p_expression: The condition to evaluated.
    :param r_true: Return this if true.
    :param r_false: Return this if false.
    :param do_conversion: Use 'truthiness'?
    :return:
    """
    if do_conversion:
        p_expression = bool(p_expression)
    return (r_false, r_true)[p_expression]

def teval(
    p_eval: (str, bool, CodeType, FunctionType),
    on_true: (str, CodeType, FunctionType, None) = None,
    on_false: (str, CodeType, FunctionType, None) = None,
    use_globals: (dict, None) = None,
    use_locals: (dict, None) = None,
    p_eval_fargs: tuple = (),
    on_true_fargs: tuple = (),
    on_false_fargs: tuple = (),
    p_eval_fkwargs: (dict, None) = None,
    on_true_fkwargs: (dict, None) = None,
    on_false_fkwargs: (dict, None) = None,
    prefix: str = "anon_func.rexec",
    dedent: bool = True,
) -> Any:
    """
    UNTESTED!!
    :param p_eval:
    :param on_true:
    :param on_false:
    :param use_globals:
    :param use_locals:
    :param p_eval_fargs:
    :param on_true_fargs:
    :param on_false_fargs:
    :param p_eval_fkwargs:
    :param on_true_fkwargs:
    :param on_false_fkwargs:
    :param prefix:
    :param dedent:
    :return:
    """

    # Gets the frame for the function call.
    # Since this code is inside a function, `frames` will always have at least 2 members.

    frame_info = inspect.stack()[1]

    if use_globals is None:
        use_globals = frame_info.frame.f_globals
    if use_locals is None:
        use_locals = frame_info.frame.f_locals

    result = None
    if isinstance(p_eval, bool):
        result = p_eval
    elif isinstance(p_eval, CodeType):
        result = eval(p_eval, use_globals, use_locals)
    # Did we get a source code string?
    elif isinstance(p_eval, str) and p_eval.strip() != "":
        if dedent:
            p_eval = textwrap.dedent(p_eval)

        result = eval(
            compile(p_eval, _get_exec_name(frame_info, prefix), "eval"),
            use_globals,
            use_locals,
        )
    elif isinstance(p_eval, FunctionType):
        if p_eval_fkwargs is None:
            p_eval_fkwargs = {}
        result = p_eval(*p_eval_fargs, **p_eval_fkwargs)
    else:
        result = bool(p_eval)


    # Determine which result var to use:
    r_action, r_fargs, r_fkwargs = tget(result, (on_true, on_true_fargs, on_true_fkwargs), (on_false, on_false_fargs, on_false_fkwargs))

    retVal = None
    if isinstance(r_action, CodeType):
        retVal = eval(r_action, use_globals, use_locals)
    # Did we get a source code string?
    elif isinstance(r_action, str) and r_action.strip() != "":
        if dedent:
            r_action = textwrap.dedent(r_action)

        retVal = eval(
            compile(r_action, _get_exec_name(frame_info, prefix), "eval"),
            use_globals,
            use_locals,
        )
    elif isinstance(p_eval, FunctionType):
        if r_fkwargs is None:
            r_fkwargs = {}
        retVal = r_action(*r_fargs, **r_fkwargs)

    else:
        return r_action

    return retVal

# Anonymous generation of regular functions:
def func(
    f_args: (str, tuple, list, None) = None,
    f_code: str = "pass",
    f_name: str = "anonymous_function",
    prefix: str = "anon_func.func",
    use_globals: (dict, None) = None,
    use_locals: (dict, None) = None,
    reindent_size: int = 4,
) -> FunctionType:

    if isinstance(f_args, str):
        if f_args.strip() != "":
            f_args += ", __secret_locals"
        else:
            f_args = "__secret_locals"

    elif isinstance(f_args, tuple) or isinstance(f_args, list):
        if len(f_args) > 0:
            f_args = ", ".join(f_args) + ", __secret_locals"
        else:
            f_args = "__secret_locals"

    else:
        f_args = "__secret_locals"

    if f_code is None or f_code == "":
        f_code = "pass"

    # Gets the frame for the function call.
    # Since this code is inside a function, `frames` will always have at least 2 members.
    frame_info = inspect.stack()[1]
    # print(frame_info.function)
    if use_globals is None:
        use_globals = frame_info.frame.f_globals
    if use_locals is None:
        # We don't ACTUALLY want this function added to the local namespace, so we'll make a duplicate.
        # As long as we feed rexec the original global dict, this shouldn't cause any problems.
        use_locals = frame_info.frame.f_locals.copy()

    # print(use_locals)

    func_text = f"def {f_name}({f_args}):\n"

    secret_locals = inspect.stack()[1].frame.f_locals

    for i in secret_locals.keys():
        func_text += f"    {i} = __secret_locals['{i}']\n"

    func_text += _parse_fexec_string(f_code, reindent_size)

    out_func: FunctionType = rexec(
        func_text,
        f_name,
        prefix=f"{f_name} from {prefix}",
        use_globals=use_globals,
        use_locals=use_locals,
    )

    if out_func.__defaults__ is not None:
        out_func.__defaults__ += (secret_locals,)
    else:
        out_func.__defaults__ = (secret_locals,)

    return out_func


def _parse_fexec_string(code_str: str, reindent_size: int = 4) -> str:
    return textwrap.indent(
        textwrap.dedent(code_str), " " * reindent_size, lambda line: True
    )

__all__ = ('rexec', 'tget', 'teval', )

# def lexec(
#     p_code: (str, CodeType, None) = None,
#     p_return: (str, CodeType, None) = None,
#     prefix: str = "anon_func.rexec",
#     dedent: bool = True
# ) -> Any:
#     frame_info_inner = inspect.stack()[1]
#     frame_info_outer = inspect.stack()[2]
#
#     if frame_info_inner.function != '<lambda>':
#         print("WARNING: `lexec` should only be used inside a lambda function!")
#
#     # print(frame_info_inner.frame.f_globals == frame_info_outer.frame.f_globals)
#
#     use_locals = {}
#     use_locals.update(frame_info_outer.frame.f_locals)
#     use_locals.update(frame_info_inner.frame.f_locals)
#
#     result = rexec(p_code, p_return, frame_info_outer.frame.f_globals, use_locals, prefix, dedent)
#
#     return result
