from typing import Any, Callable, Set

def test_fn_type(domain: Set[Any], codomain: Set[Any], relation: Callable[[Any], Any]) -> dict[str, bool]:
    types = {
        "injective": True,
        "surjective": True,
        "bijective": False
    }

    # check that relation is functional
    for s in domain:
        if not relation(s) in codomain:
            raise ValueError("Not left-total")

    # Test injectivity
    seen_outputs = set()
    for s in domain:
        if relation(s) in seen_outputs:
            types["injective"] = False

        seen_outputs.add(relation(s))

    # Test surjectivity
    types["surjective"] = seen_outputs == codomain

    # Test bijectivity
    types["bijective"] = types["injective"] and types["surjective"]

    return types
        


if __name__ == "__main__":
    # S = {1, 2, 3, 4, 5}  
    S = set(range(1, 6))

    # T = {3, 6, 9, 10} 
    T = set([3, 6, 9, 10])
    
    def relation(s):
        if s < 4:
            return s * 3
        return 10

    print(test_fn_type(S, T, relation))