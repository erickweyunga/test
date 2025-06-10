---
title: "How to Upgrade Your package.json Dependencies"
seoTitle: "How to Upgrade Your package.json Dependencies"
seoDescription: "How to Upgrade Your package.json Dependencies"
datePublished: Tue Jun 10 2025 08:22:48 GMT+0000 (Coordinated Universal Time)
cuid: cmbq96r9m000j02jucejq0zz7
slug: how-to-upgrade-your-packagejson-dependencies
tags: javascript, npm, typescript, packagejson

---

Keeping your dependencies up to date is important for security, performance, and access to new features. Here's a quick guide to upgrading your `package.json` packages — no fluff, just what you need.

---

## 1\. Upgrade All to Latest (NPM)

Use [`npm-check-updates`](https://www.npmjs.com/package/npm-check-updates) to update everything to the latest versions:

```bash
npm install -g npm-check-updates
ncu -u
npm install
```

* `ncu -u` updates `package.json` with the latest versions.
    
* `npm install` installs them.
    

---

## 2\. Upgrade a Specific Package

```bash
npm install package-name@latest
```

Want a specific version?

```bash
npm install package-name@^2.0.0
```

---

## 3\. Patch/Minor Updates Only

```bash
npm update
```

This respects version ranges (like `^1.2.0`) and keeps things safe.

---

## If You Use Bun

```bash
bun upgrade
```

Or upgrade a single package:

```bash
bun add package-name@latest
```

---

## For Yarn Users

```bash
yarn upgrade --latest
```

---

## Final Tips

* Always check your app after updates.
    
* Review your lock files (`package-lock.json`, `bun.lockb`, or `yarn.lock`).
    
* Use version ranges wisely (`^`, `~`, or exact).
    

Stay updated, stay safe!