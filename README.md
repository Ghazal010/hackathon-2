# Hackathon II - Todo App

This project is part of Hackathon II: "The Evolution of Todo – Mastering Spec-Driven Development & Cloud Native AI".

## Systematic Documentation Approach

This project implements a systematic documentation approach for tracking all phases of the hackathon. Each phase follows a consistent 6-document system:

1. **Constitution** - Project identity and constraints
2. **Specification** - Technical requirements and user stories
3. **Plan** - Implementation strategy and timeline
4. **Tasks** - Work breakdown and status tracking
5. **Implementation** - Technical details and architecture decisions
6. **Overview** - Phase summary and handoff documentation

## Phase I: In-Memory Python Console App

A command-line todo application that stores tasks in memory, built using spec-driven development with Claude Code and Spec-Kit Plus.

## Features

- Add new tasks
- View all tasks
- Update existing tasks
- Delete tasks
- Mark tasks as complete/incomplete

## Tech Stack

- Python 3.13+
- UV package manager
- Claude Code
- Spec-Kit Plus

## Systematic Documentation Structure

Complete documentation for Phase I is available in:
- `/specs/phases/phase1/` - All Phase I documentation
- `/specs/phases/index.md` - Master index of all phases
- `/SYSTEMATIC_APPROACH.md` - Explanation of the systematic approach

## Setup Instructions

1. Install UV package manager:
   ```bash
   pip install uv
   ```

2. Clone this repository

3. Navigate to the project directory

4. Install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   python src/main.py
   ```

## Spec-Driven Development

This project follows spec-driven development principles. All features are specified in the `/specs` directory before implementation.

## Project Structure

- `/specs` - Specification files with systematic documentation
- `/specs/phases/` - Phase-by-phase systematic documentation
- `/src` - Python source code
- `/test_app.py` - Test script
- `CLAUDE.md` - Claude Code instructions
- `README.md` - Project documentation