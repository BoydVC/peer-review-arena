"""Peer Review Arena engine: personas → findings → chair consensus."""
from .personas import PERSONAS, PERSONA_IDS
from .review import run_review
from .chair import chair_merge

__all__ = ["PERSONAS", "PERSONA_IDS", "run_review", "chair_merge"]
