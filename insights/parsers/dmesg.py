"""
DMesgLineList - command ``dmesg``
=================================

DMesgLineList is a simple parser that is based on the ``LogFileOutput``
parser class.

It provides one additional helper method not included in ``LogFileOutput``:

* ``has_startswith`` - does the log contain any line that starts with the
  given string?

Sample input::

[    0.000000] Linux version 3.10.0-327.36.3.el7.x86_64 (mockbuild@x86-037.build.eng.bos.redhat.com) (gcc version 4.8.5 20150623 (Red Hat 4.8.5-4) (GCC) ) #1 SMP Thu Oct 20 04:56:07 EDT 2016
[    0.000000] Command line: BOOT_IMAGE=/vmlinuz-3.10.0-327.36.3.el7.x86_64 root=/dev/RHEL7CSB/Root ro rd.lvm.lv=RHEL7CSB/Root rd.luks.uuid=luks-96c66446-77fd-4431-9508-f6912bd84194 crashkernel=auto vconsole.keymap=us rd.lvm.lv=RHEL7CSB/Swap vconsole.font=latarcyrheb-sun16 rhgb quiet LANG=en_GB.utf8
[    0.000000] PID hash table entries: 4096 (order: 3, 32768 bytes)
[    0.000000] x86/fpu: xstate_offset[2]: 0240, xstate_sizes[2]: 0100
[    0.000000] xsave: enabled xstate_bv 0x7, cntxt size 0x340
[    0.000000] AGP: Checking aperture...
[    0.000000] AGP: No AGP bridge found
[    0.000000] Memory: 15918544k/17274880k available (6444k kernel code, 820588k absent, 535748k reserved, 4265k data, 1632k init)
[    0.000000] SLUB: HWalign=64, Order=0-3, MinObjects=0, CPUs=8, Nodes=1
[    0.000000] Hierarchical RCU implementation.

Examples:

    >>> dmesg = shared[DmesgLineList]
    >>> 'BOOT_IMAGE' in dmesg
    True
    >>> dmesg.get('AGP')
    ['[    0.000000] AGP: Checking aperture...', '[    0.000000] AGP: No AGP bridge found']
"""

from .. import LogFileOutput, parser

import re


@parser('dmesg')
class DmesgLineList(LogFileOutput):
    """
    Class for reading output of ``dmesg`` using the LogFileOutput parser class.
    """
    _line_re = re.compile(r'^(?:\[\s+(?P<timestamp>\d+\.\d+)\]\s+)?(?P<message>.*)$')

    def has_startswith(self, prefix):
        """
        Parameters:
            prefix (str): The prefix of the line to look for.  Ignores any
                timestamp before the message body.

        Returns:
            (bool): Does any line start with the given prefix?
        """
        return any(
            self._line_re.search(line).group('message').startswith(prefix)
            for line in self.lines
        )

    def get_after(self, timestamp, lines=None):
        """
        Get a list of lines after the given time stamp.

        Note that the time stamp is the floating point number of seconds
        after the boot time, and is not related to an actual datetime.  If
        a time stamp is not found on the line between square brackets, then
        it is treated as a continuation of the previous line and is only
        included if the previous line's timestamp is greater than the
        timestamp given.  Because continuation lines are only included if a
        previous line has matched, this means that searching in logs that do
        not have a time stamp produces no lines.

        Parameters:
            timestamp(float): log lines after this time are returned.
            lines(list): the list of log lines to search (e.g. from ``get``).
                If not supplied, all available lines are searched.

        Yields:
            Log lines with time stamps after the given time.
        """
        if lines is None:
            lines = self.lines

        including_lines = False
        for line in lines:
            match = self._line_re.search(line)
            if match and match.group('timestamp'):
                # Get logtimestamp and compare to given timestamp
                logstamp = float(match.group('timestamp'))
                if logstamp >= timestamp:
                    including_lines = True
                    yield line
                else:
                    including_lines = False
            else:
                # If we're including lines, add this continuation line
                if including_lines:
                    yield line