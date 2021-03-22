'''
Created on Apr 27, 2018

@author: cecilia
'''

from deap import gp
from collections import deque


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
    code = str(expr)
    if len(pset.arguments) > 0:
        # This section is a stripped version of the lambdify
        # function of SymPy 0.6.6.
        args = ",".join(arg for arg in pset.arguments)
        code = "lambda {args}: {code}".format(args=args, code=code)
    try:
        return eval(code, pset.context, {})
    except MemoryError:
        _, _, traceback = sys.exc_info()
        raise MemoryError, ("DEAP : Error in tree evaluation :"
        " Python cannot evaluate a tree higher than 90. "
        "To avoid this problem, you should use bloat control on your "
        "operators. See the DEAP documentation for more information. "
        "DEAP will now abort."), traceback

class PrimitiveTree(gp.PrimitiveTree):

    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    @classmethod
    def from_string(cls, string, pset):
        """Try to convert a string expression into a PrimitiveTree given a
        PrimitiveSet *pset*. The primitive set needs to contain every primitive
        present in the expression.

        :param string: String representation of a Python expression.
        :param pset: Primitive set from which primitives are selected.
        :returns: PrimitiveTree populated with the deserialized primitives.
        """

        #added to eliminate white spaces from begining/end of terminals
        #token_list = re.split("[\t\n\r\f\v(),]", string)        
        #tokens = [tk.strip() for tk in token_list if tk != '']
        
        ######
        # esto no va a funcionar si hay una comilla sola adentro de un spot
        # VER 
        ######
        
        
        string = string.replace("\\\'", "&%^")
        
        query_parsed=''
        in_spot=False
        for ch in string:
            if (ch == "(" or ch == ")" or ch == ",") and not in_spot:
                query_parsed+="%!%"
            elif ch == "\'"  and not in_spot:
                query_parsed+="\'"
                in_spot=True
            elif ch == "\'"  and in_spot:
                in_spot=False
                query_parsed+="\'"
            else:
                query_parsed+=ch
        
        query_parsed = query_parsed.replace("&%^", "\\\'")
        
        #print query_parsed.rsplit("%!%")  
        tokens = query_parsed.rsplit("%!%")     
        tokens = [tk.strip() for tk in tokens if tk != '']
                               
        expr = []
        ret_types = deque()
        for token in tokens:
            if token == '':
                continue
            if len(ret_types) != 0:
                type_ = ret_types.popleft()
            else:
                type_ = None

            if token in pset.mapping:
                primitive = pset.mapping[token]
                if type_ is not None and not issubclass(primitive.ret, type_):
                    raise TypeError("Primitive {} return type {} does not "
                                    "match the expected one: {}."
                                    .format(primitive, primitive.ret, type_))

                expr.append(primitive)
                if isinstance(primitive, gp.Primitive):
                    ret_types.extendleft(reversed(primitive.args))
            else:
                try:
                    token = eval(token)                   
                except NameError:                    
                    raise TypeError("Unable to evaluate terminal: {}".format(token))

                if type_ is None:
                    type_ = type(token)

                if not issubclass(type(token), type_):
                    raise TypeError("Terminal {} type {} does not "
                                    "match the expected one: {}."
                                    .format(token, type(token), type_))

                expr.append(gp.Terminal(token, False, type_))        
        return expr
        