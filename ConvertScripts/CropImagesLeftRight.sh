
for f in *
do
convert ${f} -crop 5000x3632+0+0  - | convert - -crop 0x0+550+0 convert_${f}
done
