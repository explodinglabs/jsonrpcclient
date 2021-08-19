from functools import reduce
from typing import Any, Callable


identity = lambda x: x


def compose(*fs: Callable[..., Any]) -> Callable[..., Any]:
    def compose2(f: Callable[..., Any], g: Callable[..., Any]) -> Callable[..., Any]:
        return lambda *a, **kw: f(g(*a, **kw))

    return reduce(compose2, fs)
