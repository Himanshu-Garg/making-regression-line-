#!/bin/bash

awk -F';' '{print $3,";",$8}' conferences_before.csv >> conferences_after.txt
