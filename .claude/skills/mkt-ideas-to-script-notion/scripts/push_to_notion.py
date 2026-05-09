#!/usr/bin/env python3
"""Push generated short-video scripts to the Notion short-video script DB.

Reads `NOTION_API_KEY` and `NOTION_DATABASE_SHORT_VIDEO_SCRIPT_ID` from .env
(walks upward from cwd to find the nearest .env).

Two modes:
  --fetch-schema              Print the target DB's properties (name + type) and exit.
  --input <scripts.json>      Create one Notion page per script.

Input JSON schema (array):
[
  {
    "title": "Claude Code 2.5 tự fix bug trong 30 giây",
    "structure": "Before-After",          # Before-After | Three Acts | Action
    "script_body": "[HOOK]\\n...\\n[REF: https://...]\\n...",
    "references": [
      {"url": "https://youtu.be/abc", "note": "demo clip"},
      {"url": "https://i.imgur.com/x.png", "note": "screenshot cũ"}
    ],
    "duration_sec": 60,                    # optional
    "word_count": 180,                     # optional
    "status": "Draft"                      # optional — otherwise skipped
  },
  ...
]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path
from typing import Any

import requests

NOTION_VERSION = "2022-06-28"
API = "https://api.notion.com/v1"


def load_env() -> None:
    """Walk upward from cwd to find .env, then populate os.environ."""
    cwd = Path.cwd().resolve()
    for directory in [cwd, *cwd.parents]:
        env_file = directory / ".env"
        if env_file.is_file():
            for raw in env_file.read_text().splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                # Last-wins (matches `source .env` behavior) — overrides any earlier duplicate
                os.environ[k.strip()] = v.strip().strip('"').strip("'")
            return


def headers() -> dict[str, str]:
    token = os.environ.get("NOTION_API_KEY")
    if not token:
        sys.exit("ERROR: NOTION_API_KEY not set in .env")
    return {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def db_id() -> str:
    v = os.environ.get("NOTION_DATABASE_SHORT_VIDEO_SCRIPT_ID")
    if not v:
        sys.exit(
            "ERROR: NOTION_DATABASE_SHORT_VIDEO_SCRIPT_ID not set in .env\n"
            "Add: NOTION_DATABASE_SHORT_VIDEO_SCRIPT_ID=c683a4e9-5263-4536-be96-3054944bbdf3"
        )
    return v


def fetch_schema() -> dict[str, dict[str, Any]]:
    r = requests.get(f"{API}/databases/{db_id()}", headers=headers(), timeout=30)
    if r.status_code != 200:
        sys.exit(f"ERROR {r.status_code}: {r.text}")
    return r.json().get("properties", {})


def print_schema(schema: dict[str, dict[str, Any]]) -> None:
    print(f"Database: {db_id()}")
    print(f"Properties ({len(schema)}):")
    for name, meta in schema.items():
        ptype = meta.get("type", "?")
        extra = ""
        if ptype == "select":
            opts = [o.get("name") for o in meta.get("select", {}).get("options", [])]
            extra = f"  options={opts}"
        elif ptype == "status":
            opts = [o.get("name") for o in meta.get("status", {}).get("options", [])]
            extra = f"  options={opts}"
        print(f"  - {name!r:<30} type={ptype}{extra}")


def find_prop(schema: dict[str, dict[str, Any]], *candidates: str) -> tuple[str, str] | None:
    """Return (property_name, property_type) for the first candidate that exists (case-insensitive)."""
    lower_map = {k.lower(): k for k in schema.keys()}
    for cand in candidates:
        key = lower_map.get(cand.lower())
        if key:
            return key, schema[key]["type"]
    return None


def rt(text: str) -> list[dict[str, Any]]:
    """Convert plain text into Notion rich_text blocks, chunked to <2000 chars each."""
    CHUNK = 1900
    out: list[dict[str, Any]] = []
    if not text:
        return out
    for i in range(0, len(text), CHUNK):
        out.append({"type": "text", "text": {"content": text[i : i + CHUNK]}})
    return out


def build_properties(script: dict[str, Any], schema: dict[str, dict[str, Any]]) -> dict[str, Any]:
    props: dict[str, Any] = {}

    # Title (required — find the title property)
    title_name = next((k for k, v in schema.items() if v.get("type") == "title"), None)
    if not title_name:
        sys.exit("ERROR: no title property found in database schema")
    props[title_name] = {"title": rt(script.get("title", "Untitled"))}

    # Script field (rich_text) — optional
    script_prop = find_prop(schema, "Script", "Kịch bản", "Nội dung", "Content")
    if script_prop and script_prop[1] == "rich_text":
        props[script_prop[0]] = {"rich_text": rt(script.get("script_body", ""))}

    # Reference Links (rich_text) — optional
    refs = script.get("references") or []
    if refs:
        ref_text = "\n".join(
            f"- {r['url']}" + (f"  — {r['note']}" if r.get("note") else "") for r in refs
        )
        ref_prop = find_prop(schema, "Reference Links", "References", "Links", "Tham khảo")
        if ref_prop and ref_prop[1] == "rich_text":
            props[ref_prop[0]] = {"rich_text": rt(ref_text)}

    # Structure (select)
    struct = script.get("structure")
    if struct:
        sp = find_prop(schema, "Structure", "Cấu trúc", "Framework")
        if sp and sp[1] == "select":
            props[sp[0]] = {"select": {"name": struct}}

    # Status (select or status)
    status = script.get("status")
    sp = find_prop(schema, "Status", "Trạng thái")
    if sp:
        name, ptype = sp
        if ptype in ("select", "status"):
            # Use provided status; otherwise pick the first option available
            chosen = status
            if not chosen:
                opts = schema[name].get(ptype, {}).get("options", [])
                if opts:
                    chosen = opts[0]["name"]
            if chosen:
                props[name] = {ptype: {"name": chosen}}

    # Date
    dp = find_prop(schema, "Date", "Ngày")
    if dp and dp[1] == "date":
        props[dp[0]] = {"date": {"start": date.today().isoformat()}}

    # Duration (number)
    if script.get("duration_sec") is not None:
        durp = find_prop(schema, "Duration", "Duration (sec)", "Thời lượng")
        if durp and durp[1] == "number":
            props[durp[0]] = {"number": int(script["duration_sec"])}

    # Word count (number)
    if script.get("word_count") is not None:
        wcp = find_prop(schema, "Word Count", "Words", "Số từ")
        if wcp and wcp[1] == "number":
            props[wcp[0]] = {"number": int(script["word_count"])}

    return props


def build_children(script: dict[str, Any]) -> list[dict[str, Any]]:
    """Page body: ## Script, script paragraphs (with [REF] markers preserved),
    then ## Reference Links bulleted list."""
    children: list[dict[str, Any]] = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": rt("Script")},
        }
    ]

    body = script.get("script_body", "").strip()
    # Split on blank lines → each becomes a paragraph block
    for para in [p for p in body.split("\n\n") if p.strip()]:
        children.append(
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": rt(para.strip())},
            }
        )

    refs = script.get("references") or []
    if refs:
        children.append(
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": rt("Reference Links")},
            }
        )
        for r in refs:
            label = r["url"] + (f" — {r['note']}" if r.get("note") else "")
            children.append(
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {"rich_text": rt(label)},
                }
            )

    return children


def create_page(script: dict[str, Any], schema: dict[str, dict[str, Any]]) -> dict[str, Any]:
    payload = {
        "parent": {"database_id": db_id()},
        "properties": build_properties(script, schema),
        "children": build_children(script),
    }
    r = requests.post(f"{API}/pages", headers=headers(), json=payload, timeout=60)
    if r.status_code >= 300:
        return {"ok": False, "status": r.status_code, "error": r.text, "title": script.get("title")}
    data = r.json()
    return {"ok": True, "url": data.get("url"), "id": data.get("id"), "title": script.get("title")}


def main() -> int:
    load_env()
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch-schema", action="store_true")
    ap.add_argument("--input", help="Path to scripts JSON array")
    args = ap.parse_args()

    schema = fetch_schema()

    if args.fetch_schema:
        print_schema(schema)
        return 0

    if not args.input:
        ap.error("either --fetch-schema or --input <file> required")

    scripts = json.loads(Path(args.input).read_text())
    if not isinstance(scripts, list):
        sys.exit("ERROR: input JSON must be a top-level array of script objects")

    print(f"Pushing {len(scripts)} script(s) to Notion…")
    results = [create_page(s, schema) for s in scripts]

    ok = [r for r in results if r.get("ok")]
    fail = [r for r in results if not r.get("ok")]
    print(f"\n✅ Created: {len(ok)}")
    for r in ok:
        print(f"  - {r['title']}: {r['url']}")
    if fail:
        print(f"\n❌ Failed: {len(fail)}")
        for r in fail:
            print(f"  - {r['title']}  [{r.get('status')}]  {r.get('error')[:300]}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
