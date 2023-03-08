#!/bin/bash

if [ $# != 9 ]
then
    echo "8 directories needed"
    echo "usage: MOGP_EVOLUTION.bash <dir_Co1> ... <dir_Co6> <dir_Co7> <DIR_TO_SAVE>"
    echo ""
    echo "WARNING: <dir_to_read_from> must start and finish with /"
    echo ""
    echo "if dont want to plot combination put quotes "
#    exit 1
fi

echo $1
echo $2
echo $3
echo $4
echo $5
echo $6
echo $7
echo $8

echo "$(pwd)"

python "$(pwd)"/MOGP_PLOTTER/plot_avgAvgAvgPrecision_at_10_Co1_Co2_Co3_Co4_Co5_Co6.py $1 $2 $3 $4 $5 $6 $7 $8
python "$(pwd)"/MOGP_PLOTTER/plot_avgAvgGlobalJacardIndex_Co1_Co2_Co3_Co4_Co5_Co6.py $1 $2 $3 $4 $5 $6 $7 $8
python "$(pwd)"/MOGP_PLOTTER/plot_avgAvgGlobalRecall_Co1_Co2_Co3_Co4_Co5_Co6.py $1 $2 $3 $4 $5 $6 $7 $8
python "$(pwd)"/MOGP_PLOTTER/plot_avgAvgAvgEntropic_Recall_Co1_Co2_Co3_Co4_Co5_Co6.py $1 $2 $3 $4 $5 $6 $7 $8 
python "$(pwd)"/MOGP_PLOTTER/plot_avgAvgAvgEntropic_Precision_Co1_Co2_Co3_Co4_Co5_Co6.py $1 $2 $3 $4 $5 $6 $7 $8
python "$(pwd)"/MOGP_PLOTTER/plot_avgAvgAvg_Recall_Co1_Co2_Co3_Co4_Co5_Co6.py $1 $2 $3 $4 $5 $6 $7 $8


# Ejemplo
#./MOGP_PLOTTER/MOGP_PLOTTER_EVOLUTION.bash /media/cecilia/DISCO2/mogp_with_terms_results/Co1/ /media/cecilia/DISCO2/mogp_with_terms_results/Co2/ /media/cecilia/DISCO2/mogp_with_terms_results/Co3/ /media/cecilia/DISCO2/mogp_with_terms_results/Co4/ /media/cecilia/DISCO2/mogp_with_terms_results/Co5/ /media/cecilia/DISCO2/mogp_with_terms_results/Co6/ /media/cecilia/DISCO2/mogp_with_terms_results/Co7/ /home/cecilia/repos/term_weighting_methods_full_testing_dataset/MOGP/


