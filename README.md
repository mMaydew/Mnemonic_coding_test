# GitHub profile & repo fetcher

A CLI I created for a coding test given to me by Mnemonic AS as part of the interview process.

## Usage

Help screen: `python3 github.py -h`  
my-profile help screen: `python3 github.py my-profile -h`  
(If no token is passed as a command line argument the program will try to get a token from the github_config.json file)  
profile help screen: `python3 github.py profile -h`  

Example:
```
> python3 github.py profile mMaydew

mMaydew: Michael Maydew - None
name               url                                             stars
-----------------  --------------------------------------------  -------
InfoBot            https://github.com/mMaydew/InfoBot                  0
McCipher           https://github.com/mMaydew/McCipher                 0
PascalsTriangle    https://github.com/mMaydew/PascalsTriangle          0
QuakeMap           https://github.com/mMaydew/QuakeMap                 0
RazerChromeux      https://github.com/mMaydew/RazerChromeux            0
RFID               https://github.com/mMaydew/RFID                     1
SortingAlgorithms  https://github.com/mMaydew/SortingAlgorithms        0
YCRAS              https://github.com/mMaydew/YCRAS                    1
```