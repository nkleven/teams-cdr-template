==============================
NiceHash QuickMiner v0.7.8.0
==============================

Instructions:
1. Start NiceHashQuickMiner.exe.
2. You will be asked for your NiceHash mining address. Provide it.
3. All further interaction with NiceHash QuickMiner is through notification icon in taskbar.
   Right click it and then perform any action you want.
4. It is recommended to set autostart with Windows if this is your classis rig machine.
5. Use OCTune to adjust overclocks and fan speeds (do not use Afterburner, it is not needed).
6. Enjoy carefree mining! 

============================LOGGING============================

Change serviceLocation, BTC (mining address), workerName, launchCommandLine.
consoleLogLevel, fileLogLevel (for NiceHashQuickMiner); use following numbers:
0-6 which means:
0: log everything (TRACE)
1: log debug (DEBUG)
2: standard (INFO)
3: warnings (WARNING)
4: errors (ERROR)
5: fatal (FATAL)
6: no logging (disabled)

Please, enable full file logging ("fileLogLevel":0) and submit 
log files when error is found.

You can simply enable logging via menu through icon in taskbar.

============================CPU MINING============================

From version 0.2.0.0, CPU Mining with integrated XMRig is possible on modern CPUs
with AVX2. CPU Mining can be activated from the tray menu (or via Rig Manager). 
You can provide extra launch parameters for XMRig (config nhqm.conf), for example:

	"CPUMinerELP":"--cpu-max-threads-hint 50 --print-time 15"

First parameter above tells CPU miner to use only 50% of resources, second one prints
speed to console every 15 seconds. Parameters for lowest CPU priority, donation level 0%
and other important parameters are already provided by the Excavator.

============================EXCAVATOR RECOVERY============================

There are 3 options what NiceHashQuickMiner should do when device fails or when
device has too high speed.

	"whenDeviceSpeedTooHigh":2,
	"whenDeviceSpeedZero":1,

1 = no action
2 = restart Excavator
3 = restart rig

Usually, when device has too high speed, issue can be resolved by restarting Excavator.
If device has speed 0 (errored out), it means that there was some instability (either too
high OC or issue with risers). In that case, it is most likely better to restart the rig
(set to value 3).

============================UPDATING============================

From version 0.3.0.0, NiceHashQuickMiner has auto updater. You will be notified when new
version is available for download. You can participate in testing RC versions (release
candidate) which have new features faster; enable this by setting:

	"bUpdateRCVersion":true

Updating from previous version? Make sure to full uninstall it first - 
remove Windows autostart in old version before you enable autostart in new one.

============================SAVING OVERCLOCKS LOCALLY============================

Excavator has two more events: on_quickminer.start and on_quickminer.stop. You can 
put setting OC profile for mining there so when you stop the miner, mining OC profile is reset
back to your regular OC settings and you can play a game. After you return back and click start
again, mining OC profile will be applied.

Find your optimal OC with OCTune and save it inside OCTune.

============================OVERCLOCKING METHODS============================

There are two methods to apply OC profile. Alternative one takes only max core clock and absolute
memory clock. This means you can reach your ideal OC configuration faster, because first, you need
to determine your max. memory stability clock and after that just decrease max core clock so you
get wanted efficiency - leave it a bit higher for higher speed and drop it down if you want less
power consumption.

RTX 3060 Ti wants around 1350 MHz, RTX 3070 around 1200 MHz and for 3090 120 MH/s is possible with
290 W (clock limit 1095 MHz) which means 412 kH/J efficiency.

============================PAST UPDATES============================

With 0.3.0.5 experimental autotuner has been added. You can now determine almost perfect OC settings
for your card for max efficiency with just one mouse click in 5 minute time! Feature is available
under OCTune.

Version 0.3.0.7 brings GDDR6X temperature measurements (only RTX 3080 and RTX 3090).

Version 0.3.1.0 brings optimize profiles (two profiles which can be applied without struggling for
doing any manual OC). These profiles are applied remotely over Rig Manager. If you have your own
OC, then you have to have profile "Manual" selected or your OC settings may get overwritten!

Version 0.3.1.1 uses new Excavator which has a smartfan functionality - can set fan speed according
to temperature of your GPU or VRAM and GPU. Old fan management is deprecated and replaced with
smartfan. There are following smartfan modes:
1. No FAN management by Excavator (mode = 0)
2. Fixed speed (mode = 1)
3. Target GPU temperature; fan speed is set according to wanted GPU temp and current GPU temp
	(mode = 2)
4. Target GPU&VRAM temperature; as above, but also VRAM temp is considered (mode = 3)
OCTune has new UI which support these changes so fan management is easier now. Also fan settings
can be saved just like OC settings and are applied with each Excavator (re)start.

Version 0.3.1.2 contains bug fixes. Service autostart method removed. Task scheduler method is much
better and gives less problems. Excavator's speed for Pascal cards is restored back to what was in
version 0.3.0.2.

Version 0.3.2.0 has improved speed measuring. If you are upgrading, make sure to delete periodic
method "workers.reset.all" from your commands.json file. If you are not sure how to do it properly,
just start from zero. There are some other less important bug fixes and improvements. 0.3.2.0 comes 
with installer & uninstaller (Windows Add/Remove Programs).

Version 0.3.2.1 contains mostly just bug fixes and some small improvements when launching for the
first time.

Version 0.3.2.2 greatly improves SmartFan. Obtaining mining domains for correct function of NiceHash
QuickMiner is now done using DNS over HTTPS which should reduce number of issues users having with
certain Firewalls and other security solutions which are unjustifiably blocking traffic to NiceHash.
Handling of erroneous state has been improved (rig is not restarted if there is no internet and first
it tries to restart Excavator). Also because we consider this as a major stability configuration, this
setting has been moved into firstrun optional settings dialog.

0.3.2.3 adds "Game Mode". This mode disables mining on primary display GPU, applies gaming overclock
and allows you to switch into gaming mode with just a click of a button. When you are done, it is
possible to return into mining mode just as easily. Note that this feature is experimental. Some
other bugs were also fixed.

0.3.2.5 and 0.3.2.6 mostly just bug fixes and small improvements.

0.3.2.7 brings back power readings for Mobile versions of GPUs.

0.3.3.0 has automatic location select option which is recommended to be set by everyone. Automatic
location works by first testing latency of accepted shares for all possible mining locations
(currently there are 4). It remembers this data and keep it for 7 days - after 7 days, this test
is performed again because network conditions may change over time. Additionally, when you have
automatic location selected, if NiceHash informs QuickMiner that certain location is not available,
QuickMiner will select next best location by latency automatically thus keep your Rig mining without
any outtage. So it is strongly recommended to have automatic location selected. If you already
have certain location selected, you can modify nhqm.conf and set -1 for "serviceLocation".

0.3.4.0 also measures additional temperatures (HotSpot - VRAM) for other GPUs besides RTX 3080
and 3090 and gives you ability to adjust fans accordingly.

0.4.0.0 with GPU core undervoltage support. Works on all supported cards. Please, be careful when
using this feature. We do not allow setting manual voltage of more than 1000 mV, but we cannnot
guarantee that there is no bug in the code that would somehow allow to bypass this limit and
consequently cause damage to your GPU. Only use if you know what you are doing! 4th error
recovery mode was added - restart of NVIDIA driver.

0.4.1.1, 0.4.1.2 and 0.4.1.3 are mostly small improvements and bug fixes.

0.4.1.4 addresses issue with altered names of devices when using NVIDIA developer drivers
470.05 and caused OPTIMIZE not working. From this version on, SmartFan gets reset only if being
set to anything but auto. This happens when Excavator exits automatically so devices.smartfan.reset
is not needed for event "on_quit" in commands.json anymore. This would make less problems when
using 3rd party tools to manage your fans.

0.4.2.0 brings ability to set memory timings. Currently only two timings which are needed
for GDDR5X to achieve good performance. Set FAW to 16 and RRD to 4. If that does not work, you
can try FAW to 20 and RRD to 5. Example:

	{"id":1,"method":"device.set.memory.timings","params":["0","FAW=16","RRD=4"]}

If you wish to reset memory timings, set memory delta clock to 0. When DAG is being generated,
memory timings are reset to default and then reapplied (smart DAG gen just like mem OC has).
It is recommended to start this command with some delay to avoid instant crash.

0.4.3.0 brings OPTIMIZE for certain Pascal cards (1080 Ti and 1080 initially).

From version 0.4.4.0 more various OPTIMIZE profiles are available and new ones added modified
daily. Be sure to periodically check it out! These get better and better over time.

In 0.4.5.0 access to HTTP API was restructured to not allow CORS anymore. It was pointed out
by one security researcher that a remote change of mining address could be possible if user
visits a malicious website. To remedy this security bug, OCTune is now loaded by Excavator's
HTTP server and CORS is not turned on anymore. Also an 'Authorization' token is set and all
API calls need it to be able to make any changes to the mining process. There are also some
further improvements regarding CUDA detection and ID assignments which may further reduce
issues with Invalid DAG file generated problems.

0.4.5.3 is another security focused upgrade which brings N/M signature support for update
and install packages. Using several signatures to execute upgrade or install greatly increases
resiliency towards malicious attempts to distribute malware through update packages in
case there was a security breach at NiceHash.

v0.4.5.4 and v0.4.5.5 just bug fixes and small improvements.

v0.5.0.0; Game Mode: if you would like to override auto detected display device, then fill
"overrideDisplayDeviceUUID" in your nhqm.conf with the UUID value of your GPU. You can get
UUID value of your GPU if you stop/disable device in Rig Manager and then check your config
to see which UUID was disabled.

v0.5.0.0 also adds MSI-enable tweak: all your supported GPUs are set to use MSI. This can
significantly improve stability of your system. GPU crashes are way easier to handle then
and in most cases can be handled with simple driver restart (or restart of Excavator). You
can read more about MSI here: https://en.wikipedia.org/wiki/Message_Signaled_Interrupts
By default, NVIDIA drivers does not use MSI for GTX 1000 and RTX 2000 series cards, which 
is a big mistery because Pascal and Turing architecture does support MSI. Every time drivers
are updated, this value is changed back to not using MSI, so you need to apply it after
each driver update.

Target plus decrease MCC fan mode (version 0.5.1.0+) is an inteligent Smart Fan mode which
works similar as Target Core&VRAM (mode 3) with upgrade - when max set fan speed is reached
and temperature is still over target, MCC (max core clock) is being reduced thus reducing
power output of the GPU which most likely reduces temperature. The newest Smart Fan mode
takes in one more parameter - max fan speed which is identical to Smart Fan's advanced
parameters = override_level_max (default = -1 = use GPU's default max level = in most cases
this is 100%). This fan mode enables you to really take control of the temperatures and
make sure to keep them in check with drastic measures (reducing clocks, load and power)
if needed. It is NOT available for Pascal architecture, but fully supported for Volta, 
Turing and Ampere, because prior enabling it, alternative OC needs to be set with defined
MCC (core clock limit).

With version 0.5.2.0 new nhqm.conf variables were added:
	* environmentVariables: string array of EnvironmentVariables for Excavator.exe (eg:
		"CUDA_VISIBLE_DEVICES=0,1", "CUDA_LAUNCH_BLOCKING=1", ...)
	* bDisableConfigFileChecks: disable reading of nhqm.conf file during working (may
		improve issues with corrupted config file)

Since v0.5.4.0 RC QuickMiner removes LHR lock

Check other release notes here: https://github.com/nicehash/NiceHashQuickMiner/releases
