# Graduation Design Experiment Runbook

## Purpose

This runbook standardizes how to execute one formal trial for the graduation design tasks `A1`, `A2`, `B1`, and `C1`.

The recommended thesis mainline is `A2`, defined as wrench grasp-and-transfer into a circular target zone.

## One-Trial Workflow

1. Generate the standardized checklist and commands.
2. Start the simulation scene for the target task.
3. Start the XR teleoperation recording process.
4. Execute the task once.
5. Save the episode.
6. For `A2`, confirm whether the wrench finally rests inside the `0.12 m` radius circular target zone.
7. Fill the CSV row with the observed metrics.
8. Save one success screenshot and one failure screenshot if possible.

## Command Generator

```bash
python3 -m graduation_design.experiment_session A1 --participant-id P01 --trial-index 1
python3 -m graduation_design.experiment_session B1 --participant-id P02 --trial-index 3
python3 teleop/utils/formal_trial.py prepare A2 --participant-id P01 --trial-index 1
```

The generator prints:

- the standardized task and scenario identifiers
- the simulation command
- the recording command
- a CSV row skeleton that matches `experiment_log_template.csv`

The `teleop/utils/formal_trial.py` helper additionally:

- creates `teleop/utils/data/graduation_design/<trial_name>/`
- initializes or refreshes the matching CSV row
- summarizes recorded `episode_XXXX` directories
- writes back the final trial metrics after manual judgement

## Recommended Directory Convention

- episode recordings: `./teleop/utils/data/graduation_design`
- experiment table: `docs/graduation_design/experiment_log_template.csv`
- result summary input: a copy of the completed CSV file
- screenshots: `docs/graduation_design/screenshots/<task_id>/`

## Metric Filling Rules

- `success`: `1` for success, `0` for failure
- `target_zone_shape`: use `circle` for `A2`, otherwise keep empty unless another target zone is introduced
- `target_zone_radius_m`: use `0.12` for `A2`, otherwise keep empty
- `duration_s`: total trial duration in seconds
- `regrasp_count`: number of obvious re-grasp attempts
- `micro_adjust_count`: number of fine alignment adjustments
- `alignment_error_mm`: only fill for alignment-sensitive tasks, otherwise keep empty
- `collision_count`: count obvious scene collisions
- `difficulty_score`: subjective 1-5 score
- `fatigue_score`: subjective 1-5 score
- `control_score`: subjective 1-5 score, higher means easier control

## A2 Core-Task Definition

- task name: wrench grasp-and-transfer to circular target zone
- simulation scenario: `e2_wrench`
- target zone shape: circular
- target zone radius: `0.12 m`
- success rule: release the wrench and let it settle inside the circular target zone without falling from the table

## After Data Collection

Summarize recorded episodes for one formal trial:

```bash
python3 teleop/utils/formal_trial.py summarize-episodes A2 --participant-id P01 --trial-index 1
```

Update the CSV row after the operator finishes the trial:

```bash
python3 teleop/utils/formal_trial.py update-record A2 \
  --participant-id P01 \
  --trial-index 1 \
  --success success \
  --regrasp-count 1 \
  --micro-adjust-count 2 \
  --collision-count 0 \
  --difficulty-score 3 \
  --fatigue-score 2 \
  --control-score 4 \
  --notes "Stable grasp; final release stayed inside the target zone."
```

Use the summary tool on the completed CSV file:

```bash
python3 -m graduation_design.experiment_summary <your_csv_file>
```

Copy the generated Markdown table into the thesis result draft, then match it with screenshots and case analysis.
