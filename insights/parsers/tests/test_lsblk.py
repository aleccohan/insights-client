""""
``test lsblk``
================
"""
from insights.parsers import lsblk
from insights.tests import context_wrap

LSBLK_DATA = ['NAME          MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT',
              'vda           252:0    0    9G  0 disk ',
              '|-vda1        252:1    0  500M  0 part /boot',
              '`-vda2        252:2    0  8.5G  0 part',
              '  |-rhel-root 253:0    0  7.6G  0 lvm  /',
              '  |-rhel-swap 253:1    0  924M  0 lvm  [SWAP]',
              'sda             8:0    0  500G  0 disk',
              '`-sda1          8:1    0  500G  0 part /data']

LSBLK_DATA2 = ['NAME                       MAJ:MIN RM    SIZE RO TYPE  MOUNTPOINT',
               'sr0                         11:0    1   64.3M  0 rom',
               'sda                          8:0    0     25G  0 disk ',
               '|-sda1                       8:1    0    256M  0 part  /boot',
               '|-sda2                       8:2    0   18.6G  0 part  ',
               '| `-vg_root-lv_root (dm-0) 253:0    0   18.5G  0 lvm   /',
               '`-sda3                       8:3    0    6.2G  0 part  [SWAP]',
               'sdb                          8:16   0 1000.1G  0 disk  ',
               '`-mpathb (dm-2)            253:2    0 1000.1G  0 mpath ',
               '  `-mpathbp1 (dm-4)        253:4    0 1000.1G  0 part  ',
               '    `-appdg-app (dm-7)     253:7    0    2.8T  0 lvm   /splunk',
               'sdc                          8:32   0  850.1G  0 disk  ',
               '`-mpatha (dm-1)            253:1    0  850.1G  0 mpath ',
               '  `-mpathap1 (dm-5)        253:5    0  850.1G  0 part  ',
               '    `-appdg-app (dm-7)     253:7    0    2.8T  0 lvm   /splunk',
               'sdd                          8:48   0 1000.1G  0 disk  ',
               '`-mpathc (dm-3)            253:3    0 1000.1G  0 mpath ',
               '  `-mpathcp1 (dm-6)        253:6    0 1000.1G  0 part  ',
               '    `-appdg-app (dm-7)     253:7    0    2.8T  0 lvm   /splunk',
               'sde                          8:64   0 1000.1G  0 disk  ',
               '`-mpathb (dm-2)            253:2    0 1000.1G  0 mpath ',
               '  `-mpathbp1 (dm-4)        253:4    0 1000.1G  0 part  ',
               '    `-appdg-app (dm-7)     253:7    0    2.8T  0 lvm   /splunk',
               'sdf                          8:80   0  850.1G  0 disk  ',
               '`-mpatha (dm-1)            253:1    0  850.1G  0 mpath ',
               '  `-mpathap1 (dm-5)        253:5    0  850.1G  0 part  ',
               '    `-appdg-app (dm-7)     253:7    0    2.8T  0 lvm   /splunk',
               'sdg                          8:96   0 1000.1G  0 disk  ',
               '`-mpathc (dm-3)            253:3    0 1000.1G  0 mpath ',
               '  `-mpathcp1 (dm-6)        253:6    0 1000.1G  0 part  ',
               '    `-appdg-app (dm-7)     253:7    0    2.8T  0 lvm   /splunk']

# lsblk -P -o
LSBLK_EXT_DATA = """
ALIGNMENT="0" DISC-ALN="0" DISC-GRAN="0B" DISC-MAX="0B" DISC-ZERO="0" FSTYPE="" GROUP="cdrom" KNAME="sr0" LABEL="" LOG-SEC="512" MAJ:MIN="11:0" MIN-IO="512" MODE="brw-rw----" MODEL="DVD+-RW DVD8801 " MOUNTPOINT="" NAME="sr0" OPT-IO="0" OWNER="root" PHY-SEC="512" RA="128" RM="1" RO="0" ROTA="1" RQ-SIZE="128" SCHED="cfq" SIZE="1024M" STATE="running" TYPE="rom" UUID=""
ALIGNMENT="0" DISC-ALN="0" DISC-GRAN="0B" DISC-MAX="0B" DISC-ZERO="0" FSTYPE="" GROUP="disk" KNAME="sda" LABEL="" LOG-SEC="512" MAJ:MIN="8:0" MIN-IO="512" MODE="brw-rw----" MODEL="WDC WD1600JS-75N" MOUNTPOINT="" NAME="sda" OPT-IO="0" OWNER="root" PHY-SEC="512" RA="128" RM="0" RO="0" ROTA="1" RQ-SIZE="128" SCHED="cfq" SIZE="149G" STATE="running" TYPE="disk" UUID=""
ALIGNMENT="0" DISC-ALN="0" DISC-GRAN="0B" DISC-MAX="0B" DISC-ZERO="0" FSTYPE="ext4" GROUP="disk" KNAME="sda1" LABEL="" LOG-SEC="512" MAJ:MIN="8:1" MIN-IO="512" MODE="brw-rw----" MODEL="" MOUNTPOINT="/boot" NAME="sda1" OPT-IO="0" OWNER="root" PHY-SEC="512" RA="128" RM="0" RO="0" ROTA="1" RQ-SIZE="128" SCHED="cfq" SIZE="500M" STATE="" TYPE="part" UUID="c7c4c016-8b00-4ded-bffb-5cc4719b7d45"
ALIGNMENT="0" DISC-ALN="0" DISC-GRAN="0B" DISC-MAX="0B" DISC-ZERO="0" FSTYPE="LVM2_member" GROUP="disk" KNAME="sda2" LABEL="" LOG-SEC="512" MAJ:MIN="8:2" MIN-IO="512" MODE="brw-rw----" MODEL="" MOUNTPOINT="" NAME="sda2" OPT-IO="0" OWNER="root" PHY-SEC="512" RA="128" RM="0" RO="0" ROTA="1" RQ-SIZE="128" SCHED="cfq" SIZE="148.5G" STATE="" TYPE="part" UUID="fFE3aA-ifqV-09uh-1u18-b3mV-73gK-FApXf1"
ALIGNMENT="0" DISC-ALN="0" DISC-GRAN="0B" DISC-MAX="0B" DISC-ZERO="0" FSTYPE="ext4" GROUP="disk" KNAME="dm-0" LABEL="" LOG-SEC="512" MAJ:MIN="253:0" MIN-IO="512" MODE="brw-rw----" MODEL="" MOUNTPOINT="/" NAME="vg_trex-lv_root" OPT-IO="0" OWNER="root" PHY-SEC="512" RA="128" RM="0" RO="0" ROTA="1" RQ-SIZE="128" SCHED="" SIZE="50G" STATE="running" TYPE="lvm" UUID="0618daba-8dc0-4a1c-926b-4a0f968da62e"
ALIGNMENT="0" DISC-ALN="0" DISC-GRAN="0B" DISC-MAX="0B" DISC-ZERO="0" FSTYPE="swap" GROUP="disk" KNAME="dm-1" LABEL="" LOG-SEC="512" MAJ:MIN="253:1" MIN-IO="512" MODE="brw-rw----" MODEL="" MOUNTPOINT="[SWAP]" NAME="vg_trex-lv_swap" OPT-IO="0" OWNER="root" PHY-SEC="512" RA="128" RM="0" RO="0" ROTA="1" RQ-SIZE="128" SCHED="" SIZE="3.4G" STATE="running" TYPE="lvm" UUID="102e1d8a-39c9-4065-ae16-d9cbd7162691"
ALIGNMENT="0" DISC-ALN="0" DISC-GRAN="0B" DISC-MAX="0B" DISC-ZERO="0" FSTYPE="ext4" GROUP="disk" KNAME="dm-2" LABEL="" LOG-SEC="512" MAJ:MIN="253:2" MIN-IO="512" MODE="brw-rw----" MODEL="" MOUNTPOINT="/home" NAME="vg_trex-lv_home" OPT-IO="0" OWNER="root" PHY-SEC="512" RA="128" RM="0" RO="0" ROTA="1" RQ-SIZE="128" SCHED="" SIZE="95.1G" STATE="running" TYPE="lvm" UUID="eee3252d-de08-4732-9d55-f2e33f878664"
"""


def test_lsblk():
    results = lsblk.LSBlock(context_wrap(LSBLK_DATA))
    assert results is not None
    assert len(results) == 7
    rhel_root = None
    sda = None
    for result in results:
        if result.name == 'rhel-root':
            rhel_root = result
        elif result.name == 'sda':
            sda = result
    assert rhel_root is not None
    assert rhel_root.maj_min == "253:0"
    assert rhel_root.removable is False
    assert rhel_root.size == "7.6G"
    assert rhel_root.read_only is False
    assert rhel_root.type == "lvm"
    assert rhel_root.mountpoint == "/"
    assert rhel_root.parent_names == ["vda", "vda2"]
    assert sda is not None
    assert sda.maj_min == "8:0"
    assert sda.removable is False
    assert sda.size == "500G"
    assert sda.read_only is False
    assert sda.type == "disk"
    assert 'mountpoint' not in sda
    assert 'parent_names' not in sda

    # Test BlockDevice methods
    assert results.device_data['sda'] == sda
    assert sda.get('maj_min') == sda.maj_min
    assert repr(rhel_root) == 'lvm:rhel-root(/)'
    assert repr(sda) == 'disk:sda'

    results = lsblk.LSBlock(context_wrap(LSBLK_DATA2))
    assert results is not None
    assert len(results) == 30
    sr0 = None
    sdf_appdg = None
    for result in results:
        if result.name == "sr0":
            sr0 = result
        elif result.name == "appdg-app (dm-7)" and result.parent_names[0] == "sdf":
            sdf_appdg = result
    assert sr0 is not None
    assert sr0.name == "sr0"
    assert sr0.maj_min == "11:0"
    assert sr0.removable is True
    assert sr0.size == "64.3M"
    assert sr0.read_only is False
    assert sr0.type == "rom"
    assert sdf_appdg is not None
    assert sdf_appdg.name == "appdg-app (dm-7)"
    assert sdf_appdg.maj_min == "253:7"
    assert sdf_appdg.removable is False
    assert sdf_appdg.size == "2.8T"
    assert sdf_appdg.read_only is False
    assert sdf_appdg.type == "lvm"
    assert sdf_appdg.mountpoint == "/splunk"
    assert sdf_appdg.parent_names == ["sdf", "mpatha (dm-1)", "mpathap1 (dm-5)"]


def test_lsblk_po():
    results = lsblk.LSBlockPairs(context_wrap(LSBLK_EXT_DATA))
    assert results is not None
    assert len(results) == 7
    sda1 = None
    for result in results:
        if result.name == 'sda1':
            sda1 = result
    assert sda1 is not None
    assert sda1.alignment == "0"
    assert sda1.disc_aln == "0"
    assert sda1.disc_gran == "0B"
    assert sda1.disc_max == "0B"
    assert sda1.disc_zero == "0"
    assert sda1.fstype == "ext4"
    assert sda1.group == "disk"
    assert sda1.kname == "sda1"
    assert 'LABEL' not in sda1
    assert sda1.log_sec == "512"
    assert sda1.maj_min == "8:1"
    assert sda1.min_io == "512"
    assert sda1.mode == "brw-rw----"
    assert 'MODEL' not in sda1
    assert sda1.mountpoint == "/boot"
    assert sda1.name == "sda1"
    assert sda1.opt_io == "0"
    assert sda1.owner == "root"
    assert sda1.phy_sec == "512"
    assert sda1.ra == "128"
    assert sda1.removable is False
    assert sda1.read_only is False
    assert sda1.rota == "1"
    assert sda1.rq_size == "128"
    assert sda1.sched == "cfq"
    assert sda1.size == "500M"
    assert 'STATE' not in sda1
    assert sda1.type == "part"
    assert sda1.uuid == "c7c4c016-8b00-4ded-bffb-5cc4719b7d45"