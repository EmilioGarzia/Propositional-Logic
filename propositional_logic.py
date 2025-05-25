from sympy import Symbol, And, Or, Not, Equivalent, Implies, to_cnf, to_nnf, false
from sympy.logic.inference import satisfiable, entails

""" 
    Function that check if a clause is a horn clause

    @param
        clause (sympy clause): clause defined using sympy module
"""
def check_horn(clause):
    terms = clause.args

    # Check if a fact is positive
    if isinstance(clause, Symbol):
        return True

    # Check for pure clauses (disdisjunction)
    if isinstance(clause, Or):    
        positive_atoms = 0
        for term in terms:
            if not isinstance(term, Not):
                positive_atoms += 1
        if positive_atoms > 1:
            return False
        return True
    
    # Check for clauses as implications
    if isinstance(clause, Implies):
        conclusion = clause.args[1]
        premisees = clause.args[0]

        if not isinstance(conclusion, Symbol) and conclusion != false:
            return False

        if isinstance(premisees, Symbol):
            return True

        if isinstance(premisees, And):
            for literal in premisees.args:
                if not isinstance(literal, Symbol):
                    return False
            return True
        
        return False

    return False 

"""
    Apply modus ponens inference

    @params
        implication (sympy Implication): implication object from sympy
        facts list(sympy Symbol): know facts as sympy Symbol objects
"""
def modus_ponens(implication, facts):
    if not isinstance(implication, Implies):
        return None

    premises = set(implication.args[0].atoms())
    if premises.issubset(facts):
        return True
    return False

"""
    Function that converts a horn clause as implication
    
    @param
        clause (sympy clause): Horn clause defined using sympy module
"""
def horn_to_implication(clause):
    # Check if a clause is a pure horn clause
    if check_horn(clause) and isinstance(clause, Or):
        terms = clause.args
        negative_terms = []
        positive_term = None
        for term in terms:
            if isinstance(term, Not):
                negative_terms.append(term.args[0])
            else:
                positive_term = term

        if positive_term is None:
            return clause

        return Implies(And(*negative_terms), positive_term)
    else:
        return clause

"""
    Backward chaining inference algorithm

    @params
        goal (sympy.Symbol): sympy Symbol object which express a fact 
        knowledge_base (KB_class): Knoweledge base
        visited (bool): This parameter is useful for recursion
"""
def backward_chaining(goal, knowledge_base, visited=None):
    # If KB is not horn, backward is useless
    if knowledge_base.is_horn():
        knowledge_base.horn_to_implication()
    else:
        return False

    if visited is None:
        visited = set()

    # In order to avoid loops
    if goal in visited:
        return False

    visited.add(goal)

    # Check if the goal is already a known fact
    facts = knowledge_base.extract_facts()
    if goal in facts:
        return True

    # Check if goal is a conquent for any implication
    for clause in knowledge_base.knowledge_base:
        if isinstance(clause, Implies):
            conclusion = clause.args[1]
            premises = clause.args[0]
            if conclusion == goal:
                if isinstance(premises, Symbol):
                    if backward_chaining(premises, knowledge_base, visited):
                        return True
                elif isinstance(premises, And):
                    if all(backward_chaining(p, knowledge_base, visited) for p in premises.args):
                        return True
    return False

"""
    Forward chaining inference algorithm.
    knownledge_base (KB_class): All clauses in the KB must be horn clauses
"""
def forward_chaining(knowledge_base):
    if not knowledge_base.is_horn():
        print("⚠️: The knowledge is a non-horn KB!")
        return None

    knowledge_base.horn_to_implication()    
    
    KB_changed = True
    clauses = knowledge_base.knowledge_base
    inferenced_rules = []
    
    while KB_changed:
        KB_changed = False
        facts = knowledge_base.extract_facts()
        for clause in clauses:
            if isinstance(clause, Implies):
                if modus_ponens(clause, facts):
                    conclusion = clause.args[1]
                    if conclusion not in facts:
                        knowledge_base.add_clauses(conclusion)
                        inferenced_rules.append(conclusion)
                        KB_changed = True
    return inferenced_rules

"""
    Model checking entailment algorithm (this approach is expansive), use KB_class.entails()

    @params
        knowledge_base (KB_class.build_KB): use KB as And logical object. Use build_KB() method of KB_class
        query (list[sympy logic Objects]): List of sympy logical queries
        symbols (sympy.Symbol): list of all possible symbols
        model (dictionary): useful for recursion, leave this parameters empty
"""
def model_checking(knowledge_base, query, symbols, model):
    if not symbols:
        if knowledge_base.subs(model):
            return query.subs(model)
        return True
    else:    
        remaining = symbols.copy()
        p = remaining.pop()
    
        model_true = model.copy()
        model_true[p] = True
        model_false = model.copy()
        model_false[p] = False

        return (model_checking(knowledge_base, query, remaining, model_true)) and \
               (model_checking(knowledge_base, query, remaining, model_false))


"""
    Class that defines a Knowledge base, in order to manage it easily.
    
    @params:
        symbols_list (list): List of sympy.Symbol objects
        *clauses (Any): Each arguments will be handle as a separate clause
"""
class KB_class:
    def __init__(self, symbols_list, *clauses):
        self.knowledge_base = [clause for clause in clauses]
        self.symbols = [symbol for symbol in symbols_list]
    
    """
        Add one or more clauses to KB
    """
    def add_clauses(self, *clauses):
        for clause in clauses:
            self.knowledge_base.append(clause)

    """
        Remove one or more clauses from the KB
    """
    def remove_clauses(self, *clauses):
        self.knowledge_base = [clause for clause in self.knowledge_base if clause not in clauses]

    """
        Add one or more symbols 
    """
    def add_symbols(self, *symbols_list):
        for symbol in symbols_list:
            if isinstance(symbol, Symbol):
                self.symbols.append(symbol)
            else:
                print("Error: symbols must be sympy.Symbol object")
    
    """
        Remove one or more symbols, also the clauses which contain the removed symbols will be removed.
        sympy.Symbol.atoms() is used to extract the involved symbols in a clause
    """
    def remove_symbols(self, *symbols_list):
        self.symbols = [symbol for symbol in self.symbols if symbol not in symbols_list]
        for clause in self.knowledge_base:
            atoms = clause.atoms()
            for symbol in symbols_list:
                if symbol in atoms:
                    self.remove_clauses(clause)

    """
        Check if the whole knowlwdge base is composed by horn clauses
    """
    def is_horn(self):
        no_horn = 0
        
        for clause in self.knowledge_base:
            if not check_horn(clause):
                no_horn += 1
        if no_horn > 0:
            return False
        return True

    """
        Replace all horn clauses with their respective implication
    """
    def horn_to_implication(self):
        for clause in self.knowledge_base:
            if check_horn(clause) and isinstance(clause, Or):
                self.add_clauses(horn_to_implication(clause))
                self.remove_clauses(clause)
    
    """
        Returns the known facts in the knowledge base
    """
    def extract_facts(self):
        facts = []
        for clause in self.knowledge_base:
                if len(clause.atoms()) == 1:
                    facts.append(clause)
        return facts

    """
        Print all knowledge base facts/rules
    """
    def print_clauses(self):
        for clause in self.knowledge_base:
            print(clause)

    """
        Print all knowledge base symbols
    """
    def print_symbols(self):
        print(self.symbols)

    """
        Check if a sentence contained into the KB
    """
    def contains(self, clause):
        if clause not in self.knowledge_base:
            return False
        return True

    """
        Return KB as a unique AND
    """
    def build_KB(self):
        return And(*self.knowledge_base)
    
    """
        Check if KB entail a query alpha (KB:=a) using inference by resolution
    """
    def entails(self, query):
        kb_as_and = self.build_KB()
        join_expression = And(kb_as_and, Not(query))
        join_expression = to_cnf(join_expression, simplify=True)
        if not satisfiable(join_expression):
           return True
        return False