# Launcher and updater help

Draft, October 24, 2026. Based on the player package source; the package currently available to download has not been checked.

## First run

Unzip the whole package and keep its files together. Double-click **Play Shattered Legacy.bat**.

The launcher looks for usable Ultima Online files. If it cannot find an installation, it offers EA's free installer. Accept EA's license yourself, then leave EA's launcher open while it downloads the game. The package README estimates about 1.8 GB to download and about 3 GB of free drive space. This can take much longer than preparing Shattered Legacy's art.

The Shattered Legacy window continues automatically when EA finishes. Do not click Play in EA's window, which connects to EA's servers. If your existing installation needs an EA update, let that finish too.

The current launcher targets the **TEST shard**, where accounts, characters, and items can be wiped. At the login screen, choose an account name and password and keep them for later logins.

## Windows SmartScreen

The package is unsigned, so Windows may show **Windows protected your PC**. For the package you obtained from Shattered Legacy, choose **More info**, then **Run anyway**. For **Open File - Security Warning**, choose **Run**. If you are unsure where the package came from or what a warning means, ask Chase before proceeding.

## Updates

When you see **Update now? [Y/n]**, press Enter to download and install the update, or type `n` to skip it until next time. The update continues in a new window. Close the game if that window asks you to. Updates keep your saved settings, account details, Ultima Online folder, and window positions. If the update server cannot be reached, Play continues with your installed version.

## Preparing the art and map

After an update, you may see **Preparing Shattered Legacy art and map**. Its progress bar shows the current step, a count when available, and elapsed seconds. The count belongs to that step, so it can change when the next step starts. It normally finishes in a few seconds.

The rebuild has a default one-minute wait. If it is still running, the launcher is designed to continue with your previous art, or without the custom art on a first install. Preparation continues in the background. Once it finishes, a later normal start can use the new art. Other launcher steps can take longer, so one minute is not a guaranteed total launch time.

## If Play seems stuck

1. Check the launcher and updater windows for a question, a request to close the game, or a Windows permission prompt. During EA's download, check EA's window and your internet connection.
2. If EA's launcher closed before the game files were ready, check your connection and free space, then run **Play Shattered Legacy.bat** again.
3. If art preparation stays stuck, capture the window and close the stuck launcher before trying **app\Play-Skip-Art.bat** once. If offered an update during this attempt, type `n`. This shortcut skips only the art check and rebuild. Setup and connection checks still apply, and custom art may be missing or older. Use normal Play again later.
4. For **Cannot reach Shattered Legacy**, wait a few minutes and retry. If it continues, tell Chase. The skip-art shortcut cannot fix a connection problem.

## Logs to send Chase

Open the folder where you unzipped the package. Send the newest relevant files, plus a screenshot of the last message:

- `app\logs\launch-*.log`: what the launcher window said.
- `app\logs\overrides-*.log`: art and map preparation timings, if a rebuild started.
- `update-log.txt` beside **Play Shattered Legacy.bat**: updater messages if the update failed.

If a log is missing, say so and send what you have.
