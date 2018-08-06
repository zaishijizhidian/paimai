#!/bin/sh
 
clean() {
  for file in $1/*
  do
    if [ -d $file ]
    then
      clean $file
    else
      echo $file
      temp=$(tail -100 $file)
      echo "$temp" > $file
    fi
  done
}
 
dir=./bid_over.logs
clean $dir

