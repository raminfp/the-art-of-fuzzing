# Coldsnap - Python Snapshot Fuzzer Example
<img src="https://i.imgur.com/3M2rHTJ.png" width="600">

Welcome to coldsnap! This example was inspired by @gamozolabs love for snapshot fuzzing and based on @h0mbre_ blog [Fuzzing Like A Caveman 4](https://h0mbre.github.io/Fuzzing-Like-A-Caveman-4/)

## Introduction
coldsnap.py is a python-based snapshot-based ptrace-based fuzzer example. The purpose of this example is to test the performance of snapshot fuzzing entirely in python and to provide education example of a snapshot fuzzer. Coldsnap uses ptrace to control the program state for saving state and for guiding the fuzzer through ptrace-applied breakpoints. This example is not meant to be a production ready fuzzer. Instead this example should be used as educational material on how to put together a simple snapshot-based fuzzer with coverage guidance in python.

## Overview
This fuzzer forks "target" as a child process with ptrace attached as a debugger. It leverages `nm`, `objdump` and `/proc/id/maps` to locate the `.text` section of "target", derive all necessary breakpoint positions in memory, locate the start and stop snapshot points and control the saving/loading of target memory. I made an effort to comment as much as I could so the python should serve as good documentation on how to build a snapshot-based fuzzer (@h0mbre_ blog [Fuzzing Like A Caveman 4](https://h0mbre.github.io/Fuzzing-Like-A-Caveman-4/) is also good supplemental material). When the fuzzer first executes it applies as many breakpoints as possible, it then continues execution to the startpoint deleting all breakpoints along the way. It then saves program state at the start point and starts the fuzzing operation. The fuzzing loop creates a fuzzing payload, writes the payload in target memory and continues execution until it hits the endpoint. At the endpoint the fuzzer reloads the program state back to the startpoint and creates a new mutation to test. For every test case that results in a new breakpoint hit, the fuzzer captures the mutation into its corpus pool, removes the break point and continues execution. The mutation in this example is extremely trivial, it is just a byte flip of 2 random payload bytes and good enough to find the crashes. The target example contains 2 unique crashes.

## Performance
10,000 - 20,000 Fuzz cases per second depending on your CPU. The fuzzer should find the 2 unique crashes within 10-60 seconds of fuzz time.

The goal of snapshot fuzzing is performance and determinism, While snapshot fuzzing does improve performance by quite an amount, this example is written in python and thus implementations in C or Rust should perform better.

## How to install and run (Ubuntu)
### Install
1) clone this repo and change directory into it
2) sudo apt update
3) sudo apt install python3 python3-pip build-essential
4) sudo pip3 install python-ptrace
### Run
1) make

