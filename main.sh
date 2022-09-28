#!/bin/bash

case "$1" in

    calc)
        python -m gtrends.calc ${@:2}
        ;;

    collect)
        python -m gtrends.collect ${@:2}
        ;;

    *)
        echo "Usage:"
        echo "  $0 <command>"
        echo "Available command:"
        echo "  calc"
        echo "  collect"
esac
