#!/bin/bash

for envdir in $(echo $PWD/../../../env0 $PWD/../../../ENV); do
    if [ -x "$envdir/bin/python" ]; then
        export ENVDIR=$envdir
        break
    fi
done

if [ -z "$ENVDIR" ]; then
    echo No envdir exist >&2
    export ENVDIR=$PWD/../../ENV
fi

export PYTHONPATH="$ENVDIR:$PWD:$PWD/../lib:$PYTHONPATH"
export PATH="$ENVDIR/bin:$PATH"
