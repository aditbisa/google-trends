#!/bin/bash

case "$1" in

    calc)
        python gtrends/calc.py ${@:2}
        ;;

    collect)
        python gtrends/collect.py ${@:2}
        ;;

    *)
        echo "Usage:"
        echo "  $0 <command>"
        echo "Available command:"
        echo "  calc"
        echo "  collect"
esac
