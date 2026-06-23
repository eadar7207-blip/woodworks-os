#!/usr/bin/env python3
"""GSD Framework Helper - List and load workflows, templates, references."""

import json
import sys
from pathlib import Path

GSD_ROOT = Path.home() / "Desktop" / "Woodworks-OS" / ".claude" / "gsd"

def list_workflows():
    """List all available workflows."""
    workflows_dir = GSD_ROOT / "workflows"
    if not workflows_dir.exists():
        return {"error": "Workflows directory not found"}

    workflows = sorted([f.stem for f in workflows_dir.glob("*.md")])
    return {
        "type": "workflows",
        "count": len(workflows),
        "items": workflows
    }

def list_templates():
    """List all available templates."""
    templates_dir = GSD_ROOT / "templates"
    if not templates_dir.exists():
        return {"error": "Templates directory not found"}

    templates = sorted([f.stem for f in templates_dir.glob("*.md")])
    return {
        "type": "templates",
        "count": len(templates),
        "items": templates
    }

def list_references():
    """List all available references."""
    references_dir = GSD_ROOT / "references"
    if not references_dir.exists():
        return {"error": "References directory not found"}

    references = sorted([f.stem for f in references_dir.glob("*.md")])
    return {
        "type": "references",
        "count": len(references),
        "items": references
    }

def load_workflow(name):
    """Load a workflow file."""
    workflow_file = GSD_ROOT / "workflows" / f"{name}.md"
    if not workflow_file.exists():
        return {"error": f"Workflow '{name}' not found"}

    content = workflow_file.read_text()
    return {
        "type": "workflow",
        "name": name,
        "path": str(workflow_file),
        "content": content
    }

def load_template(name):
    """Load a template file."""
    template_file = GSD_ROOT / "templates" / f"{name}.md"
    if not template_file.exists():
        return {"error": f"Template '{name}' not found"}

    content = template_file.read_text()
    return {
        "type": "template",
        "name": name,
        "path": str(template_file),
        "content": content
    }

def load_reference(name):
    """Load a reference file."""
    reference_file = GSD_ROOT / "references" / f"{name}.md"
    if not reference_file.exists():
        return {"error": f"Reference '{name}' not found"}

    content = reference_file.read_text()
    return {
        "type": "reference",
        "name": name,
        "path": str(reference_file),
        "content": content
    }

def search(keyword):
    """Search across all resources."""
    keyword = keyword.lower()
    results = {
        "keyword": keyword,
        "workflows": [],
        "templates": [],
        "references": []
    }

    workflows = list_workflows().get("items", [])
    templates = list_templates().get("items", [])
    references = list_references().get("items", [])

    for item in workflows:
        if keyword in item.lower():
            results["workflows"].append(item)

    for item in templates:
        if keyword in item.lower():
            results["templates"].append(item)

    for item in references:
        if keyword in item.lower():
            results["references"].append(item)

    return results

def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: gsd_helper.py [list|load] [type] [name]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        resource_type = sys.argv[2] if len(sys.argv) > 2 else "all"

        if resource_type == "workflows":
            result = list_workflows()
        elif resource_type == "templates":
            result = list_templates()
        elif resource_type == "references":
            result = list_references()
        elif resource_type == "all":
            result = {
                "workflows": list_workflows(),
                "templates": list_templates(),
                "references": list_references()
            }
        else:
            result = {"error": f"Unknown resource type: {resource_type}"}

        print(json.dumps(result, indent=2))

    elif command == "load":
        resource_type = sys.argv[2] if len(sys.argv) > 2 else None
        resource_name = sys.argv[3] if len(sys.argv) > 3 else None

        if not resource_type or not resource_name:
            print("Usage: gsd_helper.py load [workflow|template|reference] [name]")
            sys.exit(1)

        if resource_type == "workflow":
            result = load_workflow(resource_name)
        elif resource_type == "template":
            result = load_template(resource_name)
        elif resource_type == "reference":
            result = load_reference(resource_name)
        else:
            result = {"error": f"Unknown resource type: {resource_type}"}

        print(json.dumps(result, indent=2))

    elif command == "search":
        keyword = sys.argv[2] if len(sys.argv) > 2 else None
        if not keyword:
            print("Usage: gsd_helper.py search [keyword]")
            sys.exit(1)

        result = search(keyword)
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
