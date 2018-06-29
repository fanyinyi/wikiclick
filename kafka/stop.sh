ps aux | grep produce | awk '{print $2}' | xargs kill -9
ps aux | grep consume | awk '{print $2}' | xargs kill -9
