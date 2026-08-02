#!/usr/bin/env python3
"""Executa integração headless por cenários e grava CSV e resumos JSON."""

import argparse
import csv
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sim import Simulator  # noqa: E402


CSV_FIELDS = (
    "time_s", "transport", "rpm_setpoint", "rpm", "encoder_rpm_raw",
    "encoder_rpm_filtered", "digital_tach_enabled", "control_fallback",
    "command_nominal", "command_requested", "command_applied", "err",
    "rms_error_percent", "actuator_saturated", "saturated_time_s",
    "wow_disturbance", "flutter_disturbance", "encoder_dropout",
)


def apply_event(simulator: Simulator, event: dict):
    if "transport" in event:
        simulator.set_transport(event["transport"])
    for name, value in event.get("state", {}).items():
        setattr(simulator.s, name, value)
    for name, value in event.get("controller", {}).items():
        setattr(simulator.controller, name, value)
    for component_name, parameters in event.get("disturbances", {}).items():
        component = getattr(simulator.faults.disturbances, component_name)
        for name, value in parameters.items():
            getattr(component, f"set_{name}")(value)


def sample_state(time_s: float, simulator: Simulator) -> dict:
    state = asdict(simulator.s)
    return {"time_s": round(time_s, 6), **{key: state[key] for key in CSV_FIELDS[1:]}}


def nested_value(data: dict, path: str):
    value = data
    for part in path.split("."):
        value = value[part]
    return value


def evaluate(summary: dict, expectations: list[dict]) -> list[dict]:
    checks = []
    for expectation in expectations:
        actual = nested_value(summary, expectation["path"])
        passed = True
        if "equals" in expectation:
            passed = actual == expectation["equals"]
        if "min" in expectation:
            passed = passed and actual is not None and actual >= expectation["min"]
        if "max" in expectation:
            passed = passed and actual is not None and actual <= expectation["max"]
        checks.append({**expectation, "actual": actual, "passed": passed})
    return checks


def run_scenario(path: Path, output_dir: Path) -> dict:
    scenario = json.loads(path.read_text(encoding="utf-8"))
    simulator = Simulator()
    step_s = scenario.get("step_seconds", 0.001)
    sample_s = scenario.get("sample_seconds", 0.010)
    duration_s = scenario["duration_seconds"]
    events = sorted(scenario.get("events", []), key=lambda event: event["at"])
    event_index = 0
    next_sample = 0.0
    time_s = 0.0
    rows = []

    while time_s < duration_s:
        while event_index < len(events) and events[event_index]["at"] <= time_s + 1e-12:
            apply_event(simulator, events[event_index])
            event_index += 1
        simulator.step(step_s)
        time_s += step_s
        if time_s + 1e-12 >= next_sample:
            rows.append(sample_state(time_s, simulator))
            next_sample += sample_s

    final = rows[-1]
    command_jumps = [
        abs(current["command_applied"] - previous["command_applied"])
        for previous, current in zip(rows, rows[1:])
    ]
    summary = {
        "scenario": scenario["name"],
        "duration_seconds": duration_s,
        "sample_count": len(rows),
        "final": final,
        "observed": {
            "minimum_rpm": min(row["rpm"] for row in rows),
            "maximum_rpm": max(row["rpm"] for row in rows),
            "maximum_command_jump": max(command_jumps, default=0.0),
            "saturated_time_seconds": final["saturated_time_s"],
        },
    }
    checks = evaluate(summary, scenario.get("expect", []))
    summary["checks"] = checks
    summary["passed"] = all(check["passed"] for check in checks)

    output_dir.mkdir(parents=True, exist_ok=True)
    stem = scenario["name"]
    with (output_dir / f"{stem}.csv").open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / f"{stem}-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenarios", type=Path, default=ROOT / "tests/scenarios")
    parser.add_argument("--output", type=Path, default=ROOT / "test-results")
    parser.add_argument("--scenario", help="Executa somente o nome informado")
    args = parser.parse_args()

    paths = sorted(args.scenarios.glob("*.json"))
    if args.scenario:
        paths = [path for path in paths if path.stem == args.scenario]
    if not paths:
        parser.error("nenhum cenário encontrado")

    summaries = [run_scenario(path, args.output) for path in paths]
    for summary in summaries:
        status = "PASS" if summary["passed"] else "FAIL"
        print(f"{status} {summary['scenario']}")
        for check in summary["checks"]:
            if not check["passed"]:
                print(f"  {check['path']}: obtido {check['actual']}, esperado {check}")
    return 0 if all(summary["passed"] for summary in summaries) else 1


if __name__ == "__main__":
    raise SystemExit(main())
