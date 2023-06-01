grep -n --color=auto "free_block" $1
#echo "+and+"
grep -n --color=auto "cache_alloc_refill" $1

#echo "======================================================="
grep -n --color=auto "uart_do_autoconfig" $1
#echo "+and+"
grep -n --color=auto "tty_port_open" $1

#echo "======================================================="
grep -n --color=auto "snd_ctl_elem_add" $1

#echo "======================================================="
grep -n --color=auto "tcp_set_congestion_control" $1
#echo "+and+"
grep -n --color=auto "tcp_set_default_congestion_control" $1

#echo "======================================================="
grep -n --color=auto "__fanout_unlink" $1
#echo "+and+"
grep -n --color=auto "fanout_demux_rollover" $1
#echo "==============================================================="

