#!/usr/bin/env python3
"""
Square-Tooth Generator Architecture Pipeline Gate.
Scans the hardware To-Do list to assert 100% check-off compliance before factory release.
"""

import sys
import os
import re

class TodoComplianceChecker:
    def __init__(self, todo_filepath="docs/chip_team_todo.md"):
        self.todo_path = todo_filepath
        
        # Look one directory up if called from inside the tools folder
        if not os.path.exists(self.todo_path) and os.path.exists(os.path.join("..", self.todo_path)):
            self.todo_path = os.path.join("..", self.todo_path)

    def verify_hardware_readiness(self):
        """Parses the markdown todo checkboxes to locate uncompleted silicon and ATX milestones."""
        print(f"=== Quality Gate Audit: Checking Hardware Compliance ===")
        
        if not os.path.exists(self.todo_path):
            print(f"[CRITICAL ERROR]: Chip team task file could not be resolved at path: {self.todo_path}")
            return False

        with open(self.todo_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        total_tasks = 0
        incomplete_tasks = []
        current_milestone = "General Tasks"

        # Regex patterns to find Markdown checklist brackets
        checked_pattern = re.compile(r"^\s*-\s*\[[xX]\]\s*(.*)")
        unchecked_pattern = re.compile(r"^\s*-\s*\[\s*\]\s*(.*)")
        header_pattern = re.compile(r"^#+\s*(.*)")

        for line_num, line in enumerate(lines, start=1):
            # Track active structural milestones for precise error logging
            header_match = header_pattern.match(line.strip())
            if header_match:
                current_milestone = header_match.group(1)
                continue

            # Evaluate checkbox markers
            if unchecked_pattern.match(line.strip()):
                total_tasks += 1
                task_text = unchecked_pattern.match(line.strip()).group(1)
                incomplete_tasks.append((line_num, current_milestone, task_text))
            elif checked_pattern.match(line.strip()):
                total_tasks += 1

        print(f"[AUDIT]: Discovered a total of {total_tasks} hardware and silicon validation metrics.")
        
        if incomplete_tasks:
            print(f"\n{'-'*60}\n[RELEASE REJECTED]: Unfinished chip tasks detected. Deployment halted!\n{'-'*60}")
            for line_no, milestone, task in incomplete_tasks:
                print(f"  ❌ Line {line_no} Under [{milestone}]:")
                print(f"     Task: {task}")
            print(f"\n[REASON]: All ATX mounts, reference rails, and guard rings must pass physical validation before factory sign-off.")
            return False

        print(f"[PASSED]: 100% Hardware compliance verified ({total_tasks}/{total_tasks} items checked).")
        return True

if __name__ == "__main__":
    checker = TodoComplianceChecker()
    compliance_passed = checker.verify_hardware_readiness()
    
    if not compliance_passed:
        sys.exit(3) # Explicit exit code 3 signals hardware-block to pipeline handlers
    sys.exit(0)
