alias show='sudo ovs-vsctl show'
alias dmp='sudo ovs-ofctl dump-flows br-sfc'
alias dmph='sudo ovs-ofctl dump-flows br-sfc | grep n_packets=[^0]'
alias dmph13='sudo ovs-ofctl dump-flows br-sfc -OOpenFlow13 | grep n_packets=[^0]'
alias dmp13='sudo ovs-ofctl dump-flows br-sfc -OOpenFlow13'

