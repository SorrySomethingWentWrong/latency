# latency
Python ping library that don't require root privileges.
## More about the project
This library aims to provide a set of python tools based on the ping command.
It has the advantage of __not requiring administrator privileges__.
## Some examples
```python
import latency
print(latency.ping())
```
On Windows:
```stdout

```
On Linux
```stdout
PING google.com (142.250.178.142) 56(84) bytes of data.
64 bytes from par21s22-in-f14.1e100.net (142.250.178.142): icmp_seq=1 ttl=118 time=15.1 ms
64 bytes from par21s22-in-f14.1e100.net (142.250.178.142): icmp_seq=2 ttl=118 time=18.9 ms
64 bytes from par21s22-in-f14.1e100.net (142.250.178.142): icmp_seq=3 ttl=118 time=22.9 ms
64 bytes from par21s22-in-f14.1e100.net (142.250.178.142): icmp_seq=4 ttl=118 time=19.2 ms

--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3006ms
rtt min/avg/max/mdev = 15.120/19.024/22.875/2.743 ms
```
