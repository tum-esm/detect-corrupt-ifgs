# Detect Corrupt Interferograms

I took the preprocessing code from PROFFAST 2.1 (https://www.imk-asf.kit.edu/english/3225.php). I removed everything except for the initial parsing of all files. Then I modified the code to continue on every warning and print out the missing "charfilters".

The script `main.py` (Python 3, only standard libraries) takes in a repository and prints out all corrupt ifgs in this directory. An example of usage can be found at the end of `main.py`. Example output:

```bash
The corrupt ifgs are:
{
    'mb20220421s0e00a.0056': ['GFW', 'GBW', 'HFL', 'LWN', 'TSC'],
    'mb20220421s0e00a.1872': ['GFW', 'GBW', 'HFL', 'LWN', 'TSC']
}
```
