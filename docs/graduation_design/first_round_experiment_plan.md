# First-Round Experiment Plan

Recommended first-round scope:

- participant count: `1`
- participant id: `P01`
- thesis main task: `A2`
- supporting tasks: `A1`, `B1`, `C1`
- trials per task: `1`

Generate the full command sheet with:

```bash
python3 -m graduation_design.experiment_plan --participant-ids P01 --task-ids A1 A2 B1 C1 --trials-per-task 1
```

Recommended execution order:

1. `A1` bolt grasp and transfer
2. `A2` wrench grasp and transfer into a `0.12 m` radius circular target zone
3. `B1` tool/workpiece alignment
4. `C1` tool-assisted simplified operation

Reason for this order:

- `A1` is the easiest warm-up task
- `A2` is the thesis core task and adds real tool-shape variability
- `B1` adds fine alignment difficulty
- `C1` is the hardest integrated task

After finishing the first round:

1. Fill the completed rows into `experiment_log_template.csv`
2. Save success and failure screenshots
3. Run `python3 -m graduation_design.experiment_summary <csv>`
4. Review which task fails most often before inviting more participants
