from propositional_logic import KB_class, forward_chaining, backward_chaining, model_checking
from sympy import symbols, And, Or, Not, Implies

if __name__ == "__main__":
    rain, wetGrass, slippery, srpinkler = symbols("rain wetGrass slippery sprinkler")

    KB = KB_class(
        [rain, wetGrass, slippery, srpinkler],
        Or(Not(rain), wetGrass),
        Implies(srpinkler, wetGrass),
        Implies(wetGrass, slippery),
        rain
    )

    # KB details
    print("KB clauses")
    KB.print_clauses()
    print("\nKB known facts")
    print(KB.extract_facts())

    # Backward Chaining usage
    print("\nBackward chaining inference")
    query = slippery
    result = backward_chaining(query, KB)
    print(f'Is {query} infered by KB: {result}')

    # Forward chaining usage
    print("\nForward chaining inference")
    new_facts = forward_chaining(KB)
    print(f'Infered facts: {new_facts}\n')