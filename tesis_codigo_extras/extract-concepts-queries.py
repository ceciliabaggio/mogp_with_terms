
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
    

f = open('repos/mogp_with_terms/tesis_codigo_extras/Co3_529_1_EntropicPrec@10-EntropicRecall_nGen(150)_popSize(100)_indSize(XX)_cross(0.7)_mut(0.3)_seed(12803)_queries_gen150.txt', 'r')
s = f.read()
f.close()

conceptos = set()
terminos = set()


# ###### TO DO: borrar la coma solo si a izquierda tiene parentesis que cierra y a derecha un espacio y luego una A o N o O o comilla simple
s = s.replace('\n', ',')

tokens = s.split(",")





for token in tokens:
    t = find_between(token, "'\"", "\"'")    
    
    if t and t[0].isupper(): # primero chequea que t no sea vacio
        conceptos.add(t)
    else:
        terminos.add(t)



print("############################### CONCEPTOS ")
print(conceptos)
print("############################### TERMINOS ")
print(terminos)
