#!/bin/bash
start=$[$RANDOM % 15 + 5]
speed=".$[$RANDOM % 3 + 3]"
tempo=".$[$RANDOM % 3 + 4]"
delay=".$[$RANDOM % 6 + 3]"
samples=$[44100 * $3]
echo $samples
echo "Starting at $start, Speed is $speed, tempo is $tempo"
sox $1 $2 rate 44100 speed $speed tempo $tempo gain -n -6 channels 1 delay $delay reverb 80 30 100 100 25 gain -n -6 reverb 80 30 100 100 25 gain -n -6 silence 1 0.1 1%  reverb 80 30 100 100 25 gain -n -6 delay 0.8 norm trim =$start ${samples}s 00:00:02.0