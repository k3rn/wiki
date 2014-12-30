#!/bin/sh


startup(){
	echo "Starting the regeration server"
	fab l &
	pid="$!"
	echo "$pid" > srv.pid
}

alive() {
	kill -0 "$1" >/dev/null 2>&1
}

stop(){
	pid=$(cat srv.pid)
	if alive "$pid"; then
		echo "Killing the regeneration server"
		kill "$pid"
	fi
	rm srv.pid
}

case "$1" in
	start)
		startup
		;;
	stop)
		stop
		;;
	restart)
		stop
		startup
		;;
	*)
		echo "Usage local.sh start|stop|restart"
esac
