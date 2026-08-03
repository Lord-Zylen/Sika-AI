"""Load SKILL.md files from the skills/ directory."""

import os


def load_skills(skills_dir: str | None = None) -> list[dict]:
    """Scan skills_dir for subdirectories containing SKILL.md files.

    Returns a list of dicts: {name, content, path}
    """
    if skills_dir is None:
        skills_dir = os.path.join(os.path.dirname(__file__))

    skills = []
    if not os.path.isdir(skills_dir):
        return skills

    for entry in sorted(os.listdir(skills_dir)):
        skill_md = os.path.join(skills_dir, entry, "SKILL.md")
        if os.path.isfile(skill_md):
            with open(skill_md, "r", encoding="utf-8") as f:
                content = f.read()
            skills.append({
                "name": entry,
                "content": content,
                "path": skill_md,
            })
    return skills


def get_skill_summary(skills_dir: str | None = None) -> str:
    """Return a short one-line-per-skill summary for the system prompt."""
    skills = load_skills(skills_dir)
    if not skills:
        return ""

    parts = ["## Available Skills (use load_skill to get full instructions):\n"]
    for s in skills:
        # Extract the Trigger line as a one-line summary
        lines = s["content"].split("\n")
        trigger = ""
        for line in lines:
            if line.strip().startswith("## Trigger"):
                # Get the next non-empty line
                idx = lines.index(line)
                for sub in lines[idx + 1 : idx + 4]:
                    if sub.strip():
                        trigger = sub.strip()
                        break
                break
        parts.append(f"- {s['name']}: {trigger}")
    return "\n".join(parts)


def load_skill_content(skill_name: str, skills_dir: str | None = None) -> str:
    """Load and return the full content of a specific skill by name."""
    skills = load_skills(skills_dir)
    for s in skills:
        if s["name"] == skill_name:
            return s["content"]
    available = [s["name"] for s in skills]
    return f"Skill '{skill_name}' not found. Available: {', '.join(available)}"


def get_skill_prompt(skills_dir: str | None = None) -> str:
    """Build a combined prompt section from all loaded skills (full, legacy)."""
    skills = load_skills(skills_dir)
    if not skills:
        return ""

    parts = ["## Available Skills\n"]
    for s in skills:
        parts.append(f"### {s['name']}\n{s['content']}\n")
    return "\n".join(parts)
