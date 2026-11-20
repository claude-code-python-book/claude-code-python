$ pip install --require-hashes -r requirements.txt
exit 0
# (the same version is rebuilt with different contents)
$ pip install --require-hashes -r requirements.txt
ERROR: THESE PACKAGES DO NOT MATCH THE HASHES FROM THE REQUIREMENTS FILE. If you have updated the package versions, please update the hashes. Otherwise, examine the package contents carefully; someone may have tampered with them.
    shared==1.0.0 from file:///.../dist/shared-1.0.0-py3-none-any.whl (from -r requirements.txt (line 1)):
        Expected sha256 4d8733b6edc6d2edbb06f70ed67bb7596742d6e4561797905182ba6fb4392c0c
             Got        af6a69e800ed0616b3bea59ae25f9ec8b2c378d09d2cc7a0619b4338a990f1ef

exit 1
