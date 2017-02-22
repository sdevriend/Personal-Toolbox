for filename in */*
do
round=$(echo ${filename} | awk -F '/' '{print $1}')
picturefilename=$(echo ${filename} | awk -F '/' '{print $2}')
convert ${filename} -fuzz 30% -fill Red -opaque 'rgb(0, 0, 0)
' - | convert - -crop 3600x3632+0+0 - | convert - -crop 0x0+900+0 - | convert - -fuzz 10% -fill Black -opaque 'rgb(255,
0, 0)' ${round}/CONVERT_${picturefilename}
done

#CONVERT ALL DATA
#egrep to filter out earlier converts!
for filename in $(ls | egrep -v "CONVERT")
do
convert ${filename} -fuzz 30% -fill Black -opaque 'rgb(0, 0, 0)' - |
convert - -crop 3600x2848+0+0 - | convert - -crop 0x0+900+0  CONVERT_${filename}  
done
beep
#CONVERT SINGLE
for filename in "DSC_2133EDITED_NEW-SCALE.JPG" 
do
convert ${filename} -fuzz 25% -fill Black -opaque 'rgb(0, 0, 0)' - |
convert - -crop 3500x2848+0+0 - | convert - -crop 0x0+900+0  CONVERT_${filename}  
done
#CONVERT RED SINGLE
for filename in "DSC_2133EDITED_NEW-SCALE.JPG"  
do
convert ${filename} -fuzz 25% -fill Black -opaque 'rgb(0, 0, 0)' - |
convert - -crop 3500x2848+0+0 - | convert - -crop 0x0+900+0 - |
convert - -fuzz 10% -fill Black -opaque 'rgb(147, 25, 25)' SCALECONVERT_NEW_${filename} 
done
beep
