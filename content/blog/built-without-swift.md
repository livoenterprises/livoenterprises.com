---
title: I built an iPhone app without learning Swift. The interesting part isn't the AI.
description: How LivoCapsule was built by describing it in plain English to an AI and holding it to a real engineering process, and what broke along the way.
date: 2026-09-18
updated: 2026-09-18
topics: Building with AI, Technology that serves you
author: Ken Jones
listed: no
---

## The thread

I've spent a career building applications, and for the past fifteen years I've worked in business intelligence and data --- managing BI projects, thinking about what systems know and what people can do with it. Somewhere in there a conviction formed that I didn't recognize as a single idea until recently, when I sat down to write this.

It's this: people should own their data, and devices should work for people --- not the other way around.

Those sound like two ideas. They're one. If you own your data, you decide who sees it, and you decide whether it will still open in fifty years. If devices work for you, you don't spend your life learning their menus, their gestures, their file formats --- you tell them what you want, in the language you already think in, and they do it.

For most of my career the technology wasn't there for either half. Your photos went to a social network that owned them. Building an app meant learning the platform's language whether you wanted to or not. The idea was right and the tools were wrong.

This is the story of the first thing I built when the tools caught up. It's an app called LivoCapsule, and the reason it exists is the same reason I was able to build it without reading a line of Swift.

## Why LivoCapsule

I wanted a way to preserve my family's photos, video, voices and stories that had a real chance of surviving across generations. Not as a feed on someone else's server --- where you don't know who's looking, whether the company will exist in twenty years, or whether the format will open in fifty when your great-grandchildren go looking. As something you hold, and hand to the people you choose.

So LivoCapsule gathers photos and video from the Camera Roll and OneDrive, tags them with people and places, curates them into Memories, lets you narrate a Memory in your own voice, and seals it into a self-contained time capsule: a plain zip file holding the originals, the metadata, the audio, and a static web page that opens in any browser on any machine, with no app and no account. The capsule lands in your phone's Files folder where you can copy it, AirDrop it, or put it on a drive in a drawer. There's no server. There's no sharing platform. You give a capsule to someone the way you'd give them a photo album.

The architecture followed from that goal rather than from convenience. JPEG originals pass through byte-for-byte. HEIC is transcoded to JPEG with every scrap of metadata preserved, because JPEG is the format most likely to still open in 2076. Live Photos keep their motion clip as a verbatim MOV so the pair can be reunited later. The catalog inside the app is a cache; the zip and its manifest are the truth, and a folder scan can rebuild everything else. Every one of those was a decision, and every one was argued --- with an AI.

## Why I didn't learn Swift

I had no interest in becoming an Xcode expert. I've learned my share of languages; Swift wasn't going to be one of them, and having to learn it to get an app that preserves my family's memories would have been the machine making me work for it again.

So I set up an experiment. Could a generative AI be my expert programmer, with me in the role I'd actually held for most of my career --- the person who owns the requirements, challenges the architecture, and decides whether the thing works? Not "let the AI do it." The AI wrote every line. I made every design decision, argued most of them, lost a few, and validated every feature on a physical phone.

What surprised me was not that the AI could write Swift. It was that the ordinary engineering process --- requirements, design specification, implementation, change control, verification --- still applied completely, and that I could run all of it in natural language. I wasn't translating my thinking into an IDE. I was doing engineering out loud, and the AI kept the books.

That's the alignment I'd been waiting for without quite knowing it. My natural process is the engineering process. My natural interface is language. For the first time, a collaborator could meet me on both at once.

## The process, as it stands

This is an experiment in progress. It has worked for this app, it isn't a finished method, and the next version will be better. Here is the shape of it today.

1. **The idea, in plain language.** I describe what I want the app to do, to whom, and why. The AI turns that into a requirements document I can read, argue with, and correct.
2. **Design specification.** From the requirements, the AI proposes an architecture and I challenge it --- storage, formats, what's an invariant, what's a decision with consequences. Decisions get numbers and dates. This document keeps getting revised; it's never finished.
3. **The session loop --- state handover.** Every working session opens with a fresh text export of the entire codebase, plus the three documents the last session produced. The AI confirms what build is on my phone and what's still open. Nothing depends on it remembering anything.
4. **The session loop --- decide, then build.** Open questions are settled before any code. Each change then arrives as a complete shell script that backs up what it touches, verifies its own edits, stamps the build with its own name, and tells me what to tap to prove it worked. I never see a snippet.
5. **The session loop --- verify and close.** I run the scripts and report what I actually saw on the device --- observations, never verdicts. The session ends with three documents written for a reader with no memory: a summary, a requirements delta, and a checklist for next time. Then git commit, regenerate the export.
6. **Periodic validation.** Every so often, no new features: walk every unreported check, audit the requirements against the live code, and test the artifact outside the app --- I've opened sealed capsules byte-for-byte on a Linux box with no LivoCapsule in sight. If it needs the app to open, it won't survive the app.
7. **Release.** TestFlight, App Store, and whatever comes after. This is the step I'm still working out. More to come.

The thing I'd underline is step 3. Because the project's state lives in plain-text documents on my disk rather than in any model's memory, I'm agnostic to the model. Switching costs a session of re-establishing context, not the project. The AI writes those documents at each close-out; I check them the way I check a script.

And I only noticed this while writing: that's the same principle as the capsules. Own the data, keep it in a format that will open anywhere, don't trust it to someone else's server --- whether the data is family photos or the state of a software project.

## What broke, and what we changed

Every rule in that process was paid for. A few of the invoices:

**Snippets with placement instructions.** The AI's first instinct was "add this to the top of the file." Fix: the deliverable is a script that makes the change itself, never a fragment for me to place.

**Code it remembered writing.** Patches missed because the AI worked from memory of a script that had failed or been skipped. Fix: memory is illegal; the export is the only description of the code, and the build stamp on the phone is the only statement of what's running.

**A stale export.** Once the export predated work already on disk and the AI acted on it. Fix: a contradiction between the export and the session documents is resolved before anything is written; check the export's own timestamp; only upload from the newest folder.

**The retry loop.** "Anchor found 0 times" invited variants, each costing a build. Fix: zero matches is a diagnosis with exactly three causes, and after two failed patches on one file I paste it verbatim and get a whole-file rewrite.

**The incidental dependency.** We retired a sheet that was silently refreshing the screen behind it. Fix: never retire a path before its replacement is observable, and ask what depended on it incidentally, not just what called it.

**The crash with no dialog.** Tap record, app closes, reopens on the Gallery. I reported exactly that, and the AI had it in one step: a missing microphone permission string. The lesson was about reporting, not code --- say what you tapped and what you saw. "Didn't get to it" is an answer; an assumed pass is how a wrong model of the app accumulates.

**Losing an argument.** I proposed making a Live Photo's video the primary asset. The AI argued the still is the 12-megapixel artifact every feature wants and OneDrive has no Live Photo type anyway. I was persuaded, and the decision is recorded with a number and the reasoning. Owning the decisions includes owning the ones where I changed my mind.

## Why I'm writing this down

I'm sharing this because it's a starting point, not a finished thing, and I'd rather other engineers build on it than rediscover it. Somebody with a different app, a different platform, or a different model will hit failures I haven't, and the process should absorb those the same way it absorbed mine: a symptom, a diagnosis, a standing rule. I intend to keep pushing on it. I'd be glad to find someone ahead of me.

If you take this and take it further, the only thing I'd ask is what the process asks of the AI: write down what broke, what you changed, and why --- so the next person doesn't pay for it twice.

What I have on my phone right now is a handful of zip files that my grandchildren's grandchildren should be able to open with no account, no subscription, and no one in between. And I got there by describing what I wanted, in my own language, to a machine that finally worked for me.

## Appendix --- the process documents

After the first three sessions I asked the AI to write the method down generically so it could be re-established with any model on any app. It produced these; I reviewed and corrected them against what actually happened, but I didn't write them.

- **Start Here** --- the five ideas the method rests on, and the half-hour procedure for handing a project to a new model.
- **Bootstrap Prompt** --- the contract: the script-not-snippet constraint, the two sources of truth, the requirements discipline, the session shape.
- **Session Start Prompt** --- the opening message: build stamp quoted from the phone, export timestamp, last session's checks as observations, today's aim.
- **Session Close Prompt** --- asks for the three handoff documents before anything is run; has a mid-session variant.
- **Script Delivery Contract** --- the specification every script meets, with a reference skeleton; also what gets pasted back when a rule is broken.
- **Document Templates** --- the shapes of the addendum, session summary, checklist and design note.
- **Code Export Spec** --- the export script, the build-stamp constant and its Settings row, the runner file, and why the commit is not optional.
- **Failure Playbook** --- what to do when the model drifts and when the work goes wrong.
- **Degraded Mode** --- a capability check to run before uploading anything real, and fallbacks for weaker models.
- **Worked Example** --- the generic documents filled in with LivoCapsule's real values.
- **Prompt Checklists** --- the two lists kept open at the keyboard: cold start, and drift prevention.
