#!/bin/bash
# Script converts multi fasta file to single. 
# Input: 1 Fastafile

INPUT=$1
FILENAME=$( awk -F '/' '{print $NF }' < "${INPUT}" )
stamp=$(date +"%s")

awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' < "${INPUT}" > "${INPUT}_${stamp}"
sleep 1
cat "${INPUT}_${stamp}" > "${INPUT}"
sleep 1
rm "${INPUT}_${stamp}"
