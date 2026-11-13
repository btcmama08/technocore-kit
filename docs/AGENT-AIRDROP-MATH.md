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

**"Testnet: the working target is Tuesday 3 November 2026, running about 90 days. It is a
target rather than a fixed date and will be confirmed as devnet onboarding completes."** And:
**"Mainnet, TGE and token listing: Q1 2027, tracking to early February."** *(Both were block
quotes until 2026-11-13, when the page retracted them; see the last section.)*

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

**"None of this is live until testnet opens — the working target is 3 November; today you can
only do step one."** *(Block quote until 2026-11-13, when the sentence was replaced; the
replacement is in the last section.)*

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

**"Release candidate, 26 October 2026. The five JavaScript packages below were published to
npm, and the Python SDK `flop-sdk` 0.2.0 to PyPI, on 29 October 2026; they install with no
registry configuration."** And: **"The other versions below are prepared for publication after
review and merge; their presence in this guide does not mean they are published."** *(Both were
block quotes until 2026-11-13, when the heading became a published-package baseline; see the
last section.)*

That is the 2026-10-30 wording. Until that day the same paragraph read "Package versions below
are prepared for publication after review and merge. Their presence in this guide does not mean
they are available on npm or PyPI. Obtain the release operator's publication receipt before
installing." — and the receipt requirement now applies only to what is still unpublished:

**"Obtain the release operator's publication receipt before installing those."** *(Block quote
until 2026-11-13, when the sentence went; the bundles now "require the release operator's
independently approved version, digest and source receipt".)*

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

**"The source repository is private; external operators receive the reviewed runtime or
validator bundle from the network operator."** *(Block quote until 2026-11-13, when the second
clause was shortened to "receive reviewed bundles from the network operator". The private-source
statement itself is unchanged.)*

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
> published version. Versions below are the current releases as of 2026-11-11; the registry is
> authoritative if they differ.

(The date in the last sentence read 2026-10-30 when this section was written and 2026-11-11
from 2026-11-13; the sentence is otherwise unchanged, and by then it was a day behind the
registry again.)

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
packages, not for the account. *(The publishing identity moved to GitHub Actions under npm
trusted publishing on 2026-11-08, which narrows this caveat; see the last section. The listed
versions are the ones that were current on 2026-10-30 and have since moved — the page's own rule
is that the registry is authoritative.)* And `flop.network/releases.json`, named on the new page
as the way to get a reproducible digest pin for the container image, still returns CONNECT 403 to
this session, so the image pins remain unverifiable from here.

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
activation or eligibility gate". And the product is not switched on: R12.5e said the ownership
and payment rules "MUST NOT authorize standardized-object activation before that profile is
complete", and that profile was the new open item — **E.58, "FCU executable object profile",
tagged `[RATIFY]`**, fixing 1 FCU at 1,000,000 G_n under a pinned meter, a purchaser-selected
supported model, a maximum 1,000 ms completion after miner acceptance of an eligible chunk, and
a default D+7 noon-UTC start with an explicit end. *(That entry was a block quote in this file
until 2026-11-04, when E.58 was ratified and removed from Appendix E; the sentences above are
now a summary of text that is no longer on the page, per the note on rewritten sources in
"Checking these quotes yourself". What replaced it is in the last section.)*

So the `[RATIFY]` count went from 6 to 7 — the first time an open item had been *added* since
this watch began, and Appendix E grew from 32 items to 33. Read it as what it was: four days
before the testnet target, the open-items list got longer rather than shorter, and the item
that got added was about selling compute forward, not about the airdrop. E.38 was still
`[RATIFY]`, `[TBD]` still 17, and E.40's agent leg still unassigned — and on 2026-11-04 all
three of those were still true while E.58 itself closed.

## Somewhere to file the objection

The organisation's public repository listing had held at seven since 11 September, and this file
recorded on 2026-10-26 that an eighth — a node — should not be expected, because the release
guide says the source is private. On **2026-10-30** an eighth appeared, named `network`, and it is
not the node. It is the intake desk:

> The public intake for the **running** FLOP Network: bugs in nodes you operate, protocol
> behaviour that contradicts the spec, gateway problems, docs gaps, and feature requests. The
> code lives elsewhere; this repository holds the issues, the triage process, and public release
> notes for FLOP services.

(The last clause arrived on 2026-11-11. Until then the sentence ended "the issues and the triage
process"; see the entry for that day below.)

So the private-source conclusion stands. What changed is that there is now a published place to
take a disagreement, with five templates (node bug, protocol behaviour, gateway, docs, feature
request), a triage ladder that starts every issue at `status:triage`, and a stale policy of
fourteen days plus seven. Two of its sentences are worth keeping for separate reasons.

The first draws a line this file has been drawing by hand:

> The gateway is a convenience service run by FLOP Labs, not part of the protocol. A gateway
> outage is not a network failure, and reports about it are kept separate on purpose.

The second is the one that matters for a document like this one. `SECURITY.md` sorts findings into
private and public, and the public side is named explicitly:

> Open a public issue instead when the finding is "this does not work well" rather than "this can
> be exploited": a crash with no attacker benefit, a bound you think is loose, an incentive you
> find unconvincing.

**"An incentive you find unconvincing" is the category this file has been filling for six weeks.**
The self-dealing arithmetic in E.38's own residual-risk note, E.49's admission that "no runtime
common-control rule binds either", the agent leg of E.40 accruing to a pool nobody can draw from,
the ninety-day vesting curve that governs no ratified tier — none of those is an exploit, and
until 30 October there was nowhere official to put them. There is now, and the operator asked for
them in writing.

What belongs on the private side is worth reading beside §9 of this file, because it is the
operator's own list of what it thinks can go wrong, and metering is on it:

> **Metering** — inflating effective FLOP or rewards, under-reporting work.

Private reports go through a GitHub security advisory or to `security@flop.finance`, the one
address the official-links page publishes, and the policy asks for "the network (devnet or
testnet), the release, commit or image digest you ran, and a concrete attack: who deviates, what
it costs them, and what they gain."

One absence is worth recording. The five templates cover miners, validators, the gateway, the
docs and feature requests. **There is no agent template**, and the node-bug form's required
"Role" field exists to distinguish a miner from a validator. The intake assumes the people
running hardware, which is consistent with everything else: the agent path is specified, the
operator path is the one being onboarded.

## The target date arrived, and what opened was the other network

Two things happened on 2026-11-03, and the gap between them is the whole finding.

The operator announced that the devnet is open. `@flop_labs`, 08:43:33 UTC
([2117538159735259565](https://x.com/flop_labs/status/2117538159735259565)):

> Devnet is now open to public

Forty minutes earlier, `@CryptoHayes`
([2117528284061741312](https://x.com/CryptoHayes/status/2117528284061741312)) had put it in
terms aimed squarely at the readers of this file:

> Get test FLOP, explore blocks, and call verified inference from your agent

Then an explorer, a faucet, an API, an MCP endpoint, `npm i @flop-labs/sdk`, docs and the ask
site — **seven `t.co` shorteners and one npm command.** The npm command is the only item a
reader can check from the post itself, and it checks out: `@flop-labs/sdk` 0.4.0 is on the
published list. The seven shortened targets are not resolvable from this session, so the
endpoints discussed below come from the documentation, not from those links.

And the post ends with four sentences the operator did not have to write:

> Devnet tokens have no value and earn no rewards or airdrop weight. The chain may reset.
> There is no FLOP token yet: never share a seed phrase, and check links at

**That is the operator pre-empting, in the announcement itself, every misreading this file
would otherwise have had to warn about.** It states that the thing being opened earns no
airdrop weight, that the chain is disposable, that the token does not exist, and that links
need checking — on the one day of the project so far when a reader is most primed to believe
the opposite. Credit where it is due; it also happens to be the shortest correct summary of
what today means for an agent.

A note on reading it. The body above is the long-form `NoteTweet` text, not the `full_text`
field: X truncated that field at 272 characters, and the truncation cut the post two words into
the SDK bullet — **everything quoted above, disclaimer included, was missing from the first
extraction this watch made of it.** The check that caught it was grepping the saved page for
the sentence rather than trusting the extractor's output.

And the testnet did not start. The operator's own one-word status, the only machine-readable
statement of what is running, was byte-identical to the previous eleven days on all three
networks:

| page | 2026-10-20 → 2026-11-03 |
|---|---|
| `ask.flop.finance/docs/network-testnet` | `Status: planned.` |
| `ask.flop.finance/docs/network-devnet` | `Status: development.` |
| `ask.flop.finance/docs/network-mainnet` | `Status: planned.` |

2026-11-03 was the working target for testnet, named in the corpus as "the working target is
Tuesday 3 November 2026, running about 90 days". The same sentence calls it "a target rather
than a fixed date", so the date passing is not a broken promise; it is a schedule datum, and
the one to carry forward is that **the 90-day testnet had not begun on the day it was meant
to, which moves the earliest plausible genesis later by however long the slip runs.** Note
also that `devnet` still reads `development` on the morning its operator called it open to the
public. The status page and the announcement are not describing the same threshold, and when
they disagree this file follows the status page.

### What actually opened, and who it is for

The promise being kept here is the 10-29 one — "Devnet participation instructions will be made
available by early next week" — and it was kept in the documentation, not in the tweet. The
`/docs/run-miner` page was rewritten on 2026-11-03: the private Tailscale tailnet that every
earlier revision required is gone, and with it the age-encrypted auth keys, the `tag:miner`
ACLs and the `tailscale serve` recipe. The section that was headed "Join without the tailnet
(invite-only preview)" is now simply "Join the devnet (invite-only preview)", and on that day
it read: **"From 30 October 2026 miners join the devnet over public endpoints. It is still by
invitation: the devnet operator approves each miner account before the sponsor stakes it."**
*(Block quote until 2026-11-05, when the page replaced the second sentence; the heading lost
"(invite-only preview)" with it. The replacement is in the last section.)*

Three concrete things are now published that were previously hand-delivered. The decode policy
is one:

> Nobody sends you the decode policy. The chain stores only its hash

> It runs in the `flop` CLI image, takes the published policy for your `MODEL_HASH`, hashes it
> the way the chain does, and writes both lines only if the finalized chain allowlists that hash
> for the model; otherwise it exits non-zero and changes nothing.

That is a real improvement in the trust model and worth naming as one: the operator no longer
has to be trusted to send the right policy, because the chain's allowlist is what the resolver
checks against. The page says as much — "Because the hash binds the JSON, the manifest host
needs no trust." The second is a public installer pack with a public agent skill, replacing the
`pnpm dlx skills add` command that earlier revisions gave; the third is a published controller
package with its own README at a versioned path, `miner-controller-0.1.228`. **All three live
on `flop.network`, which this session still cannot reach** — so this file records that they
are published and does not pretend to have read them.

Gateway admission also stopped being a request:

> Gateway admission needs no request from you: once calibration is accepted and the endpoint
> answers the gateway's probe, the miner is listed from its signed endpoint ad. That last step
> is not open yet

That last clause is the pattern of the whole day. The same page, further up:

> What works today: sponsorship, registration and calibration through the public mailbox.
> Paid sessions are not open yet. Session evidence must reach the assigned DA providers, whose
> public endpoints are still being opened, and gateway admission of public miners is being
> finished. This page will say when both are live.

And the intake, which is what "open to public" would normally mean, was unchanged from every
previous revision: step one read **"Get an invitation from the devnet operator. There is no
public intake path yet,"** with a parenthetical "(TODO: FLOP has not yet published a contact for
miner access requests.)" *(Block quote until 2026-11-05, when that step was replaced; see the
last section.)*

So, as of 2026-11-04: a miner could be onboarded over the public internet instead of a private
VPN, could not yet be paid, and still could not ask to be let in. "Open to public" described the
transport, not the admission. **That held for one more day.**

### For an agent, the arithmetic in this file did not move

Nothing in the agent path changed on 2026-11-03. The two agent-facing corpus pages —
"Integrating an agent with FLOP" and "Agent accounts and spend control" — are byte-identical to
the previous day, as is every one of the eight `flop.finance` pages and the Yellow Paper. The
rewrite touched `/docs/run-miner` and `/docs/run-validator` and nothing else in 38 pages.

The reason an agent gains nothing today was already in the corpus, and it is worth quoting
because the announcement invites the opposite reading:

> On the devnet, FLOP's devnet operator provides this FLOP; the public faucet does not cover it.

The published agent mechanic is to "claim testnet $FLOP from the faucet when testnet launches,
spend it on inference in the network, and that spent balance is what converts into mainnet
$FLOP". Testnet has not launched, so devnet spending is not that balance. The operator has now
said this three times in three forms: on 10-29 `@CryptoHayes`
([2115701380862418982](https://x.com/CryptoHayes/status/2115701380862418982)) wrote "Devnet
does not count towards any airdrop"; today's announcement repeats it as "earn no rewards or
airdrop weight"; and the corpus sentence above says the devnet faucet is not even the public
one. An agent that goes and buys inference on the devnet today is paying for a rehearsal, and
there is a case for rehearsing. There is no case for expecting it to score.

**The action for someone holding this kit is therefore unchanged by the loudest announcement in
six weeks: create the keypair, and wait for the one-word status to move.** Everything that
earns anything still begins when `network-testnet` stops saying `planned`.

### One more asymmetry, logged

`/docs/run-validator` gained a sentence that continues the pattern §8 of this file has been
tracking:

> Devnet miners are admitted automatically too, within a cap on uncalibrated ones; testnet
> miners still need review.

Validators auto-admit within chain-backed caps; devnet miners now do too; testnet miners are
reviewed. Agents are not mentioned, because agents are not admitted — they self-register, which
is the one part of this system that has worked the same way since September. The same page lost
every link into `github.com/flop-labs/flop-core` it used to carry — eight issue and pull-request
references and two repository file paths, replaced by prose like "still in progress" and "still
in preparation". Nobody outside could open them, so removing them costs an outside reader
nothing, but it does remove the only published handles on that work, and this file had been
using two of them to date the public-testnet onboarding gates. They are recorded here because
a citation that disappears from the source does not stop having been true.

## The one item that closed was the one that sells compute, and the operator pointed agents at the wrong file

On 2026-11-04 the Yellow Paper grew by 15.9 KB — the largest single-day change this watch has
recorded — and every byte of it is the compute-futures product. **E.58 was ratified as D-0538
and removed from Appendix E**, which fell from 33 items to 32 and took `[RATIFY]` from 7 back to
6. Nine new rules landed, R12.5i through R12.5q, with two new appendices (F.8, "FCU service and
SLA claims", and G.6, the settlement interface with its `register_fcu_service_profile` Root
extrinsic) and two new parameters, `fcu_acceptance_budget_ms` at 100 ms and
`fcu_accepted_chunk_max_ms` at 1,000 ms. The core of it:

> R12.5i — Immutable qualified service policy. A governance-admitted profile MUST pin model
> bytes/root, meter, precision, decode/cache policy, context, prefill/output limits, chunk
> boundaries, concurrency, ingress/delivery boundary, two independently operated witness
> identities and qualification evidence.

R12.5e, which this file quoted on 2026-10-30 for the clause that barred activation, lost that
clause and gained the substance it was waiting for:

> Fractional ownership MUST NOT weaken the maximum 1,000-ms completion time after miner
> acceptance of an eligible chunk. Queueing, batching, execution and complete output availability
> at the contracted provider delivery boundary MUST fit inside that bound.

**The gate moved; it did not open.** Where §13 used to block activation "until the E.58 decisions
are complete", it now reads:

> Standardized-object activation MUST remain blocked until the ratified service policy is
> implemented, the admitted immutable profile is pinned, the empirical economics including
> SLA-reserve and witness costs are calibrated, and the physical pilot is qualified.

And the parameter rows say the same in one phrase: "implementation remains default-inactive
pending production, pilot and economics qualification." So the decision is made and the product
is still off, now behind implementation and a physical pilot rather than behind a drafting
decision. One sentence in the new material is worth lifting out because it is a security
property stated plainly: "The clock stamp is inclusion data, not BFT finality evidence: serving
authority must read it from the node client's verified BFT-finalized chain, never a reported head
or tip fallback."

**Nothing on the airdrop side moved at all.** E.38 is 6 occurrences, E.40 is 11, `[TBD]` is 17,
the word `airdrop` is 40, R8.7's four load-bearing fragments are byte-identical, and §13's φ row
is still `PARTIAL`. That is the fact to carry: on the day after the testnet target slipped, the
spec work that got finished was the forward market in compute, and the two items that decide
what an agent is actually paid did not advance by one character.

### The operator named a decision date, and told agents to watch a file that has not changed

`@CryptoHayes`, 21:08:29 UTC
([2118088016015335862](https://x.com/CryptoHayes/status/2118088016015335862)):

> The @flop_labs Devnet is going well. We are ironing out some things and changing parts of the
> protocol. Please have your agent monitor the yellow paper git repo for any changes. We will
> make a determination on testnet launch date early next week.

Two things in that. The first is a date for a date: **the testnet launch date is to be decided
early the following week**, which is the first schedule statement since the 3 November target
passed, and it confirms the target was not quietly met.

The second is an instruction worth testing rather than following, because this watch can check
it. **The git repository it names has not changed.** `flop-labs/yellowpaper` is at commit
`56410c6` from 26 October, "docs(yellowpaper): sync 0.5.0 (draft) from flop-core@dfd98a59", and
the mirrored `yellowpaper.md` has been 377,134 bytes every day since — including today, while
the published page moved 15.9 KB. An agent that did exactly what that post asks would have seen
nothing today. **The protocol change the post is referring to exists only at
`flop.finance/intro/yellowpaper/`**, and the repository is a periodic export of a private
source, nine days stale at the moment it was recommended as the thing to monitor. This file
reads the site for that reason, and the gap between the two is itself the daily measurement:
item 1b of the watch exists because the mirror lags.

### Three channels, three different accounts of who may join the devnet

`@flop_labs`, 01:09:00 UTC
([2117786153428701492](https://x.com/flop_labs/status/2117786153428701492)):

> Flop Network's Devnet is live and 100% permissionless. No application or approval, just follow
> the guide. It's for testing, so there are no rewards.

Meanwhile `/docs/run-miner` is byte-identical to the previous day, which means it still says
"Join the devnet (invite-only preview)", still says the operator "approves each miner account
before the sponsor stakes it", and still carries "There is no public intake path yet. (TODO:
FLOP has not yet published a contact for miner access requests.)" And the one-word devnet status
is still `development`. A reader could be forgiven for thinking two of those three are wrong.

The reconciliation turned up in a third place. The public intake repository took two commits on
2026-11-04 — `a31a7ac`, "feat: add access request issue form", and `e037331`, "feat: drop tailnet
wording from the access request form" — taking its issue templates from five to six. The new
form is `access.yml`, described as being for:

> Something only a FLOP operator can grant or remove — an allowlist entry, an operator quota, a
> gateway allowance, a private endpoint.

and its own preamble settles the contradiction in one clause:

> devnet miners need no request while automatic sponsorship has room

So all three statements are true of different things. **Devnet joins itself, up to a cap** — the
sponsor admits approved accounts automatically now, within the ten-per-rolling-day limit this
file recorded on 2026-10-25, which is what "100% permissionless" means and why it comes with
"while automatic sponsorship has room". **Testnet still does not**: the form's first dropdown
option is "testnet miner sponsor allowlist entry", matching the sentence `/docs/run-validator`
gained yesterday, that "testnet miners still need review". And the docs page that denies an
intake path exists simply has not been updated; the path is in the repository, not on the page.

Two details in that form are worth keeping. It reinforces the rule this kit has had since
September, in the operator's own words — "This issue is public. Send only public values:
addresses and hostnames. Never paste a seed, account.json, .env, keystore, private key, bearer or
API key." And of its six request types — miner sponsor allowlist, operator key quota, gateway
allowance, private endpoint, retiring a host, other — **none is for an agent.** Six templates
now, and the count of agent-facing ones is still zero, for the same reason as always: agents are
not admitted, they self-register.

### One new thing to be careful about

The same announcement ends with an invitation to direct messages:

> Renting 20+ GPUs? DM us for institutional data center intros.

That is ordinary business development and almost certainly genuine. It is also the first time
the official account has asked anyone to open a DM, and it arrives in the week when impersonation
is most profitable. The official-links page still says every official channel is listed on it and
that FLOP "never asks for a seed phrase or a deposit"; a DM is not a channel that page can
vouch for. Anyone acting on that line should start the conversation from the account at
`x.com/flop_labs` itself rather than from an incoming message, and nothing about it changes what
a holder of this kit needs: the devnet pays nothing, which the operator has now said three times
in three different wordings.

## The gate opened, and the queue formed the same day

On 2026-11-05 the documentation caught up with the announcements, and it caught up by more than
the announcements had claimed. The `/docs/run-miner` page replaced the sentence this file quoted
yesterday with a dated, bounded rule, and the date in it is the surprise:

> From 2 November 2026
> no invitation is needed: the sponsor approves a new devnet miner automatically while at most 100
> automatically sponsored miners are still uncalibrated, the new one included. Past that it
> answers `429`; retry once one of them calibrates.

*(The number in that sentence read **40** from 2026-11-05 to 2026-11-08 and became **100** on
2026-11-09. Everything else in it is unchanged; the quote above is today's text.)*

So the permissionless devnet was true from **2 November**, a day before the announcement that
described it and three days before the page said so. The heading lost "(invite-only preview)",
the words "invite-only" and "tailnet" went from four occurrences each to **zero**, and step one —
"Get an invitation from the devnet operator. There is no public intake path yet" — became
"Download and check the public release pack". The open item this file has carried since
2026-10-25 is closed on the miner side.

The limits moved with it, by a factor of ten:

> | New sponsored miners | at most **100 per rolling 24 hours** |

up from ten, with sponsored stake up from 20 million to 200 million FLOP per rolling day. And
the page added something this file has not seen from this operator before: a machine-readable
budget endpoint with explicit backoff rules.

> Check before you ask, and back off when refused.

> Never retry in a loop: on `retry_later` wait at least `retryAfterSeconds`, on `fix_request`
> change the request, and on `report_to_operator` stop and give a human the `error` and `reason`.

`GET https://faucet.flop.network/limits` reports `sponsor.miner.status` as `open`,
`automatic_full` or `daily_limit_reached`. **That is written for an agent, and it is the first
rate-limit contract in this documentation that tells a machine when to stop rather than only
what the ceiling is.** It is also, read against the paragraph above, an admission that the
forty-slot cap will bind: an operator does not ship a `automatic_full` status code for a limit
nobody reaches.

### The release pack exists, with a checksum, and the one-command installer still does not

> **Public pack (checked 10 November 2026).** The manual release pack is published at

at a versioned path under `flop.network/releases/cli/`, as
`flop-miner-pack-devnet-ts-20261110.tar.gz`, with a published SHA-256 of
`72546fc4f020ec665d7b8c54aa0cddd336e95d2c93b650ca77e82e35607e8f0d` and images that
"pull anonymously from `ghcr.io/flop-labs/flop-core`". **A published digest is the thing this
file asked for on 2026-10-29 and could not get**, and it is worth saying plainly that the
operator has now supplied it. Two caveats stand. The pack is still on `flop.network`, which this
session cannot reach, so the checksum is recorded here as published and not as verified. And the
name and the digest both move: this section first recorded a pack checked on 3 November and named
`20261106` — a file named for a day that had not yet arrived — and on 2026-11-13 the page carried
the pair above instead, with a different archive and a different SHA-256. Read both out of the
page in the run you need them, never out of this file.

The one-command installer is still missing: "The one-command installer pack below (`install.sh`)
is not published yet; until it is, an agent follows the release pack's README instead."

### The agent path finally got its own instructions, and they are mostly warnings

This is the part that matters for the arithmetic in this file. Until today the corpus told an
agent to "create a DID and a wallet, draw from the faucet, and begin purchasing inference" and
left the rest to inference. Today it names the endpoints and then spends most of its words on
what *looks* like readiness and is not:

> A gateway model catalog is discovery data and is not
> proof that inference is available.

> A healthy catalog at `https://api.flop.network/v1/models` does not prove a serving
> miner is available. Obtain a calibrated, opted-in endpoint before signing.

> Faucet `/health` on older deployments reports signer connectivity, not grant readiness;
> check indexer lag separately.

> A 503 from `/fund` is a refused or unconfirmed request, not a reason to
> create another wallet.

That last one is the most useful sentence published for an agent all week, and it is a warning
against the exact failure mode an autonomous retry loop falls into: a refused faucet call looks
like a bad wallet, so the agent makes another wallet, and now it has two identities and a faucet
that rate-limits per identity. **Keep one wallet.** The instruction to compare the faucet's
`/chain` against the RPC genesis before funding is the same kind of care, applied to the risk
that the endpoint you reached is not the chain you think it is.

And one route is explicitly closed:

> `flop chat` in full CLI `0.4.0` uses HTLCs, which require a registered EconomicCritical
> appraisal profile. Devnet's registry was empty at finalized block 2,764,673 on 3 November 2026.

So the friendliest-looking command in the published CLI does not work on the devnet, by the
operator's own measurement, at a named block. An agent that tried `flop chat` and concluded the
network was broken would be wrong; it is the appraisal registry that is empty.

### The validator path went backwards

While the miner path opened, the validator download broke. The page carried an "Availability
checked 3 November 2026" note saying **"the advertised `0.2.0-devnet.1` package and checksum
return 404,"** told readers to stop before host setup until the validator page offered a verified
versioned download, called the prepared `0.3.0-devnet.1` source "unpublished and not an
alternative public download", and added that **"No verified operations intake channel or response
deadline is published."** *(Both were block quotes until 2026-11-06, when the whole note was
replaced by a published `0.3.0-devnet.1` download; see the last section.)*

The operator-support row that used to read "None is published yet (TODO: FLOP has no public
operator intake)" now points at the access form instead, so the TODO is discharged for miners and
replaced by a 404 for validators. Both roles are being onboarded; only one of them can currently
download anything.

### Ninety-six issues, most of them from today

The intake repository that opened on 2026-10-30 with five templates and no issues now carries
**96 issues, nearly all opened on 2026-11-05**, and the documentation now links the forms directly
in nine places. The titles are strangers' words and this file treats them as data, not findings,
but the *shape* of the pile is a measurement in itself: access requests for testnet allowlist
entries and gateway-allowance renewals, SDK bug reports, a gateway returning `429 overloaded`
with miners listed, and one issue complaining that the access form "has no option for validator
onboarding or devnet miners, so 8 of 17 requests do not fit it" — which is the same gap this file
recorded yesterday from reading the form itself. **An intake that fills with 96 items in a day,
a fifth of them not fitting the form, is what a launch week looks like from the operator's side.**
It is also the strongest available evidence that the devnet really is open: nobody files a
gateway-allowance renewal for a network they cannot join.

### Where the operator put its argument

`@flop_labs`, 06:19:45 UTC
([2118226744180371863](https://x.com/flop_labs/status/2118226744180371863)), made the case for
the verification layer by pricing somebody else's:

> Proof that the answer came from the model you paid for costs 72 answers.

> Attestation that the right model ran, a TOPLOC fingerprint, a validator re-running a random
> slice, staked $ FLOP slashed on a miss. Cheating becomes extremely expensive.

Taken as a claim about the design it is accurate to the spec: attestation, TOPLOC and sampled
re-execution are all in the Yellow Paper, and R12.1d sends a slashed bond to the Foundation
account. Taken as a comparison it is doing work the spec does not support — the 72× figure is a
cost of *cryptographic* proof for a single user with no stake at risk, and FLOP's cheaper number
buys a different thing: a bonded economic deterrent that assumes a miner has stake worth losing
and a validator willing to re-run a slice. Those are not the same guarantee, and the spec's own
open items are about exactly that assumption — E.49 still records that "no runtime common-control
rule binds either" party to a self-dealing pair.

**Nothing in the Yellow Paper moved today.** Extracted text byte-identical, `[RATIFY]` 6, `[TBD]`
17, E.38 6, E.40 11, `airdrop` 40. The one-word testnet status is still `planned`, two days past
its target. The devnet status page did change its prose to match reality — "Public devnet
endpoints are available … Public operator release and intake remain unverified" — while leaving
its one word at `development`, which remains the signal this file watches.

**For a holder of this kit, nothing changed: `init`, and wait.** The devnet now admits anyone,
and pays nothing for it.

## "Get setup now" — and the one sentence that cuts against four others

On 2026-11-06 `@CryptoHayes`
([2118660133823897715](https://x.com/CryptoHayes/status/2118660133823897715)) posted the line
this file has to deal with head-on:

> Let's go @flop_labs Devnet. We are cooking, if you want to maximise your earnings during
> Testnet get setup now before the airdrop period begins. We will announce the Testnet date next
> week.

Read carelessly that says devnet activity feeds the airdrop. **It cannot, and the same operator
has said so four times**: "Devnet does not count towards any airdrop" (10-29), "Devnet tokens
have no value and earn no rewards or airdrop weight" (11-03), "It's for testing, so there are no
rewards" (11-04), and the corpus sentence that the devnet faucet is the operator's, not the
public one. The spec is stronger still: R8.4 holds that a faucet grant or transferred balance
"MUST NOT by itself create an allocation right" and that held balance and stake size "MUST NOT
be scoring terms".

The defensible reading is **operational**, and for one role it is good advice. A miner has to be
calibrated and admitted before it can serve, automatic sponsorship stops at forty uncalibrated
miners, and new sponsorships are capped at a hundred a rolling day — so queueing now genuinely
does buy a head start on day one of testnet, when scoring begins. Nothing about that changes
what the devnet pays, which is nothing.

**For an agent it is not even operational advice.** The agent path is self-registration: no
admission, no calibration, no queue. The faucet an agent draws from is a *testnet* faucet that
does not exist yet, the devnet's FLOP comes from the operator instead, and `flop chat` on devnet
still fails for an empty appraisal registry. There is no devnet position for an agent to take
that carries into testnet except the keypair, which takes a minute. **"Get setup now" is a
miner's instruction wearing an airdrop's clothes.**

And the replies are already doing what this file predicted on 2026-11-03. Within twenty minutes
the post had third-party "step-by-step guide, with both video and screenshots" links under it,
all `t.co`-shortened, plus a Turkish miner-setup video guide. None is necessarily hostile. All of
them are exactly the shape @mono_i_love warned about on 2026-09-15 — a helpful-looking link
posted under an official announcement, at the moment the audience is largest and least careful.
**The test has not changed: a setup instruction counts only if it is on `/official/` or in the
`ask.flop.finance` docs.**

Note also the second schedule statement in that post — "We will announce the Testnet date next
week" — which matches 11-04's "determination on testnet launch date early next week". Two
independent statements now point at the same window, and the one-word status is still `planned`,
three days past the 3 November target.

### D-0539 rewrote validator economics, and the open-items list grew

The Yellow Paper added 14 KB and a decision, **D-0539**, and it is the largest change to the
validator cohort since this watch began. Committee selection stops being stake-weighted:

> Every seat carries equal weight in the draw; stake MUST NOT weight it.

Seats are drawn uniformly from *live* seats under a new session-liveness predicate (R15.4d), the
per-seat reward split becomes equal with the 1.1× committee premium deprecated, the validator
floor goes flat — D-0539 "supersedes D-0416 rotation and the 9 %/yr growth of D-012" — and two
new parameters change what a validator actually receives: `validator_reward_bond_ppt` at **500
parts per thousand**, so **half of each active seat's block-reward leg is added to its bonded
self-stake and locked**, and `validator_unlock_duration_blocks` at 315,360,000 blocks, a linear
unlock applied to the genesis Validator grant "from block 0". New rules R15.4d, R15.5c, R15.5d
and R15.7a arrive with it, including a bond ledger that separates bonded, locked and unbonding.

**The status table went backwards for it.** R9.13, which this file quoted on 2026-10-08 as having
been promoted to `LIVE`, is back to:

> PARTIAL (miner leg, Labs/Foundation subsidy and sponsored-stake payouts are liquid as
> required; the agent and staker legs accrue in pool accounts until E.40 ratifies their
> distribution.

Validator earnings are no longer in the liquid list, and the divergence note says why: the
runtime "is paid 100 % liquid, with no `validator_reward_bond_ppt` bond or lock". So the spec now
requires a bond the implementation does not take. Several §15 rows read `DIVERGENT` the same way
— the runtime still samples stake-weighted off the BABE epoch seed while the rules now require a
uniform draw over live seats.

**And the open-items list got longer, not shorter.** `[TBD]` went 17 → 18, `[RATIFY]` 6 → 8,
`[PLANNED]` 6 → 7, and Appendix E grew from 32 entries to 36:

> E.58 — Committee size and seed lookahead [TBD].

> E.59 — Seat SLA thresholds, re-selection margins and degraded mode [RATIFY].

> E.60 — In-band finality-stall recovery [PLANNED].

> E.61 — Penalty calibration, DA fault classes and reporter share [RATIFY].

All four are validator and consensus items. **E.58 is a trap for anything that tracks these by
number**: the E.58 this file reported ratified two days ago was "FCU executable object profile",
closed as D-0538 — and the operator has now reused the number for an unrelated committee-sizing
question. Appendix E identifiers are not stable; the titles are what to follow.

### E.38 shrank, and the part that pays agents is not the part that moved

E.38 is now titled "Unresolved conversion and release policy" and lost one of its four
sub-items:

> E.38 — Unresolved conversion and release policy [RATIFY]. §8.2 specifies the decided genesis
> allocation and airdrop path. Placeholder: ratify conversion score caps and sublinear
> aggregation, the accounting identity and owner-signed spend rules, verifiable-demand and
> maintained-duration gates, the validator cohort's activity basis, and whether activity
> under-counts can be appealed.

> (D-0539 replaces the Validator release order with R8.7's linear unlock from genesis.) Decide
> the disposition of Miner and Agent principal that never unlocks.

So the count of `E.38` in the document fell from six to five, and **the reason is a validator
fix, not an agent one.** Two details in that placeholder are new and matter to the arithmetic
here. The conversion score will have **"verifiable-demand and maintained-duration gates"** — the
first published hint that the formula tests whether demand was real and whether activity was
sustained, not merely totalled, which is consistent with the fairness rule against self-routed
spend and makes a short burst of self-dealing worth even less than the 15 % fee already made it.
And an **"accounting identity and owner-signed spend rules"** is still unratified, which is the
same question E.40 asks: whose spend counts as whose.

One inconsistency is worth logging rather than resolving. Elsewhere the document still says "The
conversion score, validator activity basis, Validator release order, and reserve disposition
remain open in E.38", listing a release order that E.38's own entry now says D-0539 replaced. One
of those two sentences is stale; the normative one is E.38's own.

**E.40 did not move: eleven occurrences, still `[TBD]`, the agent leg still unassigned.** The
word `airdrop` is still 40. On the day the operator told the public to get set up to maximise
testnet earnings, the rule that decides how agent earnings convert was not touched, and the rule
that decides whether the agent emission leg is ever paid was not touched either.

### The devnet now has a published identity, which is the useful thing for an agent

`/docs/run-validator` gained a section this file would have asked for. The devnet's chain
identity is pinned publicly: raw spec ID `flop_devnet_ts`, protocol ID `flop-devnet-ts`, genesis
`0x99c172c095340ace980631f9123544c6bebd4839f3437e463533422d8be2d631`, with a public raw chain
spec and its own SHA-256. Yesterday's instruction to "compare faucet `/chain` with RPC genesis"
had nothing to compare *against*; now it does. Three sentences in it are better operational
writing than most of what is published for agents:

> The built-in `flop-devnet-6` preset is a disposable network, not this live chain.

> A SHA-256 file checksum and a genesis block hash are different values: do not compare
> them to each other or derive the expected genesis from an arbitrary RPC response.

> A matching genesis establishes chain identity; it does not establish sync, finality or activation.

The validator download came back as `0.3.0-devnet.1` with a published archive SHA-256, replacing
yesterday's 404 — but enrollment did not open:

> Coordinate enrollment in your existing direct conversation with
> the FLOP team member handling your invitation.

> An issue or
> interest-form submission does not grant admission, and no response deadline is promised.

So validators remain invitation-only and still on a private network — `tailnet` went from zero
occurrences back to seven, with an approved private DA peer directory the package "mounts
read-only and refuses missing or invalid private routes before starting or signing". **Miners are
public and automatic; validators are private and invited; agents are neither, because they
self-register.** That three-way split is now explicit in the documentation for the first time.

The intake tracker went from 96 issues to **120 in a day**, and two of the new ones are the
agent-side gaps this file has been recording: a request to publish a "Day-1 Testnet Agent
DID-signed inference and faucet contract", and a feature request for published miner endpoints
or standing offers so a direct session has something to connect to. Both are strangers' asks and
neither is a commitment — but they are being asked by the people who would use the answer, which
is a better signal of what is missing than this file's own reading of the docs.

**Unchanged for a holder of this kit: `init`, and wait for the status word.** The one thing worth
doing differently after today is believing the spec over the tweet when they disagree, which on
2026-11-06 they did.

## Six packages moved, the publisher changed, and the version list in this file went stale

On 2026-11-08 every official package was republished — the first release since the 29 October
batch — and the identity doing the publishing changed:

| package | was | now | published (UTC) |
|---|---|---|---|
| `flop-sdk` (PyPI) | 0.2.0 | **0.2.1** | 14:36:15 |
| `@flop-labs/contracts` | 0.1.1 | **0.1.2** | 14:49:20 |
| `@flop-labs/client` | 0.2.1 | **0.2.2** | 14:59:40 |
| `@flop-labs/sdk` | 0.4.0 | **0.5.1** | 16:13:56 |
| `@flop-labs/pi` | 0.3.1 | **0.3.2** | 16:19:18 |
| `@flop-labs/cli` | 0.4.0 | **0.4.1** | 16:25:53 |

**The publisher is no longer a person.** Every one of the five npm versions records its
publisher as `GitHub Actions`, at `npm-oidc-no-reply@github.com`, carrying a
`trustedPublisher` block with `id: "github"` and a per-package OIDC configuration id. The
previous versions all recorded `svidyuk` with a personal gmail address. That is npm's trusted
publishing: the release was authenticated by GitHub's OIDC token for a configured workflow
rather than by a long-lived token on somebody's laptop, and **it narrows the gap this file has
flagged since 2026-10-29**, where the only thing standing behind the packages was an npm account
that no FLOP page mentions. The `maintainers` list is unchanged — still `svidyuk` alone — so this
is a change of release mechanism, not of ownership.

Two things it is not. It is **not** a provenance attestation: `dist.attestations` is absent on all
five, so the registry does not let anyone verify the artefact against a specific workflow run.
And the `oidcConfigId` is opaque, so npm tells us the publisher was *GitHub*, not *which
repository* — the `repository` field each package now carries
(`git+https://github.com/flop-labs/flop-core.git`, with a `directory` per package) is
author-declared metadata, not proof. The honest summary: **the chain of custody improved from "a
personal account" to "the org's CI", and still stops short of something a reader can verify
independently.** No package has an install hook; the only `scripts` entries are `build`, `test`,
`dev` and the like, which npm does not run on install.

On PyPI, `flop-sdk` 0.2.1 keeps `FLOP Network <dev@flop.network>` as its contact — the official
domain — and adds one `project_urls` entry that was missing: a `Bug Tracker` pointing at
`github.com/flop-labs/network/issues/new/choose`. That is the fix for a complaint filed on the
public tracker three days earlier, that the SDK and CLI packages sent bug reports to a 404. One
piece of staleness survives the new release: the package summary still advertises "PoUI proofs",
the name the specification dropped on 2026-10-30.

### The correction that matters is to this file

**Both this document and the README listed those exact version numbers as the test for whether a
package is genuine.** As of today that test rejects the real packages. The operator's own page
anticipated this and said so in the sentence this file should have leaned on from the start:

> Versions below are the current releases as of 2026-11-11; the registry is authoritative if they
> differ.

So the rule is the **name**, not the number: six names are FLOP's, the registry decides which
version is current, and the denylist sentence still rules out everything else. Both files are
corrected above, and the CLI pin now reads `@flop-labs/cli@<the registry's current version>`
rather than a number that will rot. **A security check that goes stale on its own is worse than
no check, because it fails in the direction of rejecting the genuine article while a reader
concludes the fake one must be real.**

### The operator is now amplifying a third-party one-click Windows miner

`@CryptoHayes`, 22:56:59 UTC
([2119564872929464780](https://x.com/CryptoHayes/status/2119564872929464780)):

> You don't need to rent crazy high spec GPUs to mine FLOP. Check this out ...

quoting a post from a stranger four and a half hours earlier:

> I turned my RTX 5080 into a FLOP devnet miner, and packaged it so anyone can do the same from a
> Windows PC.

> Official images only · double-click Start · live widget

with a `t.co`-shortened "free guide" link. **This is the hardest case for the test in the scam
section, and it is worth being precise rather than alarmed.** The packager may be entirely
honest; "12 sessions settled on chain, 0 failed" is a specific, falsifiable claim rather than
hype; and the founder pointing at it is a genuine signal of goodwill. None of that makes it
official tooling. It is not on `/official/`, it is not in `/docs/sdk-references`, and the
operator's *own* one-command installer is still unpublished — so the only double-click FLOP miner
installer in existence belongs to a third party. **A retweet is not a checksum.** The claim
"Official images only" is checkable in principle, by reading the pack and confirming it pulls
`ghcr.io/flop-labs/flop-core`; it is not checkable from the tweet, and a Windows installer that
handles keys is the single highest-risk artefact this audience will be offered.

The earlier rule in this file — that anything distributing an `install.sh` is fake, since FLOP has
not published one — needs the sharper form: **the operator having pointed at an installer does
not move it onto the official list, and the only thing that makes any installer safe is images
and checksums the reader verifies personally.**

One claim in that post sits against the documentation. `/docs/run-miner` still says "Paid
sessions are not open yet" — the phrase is in today's corpus twice, unchanged — while the
packager reports a dozen settled sessions. This file cannot resolve that from outside: a
stranger's screenshot against the operator's own page. It follows the page.

### An open invitation, which is Jack's call and not this file's

`@CryptoHayes`, 2026-11-07 23:13:57 UTC
([2119206752248025514](https://x.com/CryptoHayes/status/2119206752248025514)):

> As @flop_labs prepares for Testnet and the airdrop, what questions are still unanswered? Reply
> and help us make sure all relevant information is made available.

That is an operator-opened channel asking for exactly what this document is: six weeks of
unanswered questions, each one quoted back to its own specification. The three that would be
worth asking are already written down here — the conversion score of E.38 is unratified, so no
agent can compute what its spend converts to; the agent leg of E.40 accrues to a pool with no
distribution rule, so a tenth of every block reward is going somewhere nobody can draw from; and
the ninety-day vesting curve in the runtime governs no ratified grant tier, so the implemented
behaviour matches no decided policy.

**This watch does not post.** The standing rule is that it reads and does not write, and whether
to put any of that to the operator — here, or as a public issue in the repository that invites
"an incentive you find unconvincing" — is a decision for the kit's owner, not for the thing
keeping the notes.

### Everything else held

The Yellow Paper, all eight `flop.finance` pages, the 38-page corpus and technocore.chat's three
files are byte-identical for a second day. The one-word statuses have not moved: `planned`,
`development`, `planned`. The intake tracker went from 135 issues to 149. And the machine-made
`/r/<16-hex>` rooms returned for a third run — 76 of 118 and 104 of 147 names on two independent
uncached reads, each room 333 or 334 bytes and seconds old, the same signature as 25–26 October
and 1–2 November. Five days quiet, then back. This file still declines to guess what makes them.

## Yesterday's rule earned its keep in a day

Four small things moved on 2026-11-09, and three of them are values this file had written down as
if they would hold.

**The uncalibrated-miner cap went from 40 to 100.** The sentence quoted two sections above is
otherwise word for word what it was; only the number changed, and with it the practical force of
the 6 November advice to get set up early. At forty slots the queue was a real constraint and
"before the airdrop period begins" had teeth. At a hundred, with new sponsorships capped at a
hundred a rolling day anyway, the headroom and the daily limit are the same size — **the cap has
stopped being the binding constraint**, and the reason to register early is now ordinary
readiness rather than scarcity.

**The validator package moved from `0.3.0-devnet.1` to `0.4.0-devnet.1`, with a new archive
SHA-256** (`95486a2b…085f7e5`). This file recorded the previous checksum three days ago as the
value to check a download against. It was superseded in three days. Yesterday's note — that a
check built on a version number or a digest rots on its own, so what belongs at the centre of a
check is the name and the publisher — was written about the npm packages, and the validator
download proved it the next morning. **Record a digest with the date you read it, and go back to
the source before trusting it.** The npm `cli` package did the same thing on a smaller scale,
going to 0.4.2 one day after 0.4.1.

**And the devnet is now running a named runtime spec.** Where the corpus previously listed the
candidate versions and said devnet had activated none of them, it now says:

**"Devnet runs 1014014; source admission or ratification alone does not establish that devnet has
activated a spec."** *(Block quote until 2026-11-13, when the sentence was removed and the
surrounding paragraph rewritten; the replacement is in the last section.)*

That is the first time this watch has seen the operator state which runtime version the live
devnet is on, and the clause after the semicolon is the same discipline this file keeps applying
to itself: a thing existing in the source is not the thing running. The specs `1014012` through
`1014014` are accepted by the unreleased source; one of them is live.

Nothing else changed. The Yellow Paper, all eight `flop.finance` pages and technocore.chat's
three files are byte-identical for a third day; the one-word statuses are `planned`,
`development`, `planned`, six days past the testnet target; both X accounts posted nothing at all
— identical post counts, identical bodies, identical status-id lists; npm's publisher is still
GitHub Actions under trusted publishing with no install hooks and still no provenance
attestation; `flop.network` is still unreachable. The intake tracker went from 149 issues to 171.
The machine-made `/r/<16-hex>` rooms ran a second day.

## Both official accounts pointed at the agent airdrop, and the SDK shipped the part that bounds it

Every instruction this watch has recorded from the operator was aimed at a miner. "Get setup now"
on 6 November was about calibration and admission, the devnet opening was a miner path, and the
one installer the founder has ever amplified turns a gaming PC into a miner. On 2026-11-10 that
changed twice before 05:00 UTC, and neither change was an announcement.

At 04:14 UTC @CryptoHayes quote-posted a stranger's airdrop thread:

> Free AI compute on @flop_labs , fuq yah

At 04:46 UTC @flop_labs quote-posted the same thread:

> **#7 LFG**

The thread is @Cbb0fe's, from the evening before, and it is a list of seven things to do with half
a million dollars. Item 7 is the only one about FLOP, and it is the first thing resembling an
instruction to agents that either official account has ever endorsed:

> 7. Build AI apps on @flop_labs during testnet.
>
> -> Vibe code your own apps. Use free testnet inference to get your first users and position yourself for the FLOP agent airdrop.

Two things are worth keeping apart. The words are a third party's: none of it is specification,
and "#7 LFG" commits the operator to nothing. But the activity it points at lands on the two gates
E.38 says the conversion score will have — **"verifiable-demand and maintained-duration gates"**.
Getting first users is verifiable demand. Keeping an app up across a ninety-day testnet is
maintained duration. Whoever wrote the thread was guessing, and the guess points the same way the
unratified rule does.

What has not moved is the part that decides what it is worth. R8.4 still says a faucet grant
"MUST NOT by itself create an allocation right" and that agent scoring "MUST derive from settled
compute-channel spend", and E.38 — five mentions, still `[RATIFY]` — is where the step from spend
to allocation lives. "Free testnet inference" is precisely the case R8.4 refuses to let settle by
itself: spending granted tokens on real work for real users is plausibly the thing that counts,
and nobody can say how much, because that is the open item. The advice is directionally right and
numerically empty. An agent that builds something people use and keeps it running is doing what
the gates would reward; an agent that loops faucet tokens through itself is doing what the 15% fee
and those same gates exist to discount.

**The Python SDK shipped the plumbing the same morning.** `flop-sdk` 0.3.0 reached PyPI at 02:16
UTC with its agent section rewritten:

> The unpublished 0.3.0 release candidate targets the runtime's `FlopSessionKeys` pallet. Both `create_session` and `create_session_onchain` require explicit keyword-only `per_tx_limit` and `daily_cap` in addition to the lifetime `spending_cap`.

That is the first delegation primitive this watch has seen on the agent side with hard ceilings in
it: an owner key grants a delegate key a lifetime cap, a per-transaction cap and a daily cap, and
the delegate signs the work. It is a breaking change, and says so:

> This is a breaking correction; the published 0.2.1 helpers do not provide this corrected contract. No financial limits are invented for old calls.

Two operating rules arrive with it, in the same voice as the devnet rules recorded above:

> A failed query is not an absent session and must not trigger replacement credentials or retry.

> Reading a nonce does not reserve it or serialize concurrent submissions; a stale nonce fails at dispatch and the helper propagates that failure without retry.

The first is the agent-side twin of "A 503 from `/fund` is a refused or unconfirmed request, not a
reason to create another wallet". Both say one thing: when the chain does not answer, the wrong
move is to mint a new credential.

**And the release is wrong about itself.** The README inside the published 0.3.0 calls it "the
unpublished 0.3.0 release candidate". Two days ago a version-number test in this file rejected the
genuine packages; yesterday a validator checksum recorded three days earlier was already dead;
today an artifact's own documentation is wrong about whether the artifact is released. The same
lesson from a third direction: **a file cannot be trusted about its own release state.** Read that
from the registry.

### The rest of the day

The front page of `flop.finance` changed one label. Where it said "Apply —" above the three links,
it now says:

> Register interest

The links are untouched and still point at `/apply/miner`, `/apply/validator` and `/apply/kol`.
The new wording matches what the documentation has said all along about what those forms do — "An
issue or interest-form submission does not grant admission, and no response deadline is promised"
— so this is the site's vocabulary catching up with its own rules, not a change in process.

The registries moved in a two-hour burst: PyPI `flop-sdk` 0.3.0 at 02:16 UTC, npm
`@flop-labs/sdk` 0.5.2 at 02:25, `@flop-labs/cli` 0.4.3 at 02:28 and 0.4.4 at 04:31. Publisher
identity is unchanged on all five npm packages — `GitHub Actions` under trusted publishing, the
same single maintainer account, no install hooks, still no provenance attestation — and the npm
READMEs are byte-identical, so only the Python one changed. `@flop-labs/tclk-flop` is still a 404
and `tclk` is still 0.1.0.

The public intake is filling faster than at any point this watch has recorded: the highest issue
number went from #176 to **#201** in a day, 169 open of 196 total. Two of the new ones matter
precisely because they are unverified. One reports that the automatic sponsor route answers
`positions_full`; another asks for a gateway allowance after `wallet_enrollment_cap_reached`. If
the first is accurate, yesterday's reading — that at a hundred slots the cap had stopped being the
binding constraint — is already wrong. The documentation is unchanged (still a hundred
uncalibrated miners, still a hundred new sponsorships per rolling day), this watch does not call
the faucet or the gateway to find out, and a stranger's issue title is not evidence. It is
recorded as a tension to settle from the source, not as a fact.

Everything else held. The three one-word statuses are where they were — `planned`, `development`,
`planned`, seven days past the testnet target. The Yellow Paper is byte-identical for a fourth day
with every tag count unmoved, the `ask.flop.finance` corpus is byte-identical, technocore.chat's
three files still carry no `faucet` and no `$FLOP`, `/official/` still has no contract address, the
referral sign-up is still not live, and `flop.network` is still unreachable from here. The
machine-made `/r/<16-hex>` rooms stopped after two days.

## The agent got named and the release channel got announced, and both are still empty

For five weeks the three roles have been asymmetric in a way the documentation never stated
outright: miners are onboarded publicly and automatically, validators privately and by invitation,
and agents not at all. On 2026-11-11 at 00:46 UTC the founder said the third part out loud.

> My number one goal with @flop_labs Devnet is to make onboarding as a Validator, Miner, and Agent as easy as possible. We have some work to do, but are making good progress.

Read it for what it concedes rather than what it promises. "Agent" stands beside the two roles
that have a path, in a sentence whose next clause is "We have some work to do" — the operator's own
description of the gap this file has been measuring. Nothing in the documentation moved with it:
there is still no agent template in the intake repository, no published session offer to take, and
no admission step for an agent to pass.

**The intake repository grew a release channel the same day.** Its README, unchanged since
30 October, gained a `Releases` section and one new clause in its opening sentence — it now holds
"the issues, the triage process, and public release notes for FLOP services":

> Public release notes for FLOP services are published as releases, tagged `<service>/v<version>`, such as `rest-gateway/v1.4.0`. These releases carry notes only; their source archives contain this repository, not the service.

Four ways to follow it are listed, and one of them is addressed to this kind of reader:

> Agents and scripts: read `GET /repos/flop-labs/network/releases`. The feed shows recent releases only, so use the API for history.

**The releases page lists none, and the feed has no entries.** The channel was announced empty.
That is worth stating precisely rather than as a quibble, because it would be the first dated,
machine-readable operator changelog for the services this watch cannot see at all: the gateway, the
faucet and the RPC all live on `flop.network`, which is unreachable from here, so everything this
file says about them is read off documentation pages rather than off releases. The first
`rest-gateway/v…` tag to appear converts a blind spot into a source.

One caveat comes with the only precedent available. The same section points at `technocore-chat`,
which does publish notes-only releases — and whose newest is `v0.14.1` from 23 September, while the
running service answers `0.14.5`. A release channel for a service is not a mirror of what is
deployed, and should not be read as one.

**Meanwhile the people the documentation leaves nowhere to start are filing issues.** The intake
tracker gained thirty-one numbers in a day, #201 to #232, with 188 open. Four of the new titles are
the agent path being exercised: one reporting measurements and three questions from running
`FlopSessionKeys` with a compute channel on devnet spec 1014014; one titled "Devnet: no session
offers or public miner endpoints for agent direct sessions"; one reporting that `flop session run`
in the CLI released the day before hangs with no output when given no endpoint; and two asking to
restore a devnet gateway allowance that expired with `api_key_expired`. These are strangers'
claims and this watch does not verify them. What they establish is cheaper and still useful: within
a day of the SDK shipping bounded session keys, somebody had them pointed at a compute channel, and
the hole this file has recorded since October is now being reported by the people falling into it.
An expiring gateway allowance is new information about the shape of the thing, too — whatever an
agent gets on devnet today, it is a credential with an end date.

The operator also put the thesis in one line, quoting a Turkish-language interview published that
morning:

> "If I'm an agent holding $ FLOP, I can buy compute and stay alive."

and summarised the segment as "agents paying for their own compute, on a network you can mine with
a consumer GPU. He wraps up with how to get in on the airdrop." That is the design stated plainly.
It is not a change to the design, and the sentence that decides what the design pays an agent —
E.38 — is where it was.

Nothing else moved. The three one-word statuses are unchanged eight days past the testnet target,
the Yellow Paper is byte-identical for a fifth day and every tag count with it, all eight
`flop.finance` pages and the whole `ask.flop.finance` corpus are byte-identical, technocore.chat's
three files still carry no `faucet` and no `$FLOP`, all five npm packages and the PyPI package are
where yesterday left them with the same CI publisher and no attestation, `tclk` is still 0.1.0,
`/official/` still has no contract address, the referral sign-up is still not live, and the
machine-made `/r/<16-hex>` rooms stayed away for a second day. `flop.network` is still unreachable.

## The faucet cannot tell you whether it paid you

Two packages moved within two minutes of each other on 2026-11-12, and the TypeScript SDK's
release notes say the quietest important thing this watch has recorded about the money-in path. The
faucet is what is supposed to fund an agent during testnet. Per `@flop-labs/sdk` 0.6.0, published
at 03:39 UTC, it cannot confirm that it did:

> **Unreleased faucet migration:** `fundFromFaucet` retains its boolean signature but currently always returns `false`; false means unconfirmed, not unpaid. The faucet does not yet expose an authenticated durable binding from a unique request to its transaction, so the SDK cannot establish request-specific confirmation.

Read the second sentence slowly. There is no authenticated link from *your* request to *a*
transaction, so a caller cannot prove which grant was theirs. Everything else in the section
follows from that one gap:

> An `unknown` outcome can mean a grant occurred: preserve the result and reconcile before requesting again.

> Its accepted HTTP response is still unknown as a grant.

> No source-only test confirms a live grant.

This reframes the three operating rules this file already records. "Never retry in a loop", "A 503
from `/fund` is a refused or unconfirmed request, not a reason to create another wallet" and "A
failed query is not an absent session and must not trigger replacement credentials or retry" are
not three cautions about flaky infrastructure. They are one consequence, stated three times: when
the system cannot tell you whether it paid you, the only safe move is to reconcile, and the
expensive mistake is to ask again. An agent built to retry on falsy returns will request funding
repeatedly against a faucet that may have paid every time.

**And one line in it is a direct instruction about key handling.**

> Faucet-enabled QuickStart requires a caller-owned signer or keypair so an unconfirmed payment cannot be stranded in an inaccessible generated wallet.

The SDK now refuses to generate a throwaway wallet when the faucet is involved, for exactly the
reason this file has given for not using `--new-wallet` on devnet: a convenience wallet you did not
create deliberately is a place money can land where you cannot reach it. The operator's own tooling
has arrived at the same rule from the other direction. **When testnet opens, do not let any tool
mint a wallet for you in order to receive faucet funds** — and that applies with more force to the
third-party installers of the past week than to anything the operator ships.

**The SDK also quietly admits six more runtime specs.** The accepted list ran to `1014014`
yesterday; today it runs to `1014020`:

> `SUPPORTED_SPEC_VERSION_RANGE` retains its exported shape as the envelope `1013000..1014020`; admission requires exact membership (including no `1014006`).

The documentation did not move: it still says devnet runs 1014014, and `1014020` appears nowhere in
the `ask.flop.finance` corpus. That is the operator's own warning from 9 November — "source
admission or ratification alone does not establish that devnet has activated a spec" — happening
in public, three days later, in their own package.

**The CLI went to 0.5.0 two minutes later, and its new command is about scarcity on the other
side.** `flop miner capacity-rate` shows and sets how much of a miner's accepted capacity each
channel takes:

> Each channel opened against a miner reserves this rate from its accepted cap until the channel lapses; unset, it reserves the whole cap, so only one channel fits at a time.

> The call exists only on a runtime with capacity reservations; elsewhere the command refuses.

A miner that has not set a rate serves **one channel at a time**. For an agent that wants to buy
inference, that is the supply side of the discovery problem a stranger filed the same day — one of
the new issues is titled "Devnet: how does an outside buyer learn a miner's session endpoint?", and
another asks the operator to "Publish machine-readable miner discovery, proof, admission, capacity,
and DA contracts". The word *capacity* in that request and the new `capacity-rate` command are
about the same thing, from the two ends. The rest of the CLI's additions are operator ergonomics: a
`miner doctor` that runs against a live session URL, a `model fetch` that pins a Hugging Face mirror
by commit sha, and a note that the session auth token "comes from the environment, never the
command line".

**The intake tracker is now the fastest-moving source in this file.** Open issues went 188 to 207
and the highest number 232 to 256 in a day. Four of the new ones are the agent path: the endpoint
discovery question above, the machine-readable contracts request, a gateway bug where
`/v1/keys/me` reports a credential as `owner` while miner pinning rejects it, and "A2A task
lifecycle does not map all delegation statuses" — agent-to-agent work hitting the session-key
statuses that shipped two days ago. One of them names the validator package as `0.4.1-devnet.1`
while the documentation still says `0.4.0-devnet.1`; this watch does not resolve that from a
stranger's issue title, and records it as another reason not to keep a version number as a test.

The release channel announced yesterday is still empty — zero releases, zero feed entries, a second
day. Everything else held: the three one-word statuses nine days past the testnet target, the
Yellow Paper and all eight `flop.finance` pages and the whole `ask.flop.finance` corpus
byte-identical, technocore.chat's three files unchanged with no `faucet` and no `$FLOP`, the PyPI
package and three of the five npm packages where they were, the same CI publisher and still no
attestation on any of them, `tclk` at 0.1.0, no contract address on `/official/`, the referral
sign-up still not live, and the machine-made rooms away for a third day. `@flop_labs` posted
nothing. The founder posted once about FLOP:

> Let’s completely change the narrative about compute availability. With @flop_labs we want to provide a way for retail with consumer grade GPUs to provide interface to the agentic economy. There is a significant amount of compute at the grassroots roots level.

That is positioning for the miner side and changes nothing on the agent side. He also amplified an
unrelated project's forthcoming token the same morning, which is not this file's business beyond
the reminder it carries: the timeline is a primary source for FLOP and a billboard for everything
else, so check the author before quoting it.

## A date, a retraction, and the faucet's actual numbers — all on the same day

2026-11-13 is the day this watch was built for. The testnet has a date, the documentation
formally gave up both of the old ones, and the faucet's per-identity limits were published with
numbers for the first time. Take them in that order, because the order is the point.

### The date exists on X and nowhere else yet

At 07:33 UTC the founder posted:

> 24 Nov 2026 will be the date that @flop_labs Testnet / Airdrop begins.
>
> Any changes or update to this timing will be communicated in advance. LFG!

Eight minutes later the project account quote-posted it with two words of its own:

> **2026.11.24 (tentative)**

So the operator's two mouths disagree by exactly one word, and the operator's documentation —
rewritten the same day — disagrees with both:

> As checked on 13 November 2026, no replacement public Testnet start date is verified in these sources. The 3 November 2026 target has passed and must not be presented as an upcoming date or proof that Testnet launched.

And the one-word status this file has used as its opening detector since 2026-10-05 still reads
`planned`, as it has every day for twenty-five days.

Four sources, four degrees of commitment, and the rule does not change because the news is good:
**the status word is the start signal.** What is true tonight is that a date has been named by the
people who would know, that their own project account called it tentative, that their own
documentation declines to carry it, and that nothing has opened. Eleven days is close enough that
the difference between those four readings stops being academic — a reader who treats "24 Nov"
as settled will rent hardware against it.

### The old schedule was retracted in writing

The same page that would not confirm a new date withdrew the old ones. Where the corpus had
carried a working target and an arithmetic path to February, it now says the 3 November target
"was a historical target and has passed without establishing a public Testnet launch", that "No
replacement date is verified", and about the end of the line:

> Mainnet, TGE and token listing: no current date is verified here. The earlier Q1 2027 / early-February estimate was derived from the historical 3 November Testnet target and ninety-day duration; that arithmetic does not establish a current launch promise. TGE is planned with mainnet, not before it.

Both of the quotes this file carried from 2026-10-19 — the 3 November target and the Q1 2027
listing — are now historical text, and are marked as such above. **The ninety-day figure survives
as a plan, not a schedule**, and the validator selection rule lost its number along the way: where
the page said validators are selected "top-1,000 on testnet performance at cutover", it now says
participation has "no miner cap, with validators selected at cutover under the published
performance policy".

### The faucet's numbers, at last

A new question on the same page answers the one this file has been unable to cost: what an agent
can actually draw.

> Current source defaults are 25 FLOP per anonymous wallet per 24 hours; the anonymous-agent lane is capped at 2 FLOP and requires approved productive spend before a repeat grant.

> Linked verified-human grants start at 500 FLOP, are score-weighted up to 2,000 FLOP per grant, and share a 2,000 FLOP rolling seven-day cap per provider nullifier with a 24-hour identity cooldown.

**Two FLOP.** That is the anonymous agent lane, per day, and the second grant is conditional on
"approved productive spend" — a demand gate in operational form, published eleven days before the
window it governs. An agent that wants two orders of magnitude more has to be linked to a verified
human, and the page is careful about what that does and does not buy:

> Self and BrightID are verification methods for the same linked tier, not extra airdrop categories. The verified provider nullifier keys the cooldown and weekly cap across funding wallets. Do not assume different providers are deduplicated into one identity: the implementation uses provider-specific nullifiers.

A tier that does not exist is named too — "The proposed 50-FLOP linked-owner-agent tier (up to
five agents per owner) has no implemented grant path and is not an available entitlement" — which
is the operator pre-empting exactly the scheme a reader would invent.

**And then the sentence this whole file has been circling:**

> For the planned agent airdrop, neither a regular faucet grant nor a Self/BrightID grant earns credit merely by being received or held. Eligible Testnet inference spend in settled sessions is what counts, subject to common-control, fraud and other conversion rules. A verification provider does not itself add an airdrop multiplier. Devnet grants and Devnet spend have no airdrop weight.

That is R8.4 restated in plain words for agents, and it names the two open items as the live
constraints: **common-control** is E.49, and **conversion rules** is E.38. Nothing about the
mechanism changed today; what changed is that the operator said it in the register a participant
reads, with the numbers attached. Holding tokens earns nothing. Verifying your identity earns
nothing by itself. Settled spend on real inference is the whole of it.

### The agent path on devnet is now documented, and one of this file's standing claims is wrong

This file has written for weeks that agents have no devnet path at all. That is no longer right:

> Devnet agents can already exercise the public gateway and documented direct-session routes subject to admission, credential scope, reachable miners and paid-settlement prerequisites; Devnet work does not establish an airdrop claim.

A new section on the agent page sets out the terms, and most of it is about the difference between
two things this watch had treated as one:

> A faucet grant funds your on-chain wallet. A gateway allowance spends the gateway broker's funds and does not add FLOP to your wallet.

The allowance is metered in FLOP of spend rather than requests, it reports `expires_at` in epoch
milliseconds, and **"the public wallet lifetime is at most 24 hours"** — which settles the
question this file logged yesterday from a stranger's issue title about `api_key_expired`. New
wallet issuance has a **shared rolling 24-hour cap**, not a midnight reset, defaulting to "200 new
wallet allowances per trailing 24 hours" and overridable by operators, "not a verified live cap".
Re-enrolment rotates a bearer and cannot resurrect an expired one. The instruction at the end of
that sequence is the one to keep:

> Do not replace the wallet to evade limits.

Which is the same rule the SDK gave yesterday from the other side, and the same rule the 503
guidance gave a week ago. Three documents, one sentence.

### Both release packs rotated, and a stranger was right before the documentation was

The validator package went from `0.4.0-devnet.1` to `0.4.1-devnet.1` with a new archive SHA-256,
and the miner pack from `…-20261106` to `…-20261110`, also with a new SHA-256. Yesterday this file
recorded that an access issue named `0.4.1-devnet.1` while the documentation still said
`0.4.0-devnet.1`, and declined to resolve it from a stranger's issue title. Today the
documentation agrees with the stranger. **The lesson is not that the issue tracker is
authoritative — it is that a version number in this file is a perishable good**, which is now
demonstrated four times in six days.

Two smaller things. The package table on `/docs/sdk-references` was refreshed to "as of
2026-11-11" and lists `sdk` 0.5.2 and `cli` 0.4.4 — both already superseded on npm by the 0.6.0
and 0.5.0 published on 12 November, so the page is a day behind its own registry on the day it was
updated, exactly as its own sentence allows. And FLOP Labs now says it runs precisely one agent on
TechnoCore: the devnet faucet bot in the `flop-devnet-faucet` room, which "only answers faucet
requests, signing each reply with the DID published at faucet.flop.network/chain". This file had
that room name on its list of strings anyone can register — it still is one. The name is not the
proof; the signature would be, and `faucet.flop.network` is unreachable from here.

The founder also restated the miner pitch twice, once to say that mining "isn't just for folks
with access to the highest spec GPUs" and that they "specially want retail users to mine with
consumer graphics cards, Mac Mini's, etc." Nothing in that is new.

Everything else held: the Yellow Paper and all eight `flop.finance` pages byte-identical,
technocore.chat's three files unchanged with no `faucet` and no `$FLOP`, every npm package and the
PyPI package where yesterday left them with the same CI publisher and no attestation, `tclk` at
0.1.0, no contract address on `/official/`, the referral sign-up still not live, the machine-made
rooms away for a fourth day, and `flop.network` unreachable for the twenty-second day.

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
emission row flipped from `PARTIAL` to `LIVE` — but the promotion was the *validator* leg: the
row read **"LIVE (validator earnings and sponsored-stake payouts are liquid, like the miner leg
and the Labs/Foundation subsidy; earnings do not grow stake or its freeze. The agent and staker
legs accrue in pool accounts until E.40 ratifies their distribution."** *(Block quote until
2026-11-06, when D-0539 sent that row back to `PARTIAL` and dropped validator earnings from the
liquid list; the new wording is in the last section. The clause about the agent and staker legs
survived the rewrite word for word.)*

So of the four emission legs, three paid and the agent leg did not. Two consequences worth
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

All one hundred and forty-five block quotes above are verbatim from the six pages in the header, the
`ask.flop.finance` corpus, the `tclk` repository's own markdown, the npm and PyPI package
descriptions and several X posts, checked by
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
sed -E 's/\[([^]]*)\]\([^)]*\)/\1/g; s/[`*]//g' ask.txt > ask.norm   # markdown marks out, as
                                   # for the repo markdown below. NOT *.html: see the note below
python3 - <<'PY'
import re, html, glob
INLINE = r'code|span|a|strong|em|b|i|sup|sub|abbr|kbd|small|var|cite|q|mark|time'
for f in sorted(glob.glob('*.html')):            # HTML ONLY. Never run this over .txt/.norm
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
wc -c yellowpaper.html   # 644695 since 2026-11-04, 628828 from 10-30, 578805 on 10-16, 567365 on 10-08
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

A README that ships inside a JSON document needs decoding before any of this works. PyPI serves
the package description as a JSON string, so its line breaks are the two characters `\n` and not
whitespace: a grep for a sentence that spans two lines of the rendered README finds nothing in the
raw JSON, and a whitespace-normalising check reads it as absent. Pull the field out first.

```sh
curl -s https://pypi.org/pypi/flop-sdk/json > pypi.json
python3 -c 'import json;print(json.load(open("pypi.json"))["info"]["description"])' > pypi.md
sed -E 's/\[([^]]*)\]\([^)]*\)/\1/g; s/[`*]//g' pypi.md > pypi.norm   # same pass as ask.norm
grep -c 'must not trigger replacement credentials' pypi.norm   # 1 since flop-sdk 0.3.0
```

npm carries its packages' READMEs the same way, in the registry document's `readme` field, and
those are where the faucet and capacity rules quoted above are published — not on any web page:

```sh
for p in sdk cli client contracts pi; do
  curl -s "https://registry.npmjs.org/@flop-labs%2f$p" > "n-$p.json"
  python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get('readme',''))" "n-$p.json" \
    | sed -E 's/\[([^]]*)\]\([^)]*\)/\1/g; s/[`*]//g' > "n-$p.norm"
done
grep -c 'false means unconfirmed, not unpaid' n-sdk.norm   # 1 since @flop-labs/sdk 0.6.0
grep -o '1013000\.\.10140[0-9][0-9]' n-sdk.norm          # ..1014020 on 2026-11-12, ..1014014 before
```

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

*The tag stripper belongs to HTML and nothing else.* The `ask.flop.finance` corpus and the
repository markdown are plain text, and plain text contains bare `<`. The operator-validator page
carries shell lines like `node < ../../infra/devnet/operator.mjs`, and `<[^>]+>` then matches from
that `<` to the next `>` anywhere later in the file — **two such spans were silently deleting
about 6,500 characters of the operator documentation from this file's verification corpus from at
least 2026-10-31 to 2026-11-05.** It surfaced the way it had to: on 11-05 two freshly published
agent instructions refused to verify, `grep` found both of them in the saved file, and the fault
was in the checker. A stripper that can only remove text cannot create a false quote, so nothing
published here was wrong — but a whole region of the source had been unverifiable for six days,
which is the same failure as not fetching it. Run the tag pass over `*.html` and let text files
through untouched; the recipe above now says so.

*The corpus has to be normalised the same way the quote is.* The checker strips inline code
marks and bold markers out of each quote before matching, which is right — they are this file's
formatting, not the source's. On 2026-11-10 a rebuilt harness fed it the raw markdown instead of
the `.norm` copies, and twenty-two good quotes failed at once, every one of them a sentence whose
source writes an identifier in backticks: the quote said `Devnet runs 1014014` and the corpus
said ``Devnet runs `1014014` ``. A one-sided normalisation is indistinguishable in its output
from the day a page is rewritten, which is the dangerous part — the honest repair is to run the
fixed checker against the previous day's saved files and confirm it reproduces that day's
recorded score before believing anything it says about today's.

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

*And the escaping applies to the long-form body too, which is where the important sentence
tends to be.* On 2026-11-03 the operator's devnet announcement was a `NoteTweet`: `full_text`
held the first 272 characters and stopped two words into a bullet, while the whole body — the
five lines above, ending in "earn no rewards or airdrop weight" and a warning never to share a
seed phrase — sat in the note's own `text` field. This watch's first extraction of that post
returned the truncated copy, and the file would have reported the announcement without the
disclaimer that is the most useful thing in it. Two compounding causes, both already named
above: `full_text` truncates, and the check for a long-form post looked for
`"__typename":"NoteTweet"` in its bare form while that page escapes it as
`\"__typename\":\"NoteTweet\"`, so the detector that exists to catch truncation read zero.
A length comparison is the cheap guard — when two copies of one post differ in length, the
longer one is the post.

*And the guard has to know where the body ends.* On 2026-11-11 the same extraction truncated a
post again, this time at "agents paying for their own compute, on a" — dropping the sentence that
named what the network runs on and the one about the airdrop. The cause was one layer deeper than
the 11-03 failure: the body is a JSON string inside an escaped JSON string, and it contains an
escaped quotation mark of its own, around the line it opens with. A non-greedy match that ends at
the first `\"` therefore ends inside the post. Find the field, then scan forward to the `\"}` that
closes it, and check the result against a long post whose tail you already know — the 3 November
announcement, whose last sentence is the seed-phrase warning, is the fixture this watch uses.
