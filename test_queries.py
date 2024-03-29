#!/usr/bin/env python
'''
Created on May 10, 2018

@author: cecilia
'''
from index import SearchFiles

from sets import Set
S = Set(['134_1080', '134_1082', '134_1083', '134_1085', '134_1086', '134_453', '134_511', '134_100', '134_899', '134_898', '134_891', '134_896', '134_586', '134_351', '134_355', '134_352', '134_728', '134_358', '134_873', '134_200', '134_682', '134_687', '134_195', '134_196', '134_68', '134_193', '134_63', '134_969', '134_66', '134_613', '134_1247', '134_758', '134_610', '134_616', '134_1240', '134_806', '134_804', '134_751', '134_803', '134_800', '134_801', '134_85', '134_86', '134_81', '134_83', '134_82', '134_538', '134_88', '134_458', '134_432', '134_431', '134_435', '134_338', '134_1011', '134_1016', '134_19', '134_218', '134_708', '134_333', '134_336', '134_701', '134_702', '134_704', '134_707', '134_545', '134_1076', '134_542', '134_227', '134_839', '134_220', '134_1070', '134_1147', '134_1141', '134_1224', '134_985', '134_1149', '134_981', '134_868', '134_869', '134_639', '134_638', '134_636', '134_1332', '134_865', '134_633', '134_632', '134_142', '134_147', '134_413', '134_148', '134_418', '134_387', '134_799', '134_1362', '134_666', '134_1262', '134_1032', '134_1034', '134_1071', '134_38', '134_33', '134_34', '134_36', '134_814', '134_648', '134_311', '134_317', '134_314', '134_278', '134_562', '134_564', '134_818', '134_569', '134_1228', '134_246', '134_1203', '134_840', '134_847', '134_844', '134_1209', '134_1354', '134_1350', '134_956', '134_346', '134_1183', '134_169', '134_168', '134_164', '134_166', '134_94', '134_362', '134_93', '134_52', '134_1026', '134_56', '134_523', '134_1059', '134_1027', '134_1054', '134_1050', '134_1116', '134_760', '134_767', '134_936', '134_1294', '134_935', '134_486', '134_1293', '134_931', '134_267', '134_264', '134_460', '134_721', '134_463', '134_469', '134_205', '134_1373', '134_1370', '134_59', '134_217', '134_215', '134_343', '134_690', '134_344', '134_694', '134_1074', '134_1077', '134_184', '134_78', '134_1179', '134_1073', '134_74', '134_1079', '134_71', '134_1273', '134_665', '134_815', '134_1276', '134_817', '134_744', '134_954', '134_668', '134_669', '134_524', '134_527', '134_1098', '134_92', '134_520', '134_90', '134_91', '134_1093', '134_1097', '134_281', '134_99', '134_884', '134_885', '134_119', '134_448', '134_881', '134_444', '134_445', '134_111', '134_112', '134_932', '134_484', '134_597', '134_599', '134_322', '134_326', '134_325', '134_735', '134_736', '134_732', '134_733', '134_231', '134_235', '134_252', '134_1152', '134_1153', '134_795', '134_977', '134_612', '134_1250', '134_1158', '134_1254', '134_600', '134_601', '134_603', '134_604', '134_607', '134_1303', '134_609', '134_1300', '134_876', '134_1304', '134_137', '134_780', '134_786', '134_422', '134_750', '134_483', '134_907', '134_906', '134_904', '134_903', '134_1023', '134_900', '134_461', '134_309', '134_656', '134_307', '134_301', '134_300', '134_651', '134_650', '134_555', '134_556', '134_550', '134_536', '134_256', '134_255', '134_855', '134_850', '134_995', '134_1231', '134_1321', '134_629', '134_106', '134_1324', '134_1326', '134_1329', '134_623', '134_620', '134_627', '134_151', '134_679', '134_401', '134_154', '134_1063', '134_158', '134_1197', '134_1194', '134_409', '134_1193', '134_1190', '134_396', '134_399', '134_27', '134_24', '134_22', '134_21', '134_517', '134_1041', '134_1042', '134_28', '134_1123', '134_1289', '134_498', '134_710', '134_929', '134_1129', '134_37', '134_718', '134_275', '134_271', '134_671', '134_670', '134_673', '134_674', '134_677', '134_676', '134_474', '134_577', '134_574', '134_772', '134_1340', '134_949', '134_408', '134_821', '134_178', '134_170', '134_176', '134_1220', '134_374', '134_375', '134_372', '134_1062', '134_40', '134_79', '134_1066', '134_1065', '134_49', '134_1069', '134_1106', '134_824', '134_1261', '134_699', '134_948', '134_1265', '134_823', '134_978'])
#print sorted(S, key=str.lower)




def unescape(s):
    s = s.replace("&lt;", "\\<")
    s = s.replace("&gt;", "\\>")
    s = s.replace("&#39;","\\'")
    s = s.replace("&quot;",'\\"') 
    # this has to be last:
    s = s.replace("&amp;", "\\&")
    return s

#===============================================================================
#    
# 
# s,a = SearchFiles.createAnalyzer("/home/cecilia/repos/mogp_with_spots/index/Set12_utf8.index")
# ############### ANDA - devuelve lo que tiene que devolver
# q1 = 'elementary&quot; number theory'
# 
# 
# print "query ", repr(q1)
# q1=unescape(q1)
# q1='"'+q1+'"'
# print repr(q1)
# print "\n"
# res = SearchFiles.searchWithLucene(s, a, q1)
# 
# #es un solo resultado devuelto
# for r in res:
#     print r.getDocUrl()
#     print r.getDocId()
#     
#     spot_list=r.getDocSpots()
#     
#     #capturo el SPOT del problema
#     matching = [x for x in spot_list if "elementary" in x]
#         
#     print "matching=", matching
#     for i in matching:
#         print "matching[", matching.index(i), "]=", repr(i)
#         
# print "matching=", matching
#         
# query=matching[2]
#         
# #query='"Thue\'s Theorem"'
# #query='"Pollard\'s p-1"'
#         
# print "\nquery:", repr(query)
# print "\n"
# # vuelvo a consultar a lucene con ese SPOT
# result = SearchFiles.searchWithLucene(s, a, query)
# for r in result:
#     print r.getDocUrl()
#     print r.getDocId()  
#     print r.getDocSpots() 
#     
# 
# SearchFiles.eliminateAnalyzer(s, a)     
#===============================================================================

#####################
from deap import gp
from deap import creator

def AND(spot1, spot2):
    return  '(' + spot1 + ' AND '+ spot2 + ')'  
  
def OR(spot1, spot2):    
    return '(' + spot1 + ' OR ' + spot2 + ')' 
  
""" en Lucene el NOT es binario: diferencia de conjuntos"""
def NOT(spot1, spot2):
    return '(' + spot1 + ' NOT '+ spot2 + ')'
"""
VER --> https://lucene.apache.org/core/2_9_4/queryparsersyntax.html
"""

"""Strongly Typed GP"""
pset = gp.PrimitiveSetTyped("main",in_types=[], ret_type=str)
pset.addPrimitive(AND,[str, str], str)
pset.addPrimitive(OR,[str, str], str)
pset.addPrimitive(NOT,[str, str], str)

s,a = SearchFiles.createAnalyzer("/home/cecilia/repos/mogp_with_spots/index/Set12_utf8.index")
q1 = '((("Serving Size" OR (((((("Serving Size" OR "vegetables") OR ((("recipes" OR "vegetables") OR ("cup" OR "display")) OR "fruits")) OR "brown") OR (("Serving Size" OR "vegetables") OR "brown")) OR "vegetables") OR "teaspoon")) OR ((("recipes" OR "vegetables") OR ("cup" OR ("Serving Size" OR "cup"))) OR "fruits")) OR "Potato Salad")'

q1 = '("Vegetable" OR "Fruit")'
 


prim_tree = gp.PrimitiveTree.from_string(str(q1), pset=pset)       
print prim_tree  

result = SearchFiles.searchWithLucene(s, a, q1)
print repr(q1)

for r in result:
    #print r.getDocUrl()
    print r.getDocId(), "\t\t#spots ", len(r.getDocSpots()) 

print "results: ", len(result)
     
SearchFiles.eliminateAnalyzer(s, a)   





