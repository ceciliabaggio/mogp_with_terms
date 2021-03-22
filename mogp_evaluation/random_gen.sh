#!/bin/sh

#para llamarlo : 
#  ./random_gen.sh 69

if [ $# != 1 ]
then
    echo "falta argumento <seed>"
    exit 1
fi

echo "seed $1 ="$1

bash -c 'RANDOM='$1'; for i in `seq 10`; do echo -n "$RANDOM "; done; echo'


