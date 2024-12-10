import inspect
from typing import Any, Callable, List, Tuple
import itertools

def is_unary(fn: Callable):
    return len(inspect.signature(fn).parameters) == 1

def make_recursive_set(base: set, constructors: List[Callable[..., Any]]):
    while True:
        
        # # split constructors into unary and binary ones
        # unary_cons, binary_cons = [], []
        # for con in constructors:
        #     if is_unary(con):
        #         unary_cons.append(con)
        #     else:
        #         binary_cons.append(con)
        
        # Every pair in cartesian product
        product = itertools.product(base, base)

        for x, y in product:
            new_elems = {con(x)
                        if is_unary(con)
                        else con(x, y) for con in constructors}

            base = base.union(new_elems)

        yield base

        
if __name__ == "__main__":
    A = set([""])
    constructed = make_recursive_set(A, [lambda x, y: f"♡{x}♣{y}"])

    print(sorted(next(constructed)))
    print(sorted(next(constructed)))

    items = list(next(constructed))

    for item in items:
        assert item.count("♡") == item.count("♣"), "Unequal length"
