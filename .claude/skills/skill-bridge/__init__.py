"""Skill Bridge - REST API for Claude Code skills.

A middleware service that makes Claude Code skills callable via HTTP requests,
enabling the automation executor to invoke skills without subprocess calls.
"""

__version__ = "1.0.0"
__author__ = "Adar Realty Studio"

from skill_invoker import SkillInvoker
from skill_definitions import get_skill_definition, get_all_skills, validate_parameters
from response_parser import parse_skill_response
from bridge_database import SkillBridgeDatabase

__all__ = [
    "SkillInvoker",
    "SkillBridgeDatabase",
    "get_skill_definition",
    "get_all_skills",
    "validate_parameters",
    "parse_skill_response",
]
