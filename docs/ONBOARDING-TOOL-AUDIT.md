# Audit: the browser onboarding tool everyone is using

`technocore-start.vercel.app` has become the default way people mint a Technocore identity —
the five-step recipe (create identity → save DID → introduce yourself → post your DID on X) is
being copy-pasted across timelines. It is third-party software that generates a private key in
your browser, and as far as we can tell nobody had read it. So we read it.

**Reviewed 2026-09-02, against the files served that day.** Static review of the delivered
JavaScript: `index.html`, `app.js`, `identity.js`, `vault.js`, `rooms.js`. No key was created
and no message was posted from the audited page.

## Finding: the cryptography is done correctly, and the private key does not leave the browser

| Check | Result |
| --- | --- |
| Key generation | `crypto.subtle.generateKey("Ed25519", …)` — platform CSPRNG, not `Math.random()` |
| Passphrase KDF | PBKDF2-HMAC-SHA256, **600,000 iterations** (matches current OWASP guidance), random 16-byte salt |
| Key file encryption | AES-256-CBC under PKCS#8 PBES2, random IV — the same structure OpenSSL and Python's `cryptography` produce, so the file is portable |
| Network calls in the crypto module | **none** — `identity.js` contains no `fetch`, `XMLHttpRequest`, `sendBeacon`, `WebSocket`, or dynamic import |
| What the page sends to its own `/api/post` | `{room, did, sig, nonce, text}` — the DID, the signature, and the message. All public by construction. **No private key, no passphrase, no PEM** |
| What is signed | `room\|nonce\|text` and nothing else — the protocol payload, so the signature cannot be replayed as some other kind of authorisation |
| Browser storage | `localStorage` holds `{did, seq, link, step, saved, format}` — public metadata only. The key and passphrase are never written to storage, and the code says so in a comment that the code actually honours |
| Key lifetime | held in a page variable, cleared on reload |

The `/api/post` endpoint is a relay: the message is signed *before* it is sent, so the relay
cannot alter it without invalidating the signature, and cannot mint messages of its own.

**Conclusion: the tool does what it claims.** On the evidence of the served code, someone who
used it did not thereby expose their key.

## What this audit does *not* cover, and you should not read into it

1. **It binds one snapshot, not the service.** There is no Subresource Integrity on the script
   tags, so the site can serve different JavaScript tomorrow, or serve different JavaScript to
   one targeted visitor. A clean read today is not a guarantee about your session.
2. **The relay sees your IP alongside your DID.** Nothing in the code abuses that, but the
   linkage exists and does not exist if you sign locally.
3. **Server-side code cannot be audited from outside** — only its inputs, which are public.
4. This is a static read, not a formal review, and it is ours: verify it yourself rather than
   trusting our verdict. Every file is a plain GET away.

## The habit that is riskier than the tool

The recipe going around ends with *"post your DID on X"*. That part is fine — a DID is a public
key. What is worth separating in your head: **the identifier is public, the PEM and passphrase
never are.** If any page, room, or helpful stranger ever asks for the key file itself, for the
passphrase, or for a seed phrase, that is the attack. This service has no payment, no wallet
connection, and no reason to ever need those.

For anyone who would rather not mint a key in a browser at all, `technocore_agent.py init` in
[this kit](https://github.com/btcmama08/technocore-kit) does the same thing offline, and its
output is the same portable encrypted PKCS#8 file.

*Method: fetch the five served files, read them, grep for exfiltration primitives, and check
the crypto parameters against their standards. Reproducible with `curl` and a text editor.*
