def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
    

f = open('/home/cecilia/repos/mogp_with_terms/tesis_codigo_extras/Co3_529_1_EntropicPrec@10-EntropicRecall_nGen(150)_popSize(100)_indSize(XX)_cross(0.7)_mut(0.3)_seed(12803)_queries_last_gen.txt', 'r')
s = f.read()
f.close()

conceptos = set()
terminos = set()


# ###### TO DO: borrar la coma solo si a izquierda tiene parentesis que cierra y a derecha un espacio y luego una A o N o O o comilla simple
s = s.replace('\n', ',')

tokens = s.split(",")

for token in tokens:
    t = find_between(token, "'\"", "\"'")    
    cant = t.split(" ")
    if t and len(cant) > 1: # primero chequea que t no sea vacio, y que tenga mas de un termino sep por espacio
        conceptos.add(t)
        print("concepto: ", t)
    elif t and  t[0].isupper(): # luego si empieza con mayuscula es concepto
        conceptos.add(t)
        print("concepto upper: ", t)
    else:
        terminos.add(t)
        print("termino: ", t)


conceptos = sorted(conceptos)
terminos = sorted(terminos)

print("############################### CONCEPTOS ")
print(conceptos)
print("############################### TERMINOS ")
print(terminos)


headers = ["Terminos","Conceptos"]

#terminos.remove(terminos[0]) #borra un espacio que me quedaba de mas :@

print(terminos)
while terminos: #terminos tiene elementos
    if conceptos:#conceptos tiene elementos
        print(terminos[0] + " & " + conceptos[0] + "\\\\")
        terminos.remove(terminos[0])
        conceptos.remove(conceptos[0])
    else:
        print(terminos[0] + "\\\\")
        terminos.remove(terminos[0])

while conceptos: #a conceptos le quedan elementos
    print(" " + " & " + conceptos[0] + "\\\\")
    conceptos.remove(conceptos[0])