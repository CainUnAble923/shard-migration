# Town Houses, townsfolk, and resting

**Draft based on the merged code on October 26, 2026.** Town Houses support staff-run test leases. Townsfolk conversations are off by default and need staff to place the residents. Paid inn rest has not been built. Live availability and appearance in the player client have not been verified.

| Feature | Current availability |
|---|---|
| Town Houses | Staff can assign a free lease on the test shard. Players cannot rent a building themselves. |
| Mara and Ellis | Conversation support is built. Staff must place them and turn on conversations before they answer. |
| Innkeeper conversations and paid rest | Planned. The existing innkeeper has neither of these new services yet. |

## Town Houses: using a test lease

A Town House makes a defined part of an existing building work as your house. Staff choose its boundaries and assign the test lease. An empty town building is not something you can claim by walking in or clicking its door.

Your account must have no other house. The test lease uses your account's one-house entitlement, including your other characters. It costs no gold, has no rent payments or overdue timer, and does not undergo ordinary house decay. Staff can end it.

After assignment, double-click the house sign to open the usual house menu. It provides the normal household controls for friends, co-owners, and public or private access. Registered building doors use house access rules while the lease lasts. In a guarded town with the correct town region, guard protection continues inside the leased area.

Stand inside the leased boundaries to use the usual house phrases, then target your own item:

| Phrase | Who can use it |
|---|---|
| `I wish to lock this down` | Owner or co-owner |
| `I wish to release this` | Owner or co-owner |
| `I wish to secure this` | Owner; use it on a container placed on the floor |
| `I wish to unsecure this` | Owner; normal strongbox restrictions still apply |

A friend does not gain the owner's storage permissions. Access to secure containers also depends on their security setting.

### Boundaries and storage

The current test supports one rectangular area, from a lowest to a highest floor height. Space outside that rectangle or height range is outside your house, even if it looks like part of the same building. Each side can be 1 to 32 tiles, and the highest floor can be at most 60 height units above the lowest. Additional floors do not multiply the storage allowance.

The provisional allowances depend on the rectangle's width times its depth:

| Allowance | Current formula |
|---|---|
| Lockdown ceiling | 8 times the rectangle's tile area |
| Total item storage limit | Tile area divided by 16, rounded down, with a minimum of 1 |

The total item limit is especially small in this first test build. It counts lockdowns, secure containers, and the items inside secure containers. It is **not** a count of secure containers you may fill. For example, a 7 by 7 rectangle reports a lockdown ceiling of 392 but a total storage limit of only 3. Normal lockdowns must pass both limits, so the larger number is not usable storage by itself. Ask staff to confirm the test site's allowance before bringing items.

Player vendors have zero capacity. There is no house customization for changing the town building's walls or floor plan, and there are no room sublets or separate room storage rights.

### Before a test lease ends

**Collect your belongings before staff end the lease.** Release and collect your lockdowns, empty and collect secure storage, and redeed your own addons where possible. Have co-owners empty their strongboxes too.

There is no belongings recovery crate or automatic bank delivery. House deletion leaves ordinary lockdowns and secures loose in the building and destroys secure strongboxes. Staff should end the lease only after it is empty. The lease's house doors are removed and the site's registered town doors are restored.

Use staff to end a test lease. There is no player lease-ending menu yet. The stock house menu still exposes transfer controls, but transferring a house is not a way to cancel its lease. Player demolition cannot end this lease because it has no house deed or refundable purchase price.

## Talking to Mara and Ellis

Mara is the town steward, and Ellis is the workshop runner. Their conversations work when staff have placed them in New Haven and enabled the feature. There are no confirmed public placement coordinates to follow yet.

With the default settings, stand within **3 tiles** while alive, with a clear line of sight to the resident. Double-click them or choose **Talk** from their context menu to open the topic list. Opening it costs nothing and gives no reward. Choose a topic to receive an answer.

You can also speak or whisper one of these phrases:

| Topic | Example phrases |
|---|---|
| Greeting | `hello`, `hi`, `good day` |
| Name | `name`, `who are you` |
| Work | `job`, `what is your job` |
| Help | `help`, `where do I start` |
| Inn | `inn`, `where is the inn`, `tavern` |
| Rumors | `rumors`, `rumours`, `news` |
| Farewell | `goodbye`, `bye`, `farewell` |

Capitalization and punctuation do not matter. Use a listed phrase by itself, or put the resident's name first, such as `Mara, hello` or `Ellis, what is your job?` A longer sentence merely containing a topic word will not match. Speech longer than 160 characters is ignored. Yelling does not start a conversation.

When more than one eligible resident hears a matching phrase, the nearest answers. Use their name to address a particular resident. The reply is sent privately to you from that NPC.

The default wait is **3 seconds between answers**, shared across residents, speech, and menu buttons. Repeating the same topic with the same NPC requires **15 seconds**. Reopening the menu does not bypass either wait. A request made too soon gets no answer.

Help points a character still doing the tutorial core back to Rook Hallowell. Other characters get general directions. Mara directs visitors to the bank beside the plaza, the League office southwest of it, and the Bountiful Harvest Inn north of the plaza. Conversations do not complete lessons, award items, train skills, or change tutorial progress. Mara and Ellis do not sell goods or accept gifts.

If nobody answers, come closer, check your line of sight, wait for the cooldown, and use an exact phrase or the Talk menu. Staff may also have conversations disabled or the resident outside its New Haven conversation area.

## Resting at the inn

There is currently no new paid-rest action, Rest confirmation window, or Rest button. Saying `rest` does not invoke this planned service. The dialogue file includes an innkeeper profile, but the existing innkeeper has not been connected to it.

The intended service would restore only your own health, stamina, and mana. Its recorded defaults are **25 gold from your backpack**, **120 seconds without harm**, and **60 seconds between successful rests**. These are plans, not a service you can buy now. Combat restrictions, payment, and restoration still need implementation and verification.

Player rentals, weekly rent, sublets, and protected belongings recovery also remain later Town Houses work. Town Houses are separate from the proposed inn-room and guild-hall systems.

Source and verification record: [P652 guide notes](../cc-P652-guide-town-houses-townsfolk.md).
