# usage
# vhsize.sh source dest
# 
# dims=`identify $1 | grep -o "[0-9]\+x[0-9]\+" | uniq`
# width=`echo $dims | sed -e 's/x[0-9]*/ /'`
# height=`echo $dims | sed -e 's/[0-9]*x/ /'`

# lines=("$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]")

channels=('R' 'G' 'B')

randchannel=${channels[$RANDOM % ${#channels[@]} ]}
convert $1 -scale 640x426 -depth 4 /tmp/small.png

xoffset=$[$RANDOM % 2 - 1]
yoffset=$[$RANDOM % 2 - 1]

# qualityx=$[$RANDOM % 4 + 8]
# qualityy=$[$RANDOM % 40 + 40]
qualityx=90
qualityy=90

dims=`identify /tmp/small.png | grep -o "[0-9]\+x[0-9]\+" | uniq`
width=`echo $dims | sed -e 's/x[0-9]*/ /'`
height=`echo $dims | sed -e 's/[0-9]*x/ /'`

colors=("FF CC AA 00 44 77 22 DD 66 55")

lines=("$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]")

convert /tmp/small.png -page +${xoffset}+${yoffset} -background black -flatten - | \
  # -distort Barrel "0.0 0.0 -0.075 1.1" - | \
convert - -contrast -colorspace YIQ -channel Y -ordered-dither diag -colorspace RGB - | \
convert - \
   -fill "#FFF0" -stroke "#FFF2" -strokewidth "$[RANDOM % 17 + 5]" -draw "line 0,${lines[0]} $width,${lines[0]}" \
   -fill "#FFF0" -stroke "#F0F2" -strokewidth "$[RANDOM % 17 + 5]" -draw "line 0,${lines[1]} $width,${lines[1]}" \
   -fill "#FFF0" -stroke "#F0F2" -strokewidth "$[RANDOM % 17 + 5]" -draw "line 0,${lines[2]} $width,${lines[2]}" \
   -fill "#FFF0" -stroke "#F002" -strokewidth "$[RANDOM % 17 + 5]" -draw "line 0,${lines[3]} $width,${lines[3]}" \
   -fill "#FFF0" -stroke "#FF02" -strokewidth "$[RANDOM % 17 + 5]" -draw "line 0,${lines[4]} $width,${lines[4]}" \
   -fill "#FFF0" -stroke "#0FF2" -strokewidth "$[RANDOM % 17 + 5]" -draw "line 0,${lines[5]} $width,${lines[5]}" \
   -contrast -contrast -contrast -contrast \
   -  | \
   # convert - \
   #    -stroke "${colors[$[RANDOM % 10]]}${colors[$[RANDOM % 10]]}" -strokewidth "$[RANDOM % 17 + 5]" -draw "line 0,${lines[0]} $width,${lines[0]}" \
   #    -stroke "${colors[$[RANDOM % 10]]}${colors[$[RANDOM % 10]]}" -strokewidth "$[RANDOM % 17 + 5]" -draw "line 0,${lines[1]} $width,${lines[1]}" \
   #    -stroke "${colors[$[RANDOM % 10]]}${colors[$[RANDOM % 10]]}" -strokewidth "$[RANDOM % 17 + 5]" -draw "line 0,${lines[2]} $width,${lines[2]}" \
   #    -stroke "${colors[$[RANDOM % 10]]}${colors[$[RANDOM % 10]]}" -strokewidth "$[RANDOM % 17 + 5]" -draw "line 0,${lines[3]} $width,${lines[3]}" \
   #    -stroke "${colors[$[RANDOM % 10]]}${colors[$[RANDOM % 10]]}" -strokewidth "$[RANDOM % 17 + 5]" -draw "line 0,${lines[4]} $width,${lines[4]}" \
   #    -stroke "${colors[$[RANDOM % 10]]}${colors[$[RANDOM % 10]]}" -strokewidth "$[RANDOM % 17 + 5]" -draw "line 0,${lines[5]} $width,${lines[5]}" \
   #    -contrast -contrast -contrast  -normalize -contrast \
   #    -  | \
# convert - -modulate 50,500 -contrast -contrast - | \
convert - -quality $qualityx -  | \
composite -geometry "${width}x${height}" -alpha on -blend 50x60 -quality $qualityy /tmp/small.png - -  | \
convert - -scale 640x426 -contrast -contrast - | \
# composite -compose Darken -quality 90 -alpha on -tile dotcrawl.png - -  | \
# convert - -contrast $2

#convert - -scale 400x400 -quality 1 -contrast -contrast -contrast $2
# composite -quality 90 -alpha on -blend 50% -tile colornoise.png - - | \
composite -blend 50% -compose lighten -geometry 640x426 $1 - $2
# composite -quality 90 -alpha on -blend 20% -tile dotcrawl.png - $2 
#convert - -contrast -contrast -contrast $2

