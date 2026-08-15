# S187 — Extension Candidate Report Projection

S187 packages the extension-candidate queue as a read-only semantic projection.

It preserves source order and references existing validation results. Candidate extraction does not approve, promote, mutate, or infer ontology changes.

```text
Validation Results
      ↓
extension_candidate_queue()
      ↓
Extension Candidates
      ↓
Human / governed extension workflow
```
