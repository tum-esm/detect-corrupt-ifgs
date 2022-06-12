I took the preprocessing code from PROFFAST 2.1. I removed everything except for the initial parsing of all files. Then I modified the code to continue on every warning and print out the missing charfilters.

The script `run.py` (Python 3!) takes a repository and prints out all corrupt ifgs in this directory. Example output:

```bash
The corrupt ifgs are:
{
    'mb20220421s0e00a.0056': ['GFW', 'GBW', 'HFL', 'LWN', 'TSC'],
    'mb20220421s0e00a.1872': ['GFW', 'GBW', 'HFL', 'LWN', 'TSC']
}
```
