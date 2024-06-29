#!/bin/bash

# Detect architecture
ARCH=$(uname -m)

if [ "$ARCH" = "x86_64" ]; then
    echo "Running on x86_64 architecture"
    # Commands for x86_64 architecture
elif [ "$ARCH" = "arm64" ] || [ "$ARCH" = "aarch64" ]; then
    echo "Running on arm64 architecture"
    # Commands for arm64/aarch64 architecture
else
    echo "Unknown architecture: $ARCH"
    exit 1
fi
