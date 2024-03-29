#!/bin/bash

# MOGP
jupyter nbconvert --execute --to notebook --inplace mogp_Precision10.ipynb
jupyter nbconvert --execute --to notebook --inplace mogp_Precision10_Gen_1.ipynb
jupyter nbconvert --execute --to notebook --inplace mogp_globalRecall.ipynb
jupyter nbconvert --execute --to notebook --inplace mogp_globalRecall_Gen1.ipynb
jupyter nbconvert --execute --to notebook --inplace mogp_jaccard_similarity.ipynb
jupyter nbconvert --execute --to notebook --inplace mogp_jaccard_similarity_Gen_1.ipynb

# MOEIR
jupyter nbconvert --execute --to notebook --inplace moeir_precision10.ipynb
jupyter nbconvert --execute --to notebook --inplace moeir_globalRecall.ipynb
jupyter nbconvert --execute --to notebook --inplace moeir_jaccard.ipynb

# plots - correrlos aparte. falla el plot si se corre desde bash
# jupyter nbconvert --execute --to notebook --inplace mogp_vs_moeir_p10.svg
# jupyter nbconvert --execute --to notebook --inplace mogp_vs_moeir_gr.svg
# jupyter nbconvert --execute --to notebook --inplace mogp_vs_moeir_jsi.svg

