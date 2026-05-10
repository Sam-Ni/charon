#!/bin/bash

rustup component add miri

SYSROOT=$(cargo miri setup -v --print-sysroot)

echo "fn main() {}" > file.rs

cargo build

if [ "$1" = "mono" ]; then
    ./target/debug/charon rustc --start-from=std --include=std --no-serialize --monomorphize -- --sysroot="$SYSROOT" file.rs
else
    ./target/debug/charon rustc --start-from=std --include=std --no-serialize -- --sysroot="$SYSROOT" file.rs
fi
