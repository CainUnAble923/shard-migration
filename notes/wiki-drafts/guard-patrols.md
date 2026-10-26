# Guard patrols pilot: what players can use today

Draft checked against merged source on October 26, 2026, through P628 and its P635 fix-up. The current pilot records witnesses and guard calls in **Cove on Trammel** when staff enable it. It does not add walking patrols or change how guards punish crimes. It starts off, and the running shard's deployment and settings have not been checked.

## What changes for players

Ordinary play stays the same. Say **"guards"** to call for help in an active guarded region. You do not need a new skill, item, payment, or patrol menu. The existing guard response still runs, including during an observation test.

The added recorder is intended for staff-supervised tests on the test shard. Players cannot switch it on or read its log. Staff can use it to compare who saw a crime with which guards were near enough to hear a call. It gives players no new confirmation or refusal message.

Only Cove on Trammel is in this pilot, including regions nested under Cove. Cove on Felucca, New Haven, and other towns are outside the recorder's current coverage. Their guard behavior is unchanged by this work.

## Taking part in an observation test

If staff arrange a test, use ordinary guard-call speech while alive in Cove. Normal speech, yelling, and whispering have different recorded hearing ranges. Wait at least two seconds between calls if you want each one recorded. Calling sooner still reaches the ordinary guard response; the recorder skips that extra report.

The recorder automatically chooses the newest incident in that town that credits your character as a witness and is no more than 15 seconds old. There is no choice of incident or suspect. Naming someone in chat does not create evidence against them.

If you have no recent witnessed incident, the log labels your call an **investigation with no suspect** at your location. That is only a record. It does not send a patrol to search the area. Being attacked does not by itself give the recorder evidence that you saw the attacker.

Staff must check the log to tell you what the recorder captured. A guard arriving is still the ordinary response and does not prove that a guard heard the recorded report.

## Numbers used by the recorder

These limits describe observation records, not new limits on ordinary guard enforcement.

| Check | Current value |
| --- | --- |
| Witness distance from the actor | Within 14 tiles |
| Age of an incident that can be reported | Up to 15 seconds from its recorded time |
| Delay between recorded calls by one character | At least 2 seconds |
| Guard hearing range for normal speech | 15 tiles from the caller |
| Guard hearing range for a yell | 18 tiles from the caller |
| Guard hearing range for a whisper | 1 tile from the caller |

A recorded witness must be alive, on the actor's facet, able to see the actor, and have line of sight to them. Walls can block that sight. There is no facing requirement. Guards, eligible human townspeople, and players can be witnesses; staff sight is excluded. A hidden onlooker can still witness a visible actor. An actor who is hidden at the observation check is excluded.

Hearing works around corners without a line-of-sight check. A recorded listener must be a living guard within the call's range and in the same Cove jurisdiction. The report refers to the incident and recorded last-seen places; it does not track the suspect's movements. A civilian witness is recorded but does not automatically report through this new service.

The recorder is experimental. Reviews found cases where its records credit people who did not see the actual act, including around corners and with distant pet owners. Separate offenses by one culprit within one second can also be combined. The log is test data and can contain mistakes.

## What this means for criminals

**An empty witness record does not make a crime safe.** The ordinary guard system still handles the offense. Its call path does not require the caller to have witnessed it or a nearby guard to have heard it. Walls, hiding, or a report with no recorded listener do not add protection from that response.

Stock calls search for eligible offenders within **14 tiles of the caller**. A newly registered guard candidate normally has a **15-second call window**, which further qualifying actions can renew. An eligible nearby town NPC within **8 tiles** can trigger an immediate stock call. These are separate rules from the recorder's sight and report windows. Leaving a guarded-region boundary does not necessarily end existing stock candidacy.

Stock guards can still appear at the target and teleport. Their instant-kill setting defaults to on in the source; its running value is unverified. The pilot does not replace this with ordinary patrol combat, hiding searches, or a chance to surrender.

Theft keeps its existing caught, criminal, and revealing rules. Hiding after being recorded does not erase the earlier witness entry. Criminal flags, murder counts, lawful aggression, red-name rules, and existing town restrictions are unchanged. Persuasion supplies no new way to cancel a crime or stop a guard response. Den membership gains no new exemption.

## What is still being built

There are no new patrol posts, walking routes, dispatched responders, alarm relays, pursuit limits, or searches in P628/P635. Calls do not yet produce the planned "No guard answers nearby" message. There are no new checkpoint challenges, arrests, fines, bribes, or bounty rewards from this pilot.

New Haven has not been converted, and this work adds no new Young protection or guard coverage to Old Haven or Rootdeep. Proposed patrol strength, walking speeds, staffing, arrival times, and Persuasion thresholds are future design values, not current player rules.

Observation is temporary: a restart switches it off and loses its records. Switching it off during the same session stops new recording but does not clear the old log. Actual Cove floors, building sight lines, guard placement, and performance still need testing with the real map.

Source basis: [P628 build notes](../cc-P628-build-guard-patrols-pilot.md), [P635 integration notes](../cc-P635-cont-fixup-build-guard-patrols-pilot.md), and [P640 source review](../cc-P640-review-build-guard-patrols-pilot.md). The [P608 design](../cc-P608-guards-patrol-design.md) describes the later patrol system.
