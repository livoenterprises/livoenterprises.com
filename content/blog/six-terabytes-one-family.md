---
title: Six terabytes, one family: how I actually use the family OneDrive
description: A Microsoft 365 Family plan gives six people a terabyte each. Here is how one family turned that into a photo archive that nobody can lose and nobody can break.
date: 2026-11-08
updated: 2026-11-11
topics: Own your data, Technology that serves you
author: Livo Enterprises
listed: yes
front: yes
---

I keep my family's photos. Not by appointment; it just happened, the way it happens in most families. I'm the one people send pictures to, the one with the scanner, the one who knows which hard drive the 2009 vacation is on. Thirty years of this leaves you with photos in every format a camera has ever produced, on every kind of storage anyone has ever sold, and a quiet dread that one bad drive or one closed account will take a decade with it.

The best storage deal I have found for this is not a photo service. It's the Microsoft 365 Family plan: six people, one terabyte of OneDrive each, about $150 a year for all six. Six terabytes is more than a family of six will fill with photos in a lifetime. The trick is using it so the space helps instead of becoming one more place things get lost. This is how I do it.

## Each person owns their own terabyte

The first decision is the one most families get wrong. It's tempting to make one giant shared folder and have everyone dump into it. Don't. On OneDrive, a file counts against the quota of the person who owns the folder it sits in, and anyone with edit rights to a shared folder can delete anything in it. One shared bucket means one person pays for everyone's storage and one child's slip takes out a sibling's photos.

So every person in the family keeps their own photos in their own account. Each phone backs up its own Camera Roll into its own OneDrive with the OneDrive app's camera upload. Nothing crosses between accounts unless someone decides it should. If a phone is lost, the photos are already in that person's terabyte. If someone leaves the plan one day, their photos go with them, intact, because they were always theirs.

## Sharing is a folder you write and others read

Within that, each person has one folder, shared with the other five, that works as an outbox. I put something in mine; the family can see it. I can't put anything in theirs, and they can't touch mine. The rights are view only, on purpose. The files stay in the owner's quota, nobody can overwrite or delete anyone else's, and there is no single folder whose permissions have to be right for the whole family's archive to be safe.

This sounds restrictive and feels the opposite. Because nobody can damage anything, nobody is afraid to use it.

There are two kinds of shared folder, and it helps to keep them apart in your head.

The first is the **shared folder**: the outbox, for things meant to be seen this week. The video of the birthday Memory, so everyone can watch it on whatever they own. The capsule for Grandma's eightieth. The twenty best photos from the trip, not the four hundred. The scan of the wedding photo somebody asked for at Thanksgiving. A short clip of the grandchildren for the aunt who isn't on anything. Things go in, get looked at, and can stay or go; nobody treats it as the archive.

The second is the **family library**: a whole collection, shared once, also mine and read-only, that carries a small catalog of what's in it so the family's phones can find a photo by name instead of browsing thousands of files. That is where the long-lived sets live. The 1970s slides after they were scanned and named. Every photo of my parents I have been able to find, in one place. The complete run of a trip, not just the picks. The Christmas and Thanksgiving photos going back twenty years, by year. My father's slides, which my sister also wants, without either of us emailing anything. A family member points their phone at it once, and from then on "Dad in 1978" finds the slide.

In LivoCapsule those two are Family Share and the Family Library: the first for the things you make, the second for the archive itself. The phone shows them the same way, as photos with names; the difference is only how long they are meant to stay and how big they are allowed to get.

## The originals live in the cloud, not on the phone

A phone is for taking photos and looking at them, not for storing thirty years of them. Once the Camera Roll is safely in OneDrive, the originals' home is OneDrive. The phone keeps small copies of everything, enough to scroll, search and tag without a connection, and fetches a full-size original only when one is needed: to zoom in, to seal a capsule, to make a gift. My own OneDrive holds about fifty thousand photos and videos, and all of them are on my phone at thumbnail size, a few gigabytes in all. The originals would not fit on any phone I could buy, and they don't need to.

That also means the phone can be replaced without ceremony. A new one gets the small copies back and knows where every original is.

## The cloud is a rented shelf

Here is the part nobody puts on the box. If the Microsoft 365 subscription lapses, the account drops back to the free 5 GB, and a terabyte of photos is suddenly two hundred times over the limit. Microsoft's own rules for an over-limit OneDrive: everything goes read-only at once (you can still download and delete, but nothing new goes up); after three months over the limit the account is frozen; after six months Microsoft may delete the OneDrive and everything in it, and that deletion is not recoverable. Renewing stops the clock at any point. So a family that lets the plan go has a window of a few months to pull a terabyte down over a home connection before it is at risk. The cloud copy is not the archive. It is a rented shelf, and the rent is $150 a year.

Which is why the originals' home has to be two places, and one of them has to be something you own outright: an external hard drive on a shelf. The way to keep it current is the OneDrive folder on a computer. Every Mac and PC with the OneDrive app has one, and it can be mirrored to a drive. Two things to know before you trust it:

- The OneDrive folder on a computer is mostly placeholders unless you tell it otherwise. Right-click the photo folders and choose **Always keep on this device** first; otherwise your "mirror" is a folder of icons. Give it a day to fill.
- Then mirror the folder to the drive and repeat it once a month. On a Mac, Carbon Copy Cloner or ChronoSync does it, or a plain Finder copy for the first time; on Windows, FreeFileSync, or `robocopy /MIR` for anyone comfortable with a command line.

The trouble with every backup is that nobody looks at it until the day they need it. So LivoCapsule can write two small files into the top of your OneDrive, a manifest of everything it knows about your photos and a page called **CHECK MY BACKUP**. They ride along with the next mirror. On the computer, open the page from the drive itself in Chrome or Edge, choose the folder, and it reads what is actually there and tells you: 48,912 expected, 48,912 found, 48,909 match, 2 missing, 1 changed, with the names. Nothing is sent anywhere; the page only reads the folder you point it at. A number you can read once a month is what confidence in a backup actually looks like.

## One clean account, eventually

I'll be honest about the mess. I have several Microsoft accounts from different eras, and photos ended up in most of them. Folders got named by whoever was holding the camera. Some of it was in a work account's cloud for a while. My rule now is that everything gets found and named first, wherever it is, and consolidated second, into one clean account, one folder tree, one naming scheme. Naming is the part that can't wait, because the people who know the faces in the oldest pictures are the people who won't be here longest. Moving files can happen any time.

## What goes in the shared folder, and what doesn't

Shared: things made to be seen. Memory videos, because anyone can play an .mp4 with or without any particular app. Capsules, because they open in a web browser and carry the names and stories inside the photos. Picks: the photos worth the family's time, not the four hundred near-duplicates of the cake.

Not shared: backups. A backup of a photo library's names, stories and settings is private, and it lives in a private folder in the owner's own account, never in anything the family can see. The same goes for the drafts, the duplicates, the photos that didn't come out. The family folder is the album on the coffee table, not the drawer under it.

## What I'd tell a family starting today

Get the plan, give everyone their own account, turn on camera upload on every phone, and stop there for a month. You have already solved the problem that matters most: nothing is only on a phone any more. Then make one shared, read-only folder each, and start putting the good things in it. Then, and only then, start on the shoebox.

Everything above works with the OneDrive app alone, plus one drive and one afternoon a month. It's the structure I built LivoCapsule's family features around, and it's why LivoCapsule never needed a server: the family already has six terabytes, owned by the people whose photos they are. The tool's job is to make the folders, set the rights, put the names and stories into the files, and hand you a way to check the copy on the shelf, so that what we know about these pictures is still there when the subscription, the phone and the app are long gone.
