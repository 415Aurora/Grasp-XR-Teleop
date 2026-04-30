# Task Mapping

## Primary Task Line

| Research Task | Scenario | Existing Simulation Task | Goal |
| --- | --- | --- | --- |
| A1 | Fastener grasp-and-transfer | `e1` | Pick the bolt and place it into the target container |
| A2 | Hand tool grasp-and-transfer | `e2_wrench` | Pick the wrench and place it inside a circular target zone |
| B1 | Tool/workpiece alignment | `e3` | Align the tool and target part into an executable pose |
| C1 | Tool-assisted simplified operation | `e4` | Complete a simplified operation after grasping the tool |

## Expansion Asset Priority

1. `wrench`
2. `cordless_drill`
3. `hammer`

Use the expansion assets only after the primary task line is stable enough to support repeatable experiments.

## Extension Task Line

| Research Extension | Scenario | Goal |
| --- | --- | --- |
| A2-wrench-extension | `e2_wrench` | Validate the imported real wrench mesh and the circular target-zone transfer task |
