# Tethered iOS 15 Downgrade Guide
**Originally written by [@mineek](https://github.com/mineek), modified and updated by [@dleovl](https://github.com/dleovl)** to (theoretically) support every version of i(Pad)OS 15. Please read the guide in its entirety and follow along closely to ensure nothing goes wrong.

This guide was written specifically for iPads running iPadOS 17. While personally untested, devices with i(Pad)OS 16/18 ***should*** work, though [YMMV](https://dictionary.cambridge.org/us/dictionary/english/ymmv). This guide assumes SEP is compatible. If not, take a look at ~~hell~~ [`seprmvr64`](https://github.com/mineek/seprmvr64). `seprmvr64` might actually work with some knowledge from here, just not out of the box unfortunately.

Additionally, this guide **does not take into account devices that have kpp** (do any 15 devices even have `kpp`...?). This guide is for MacOS only, though should be 100% possible with Linux if you know what you're doing.

This guide is officially certified as **bootloop free** (assuming you do everything correctly, don't ban me for something that's out of my hands)! Remember, this is a ***tethered boot***, not a dualboot. All data on the device will be ***LOST***.

This guide is assuming you set up your `$PATH` environment variable to contain a directory which you have access to and can place binaries into. Please edit `~/.bash_profile` or `~/.zshrc`, whichever exists, to add your working directory into `$PATH`. For example, you can add `export PATH="$PATH:/Users/myusername/Desktop/ios15tether"`.

## Requirements
- You will need the Xcode Command Line Tools; these can be installed with `xcode-select --install`.
- [`irecovery`](https://github.com/libimobiledevice/libirecovery) - download archive from releases, extract, and ***run*** the `install-sh` binary located in the archives extracted directory.
- [`futurerestore`](https://github.com/futurerestore/futurerestore) - download `futurerestore-macOS-DEBUG` archive from latest GitHub Actions workflow run, extract, and take the `futurerestore` binary.
- [`gaster`](https://github.com/0x7ff/gaster) - clone repository, run `make`, and take the binary made.
- `pyimg4` - install the latest version of [Python](xhttps://www.python.org/downloads/), then run `pip3 install pyimg4` (you may need to restart your terminal in order to run the command).
- [`iBoot64patcher`](https://github.com/Cryptiiiic/iBoot64Patcher) - clone repository, run `build.sh`, and take the binary made.
- [`Kernel64patcher`](https://github.com/edwin170/Kernel64Patcher) - clone repository, run `gcc Kernel64Patcher.c -o Kernel64Patcher`, and take the binary made.
- [`img4tool`](https://github.com/tihmstar/img4tool) - download archive from releases, extract, and take the binary located at `{extracted archive directory}/usr/local/bin/img4tool`.
- [`img4`](https://github.com/xerub/img4lib) - ***recursively*** clone repository, run `make -C lzfse && make`, and take the binary made.
- [`ldid`](https://github.com/ProcursusTeam/ldid) - download binary from releases, and rename binary to `ldid`.
- [`restored_external64_patcher`](https://github.com/iSuns9/restored_external64patcher) - clone repository, run `make`, and take the binary made.
- [`asr64_patcher`](https://github.com/iSuns9/asr64_patcher) - clone repository, run `make`, and take the binary made.

***Note: Please make sure you are using the repositories listed above. Using outdated / modified forks / binaries can and will make it so this guide doesn't work. These tools MUST be under the $PATH environment variable.***

You will need to back up your ***activation records*** in order to activate & use the device (if you're thinking about bypassing, you won't be able to jailbreak the device if you patch AMFI). Before restoring your device, update it to latest, activate the device (get to the home screen), jailbreak it (you can use [`palera1n`](https://ios.cfw.guide/installing-palera1n/)) and install `Filza File Manager 64-bit`. You can then follow [this guide](https://gist.github.com/pwnapplehat/f522987068932101bc84a8e7e056360d) to figure out what files and directories need to be backed up.
<!-- TODO -->

You will need an `.shsh2` blob from your device. For simplicity sake, you can use [blobsaver](https://github.com/airsquared/blobsaver) (download and install the `.dmg` from releases). Connect your device, read the ECID from the device, and press "Go". Once finished, take the `.shsh2` with the latest i(Pad)OS version listed from the directory listed (may be `~/Blobs`), copy it to your working directory, and rename it to `shsh.shsh2`. ***You cannot use a blob dumped from your device (aka. an 'onboard' blob)***. Blobs from blobsaver work just fine.

## Firmware Keys
In order to restore and boot your device, you need to obtain keys for your devices target versions iBoot, iBEC, iBSS, and LLB. One source `futurerestore` looks to for keys is [The Apple Wiki](https://theapplewiki.com/wiki/Firmware_Keys/15.x), so you can check there for keys. If the link for your device & version combination is red, you will need to do extra work.

A dead simple software I like to use is [Criptam](https://github.com/m1stadev/Criptam), though at the time of writing it's broken because [ipsw.me](https://ipsw.me/) is incompetent ~~(as always)~~. Assuming a fix isn't pushed yet (please check the repository), here's a [fork](https://github.com/dleovl/Criptam) I provided where you can input data via a `.json` file. You can use it like so:

1. Install Poetry by running `curl -sSL https://install.python-poetry.org | python3 -`.
2. Clone the fork mentioned above using `git clone https://github.com/dleovl/Criptam --branch develop`.

Your device identifier can be found by going to [ipsw.me](https://ipsw.me/), selecting your devices model, and clicking the "Device Information" tab. Alternatively, you could refer to this [GitHub Gist](https://gist.github.com/adamawolf/3048717), though pictures may be easier for you. It'll look similar to `iPad7,1`, take a note of this as your identifier.

When you select a version on [ipsw.me](https://ipsw.me/), you will see the build identifier for that version in parenthesis (ie. `19H12` is the build identifier for iPadOS 15.7). Take note of this as the build identifier for the version you want keys of.

3. From the repositories main directory, run `./install.sh` to build and install the fork of Criptam.

Now, we need to supply the `fw.json`. You can get this by running `wget https://api.ipsw.me/v4/device/{deviceid} -O fw.json`, where `{deviceid}` is the device identifier of your device (ie. iPad7,1), just remember to not include the `{}`. A file named your device identifier should be saved. Ensure you're `cd`'d into the directory where the `fw.json` fie is saved. Please remember you need to update this file if a new version comes out for your device and you wish to obtain keys for it.

Running a command like `wget https://api.ipsw.me/v4/device/iPad7,1 -O fw.json` will give me the firmware data for the iPad Pro 2 (12.9-inch, WiFi).

4. Run the following command: `criptam -d {deviceid} -b {buildid}`, where `{deviceid}` is your device identifier (ie. iPad7,1), and `{buildid}` is the build identifier of the version you want keys of (ie. `19H12` for iPadOS 15.7), just remember to not include the `{}`.

Running a command like `criptam -d iPad7,1 -b 19H12` will give me the keys for the iPad Pro 2 (12.9-inch, WiFi) on iPadOS 15.7.

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

A good reminder of the device & version combination is to write the device identifier and build identifier in your note, so you should do something like replacing:

```
Firmware keys:
```

with:

```
Firmware keys for J120AP 19H12:
```

You can now serve these keys on your `localhost` server for `futurerestore`.
<!-- TODO -->

## Restoring
Take note of the board configuration of your device. When you're looking at the version list on [ipsw.me](https://ipsw.me/), click the "Device Information" tab and note the `BoardConfig`. For example, the iPad Pro 2 (12.9-inch, WiFi) has a BoardConfig of `J120AP`.

1. Get an `.ipsw` of the `15.x` version you want to go down to. You can download this from [ipsw.me](https://ipsw.me/). Once you obtain the `.ipsw`, rename it to `ipsw.ipsw` and copy it to your working directory.
2. Extract the `.ipsw` with `unzip ipsw.ipsw -d ipsw`.
3. From the `ipsw` directory, copy the kernel cache. The kernel cache should be at the root of the extracted `ipsw` directory and named after your device (ie. `kernelcache.release.ipad7` for the `iPad7,x`, a shortened version related to the device identifier). Copy the kernel cache to your working directory and rename it to `kernelcache`.
4. From the `ipsw` directory, copy the restore ramdisk; you can identify this using the build manifest. You can open `BuildManifest.plist` with TextEdit by either using Finder or `open -e BuildManifest.plist`. Search for "RestoreRamDisk" and look for the second result. Look a couple lines beneath, until you see `<key>Path</key>` under the `RestoreRamDisk` key and dictionaries. The `<string>` underneath the Path key is the name of the restore ramdisk `.dmg`. Copy the `.dmg` with the same name as the `.dmg` in the `<string></string>` to your working directory, and rename it to `restore_ramdisk`.
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
20. Rebuild the kernel cache with `pyimg4 im4p create -i krnl.patched -o krnl.im4p-f rkrn --lzss`.

Now that your restore files are prepared, you can restore the device with `futurerestore`.

In order to restore the device, you need to first exploit the device. Put your device into [DFU mode](https://theapplewiki.com/wiki/DFU_Mode) and run `gaster pwn && gaster reset`. If `gaster` hangs or goes into a loop, redo the combination for entering DFU mode and run the command again.

If your device has a baseband, run `futurerestore -t shsh.shsh2 --use-pwndfu --skip-blob --rdsk ramdisk.im4p --rkrn krnl.im4p --latest-sep --latest-baseband ipsw.ipsw`. If your device does not have baseband, change `--latest-baseband` to `--no-baseband`. If you are unsure whether or not your device has baseband, try the command with `--latest-baseband`; the restore will fail (your data is untouched) if `futurerestore` errors due to your device not having baseband.

## Booting
We need to copy more files from `ipsw`. Some files may be named after your board configuration (ie. `J120AP`), albeit seems like they're cut down in `ipsw/Firmware/dfu` (the files are named with `j120` instead of `J120AP`). Please make sure to get the correct files for your device.

- From `ipsw/Firmware/dfu`, locate `iBEC.{boardid}.RELEASE.im4p`, where `{boardid}` is your cut down board configuration without the `{}`. Copy this to your working directory and rename it to `ibec`.
- From `ipsw/Firmware/dfu`, locate `iBSS.{boardid}.RELEASE.im4p`, where `{boardid}` is your cut down board configuration without the `{}`. Copy this to your working directory and rename it to `ibss`.
- From `ipsw/Firmware/all_flash/`, locate `DeviceTree.{boardid}.im4p`, where `{boardid}` is your board configuration without the `{}`. Copy this to your working directory and rename it to `devicetree`.

In `ipsw`, you should locate the largest `.dmg`'s name. For example, the `J120AP` `19E258` root filesystem `.dmg` is named `078-28735-012.dmg`. From `ipsw/Firmware`, copy the `.trustcache` for the root filesystem `.dmg` (ie. `078-28735-012.dmg.trustcache`) to your working directory and rename it to `rootfs_trustcache`.

Lastly, you need to reopen `BuildManifest.plist`. Search for `IsFUDFirmware` and look through every results entire dictionary; if the `Path` `<key>` has a `<string>` that shows a file ending in `.im4p`, copy the corresponding files to your working directory. These files are all inside of the `ipsw` directory.

Please refer to the "Firmware Keys" section of this guide to get `ivkey`'s. If they are on The Apple Wiki, you may use them here. Otherwise, please follow the Criptam guide in getting the keys. Remember, `ivkey` means the IV concatenated with the Key. If the IV is `123` and the Key is `456`, the `ivkey` is `123456`. The keys must be for your exact device and exact i(Pad)OS version you want to go to.

1. Decrypt your `ibss` with `img4 -i ibss -o ibss.dmg -k {ibss ivkey}`, where `{ibss ivkey}` is the `ivkey` for iBSS, just remember to not include the `{}`.
2. Decrypt your `ibec` with `img4 -i ibec -o ibec.dmg -k {ibec ivkey}`, where `{ibec ivkey}` is the `ivkey` for iBEC, just remember to not include the `{}`.

If you want to ensure your keys are correct, open either `ibss.dmg` or `ibec.dmg` in a text editor; you should immediately see "Copyright 2007-20xx, Apple Inc." near the top. If the ***entire*** file is gibberish, the keys are invalid.

3. Patch iBSS with `iBoot64Patcher ibss.dmg ibss.patched`.
4. Patch iBEC with the verbose boot argument with `iBoot64Patcher ibec.dmg ibec.patched -b "-v"`.
5. Create an IM4M with `img4tool -e -s shsh.shsh2 -m IM4M`.
6. Repack iBSS with `img4 -i ibss.patched -o ibss.img4 -M IM4M -A -T ibss`.
7. Repack iBEC with `img4 -i ibec.patched -o ibec.img4 -M IM4M -A -T ibec`.
8. Sign device tree with `img4 -i devicetree -o devicetree.img4 -M IM4M -T rdtr`.
9. Sign root filesystem trustcache with `img4 -i rootfs_trustcache -o rootfs_trustcache.img4 -M IM4M -T rtsc`.

Now, you need to sign every `.im4p` that was copied when you searched `IsFUDFirmware` in the `BuildManifest.plist`. Run `img4 -i {im4p filename} -o {img4 filename} -M IM4M -T idfk`, where `{im4p filename}` is the filename of one firmwares `.im4p` filename, and `{img4 filename}` is the filename with `.im4p` replaced with `.img4` (ie. `aopfw.im4p` and `aopfw.img4`), just remember to not include the `{}`. Running these commands will make the terminal spit out a four letter code, you should rerun the command for each firmware but replace `idfk` with the four letter code that was outputted for that firmware file. Repeat this entire step for every single firmware file you copied.

10. Patch the kernel cache with `Kernel64Patcher kcache.raw krnlboot.patched -f -r -o -e`, make sure you are using the correct fork!
11. Repack the kernel into an `.im4p` with `pyimg4 im4p create -i krnlboot.patched -o krnlbootim4p -f rkrn --lzss`.
11. Repack the kernel into an `.img4` with `pyimg4 img4 create -p krnlboot.im4p -o krnlboot.img4 -m IM4M`.

You're now ready to boot. You can automate the boot process by copying your iBEC, iBSS, device tree, `krnlboot`, root filesystem trustcache, and all firmware `.img4`'s into a separate directory for ease of access.

To boot the device, you need to enter [DFU mode](https://theapplewiki.com/wiki/DFU_Mode), run `gaster pwn && gaster reset`, and run the following commands (do ***NOT*** run `irecovery -c go` if your device does not have an A10 or higher chipset):

```
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

```
irecovery -f {firmware img4 filename}
irecovery -c
```

where `{firmware img4 filename}` is the `.img4` filename of the firmware (ie. `aopfw.img4`), just don't include the actual `{firmwares}`. You can save this as `boot.sh`. Here's an example of `boot.sh` for the `J120AP` `19E258`:

```
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

Since (besides the root filesystem trustcache) there is the AVE and AOP firmware, they've both been added along with their `-c` commands. Since the device is A10X, it includes `-c go`. ***Do not use this script for your device; please only use it as a template***.

## Activation
Refer to [this guide](https://gist.github.com/pwnapplehat/f522987068932101bc84a8e7e056360d) on how to replace activation records to activate your device. iPadOS 17 activation records have been tested to work on i(Pad)OS 15.
<!-- TODO -->

## Known Caveats
- As the name suggests, this is a tethered boot. You need access to a computer every time you want to boot.
- You cannot set a passcode / enable any biometrics. Your device will panic if you enable a passcode, though a force reboot reverts the changes.
- The microphone may not work; tested with 'Voice Memos'.
- The camera may not work; tested with 'Camera'.
- The gyroscope may not work (this means the screen won't rotate, and you will need to enable AssistiveTouch and add the screen rotation option to the AssistiveTouch menu; you will use the AssistiveTouch menu to rotate the screen); tested with 'Gyro Racer'.
- The device will look ***bricked*** after a reboot once you restore. If the device reboots, it enters a kind of 'weird' DFU mode. You will still need to do the [DFU mode](https://theapplewiki.com/wiki/DFU_Mode) button combination to enter the actual DFU though, else `gaster pwn` will make your terminal go in a loop (press Ctrl+C to stop it).
- Your device may reboot automatically if the device is locked for too long. You can mitigate this by keeping the devices WiFi on at all times. You can install [Fiona](https://julioverne.github.io/debfiles/com.julioverne.fiona_0.1_iphoneos-arm.deb) by julioverne to keep the WiFi on (you will need to run the tweak through [Derootifier](https://github.com/haxi0/Derootifier) to convert the `iphoneos-arm` tweak to `iphoneos-arm64`). You can also install [Reverie](https://paisseon.github.io/debs/lilliana.reverie_0.0.3_iphoneos-arm64.deb) (direct `.deb` link) by Paisseon to put the device into a 'hibernation' mode so the device doesn't automatically reboot; battery usage is significantly lower and doesn't reboot the device. Despite the developers subjectively being shady, these are great tweaks that make the deep sleep issue essentially non-existent on tethered boots.

## Credits
- [@mineek](https://github.com/mineek) for writing the original guide and always providing help through my countless skissues
- [@edwin170](https://github.com/edwin170) for general support
- [@pwnapplehat](https://github.com/pwnapplehat) for [updating the orangera1n activation records guide](https://gist.github.com/pwnapplehat/f522987068932101bc84a8e7e056360d)
- All developers & repository owners of the software used in this guide
