# Health Simplified
Health Simplified is a terminal-based calorie tracking application that helps users log meals, set calorie goals, and plan weekly meals easily via a CLI interface.

# Features
- Quickly log meals with calorie counts
- Set daily and weekly calorie goals
- View daily summary reports
- Generate weekly meal prep schedules

# Installation
You can install the package locally using:
pip install dist/health_simplified-0.1.0-py3-none-any.whl

# Usage
Run the CLI app from your terminal:
- health_simplified --help
# User Management
- myapp.main user create --name <name>
- myapp.main user list
# Food Entries
- myapp.main entry add --user <name> --food <food> --calories <int> --date <YYYY-MM-DD>
- myapp.main entry list [--user <name>] [--entry-date <date>]
- myapp.main entry update --id <int> [fields...]
- myapp.main entry delete --id <int>
## Goals
- myapp.main goal set --user <name> --daily <int> --weekly <int>
- myapp.main goal list --user <name>
## Meal Planning
- myapp.main plan-meal create --user <name> --week 
- myapp.main plan-meal update --id <int> 
- myapp.main plan-meal list --user 
## Reporting
- myapp.main report daily --user <name> --date

