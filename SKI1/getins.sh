#!/bin/bash
echo $1 $2
#function sourcefile

grep "$1.*$2" snowboard/testsuite/kernel/linux-5.12-rc3/vmlinux.map | cut -d":" -f 1 > $1.ins

while read line
do
        # echo "grep $line ssdata/sequential-analysis-2023-05-02-21-34-29/PMC-2019-05-03-02-52-88/uncommon-ins-pair.txt"
        grep $line ssdata/sequential-analysis-2023-05-02-21-34-29/PMC-2019-05-03-02-52-88/uncommon-ins-pair.txt >> tmp-ins-pair.txt
done < $1.ins
