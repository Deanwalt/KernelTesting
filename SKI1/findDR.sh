#!/bin/bash
if [ "$REDIS_URL" = "" ]; then
	cd snowboard/scripts/
	source setup.sh /home/wangguangke/SKI/ssdata/
	cd ../../
	echo "$REDIS_URL"
fi

find $1 -name "concurrent-test*[^sh]" > concutest
sort concutest > concutest.tmp
lines=$(wc -l concutest.tmp | cut -d " " -f 1)
num=$(($lines-1))

head -n $num concutest.tmp > concutest.new

while read raw
do
	echo $raw
	
	du $raw/2023*ins*.txt

	if [ -f $raw/*.txt.source ]; then
		echo "exists!"
		# rm $raw/*.txt.source
		continue
	elif [ -f $raw/2023*race*de*.txt ]; then
		echo "analysis..."
		cd snowboard/scripts/analysis/
		./data-race.sh ../../../$raw
		cd ../../../
	else
		echo "no file in this dir!"
	fi

		
	echo ""
done < concutest.new
		
# exit

find $1 -name "2023*.txt.source" > sou.paths

while read path
do
	echo "about : $path "
	grep -n --color=auto "free_block" $path
	#echo "+and+"
	grep -n --color=auto "cache_alloc_refill" $path

	#echo "======================================================="
	grep -n --color=auto "uart_do_autoconfig" $path
	#echo "+and+"
	grep -n --color=auto "tty_port_open" $path

	#echo "======================================================="
	grep -n --color=auto "snd_ctl_elem_add" $path

	#echo "======================================================="
	grep -n --color=auto "tcp_set_congestion_control" $path
	#echo "+and+"
	grep -n --color=auto "tcp_set_default_congestion_control" $path

	#echo "======================================================="
	grep -n --color=auto "__fanout_unlink" $path
	#echo "+and+"
	grep -n --color=auto "fanout_demux_rollover" $path

	grep -n --color=auto "l2tp_tunnel_register" $path

	grep -n --color=auto "pppol2tp_connect" $path
	grep -n --color=auto "l2tp_xmit_core" $path
	grep -n --color=auto "spin_lock(&configfs_dirent_lock)" $path

	grep -n --color=auto "configfs_lookup" $path
	echo "==============================================================="
done < sou.paths

rm sou.paths
rm concutest
rm concutest.new concutest.tmp
