#!/usr/bin/env python3
"""Generate one interactive-video act from a JSON production config.

The engine keeps generation state in a manifest so image and video requests are
resumable. Production configs own story-specific prompts; this file owns the
Aigram image/video API contract and download/retry behavior.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path


IMAGE_API = "https://chat.aiwaves.tech/aigram/api/gen-image"
VIDEO_SUBMIT = "https://u545921-b746-8a491f44.westc.seetacloud.com:8443/video"
VIDEO_POLL = "https://u545921-b746-8a491f44.westc.seetacloud.com:8443/video_task"


def post(url: str, payload: dict, timeout: int = 900, origin: bool = False) -> dict:
    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
    if origin:
        headers.update({"Origin": "https://aigram.app", "Referer": "https://aigram.app/"})
    request = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST", headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read())


def generate_image(prompt: str, ref_url: str | None = None) -> str:
    for attempt, delay in enumerate((3, 8, 15), start=1):
        try:
            payload = {"prompt": prompt}
            if ref_url:
                payload["ref_url"] = ref_url
            result = post(IMAGE_API, payload, origin=True)
            if not result.get("url"):
                raise RuntimeError(result)
            return result["url"]
        except urllib.error.HTTPError as error:
            if error.code not in (429, 500, 502, 503, 504) or attempt == 3:
                raise
            time.sleep(delay)
    raise RuntimeError("image generation failed")


def download(url: str, destination: Path) -> None:
    last_error: Exception | None = None
    for delay in (2, 5, 10, 20, 30):
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(request, timeout=600) as response:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(response.read())
                return
        except urllib.error.HTTPError as error:
            last_error = error
            if error.code not in (424, 429, 500, 502, 503, 504):
                raise
            print(f"asset not ready (HTTP {error.code}); retry in {delay}s", flush=True)
            time.sleep(delay)
    raise last_error or RuntimeError(f"download failed: {url}")


def submit_and_wait(start_url: str, end_url: str, prompt: str, video_time: int) -> tuple[str, str]:
    submitted = post(
        VIDEO_SUBMIT,
        {"query": "", "params": {
            "image_url": start_url,
            "end_image_url": end_url,
            "prompt": prompt,
            "env": "prod",
            "target_image_ratio": "9x16",
            "video_time": video_time,
        }},
        timeout=300,
    )
    task_id = submitted.get("task_id") or submitted.get("data", {}).get("task_id")
    if not task_id:
        raise RuntimeError(submitted)
    deadline = time.time() + 1800
    while time.time() < deadline:
        time.sleep(15)
        try:
            result = post(VIDEO_POLL, {"query": "", "params": {"task_id": task_id}}, timeout=300)
        except urllib.error.HTTPError as error:
            if error.code == 429:
                print(f"task {task_id} poll throttled; continue", flush=True)
                continue
            raise
        status = result.get("status") or result.get("data", {}).get("status")
        print(f"task {task_id} status={status}", flush=True)
        if status == "success":
            url = result.get("url") or result.get("data", {}).get("url")
            if not url:
                raise RuntimeError(result)
            return task_id, url
        if status == "failed":
            raise RuntimeError(result)
    raise TimeoutError(task_id)


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    parser.add_argument("--choice-only", action="store_true")
    parser.add_argument("--start-only", action="store_true")
    parser.add_argument("--frames-only", action="store_true")
    parser.add_argument("--restart-choice", action="store_true")
    parser.add_argument("--restart-start", action="store_true")
    parser.add_argument("--restart-outcomes", action="store_true")
    parser.add_argument("--restart-outcome", action="append", default=[])
    parser.add_argument("--repair-outcome", action="append", default=[])
    parser.add_argument("--restart-videos", action="store_true")
    parser.add_argument("--restart-setup-video", action="store_true")
    args = parser.parse_args()

    config = json.loads(args.config.read_text())
    root = args.config.resolve().parents[1]
    output = root / config["output_dir"]
    manifest_path = root / config["manifest"]
    output.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}

    if args.restart_start:
        manifest = {}
    elif args.restart_choice:
        manifest = {}
    manifest.setdefault("act_id", config["act_id"])
    if not manifest.get("setup_start_url"):
        if config.get("setup_start_url"):
            manifest["setup_start_url"] = config["setup_start_url"]
            manifest["setup_start_prompt"] = config.get("setup_start_prompt", "approved prior-act endpoint")
        else:
            print("generating setup start frame", flush=True)
            setup_ref_url = config.get("setup_start_ref_url")
            manifest["setup_start_url"] = generate_image(config["setup_start_image_prompt"], setup_ref_url)
            manifest["setup_start_prompt"] = config["setup_start_image_prompt"]
            if setup_ref_url:
                manifest["setup_start_ref_url"] = setup_ref_url
            save(manifest_path, manifest)
    download(manifest["setup_start_url"], output / "setup_start.webp")
    if args.start_only:
        print(json.dumps(manifest, ensure_ascii=False), flush=True)
        return

    if not manifest.get("choice_url"):
        print("generating choice frame", flush=True)
        manifest["choice_url"] = generate_image(config["choice_prompt"], manifest["setup_start_url"])
        manifest["choice_prompt"] = config["choice_prompt"]
        save(manifest_path, manifest)
    download(manifest["choice_url"], output / "choice.webp")
    if args.choice_only:
        print(json.dumps(manifest, ensure_ascii=False), flush=True)
        return

    if args.restart_outcomes:
        manifest.pop("outcomes", None)
    outcomes = manifest.setdefault("outcomes", {})
    for outcome_id in args.restart_outcome:
        outcomes.pop(outcome_id, None)
    config_by_id = {outcome["id"]: outcome for outcome in config["outcomes"]}
    for outcome_id in args.repair_outcome:
        entry = outcomes[outcome_id]
        outcome = config_by_id[outcome_id]
        print(f"repairing {outcome_id} end frame", flush=True)
        repaired_from = entry["end_url"]
        entry["end_url"] = generate_image(outcome["repair_prompt"], repaired_from)
        entry["end_prompt"] = outcome["repair_prompt"]
        entry["repaired_from"] = repaired_from
        for key in ("task_id", "video_url", "video_prompt", "video_time"):
            entry.pop(key, None)
        save(manifest_path, manifest)
    for outcome in config["outcomes"]:
        entry = outcomes.setdefault(outcome["id"], {})
        if not entry.get("end_url"):
            print(f"generating {outcome['id']} end frame", flush=True)
            entry["end_url"] = generate_image(outcome["end_prompt"], manifest["choice_url"])
            entry["end_prompt"] = outcome["end_prompt"]
            save(manifest_path, manifest)
        download(entry["end_url"], output / f"{outcome['id']}_end.webp")
    if args.frames_only:
        print(json.dumps(manifest, ensure_ascii=False), flush=True)
        return

    if args.restart_videos:
        manifest.pop("setup", None)
        for entry in outcomes.values():
            for key in ("task_id", "video_url", "video_prompt", "video_time"):
                entry.pop(key, None)
        save(manifest_path, manifest)

    if args.restart_setup_video:
        manifest.pop("setup", None)
        save(manifest_path, manifest)

    setup = manifest.setdefault("setup", {})
    if not setup.get("video_url"):
        print("submitting setup video", flush=True)
        video_time = int(config.get("setup_video_time", 5))
        task_id, url = submit_and_wait(manifest["setup_start_url"], manifest["choice_url"], config["setup_video_prompt"], video_time)
        setup.update({"task_id": task_id, "video_url": url, "video_prompt": config["setup_video_prompt"], "video_time": video_time})
        save(manifest_path, manifest)
    download(setup["video_url"], output / "setup.mp4")

    outcome_config = config_by_id
    for outcome_id, entry in outcomes.items():
        if not entry.get("video_url"):
            outcome = outcome_config[outcome_id]
            video_time = int(outcome.get("video_time", 5))
            print(f"submitting {outcome_id} result video ({video_time}s)", flush=True)
            task_id, url = submit_and_wait(manifest["choice_url"], entry["end_url"], outcome["video_prompt"], video_time)
            entry.update({"task_id": task_id, "video_url": url, "video_prompt": outcome["video_prompt"], "video_time": video_time})
            save(manifest_path, manifest)
        download(entry["video_url"], output / f"{outcome_id}.mp4")

    print(json.dumps(manifest, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
