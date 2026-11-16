# FAQ, safety and privacy

## What does the agent actually do on its own?

It reads, analyzes, drafts and reminds. It writes outputs to your workspace and delivers summaries to you. It does not send messages to anyone else, change payer contracts, claims, patient records, prices or system settings, or take any irreversible step. In an unattended run, anything that needs a decision becomes a tracker item that the Monday brief raises.

## Where does patient data go?

Nowhere new. Outputs use counts and rates. Patient-level worklists (for example, expansion adults due for renewal) stay inside the workspace or your revenue cycle systems and are never put in an email or chat delivery. Keep the workspace in a location your organization already approves for PHI, and never in a public repository.

## Is this legal, financial or coding advice?

No. Every place where counsel, the CFO or a certified coder must decide is marked in the skills. State law summaries come from law firm and policy sources dated November 2026 and need counsel's confirmation for any filing.

## How current are the facts?

Every date and figure in `reference/` carries its source and an as-of date of November 16, 2026. `policy-radar` keeps them current: it confirms each calendar event on the day, logs material changes from sources scored 4 or higher, and proposes assumption updates on the record. The regulatory calendar marks dates that are projections ("expected") separately from final ones.

## Our data is messy. Will it still work?

Yes. That is what the four-tier ladder is for. The program runs on public defaults if it has to and says so on every number. The data map tells you which two or three exports would raise confidence the most.

## Can we change the thresholds and defaults?

Yes: `kpi_overrides`, `schedule_overrides` and the assumption register (`assumptions.json`) in your workspace. Every change should record who made it and why; the skills do this automatically for their own changes.

## What if the agent cannot reach the workspace?

It delivers a one-line failure notice naming what was unreachable and stops. It never improvises a new workspace.

## Does it work outside Claude?

The skills follow the common SKILL.md format and the scripts use only the Python standard library, so any agent that reads skill folders and can run Python can use them. Scheduling tier B (cron or GitHub Actions) uses the Claude CLI, and tier C (calendar reminders) needs no agent at all.

## How do I update the plugin?

Pull the latest version, or download the newest `.plugin` file from the [releases page](https://github.com/mclean/healthcare-2027-autopilot/releases) and open it in Claude. Your workspace is separate from the plugin, so updates never touch your profile, data or state. Reference data updates (calendar, state rules) flow in with the plugin; your assumption register keeps your overrides. [CHANGELOG.md](../../CHANGELOG.md) lists what changed in each release.

## How do I remove it?

Stop the jobs first, then uninstall. Say "Remove the readiness jobs" and the scheduler lists every task it created and asks before deleting anything. If you used cron, GitHub Actions or calendar reminders instead, delete those entries yourself. Then uninstall the plugin from the `/plugin` menu in Claude Code or from your plugin settings in Claude desktop or web. Your workspace folder stays where it is, so your records survive until you delete it.
