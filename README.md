# Health Simplified

Health Simplified is a terminal-based calorie tracking application that helps users log meals, set calorie goals, and plan weekly meals easily via a CLI interface.

## Features

- Quickly log meals with calorie counts
- Set daily and weekly calorie goals
- View daily summary reports
- Generate weekly meal prep schedules

## Installation

You can install the package locally using:
pip install dist/health_simplified-0.1.0-py3-none-any.whl

## Usage
Run the CLI app from your terminal:
health_simplified --help

User Management

myapp user create --name <name>
myapp user list


Food Entries

myapp entry add --user <name> --food <food> --calories <int> --date <YYYY-MM-DD>
myapp entry list [--user <name>] [--date <date>]
myapp entry update --id <int> [fields...]
myapp entry delete --id <int>


Goals
myapp goal set --user <name> --daily <int> --weekly <int>
myapp goal list --user <name>

Meal Planning
myapp plan-meal --user <name> --week <int>
myapp plan-meal update --id <int> [fields...]


## Run tests
pytest