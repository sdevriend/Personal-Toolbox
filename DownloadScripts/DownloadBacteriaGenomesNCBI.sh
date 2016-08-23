#!/bin/bash

# Script for downloading all available bacteria genomes.
# WARNING: ABOUT 40GB OF FREE SPACE IS NEEDED!
# WARNING: SCRIPT TAKES A LONG TIME TO COMPLETE DOWNLOAD
echo "start script!"
# Location with all bacteria genomes urls
wget "ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/bacteria/assembly_summary.txt"
# Checks if genome is complete. Then it prints the url location.
GenomeList=$(cat assembly_summary.txt | awk -F '\t' '{if($12=="Complete Genome") print $20}')

mkdir Genomes
cd Genomes

# create download list
touch DownloadList.txt
# fill downloadfile with prefix for downloading
for Genome in $GenomeList
do
	echo "${Genome}/*cds*.fna.gz" >> DownloadList.txt
done
# Download and extract all files in DownloadList.txt
wget -i DownloadList.txt
gunzip *