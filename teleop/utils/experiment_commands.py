import shlex

from teleop.utils.experiment_tasks import get_task_definition


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
