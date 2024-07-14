# Tethered iOS 15 Downgrade Guide
**Originally written by [@mineek](https://github.com/mineek) for i(Pad)OS 14, modified and updated for simplicity** to (theoretically) support every version of i(Pad)OS 15. Please read the guide in its entirety and follow along closely to ensure nothing goes wrong. This guide does not assist with iCloud bypass, activation lock bypass, MDM bypass, etc. as it uses legitimate activation records. The device is rendered useless without them.

This guide was written specifically for iPads running iPadOS 17. While personally untested, devices with i(Pad)OS 16/18 ***should*** work, though [YMMV](https://dictionary.cambridge.org/us/dictionary/english/ymmv) (I doubt the iPhone X will work). This guide assumes SEP is compatible. If not, take a look at ~~hell~~ [`seprmvr64`](https://github.com/mineek/seprmvr64). `seprmvr64` might actually work with some knowledge from here, just not out of the box unfortunately.

Additionally, this guide **does not take into account devices that have kpp**; refer to the [original guide](https://github.com/mineek/iostethereddowngrade) by [@mineek](https://github.com/mineek) on `kpp`. This guide is for MacOS only, though should be 100% possible with Linux if you know what you're doing. Unsure if it works on Apple Silicon, but ensure you don't use an AMD processor if you're using a Hackintosh. For checkm8, you should use a USB-A to Lightning cable. If your device only has USB-C ports, you can use a USB-C to USB-A adapter; most if not all work.

This guide is officially certified as **bootloop free** assuming you do everything correctly, don't ban me for something that's out of my hands! Remember, this is a ***tethered boot***, not a dualboot. All data on the device will be ***LOST*** as a restore takes place.

This guide is assuming you set up your `$PATH` environment variable to contain a directory which you have access to and can place binaries into. Please edit `~/.bash_profile` or `~/.zshrc`, whichever exists, to add your working directory into `$PATH`. For example, you can add `export PATH="$PATH:/Users/myusername/Desktop/ios15tether"` (replace `/Users/myusername/Desktop/ios15tether` with your working directory; you can determine this by typing `pwd`).

This guide is considered ***complete*** (in the context of "it just works, I guess") and should work if you follow every instruction with a bit of common sense. If you're aware of what you're doing, and something isn't working right / you have an idea for improvement, please consider making a pull request. If this guide seems too much, please consider looking into [downr1n](https://github.com/edwin170/downr1n); the people behind it know what they're doing (this tool does not assist with iCloud bypass, activation lock bypass, MDM bypass, etc.). The tool is messy, unorganized, and honestly buggy, though with common sense it works ***just fine***. Hop off Aaron.

## Table of Contents
- [Requirements](#requirements)
- [Obtaining Activation Records](#obtaining-activation-records)
- [Firmware Keys](#firmware-keys)
- [Restoring](#restoring)
- [Booting](#booting)
- [Replacing Activation Records](#replacing-activation-records)
- [Known Problems](#known-problems)
- [Credits](#credits)

## Requirements
***[Back to Table of Contents](#table-of-contents)***

- You will need the Xcode Command Line Tools; these can be installed with `xcode-select --install`.
- [`irecovery`](https://github.com/libimobiledevice/libirecovery) - download archive from releases, extract, and ***run*** the `install-sh` binary located in the archives extracted directory.
- [`futurerestore`](https://github.com/futurerestore/futurerestore) - download `futurerestore-macOS-DEBUG` archive from latest GitHub Actions workflow run, extract, and take the `futurerestore` binary.
- [`gaster`](https://github.com/0x7ff/gaster) - clone repository, run `make`, and take the binary made.
- `pyimg4` - install the ***latest version*** of [Python](https://www.python.org/downloads/), then run `pip3 install pyimg4` (you may need to restart your terminal in order to run the command).
- [`iBoot64patcher`](https://github.com/Cryptiiiic/iBoot64Patcher) - clone repository, run `build.sh`, and take the binary made.
- [`Kernel64patcher`](https://github.com/edwin170/Kernel64Patcher) - run `wget https://github.com/edwin170/Kernel64Patcher/raw/master/Kernel64Patcher_Darwin -O Kernel64Patcher && chmod +x Kernel64Patcher`, and take the binary downloaded.
- [`img4tool`](https://github.com/tihmstar/img4tool) - download archive from releases, extract, and take the binary located at `{extracted archive directory}/usr/local/bin/img4tool`.
- [`img4`](https://github.com/xerub/img4lib) - ***recursively*** clone repository, run `make -C lzfse && make`, and take the binary made.
- [`restored_external64_patcher`](https://github.com/iSuns9/restored_external64patcher) - clone repository, run `make`, and take the binary made.
- [`asr64_patcher`](https://github.com/iSuns9/asr64_patcher) - clone repository, run `make`, and take the binary made.
- [Homebrew](https://brew.sh/) - if you do not already have homebrew on your system, run `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` in a terminal (I'm so sorry for this).
- `sshpass` - if you do not already have `sshpass` on your system, run `brew tap esolitos/ipa && brew install sshpass` in a terminal.

***Note: Please make sure you are using the repositories listed above. Using outdated / modified forks / binaries can and will make it so this guide doesn't work. These tools MUST be under the $PATH environment variable.***

You will need an `.shsh2` blob from your device. For simplicity sake, you can use [blobsaver](https://github.com/airsquared/blobsaver) (download and install the `.dmg` from releases). Connect your device, read the ECID from the device, and press "Go". Once finished, take the `.shsh2` with the latest i(Pad)OS version listed from the directory listed (may be `~/Blobs`), copy it to your working directory, and rename it to `shsh.shsh2`. ***You cannot use a blob dumped from your device (aka. an "onboard" blob)***. Blobs from blobsaver work just fine.

## Obtaining Activation Records
***[Back to Table of Contents](#table-of-contents)***

You will need to back up your ***activation records*** in order to activate & use the device (if you're thinking about bypassing, you won't be able to jailbreak the device if you patch AMFI). Before restoring your device, update it to latest, activate the device (get to the home screen), jailbreak it (you can use [`palera1n`](https://ios.cfw.guide/installing-palera1n/)) and install `Filza File Manager` from Sileo / Zebra.

1. Open Filza. You should be accessing the following files and directories from the root filesystem.
2. Open `/var/mobile/Documents` and make a folder named `Activation` (you can favorite this directory for ease of access).
3. Open `/var/containers/Data/System`. Then, open the folder that Filza says is `com.apple.mobileactivationd`. Then, open `Library` (you can favorite this directory for ease of access). 
4. From `activation_records`, copy `activation_record.plist` to `/var/mobile/Documents/Activation`.
5. From `internal` (next to `activation_records`), copy `data_ark.plist` to `/var/mobile/Documents/Activation`.
6. Open `/var/containers/Data/System`. Then, open the folder that Filza says is `com.apple.fairplayd.A2`. Then, open `Documents/Library`. Copy the `FairPlay` folder and paste it into `/var/mobile/Documents/Activation`.
7. From `/var/wireless/Library/Preferences`, copy `com.apple.commcenter.device_specific_nobackup.plist` to `/var/mobile/Documents/Activation`.
8. Open `/var/mobile/Documents` and select "Create ZIP" on the `Activation` folder. Hold down the `.zip`, press "Open in", and select "Save to Files".
9. Upload the `.zip` to your computer by either going to [tmpfiles.org](https://tmpfiles.org/) and opening the download link on your computer or using FTP / SSH / SFTP. Save the `.zip` to your working directory and extract it. Make sure the `Activation` folder is inside of your working directory (if the files spill into your working directory, run `mkdir Activation && cp activation_record.plist com.apple.commcenter.device_specific_nobackup.plist data_ark.plist FairPlay Activation`).

Once the `Activation` folder is on your computer, `chmod` it with `sudo chmod -R 755 Activation` (assuming you're in the directory that has the `Activation` folder).

## Firmware Keys
***[Back to Table of Contents](#table-of-contents)***

In order to restore and boot your device, you need to obtain keys for your devices target versions iBoot, iBEC, iBSS, and LLB. One source `futurerestore` looks to for keys is [The Apple Wiki](https://theapplewiki.com/wiki/Firmware_Keys/15.x), so you can check there for keys.

If the link for your device & version combination is blue (and has keys visible when you click it, you can skip to [Restoring](#restoring). If the link for your device & version combination is red, you will need to do extra work, please continue with this section.

A dead simple software I like to use is [Criptam](https://github.com/m1stadev/Criptam), though at the time of writing it's broken. Assuming a fix isn't pushed yet (please check the repository), here's a [fork](https://github.com/immoonlightsonata/Criptam) (`develop` branch) I provided where you can input data via a `.json` file. You can use it like so:

1. Install Poetry by running `curl -sSL https://install.python-poetry.org | python3 -`.
2. Clone the fork mentioned above using `git clone https://github.com/immoonlightsonata/Criptam --branch develop`.

Your device identifier can be found by going to [ipsw.me](https://ipsw.me/), selecting your devices model, and clicking the "Device Information" tab. Alternatively, you could refer to this [GitHub Gist](https://gist.github.com/adamawolf/3048717), though pictures may be easier for you. It'll look similar to `iPad7,1`, take a note of this as your identifier.

When you select a version on [ipsw.me](https://ipsw.me/), you will see the build identifier for that version in parenthesis (ie. `19H12` is the build identifier for iPadOS `15.7`). Take note of this as the build identifier for the version you want keys of.

3. From the repositories main directory, run `./install.sh` to build and install the fork of Criptam.

Now, we need to supply the `fw.json`. You can get this by running `wget https://api.ipsw.me/v4/device/{deviceid} -O fw.json`, where `{deviceid}` is the device identifier of your device (ie. iPad7,1), just remember to not include the `{}`. Ensure you're `cd`'d into the directory where the `fw.json` fie is saved. Please remember you need to update this file if a new version comes out for your device and you wish to obtain keys for it.

For example, running a command like `wget https://api.ipsw.me/v4/device/iPad7,1 -O fw.json` will give me the firmware data for the iPad Pro 2 (12.9-inch, WiFi).

4. Run the following command: `criptam -d {deviceid} -b {buildid}`, where `{deviceid}` is your device identifier (ie. iPad7,1), and `{buildid}` is the build identifier of the version you want keys of (ie. `19H12` for iPadOS `15.7`), just remember to not include the `{}`.

For example, running a command like `criptam -d iPad7,1 -b 19H12` will give me the keys for the iPad Pro 2 (12.9-inch, WiFi) on iPadOS `15.7`.

Take a note of these keys; they will be used to decrypt iBEC and iBSS in the boot process. Though, now we need to set up a server for `futurerestore` to reference for the restore process. Remember, `ivkey` stands for the IV concatenated with the Key; if IV were `123` and the Key were `456` the `ivkey` would be `123456`. Here's a layout of what you should save:

```
Firmware keys:
iBSS IV: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
iBSS Key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

iBEC IV: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
iBEC Key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

LLB IV: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LLB Key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

iBoot IV: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
iBoot Key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

A good reminder of the device & version combination is to write the device identifier and build identifier in your note, so you should do something like replacing

```
Firmware keys:
```

with

```
Firmware keys for J120AP 19H12:
```

You can now serve these keys on your `localhost` server for `futurerestore`.

1. Install prerequisites with `pip3 install requests pyquery Flask`.
2. Download `proxy.py` with `wget https://raw.githubusercontent.com/immoonlightsonata/ios15tether/main/proxy.py`. Ensure this is run in your working directory.
3. In another terminal window, type `python3 proxy.py`.

Now, you need to make the `.json` file for the restore. In your working directory, make a file named `{deviceid}+{buildid}.json`, where `{deviceid}` is the device identifier (ie. `iPad7,1`) and `{buildid}` is the build identifier for the version you're going to (ie. `19H12`), just remember to not include the `{}`. For example, the `iPad7,1` with the `19H12` build identifier should have its `.json` file named `iPad7,1+19H12.json`.

Open the `.json` file and structure it as follows:
```json
{
    "identifier": "",
    "buildid": "",
    "codename": "",
    "keys": [
        {
            "image": "iBEC",
            "filename": "",
            "date": "",
            "iv": "",
            "key": "",
            "kbag": ""
        },
        {
            "image": "iBoot",
            "filename": "",
            "date": "",
            "iv": "",
            "key": "",
            "kbag": ""
        },
        {
            "image": "iBSS",
            "filename": "",
            "date": "",
            "iv": "",
            "key": "",
            "kbag": ""
        },
        {
            "image": "LLB",
            "filename": "",
            "date": "",
            "iv": "",
            "key": "",
            "kbag": ""
        },
        {
            "image": "SEPFirmware",
            "filename": "",
            "date": "",
            "iv": "Unknown",
            "key": "Unknown",
            "kbag": ""
        }
    ]
}
```

- In the `identifier` key, add the device identifier (ie. `iPad7,1`).
- In the `buildid` key, add the build identifier (ie. `19H12`).
- In the `codename` key, add the codename for the version you're going to. For iOS 15, you can use [Wikipedia](https://en.wikipedia.org/wiki/IOS_15#Release_history) for codenames (ie. `SkySecuritySydney` for `15.7`).

The rest should be quite self explanatory. For iBEC, iBoot, iBSS, and LLB, you need to input the `filename` (which is the name of the corresponding file in the `.ipsw`), along with the `iv` & `key` of the file (which you can get from your results with Criptam).

While in your working directory, run this to get the filenames of every component you need (your device must be connected in DFU in order for `irecovery` to work):
```bash
rm BuildManifest.plist && cp extipsw/BuildManifest.plist .
boardconfig=$(irecovery -q | awk '/MODEL/ {print $NF}')
echo -e "\niBSS is: $(awk "/""${boardconfig}""/{x=1}x&&/iBSS[.]/{print;exit}" BuildManifest.plist | grep '<string>' |cut -d\> -f2 |cut -d\< -f1)"
echo "iBEC is: $(awk "/""${boardconfig}""/{x=1}x&&/iBEC[.]/{print;exit}" BuildManifest.plist | grep '<string>' |cut -d\> -f2 |cut -d\< -f1)"
echo "iBoot is: $(awk "/""${boardconfig}""/{x=1}x&&/iBoot[.]/{print;exit}" BuildManifest.plist | grep '<string>' |cut -d\> -f2 |cut -d\< -f1)"
echo "LLB is: $(awk "/""${boardconfig}""/{x=1}x&&/LLB[.]/{print;exit}" BuildManifest.plist | grep '<string>' |cut -d\> -f2 |cut -d\< -f1)"
echo -e "SEPFirmware is: $(awk "/""${boardconfig}""/{x=1}x&&/sep-firmware[.]/{print;exit}" BuildManifest.plist | grep '<string>' |cut -d\> -f2 |cut -d\< -f1)\n"
```
Copy the ***FILENAMES*** (ie. `iBEC.j120.RELEASE.im4p` ***NOT*** `Firmware/dfu/iBEC.j120.RELEASE.im4p`) into their corresponding `filename` keys.

You do ***NOT*** need to fill `SEPFirmware` `iv` or `key`. You do not need to fill any `kbag` keys.

You can now restore, hooray! Don't forget to keep `python3 proxy.py` running.

## Restoring
***[Back to Table of Contents](#table-of-contents)***

Take note of the board configuration of your device. When you're looking at the version list on [ipsw.me](https://ipsw.me/), click the "Device Information" tab and note the `BoardConfig`. For example, the iPad Pro 2 (12.9-inch, WiFi) has a BoardConfig of `J120AP`.

1. Get an `.ipsw` of the `15.x` version you want to go down to. You can download this from [ipsw.me](https://ipsw.me/). Once you obtain the `.ipsw`, rename it to `ipsw.ipsw` and copy it to your working directory.
2. Extract the `.ipsw` with `unzip ipsw.ipsw -d extipsw`.
3. From the `extipsw` directory, copy the kernel cache. The kernel cache should be at the root of the extracted `extipsw` directory and named after your device (ie. `kernelcache.release.ipad7` for the `iPad7,x`, a shortened version related to the device identifier). Copy the kernel cache to your working directory and rename it to `kernelcache`.
4. From the `extipsw` directory, copy the restore ramdisk; you can identify this using the build manifest. You can open `BuildManifest.plist` with TextEdit by either using Finder or `open -e BuildManifest.plist`. Search for "RestoreRamDisk" and look for the second result. Look a couple lines beneath, until you see `<key>Path</key>` under the `RestoreRamDisk` key and dictionaries. The `<string>` underneath the Path key is the name of the restore ramdisk `.dmg`. Copy the `.dmg` with the same name as the `.dmg` in the `<string></string>` to your working directory, and rename it to `restore_ramdisk`.
5. Extract the ramdisk with `img4 -i restore_ramdisk -o ramdisk.dmg`.
6. Mount the ramdisk with `mkdir ramdisk && hdiutil attach ramdisk.dmg -mountpoint ramdisk`.
7. Patch `asr` with `asr64_patcher ramdisk/usr/sbin/asr patched_asr`.
8. Resign the patched `asr` with `ldid -e ramdisk/usr/sbin/asr > ents.plist && ldid -Sents.plist patched_asr`.
9. Copy `restored_external` from the ramdisk with `cp ramdisk/usr/local/bin/restored_external .`.
10. Patch `restored_external` with `restored_external64_patcher restored_external restored_external_patched`.
11. Extract the entitlements from `restored_external` with `ldid -e restored_external > restored_external_ents.plist`.
12. Remove the unpatched `asr` and `restored_external` from the ramdisk with `rm ramdisk/usr/sbin/asr && rm ramdisk/usr/local/bin/restored_external`
13. Sign `restored_external_patched` with `ldid -Srestored_external_ents.plist restored_external_patched`.
14. Change permissions of the patched files to `755` with `chmod -R 755 restored_external_patched && chmod -R 755 patched_asr`.
15. Copy `restored_external_patched` and `patched_asr` into the ramdisk replacing the original files with `cp -a restored_external_patched ramdisk/usr/local/bin/restored_external && cp -a patched_asr ramdisk/usr/sbin/asr`.
16. Detach the ramdisk with `hdiutil detach ramdisk`.
17. Turn the ramdisk `.dmg` into an `.im4p` with `pyimg4 im4p create -i ramdisk.dmg -o ramdisk.im4p -f rdsk`.
18. Extract the kernel cache with `pyimg4 im4p extract -i kernelcache -o kcache.raw`.
19. Patch the kernel cache with `Kernel64Patcher kcache.raw krnl.patched -f -a`.
20. Rebuild the kernel cache with `pyimg4 im4p create -i krnl.patched -o krnl.im4p -f rkrn --lzss`.

Now that your restore files are prepared, you can restore the device with `futurerestore`.

***Optional:*** If you want the device to be in recovery mode instead of DFU on boot (essentially removing the 'fake DFU' from [Known Problems](#known-problems)), you can replace LLB by updating the `.ipsw` with an LLB signed by your `.shsh2`. In order to do that, run the following commands in your working directory (replace `{ipsw url}` with the `.ipsw` URL of the i(Pad)OS version that your `.shsh2` comes from, just remember to not inculde the `{}`):
```bash
mkdir -p Firmware/all_flash
cp extipsw/BuildManifest.plist .
boardconfig=$(irecovery -q | awk '/MODEL/ {print $NF}')
cd Firmware/all_flash
pzb -g "Firmware/all_flash/$(awk "/""${boardconfig}""/{x=1}x&&/LLB[.]/{print;exit}" BuildManifest.plist | grep '<string>' |cut -d\> -f2 |cut -d\< -f1)" {ipsw url}
cd ../..
zip -ur ipsw.ipsw Firmware/all_flash/
```

***Optional:*** If you replaced LLB and want the device to have a graphic when the device is in recovery mode instead of the backlight simply being on, you can replace the RestoreLogo by updating the `.ipsw` with a RestoreLogo signed by your `.shsh2`. In order to do that, run the following commands in your working directory (assuming you already did LLB, replace `{ipsw url}` with the `.ipsw` URL of the i(Pad)OS version that your `.shsh2` comes from, replace `{recoverymode}` with the `.im4p` filename of your devices `recoverymode` `.im4p`; if there is only one `recoverymode` `.im4p` in the `.ipsw` (you can use `pzb -l {ipsw url}` to see the contents of the `.ipsw`), use that, otherwise use the `.im4p` related to your screens resolution (ie. `recoverymode@2732~ipad-lightning.im4p` for the iPad Pro 2 (12.9-inch) as it has a 2732 by 2048 screen resolution (Google yours!), just remember to not include the `{}`):
```bash
boardconfig=$(irecovery -q | awk '/MODEL/ {print $NF}')
cd Firmware/all_flash
pzb -g "Firmware/all_flash/{recoverymode}" {ipsw url}
cd ../..
zip -ur ipsw.ipsw Firmware/all_flash/
```

You can likely add the rest of the firmware payloads from the `.ipsw` following the same process above, though I won't be covering those specifically here since they're less important.

In order to restore the device, you need to first exploit the device with `gaster`. Put your device into [DFU mode](https://theapplewiki.com/wiki/DFU_Mode) and run `gaster pwn && gaster reset`. If `gaster` hangs or goes into a loop, redo the combination for entering DFU mode and run the command again.

If your device has a baseband, run `futurerestore -t shsh.shsh2 --use-pwndfu --skip-blob --rdsk ramdisk.im4p --rkrn krnl.im4p --latest-sep --latest-baseband ipsw.ipsw`. If your device does not have baseband, change `--latest-baseband` to `--no-baseband`. If you are unsure whether or not your device has baseband, try the command with `--latest-baseband`; the restore will fail (your data is untouched) if `futurerestore` errors due to your device not having baseband.

***Note:*** If keys are available on The Apple Wiki but `futurerestore` is unable to obtain them, look into [`m1stadev/wikiproxy`](https://github.com/m1stadev/wikiproxy). Similar to `proxy.py`, it allows `futurerestore` to reference The Apple Wiki for firmware keys. Ensure `wikiproxy` is running while running `futurerestore` so the keys can be obtained successfully.

## Booting
***[Back to Table of Contents](#table-of-contents)***

We need to copy more files from the `extipsw` directory. DeviceTree may be named after your board configuration (ie. `J120AP`), though other components are likely named differently. Please make sure to get the correct files for your device.

While in your working directory, run this to copy and rename the required components (your device must be connected in DFU in order for `irecovery` to function):
```bash
rm BuildManifest.plist && cp extipsw/BuildManifest.plist .
boardconfig=$(irecovery -q | awk '/MODEL/ {print $NF}')
cp -v extipsw/$(awk "/""${boardconfig}""/{x=1}x&&/iBSS[.]/{print;exit}" BuildManifest.plist | grep '<string>' |cut -d\> -f2 |cut -d\< -f1) ibss
cp -v extipsw/$(awk "/""${boardconfig}""/{x=1}x&&/iBEC[.]/{print;exit}" BuildManifest.plist | grep '<string>' |cut -d\> -f2 |cut -d\< -f1) ibec
cp -v extipsw/$(awk "/""${boardconfig}""/{x=1}x&&/DeviceTree[.]/{print;exit}" BuildManifest.plist | grep '<string>' |cut -d\> -f2 |cut -d\< -f1) devicetree
```

In `extipsw`, you should locate the largest `.dmg`'s name. For example, the `J120AP` `19E258` root filesystem `.dmg` is named `078-28735-012.dmg`. From `extipsw/Firmware`, copy the `.trustcache` for the root filesystem `.dmg` (ie. `078-28735-012.dmg.trustcache`) to your working directory and rename it to `rootfs_trustcache`.

Lastly, you need to reopen `BuildManifest.plist`. Search for `IsFUDFirmware` and look through every results entire dictionary; if the `Path` `<key>` has a `<string>` that shows a file ending in `.im4p`, copy the corresponding files to your working directory. These files are all inside of the `extipsw` directory.

Please refer to the [Firmware Keys](#firmware-keys) section of this guide to get `ivkey`'s. If they are on The Apple Wiki, you may use them here. Otherwise, please follow the Criptam guide in getting the keys. Remember, `ivkey` means the IV concatenated with the Key. If the IV is `123` and the Key is `456`, the `ivkey` is `123456`. The keys must be for your exact device and exact i(Pad)OS version you want to go to.

1. Decrypt your `ibss` with `img4 -i ibss -o ibss.dec -k {ibss ivkey}`, where `{ibss ivkey}` is the `ivkey` for iBSS, just remember to not include the `{}`.
2. Decrypt your `ibec` with `img4 -i ibec -o ibec.dec -k {ibec ivkey}`, where `{ibec ivkey}` is the `ivkey` for iBEC, just remember to not include the `{}`.

If you want to ensure your keys are correct, open either `ibss.dec` or `ibec.dec` in a text editor; you should immediately see "Copyright 2007-20xx, Apple Inc." near the top. If the ***entire*** file is gibberish, the keys are invalid.

3. Patch iBSS with `iBoot64Patcher ibss.dec ibss.patched`.
4. Patch iBEC with the verbose boot argument with `iBoot64Patcher ibec.dec ibec.patched -b "-v"`.
5. Create an IM4M with `img4tool -e -s shsh.shsh2 -m IM4M`.
6. Repack iBSS with `img4 -i ibss.patched -o ibss.img4 -M IM4M -A -T ibss`.
7. Repack iBEC with `img4 -i ibec.patched -o ibec.img4 -M IM4M -A -T ibec`.
8. Sign device tree with `img4 -i devicetree -o devicetree.img4 -M IM4M -T rdtr`.
9. Sign root filesystem trustcache with `img4 -i rootfs_trustcache -o rootfs_trustcache.img4 -M IM4M -T rtsc`.

Now, you need to sign every `.im4p` that was copied when you searched `IsFUDFirmware` in the `BuildManifest.plist`. Run `img4 -i {im4p filename} -o {img4 filename} -M IM4M -T {tag}`, where `{im4p filename}` is the filename of one firmwares `.im4p` filename (ie. `aopfw.im4p`), `{img4 filename}` is the filename with `.im4p` replaced with `.img4` (ie. `aopfw.img4`), and `{tag}` is the [`TYPE`](https://theapplewiki.com/index.php?title=TYPE) of the firmware (ie. `aopf`), just remember to not include the `{}`. Make sure you do ***every firmware***.

10. Patch the kernel cache with `Kernel64Patcher kcache.raw krnlboot.patched -b15 -r -o -e`, make sure you are using the correct fork!
11. Repack the kernel into an `.im4p` with `pyimg4 im4p create -i krnlboot.patched -o krnlbootim4p -f rkrn --lzss`.
11. Repack the kernel into an `.img4` with `pyimg4 img4 create -p krnlboot.im4p -o krnlboot.img4 -m IM4M`.

You're now ready to boot. You can automate the boot process by copying your iBEC, iBSS, device tree, `krnlboot`, root filesystem trustcache, and all firmware `.img4`'s into a separate directory for ease of access.

To boot the device, you need to enter [DFU mode](https://theapplewiki.com/wiki/DFU_Mode), run `gaster pwn && gaster reset`, and run the following commands (do ***NOT*** run `irecovery -c go` if your device does not have an A10 or higher chipset):

```bash
irecovery -f ibss.img4
sleep 2
irecovery -f ibec.img4
{go}
sleep 2
irecovery -f devicetree.img4
irecovery -c devicetree
{firmwares}
irecovery -f rootfs_trustcache.img4
irecovery -c firmware
irecovery -f krnlboot.img4
irecovery -c bootx
```

If your device has an A10 or above chipset (Google your device name alongside the word "chipset"), replace `{go}` in the command with `irecovery -c go`. If your device is not A10 or above, do not add anything (remove `{go}`).

For `{firmwares}`, you need to send every `IsFUDFirmware` firmware made into an `.img4`. You need to replace `{firmwares}` with these two lines for ***every*** firmware:

```bash
irecovery -f {firmware img4 filename}
irecovery -c
```

where `{firmware img4 filename}` is the `.img4` filename of the firmware (ie. `aopfw.img4`), just don't include the actual `{firmwares}`. You can save this elsewhere as `boot.sh` (make sure to copy all files required too!). Here's an example of `boot.sh` for the `J120AP` `19E258`:

```bash
gaster pwn
gaster reset
irecovery -f ibss.img4
sleep 2
irecovery -f ibec.img4
irecovery -c go
sleep 2
irecovery -f devicetree.img4
irecovery -c devicetree
irecovery -f avefw.img4
irecovery -c firmware
irecovery -f aopfw.img4
irecovery -c firmware
irecovery -f rootfs_trustcache.img4
irecovery -c firmware
irecovery -f krnlboot.img4
irecovery -c bootx
```

Since (besides the root filesystem trustcache) there is the AVE and AOP firmware, they've both been added along with their `-c` commands. Since the device is A10X, it includes `-c go`. ***Do not use this script for your device; please only use it as a template***. You need to keep in the `sleep` commands though, and if they are insufficient, make them a few seconds longer.

## Replacing Activation Records
***[Back to Table of Contents](#table-of-contents)***

Once the device has booted, attempt to set up the device. You'll be met with an error saying "Unable to Activate", this is normal.

1. Clone and enter `SSHRD_Script` with `git clone --recursive https://github.com/verygenericname/SSHRD_Script && cd SSHRD_Script`.
2. Redo the button combination to enter [DFU mode](https://theapplewiki.com/wiki/DFU_Mode).
3. Make a ramdisk by running `./sshrd.sh {version}`, where `{version}` is the i(Pad)OS version you restored to (ie. `15.7`). If the script hangs on "Getting device info and pwning", restart from step 2. If the script stops on "[-] An error occurred", restart from step 3.
4. Boot the ramdisk with `./sshrd.sh boot`. Wait for the device to stop moving text on the screen.
5. Enter SSH with `./sshrd.sh ssh`.

In the SSH terminal, run the following commands:

```bash
mount_filesystems
find /mnt2/containers/Data/System -name internal
```

The second command will return something along the lines of `/mnt2/containers/Data/System/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/Library/internal`. Take off `/Library/internal` at the end and put it into the next command (after `rm -rf`):

```bash
rm -rf /mnt2/containers/Data/System/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
```

6. Enter [DFU mode](https://theapplewiki.com/wiki/DFU_Mode) and boot the device normally by [Booting](#booting). Attempt to activate the device again.
7. Redo the button combination to enter [DFU mode](https://theapplewiki.com/wiki/DFU_Mode).
8. Boot into the ramdisk by running `./sshrd.sh boot`. Wait for the device to stop moving text on the screen.
9. Enter SSH with `./sshrd.sh ssh`.
10. Mount filesystems with `mount_filesystems`. Wait until the command finishes.
11. Run `exit`. Then, run `cd Darwin && killall iproxy && ./iproxy 2222 22 &` (ignore process not found error).
12. Run `./iproxy 2222 22 &`.

This terminal tab will be running in the background, you do not need to interact with it!

13. Open a new terminal tab / process and `cd` into the `SSHRD_Script` directory. Then, connect to SSH with `./sshrd.sh ssh`.

This terminal tab will be referred to as the "SSH console".

14. Open a new terminal tab / process.

This terminal tab will be referred to as the "normal console".

***In the normal console:***
```bash
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 rm -rf /mnt2/mobile/Media/Downloads/1
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 rm -rf /mnt2/mobile/Media/1
```

***In the SSH console:***
```bash
mkdir /mnt2/mobile/Media/Downloads/1
mkdir /mnt2/mobile/Media/Downloads/1/Activation
```

***In the normal console (ensure you are in your working directory, and the `Activation` folder with activation records exists in the current directory):***
```bash
sshpass -p alpine scp -rP 2222 -o StrictHostKeyChecking=no Activation root@localhost:/mnt2/mobile/Media/Downloads/1
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 mv -f /mnt2/mobile/Media/Downloads/1 /mnt2/mobile/Media
```

***In the SSH console:***
```bash
chown -R mobile:mobile /mnt2/mobile/Media/1
```

***In the normal console:***
```bash
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 chmod -R 755 /mnt2/mobile/Media/1
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 chmod 644 /mnt2/mobile/Media/1/Activation/activation_record.plist
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 chmod 644 /mnt2/mobile/Media/1/Activation/data_ark.plist
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 chmod 644 /mnt2/mobile/Media/1/Activation/com.apple.commcenter.device_specific_nobackup.plist
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 killall backboardd
sleep 12
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 mv -f /mnt2/mobile/Media/1/Activation/FairPlay /mnt2/mobile/Library/FairPlay
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 chmod 755 /mnt2/mobile/Library/FairPlay
ACT1=$(sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 find /mnt2/containers/Data/System -name internal)
ACT2=${ACT1%?????????????????}
ACT3=$ACT2/Library/internal/data_ark.plist
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 chflags nouchg $ACT3
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 mv -f /mnt2/mobile/Media/1/Activation/data_ark.plist $ACT3
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 chmod 755 $ACT3
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 chflags uchg $ACT3
ACT4=$ACT2/Library/activation_records
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 mkdir $ACT4
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 mv -f /mnt2/mobile/Media/1/Activation/activation_record.plist $ACT4/activation_record.plist
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 chmod 755 $ACT4/activation_record.plist
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 chflags uchg $ACT4/activation_record.plist
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 chflags nouchg /mnt2/wireless/Library/Preferences/com.apple.commcenter.device_specific_nobackup.plist
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 mv -f /mnt2/mobile/Media/1/Activation/com.apple.commcenter.device_specific_nobackup.plist /mnt2/wireless/Library/Preferences/com.apple.commcenter.device_specific_nobackup.plist
```

(Ignore any errors related to processes)

***In the SSH console:***
```bash
chown root:mobile /mnt2/wireless/Library/Preferences/com.apple.commcenter.device_specific_nobackup.plist
```

***In the normal console:***
```bash
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 chmod 755 /mnt2/wireless/Library/Preferences/com.apple.commcenter.device_specific_nobackup.plist
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 chflags uchg /mnt2/wireless/Library/Preferences/com.apple.commcenter.device_specific_nobackup.plist
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 launchctl unload /System/Library/LaunchDaemons/com.apple.mobileactivationd.plist
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 launchctl load /System/Library/LaunchDaemons/com.apple.mobileactivationd.plist
sshpass -p alpine ssh -o StrictHostKeyChecking=no root@localhost -p 2222 ldrestart
```

(Ignore any errors related to commands not being found)

15. Enter [DFU mode](https://theapplewiki.com/wiki/DFU_Mode) and boot the device normally by [Booting](#booting). Attempt to activate the device again.

## Known Problems
***[Back to Table of Contents](#table-of-contents)***

- As the name suggests, this is a tethered boot. You need access to a computer every time you want to boot if the device dies or panics. While stability is essentially perfect, the device can still panic while jailbreaking, so if you intend to jailbreak please do so before you lose access to a computer.
- Activation records cannot be used twice (somewhat). While you can activate and use the device, you cannot log in to iCloud. You need to restore the device to latest, activate the device, back up the new activation records, restore to `15.x`, and add the new activation records.
- AltStore / SideStore / Sideloadly etc. ***will not work*** (this also includes applications installed via `itms-services://`) as you cannot verify applications from "VPN(, DNS,) & Device Management". If your device does not support TrollHelperOTA, follow these steps to install TrollStore:

1. Install [Tips](https://apps.apple.com/us/app/tips/id1069509450) from the App Store.
2. In the `SSHRD_Script` directory, run `./sshrd.sh {version} TrollStore Tips`, where `{version}` is the i(Pad)OS version you downgraded to, just remember to not include the `{}`.
3. Boot the new ramdisk with `./sshrd.sh boot`. Wait for the installation to finish.
4. Remove the TrollStore ramdisk with `./sshrd.sh clean`.
5. Enter [DFU mode](https://theapplewiki.com/wiki/DFU_Mode) and boot the device normally by [Booting](#booting).

TrollStore Helper should now be installed into the Tips app. Open the Tips app and install TrollStore. If Tips doesn't say "Uninstall Persistence Helper", register Tips as a persistence helper.

- Currently, you cannot set a passcode / enable any biometrics. Your device will panic if you enable a passcode, though a force reboot reverts the changes. If jailbroken, you can install [FakePass](https://repo.alexia.lol/), though it will ***only work while jailbroken***. Install the tweak, respring, and attempt to set a passcode in the Settings app. This tweak does not provide real security, though would prompt a potential intruder to restore the device as rebooting simply enters DFU (they cannot boot as they do not have the required files). Please do ***not*** keep sensitive information on the device, even if you are jailbroken 24/7 as either simply forgetting to jailbreak or someone knowing what files are required to boot instantly compromise the security of your device.
- If you didn't replace LLB, the device will look ***bricked*** after a reboot as it's now in a kind of "fake" DFU mode. You will still need to do the [DFU mode](https://theapplewiki.com/wiki/DFU_Mode) button combination to enter real DFU, else running `gaster pwn` will make your terminal go in a loop (press `Ctrl + C` to stop `gaster`). If LLB is replaced, you can use normal DFU helpers like `palera1n -D` or holding the [DFU mode](https://theapplewiki.com/wiki/DFU_Mode) button combination, you just don't need to worry about "fake" DFU. You can turn off the device by holding the force reboot button combination and letting go once the device backlight turns off (assuming LLB is replaced).
- A tweak that causes SpringBoard to crash ***may*** put your device into a respring loop, albeit unlikely. Hold the Volume Up button while the device is respringing to enter safe mode if this occurs (you may need to keep the button held down upwards of 30 seconds).
- You need have opened the Messages app first to be able to enable Messages in iCloud settings.
- Cellular service should work, though is untested.
- The ability to make calls should work, though is untested.
- The ability to send and receive SMS texts should work, though is untested.

## Credits
***[Back to Table of Contents](#table-of-contents)***

- [@mineek](https://github.com/mineek) for writing the original guide and providing general support concerning this repository.
- [@edwin170](https://github.com/edwin170) for providing general support concerning this repository.
- [@pwnapplehat](https://github.com/pwnapplehat) for [updating the orangera1n activation records guide](https://gist.github.com/pwnapplehat/f522987068932101bc84a8e7e056360d).
- All developers & repository owners of the software used in this guide listed under [Requirements](#requirements).
