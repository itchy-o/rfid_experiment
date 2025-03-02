#! /bin/sh -x

CIRCUITPY=/media/mew/CIRCUITPY

TGTDIR=$CIRCUITPY/$(basename $(pwd))

mkdir -p $TGTDIR

echo "gitdir: $(pwd)/.git" > $TGTDIR/.git

cd "$TGTDIR"
git checkout
git checkout .
