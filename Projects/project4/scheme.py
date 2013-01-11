"""This module implements the core Scheme interpreter functions, including the
eval/apply mutual recurrence, environment model, and read-eval-print loop.
"""

from buffer import Buffer
from scheme_primitives import *
from scheme_reader import *
from scheme_tokens import tokenize_lines, DELIMITERS
from ucb import main, trace

##############
# Eval/Apply #
##############
#@trace
def scheme_eval(expr, env):
    """Evaluate Scheme expression EXPR in environment ENV.

    >>> expr = read_line("(+ 2 2)")
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    if expr is None:
        raise SchemeError("Cannot evaluate an undefined expression.")

    # Evaluate Atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif scheme_atomp(expr):
        return expr

    # All non-atomic expressions are lists.
    if not scheme_listp(expr):
        raise SchemeError("malformed list: {0}".format(str(expr)))
    first, rest = expr.first, expr.second

    # Evaluate Combinations
    if first in LOGIC_FORMS:
        return scheme_eval(LOGIC_FORMS[first](rest, env), env)
    elif first == "lambda":
        return do_lambda_form(rest, env)
    elif first == "mu":
        return do_mu_form(rest)
    elif first == "define":
        return do_define_form(rest, env)
    elif first == "quote":
        return do_quote_form(rest)
    elif first == "let":
        expr, env = do_let_form(rest, env)
        return scheme_eval(expr, env)
    else:
        procedure = scheme_eval(first, env)
        args = rest.map(lambda operand: scheme_eval(operand, env))
        return scheme_apply(procedure, args, env)
#@trace
def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS in environment ENV.
    >>> env = create_global_frame()
    >>> scheme_eval(read_line("(f2 2)"), env) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    SchemeError:"""
    if isinstance(procedure, PrimitiveProcedure):
        return apply_primitive(procedure, args, env)
    elif isinstance(procedure, LambdaProcedure):
        "*** YOUR CODE HERE ***"
        #need to call a new frame with the parent environment that the lambda procedure was defined in 
        frame1 = procedure.env.make_call_frame(procedure.formals, args)
        return scheme_eval(procedure.body, frame1)
    elif isinstance(procedure, MuProcedure):
        "*** YOUR CODE HERE ***"
        #call a new frame with the parent environment that the mu procedure is called in
        frame1 = env.make_call_frame(procedure.formals, args)
        return scheme_eval(procedure.body, frame1)
    else:
        raise SchemeError("Cannot call {0}".format(str(procedure)))
#@trace
def apply_primitive(procedure, args, env):
    """Apply PrimitiveProcedure PROCEDURE to a Scheme list of ARGS in ENV.

    >>> env = create_global_frame()
    >>> plus = env.bindings["+"]
    >>> twos = Pair(2, Pair(2, nil))
    >>> apply_primitive(plus, twos, env)
    4
    """
    "*** YOUR CODE HERE ***"
    try:
        arguments = [] #make a list to hold each argument
        while args != nil:
            arguments.append(args.first)
            args = args.second
        if procedure.use_env: #if the procedure requires the env, append to the argument list
            arguments.append(env)
        return procedure.fn(*arguments)
        
    except TypeError:
        raise SchemeError()
        

################
# Environments #
################

class Frame(object):
    """An environment frame binds Scheme symbols to Scheme values."""

    def __init__(self, parent):
        """An empty frame with a PARENT frame (that may be None)."""
        self.bindings = {}
        self.parent = parent

    def __repr__(self):
        if self.parent is None:
            return "<Global Frame>"
        else:
            s = sorted('{0}: {1}'.format(k,v) for k,v in self.bindings.items())
            return "<{{{0}}} -> {1}>".format(', '.join(s), repr(self.parent))

    def lookup(self, symbol):
        """Return the value bound to SYMBOL.  Errors if SYMBOL is not found."""
        "*** YOUR CODE HERE ***"
        if symbol in self.bindings: #if symbol is in the bindings of the env, return it
            return self.bindings[symbol]
        elif self.parent: #else look through each successive parent frame until reach the global frame
            return Frame.lookup(self.parent, symbol)
        else:
            raise SchemeError("unknown identifier: {0}".format(str(symbol)))

    def global_frame(self):
        """The global environment at the root of the parent chain."""
        e = self
        while e.parent is not None:
            e = e.parent
        return e

    def make_call_frame(self, formals, vals):
        """Return a new local frame whose parent is SELF, in which the symbols
        in the Scheme formal parameter list FORMALS are bound to the Scheme
        values in the Scheme value list VALS.

        >>> env = create_global_frame()
        >>> formals, vals = read_line("(a b c)"), read_line("(1 2 3)")
        >>> env.make_call_frame(formals, vals)
        <{a: 1, b: 2, c: 3} -> <Global Frame>>
        >>> formals, vals = read_line("(a b c)"), read_line("(1 2)")
        >>> env.make_call_frame(formals, vals) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        SchemeError:
        """
        frame = Frame(self)
        "*** YOUR CODE HERE ***"
        if len(vals) == len(formals): #check to make sure that the number of values is equivalent to the number of formals
            while len(vals) > 0 and len(formals) > 0:
                frame.define(formals.first, vals.first) #iterate through each val and formal and defining it in new frame
                vals, formals = vals.second, formals.second
            return frame
        else:
            raise SchemeError('more values or args than there are arguments or vals')

    def define(self, sym, val):
        """Define Scheme symbol SYM to have value VAL in SELF."""
        self.bindings[sym] = val

class LambdaProcedure(object):
    """A procedure defined by a lambda expression or the complex define form."""

    def __init__(self, formals, body, env):
        """A procedure whose formal parameter list is FORMALS (a Scheme list),
        whose body is the single Scheme expression BODY, and whose parent
        environment is the Frame ENV.  A lambda expression containing multiple
        expressions, such as (lambda (x) (display x) (+ x 1)) can be handled by
        using (begin (display x) (+ x 1)) as the body."""
        self.formals = formals
        self.body = body
        self.env = env

    def __str__(self):
        return "(lambda {0} {1})".format(str(self.formals), str(self.body))

    def __repr__(self):
        args = (self.formals, self.body, self.env)
        return "LambdaProcedure({0}, {1}, {2})".format(*(repr(a) for a in args))

class MuProcedure(object):
    """A procedure defined by a mu expression, which has dynamic scope.
     _________________
    < Scheme is cool! >
     -----------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
    """

    def __init__(self, formals, body):
        """A procedure whose formal parameter list is FORMALS (a Scheme list),
        whose body is the single Scheme expression BODY.  A mu expression
        containing multiple expressions, such as (mu (x) (display x) (+ x 1))
        can be handled by using (begin (display x) (+ x 1)) as the body."""
        self.formals = formals
        self.body = body

    def __str__(self):
        return "(mu {0} {1})".format(str(self.formals), str(self.body))

    def __repr__(self):
        args = (self.formals, self.body)
        return "MuProcedure({0}, {1})".format(*(repr(a) for a in args))


#################
# Special forms #
#################
#@trace
def do_lambda_form(vals, env):
    """Evaluate a lambda form with parameters VALS in environment ENV."""
    check_form(vals, 2)
    formals = vals[0]
    check_formals(formals)
    "*** YOUR CODE HERE ***"
    body = vals[1]
    if len(vals) > 2:
        body = Pair('begin', vals.second) #if the body has more than 1 expression, add begin
    return LambdaProcedure(formals, body, env)
    
#@trace
def do_mu_form(vals):
    """Evaluate a mu form with parameters VALS."""
    check_form(vals, 2)
    formals = vals[0]
    check_formals(formals)
    "*** YOUR CODE HERE ***"
    body = vals[1]
    if len(vals) > 2:
        body = Pair('begin', vals.second) #if the body has more than 1 expression, add begin
    return MuProcedure(formals, body)

#@trace
def do_define_form(vals, env):
    """Evaluate a define form with parameters VALS in environment ENV.
    >>> global_frame = create_global_frame()
    >>> frame1 = Frame(global_frame)
    >>> global_frame.define('a', 1)
    >>> global_frame.define('b', 4)
    >>> frame1.define('a', 2)
    >>> frame1.define('c', 3)
    >>> frame1.lookup('a')
    2
    >>> frame1.lookup('b')
    4
    >>> frame1.lookup('c')
    3
    >>> global_frame.lookup('a')
    1
    >>> global_frame.lookup('c') # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    SchemeError:
    >>> env = create_global_frame()
    >>> vals = read_line('( (pow x y) (* x y) )')
    >>> do_define_form(vals, env)
    >>> print(env.lookup('pow'))
    (lambda (x y) (* x y))
    >>> vals = read_line('( (0 x y) (* x y) )')
    >>> do_define_form(vals, env) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    SchemeError:"""
    check_form(vals, 2)
    target = vals[0]
    if scheme_symbolp(target):
        check_form(vals, 2, 2)
        "*** YOUR CODE HERE ***"
        env.define(target, scheme_eval(vals[1], env))
        
    elif isinstance(target, Pair):
        "*** YOUR CODE HERE ***"
        params = target.second
        if not scheme_symbolp(target.first): #check that target is a valid scheme formal
            raise SchemeError('not a valid argument to define')
        body = vals.second
        values = Pair(params, body)
        env.define(target.first, do_lambda_form(values, env)) #if target is defining a lambda function, create new lambda procedure
    else:
        raise SchemeError("bad argument to define")

def do_quote_form(vals):
    """Evaluate a quote form with parameters VALS."""
    check_form(vals, 1, 1)
    "*** YOUR CODE HERE ***"
    return vals[0]

def do_let_form(vals, env):
    """Evaluate a let form with parameters VALS in environment ENV."""
    check_form(vals, 2)
    bindings = vals[0]
    exprs = vals.second
    if not scheme_listp(bindings):
        raise SchemeError("bad bindings list in let form")

    # Add a frame containing bindings
    names, vals = nil, nil
    "*** YOUR CODE HERE ***"
    for value in bindings:
        if len(value) > 2:
            raise SchemeError('bad bindings in let form')
        vals = Pair(scheme_eval(value[1], env), vals)
        names = Pair(value.first, names)    
    new_env = env.make_call_frame(names, vals) #create new frame with all the names and vals in their respective sequential order    

    # Evaluate all but the last expression after bindings, and return the last
    last = len(exprs)-1
    for i in range(0, last):
        scheme_eval(exprs[i], new_env)
    return exprs[last], new_env

#########################
# Logical Special Forms #
#########################
#@trace
def do_if_form(vals, env):
    """Evaluate if form with parameters VALS in environment ENV."""
    check_form(vals, 3, 3)
    "*** YOUR CODE HERE ***"
    ret_val = scheme_eval(vals[0], env)
    if scheme_true(ret_val): 
        return vals[1] #return 1st expression if condition is true
    else:
        return vals[2] #return 2nd expression if condition is true

def do_and_form(vals, env):
    """Evaluate short-circuited and with parameters VALS in environment ENV."""
    "*** YOUR CODE HERE ***"
    if len(vals) == 0:
        return True
    for val in vals:
        ret_val = scheme_eval(val, env)
        if scheme_false(ret_val):
            return False
    return vals[len(vals)-1]      #return val of second expression if condition is true, returns false otherwise
        

def do_or_form(vals, env):
    """Evaluate short-circuited or with parameters VALS in environment ENV."""
    "*** YOUR CODE HERE ***"
    if len(vals) == 0:
        return False
    for val in vals:
        return_val = scheme_eval(val, env)
        if scheme_true(return_val):
            return return_val           #return val of first expression to eval true, returns false otherwise
    return False

    
#@trace
def do_cond_form(vals, env):
    """Evaluate cond form with parameters VALS in environment ENV.
    >>> env = create_global_frame()
    >>> scheme_eval(read_line("(cond ((= 1 2)))"), env) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    SchemeError:"""
    num_clauses = len(vals)
    for i, clause in enumerate(vals):
        check_form(clause, 1)
        if clause.first == "else":
            if i < num_clauses-1:
                raise SchemeError("else must be last")
            test = True
            if clause.second is nil:
                raise SchemeError("badly formed else clause")
        else:
            test = scheme_eval(clause.first, env)
        if test:
            "*** YOUR CODE HERE ***"
            if scheme_true(test):
                if clause.second == nil:
                    return test
            if len(clause.second) > 1:
                    return do_begin_form(clause.second, env)
            return clause.second.first #return first clause that has a condition that evaluates as true. Otherwise return else clause
            
#@trace
def do_begin_form(vals, env):
    """Evaluate begin form with parameters VALS in environment ENV."""
    check_form(vals, 1)
    "*** YOUR CODE HERE ***"
    for i in range(0, len(vals)-1):  
        scheme_eval(vals[i], env)  #evaluate every expression except the last one
    return vals[len(vals)-1]       #return the last expression
        

LOGIC_FORMS = {
        "and": do_and_form,
        "or": do_or_form,
        "if": do_if_form,
        "cond": do_cond_form,
        "begin": do_begin_form,
        }

# Utility methods for checking the structure of Scheme programs

def check_form(expr, min, max = None):
    """Check EXPR (default SELF.expr) is a proper list whose length is
    at least MIN and no more than MAX (default: no maximum). Raises
    a SchemeError if this is not the case."""
    if not scheme_listp(expr):
        raise SchemeError("badly formed expression: %s", expr)
    length = len(expr)
    if length < min:
        raise SchemeError("too few operands in form")
    elif max is not None and length > max:
        raise SchemeError("too many operands in form")

#@trace
def check_formals(formals):
    """Check that FORMALS is a valid parameter list, a Scheme list of symbols
    in which each symbol is distinct.

    >>> check_formals(read_line("(a b c)"))
    >>> check_formals(read_line("(a . b)")) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    SchemeError:
    >>> check_formals(read_line("(a b c a)")) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    SchemeError:
    >>> check_formals(read_line("(a b 0 c)")) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    SchemeError:
    >>> check_formals(read_line("()"))
    """
    "*** YOUR CODE HERE ***"
    val_list = []
    if scheme_listp(formals): #make sure that the formals list is a scheme list
        for val in formals:
            if not scheme_symbolp(val): #checks every formal in formals list whether if its a valid scheme symbol
                raise SchemeError("badly formed formals: %s", formals)
            if val in val_list:
                raise SchemeError("formals require unique values")
            val_list.append(val) #create a list of vals to make sure that every formal is unique
    else:
        raise SchemeError("badly formed formals: %s", formals)

    

##################
# Tail Recursion #
##################
#@trace
def scheme_optimized_eval(expr, env):
    """Evaluate Scheme expression EXPR in environment ENV."""
    while True:
        if expr is None:
            raise SchemeError("Cannot evaluate an undefined expression.")

        # Evaluate Atoms
        if scheme_symbolp(expr):
            return env.lookup(expr)
        elif scheme_atomp(expr):
            return expr

        # All non-atomic expressions are lists.
        if not scheme_listp(expr):
            raise SchemeError("malformed list: {0}".format(str(expr)))
        first, rest = expr.first, expr.second

        # Evaluate Combinations
        if first in LOGIC_FORMS:
            "*** YOUR CODE HERE ***"
            #since there's a while loop, just make expr = the expression that was
            #generated by scheme_eval in the original scheme_eval
            #as the while loop does what scheme_eval used to do
            expr = LOGIC_FORMS[first](rest, env)
            
        elif first == "lambda":
            return do_lambda_form(rest, env)
        elif first == "mu":
            return do_mu_form(rest)
        elif first == "define":
            return do_define_form(rest, env)
        elif first == "quote":
            return do_quote_form(rest)
        elif first == "let":
            "*** YOUR CODE HERE ***"
            expr, env = do_let_form(rest, env)
        else:
            "*** YOUR CODE HERE ***"
            procedure = scheme_optimized_eval(first, env)
            args = rest.map(lambda operand: scheme_optimized_eval(operand, env))
            if isinstance(procedure, PrimitiveProcedure):
                return apply_primitive(procedure, args, env)
            elif isinstance(procedure, LambdaProcedure):
                env = procedure.env.make_call_frame(procedure.formals, args)
            elif isinstance(procedure, MuProcedure):
                env = env.make_call_frame(procedure.formals, args)
            else:
                raise SchemeError("Cannot call {0}".format(str(procedure)))
            expr = procedure.body
                        
            

################################################################
# Uncomment the following line to apply tail call optimization #
################################################################
scheme_eval = scheme_optimized_eval


################
# Input/Output #
################

def read_eval_print_loop(next_line, env):
    """Read and evaluate input until an end of file or keyboard interrupt."""
    while True:
        try:
            src = next_line()
            while src.more_on_line:
                expression = scheme_read(src)
                result = scheme_eval(expression, env)
                if result is not None:
                    print(result)
        except (SchemeError, SyntaxError, ValueError) as err:
            print("Error:", err)
        except (KeyboardInterrupt, EOFError):  # <Control>-D, etc.
            return

def scheme_load(sym, env):
    """Load Scheme source file named SYM in environment ENV."""
    check_type(sym, scheme_symbolp, 0, "load")
    with scheme_open(sym) as infile:
        lines = infile.readlines()
    def next_line():
        return buffer_lines(lines)
    read_eval_print_loop(next_line, env.global_frame())

def scheme_open(filename):
    """If either FILENAME or FILENAME.scm is the name of a valid file,
    return a Python file opened to it. Otherwise, raise an error."""
    try:
        return open(filename)
    except IOError as exc:
        if filename.endswith('.scm'):
            raise SchemeError(str(exc))
    try:
        return open(filename + '.scm')
    except IOError as exc:
        raise SchemeError(str(exc))

def create_global_frame():
    """Initialize and return a single-frame environment with built-in names."""
    env = Frame(None)
    env.define("eval", PrimitiveProcedure(scheme_eval, True))
    env.define("apply", PrimitiveProcedure(scheme_apply, True))
    env.define("load", PrimitiveProcedure(scheme_load, True))
    add_primitives(env)
    return env

@main
def run(*argv):
    next_line = buffer_input
    if argv:
        try:
            filename = argv[0]
            input_file = open(argv[0])
            lines = input_file.readlines()
            def next_line():
                return buffer_lines(lines)
        except IOError as err:
            print(err)
            sys.exit(1)
    read_eval_print_loop(next_line, create_global_frame())
