"""Manually curated link metadata, checked 16 November 2026.

No external pages are downloaded, indexed or represented as full-text evidence.
Descriptions below are original short descriptions, not extracted source text.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import Source

SEEDS = [
    {
        "title": "SMARD electricity market data",
        "publisher": "Bundesnetzagentur",
        "description": "Explore Germany's electricity generation, consumption and market data at the original public data portal.",
        "url": "https://www.smard.de/en",
        "topic": "Electricity",
        "kind": "Data portal",
    },
    {
        "title": "Energy-Charts",
        "publisher": "Fraunhofer ISE",
        "description": "Open the original Energy-Charts portal for interactive electricity and energy visualisations.",
        "url": "https://www.energy-charts.info/",
        "topic": "Electricity",
        "kind": "Data portal",
    },
    {
        "title": "Renewable energies",
        "publisher": "Umweltbundesamt",
        "description": "Start with the German Environment Agency's overview of renewable energy and its related publications.",
        "url": "https://www.umweltbundesamt.de/en/topics/climate-energy/renewable-energies",
        "topic": "Renewables",
        "kind": "Overview",
    },
    {
        "title": "Germany's energy balances",
        "publisher": "AG Energiebilanzen",
        "description": "Find national energy balances, evaluation tables and annual reports from AG Energiebilanzen.",
        "url": "https://ag-energiebilanzen.de/en/",
        "topic": "Energy system",
        "kind": "Statistics",
    },
]


def seed_sources(session: Session) -> None:
    existing = set(session.scalars(select(Source.url)).all())
    for data in SEEDS:
        if data["url"] not in existing:
            session.add(Source(**data, saved=False))
    session.commit()
