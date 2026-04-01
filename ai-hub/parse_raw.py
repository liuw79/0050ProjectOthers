#!/usr/bin/env python3
"""Parse raw detailed text into structured Q&A data - v2."""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent
RAW_FILE = BASE_DIR / "raw_detailed.txt"
OUTPUT_JSON = BASE_DIR / "questions.json"
OUTPUT_MD = BASE_DIR / "questions.md"


def parse_raw(text):
    lines = text.split('\n')
    results = []

    # Find "课堂答疑 - 学员提问列表"
    qa_start = None
    for i, line in enumerate(lines):
        if '课堂答疑' in line and '学员提问列表' in line:
            qa_start = i + 1
            break

    if qa_start is None:
        print("ERROR: Could not find Q&A section")
        return results

    # Skip to first status marker
    i = qa_start
    while i < len(lines):
        if re.match(r'^(已回答|待回答)\s*\(\d+\)', lines[i].strip()):
            break
        i += 1

    # State machine
    # After status marker, the pattern repeats:
    #   [avatar char]  <- single character
    #   [full name]    <- 2-10 chars
    #   [company]      <- optional, contains company keywords or not a timestamp
    #   [timestamp]    <- 2026-03-28 HH:MM:SS
    #   [question text...]
    #   老师解答
    #   AI优化
    #   [answer text...]
    #   [next avatar char] <- signals new entry

    current = None
    state = "seeking_status"
    pending_lines = []  # Buffer for content between markers

    def is_timestamp(line):
        return bool(re.match(r'20\d{2}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}', line))

    def is_avatar(line):
        """Avatar is a single character (usually the first char of the name)."""
        return len(line) <= 4 and len(line) >= 1 and not line[0].isdigit()

    def is_name(line):
        """Name is 2-10 chars, Chinese characters."""
        return 2 <= len(line) <= 15 and re.match(r'^[\u4e00-\u9fffA-Za-z（）()]+$', line)

    def is_end_marker(line):
        return line == 'Close' or line.startswith('沙盘作业') or line.startswith('Part0')

    while i < len(lines):
        line = lines[i].strip()

        if is_end_marker(line):
            if current:
                results.append(current)
            break

        if state == "seeking_status":
            if re.match(r'^(已回答|待回答)\s*\(\d+\)', line):
                state = "seeking_avatar"
            i += 1
            continue

        if state == "seeking_avatar":
            if not line:
                i += 1
                continue
            # Check if this looks like an avatar (single char or very short)
            # followed by a name on next line
            if is_avatar(line):
                # Look ahead: next non-empty line should be a name
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1

                if j < len(lines) and is_name(lines[j].strip()):
                    # This is a new entry!
                    if current:
                        results.append(current)

                    avatar = line
                    name = lines[j].strip()

                    # After name: company (optional) or timestamp
                    k = j + 1
                    while k < len(lines) and not lines[k].strip():
                        k += 1

                    company = ""
                    time_str = ""

                    if k < len(lines):
                        next_line = lines[k].strip()
                        if is_timestamp(next_line):
                            time_str = next_line
                            k += 1
                        else:
                            # It's a company name
                            company = next_line
                            k += 1
                            # Next should be timestamp
                            while k < len(lines) and not lines[k].strip():
                                k += 1
                            if k < len(lines) and is_timestamp(lines[k].strip()):
                                time_str = lines[k].strip()
                                k += 1

                    current = {
                        "number": len(results) + 1,
                        "status": "待回答" if len(results) == 0 else "已回答",
                        "name": name,
                        "company": company,
                        "time": time_str,
                        "question": "",
                        "answer": "",
                    }
                    state = "reading_question"
                    i = k
                    continue
            i += 1
            continue

        if state == "reading_question":
            if not line:
                i += 1
                continue
            if line == '老师解答':
                state = "skip_ai_optimize"
                i += 1
                continue
            # Check if a new entry starts (avatar + name pattern)
            if is_avatar(line):
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and is_name(lines[j].strip()):
                    state = "seeking_avatar"
                    continue  # Don't increment i, re-process as avatar
            current["question"] += (current["question"] and "\n") + line
            i += 1
            continue

        if state == "skip_ai_optimize":
            if line == 'AI优化':
                state = "reading_answer"
                i += 1
                continue
            if not line:
                i += 1
                continue
            # If not AI优化, this might be the answer already (some don't have AI优化 marker)
            state = "reading_answer"
            # Don't increment, re-process as answer
            continue

        if state == "reading_answer":
            if not line:
                i += 1
                continue
            # Check if a new entry starts
            if is_avatar(line):
                j = i + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines) and is_name(lines[j].strip()):
                    state = "seeking_avatar"
                    continue  # Re-process as avatar
            if is_end_marker(line):
                if current:
                    results.append(current)
                    current = None
                break
            current["answer"] += (current["answer"] and "\n") + line
            i += 1
            continue

        i += 1

    if current:
        results.append(current)

    # Deduplicate by name (keep first occurrence)
    seen = set()
    deduped = []
    for q in results:
        key = q["name"]
        if key not in seen:
            seen.add(key)
            deduped.append(q)

    # Re-number
    for i, q in enumerate(deduped):
        q["number"] = i + 1

    return deduped


def main():
    text = RAW_FILE.read_text(encoding="utf-8")
    questions = parse_raw(text)

    print(f"解析到 {len(questions)} 个问答\n")

    for q in questions:
        q_preview = q["question"][:60].replace("\n", " ")
        a_len = len(q["answer"])
        print(f"  #{q['number']:2d} [{q['status']}] {q['name']:8s} | {q.get('company',''):20s} | Q: {q_preview}... | A: {a_len} chars")

    # Save JSON
    OUTPUT_JSON.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"\n已保存 JSON: {OUTPUT_JSON}")

    # Save Markdown
    md = [
        "# 升级定位与品牌战略 [深圳第70期] - 学员提问汇总",
        "",
        "> 课程时间：2026-03-28 ~ 2026-03-29",
        "> 主讲：冯卫东",
        f"> 共 {len(questions)} 个问题",
        "",
        "---",
        "",
    ]

    for q in questions:
        md.append(f"## 问题 {q['number']}")
        meta = []
        if q.get("name"):
            meta.append(f"提问人: {q['name']}")
        if q.get("company"):
            meta.append(f"公司: {q['company']}")
        if q.get("time"):
            meta.append(f"时间: {q['time']}")
        meta.append(f"状态: {q.get('status', '未知')}")
        md.append(f"**{' | '.join(meta)}**")
        md.append("")
        md.append("### 问题")
        md.append(q.get("question", ""))
        md.append("")
        if q.get("answer"):
            md.append("### 老师解答")
            md.append(q["answer"])
            md.append("")
        md.append("---")
        md.append("")

    OUTPUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"已保存 Markdown: {OUTPUT_MD}")


if __name__ == "__main__":
    main()
