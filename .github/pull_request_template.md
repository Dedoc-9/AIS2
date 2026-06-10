## Pull Request: [Brief Description]

**Related Issue(s)**: Closes #___ (or "N/A" if no issue)

### Type of Change
Please select the relevant option:
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] Feature addition (non-breaking change that adds functionality)
- [ ] Documentation update
- [ ] Refactoring (code cleanup, no functional change)
- [ ] Test coverage improvement
- [ ] Performance optimization
- [ ] Other (please describe):

### Description
Please provide a clear and concise description of the changes in this PR.

**What problem does this solve?** (if applicable)

**How does this change address the problem?**

---

## Checklist

### Code Quality
- [ ] Changes follow PEP 8 and project style guidelines
- [ ] Code has been formatted with `black`
- [ ] Code passes `ruff` linting checks
- [ ] Type hints are added where appropriate
- [ ] Code passes `mypy` type checking
- [ ] Docstrings are added to public functions/classes

### Testing
- [ ] New tests added (or not applicable)
- [ ] All existing tests pass locally: `pytest tests/ -v`
- [ ] Determinism is preserved (if applicable)
  - [ ] Run twice: `python examples/minimal_system.py` (should be byte-identical)
- [ ] Coverage maintained or improved (if applicable)

### Documentation
- [ ] README.md updated (if applicable)
- [ ] AIS2_USER_GUIDE.md updated (if applicable)
- [ ] CHANGELOG.md updated with this change
- [ ] Docstrings added/updated (if applicable)
- [ ] Comments added for complex logic (if applicable)

### System Integrity
- [ ] **NO changes to core system** (phase_c/, validator/)
  - If changes to frozen core: explain architectural necessity
- [ ] **NO changes to invariants** (FREEZE.md, INVARIANTS.md)
  - If changes needed: open separate architectural discussion issue
- [ ] **NO changes to trace format** (TraceEvent, TraceLog schema)
- [ ] **NO new system ← UI reverse edges** (rendering remains pure)

### Final Review
- [ ] I have self-reviewed my code
- [ ] I have tested my changes thoroughly
- [ ] I am confident this PR does not break existing functionality
- [ ] All CI checks pass (GitHub Actions: test, lint, reproducibility)

---

## Breaking Changes

Does this PR introduce any breaking changes?
- [ ] No breaking changes
- [ ] Yes, breaking changes (please describe below and justify):

**Justification** (if applicable):

---

## Notes for Reviewers

**@Dedoc-9**: Please review with focus on:
1. Adherence to frozen architecture (phase_c/, validator/)
2. Preservation of determinism guarantees
3. Type safety of Ω-domain isolation
4. No introduction of system ← UI reverse edges

---

## Additional Context

Add any other context, screenshots, or examples that help explain the change.

### Before
(if applicable: paste code or screenshot showing previous behavior)

### After
(if applicable: paste code or screenshot showing new behavior)

---

**Thank you for contributing to AIS²!**

---

*Please ensure all checklist items are completed before requesting review.*
