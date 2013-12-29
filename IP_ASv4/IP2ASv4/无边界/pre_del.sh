#!/bin/bash
cd traceroute
for filename in `ls`
do
echo $filename
sed -i '/#/d' $filename
done
