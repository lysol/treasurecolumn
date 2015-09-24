# usage
# vhsize.sh source dest
# 
# dims=`identify $1 | grep -o "[0-9]\+x[0-9]\+" | uniq`
# width=`echo $dims | sed -e 's/x[0-9]*/ /'`
# height=`echo $dims | sed -e 's/[0-9]*x/ /'`

# lines=("$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]")

channels=('R' 'G' 'B')

# randchannel=${channels[$RANDOM % ${#channels[@]} ]}
# convert $1 -scale 420x420 /tmp/small.png

xoffset=$[$RANDOM % 2 - 1]
yoffset=$[$RANDOM % 2 - 1]
qualityx=$[$RANDOM % 80 + 20]
# qualityy=$[$RANDOM % 80 + 20]
# qualityx=90
# qualityy=90

# dims=`identify /tmp/small.png | grep -o "[0-9]\+x[0-9]\+" | uniq`
width=420
height=420

lines=("$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]")

convert $1 -scale 420x420 -contrast -contrast \
   -colorspace YIQ -channel Y -contrast -colorspace RGB \
   -modulate 100,0 -equalize \
   -modulate 100,0 \
   -contrast -contrast \
   -quality $qualityx -scale 800x800 -gravity Center -crop 93%x93%+0+0 $2

