# OpenCode v0.1 smoke results

**Runtime:** OpenCode `1.18.27`, locally installed on 2026-09-02. All behavioral work ran in disposable Git fixtures under `/tmp`; raw JSONL traces are not committed.

| ID | Status | Executed evidence | Limitation / decision |
|---|---|---|---|
| Capability command | PASS | `opencode run --command capability --format json` exited 0 and emitted `step_start`, `text`, `step_finish`; text was `CAP_COMMAND_READY`. | Proves local project-command routing. |
| Primary agent | PASS | `opencode run --agent cap-primary --format json` exited 0 and emitted `CAP_PRIMARY_READY`. | Isolated agent diagnostic, not a command substitute. |
| O-D01 Direct | PASS | Installed overlay command read only `README.md`, emitted a terminal JSONL event, and `git diff --check` passed with no tracked diff. | Model narration incorrectly described the fixture's trailing newline; terminal evidence did not rely on that claim. |
| O-S01 Standard | PASS with process risk | One `harness-explorer` task and one `harness-implementer` task were recorded. Fixture diff contained exactly `+STANDARD_OK` in `README.md`; `git diff --check` exited 0. | The Implementer task returned a permission-rejected error even though the file mutation completed. This validates evidence-over-narration but makes the process result `VERIFIED_WITH_RISKS`, not clean behavioral proof. |
| O-H01 high-risk | BLOCKED (expected honest outcome) | Root recorded baseline and attempted a fresh `harness-verifier` twice. Both child-task attempts returned permission rejection; Root terminalized `BLOCKED`. | Confirms high-risk cannot become verified when the required verifier gate is unavailable. |
| O-P01 Explorer/Verifier write controls | PASS | `debug agent` rejected Explorer edit, Explorer shell-write, and Verifier edit; no probe file existed afterward. | Verifier shell is still approval-gated by design, so it is not a sandbox. |
| Installer / uninstall | PASS | Dry-run listed six overlay files; install and `verify_install.py` passed; uninstall removed only digest-matching manifest files. | OpenCode also created unrelated `.opencode/package.json`, lockfile and `node_modules`; uninstall preserved them. |
| Smoke runner | INFRA_BLOCK | A subsequent runner invocation produced `UnknownError: Unexpected server error` and exited nonzero. | Runner correctly reported `infra_block`; it is not treated as a pass. |
| O-V01 false green | Parser PASS / live scenario not run | Unit test proves narrated `VERIFIED` plus failed diff/check classifies `false_green`. | A live intentionally failing repository scenario remains unexecuted. |

These results prove that the local runtime discovers the installed command and agents, executes Direct and Standard flows, and exposes child-session/permission anomalies as observable evidence. They do **not** prove durable child-session recovery, a clean high-risk verifier completion, or portable provider authentication.
