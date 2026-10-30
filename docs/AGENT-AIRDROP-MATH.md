# The agent airdrop: what the spec actually pins down, and what it doesn't

Sources are the published documents, read directly:

- **Yellow Paper v0.5.0 (draft)** — `flop.finance/intro/yellowpaper/`. The definitive
  specification. Its version string still reads 0.5.0 / updated 2026-09-24, but the body has
  changed twice since: **2026-10-05**, 12 KB longer, one fewer `[TBD]`, the agent airdrop
  ratified; and **2026-10-08**, 6 KB longer with `[TBD]` and `[RATIFY]` both unmoved. A static
  version string is not evidence that the text is static, and neither are the tag counts.
- **Airdrop, updated 2026-10-05** — `flop.finance/airdrop/`. New page. Allocation basis,
  snapshot procedure and the per-cohort unlock table. Body edited 2026-10-08 (security
  disclosures); the "updated" line did not move.
- **Testnet, updated 2026-10-05** — `flop.finance/testnet/`. New page. Timeline, what counts,
  the four fairness rules, and how each role onboards. Body edited 2026-10-08, same reason.
- **Whitepaper, updated 2026-10-05** — `flop.finance/whitepaper/`. The non-normative
  companion. Its year-10 supply split is the only published breakdown that names the team's
  share, and §10 is given over to technocore.chat.
- **The homepage** — `flop.finance/`. Four lines of copy, one of which ties airdrop
  eligibility to following an X account and appears in no specification. It does not link to
  `/airdrop/` or `/testnet/`.
- **Project intro v0.1 (draft), updated 2026-10-26** — `flop.finance/teaser/`, formerly "the
  teaser" and dropped from the site navigation. Earlier revisions of this file called its agent
  paragraph stale, because it said the unlock schedule "is not yet set" while the Yellow Paper
  had already ratified spend-to-unlock. **On 2026-10-26 that sentence was replaced** with
  "every 3 $FLOP of it spent on inference unlocks 1 $FLOP", and the page's two caveats about
  the 85/15 split leading the parameters of record were deleted. The discrepancy is closed, in
  the Yellow Paper's favour.

- **Ask FLOP, found 2026-10-20** — `ask.flop.finance`, with its corpus published beside it at
  `/llms.txt` (an index of 34 pages) and `/llms-full.txt` (the whole text, 356 KB). The index
  calls these pages "published-tier: the same text the assistant at https://ask.flop.finance
  is allowed to quote, and the same text it cites", which makes the corpus citable. **The
  assistant's own answers are not**, and nothing in this file comes from asking it anything.
  Three status pages under `/docs/` give each network a one-word readiness state.

Everything below is quoted from those pages and re-derivable with division; see
[Checking these quotes yourself](#checking-these-quotes-yourself).

## The genesis numbers (Yellow Paper §9.3, R9.4/R9.7)

`genesis_supply = 4,400,000,000 FLOP` (18 decimals), allocated to exactly four buckets:

| bucket | FLOP | share of genesis |
| --- | ---: | ---: |
| `genesis_miner_airdrop` | 1,200,000,000 | 27.27% |
| `genesis_validator_airdrop` | 1,200,000,000 | 27.27% |
| `genesis_agent_airdrop` | 1,200,000,000 | 27.27% |
| `genesis_reserve` (not an airdrop) | 800,000,000 | 18.18% |

No token sale and no investor allocation — the airdrop page and the whitepaper both say so in
those words. **But "no team allocation" would be wrong**, and earlier revisions of this file
said it. The team's share is not in the genesis pool; it arrives through emission, and the
whitepaper now names it:

> **Team + Foundation — 2.0bn $FLOP, 10.8% of year-10 supply.** Funds network development and
> upkeep: 8 $FLOP per block each to FLOP Labs and the FLOP Foundation, issued on top of the
> block reward, halving on the same schedule and sunsetting after year ten.

That is R9.3's `subsidy_per_block_per_recipient = 8 + 8 FLOP/block` — the line already in the
derivation below — relabelled as what it is. At 10.8% it is larger than any single airdrop
cohort's year-10 share, so read "no pre-mint" as a statement about the genesis pool only.

The cohort table words the miner and agent legs as **"up to" 1,200,000,000** — a ceiling, not a
guarantee — while the validator leg, being posted stake rather than a payout, is flat.

**Year-10 supply is 18,086,624,000 FLOP**, reproducible from the emission rules:

```
emission, years 0-10   63,072,000 blocks/era x (96+48+24+12+6)  = 11,731,392,000   # R9.1, R9.2
Labs/Foundation subsidy 63,072,000 x (16+8+4+2+1)               =  1,955,232,000   # R9.3
genesis                                                          =  4,400,000,000   # R9.7
                                                                   --------------
                                                                   18,086,624,000
```

The subsidy line is the paper's own: `subsidy_per_block_per_recipient = 8 + 8 FLOP/block`
over `subsidy_duration_blocks = 315,360,000`, which it totals at 1,955,232,000 FLOP. The
year-10 sum is our addition, not a quoted figure — but the whitepaper's own year-10 split now
reproduces it component by component, which is a better check than the percentages alone:

| whitepaper's year-10 line | our derivation |
| --- | --- |
| Genesis allocation — 4.4bn, 24.3% | 4,400,000,000 (R9.7) |
| Miners — 8.8bn, 48.6% | 11,731,392,000 × 75% = 8,798,544,000 |
| Validators — 1.2bn, 6.5% | × 10% = 1,173,139,200 |
| Brokers/agents — 1.2bn, 6.5% | × 10% = 1,173,139,200 |
| Team + Foundation — 2.0bn, 10.8% | 1,955,232,000 (R9.3) |
| Staking rewards — 0.6bn, 3.2% | × 5% = 586,569,600 |

Those six sum to **18,086,624,000**, and 1,955,232,000 / 18,086,624,000 = 10.81%, which is the
10.8% the page prints. The derivation and the site agree.

One discrepancy to know about: the **airdrop page prints each cohort leg at 6.6%** and the
**whitepaper prints 6.5%**. 1.2bn / 18,086,624,000 = 6.63%, so 6.6% is the closer rounding.
Neither changes anything that matters, but two official pages do disagree.

### These numbers moved recently

Earlier revisions of this file used pre-D-0440 figures. The Yellow Paper's provenance note
records the trail, and the teaser has now caught up to it:

| | old | current |
| --- | ---: | ---: |
| genesis pool | 3,500,000,000 (D-0438) | **4,400,000,000** (D-0440) |
| validator cohort | 305,505,000 | **1,200,000,000** |
| year-10 supply | 17.2bn | **18.1bn** |
| miner / agent legs | 1,200,000,000 each | **unchanged** |

D-0440 raised `validator_min_stake` to 1,200,000, which carried the validator cohort and the
whole pool with it; the paper records it as "validator bond 305,505 → 1,200,000, carrying the
validator cohort 305,505,000 → 1,200,000,000 and the pool 3,500,000,000 → 4,400,000,000 …
leaves emission untouched". The teaser's stale "3.5bn … ratified by D-0438" banner is gone as
of its 2026-09-30 update; `3.5bn`, `3,500,000,000` and `D-0438` now return zero matches there.
Secondary coverage quoting 2.48bn or 3.5bn is quoting superseded decisions.

## The 3:1 rule shipped

Revisions of this file between 2026-09-30 and 2026-10-04 reported that the 3:1
spend-to-unlock rule had been withdrawn, because the teaser had deleted it and the Yellow
Paper's E.38 listed "whether spend-to-unlock ships" as an open question. **On 2026-10-05 it
shipped**, as normative `MUST` language in §8.2:

> An Agent grant MUST NOT unlock any principal at its start block, and **it has no end
> block**. It MUST unlock only against spend credit: **one FLOP of principal for each three
> FLOP of its locked part (R8.8) in the payable** (Appendix F.3, the gross settlement amount
> before the audit earmark) of a session settled by `settle`, by `certificate_settle`, or by
> `force_settle` → `finalize`. A payable MUST count only once its settlement block is
> finalized, `channel_dispute_window_blocks` have passed since it, and every fraud dispute
> raised against the session in that window has resolved with none upheld. Locked principal
> spent through `agent_transfer`, refunds, the R12.1d penalty, and any other leg outside the
> payable MUST NOT accrue credit. An Agent grant's unlocked amount is **⌊K/3⌋**, where K is
> the total locked part of its credited `payable`s. Its locked compute spend C, the principal
> drawn by the R8.8 compute calls net of refunds returned to the grant, **MUST NOT exceed
> ⌊3P/4⌋**, where P is its principal at creation, so spend cannot consume the quarter that its
> credit unlocks; principal neither spent nor unlocked MUST stay frozen.

The airdrop page states the same rule in one sentence:

> Spendable only on inference. **Every 3 $FLOP of the locked balance spent in settled sessions
> unlocks 1 $FLOP, so three quarters is spent on compute and one quarter becomes liquid.**
> There is no end date; balance never spent stays locked.

**The window is what was dropped, not the ratio.** E.38 used to note that a 3:1 requirement
over a Y1–Y3 release "exceeds projected inference demand over that window"; that sentence and
the open question are both gone, and the grant now "has no end block". With no deadline the
mismatch it described cannot arise.

### The unlock ceiling, which is now computable

The two bounds close the mechanism exactly. Spend at most `⌊3P/4⌋` of principal on compute;
earn `⌊C/3⌋` unlocked. At the cap:

```
spend    C = 3P/4          the most the rule will credit
unlock   C/3 = P/4         one FLOP per three spent
                 -------
total          P           three quarters consumed, one quarter liquid
```

So **a quarter of an agent grant can become liquid and no more**, there is no deadline, and
anything never spent "stays locked" permanently. Earlier revisions of this file said there was
no ceiling to plan against. There is one, it is `P/4`, and it does not expire.

### All three cohorts now have published terms

| cohort | at genesis | after genesis |
| --- | --- | --- |
| miners | 25% liquid | "The remaining 75% unlocks one $FLOP for each $FLOP the miner earns on mainnet, from block rewards and inference fees alike." Loosened on 2026-10-16 (D-0527); it read "Block rewards do not count" until then. |
| validators | "Nothing liquid: the airdrop is the bond" | "Frozen until the first halving, about two years after genesis, then released one validator per day, in an order fixed before the first release, until all are free." |
| agents | "Nothing liquid" | 3 spent → 1 unlocked, capped at a quarter, no end date |

A miner may post its locked airdrop as its own stake; a validator's release lifts only the
freeze. Ongoing block rewards and inference fees are paid liquid — "the lock applies to the
airdrop alone".

**The miner leg was loosened on 2026-10-16, and the agent leg was not.** D-0527 — "Miner unlock
credit for the grantee's minted miner-leg block rewards alongside its settled payouts;
supersedes D-0517 item 1" — adds a second source of credit for miners: a grant now unlocks
against its "share of the miner leg of the block reward (`miner_share_ppt`, §9) as actually
minted to the grantee account", as well as against channel payouts. Until that day the airdrop
page said flatly "Block rewards do not count."

Nothing equivalent exists for agents. The same rule spells out what still earns a miner
nothing — "The validator, **agent**, and staker legs of the block reward, the Labs/Foundation
subsidy, transaction fees and tips, forward-availability payments, refunds…" — and R8.7 is
unchanged: an agent's credit comes only from locked compute spend inside the payable, three for
one, capped at `⌊3P/4⌋`.

Read the two days together and the asymmetry is the point. On 10-14 D-0525 took 15% of every
settlement away from the miner and gave it to validators, slowing the miner's unlock; on 10-16
D-0527 handed miners a second, passive source of credit that more than covers it. **A miner
whose hardware simply runs now unlocks the rest of its grant without buying anything.** An
agent still has to spend three FLOP of real inference demand for every one it frees, and that
spend now carries the 15% fee. Whatever the reason, the miner leg became easier to finish and
the agent leg did not.

## What the spec does pin down — and it is the opposite of a farm

§8.2's requirements are normative `MUST` language, not placeholders. R8.4 is the one to read:

> **R8.4 — Conversion eligibility.** A faucet grant, sponsored bond, or transferred balance
> MUST NOT by itself create an allocation right; held Era-T balance and stake size MUST NOT
> be scoring terms. Agent scoring MUST derive from settled compute-channel spend and Miner
> scoring from PoI-verified effective-FLOP served; **completed job count and active days
> MUST NOT be scoring terms.** A fraud-flagged account MUST receive zero allocation unless
> its flag is overturned before the genesis specification is locked; it MUST NOT receive
> partial credit while flagged.

Every cheap farm is named and excluded: claiming the faucet, being sent tokens, being staked
by someone else, holding a balance, racking up job counts, showing up daily. The only agent
input that scores is **settled compute-channel spend**.

R8.3 closes the supply side —

> conversion MUST NOT create incremental emission or fund an allocation twice. Each miner,
> validator, and agent allocation MUST draw only from its respective `genesis_miner_airdrop`,
> `genesis_validator_airdrop`, or `genesis_agent_airdrop` pool; cohorts MUST NOT
> cross-subsidize. The `genesis_reserve` is not an Era-T airdrop pool.

— and R8.5 fixes how the snapshot must behave, even though no snapshot has been published:

> **R8.5 — Snapshot.** Conversion MUST use Era-T activity no later than a
> governance-ratified, finalized snapshot height. The per-account allocation and its hash
> MUST be published before the genesis specification is locked; the snapshot MUST remain
> revocable and correctable until that lock. The snapshot MUST identify each account's
> cohort, activity, fraud flag, and cluster identity.

"Cluster identity" is the sybil term: accounts are grouped before they are scored.

R8.8 specifies the plumbing a spend-to-unlock rule would use, if one ships:

> Still-locked principal of an Agent grant MAY be spent only through `agent_transfer`,
> `open_channel`, `top_up_escrow`, and `force_open` for compute, **within the R8.7 spend
> cap**; that spend MUST consume vesting principal and MUST NOT turn it into freely
> transferable credit.

Mechanism specified, policy unratified. That is the state of the agent airdrop.

What E.38 still lists as open, verbatim:

> ratify conversion score caps and sublinear aggregation, the accounting identity and
> owner-signed spend rules, verifiable-demand and maintained-duration gates, the validator
> cohort's activity basis, and whether activity under-counts can be appealed

"Caps and sublinear aggregation" is an anti-sybil weighting: the tenth unit of activity counts
for less than the first, and caps bound any single identity. "Verifiable-demand and
maintained-duration gates" means the spend has to look like someone actually wanted the
inference, for a while. Neither the levels nor the form is published.

The appendix also records a hole the operators have not closed:

> Residual risk: once its quarter is liquid, a miner can buy inference from itself through an
> agent it controls and unlock the rest at the 15% validator fee leg (of which 1% funds the
> audit pool; D-0525), roughly 11.25% of principal; **an agent can likewise pay a miner it
> controls from locked principal, receive about 85% of it back as that miner's payout, and
> unlock a further third of the spend. No runtime common-control rule binds either** (see
> E.49).

**Those numbers were 1%, 0.75% and 99% until 2026-10-14.** What changed is not the loop but
its price, and the change came from outside §8 entirely — see the fee split below.

### Inference now carries a 15% fee, decided on 2026-10-14

R12.1a used to end the matter in six words: settle "pays the reserved amount in full (no
settlement fee)". It now splits the money:

> At settlement (`settle`, `certificate_settle`, or `force_settle` → `finalize`), the settled
> payable amount MUST be split: `inference_fee_miner_share_ppt` = 85% to the miner, and
> `inference_fee_validator_share_ppt` = 15% to the validator pool (D-0525). The 1% audit pool
> earmark (`audit_fee_split_ppm = 10,000 ppm`) MUST be deducted from the 15% validator share
> to fund verification audits; the remainder of the validator leg is distributed intra-pool by
> the R9.5 weighting, liquid on issue (R9.13, D-0518).

The parameter table dates it precisely — `inference_fee_miner_share_ppt` 850 ppt and
`inference_fee_validator_share_ppt` 150 ppt, both carrying "#2702 (D-0525): Executive ruling
(Shu, 2026-10-14)". The audit earmark moved with it: 1% of the settlement used to come out of
the miner's payment, and now comes out of the validator leg.

**For an agent buying inference honestly, nothing in the airdrop arithmetic moves.** R8.7 is
untouched: credit is still "one FLOP of principal for each three FLOP of its locked part … in
the payable (Appendix F.3, the gross settlement amount before the audit earmark)". The payable
is what the agent pays; the 85/15 split decides who receives it. Spend three, unlock one, cap
at `⌊3P/4⌋`, all unchanged.

**For the self-dealing loop it is a fifteenfold price rise.** Routing a purchase to a miner you
control used to return about 99 cents on the dollar, with the 1% earmark the only leakage.
Now 15% goes to a validator pool you do not control, so recovering the quarter costs about
11.25% of principal rather than 0.75%. The hole E.49 leaves unbound is still unbound — but it
is no longer nearly free, and the specification's own risk note was rewritten the same day to
say so.

Five days on, the operator stated the miner's side of that split itself. On 2026-10-19
`@flop_labs` posted about CoreWeave's five-year CDS at 1,194 bps
([status 2112027080598982886](https://x.com/flop_labs/status/2112027080598982886)), and closed
with the arithmetic D-0525 had just written into R12.1a:

> A GPU owner selling inference by the job doesn’t need anyone to believe a five-year
> promise. Paid when the work clears, 85% of the fee, liquid.

Nothing in the specification moved with it, and the post is positioning rather than policy.
It is worth recording for two reasons. The 85% is now the operator's own public number, so the
split reads as settled intent rather than a revision that might be reverted — the whole of
this file's D-0525 reading rests on an edit five days old. And the word doing the work is
**liquid**: the miner's fee arrives unencumbered, while the airdrop grant the same operator
offers an agent is frozen, released only by spending three FLOP for each one freed, at a
price this very split raised by fifteen times.

Fixed dates: testnet **Q4 2026 for roughly ninety days**, mainnet **Q1 2027**; results settled
into the genesis block at testnet end, with "the bulk of the pool … expected to be distributed
at the token generation event, with any remainder released at a later stage".

## The on-ramp is now named, and so are the limits

Earlier revisions of this file reported that no eligibility basis, snapshot height or
weighting had been published anywhere, and that "the link between holding a `did:key` on
technocore.chat and receiving an airdrop appears in neither document". **Both statements
stopped being true on 2026-10-05.** The testnet page's onboarding section says, of agents:

> Agents — **create a DID and a wallet, draw from the faucet, and begin purchasing inference
> or transacting with other agents on technocore.chat.**

That is flop.finance naming a DID, the faucet and technocore.chat as the agent path. The
whitepaper goes further and gives it a numbered section of its own, §10:

> Technocore (technocore.chat) is a commerce platform for AI agents: the venue in which agents
> locate one another, interact, transact, list and accept work, and store and retrieve memory.

It mentions "technocore" 22 times. The Yellow Paper still contains zero occurrences of
"technocore" and "did:key" — it specifies the protocol, not the venue — so the division of
labour between the two documents is deliberate rather than an omission.

### The homepage adds a fifth condition that no specification contains

`flop.finance/` carries four lines of body copy under the tagline. Three are the familiar
claims. The fourth is not in any specification:

> No pre-sale
> No VCs
> 100% fair launch
> Follow @flop_labs for airdrop eligibility

That is live visible copy, not a meta tag or a comment — a `<p>` in the same list as the other
three. And it is the only place such a condition appears. `/testnet/` defines agent eligibility
as "create a DID and a wallet, draw from the faucet, and begin purchasing inference"; `/airdrop/`
scores it on settled sessions; R8.4 lists the conversion MUST NOTs and names no social
requirement. Searching all five of the other pages in the header for "follow", "x.com", "twitter"
or the handle returns **zero** hits.

So one of two things is true: the line is loose marketing copy that overstates a social follow,
or there is an eligibility input the specifications do not document. Nothing published
distinguishes them. The asymmetry decides the action: following an account costs nothing and
takes seconds, the operator's own front page ties it to eligibility, and no specification
contradicts it — it adds a condition rather than denying one. **Follow the account, and keep
expecting the allocation to be decided by settled compute spend**, which is what every normative
source says.

Worth noting alongside it: the homepage does not link to `/airdrop/` or `/testnet/` at all. Its
navigation offers the project intro, the whitepaper and media. The two pages that actually define
the airdrop are reachable only if you already know they exist.

What counts, verbatim:

> Agents — compute purchased in settled sessions. Holding test tokens earns nothing.
> **Minimum activity** — each role has a floor below which no allocation is earned, so dormant
> accounts do not dilute those that did the work.

And the four rules that govern the record:

> **One participant, one score** — wallets under common control are scored as a single
> participant; dividing activity across accounts earns no additional allocation.
> **Independent demand only** — spend routed to a miner under common control, or circulated
> between wallets under common control, is not credited as demand. **Fraud forfeits** — an
> account flagged for manufactured activity forfeits its allocation, subject to appeal within
> the review window. **Security disclosure** — vulnerabilities reported responsibly during the
> testnet, privately to security@flop.finance, could be eligible for a reward from the
> ecosystem reserve; exploiting a vulnerability forfeits eligibility.

The fourth rule was weaker on 2026-10-08 than it had been the day before. Until then it read
"are **rewarded** from the ecosystem reserve"; now a report "could be **eligible for** a
reward", and the airdrop page adds "this is not a bug bounty programme". The same edit
published the channel — `security@flop.finance`, the first contact address either page has
carried. Read it as discretion, not entitlement: finding a bug is not a route to an
allocation.

The second rule is the one that kills the obvious plan. Buying inference from a miner you also
run, or moving balance between your own wallets, **is not demand** and earns nothing. Combined
with R8.7's exclusion of `agent_transfer` and refunds from unlock credit, self-dealing is
barred on both the allocation side and the unlock side.

### The timeline and the snapshot

| phase | when | what happens |
| --- | --- | --- |
| testnet opens | Q4 2026 | onboarding opens for all three roles |
| testnet runs | about 90 days | work is verified and recorded on the testnet chain |
| **snapshot** | **close of testnet** | "The record is frozen at a published, finalized block height. Activity after that height is not credited, and **no rolling snapshot is taken**." |
| review | before genesis | "The complete allocation list and its hash are published, so every participant can verify their entry and lodge a dispute within the stated window." |
| genesis | Q1 2027 | allocation written into the genesis block; "Testnet chain state is not migrated; only the allocation is carried forward." |

"Q4 2026" is not a commitment, and the page says so in the line directly under its own
timeline — a sentence earlier revisions of this file never quoted:

> **Dates and rules are provisional** The testnet opens when its readiness criteria are met,
> and may be extended if they are not. Operational rules and the minimum-activity floors are
> published with the testnet rules.

Two things follow. The opening date is conditional on criteria that are not themselves
published, so a slip needs no announcement — and **the minimum-activity floors arrive with the
testnet rules**, not through E.38. That is the first published answer to *when* any part of the
scoring becomes knowable: at the open, not before.

Against that, the operator's own timing. On 2026-10-11 Arthur Hayes posted from `@CryptoHayes`
([status 2109428767856951404](https://x.com/CryptoHayes/status/2109428767856951404), still
served; the profile page no longer carries it):

> What a great @token2049. I got some youthful energy with cellular medicine from
> @VeritaHealthHQ and then dropped the thinking behind @flop_labs all week. Now it’s back on
> the grid so we can ship FLOP Testnet in a few weeks.

"A few weeks" from the CEO, and a page that reserves the right to extend. Treat the window as
real and the date as unset.

One snapshot at the close, not a rolling average, so there is no benefit to being early beyond
the activity that accumulates — and no way to arrive at the last minute, since allocation is
pro rata to accumulated settled spend. And the airdrop itself has no claim pressure:

> There is no claim window and no deadline: the account holder releases unlocked amounts from
> the freeze with a claim transaction, whenever they choose.

(The 90-day window in this kit's close-1 notes was that contest's *prize* claim, a different
thing.)

## A date, and thirty-four pages that were not there yesterday

On 2026-10-20 both operator accounts pointed at a surface this file had never seen — a
documentation assistant at `ask.flop.finance`, "Ask the docs", whose corpus is published
beside it. The assistant is a chatbot and its answers are worth nothing as evidence; the
corpus is primary, and it answers questions this file has been carrying open for weeks.

The first is a date. Until 10-19 the only published timing was the testnet page's conditional
opening and a CEO post saying "a few weeks". Now:

> Testnet: the working target is Tuesday 3 November 2026, running about 90 days. It is a
> target rather than a fixed date and will be confirmed as devnet onboarding completes.

> Mainnet, TGE and token listing: Q1 2027, tracking to early February.

The arithmetic is given rather than asserted — ninety days from 3 November lands at the start
of February — and a private devnet has been admitting outside operators "from the week of 13
October", earning nothing, purely to have machines proven before scoring starts. Three status
pages carry a one-word state each, which is a better opening detector than any prose: testnet
and mainnet both read "Status: planned.", devnet reads "Status: development."

### What an agent is supposed to do, in the operator's own words

> 1. Create an agent and get a DID key — the community has built easy ways to do this. 2. When
> testnet launches, claim testnet $FLOP from the faucet into your wallet (the claim period —
> hourly or daily — is not yet decided). 3. Instruct your agent to actually spend it on an
> inference request; the task itself does not matter. 4. Spent testnet $FLOP becomes your
> claim on mainnet $FLOP. 5. The mainnet allocation is locked, and unlocks as you spend it on
> mainnet inference at 3:1 — every three $FLOP you spend on inference releases one locked
> $FLOP. There is no time-based vesting: what you never spend stays locked.

Two sentences follow it that settle what the preparation is worth:

> If you don't use it, you lose it. Creating DIDs earns nothing; posting your DID in a
> TechnoCore room earns nothing.

> None of this is live until testnet opens — the working target is 3 November; today you can
> only do step one.

Step one is a keypair. That is the whole of what can be done before the window opens, and it
is what this kit's `init` already does.

On 2026-10-24 the corpus grew from 34 pages to 36, and one of the new ones is the toolchain for
step three. *Send a request to a specific miner* documents a CLI (`flop … session run --miner
<ss58> --model … --max-flop 0.01`), an SDK (`@flop-labs/sdk`, `runDirectSession`) and a local
MCP tool, and it is explicit that all of this is devnet today. Two sentences in it are worth
carrying here, because they describe how an agent will be funded and what that costs in care:

> `--new-wallet` replaces the keystore options on devnet: it saves an unencrypted, owner-only
> test wallet in `~/.flop/session-wallets/` and requests faucet funding after comparing faucet
> and RPC genesis hashes.

> Use an encrypted keystore for valuable funds.

So a faucet does exist and the official tooling already calls it — on devnet, which earns
nothing. The agent-facing testnet faucet is still absent: technocore.chat's three
machine-readable files have carried zero occurrences of "faucet" since 24 September, and the
corpus still says that is where it will appear.

The same page is the first place the organisation names software an outsider would install, so
it is also the first place a convincing fake becomes possible. The genuine artefacts are
`@flop-labs/sdk` and images under `ghcr.io/flop-labs/flop-core/`, and the documentation is
emphatic about how to reference them:

> Use these exact pins rather than floating `latest` or `stable` tags.

### The faucet is the ceiling, and it arrives through technocore.chat

> Agents draw testnet $FLOP from a faucet with per-identity limits, so an agent's inference
> volume on testnet is bounded by the faucet rather than by how much it can acquire.

This is the most consequential line in the corpus for sizing the agent leg, and it cuts
against the reading this file has carried since the beginning. The pool is fixed and the
allocation is pro rata to spend, so the obvious conclusion was that whoever spends most wins.
On testnet nobody can spend much: the faucet meters every identity, so capital cannot buy a
larger share of the agent pool, and what separates participants is showing up and spending
what they are given. The spend-to-unlock ratio on *mainnet* is untouched by this — three for
one, cap `⌊3P/4⌋`, no end block — but the testnet allocation that creates the principal is
rationed at the tap.

The same page says where the tap is:

> It is also the front door to testnet: the testnet faucet is reached through it, and the
> network's functions are integrated into it as testnet and then mainnet go live.

So watching technocore.chat's own machine-readable files for the word "faucet" is the right
detector, and on 2026-10-20 it still returns zero.

### Why no conversion formula can be published

E.38 has sat at `[RATIFY]` for weeks. The corpus explains the shape of the hole rather than
filling it:

> the total number of tokens credited at the genesis block is fixed and published, but the
> ratio a given participant converts at is not, and cannot be until testnet is over.

> That is a feature rather than an omission — a fixed pool divided by measured work is what
> stops the airdrop rewarding registration instead of use — but it means no conversion formula
> can be published in advance, and anyone modelling a per-unit outcome should model the pool
> and their expected share of it.

Read with the faucet limit, that is as close to a usable answer as exists: model the pool,
assume your spend is capped at whatever the faucet gives one identity, and expect your share
to fall as more agents arrive.

### Ratified is not built

> These rules are ratified but not yet built: the runtime still vests every grant on a 90-day
> linear curve.

> Draft whitepaper. The genesis distribution ceremony is not yet wired.

Every unlock rule quoted in this file — the miner quarter, the agent 3:1, the validator freeze
— describes a specification whose implementation is a linear 90-day vest. That gap is the
operator's own disclosure, not an inference, and it is the strongest reason to treat all of
this as live text rather than settled fact.

On the agent leg the corpus used to be vaguer than the Yellow Paper. Until 2026-10-26 it read
"**Agents:** the release schedule is not yet set (see above)" and, on its airdrop page, "**When
it becomes liquid is not yet set** — the Yellow Paper keeps the agent release schedule open".
Earlier revisions of this file quoted the first of those and argued that both statements were
true if "release schedule" meant a calendar, since nothing releases with time.

**That argument is no longer needed.** On 2026-10-26 the corpus replaced every one of those
sentences with the rule itself:

> **Every 3 FLOP of locked airdrop spent on inference unlocks 1 FLOP.**

> **Agents:** every 3 FLOP of locked airdrop spent on inference unlocks 1 FLOP (see above).

The same edit landed on the agent-integration page, in the one-line summary inside
`/llms.txt`, and on the project intro — four surfaces on one day. The summary tier now states
what §8.2 and R8.7 have specified since 2026-10-05, and the remaining gap is the one this file
has been pointing at all along: what the *runtime* does. That sentence did not change:

> These rules are ratified but not yet built: the runtime still vests every grant on a 90-day
> linear curve.

The Yellow Paper sharpened the same point on the same day. `airdrop_vesting_duration_blocks` is
still 7,776,000 blocks, but its description is no longer a plain statement of the schedule:

> Interim pallet schedule: 90-day linear airdrop vesting at 1-second block time, governing no
> ratified grant tier (§8.2).

Read that twice. The only vesting curve the runtime implements **governs no ratified grant
tier** — it is scaffolding that matches nothing the specification has decided. E.38 is still
`[RATIFY]`, `[TBD]` is still 17, and Appendix E still carries the same 32 items it carried
yesterday.

One piece of the plumbing is observably being built, which is worth recording next to the
disclosure above. On 2026-10-22 `tclk` — the org's HTLC library for agents that meet in a
technocore.chat room, idle in the repository listing since 29 September — moved, and its
changelog's `[Unreleased]` section had gained:

> `@flop-labs/tclk-flop`: native FLOP HTLC settlement with devnet defaults and explicit
> testnet/mainnet RPC and genesis configuration.

> A hosted deployment of the MCP server at https://tclk.technocore.chat/mcp, streamable HTTP,
> no account and no key.

Read it for exactly what it is: an *unreleased* entry in a library whose own README says
"Alpha. `PaperRail` rehearses the lifecycle without backing it with value", at version 0.1.0
with 29 commits. Nothing settles FLOP today. But the rail that would move it now has testnet
and mainnet RPC and genesis configuration written for it, which is the first code-side
movement toward the 3 November target anywhere in the organisation's public repositories — the
Yellow Paper mirror is three site revisions behind and technocore-chat's published files have
not changed since 24 September.

## The fourth slice has a purpose now, and it pays for audience, not compute

Everything above measures one thing: how much $FLOP a unit of verified compute earns. The
genesis table has a fourth row that earns nothing by computing, and until this revision this
file described it only by what it is not — `genesis_reserve`, 800,000,000 FLOP, 18.18% of
genesis, "not an Era-T airdrop pool". The published corpus says what it *is*, and has said so
since at least 2026-10-21:

> **Funding:** the 800,000,000 $FLOP ecosystem reserve inside the airdrop pool (4.4% of
> year-10 supply), which also covers builder programmes and security-disclosure rewards.

What it funds is a referral programme. The normative spec records the decision inside E.38's
own residual-risk note:

> Under D-0531 (#1358), the workbook's legacy on-chain referral commission model (6–10%) is
> superseded by a public explorer leaderboard and periodic referral lotteries funded from
> `genesis_reserve` = 800,000,000 FLOP and settled off-chain.

Three words in that sentence matter more than the mechanism: **settled off-chain**. Every
other number in this document is a claim a verifier co-signs and a chain settles. This one is
a payout decided by an operator-held ranking, and the spec's own open questions say the
controls are not written yet — the same sentence continues:

> Decide the unallocated-remainder disposition, publication of operator-held filter inputs,
> and the `genesis_reserve` release controller.

So: nobody has decided who releases the 800,000,000, what happens to whatever is never paid
out, or whether the inputs to the ranking get published at all. That is a fifth of the genesis
pool with no named controller, sitting in the same appendix item that still blocks the
airdrop.

The mechanism, where it is specified, is deliberately resistant to the obvious gaming:

> Payment follows what the referred audience does on the network, never views or likes, which
> can be manufactured.

Ranking during testnet is on "the $FLOP that referred wallets spent on inference, received
from inference and spent through the HTLC"; at mainnet, on net change in $FLOP held. Payouts
go to the leading creators in proportion to their share of $FLOP held across the cohort, and a
separate lottery draws a fixed number of referred wallets at random each period for an equal
share of that period's pool. Referrals are single-tier, validators cannot be referred, and
there are "no bespoke deals for individual KOLs or agencies — no paid posts, no retainers and
no private allocations."

**For a compute participant the practical consequence is small but real.** The reserve is not
drawn from the miner, agent or validator legs — those are 1,200,000,000 each and fixed — so a
referral programme does not dilute a miner's share of its own pool. What it changes is the
read on the 4,400,000,000 headline: 3,600,000,000 of it is earned by machines, and
800,000,000 is a growth budget whose release nobody controls on paper yet.

### Why this section is dated 2026-10-25 and the source is dated 2026-10-21

It was published four days before this file noticed. The corpus carried `referral` fifteen
times, `lottery` nine times and the funding sentence verbatim on every daily fetch from
2026-10-21 onward; the page-level diff that runs each day correctly reported "no change"
because there was none. The gap was a reading gap, not a source change: the daily check
compared the corpus against yesterday's copy and never asked what was in it that this file had
failed to mention. A diff tells you what moved. It will never tell you what you missed the
first time.

### Somebody else can post your bond — on testnet, by a build flag

The second thing in this revision is smaller and more immediately useful. Registration on this
network requires a bond, and the capital question has been "whose". The spec now carries a
parameter that answers it for testnet only:

> D-0528: active sponsored principal counts toward the miner capacity bond and the validator
> effective minimum, and sponsors may post an operator's whole registration bond
> (sponsor_register_miner / sponsor_register_validator).

It is gated at compile time — `sponsored_self_stake_enabled` is a
`cfg!(feature = "sponsored-self-stake")` flag — and the §13 status table is explicit about
which runtimes get it:

> Sponsored registration bonds (R6.1a) §6.1, §15.2 PARTIAL: source landed; on by build feature
> in the devnet (volta) and testnet runtimes (the feature alone is a compile error; CI checks
> the default-feature mainnet node reports it off); the sponsor's own fungible holds can still
> overlap its frozen principal (E.32)

Read the three claims in order. *Source landed* — this is written code, not a planned stub,
which puts it among the small set of testnet mechanisms that exist today. *On by build feature
in the devnet and testnet runtimes* — so it is a testnet affordance by design, and CI actively
asserts that the mainnet node reports it off. *The sponsor's own fungible holds can still
overlap its frozen principal* — the sponsor's collateral is not proven distinct from its other
commitments, and that is a numbered open item, E.32.

For anyone deciding whether to enter the testnet, this is the first published route in which
the bond is not necessarily your own money. It is also, for the same reason, the shape a
sponsorship scam would take, and the programme that would route it does not exist yet.

## The week it stops being a document

For six weeks everything in this file has been text. On 2026-10-26 the operator said, on both
accounts within forty-five minutes of each other, that it is about to become a network you can
connect to:

> In the coming days @flop_labs will open up Devnet for anyone to join as a miner or validator
> and for agents to connect to the network. Participation does not count toward any token
> allocation. The point of Devnet is to do some public tests before we graduate to Testnet /
> airdrop

> Devnet coming very soon

Two sentences in that announcement are worth separating. "**for agents to connect to the
network**" is the first time an operator statement invites agents, rather than miners and
validators, to join anything. "**Participation does not count toward any token allocation**" is
the operator confirming, in their own words, what this file has said about every devnet
measurement: the private devnet running since mid-October earns nothing, and the public one
about to open earns nothing either. The airdrop begins at testnet, whose working target is
still 3 November and whose one-word status is still `planned`.

### The release candidate names its packages, and none of them exists

The same day, the corpus gained a thirty-seventh page: an upgrade guide for miners, validators,
SDKs and agents, headed

> **Release candidate, 26 October 2026.** The five JavaScript packages below were published to
> npm, and the Python SDK `flop-sdk` 0.2.0 to PyPI, on 29 October 2026; they install with no
> registry configuration.

> The other versions below are prepared for publication after review and merge; their presence
> in this guide does not mean they are published.

That is the 2026-10-30 wording. Until that day the same paragraph read "Package versions below
are prepared for publication after review and merge. Their presence in this guide does not mean
they are available on npm or PyPI. Obtain the release operator's publication receipt before
installing." — and the receipt requirement now applies only to what is still unpublished:

> Obtain the release operator's publication receipt before installing those.

It names `@flop-labs/contracts@0.1.1`, `@flop-labs/client@0.2.1`, `@flop-labs/sdk@0.4.0`,
`@flop-labs/pi@0.3.1`, `@flop-labs/cli@0.4.0` and a Python `flop-sdk` at source version 0.2.0,
"no public PyPI launch is certified here". The agent instructions are concrete — install
`@flop-labs/pi@0.3.1` through a Pi package manager, run the CLI with `pnpm --package
@flop-labs/cli@0.4.0 dlx flop --help`, and

> do not globally replace the public Hermes launcher's `flop` command

**Every one of those package names returns 404 on the npm registry.** Checked on 2026-10-26
against `registry.npmjs.org`: `@flop-labs/sdk`, `@flop-labs/cli`, `@flop-labs/pi`,
`@flop-labs/client`, `@flop-labs/contracts` and `@flop-labs/tclk-flop` are all absent, which
means the `@flop-labs` scope is currently unclaimed. So the guide is exactly as literal as it
sounds: today, `npm i @flop-labs/sdk@0.4.0` cannot install the operator's SDK, because the
operator has not published it. Anything that *does* resolve under one of those names before the
publication receipt exists was put there by somebody else.

This also settles a question this watch has been carrying as its strongest pre-testnet signal —
whether a public node repository would appear. The guide answers it directly:

> The source repository is private; external operators receive the reviewed runtime or
> validator bundle from the network operator.

The organisation's public listing has held at the same seven repositories since 11 September and
should not be expected to grow a node. Miner images come from a manifest at
`https://flop.network/releases.json`, which this session cannot read — `flop.network` still
returns CONNECT 403 — so the pinned digests an operator is told to verify are not checkable
from here.

### A status row went backwards, and it costs an agent 20%

One line in §13 moved from `LIVE` to `PARTIAL`, which is the first regression this watch has
recorded:

> Failed/early-close three-way split (φ) PARTIAL: tariff P, the (1−φ)(E−P) refund and the
> all-or-nothing split are wired, but the runtime still burns the φ·(E−P) leg (burn_from into
> TotalBurned, reported as Settled.burned) instead of transferring it to FLOPFoundationAccount
> as R12.1d and R9.10 require under D-0529

Nothing broke; the specification moved past the code. D-0529 made zero burn protocol-wide, so
§12.1's penalty rule was rewritten the same day —

> Otherwise, the agent is refunded (1−φ)·(E−P), and the penalty φ·(E−P)
> (refund_penalty_phi_percent = 20%) MUST be transferred in full to FLOPFoundationAccount (§9.3
> R9.10) with zero burn — never the miner.

— and the invariant that keeps settlement atomic was widened to cover that leg. The row above is
the honest consequence: the runtime still burns it.

For an agent the arithmetic is the same either way, and it is worth knowing before opening a
session. Escrow `E`, tariff `P` actually consumed, ambiguous early close: the agent gets back
`(1−φ)(E−P)` with `φ` = 20%, so **a fifth of the unspent escrow is gone** — to the Foundation
once the code catches up, to nobody until then. A miner-fault non-delivery uses `φ = 0` and
refunds in full. Size the escrow to the work, not to the session's ceiling.

A second correction, to yesterday's reading of sponsored bonds. D-0528 does let a sponsor post
"an operator's whole registration bond", but the parameter reference gained a line the same day
that bounds it for validators:

> validator_min_self_stake_ratio_percent 20 percent §15.2 Legacy minimum validator self-stake
> ratio when sponsored backing is enabled (§15.2).

So on a sponsorship-enabled build a validator still has to find a fifth of its own floor. The
table it sits in is prefaced as covering parameters "single-site or not yet wired for
cross-language enforcement (enforce: false)", so treat the number as the intended bound rather
than an enforced one.

### What the non-normative pages stopped disagreeing about

The whitepaper keeps a standing list of its own statements that differ from the Yellow Paper. On
2026-10-26 it shrank from nine entries to four. Gone: the 85/15 inference-fee split, that no
$FLOP is burned, that validators take no delegated stake, and the seven staking tiers — the four
things D-0525, D-0529 and D-0530 settled over the previous eleven days. Still differing:

> These statements still differ from the Yellow Paper: governance decided by validators, an
> hourly committee, per-block settlement, and slashing a miner for non-delivery.

None of the four touches the agent leg. And the Yellow Paper's own front matter now adds
Appendix I (Pallet Index Reference) to the list of normative sections, while Appendix B's
decision index finally reads `D-0401..D-0441` and `D-0501..D-0533` — the two lines that were
repository-only yesterday. The mirror and the site agree again, in both directions, and the
mirror's source commit moved from `flop-core@4e2b00890` to `flop-core@dfd98a59d` on the same
day.

## The packages exist now, and the operator's own check for them does not

Three days ago this file recorded that the release guide named five npm packages and that every
one of them returned 404. On **2026-10-29 between 04:00:46 and 04:03:01 UTC** all five appeared
on the public registry, in dependency order:

| package | version | first published (UTC) |
| --- | --- | ---: |
| `@flop-labs/contracts` | 0.1.1 | 04:00:46 |
| `@flop-labs/client` | 0.2.1 | 04:00:48 |
| `@flop-labs/pi` | 0.3.1 | 04:00:56 |
| `@flop-labs/cli` | 0.4.0 | 04:00:59 |
| `@flop-labs/sdk` | 0.4.0 | 04:00:53 |

Every version matches the release candidate exactly. `@flop-labs/tclk-flop`, the FLOP settlement
rail still sitting in `tclk`'s `[Unreleased]`, is **not** among them and still returns 404.

**What the metadata supports.** All five declare
`repository: git+https://github.com/flop-labs/flop-core.git`, carry one maintainer
(`svidyuk`), are licensed `MIT OR Apache-2.0`, depend on each other in the order they were
published, and each has a sibling `0.0.0-stage` version — the fingerprint of a release pipeline
rather than a hand-made squat. None of the five declares an install-time script: the `scripts`
blocks hold only `build`, `test`, `typecheck` and similar, and npm does not run those on
install. On that evidence this is the operator shipping its own code.

**What nothing supported, on the day the packages appeared.** The guide that named them had not
changed: through 2026-10-29 it still said that their presence in the guide "does not mean they
are available on npm or PyPI" and to "obtain the release operator's publication receipt before
installing". That wording was replaced the next day — see below — so it is quoted here inline
rather than as a live block quote.

**The gap this file recorded on 2026-10-29 lasted one day.** That revision said the packages
were almost certainly real but that the operator's own way of confirming them had not been
satisfied — no receipt, and npm absent from the official-links page — and concluded that
installing was "a decision taken on inference". The first of the three wait conditions landed on
2026-10-30: the upgrade page was rewritten to state the publication itself, and the corpus
gained a thirty-eighth page whose whole job is to list the published packages.

> These are the FLOP packages anyone can install today without a token or a private registry.
> Each name links to its registry page, which carries the full reference README for the
> published version. Versions below are the current releases as of 2026-10-30; the registry is
> authoritative if they differ.

It lists the same five at the same versions this watch measured on the registry, plus
`flop-sdk` **0.2.0** on PyPI — whose metadata gives `FLOP Network <dev@flop.network>`, an
address on one of the four domains the official-links page names, and an upload time of
2026-10-29T05:27:41Z, an hour and a half after the npm batch. That is the first tie between a
published artefact and FLOP's own namespace that does not depend on reading the package's own
`repository` field.

The same page carries the sentence worth pinning to a wall, because it converts a guess into a
list:

> FLOP has not published Rust crates, a Go module, or the agent SDK, gateway core, x402 types
> or Hermes plugin packages. A package with one of those names on a public registry is not
> FLOP's.

Two caveats survive. The maintainer account is still `svidyuk` on all five npm packages and
still appears in no primary source; what changed is that the operator now vouches for the
packages, not for the account. And `flop.network/releases.json`, named on the new page as the
way to get a reproducible digest pin for the container image, still returns CONNECT 403 to this
session, so the image pins remain unverifiable from here.

### "By early next week", which is also testnet week

The same day, both accounts posted about the public devnet. Hayes, at 07:04:51 UTC:

> The @flop_labs Devnet will be opening to the public in days.

And an hour later, from `@flop_labs`:

> Devnet participation instructions will be made available by early next week. stay tuned...

Put that beside the published timeline and the arithmetic is uncomfortable rather than alarming.
The testnet working target is **Tuesday 3 November** — early next week. The corpus says the
target "will be confirmed as devnet onboarding completes". So the instructions for the devnet
that gates the testnet are now due in the same few days as the testnet itself, and the one-word
status at `/docs/network-testnet` still reads `planned`, as it has every day since 20 October.

Nothing in that changes what this file computes, and nothing in it changes what a participant
should do: the devnet earns nothing, by the operator's own statement, and the airdrop begins at
testnet. It does mean the 3 November target should be read as what the corpus calls it — "a
target rather than a fixed date" — and that the status word, not the calendar, remains the thing
to watch.

## The word "useful" came out of the name

On 2026-10-30 every published surface stopped calling the mechanism proof of **useful**
inference. The Yellow Paper went from 39 occurrences of `PoUI` to zero and 39 of `PoI`; the
whitepaper and the project intro went 3 → 0 each; the corpus went 13 → 2, and its 16 instances
of the phrase "useful inference" went to zero. The glossary entry was rewritten with it:

> PoI — Proof of inference; the verification stack that establishes a miner performed the
> requested inference on the requested model.

This is a naming sweep, and the lesson of the 2026-10-20 sweep applies again: **it landed
inside a sentence this file quotes.** R8.4, the rule that decides what counts toward an
allocation, now reads "Miner scoring from `PoI`-verified effective-FLOP served" where it read
`PoUI`-verified the day before. Every other clause of R8.4 is identical, word for word — the
faucet-grant exclusion, the ban on balance and stake as scoring terms, the agent leg deriving
from settled compute-channel spend, the fraud-flag rule. **Nothing about eligibility changed.**
The quote check is what surfaced it; a byte count would have called the day quiet on a page
that grew by 17 KB for unrelated reasons.

Whether dropping "useful" means anything is not something this file can measure, and it is
worth resisting the urge to read intent into a find-and-replace. What can be said is narrow:
the claim that the inference is *useful* was load-bearing in the project's own rhetoric, it is
no longer in the name of the mechanism, and the same revision added a section about selling
compute forward to venues.

### A market for compute entered the normative spec

That section is new and large: **§12.5, FLOP Compute Unit (FCU)**, with six normative rules and
a new open item. The Compute Reservation Unit the whitepaper described has been renamed —

> FCU is the current name for the Capacity/Compute Reservation Unit (FCU) ratified in D-0434;
> this rename preserves the existing contract terms.

— and the mechanics are now specified rather than sketched. An FCU denominates 1,000,000 integer
G_n under a pinned meter, with accounting to 0.000001 FCU. Positions launch bilaterally and may
then be shared by at most ten holders with a minimum lot of a tenth. Resale pays the selling
holder, must not repeat the provider's original payment, and binds a non-reusable identifier
plus a delivered-work snapshot. New primary offers must support fourteen UTC-calendar start
dates, D+1 through D+14 at 12:00 UTC, with D+7 the default. Four decisions arrived with it:
**D-0534** (representation and payment), **D-0535** (`content-v1` model identity from published
per-file SHA-256), **D-0536** (booking horizon and retained activation gates) and **D-0537**
(pause semantics and indexed events).

The whitepaper's version of the section now argues a regulatory position in public, citing
specific comment letters by docket number — OneChronos at CFTC-2026-1850-0068, Hyperbolic at
-0050, ACU Markets 0011 and DNA Compute 0094, plus comments 0021, 0049 and 0045 — and a NYMEX
submission, 26-370, for a 730-GPU-hour contract month. It states what it is reaching for:

> The intended classification is a bonded, prepaid, physically redeemed forward with intent to
> deliver, whose units are transferable claims on that delivery.

and immediately disclaims it:

> These submissions corroborate the design intent; this description is not a regulatory
> determination or legal advice.

It also draws a boundary this file had not seen stated: **"Scope — FCUs cover inference only."**
Training capacity is excluded, on the argument that a contiguous cluster is worth more than the
same GPUs scattered and that "no flat unit prices its topology".

**None of this touches the airdrop, and the spec says so in two places.** The count of the word
`airdrop` in the Yellow Paper is 40, the same as yesterday. D-0537's rule is explicit that
existing "transfers/resales, cancellation, settlement, refunds, distribution claims and bond
release MUST retain their existing rules", and that "Unpause MUST NOT bypass any other
activation or eligibility gate". And the product is not switched on: R12.5e says the ownership
and payment rules "MUST NOT authorize standardized-object activation before that profile is
complete", and that profile is the new open item:

> **E.58 — FCU executable object profile [RATIFY]**. Fixed object inputs: 1 FCU = 1,000,000 G_n
> under a pinned meter; purchaser-selected supported model; maximum 1,000 ms completion after
> miner acceptance of an eligible chunk; default D+7 noon UTC start with an explicit end

So the `[RATIFY]` count went from 6 to 7 — the first time an open item has been *added* since
this watch began, and Appendix E grew from 32 items to 33. Read it as what it is: four days
before the testnet target, the open-items list got longer rather than shorter, and the item
that got added is about selling compute forward, not about the airdrop. E.38 is still
`[RATIFY]`, `[TBD]` is still 17, and E.40's agent leg is still unassigned.

## What is still open

E.38 is shorter than it was, and what remains does not include the agent unlock:

> The conversion score, validator activity basis, Validator release order, and reserve
> disposition remain open in E.38.

So the **unlock** is specified and the **allocation formula** is not. The airdrop page states
the agent basis in prose — "The allocation is shared pro rata to compute purchased in settled
sessions" — while the Yellow Paper still lists the conversion score as open. Where they
disagree the Yellow Paper wins, and it has not yet ratified "pro rata". Treat the prose as the
operator's stated intent, not as a ratified formula; the caps, the sublinear form and the
activity floors are still unpublished numbers.

### Reading the tags, and how an item actually closes

The appendix defines its own vocabulary, and the definitions change what E.38's state means:

> Tags: **[TBD]** value/definition absent · **[RATIFY]** proposed, awaiting sign-off ·
> **[PLANNED]** decided, not yet wired. To close an item: write the value into its home
> section, then delete the stub (closed numbers are retired, not reused).

**E.38 is tagged `[RATIFY]`, not `[TBD]`.** By the paper's own definition that means the
conversion score has been *proposed* and is awaiting sign-off — drafted, not absent. It is one
stage from publication, and the stub already names what will land: "ratify conversion score
caps and sublinear aggregation, the accounting identity and owner-signed spend rules,
verifiable-demand and maintained-duration gates, the validator cohort's activity basis, and
whether activity under-counts can be appealed."

**And the closing rule means the signal is a disappearance, not an edit.** Watching E.38's text
for the formula is watching the wrong thing: when it ratifies, the value goes into §8.2 and the
stub is deleted. The detector is `E.38` dropping to zero occurrences — currently six.

This is not a guess about process. E.39 "Validator-reward liquidity" was `[RATIFY]` in the
repository snapshot of 2026-09-24 and is **absent from the live paper** — and the §13 row for
emission went `PARTIAL` → `LIVE` for the validator leg on 2026-10-08. A `[RATIFY]` item closed,
its stub vanished, and a status row flipped, exactly as the legend describes. E.38 is the same
tag at the same stage, for the agents.

### The repository ran nineteen days behind the site, and then caught up in one day

`github.com/flop-labs/yellowpaper` calls itself the "normative specification". Its markdown is
readable at `raw.githubusercontent.com/flop-labs/yellowpaper/main/yellowpaper.md` even though
github.com's HTML refuses this session's proxy, so the lag could be counted rather than inferred:

| marker | repo `3c97bbc` (2026-09-24) | live site, 2026-10-09 |
| --- | ---: | ---: |
| `[TBD]` stubs | 20 | **18** |
| `[RATIFY]` stubs | 6 | 6 |
| E.38 — conversion and release policy | `[TBD]` | **`[RATIFY]`** |
| E.39 — validator-reward liquidity | `[RATIFY]` | **closed, stub deleted** |
| E.44 — cooperative work-credit eligibility | `[TBD]` | `[PARTIAL; future activation/recovery TBD]` |
| "it has no end block" (R8.7 agent unlock) | 0 | **1** |
| "whether spend-to-unlock ships" | **1** | 0 |

Those counts reconciled exactly: 20 − 1 (E.38 promoted out of TBD) − 1 (E.44 promoted to
PARTIAL) = 18, and 6 + 1 (E.38 in) − 1 (E.39 deleted) = 6.

**On 2026-10-13 the gap closed.** Two sync commits landed the same day — `b03378c` from
`flop-core@a1f3759e`, then `70e691c` from `flop-core@5e6e2427` — and `yellowpaper.md` went from
313,714 to 351,901 bytes. Every marker above now matches the site: `[TBD]` 18, `[RATIFY]` 6,
E.38 `[RATIFY]`, E.39 gone, "it has no end block" present, "whether spend-to-unlock ships"
absent. **The sync brought the repository up to the site. It did not move the specification
forward**: nothing in the new text ratifies a conversion score, names an activity floor, or
changes E.38 or E.40.

Two things worth keeping from the episode. First, the private core repository is moving:
`c65e3fc5` (2026-09-24) → `a1f3759e` → `5e6e2427` in one day, and a fourth hash, `600cfffb`,
appears in a render published in a different repository. Second, **the lag can reopen at any
time** — it ran nineteen days once. The byte count of `yellowpaper.md` is the cheap detector,
and the site remains the copy to quote.

**It reopened, and closed again, on 2026-10-25.** `yellowpaper.md` sat at exactly 351,901
bytes on every daily fetch from 2026-10-13 through 2026-10-24 — twelve days — and then went to
376,464 (+24,563 bytes, 392 lines added, 231 removed). Eleven decision identifiers arrived at
once, taking the repository from 53 distinct `D-0…` records to 64: `D-0441`, `D-0518`,
`D-0521`, `D-0525` through `D-0531`, and `D-0533`. `E.41` went `[PLANNED]` → `[RESOLVED]` in
the repository's Appendix E.

**Nine of those eleven were already on the site**, whose extracted text has not changed since
2026-10-23 — `D-0518`, `D-0521` and `D-0525` through `D-0531` all appear on the published page
and did not arrive today. `E.41` reads `[RESOLVED]` on the page too. So this was the mirror
catching up a second time, and again it moved no specification forward: the item that gates the
airdrop is `[RATIFY]` on both copies, the `[RATIFY]` count is 6 on both, and the set of
Appendix E item numbers is the same 32 on both copies on both days.

The two exceptions run the other way, which is new. `D-0441` and `D-0533` appear **only in the
repository**, and only inside Appendix B's decision-log ranges — the repository now cites
`` `D-0401`..`D-0441` `` and `` `D-0501`..`D-0533` `` where the page still shows
`D-0401..D-0432`. Neither identifier's text is on either copy; the records themselves live in
`decisions/v0.4.md` and `decisions/v0.5.md`, which this watch does not yet fetch. The repository
can therefore be *ahead* on an index line while being behind on content, so "the site is newer"
is a rule about the body text, not about every line.

One correction to the detector. The byte count caught today's sync, as the paragraph above
predicted it would — but it only works on the repository markdown, where a sync lands as tens of
kilobytes. On the published page it has already failed once, on 2026-10-20, when five pages
changed their visible text at an identical length. Byte count is the cheap detector *for the
mirror*; extracted-text comparison is the detector for the site.

One trap in reading that markdown. The repository writes cross-references as markdown links, so
`grep -c 'remain open in E.38' yellowpaper.md` returns **0** while the sentence is present as
`remain open in [E.38](#appendix-e--open-specification-items)` — the same false zero that HTML
tags produce on the rendered page, in a different costume. Strip `[text](url)` to `text` before
counting. Strip backticks too, but **never** underscores: `htlc_burn_share_ppt` becomes
`htlcburnshareppt` and silently stops matching.

### The second open gate: E.40, and it is not about the airdrop

E.38 governs the genesis airdrop. A separate item governs what agents earn *afterwards*, from
emission, and earlier revisions of this file did not mention it at all. `agent_share_ppt` is
10% of every block reward, and it is not being paid to anyone:

> **E.40 — Agent & staker leg distribution [TBD]**. Specify how the `agent_share_ppt` (10%)
> and `staker_share_ppt` (5%) pools are paid out: under D-0530, the 5% `staker_share_ppt` leg
> is allocated to the duration-locked community staking pool across seven lock duration tiers
> with zero slashing risk and no validator or miner intermediary (exact tier weights and claim
> distribution mechanics remain E.40); the eligible set for the agent leg and its pro-rata
> basis (agents: verified inference spend, unconfirmed), cadence, dust handling, and, for the
> staker leg, whether payouts are liquid on issue (agent-leg payouts are liquid under R9.13).
> The agent leg must also choose its accounting unit (owner account, delegate key, or
> registered agent identity), whether owner-signed spend outside the §6.2 delegate caps counts
> (yellowpaper#31), and its spend basis … **Until this ratifies both legs accrue in sovereign
> pool accounts and are never distributed (§9.1 R9.12).**

**That stub was rewritten on 2026-10-20**, in a revision that added 21.8 KB and closed one
`[TBD]` (18 → 17). The clause from "under D-0530" to "remain E.40" is new, and it splits the
item: the staker leg now has a destination, and the agent leg still has none. What the
placeholder says of each is the whole story:

> Placeholder: duration-locked community staking pool across 7 tiers for the staker leg; the
> agent accounting unit and spend basis remain unconfirmed, with both escrow-settled and
> work-settled bases open.

And §13's status table, reworded on 2026-10-08, says the same from the other direction. The
emission row flipped from `PARTIAL` to `LIVE` — but the promotion is the *validator* leg:

> LIVE (validator earnings and sponsored-stake payouts are liquid, like the miner leg and the
> Labs/Foundation subsidy; earnings do not grow stake or its freeze. **The agent and staker
> legs accrue in pool accounts until E.40 ratifies their distribution.**

So of the four emission legs, three now pay and the agent leg does not. Two consequences worth
keeping straight:

- **The airdrop and the emission leg are different questions with different open items.** A
  ratified E.38 would settle the genesis 1,200,000,000; it would say nothing about the 10% of
  every block thereafter. Both are unpublished, and they can resolve in either order.
- **E.40 names the question this kit exists to answer.** "The agent leg must also choose its
  accounting unit (owner account, delegate key, or registered agent identity)" — and the
  paper's own warning is that "Per-identity accounting makes identity count the reward lever,
  so per-identity credits need verifiable-demand gating". Whichever unit wins, a DID that a
  third party can verify without the key is the artefact that survives the choice.

## What follows

1. **The unlock is now plannable and the allocation still is not.** `ceiling = allocation / 4`,
   no deadline, three quarters spent on inference you actually wanted. What remains unknown is
   the size of the allocation, which depends on an unratified score and unpublished activity
   floors.
2. **Settled compute-channel spend is the only agent input that scores**, on both the Yellow
   Paper's side (R8.4) and the site's ("compute purchased in settled sessions"). Nothing about
   holding, receiving, transferring, job counts or active days counts, and self-routed demand
   is explicitly excluded.
3. **Being checkable is still the cheap, durable position**, and it now has a named venue: a
   DID and technocore.chat are the published agent on-ramp. R8.5's "cluster identity" and the
   site's "one participant, one score" both say the same thing — many keys under one hand count
   once, so the work goes into one identity rather than across several. Our census finds 740 of
   2,310 claimed DIDs (32%) clear even the cheapest checkability bar, up from 21% of a 487-DID
   population five days earlier.
4. **Wash-spend is barred on the allocation and unbound on the unlock.** "Independent demand
   only" excludes self-routed spend from the allocation, and R8.7 excludes `agent_transfer`,
   refunds and the R12.1d penalty from unlock credit. But E.38's residual-risk note, extended
   on 2026-10-05, now spells out the agent-side loop as well: pay a miner you control from
   locked principal, take about 85% back as that miner's payout, and unlock a further third of
   the spend — with "no runtime common-control rule binds either".

   The `⌊3P/4⌋` cap still holds, so the quarter is still the most that can come liquid. What
   the loop changes is its **price** — and on 2026-10-14 that price went up fifteenfold.
   D-0525 split the settlement 85/15 between miner and validators, so reaching that quarter
   now costs roughly 11.25% of principal instead of the 0.75% it cost when the 1% audit
   earmark was the only leakage. The allocation-side
   rule is enforced by the operator's filters at snapshot time; the unlock-side gap is
   acknowledged in the specification as unenforced at runtime. Anyone modelling the agent leg
   should price both, and anyone relying on the ratio to create real demand should note that
   the paper does not claim it will.

## Checking these quotes yourself

All seventy block quotes above are verbatim from the six pages in the header, the
`ask.flop.finance` corpus, the `tclk` repository's own markdown and several X posts, checked by
extracting each quote, normalising whitespace, and grepping every five-word window back out of
the fetched text. To re-verify:

```sh
for u in intro/yellowpaper airdrop testnet teaser whitepaper; do
  curl -s "https://flop.finance/$u/" > "$(basename "$u").html"
done
curl -s https://flop.finance/ > root.html   # four lines of copy, easy to skip and worth reading
curl -s -A "$UA" https://x.com/CryptoHayes/status/2109428767856951404 > hayes.html  # the posts
curl -s -A "$UA" https://x.com/flop_labs/status/2112027080598982886 > flop.html     # themselves;
                                                       # the profiles roll past them in a few days
curl -s https://ask.flop.finance/llms-full.txt > ask.txt       # the whole published-tier corpus
curl -s https://raw.githubusercontent.com/flop-labs/tclk/main/CHANGELOG.md > tclk.txt
curl -s https://raw.githubusercontent.com/flop-labs/tclk/main/README.md >> tclk.txt
sed -E 's/\[([^]]*)\]\([^)]*\)/\1/g; s/[`*]//g' ask.txt > ask.html   # markdown marks out, as
                                                      # for the repo markdown below
python3 - <<'PY'
import re, html, glob
INLINE = r'code|span|a|strong|em|b|i|sup|sub|abbr|kbd|small|var|cite|q|mark|time'
for f in sorted(glob.glob('*.html')):
    h = open(f, encoding='utf-8', errors='replace').read()
    t = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', h)
    t = re.sub(r'(?is)</?(%s)(\s[^>]*)?>' % INLINE, '', t)  # inline: NO separator
    t = re.sub(r'(?s)<[^>]+>', ' ', t)                       # block: a space
    open(f[:-5] + '.txt', 'w').write(re.sub(r'\s+', ' ', html.unescape(t)))
PY
grep -c 'whether spend-to-unlock ships' yellowpaper.txt  # 0 since 2026-10-05
grep -o '\[TBD\]' yellowpaper.txt | wc -l                # 18 on 2026-10-05, was 19
grep -o '\[RATIFY\]' yellowpaper.txt | wc -l             # 6; E.38 is one of them
grep -o 'technocore.chat' testnet.txt | head -1          # the named agent on-ramp
wc -c yellowpaper.html                     # 578805 since 2026-10-16, 578190 on 10-15, 567365 on 10-08
```

The repository's own markdown is fetchable too, and it is a *different revision* — useful as a
contrast, never as a source for a quote:

```sh
curl -s https://raw.githubusercontent.com/flop-labs/yellowpaper/main/yellowpaper.md > repo.md
wc -c repo.md             # 377134 on 2026-10-26, 376464 on 10-25, 351901 from 10-13, 313714 before
grep -o '\[TBD\]' repo.md | wc -l                 # 17, matching the site since the 10-25 sync
grep -oE 'D-0[0-9]{3}' repo.md | sort -u | wc -l  # 64 after that sync, 53 before it
grep -o 'flop-core@[0-9a-f]*' repo.md | head -1   # dfd98a59d on 10-26, 4e2b00890 on 10-25
sed -E 's/\[([^]]*)\]\([^)]*\)/\1/g; s/[`*]//g' repo.md > repo.txt   # links and code marks out,
grep -c 'remain open in E.38' repo.txt            # underscores left alone -- 1, not the raw 0
```

`github.com` HTML returns 403 to this session's proxy but `raw.githubusercontent.com` does not,
so repository *files* are readable even when repository *pages* are not.

Three notes on method, all learned the hard way.

**Quote from the fetched copy, not from memory.** Revisions of this file before 2026-09-30
carried four block quotes that were paraphrases or inventions rather than quotations —
including figures for a 3:1 arithmetic that appear nowhere in the source, and the word
"infeasible", which the Yellow Paper has never used. The numbers all checked out; the
quotation marks did not.

**A byte count is not a static document either.** On 2026-10-20 six of the seven pages this
file quotes changed their visible text, and five of them — airdrop, testnet, whitepaper, media
and teaser — did it at a byte count identical to the day before. The edit was a naming sweep:
"Flop" became "FLOP" throughout, which the new `ask.flop.finance` index states as a rule
("Always written FLOP, in capitals; FLOPs is the compute unit, not the name"), and one phrase
was reworded around it ("Flop's implementation of the HTLC" → "the FLOP implementation"). Same
length, different text, in the sentence this file quotes for the Labs/Foundation subsidy. Only
the extracted-text comparison caught it; the quote check then named the sentence. Compare the
text, not the size.

**A static version string is not a static document.** The Yellow Paper still says "Version
0.5.0 (draft) / Updated 2026-09-24", and on 2026-10-05 its body grew by 12 KB, ratified the
agent unlock, resolved one `[TBD]`, and extended the E.38 residual-risk note mid-sentence.
Watching the version line would have missed all of it. **Byte count and the `[TBD]` count are
the signals that caught it**, and the grep-back check above caught two same-day edits inside
sentences this file was already quoting ("within the R8.7 spend cap", and the agent-side half
of the residual risk). Re-run the check on every revision, not only when the version changes.
It caught a third revision on 2026-10-08 — another 6 KB, with `[TBD]` and `[RATIFY]` both
unmoved, so the counts alone would have called it quiet.

**The extraction is part of the measurement, and it fails in two directions.**

*Counting against the raw HTML gives false zeros.* `grep -c 'remain open in E.38'
yellowpaper.html` returns 0 while the sentence is plainly on the page: the markup breaks it
across a tag and a newline, and `grep` works a line at a time. A multi-word phrase counted
against `.html` is not a measurement — it is a false zero that reads exactly like a removal.
Count against `.txt`. Single words are safe either way, which is why this hid for as long as
it did.

*HTML comments are invisible and must go first, with no separator.* X renders a mention as
`@<!-- -->VeritaHealthHQ`; a stripper that treats the comment as a tag and leaves a space
yields `@ VeritaHealthHQ`, and the quote stops matching. Remove `<!--…-->` before anything
else.

*Replacing every tag with a space gives false mismatches.* The Yellow Paper sets identifiers
in `<code>`, so a naive strip yields `settle , by certificate_settle , or` and splits
``payable``s into `payable s` — four of the quotes above failed the check on text no reader
would recognise. Hence the two-pass strip in the snippet: inline elements out with no
separator, block elements out with a space. Get that wrong and the check either passes bad
quotes or condemns good ones, and there is no way to tell which from the output.

**A rename lands inside the sentences you quote.** On 2026-10-20 "Flop" became "FLOP" across
six pages; on 2026-10-30 "proof of useful inference" and `PoUI` became "proof of inference" and
`PoI` across every page and the corpus, and that one reached into R8.4, the eligibility rule
quoted above. Both times the grep-back check named the sentence and a size comparison would not
have: the 10-20 sweep was byte-identical and the 10-30 revision changed 17 KB for unrelated
reasons. Run the quote check before reading the diff, not after.

**A diff reports what moved, never what you missed.** The `ask.flop.finance` corpus carried
the referral programme — its funding out of `genesis_reserve`, its leaderboard, its lottery and
its not-yet-live sign-up — on every daily fetch from 2026-10-21, and the daily page-level
comparison correctly reported no change on each of them, because there was none. Four
revisions of this file went out without mentioning a second claim on a fifth of the genesis
pool. A change detector is only as good as the first read it is differencing against, so a
corpus that is newly in scope needs an inventory pass, not just a baseline.

**A profile page is not an archive.** The `@CryptoHayes` quote above was taken from
`https://x.com/CryptoHayes` on 2026-10-14, and by 2026-10-15 it was gone from that page: the
profile embeds only a handful of recent posts. The recipe above used to name the profile URL,
so for three days it could not re-verify a quote that was correct the whole time — the check
reported 21 of 22 and the fault was in the recipe. Cite the status URL, which still serves the
post. Three more traps live in the same markup. The embedded JSON comes both bare
(`full_text:"…"`) and escaped (`\"full_text\":\"…\"`), so a selector written against one form
reads as zero against the other. `full_text` is truncated for a long post, with the fuller
body in the adjacent `text` field. And a fetched X page carries bytes that make `grep` call
the file binary, which puts its warning on stderr and leaves a counting pipeline reading 0 —
pass `-a`. That last one cost this watch a day on 2026-10-16: three posts were sitting in the
file while the count said nothing had been fetched.
