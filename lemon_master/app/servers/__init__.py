[root@om-center salt]# salt '*' ps.cpu_percent
test-client.mgtest.com:
    'ps' __virtual__ returned False: The ps module cannot be loaded: python module psutil not installed.
ERROR: Minions returned with non-zero exit code
[root@om-center salt]#

python-psutil.x86_64 : A process and system utilities module for Python
    dmidecode
    smbios