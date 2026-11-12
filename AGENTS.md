# Maintaining KiteSkill

KiteSkill is a bilingual, evidence-led research skill suite. Keep the seven
`skills/kite-*/` folders independently installable. A skill may recommend another
Kite module, but must describe a useful fallback if that module is unavailable.

Instructions are original syntheses, not mirrored third-party skill bundles.
Record conceptual sources and optional tools in `THIRD_PARTY.md`. Copying upstream
code or substantial text requires a separate license/notice review.

Preserve user scope, language, completed work, and explicit choices. Local machine
paths, credentials, project names, unpublished results, and SSH details do not
belong in the public package. Do not auto-install heavy research frameworks.

Validate changes with `python scripts/validate.py` and
`python -m unittest discover -s tests -v`. Update both README languages when
installation, invocation, modules, or dependencies change. Behavioral examples
are documented acceptance cases; do not call them passed unless actually run.
