'''
Created on May 14, 2018

@author: cecilia
'''

import sys

######################################
# GP Tree compilation functions      #
######################################
def compile(expr, pset):
    """Compile the expression *expr*.

    :param expr: Expression to compile. It can either be a PrimitiveTree,
                 a string of Python code or any object that when
                 converted into string produced a valid Python code
                 expression.
    :param pset: Primitive set against which the expression is compile.
    :returns: a function if the primitive set has 1 or more arguments,
              or return the results produced by evaluating the tree.
    """
    
    # if there are quotes inside a Spot
    # they come like this AND('"s$#$ec"', '"Sun"')
    # and are replaced after the eval
    
    code = str(expr)
    #print "code:", code
    
    if len(pset.arguments) > 0:
        # This section is a stripped version of the lambdify
        # function of SymPy 0.6.6.
        args = ",".join(arg for arg in pset.arguments)
        code = "lambda {args}: {code}".format(args=args, code=code)        

    try:
             
        result = eval(code, pset.context, {})    

        # replace the '$#$' for '\\"' so Lucene can process it        
        result = result.replace('$#$','\\"')        
        print "result after replace: ", repr(result)
        return result
    except MemoryError:
        _, _, traceback = sys.exc_info()
        raise MemoryError, ("DEAP : Error in tree evaluation :"
        " Python cannot evaluate a tree higher than 90. "
        "To avoid this problem, you should use bloat control on your "
        "operators. See the DEAP documentation for more information. "
        "DEAP will now abort."), traceback
        
        
        