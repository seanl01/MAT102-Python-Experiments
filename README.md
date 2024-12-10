# MAT102 Experiments in Python
This repository contains some experiments I did for my own exploration and fun, to see if I could use code to represent some of the mathematical concepts I learned in my _MAT102: Introduction to Mathematical Proofs_ course during my exchange program in the University of Toronto Mississauga.

You can find some great lecture notes by Prof Tyler Holden from the course [here](http://home.tykenho.com/index.html?notes).

## Recursively defined sets in Python
> Code found in [recursive_set.py](recursive_set.py). The code is not optimised, and contains redundant union operations which are thankfully idempotent. It's more of a proof of concept but one day I may take the time to optimise it!

During the course we discussed recursively defined sets, sequences and how to perform structural induction on these types of mathematical objects.

This prompted me to experiment with recursively defined sets in Python code, and it proved to be an interesting mental exercise trying to represent the constructors in code.

```py
print(sorted(next(constructed)))
print(sorted(next(constructed)))

>> ['', '♡♣']
>> ['', '♡♡♣♣', '♡♡♣♣♡♣', '♡♣', '♡♣♡♣']
``` 
> An example of how an infinite set might be represented with generators. In this case, what is given is the previous set with new values added, and not a stream of new values, which might also work.

### Approach
#### Generators:
Recursively defined sets are often infinite, and it seemed fitting to use generators, which were lazily evaluated to represent these infinite objects. Generators are great for providing values when they are needed, and can yield the next value, the next value, and so on, without having to evaluate the entire structure which would be impossible for infinite structures anyway.

#### Constructor Functions:
Recursively defined sets start with basis elements, and some defined constructor function(s) which create new elements from old elements. It seemed fitting to allow the user to pass in a list of lambda functions which would take in a single element $x$ or a pair of elements $(x, y)$ and yield a new object.

Say $A$ is a recursively defined set:

$$
\begin{align}
x, y \in A \\
x + 2y \in A \\
x - y \in A \\
c_1, c_2: (A \times A) \rightarrow A \\
c_1((x, y)) = x + 2y \\
c_2((x, y)) = x - y
\end{align}
$$

> Here, if $x$ and $y$ are in set $A$, then $x + 2y$ is also in set $A$ can also be given as a constructor function mapping from $(A \times A)$ to $A$ which produces the new elements

How this might look in Python:

```py
constructors = [lambda x, y: x + 2 * y, lambda x, y : x - y]
```
#### Putting it together

```py
# Initialise basis set
A = set([""])

# Define constructor functions
constructors = [lambda x, y: f"♡{x}♣{y}"]

# Initialise recursive set
recursive_A = make_recursive_set(A, constructors)

# Yield next value and print
print(sorted(next(constructed)))
print(sorted(next(constructed)))

>> ['', '♡♣']
>> ['', '♡♡♣♣', '♡♡♣♣♡♣', '♡♣', '♡♣♡♣']

# Get set of elements from third pass
items = list(next(constructed))

# Make some assertions about elements
for item in items:
    assert item.count("♡") == item.count("♣"), "Unequal symbol count"
```

> The last part should be proved using structural induction, but it's just an interesting idea that one can test assumptions using a recursively defined set. It may have some useful applications for quick empirical testing when formal methods might be difficult.

## Function Properties
> Code found in [fn_prop_tester.py](fn_prop_tester.py)

During the course, we also learned about injections, surjections, and bijections. I wanted to see if I could use the properties I learned to test injectivity, surjectivity, and bijectivity given a domain, codomain, and a relation in code.

We learn that given a function $f: A \rightarrow B$, if for $x, y \in A$, $f(x) = f(y)$, then if $x = y$, $f$ is __injective__. In simpler terms, this means that every possible input in the function produces a unique output. If two inputs produce the same output, that means they are equal.

We learned that if for every $b \in B$, there exists some $a \in A$ for which $f(a) = b$, then $f$ is **surjective**. This basically means that we have some way of producing every possible output in $B$. For every value of $B$ there is some value in $A$ that would produce this value when input into $f$.

Now if $f$ is both __injective__ and __surjective__, it is __bijective__ i.e. there is a one-to-one mapping between every input in $A$ and every output in $B$

### Approach
I need a domain, codomain, and relation, which I represent using Python `Set`, and functions.

```py
# S = {1, 2, 3, 4, 5}  
S = set(range(1, 6))

# T = {3, 6, 9, 10} 
T = set([3, 6, 9, 10])

# function which multiplies its input by 3 if input < 4, and returns 10 otherwise
def relation(s):
    if s < 4:
        return s * 3
    return 10

# See what properties our function fulfills
test_fn_type(S, T, relation)
>> {'injective': False, 'surjective': True, 'bijective': False}
```
What's behind `test_fn_type`? First, we see that we output the properties of the provided function using a dictionary which is initialised as so:

```py
types = {'injective': True, 'surjective': True, 'bijective': False}
```

Now how do we evaluate the properties? Let's start with __injectivity__.

How do we test **injectivity**? Well we need to get all the possible outputs for all the inputs we have in $S$, and make sure none of them are equal to one another. Every input should have a unique output. Let's test this using a hash set of the outputs we have already seen. If we repeat even one of these, we are not injective.

```py
# Hash set of seen outputs i.e. the image of the domain for the nerds out there
seen_outputs = set()
for s in domain:
    # Test if we have seen it before
    if relation(s) in seen_outputs:
        types["injective"] = False

    seen_outputs.add(relation(s))
```
Notice that we could terminate the loop once we found a repeated output, but we don't. This is because seen outputs is useful later on for our surjectivity test.

For a function to be surjective, we must be able to produce all the possible outputs that are in the codomain $T$, so whatever outputs we have created in `seen_outputs` should be equal to the entire codomain $T$

```py
types["surjective"] = seen_outputs == codomain
```

> Python implements an internal equality check method for the `Set` type to check for set equality

The easiest one to conclude is bijectivity. If either injectivity or surjectivity is false, then bijectivity is false.

After testing the former two, a simple `and` check suffices. So we can put this last.

```py
types["bijective"] = types["injective"] and types["surjective"]
```

With relatively simple logic, we can now tell if a given function is injective, surjective, and/or bijective!









