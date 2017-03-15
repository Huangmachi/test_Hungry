#!/bin/bash
# Copyright (C) 2016 Huang MaChi at Chongqing University
# of Posts and Telecommunications, China.

out_dir="./results"
rm -f -r ./results
mkdir -p $out_dir

# Run the test.
sudo python hungry.py

# Plot results.
sudo python ./plot_results.py
