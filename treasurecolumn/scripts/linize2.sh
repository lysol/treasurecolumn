RANDOM=$$
width=320
height=214
phase=$3
lines=("$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]" "$[RANDOM % height]")
convert $1 -scale 320x214 -depth 4 /tmp/small.png
convert /tmp/small.png -contrast -contrast -colorspace YIQ -channel Y -ordered-dither ${phase} -colorspace RGB -scale 320x214 \
   -fill "#FFF0" -stroke "#FFF2" -strokewidth "$[RANDOM % 17 + 5]" -draw "line 0,${lines[0]} $width,${lines[0]}" \
   -fill "#FFF0" -stroke "#F0F2" -strokewidth "$[RANDOM % 17 + 5]" -draw "line 0,${lines[1]} $width,${lines[1]}" \
   -fill "#FFF0" -stroke "#F0F2" -strokewidth "$[RANDOM % 17 + 5]" -draw "line 0,${lines[2]} $width,${lines[2]}" \
   -fill "#FFF0" -stroke "#F002" -strokewidth "$[RANDOM % 17 + 5]" -draw "line 0,${lines[3]} $width,${lines[3]}" \
   -fill "#FFF0" -stroke "#FF02" -strokewidth "$[RANDOM % 17 + 5]" -draw "line 0,${lines[4]} $width,${lines[4]}" \
   -fill "#FFF0" -stroke "#0FF2" -strokewidth "$[RANDOM % 17 + 5]" -draw "line 0,${lines[5]} $width,${lines[5]}" \
   -alpha on \
   -depth 4 \
   -contrast -contrast -contrast \
   $1 -compose blend -define "compose:args=95,10" -define "geometry:args=320,214" -geometry 320x214 -composite \
   -contrast -contrast -contrast -contrast  -contrast -contrast  -contrast -contrast -resize 320x214 $2
# composite -compose lighten -geometry 320x214 /tmp/small.png - $2