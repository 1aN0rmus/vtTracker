# VTTracker

Summary: This tool was written to monitor and track relevant data from VT Intelligence Notifications feeds.

*This was a quick project that I intend to update at a later date.



## Usage:

```
optional arguments:

  -h, --help            show this help message and exit

  -u URL, --url URL     Specify the VT Notifications URL to pull notifications from

  -d DB, --db DB        This option allows the user to set the name of the SQLLite database, if they do not like the default

  -r RULE, --rule RULE  Query for a specific rule name. CASE-SENSITIVE

  -s, --summary         Basic statistics

  -a, --dumpall         This option will dump all rows to STDOUT

```

## Examples:

### Pull data from notifications feed:

```
Command:
python vtTracker.py -u https://www.virustotal.com/intelligence/hunting/notifications-feed/?key=<apikey>

Result:
### UPDATE STATUS ###
[+] Samples added to DB: 3
[+] Already in DB: 97
```

### Show summary data for collected information:

```
D:\tools>python vtTracker.py -s
### RULE STATS ###
[+] FE_APT_Downloader_OCEANLOTUS_Macro: 5
[+] FE_COBALTSTRIKE_EMPIRE: 3
[+] FE_CVE20170199_RTF: 6
[+] FE_China_Z: 2
[+] FE_FIN7_CATCHALL: 4
[+] FE_FIN7_Halfbaked: 4
[+] FE_HOUDINIRAT_VBS: 2
[+] FE_MAYHEM: 3
[+] FE_NEW_HOTNESS: 2
[+] FE_NEW_HOTNESS2: 1
[+] FE_POWERSHELL_OBSFUCATION: 111
[+] FE_QUICKFLOOD: 7
[+] FE_RANSOMWARE_WANNACRY: 37
[+] FE_RANSOMWARE_WANNACRY_EB: 141
[+] FIN7_SERVICES_SDB_YARA: 1
[+] SCT_scriplet_collector: 7
[+] SEAWOLF_methodology: 1
[+] dragos_crashoverride_configReader: 1
[+] dragos_crashoverride_hashes: 2
[+] dragos_crashoverride_moduleStrings: 2
[+] dragos_crashoverride_serviceStomper: 4
[+] dragos_crashoverride_wiperFileManipulation: 2
[+] fin7_rtf_scripts: 11
[+] 359 samples in this database!

### FILETYPE STATS ###
[+] C: 1
[+] C++: 5
[+] ELF: 12
[+] Email: 4
[+] HTML: 19
[+] MS Excel Spreadsheet: 4
[+] MS PowerPoint Presentation: 1
[+] MS Word Document: 19
[+] PDF: 1
[+] Rich Text Format: 7
[+] Text: 76
[+] Win32 DLL: 130
[+] Win32 EXE: 65
[+] unknown: 15
```

### Query for all MD5's matching a rule:

```
python vtTracker.py -r FE_QUICKFLOOD
### Samples for FE_QUICKFLOOD ###
ef170103e3eb95a6e809d947ee6eb848
c3b424c0978555704a2395c2664ae673
844a7a49778c7ed4dd0e40c10452cce9
162ffab9d9d4f5bf9041056ba99e01eb
3ebb00632ebfc8df1e3baf4657d70331
ccc382d66a2a24a39f34b0ae5ce44935
a4dbe5b828940f510c91966469f786da
```

### Dump all collected data to CSV:

```
python vtTracker.py -a > <output file>
```
