---
title: Backup & Restore
description: What a backup holds, where it goes, and how to restore onto this phone or a new one.
version: 5
updated: 2026-11-12
order: 17
app: guide
screen: backup
lede: A backup holds everything Livo knows about your photos. Your photos themselves stay where they are.
---

## What is in a backup

[Open Organize › Curator › Backup & Restore](livo://organize/backup). A backup holds every name, place, story, tag and face you have added, your Memories and narrations, Livo's small copies of your photos, what Livo Search has learned, your family folders list, and your settings. It does not hold the photos themselves (they stay in Photos, or in OneDrive with Curator) or your Time Capsules (they are files; see [Keeping capsules safe](/guide/keeping-capsules-safe.html)).

## Making one

**Create Backup Now** runs in the background; the card and Activity show the steps. Livo keeps the screen on while it works. Backups are named Livo_Backup_ with the date and time, and nothing already there is ever overwritten. The backup is saved on this phone (On My iPhone › Livo › Livo Backup); **Share** on a backup puts it in iCloud Drive or any folder in Files. With [Curator](/guide/curator.html), **Copy new backups to OneDrive** copies each one to the private **Livo Backup** folder in your OneDrive as well. "Last backup: …" under the row tells you how long ago. Livo never backs up on its own and never reminds you with a pop-up.

A backup on the phone is deleted with the app, so keep one off the phone: share it to iCloud Drive, or, with Curator, let Livo copy it to OneDrive.

## Restoring

Tap a backup in the list (on the phone, or from Files, or with Curator under **Backups in OneDrive**) and **Restore**. Restoring replaces what Livo has now (your photos' records, people, places, tags, stories, Memories and learned search data) with what the backup holds; this cannot be undone. It does not touch your Time Capsule files, your Camera Roll, or anything in a cloud account. Swiping a backup on the phone to delete it asks first; a copy in OneDrive stays. On the same phone, every photo links back at once.

## A new phone

Install Livo, allow access to Photos, and restore the backup. Livo finds each photo in the new phone's library by its iCloud identity, then by its content, and re-links it; a photo it cannot find keeps its record and small copy, and is counted ("N photos not found on this phone"). Copy your Time Capsules from the folder where you keep a copy (iCloud Drive, or the old phone's TimeCapsules folder). With Curator, sign in to OneDrive again for OneDrive photos and the Livo Vault folder.

## Check a backup drive (Curator)

A copy of your photos on an external drive is only a backup if it is complete. Under **Check a backup drive**, **Write the check kit** makes two plain files from what Livo knows about every photo (name, size, a fingerprint of its first 64 KB, date): a manifest and a page called **CHECK MY BACKUP - open with Chrome or Edge**. **Write it to OneDrive** puts them in a folder called Livo Archive Check at the top of each signed-in OneDrive, so the next mirror carries them to the drive; **Share the kit…** hands them to AirDrop or Files instead. On the Mac or PC, open the page *from the drive*, tap **Choose the folder**, pick the mirrored folder, and it reports expected, found, match, missing and changed, with the names; **Check fingerprints too** reads the start of each file to confirm it is the same file, and finds photos saved under another name. Nothing is sent anywhere. Before you mirror, mark the OneDrive photo folders **Always keep on this device**, or the mirror copies placeholders. A copy in a cloud account lasts only as long as the account; keep one on a drive you own.
