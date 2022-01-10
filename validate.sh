#!/bin/bash
for (( in=1; in<7; in++ ))
do
  printf '%s' "Instance $in"
  printf "\n"
  input="resources/instance$in"
  for j in "1m" "5m" "un";
  do
    out="results/res-$j-i$in.txt"
    python validator.py -i $input -o $out
  done
done
printf "\n"