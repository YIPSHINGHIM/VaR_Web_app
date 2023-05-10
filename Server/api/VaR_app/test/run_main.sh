#!/bin/bash

while true; do
  python3 temp.py
  exit_status=$?
  if [ $exit_status -eq 0 ]; then
    break
  fi
  echo "Error encountered (exit status: $exit_status). Restarting script..."
  sleep 1
done
