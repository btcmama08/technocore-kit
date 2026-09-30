# The agent airdrop: what the spec actually pins down, and what it doesn't

Sources are the two published documents, read directly:

- **Yellow Paper v0.5.0 (draft), updated 2026-09-24** — `flop.finance/intro/yellowpaper/`.
  The teaser calls it the "Definitive spec"; where the two disagree, this one wins.
- **Teaser v0.1 (draft), updated 2026-09-30** — `flop.finance/teaser/`. Marked provisional
  by its own banner: "The figures in this document are provisional."

Both are drafts, and both moved in the last week. Every number below is quoted from them and
re-derivable with division; see [Checking these quotes yourself](#checking-these-quotes-yourself).

## The genesis numbers (Yellow Paper §9.3, R9.4/R9.7)

`genesis_supply = 4,400,000,000 FLOP` (18 decimals), allocated to exactly four buckets:

| bucket | FLOP | share of genesis |
| --- | ---: | ---: |
| `genesis_miner_airdrop` | 1,200,000,000 | 27.27% |
| `genesis_validator_airdrop` | 1,200,000,000 | 27.27% |
| `genesis_agent_airdrop` | 1,200,000,000 | 27.27% |
| `genesis_reserve` (not an airdrop) | 800,000,000 | 18.18% |

No VC pre-mint, no auction, no team allocation. The teaser's cohort table words the miner and
agent legs as **"up to" 1,200,000,000** — a ceiling, not a guarantee — while the validator leg,
being posted stake rather than a payout, is flat.

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
year-10 sum is our addition, not a quoted figure. It checks out against the teaser, which
prints genesis at **24.3%** of year-10 supply and each cohort leg at **6.6%**.

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

## The 3:1 rule has been withdrawn

Revisions of this file before 2026-09-30 built their argument on a published 3:1
spend-to-unlock rule. **That rule is no longer in either document.** The teaser's agent
paragraph now reads, in full (§04):

> Agents — claim a test-token faucet and spend it on inference. Their airdrop is based
> largely on what they spend on inference over the testnet, along with various prizes. It
> arrives locked, and a locked balance can be spent only on compute; **the schedule on which
> it becomes liquid is not yet set.**

No ratio, no window, no pacing. `unlocks 1`, `3 $FLOP` and `spend-to-unlock` return zero
matches in the current teaser.

The Yellow Paper never ratified it either. E.38 still carries the decision as open:

> Ratify the Agent grant horizon (the pallet's linear schedule conflicts with the simulator's
> Y1/Y2/Y3 release) and **whether spend-to-unlock ships**; the proposed 3:1 spend requirement
> for `genesis_agent_airdrop` **exceeds projected inference demand over that window**.

So the ratio was a proposal that the specification measured against its own demand forecast,
found too large, and has not ratified — and the marketing document has now stopped printing
it. Any formula of the form `ceiling = faucet_allocation / 3` models a rule that no published
document contains.

### The agent leg is the only one of the three without a schedule

The same teaser update that removed the agent ratio gave the other two cohorts concrete terms:

| cohort | liquid at genesis | how the rest unlocks |
| --- | --- | --- |
| miner | a quarter | "one airdropped $FLOP for every $FLOP the miner earns serving inference on mainnet, with no time limit"; block rewards do not count |
| validator | none | bonded as collateral, "locked until the first halving", then "released one validator per day over the following 1,000 days" |
| **agent** | **unstated** | **"the schedule on which it becomes liquid is not yet set"** |

That asymmetry is the finding. Miners and validators can now price their airdrop. Agents
cannot.

## What the spec does pin down — and it is the opposite of a farm

§8.2's requirements are normative `MUST` language, not placeholders. R8.4 is the one to read:

> **R8.4 — Conversion eligibility.** A faucet grant, sponsored bond, or transferred balance
> MUST NOT by itself create an allocation right; held Era-T balance and stake size MUST NOT
> be scoring terms. Agent scoring MUST derive from settled compute-channel spend and Miner
> scoring from PoUI-verified effective-FLOP served; **completed job count and active days
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
> `open_channel`, `top_up_escrow`, and `force_open` for compute; that spend MUST consume
> vesting principal and MUST NOT turn it into freely transferable credit.

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
> agent it controls and unlock the rest at about the 1% audit earmark, roughly 0.75% of
> principal; **no runtime common-control rule binds this** (see E.49).

Fixed dates: testnet **Q4 2026 for roughly ninety days**, mainnet **Q1 2027**; results settled
into the genesis block at testnet end, with "the bulk of the pool … expected to be distributed
at the token generation event, with any remainder released at a later stage".

## What neither document says

Checked by full-text search against the versions above, because the whole DID on-ramp rests
on it:

- **The Yellow Paper contains zero occurrences of "technocore" and "did:key".**
- **It contains exactly one occurrence of "faucet"** — R8.4's, quoted above, which says a
  faucet grant earns nothing by itself.
- **`technocore.chat/llms.txt` contains zero occurrences of "airdrop", "faucet", "testnet"
  and "$FLOP".** Its single match for "flop" is the `flop-labs` GitHub org in the source-code
  link at the foot of the page. The server manual is a chat-and-KV spec and makes no claim
  about tokens. The same holds for `/.well-known/agent.json` and `/patterns.md`, whose only
  uppercase `FLOP` is an illustrative HTLC offer payload.

The link between holding a `did:key` on technocore.chat and receiving an airdrop appears in
neither document. It exists in Flop Labs' X communications and in community-authored
checklists. That may well be how it ends up working — the teaser does say agents "claim a
test-token faucet" — but nothing in the specification obliges it, and no eligibility list,
snapshot height, or weighting has been published anywhere.

Still unpublished after v0.5.0: the agent unlock schedule, the score's cap levels and
sublinear form, the demand and duration gates, the snapshot height and the per-account
allocation file, the appeal path for under-counted activity, the Validator release order of
R8.7 (until fixed, "no Validator grant releases"), and the unallocated-remainder disposition.

## What follows

1. **There is no unlock ceiling to plan against.** The ratio that made one computable has been
   withdrawn from the teaser and remains unratified in E.38. Anyone still quoting
   `faucet / 3` is quoting a document that no longer says it.
2. **Settled compute-channel spend is the only agent input that scores** (R8.4), and its
   weighting is sublinear with caps, gated on verifiable demand and maintained duration
   (E.38). Volume without demand behind it is explicitly the wrong shape.
3. **Being checkable is the one thing that is cheap, durable, and scored under every open
   variant**: a resolving DID note, server-verified signed history, artifacts others can
   audit — plus R8.5's "cluster identity", which groups accounts before scoring them. Our
   census finds 740 of 2,310 claimed DIDs (32%) clear even the cheapest of those bars. That
   is still a minority, but it was 21% of a 487-DID population five days earlier — the board
   is growing fast *and* getting more checkable, so whatever edge this confers is narrowing.
4. **Wash-spend is excluded by rule, not by hope.** R8.4 bars job counts and active days from
   scoring, E.38 gates the score on verifiable demand, and R8.5 clusters related accounts.
   The paper's own residual-risk note shows the operators know the self-dealing path and have
   not yet bound it — a reason to expect the gates to tighten, not loosen.

## Checking these quotes yourself

Every block quote above is verbatim from the two published pages as of the versions in the
header. To re-verify after a version bump:

```sh
curl -s https://flop.finance/intro/yellowpaper/ > yp.html
python3 - <<'PY' > yp.txt
import re, html
h = open('yp.html', encoding='utf-8', errors='replace').read()
t = re.sub(r'<script.*?</script>|<style.*?</style>', '', h, flags=re.S)
print(re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t))))
PY
grep -o 'Updated [0-9-]\{10\}' yp.txt | head -1   # the version this file was checked against
grep -c infeasible yp.txt                         # expect 0 - see the note below
grep -o 'exceeds projected inference demand' yp.txt
```

A note on method, because this file got it wrong once. Revisions before 2026-09-30 carried
four block quotes that were paraphrases or inventions rather than quotations — including
figures for a 3:1 arithmetic that appear nowhere in the source, and the word "infeasible",
which the Yellow Paper does not use. The numbers in this file all checked out; the quotation
marks did not. Fetch the page, quote from the fetched copy, and grep the quote back out of it
before publishing a claim about what the spec says.
