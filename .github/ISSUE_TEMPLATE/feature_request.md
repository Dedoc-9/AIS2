---
name: Feature Request
about: Suggest an enhancement or new feature
title: "[FEATURE] "
labels: enhancement
assignees: ''

---

## Description

**What problem does this solve?**

Please describe the use case or problem you're trying to address with this feature.

**Proposed solution**

Describe how you would like AIS² to work with this feature.

**Alternative solutions**

Describe any alternative approaches you've considered.

---

## Scope & Impact

**What area of AIS² does this affect?**
- [ ] Core system (phase_c/, validator/) — requires architectural review
- [ ] Implementation (trace_exporter, examples)
- [ ] Dashboard (UI/rendering layer)
- [ ] Documentation
- [ ] Testing & CI
- [ ] Other: ___________

**Will this break existing functionality?**
- [ ] No breaking changes
- [ ] Yes, breaking changes (describe implications):

---

## Constraints & Invariants

**Does this feature preserve system invariants?**
- [ ] I1 — Execution Contract Validity ✓
- [ ] I2 — Trace Determinism ✓
- [ ] I3 — Observational Purity ✓
- [ ] I4 — Type-Safe Ω Isolation ✓
- [ ] I5 — Irreversible State Transitions ✓

**For core system changes only:**
- [ ] Does NOT modify phase_c/ or validator/ (unless architecturally necessary)
- [ ] Does NOT change trace format or schema
- [ ] Does NOT introduce system ← UI reverse edges
- [ ] Does NOT expose Ω-domain semantically

---

## Acceptance Criteria

Describe the conditions that must be met for this feature to be considered complete:

1. [ ] Feature requirement #1
2. [ ] Feature requirement #2
3. [ ] Feature requirement #3

---

## Testing Strategy

**How will this feature be tested?**
- [ ] Unit tests
- [ ] Integration tests
- [ ] Invariant tests
- [ ] Determinism verification
- [ ] Other: ___________

**Test plan** (optional):

---

## Documentation

**What documentation needs to be updated?**
- [ ] README.md
- [ ] AIS2_USER_GUIDE.md
- [ ] CHANGELOG.md
- [ ] Docstrings
- [ ] CONTRIBUTING.md
- [ ] Other: ___________

---

## Priority & Effort

**Priority**: (Low / Medium / High / Critical)

**Estimated effort**: (Small / Medium / Large / Unknown)

---

## Additional Context

Add screenshots, diagrams, code examples, or other context that helps explain this feature request.

### Related Issues

- Related to #___ (if applicable)
- Depends on #___ (if applicable)

---

## Checklist

- [ ] I have verified this is not already implemented
- [ ] I have searched existing issues and this is not a duplicate
- [ ] I understand the architectural constraints (frozen core, invariants)
- [ ] I have considered the impact on determinism and type safety
- [ ] I am prepared to help implement or review this feature

---

**Thank you for your feature suggestion!** The AIS² team will review and prioritize accordingly.

**Note**: Features affecting the core system (phase_c/, validator/) will require architectural review and may not be accepted if they violate the frozen contract. Consider opening an architectural discussion issue first for significant changes.
