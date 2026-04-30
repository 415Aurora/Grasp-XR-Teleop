TASK_DEFINITIONS = {
    "A1": {
        "scenario_id": "e1",
        "task_name": "bolt-grasp-transfer",
        "task_goal": "Grasp the bolt and place it into the target container.",
        "task_desc": "Single-tool grasp-and-transfer task using the bolt scene.",
        "task_steps": "step1: approach the bolt; step2: grasp the bolt; step3: lift and transfer; step4: place into container;",
        "target_zone_shape": "",
        "target_zone_radius_m": "",
    },
    "A2": {
        "scenario_id": "e2_wrench",
        "task_name": "wrench-grasp-transfer",
        "task_goal": "Grasp the wrench and place it inside the 0.12 m radius circular target zone.",
        "task_desc": "Single-tool grasp-and-transfer task using the wrench scene and a 0.12 m radius circular target zone.",
        "task_steps": "step1: approach the wrench; step2: grasp the wrench; step3: lift and transfer; step4: release inside the circular target zone;",
        "target_zone_shape": "circle",
        "target_zone_radius_m": "0.12",
    },
    "B1": {
        "scenario_id": "e3",
        "task_name": "tool-alignment",
        "task_goal": "Align the tool and workpiece into an executable pose.",
        "task_desc": "Fine alignment task focusing on tool-workpiece relative pose control.",
        "task_steps": "step1: grasp the tool or part; step2: approach target pose; step3: micro-adjust alignment; step4: hold aligned pose;",
        "target_zone_shape": "",
        "target_zone_radius_m": "",
    },
    "C1": {
        "scenario_id": "e4",
        "task_name": "tool-assisted-operation",
        "task_goal": "Complete a simplified construction-style operation with the grasped tool.",
        "task_desc": "Tool-assisted task that evaluates grasp stability and post-grasp manipulation.",
        "task_steps": "step1: grasp the tool; step2: move to work area; step3: align for operation; step4: execute simplified action;",
        "target_zone_shape": "",
        "target_zone_radius_m": "",
    },
}


def get_task_definition(task_id):
    try:
        return TASK_DEFINITIONS[task_id]
    except KeyError as exc:
        raise ValueError(f"Unsupported task_id: {task_id}") from exc


def get_target_zone_fields(task_id):
    task = get_task_definition(task_id)
    return {
        "target_zone_shape": task["target_zone_shape"],
        "target_zone_radius_m": task["target_zone_radius_m"],
    }
