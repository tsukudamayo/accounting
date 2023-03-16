#!/bin/bash

mkdir -p /data/balance/income
mkdir -p /data/balance/expenses
poetry config virtualenvs.create false
poetry install --with dev
