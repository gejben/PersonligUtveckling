# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Personal management repository for Gabriel Fiedler. Contains documentation for weekly reviews, personal development, health, relationships, studies, and finances.

## Progress File (VIKTIGT!)

**`progress.md`** i root är en levande fil som håller koll på veckans framsteg.

**Regler:**
1. **Läs alltid** `progress.md` i början av varje session för att veta var vi är
2. **Uppdatera** när något bockas av eller händer
3. **Rensas** vid veckoreview och startar om för ny vecka
4. **Notera** saker som är värda att komma ihåg

## Subfolders with Their Own CLAUDE.md

Each main folder has its own CLAUDE.md with specific guidance:

| Folder | Content | CLAUDE.md Focus |
|--------|---------|-----------------|
| `WeeklyReview/` | Weekly reflections | Coaching, pattern recognition, "honest mirror" |
| `Studies/` | University courses | Study planning, deadlines, "study buddy" role |
| `Health/` | Training & Diet | Tracking consistency, accountability |
| `Relationships/` | Partner & Social | Knowledge bank, "trauma-aware" check-ins |
| `Development/` | Personal Growth | Focus areas, reading list |
| `Finances/` | Economy | Budget & planning |
| `Fiedler Consulting/` | Business | Strategy & admin |
| `Goals/` | Annual Goals | Long-term alignment |

**Read the relevant CLAUDE.md before working with a folder!**

## Philosophy

1. **Honest over nice** — Self-reflection that avoids real issues is useless. Name what's actually happening.
2. **Few things, done well** — Maximum 2-3 active focus areas at a time.
3. **Systems over willpower** — Build habits and structures that make the right choice the easy choice.
4. **Progress over perfection** — Track direction, not just outcomes. A bad week isn't failure if you learn from it.
5. **Regular review** — Weekly reflection keeps you honest. Quarterly review adjusts the course.

## Structure

```
personlig/
├── CLAUDE.md            # This file
├── progress.md          # Week progress (RESET WEEKLY)
├── Contacts.md          # Key contacts
├── Health/              # Training, diet, recovery tracking
│   └── CLAUDE.md
├── Development/         # Personal development plan, reading list
│   └── CLAUDE.md
├── Goals/               # Annual goals (2025.md, etc.)
│   └── CLAUDE.md
├── WeeklyReview/        # Weekly reflections using Structure.md template
│   └── CLAUDE.md
├── Relationships/       # Relationship insights and knowledge bank
│   └── CLAUDE.md
├── Studies/             # Academic tracking (Spring2026.md)
│   └── CLAUDE.md
├── Finances/            # Financial planning
│   └── CLAUDE.md
├── Moving/              # Relocation checklist
├── Fiedler Consulting/  # Business strategy
│   └── CLAUDE.md
└── gabriel_*.md         # AI-generated personality profiles
```

## Key Workflows

### Weekly Review
- Template: `WeeklyReview/Structure.md`
- Create new entries as `WeeklyReview/YYYY_WXX.md`
- Covers: training, health, relationships, development areas, next week priorities

### Chat Analysis Scripts
- `consume_chat.py` — Reads WhatsApp chat in chunks (2000 lines at a time)
- `analyze_chat.py` — Analyzes chat for emotional patterns, message volume, sender balance
- Run with: `python consume_chat.py` or `python analyze_chat.py`

## Working Style

When helping with this repository:
- Be specific about what actually happened, not what was planned
- Challenge vague goals and assumptions
- Look for patterns across weekly reviews
- Connect observations to goals and development areas
- Cross-reference `Relationships/KnowledgeBank.md` for relationship-related discussions
