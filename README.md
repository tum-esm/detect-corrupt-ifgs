# Detect Corrupt Interferograms

This tool detects individual interferogram files in a given directory that PROFFAST cannot process.

<br/>

## 🪄 How it was made?

We took the preprocessing code from PROFFAST 2.1 (https://www.imk-asf.kit.edu/english/3225.php) and removed everything except for the initial parsing of all files. Then we modified the code to continue on every warning and print out the missing "charfilters" as well as the corrupt filename.

<br/>

## ⚔️ How to use it?

The script `main.py` (Python 3, only standard libraries) takes in a directory and prints out all corrupt interferograms in this directory. An example of usage can be found at the end of `main.py`. Example output:

```bash
The corrupt ifgs are:
{
    'mb20220421s0e00a.0056': ['GFW', 'GBW', 'HFL', 'LWN', 'TSC'],
    'mb20220421s0e00a.1872': ['GFW', 'GBW', 'HFL', 'LWN', 'TSC']
}
```
