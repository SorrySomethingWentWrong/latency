#!python
"""Latency measurements tools. (using system ping in shell subprocess)
"""

import platform  # For getting the operating system name
import re
import subprocess  # For executing a shell command
import traceback


class _Latency:
    """Latency measurements tools class. (using system ping in shell subprocess)"""

    def __init__(self):
        self.is_windows_platform: bool = platform.system().lower() == "windows"

    def __win_command(
        self,
        _url="google.com",
        _packets_sent: int | None = None,
        _packet_size: int | None = None,
    ) -> list[str]:
        """Args:
            _url (str, optional): url or ip adress of the host to ping. Defaults to "google.com".
            _packets_sent (PositiveInt | None, optional):
                Stop after sending this many ECHO_REQUEST packets. Defaults to None.
            _packet_size (PositiveInt | None, optional):
                Specifies the number of data bytes to be sent. Defaults to None.

        Returns:
            list[str]: ['ping','-n', str(_packets_sent), {'-l', str(_packet_size)}->optional, _url]
        """
        # Building the command. Ex: "ping -n 4 google.com"
        command = ["ping", "-n", str(_packets_sent)]
        # Option for the number of packets sent
        if _packet_size is not None:
            command.append("-l")
            command.append(str(_packet_size))
        command.append(_url)
        return command

    def __linux_command(
        self,
        _url="google.com",
        _packets_sent: int | None = None,
        _packet_size: int | None = None,
    ) -> list[str]:
        """Args:
            _url (str, optional): url or ip adress of the host to ping. Defaults to "google.com".
            _packets_sent (PositiveInt | None, optional):
                Stop after sending this many ECHO_REQUEST packets. Defaults to None.
            _packet_size (PositiveInt | None, optional):
                Specifies the number of data bytes to be sent.
                The default is 56, which translates into 64 ICMP data bytes when combined
                with the 8 bytes of ICMP header data. Defaults to None.

        Returns:
            list[str]: ['ping','-c', str(_packets_sent), {'-s', str(_packet_size)}->optional, _url]
        """
        # Building the command. Ex: "ping -c 4 google.com"
        command = ["ping", "-c", str(_packets_sent)]
        # Option for the number of packets sent
        if _packet_size is not None:
            command.append("-s")
            command.append(str(_packet_size))
        command.append(_url)
        return command

    def ping(
        self,
        url="google.com",
        packets_sent: int | None = 4,
        packet_size: int | None = None,
    ) -> str | None:
        """Returns shell output response to a ping request. (return str)
        Remember that a host may not respond to a ping (ICMP)
        request even if the host name is valid.
        The terminal may not be supported. (return None)
        Supported operating systems:
        ->Windows: ['ping','-c', str(_packets_sent), {'-s', str(_packet_size)}->optional, _url]
        ->linux:   ['ping','-c', str(_packets_sent), {'-s', str(_packet_size)}->optional, _url]
        Args:
            url (str, optional): url or ip adress of the host to ping. Defaults to "google.com".
            packets_sent (PositiveInt | None, optional):
                Stop after sending this many ECHO_REQUEST packets. Defaults to 4.
            packet_size (PositiveInt | None, optional):
                Specifies the number of data bytes to be sent. Defaults to None.

        Returns:
            str | None: Return shell output String response to a ping request,
                None if system platform not supported.
        """
        try:
            if self.is_windows_platform:
                return subprocess.getoutput(
                    cmd=self.__win_command(
                        _url=url, _packets_sent=packets_sent, _packet_size=packet_size
                    ),
                    encoding="oem",
                )
            return subprocess.check_output(
                    args=self.__linux_command(
                        _url=url, _packets_sent=packets_sent, _packet_size=packet_size
                    )
                ).decode()

        except SyntaxError:
            traceback.print_exc()
        return None

    def __msmax_output_extract(self, command_output: str) -> float | None:
        """Extract max ping response time in ms from shell outputa.
        Args:
            command_output (str): Shell output from stdout.

        Returns:
            float| None: _description_
        """
        if self.is_windows_platform:
            return float(
                re.search(
                    pattern="(?<=Maximum = )(?:\\d+)(?=ms,)",
                    string=command_output,
                    flags=re.RegexFlag.ASCII,
                ).group(  # type: ignore
                    0
                )
            )
        try:
            return float(
                re.search(
                    pattern="(?<!/max/)(?:\\d+\\.\\d+)(?=/\\d+\\.\\d+ ms)",
                    string=command_output,
                    flags=re.RegexFlag.ASCII,
                ).group(  # type: ignore
                    0
                )
            )
        except RuntimeError as exc:
            exc.add_note(
                "latency._Latency::__msmax_output_extract(command_output: str):\
                \n"
                + repr(command_output)
                + "\nUnsupported,or empty:"
                + command_output
            )
            traceback.print_exc()
            return None

    def get_max_latency(
        self,
        url="google.com",
        packets_sent: int | None = 4,
        packet_size: int | None = None,
    ) -> float | None:
        """Gather max latency response time in ms via shell ping request.
        Remember that a host may not respond to a ping (ICMP)
        request even if the host name is valid.
        The terminal may not be supported. (return None)
        Supported operating systems:
        ->Windows: ['ping','-c', str(_packets_sent), {'-s', str(_packet_size)}->optional, _url]
        ->linux:   ['ping','-c', str(_packets_sent), {'-s', str(_packet_size)}->optional, _url]
        Args:
            url (str, optional): url or ip adress of the host to ping. Defaults to "google.com".
            packets_sent (PositiveInt | None, optional):
                Stop after sending this many ECHO_REQUEST packets. Defaults to 4.
            packet_size (PositiveInt | None, optional):
                Specifies the number of data bytes to be sent. Defaults to None..

        Returns:
            int | None: return maximum ping latency response time in ms
        """
        command_output = self.ping(
            url=url, packets_sent=packets_sent, packet_size=packet_size
        )
        if command_output is None:
            return command_output
        return self.__msmax_output_extract(command_output=command_output)


__Latency_instance = _Latency()
ping = __Latency_instance.ping
max_latency = __Latency_instance.get_max_latency
