import argparse
import shlex


TASK_DEFINITIONS = {
    "A1": {
        "scenario_id": "e1",
        "task_name": "bolt-grasp-transfer",
        "task_goal": "Grasp the bolt and place it into the target container.",
        "task_desc": "Single-tool grasp-and-transfer task using the bolt scene.",
        "task_steps": "step1: approach the bolt; step2: grasp the bolt; step3: lift and transfer; step4: place into container;",
    },
    "A2": {
        "scenario_id": "e2_wrench",
        "task_name": "wrench-grasp-transfer",
        "task_goal": "Grasp the wrench and place it inside the 0.12 m radius circular target zone.",
        "task_desc": "Single-tool grasp-and-transfer task using the wrench scene and a 0.12 m radius circular target zone.",
        "task_steps": "step1: approach the wrench; step2: grasp the wrench; step3: lift and transfer; step4: release inside the circular target zone;",
    },
    "B1": {
        "scenario_id": "e3",
        "task_name": "tool-alignment",
        "task_goal": "Align the tool and workpiece into an executable pose.",
        "task_desc": "Fine alignment task focusing on tool-workpiece relative pose control.",
        "task_steps": "step1: grasp the tool or part; step2: approach target pose; step3: micro-adjust alignment; step4: hold aligned pose;",
    },
    "C1": {
        "scenario_id": "e4",
        "task_name": "tool-assisted-operation",
        "task_goal": "Complete a simplified construction-style operation with the grasped tool.",
        "task_desc": "Tool-assisted task that evaluates grasp stability and post-grasp manipulation.",
        "task_steps": "step1: grasp the tool; step2: move to work area; step3: align for operation; step4: execute simplified action;",
    },
}


def get_task_definition(task_id):
    try:
        return TASK_DEFINITIONS[task_id]
    except KeyError as exc:
        raise ValueError(f"Unsupported task_id: {task_id}") from exc


def make_trial_name(task_id, participant_id, trial_index):
    return f"{task_id}_{participant_id}_T{int(trial_index):02d}"


def build_sim_command(task_id):
    task = get_task_definition(task_id)
    return (
        f"python sim_main.py --device cpu --enable_cameras --task {task['scenario_id']} "
        "--enable_dex3_dds --robot_type g129"
    )


def build_recording_command(task_id, participant_id, trial_index, task_dir, img_server_ip):
    task = get_task_definition(task_id)
    trial_name = make_trial_name(task_id, participant_id, trial_index)
    parts = [
        "python teleop_hand_and_arm.py",
        "--input-mode=hand",
        "--arm=G1_29",
        "--ee=dex3",
        "--sim",
        "--record",
        f"--img-server-ip {img_server_ip}",
        f"--task-dir {shlex.quote(task_dir)}",
        f"--task-name {trial_name}",
        f"--task-goal {shlex.quote(task['task_goal'])}",
        f"--task-desc {shlex.quote(task['task_desc'])}",
        f"--task-steps {shlex.quote(task['task_steps'])}",
    ]
    return " ".join(parts)


def render_task_sheet(task_id, participant_id, trial_index, task_dir, img_server_ip):
    task = get_task_definition(task_id)
    trial_name = make_trial_name(task_id, participant_id, trial_index)
    return "\n".join(
        [
            f"Task ID: {task_id}",
            f"Scenario ID: {task['scenario_id']}",
            f"Participant ID: {participant_id}",
            f"Trial Name: {trial_name}",
            "",
            "Simulation Command:",
            build_sim_command(task_id),
            "",
            "Recording Command:",
            build_recording_command(task_id, participant_id, trial_index, task_dir, img_server_ip),
        ]
    )


def main():
    parser = argparse.ArgumentParser(description="Generate standardized commands for graduation design experiments.")
    parser.add_argument("task_id", choices=sorted(TASK_DEFINITIONS.keys()))
    parser.add_argument("--participant-id", default="P01")
    parser.add_argument("--trial-index", type=int, default=1)
    parser.add_argument("--task-dir", default="./teleop/utils/data/graduation_design")
    parser.add_argument("--img-server-ip", default="100.79.86.139")
    args = parser.parse_args()

    print(
        render_task_sheet(
            args.task_id,
            participant_id=args.participant_id,
            trial_index=args.trial_index,
            task_dir=args.task_dir,
            img_server_ip=args.img_server_ip,
        )
    )


if __name__ == "__main__":
    main()
