#!/bin/bash

# EJEMPLO:
#./MOGP_PLOTTER_TESTING.bash /home/cecilia/workspace/MOGP_local_EVALUATION_lucene/Co1_Co2_Co3_Co4_Co5_mutacion_hoja_FULL/


if [ $# != 1 ]
then
    echo "usage: MOGP_PLOTTER_TESTING.bash <dir_of_combinations>"
    echo ""
    echo "WARNING: <dir_to_read_from> must start and finish with /"
    echo ""
    echo "donde se encuentran archivos del tipo Co1_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_GEN_1.txt"
    exit 1
fi

echo $1


python "$(pwd)"/MOGP_PLOTTER/EVAL_NORMFIT_CI_1st_and_last_gen_GLOBAL_RECALL.py $1
python "$(pwd)"/MOGP_PLOTTER/EVAL_NORMFIT_CI_1st_and_last_gen_PRECISION_at_10.py $1
python "$(pwd)"/MOGP_PLOTTER/EVAL_NORMFIT_CI_1st_and_last_gen_JACCARD.py $1
