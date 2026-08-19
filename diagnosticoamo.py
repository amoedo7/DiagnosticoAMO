#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

SCHEMA = "desarrollamo.diagnostico.v1"
KNOWN = {
    "desarrollamo.midispositivo.v1": "device",
    "desarrollamo.mired.v1": "network",
    "desarrollamo.misistema.v1": "system",
}


def load_reports(paths: list[str]) -> tuple[dict, list[dict]]:
    reports = {}
    unknown = []
    for raw_path in paths:
        path = Path(raw_path)
        data = json.loads(path.read_text(encoding="utf-8"))
        schema = data.get("schema")
        role = KNOWN.get(schema)
        if role:
            reports[role] = data
        else:
            unknown.append({"file": str(path), "schema": schema})
    return reports, unknown


def demo_reports() -> dict:
    return {
        "device": {
            "schema": "desarrollamo.midispositivo.v1",
            "device": {"os": "Linux", "architecture": "aarch64", "logical_cores": 8, "memory_total_bytes": 8_000_000_000, "disk": {"free_bytes": 50_000_000_000}},
            "network": {"local_ip": "192.168.1.20"},
        },
        "network": {
            "schema": "desarrollamo.mired.v1",
            "summary": {"score": 100},
            "checks": {"dns": {"ok": True}, "tcp": {"ok": True}, "https": {"ok": True}},
        },
        "system": {
            "schema": "desarrollamo.misistema.v1",
            "runtimes": {"python": {"available": True}, "node": {"available": True}, "git": {"available": True}, "docker": {"available": False}},
            "capabilities": {"python_automation": True, "javascript_tooling": True, "git_workflows": True, "container_runtime": False},
        },
    }


def aggregate(reports: dict, unknown: list[dict]) -> dict:
    device = reports.get("device", {})
    network = reports.get("network", {})
    system = reports.get("system", {})

    dev = device.get("device", {})
    runtimes = system.get("runtimes", {})
    capabilities = system.get("capabilities", {})
    network_score = network.get("summary", {}).get("score")

    completeness = round(len(reports) / 3 * 25)
    device_fields = [dev.get("os"), dev.get("architecture"), dev.get("logical_cores"), dev.get("memory_total_bytes"), (dev.get("disk") or {}).get("free_bytes")]
    device_points = round(sum(v is not None for v in device_fields) / len(device_fields) * 25) if device else 0
    network_points = round((network_score or 0) / 100 * 25) if network else 0
    cap_values = [bool(v) for v in capabilities.values()]
    system_points = round(sum(cap_values) / max(len(cap_values), 1) * 25) if system else 0
    total = min(100, completeness + device_points + network_points + system_points)

    recommendations = []
    if "device" not in reports:
        recommendations.append("Generar reporte MiDispositivo.")
    if "network" not in reports:
        recommendations.append("Generar reporte MiRed.")
    if "system" not in reports:
        recommendations.append("Generar reporte MiSistema.")
    if system:
        if not runtimes.get("python", {}).get("available"):
            recommendations.append("Python no fue detectado; algunas herramientas multiplataforma pueden requerirlo.")
        if not runtimes.get("git", {}).get("available"):
            recommendations.append("Git no fue detectado; instalarlo facilita flujos de código y actualización.")
        if not runtimes.get("docker", {}).get("available"):
            recommendations.append("Docker no fue detectado. Sólo es relevante si el proyecto necesita contenedores.")
    if network and network_score is not None and network_score < 100:
        recommendations.append("Revisar los checks fallidos de MiRed antes de depender de servicios externos.")

    return {
        "schema": SCHEMA,
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "privacy": {"external_requests_performed": False, "input_reports_modified": False},
        "inputs": {"received": sorted(reports.keys()), "unknown": unknown},
        "overview": {
            "os": dev.get("os"),
            "architecture": dev.get("architecture"),
            "logical_cores": dev.get("logical_cores"),
            "memory_total_bytes": dev.get("memory_total_bytes"),
            "network_score": network_score,
            "capabilities": capabilities,
        },
        "score": {
            "total": total,
            "breakdown": {
                "report_completeness": completeness,
                "device_information": device_points,
                "network_health": network_points,
                "runtime_capabilities": system_points,
            },
            "max": 100,
            "method": "transparent heuristic, not a certification",
        },
        "recommendations": recommendations,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="DiagnosticoAMO: agrega reportes MiDispositivo, MiRed y MiSistema")
    p.add_argument("reports", nargs="*")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--output")
    p.add_argument("--compact", action="store_true")
    args = p.parse_args()
    if args.demo:
        reports, unknown = demo_reports(), []
    else:
        if not args.reports:
            p.error("indicá al menos un reporte JSON o usá --demo")
        reports, unknown = load_reports(args.reports)
    result = aggregate(reports, unknown)
    text = json.dumps(result, ensure_ascii=False, indent=None if args.compact else 2)
    print(text)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
