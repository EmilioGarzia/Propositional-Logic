# Propositiona logic with `sympy`

In this repo I have experienced the basics of propositional logic using `sympy` module on `python`. In particular, in this repo you will find:

* A dedicated class named `KB_class` to handle knowledge base in easy way, this class provides many useful methods, such aa:
    * methods to manage horn clauses
    * add/remove clauses on KB easily
    * apply inference by resolution
    * retrive KB insights
* An implementation of the following algorithms:
    *  *Model checking* (for entailment)
    * *Inference by resolution* (for entailment)
    * *Forward chaining*
    * *Backward chaining*
* And others useful functions:
    * `modus_ponens()` to apply modus ponens inference on implications
    * `check_horn()` to check if a clause is a horn clause
    * `horn_to_implication()` to convert horn clauses as implications

All theese tools (`KB_class` included) are contained into the python source file `propositional_logic.py`. In addition, an example usage is provided in the source file named `main.py`.

## More on propositional logic

Insights and details are contained into the **jupyter notebook** named `propositional_logic_introduction.ipynb`.

In this notebook the main concepts of the propositional logic are explained. Moreover, all implemented tools are viewed in detail.

## Author

Emilio Garzia, 2025