for filename in */*
do
round=$(echo ${filename} | awk -F '/' '{print $1}')
picturefilename=$(echo ${filename} | awk -F '/' '{print $2}')
convert ${filename} -fuzz 30% -fill Red -opaque 'rgb(0, 0, 0)
' - | convert - -crop 3600x3632+0+0 - | convert - -crop 0x0+900+0 - | convert - -fuzz 10% -fill Black -opaque 'rgb(255,
0, 0)' ${round}/CONVERT_${picturefilename}
done
