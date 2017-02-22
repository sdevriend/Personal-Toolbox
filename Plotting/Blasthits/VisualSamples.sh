#!/bin/bash
# This script parses the data from the sampledir and genome dir into plots
# that are stored in the outdir. 

# The script takes each file and loops through the contig of each file.
# for each contig the length is taken from the sample genome at the contig site.
# For each contig the visualContig script is used to create a visualisation.

# INPUT:
# The samples need to be in tabular blast output.
# The program can handle SAMPLENAME|PROKKA|CONTIGNUMBER
# Please make sure that the blastfiles are named as followed:
# SAMPLENAME_out.out


# INPUT Genomes:
# The program needs to have genomes of the samples. Please name the GENOMES
# as SAMPLENAME.fa


#SAMPLESDIR="/media/sf_D_DRIVE/Dropbox/werk/Generade-TOPLAB-2016/Blastx/BC/"
SAMPLESDIR="/media/sf_D_DRIVE/TOPLAB/visual_17-8/INPUT_BC_FINAL/"
GENOMEDIR="/media/sf_D_DRIVE/TOPLAB/visual_17-8/Genomes_BC/"
OUTDIR="/media/sf_D_DRIVE/TOPLAB/visual_17-8/FINAL_RES/"

#Creation of directories
if [ ! -d "${OUTDIR}" ]
then
mkdir -p "${OUTDIR}"
fi

for FILE in $( ls ${SAMPLESDIR}*.out* )
do
	samplename=$( awk -F '/' '{ print $NF} ' <<< ${FILE} | awk -F '_' '{print $1}') 
	sampledir="${OUTDIR}${samplename}"
    contigs=($( cat ${FILE} | awk '{print $1}' | sort | uniq ))
	if [ ! -d "${sampledir}" ]
	then
		mkdir -p "${sampledir}"
	fi
	for contig in "${contigs[@]}"
	do
		
		contigid=$( awk -F '|' '{print $NF}' <<< ${contig} )
		
		length=$( cat ${GENOMEDIR}${samplename}.fasta | egrep -A 1 "${contigid}" | awk '{ if(substr($1, 1, 1) != ">") print length($1) }')
		tempfilename="${sampledir}/${contigid}"
		$( cat ${FILE} | egrep "${contigid}" > "${tempfilename}")
		python VisualContig.py ${tempfilename} ${contig} ${length}
		rm "${tempfilename}"
		
	done 
done
