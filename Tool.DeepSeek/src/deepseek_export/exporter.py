"""Markdown 导出器"""
import re
from pathlib import Path
from datetime import datetime
from typing import Optional


def sanitize_filename(title: str) -> str:
    """清理文件名，移除非法字符"""
    title = re.sub(r'[<>:"/\\|?*]', '', title)
    title = title.strip()
    if len(title) > 100:
        title = title[:100]
    if not title:
        title = f"untitled-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    return title


def format_markdown(
    title: str,
    messages: list[dict],
    created_at: Optional[datetime] = None,
    message_count: Optional[int] = None
) -> str:
    """格式化为 Markdown"""
    lines = [f"# {title}", ""]

    if created_at or message_count:
        lines.append("---")
        if created_at:
            lines.append(f"created: {created_at.strftime('%Y-%m-%d %H:%M')}")
        if message_count:
            lines.append(f"messages: {message_count}")
        lines.append("---")
        lines.append("")

    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        role_display = "## User" if role == "user" else "## Assistant"
        lines.append(role_display)
        lines.append("")
        lines.append(content)
        lines.append("")

    return "\n".join(lines)


def export_to_file(
    output_dir: Path,
    title: str,
    messages: list[dict],
    created_at: Optional[datetime] = None,
    overwrite: bool = False
) -> Path:
    """导出为 MD 文件"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = sanitize_filename(title) + ".md"
    filepath = output_dir / filename

    if filepath.exists() and not overwrite:
        counter = 1
        while filepath.exists():
            filepath = output_dir / f"{sanitize_filename(title)}-{counter}.md"
            counter += 1

    content = format_markdown(
        title=title,
        messages=messages,
        created_at=created_at,
        message_count=len(messages)
    )

    filepath.write_text(content, encoding="utf-8")
    return filepath
