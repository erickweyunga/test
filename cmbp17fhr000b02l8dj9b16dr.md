---
title: "Resolving the “google-services.json is missing” error in Expo SDK 53"
seoTitle: "Resolving the “google-services.json is missing” error in Expo SDK 53"
seoDescription: "Resolving the “google-services.json is missing” error in Expo SDK 53"
datePublished: Mon Jun 09 2025 11:51:36 GMT+0000 (Coordinated Universal Time)
cuid: cmbp17fhr000b02l8dj9b16dr
slug: resolving-the-google-servicesjson-is-missing-error-in-expo-sdk-53
cover: https://cdn.hashnode.com/res/hashnode/image/upload/v1749469798514/6d1c21f2-f2d3-41a6-b475-8f06018e5260.png
ogImage: https://cdn.hashnode.com/res/hashnode/image/upload/v1749469867299/b48f03b2-a556-4432-9d4f-4bb562e798f0.png
tags: firebase, react-native, expo

---

During an EAS Build or **expo prebuild**, Expo will try to include the Android Firebase configuration file (`google-services.json`) if you set `android.googleServicesFile` in your app config. The error above occurs because EAS could *not* find the file at `/home/expo/workingdir/build/google_secrets/google-services.json`. In your case, the `googleServicesFile` is set to `./google_secrets/google-services.json`, but your logs and config show that `/google_secrets` is listed in `.gitignore`. This means the file is **not tracked by Git**, so EAS never sees it. By default **EAS Build only uploads files that are committed to the repo** – any ignored files won’t be present on the build server. In short, the build fails because the `google-services.json` file is missing in the build context. Expo’s documentation confirms that you must provide this file for the Android standalone build (it enables FCM and other Firebase services)[docs.expo.dev](https://docs.expo.dev/guides/google-authentication/#:~:text=If%20you%20use%20the%20Firebase,make%20them%20available%20in%20EAS)[docs.expo.dev](https://docs.expo.dev/versions/latest/config/app/#:~:text=).

## Why the file wasn’t included

The error message even hints at the cause: “EAS Build only uploads files tracked by git. Use EAS environment variables to provide EAS Build with the file.” In your project, `.gitignore` contains `/google_secrets`, so the `google-services.json` is explicitly ignored. As a result, when the build runs, the `withAndroidDangerousBaseMod` (Expo’s native config plugin) cannot copy the file into the Android project, and you get the ENOENT error shown. Expo’s official guides note that you can either check these Firebase config files into your repo *or* treat them as secrets. For example, the Expo Google Sign-In guide says you can “check them into your repository because the files should not contain sensitive values, or you can treat the files as secrets, add them to .gitignore and use the guide below to make them available in EAS.”[docs.expo.dev](https://docs.expo.dev/guides/google-authentication/#:~:text=If%20you%20use%20the%20Firebase,make%20them%20available%20in%20EAS). In other words, either commit the file or use the EAS secrets mechanism.

## Solutions

**Option 1: Include the file in your repository.** The simplest fix is to remove `google-services.json` (or the `google_secrets/` directory) from `.gitignore` and commit the file to Git. Expo’s documentation explicitly allows this: it notes that `google-services.json` “should not contain sensitive values” and may be checked into the repository[docs.expo.dev](https://docs.expo.dev/guides/google-authentication/#:~:text=If%20you%20use%20the%20Firebase,make%20them%20available%20in%20EAS). If you commit it, the EAS build will find it (at `android/app/google-services.json` after prebuild) and the error will go away. *However*, committing these files is a security decision – while they often contain only API keys that are not highly secret, some teams prefer not to store them in VCS. If you opt to commit, ensure the path in `app.json` matches (e.g. `"googleServicesFile": "./google-services.json"` if it’s at the project root).

**Option 2 (recommended): Use an EAS secret file.** Expo’s modern workflow encourages using **EAS environment variables** (secrets) to supply this file to the build, rather than checking it into Git. You create a secret of type *file* on your Expo project, upload the `google-services.json` to it, and then reference that secret in your app config. For example, you might run:

```bash
bashCopyEditeas env:create --scope project --name GOOGLE_SERVICES_JSON --type file --value ./google-services.json
```

This command (per Expo’s docs) creates a project-scoped secret named `GOOGLE_SERVICES_JSON` containing your `google-services.json` file[stackoverflow.com](https://stackoverflow.com/questions/78301058/expo-push-notifications-google-services-json-is-missing-for-firebase#:~:text=Step%203%3A%20Run%20this%20command,in%20the%20project%20root%20directory). Once that is done, modify your app config (for a dynamic config you need `app.config.js` or `app.config.ts` instead of a static JSON) so that it uses this environment variable for the path. For instance:

```javascript
jsCopyEdit// app.config.js
export default {
  expo: {
    // ... other settings ...
    android: {
      // Use the EAS secret; fallback to a local path for development
      googleServicesFile: process.env.GOOGLE_SERVICES_JSON 
                          || "./google-services.json",
      // ... other android settings ...
    }
  }
};
```

Here, `process.env.GOOGLE_SERVICES_JSON` is the content of the secret you uploaded, and Expo’s EAS build system will substitute it at build time. The official EAS docs even illustrate this approach: “The `GOOGLE_SERVICES_JSON` is a secret file variable ... used to provide the git ignored google-services.json file to the build job. To use it in the app config, you can use the `process.env` variable and provide a fallback value in case the variable is not set (for local development)”[docs.expo.dev](https://docs.expo.dev/eas/environment-variables/#:~:text=The%20,it%20inside%20your%20project%27s%20repository)[docs.expo.dev](https://docs.expo.dev/eas/environment-variables/#:~:text=Copy). In short, Expo recommends storing the JSON file as an EAS secret and pointing `android.googleServicesFile` to `process.env.GOOGLE_SERVICES_JSON`[stackoverflow.com](https://stackoverflow.com/questions/78301058/expo-push-notifications-google-services-json-is-missing-for-firebase#:~:text=The%20file%20google,it%20in%20my%20app%20config)[docs.expo.dev](https://docs.expo.dev/eas/environment-variables/#:~:text=app).

After these changes, run your EAS build again. The secret file will be injected, and the build process can copy it into `android/app/google-services.json` as needed. As one community answer summarizes, “the file google-services.json should be in android/app and can’t be in .gitignore. You can set google-services.json as an expo secret in your project \[on expo.dev\]… using `googleServicesFile: process.env.GOOGLE_SERVICES_JSON` in your app config”[stackoverflow.com.](https://stackoverflow.com/questions/78301058/expo-push-notifications-google-services-json-is-missing-for-firebase#:~:text=The%20file%20google,it%20in%20my%20app%20config) This matches Expo’s guidance and should resolve the error without checking the secret file into your repo.

**In summary:** The error means the Firebase config file is missing in the build. Make sure EAS can access it – either commit the file into version control or (preferably) upload it as an EAS secret and reference it via `process.env.GOOGLE_SERVICES_JSON` in your Expo config[docs.expo.dev](https://docs.expo.dev/guides/google-authentication/#:~:text=If%20you%20use%20the%20Firebase,make%20them%20available%20in%20EAS)[docs.expo.dev](https://docs.expo.dev/eas/environment-variables/#:~:text=The%20,it%20inside%20your%20project%27s%20repository). This will allow the build to find and copy `google-services.json` correctly.

**Sources:** Expo documentation on Google/Firebase setup and EAS secrets[docs.expo.dev](https://docs.expo.dev/guides/google-authentication/#:~:text=If%20you%20use%20the%20Firebase,make%20them%20available%20in%20EAS)[docs.expo.dev](https://docs.expo.dev/eas/environment-variables/#:~:text=The%20,it%20inside%20your%20project%27s%20repository); community solutions for using `process.env.GOOGLE_SERVICES_JSON` and the `eas env:create` workflow[stackoverflow.com](https://stackoverflow.com/questions/78301058/expo-push-notifications-google-services-json-is-missing-for-firebase#:~:text=The%20file%20google,it%20in%20my%20app%20config)[stackoverflow.com.](https://stackoverflow.com/questions/78301058/expo-push-notifications-google-services-json-is-missing-for-firebase#:~:text=Step%203%3A%20Run%20this%20command,in%20the%20project%20root%20directory)

Citations

![Favicon](https://www.google.com/s2/favicons?domain=https://docs.expo.dev&sz=32 align="left")

[Using Google authentication - Expo Documentation](https://docs.expo.dev/guides/google-authentication/#:~:text=If%20you%20use%20the%20Firebase,make%20them%20available%20in%20EAS)

[https://docs.expo.dev/guides/google-authentication/](https://docs.expo.dev/guides/google-authentication/#:~:text=If%20you%20use%20the%20Firebase,make%20them%20available%20in%20EAS)

![Favicon](https://www.google.com/s2/favicons?domain=https://docs.expo.dev&sz=32 align="left")

[app.json / app.config.js - Expo Documentation](https://docs.expo.dev/versions/latest/config/app/#:~:text=)

[https://docs.expo.dev/versions/latest/config/app/](https://docs.expo.dev/versions/latest/config/app/#:~:text=)

[react native - expo push notifications "google-services.json" is missing for firebase - Stack Overflow](https://stackoverflow.com/questions/78301058/expo-push-notifications-google-services-json-is-missing-for-firebase#:~:text=Step%203%3A%20Run%20this%20command,in%20the%20project%20root%20directory)

[https://stackoverflow.com/questions/78301058/expo-push-notifications-google-services-json-is-missing-for-firebase](https://stackoverflow.com/questions/78301058/expo-push-notifications-google-services-json-is-missing-for-firebase#:~:text=Step%203%3A%20Run%20this%20command,in%20the%20project%20root%20directory)

![Favicon](https://www.google.com/s2/favicons?domain=https://docs.expo.dev&sz=32 align="left")

[Environment variables in EAS - Expo Documentation](https://docs.expo.dev/eas/environment-variables/#:~:text=The%20,it%20inside%20your%20project%27s%20repository)

[https://docs.expo.dev/eas/environment-variables/](https://docs.expo.dev/eas/environment-variables/#:~:text=The%20,it%20inside%20your%20project%27s%20repository)

![Favicon](https://www.google.com/s2/favicons?domain=https://docs.expo.dev&sz=32 align="left")

[Environment variables in EAS - Expo Documentation](https://docs.expo.dev/eas/environment-variables/#:~:text=Copy)

[https://docs.expo.dev/eas/environment-variables/](https://docs.expo.dev/eas/environment-variables/#:~:text=Copy)

[react native - expo push notifications "google-services.json" is missing for firebase - Stack Overflow](https://stackoverflow.com/questions/78301058/expo-push-notifications-google-services-json-is-missing-for-firebase#:~:text=The%20file%20google,it%20in%20my%20app%20config)

[https://stackoverflow.com/questions/78301058/expo-push-notifications-google-services-json-is-missing-for-firebase](https://stackoverflow.com/questions/78301058/expo-push-notifications-google-services-json-is-missing-for-firebase#:~:text=The%20file%20google,it%20in%20my%20app%20config)

![Favicon](https://www.google.com/s2/favicons?domain=https://docs.expo.dev&sz=32 align="left")

[Environment variables in EAS - Expo Documentation](https://docs.expo.dev/eas/environment-variables/#:~:text=app)

[https://docs.expo.dev/eas/environment-variables/](https://docs.expo.dev/eas/environment-variables/#:~:text=app)