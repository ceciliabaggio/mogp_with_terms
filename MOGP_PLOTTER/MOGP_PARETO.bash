#!/bin/bash


co1='/media/cecilia/DISCO2/mogp_with_terms_results/Co1/'
co2='/media/cecilia/DISCO2/mogp_with_terms_results/Co2/'
co3='/media/cecilia/DISCO2/mogp_with_terms_results/Co3/'
co4='/media/cecilia/DISCO2/mogp_with_terms_results/Co4/'
co5='/media/cecilia/DISCO2/mogp_with_terms_results/Co5/'
co6='/media/cecilia/DISCO2/mogp_with_terms_results/Co6/'
co7='/media/cecilia/DISCO2/mogp_with_terms_results/Co7/'

# python generar_paretos_Pr_Rec.py <directorio><combinacion><popsize>
python generar_paretos_Pr_Rec.py $co1 1 100
python generar_paretos_Pr_Rec.py $co2 2 100
python generar_paretos_Pr_Rec.py $co3 3 100
python generar_paretos_Pr_Rec.py $co4 4 100
python generar_paretos_Pr_Rec.py $co5 5 100
python generar_paretos_Pr_Rec.py $co6 6 100
python generar_paretos_Pr_Rec.py $co7 7 100



