# Madeira Source (Unofficial)

An auto-updating AltStore / SideStore source for [Madeira](https://github.com/willfaust/Madeira), which runs Windows PC games on iPhone without a jailbreak.

Add this source once, and new Madeira releases will appear as updates in your sideloading app.

## Source URL

```
https://tinustk.github.io/madeira-source-unofficial/source.json
```

## How to add it

**SideStore / AltStore**
1. Open the app and go to **Sources** (or **Browse → Sources**).
2. Tap **+**.
3. Paste the source URL above and confirm.
4. Madeira will appear in the source. Install it from there, or update your existing copy.

**Other apps (Feather, ESign, etc.)**
Look for **Sources** or **Repos**, tap **+** / **Add**, and paste the same URL.

## How it works

A GitHub Action checks [Madeira's releases](https://github.com/willfaust/Madeira/releases) every 6 hours. When a new IPA is published, it reads the app's version and bundle ID from it and rebuilds `source.json`. Downloads come straight from the official Madeira releases. Nothing is re-hosted or modified.

## Before you install

- Madeira needs **JIT** to run games (via StikDebug or its built-in helper). See the official [JIT setup guide](https://github.com/willfaust/Madeira/blob/main/docs/JIT.md).
- The official README recommends **iOS 26 or later**.
- With a free Apple ID, sideloaded apps expire after 7 days and need refreshing.

## Disclaimer

This is an **unofficial** source and isn't affiliated with the Madeira project. All credit goes to [Will Faust](https://github.com/willfaust) and the Madeira contributors. For bugs or support with the app itself, use the [official repo](https://github.com/willfaust/Madeira) or the [Madeira Discord](https://discord.gg/4t5mNjwCn7).
