#!/bin/bash


co1='/home/cecilia/workspace/MOGP_multiple_op_AND_OR_NOT_results/Co1/'
co2='/home/cecilia/workspace/MOGP_multiple_op_AND_OR_NOT_results/Co2/'
co3='/home/cecilia/workspace/MOGP_multiple_op_AND_OR_NOT_results/Co3/'
co4='/home/cecilia/workspace/MOGP_multiple_op_AND_OR_NOT_results/Co4/'
co5='/home/cecilia/workspace/MOGP_multiple_op_AND_OR_NOT_results/Co5/'
co6='/home/cecilia/workspace/MOGP_multiple_op_AND_OR_NOT_results/Co6/'
co7='/home/cecilia/workspace/MOGP_multiple_op_AND_OR_NOT_results/Co7/'

# python generar_paretos_Pr_Rec.py <directorio><combinacion><popsize>
python generar_paretos_Pr_Rec.py $co1 1 100
python generar_paretos_Pr_Rec.py $co2 2 100
python generar_paretos_Pr_Rec.py $co3 3 100
python generar_paretos_Pr_Rec.py $co4 4 100
python generar_paretos_Pr_Rec.py $co5 5 100
python generar_paretos_Pr_Rec.py $co6 6 100
python generar_paretos_Pr_Rec.py $co7 7 100



