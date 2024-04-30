# latency
Python ping library that don't require root privileges.
## More about the project
This library aims to provide a set of python tools based on the ping command.
It has the advantage of __not requiring administrator privileges__.
## Some examples
#### `latency.ping() -> str:`
With the execution of this python program:
```python
#!python
import latency
print(latency.ping())
```
On Windows:
```console 
Pinging google.com [2a00:1450:4007:813::200e] with 32 bytes of data:
Reply from 2a00:1450:4007:813::200e: time=15ms
Reply from 2a00:1450:4007:813::200e: time=17ms
Reply from 2a00:1450:4007:813::200e: time=21ms
Reply from 2a00:1450:4007:813::200e: time=17ms

Ping statistics for 2a00:1450:4007:813::200e:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 15ms, Maximum = 21ms, Average = 17ms
```
On Linux:
```console
PING google.com (142.250.178.142) 56(84) bytes of data.
64 bytes from par21s22-in-f14.1e100.net (142.250.178.142): icmp_seq=1 ttl=118 time=15.1 ms
64 bytes from par21s22-in-f14.1e100.net (142.250.178.142): icmp_seq=2 ttl=118 time=18.9 ms
64 bytes from par21s22-in-f14.1e100.net (142.250.178.142): icmp_seq=3 ttl=118 time=22.9 ms
64 bytes from par21s22-in-f14.1e100.net (142.250.178.142): icmp_seq=4 ttl=118 time=19.2 ms

--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3006ms
rtt min/avg/max/mdev = 15.120/19.024/22.875/2.743 ms
```
As you can see, `latency.ping()` is a seamless output from your platform integrated terminal.
By default, it sets the number of times it will request in its sequence to 4.
#### `latency.max_latency() -> float:`
```python
#!python
import latency
print(latency.max_latency()," ms")
```
On Windows:
```console
17.0  ms
```
On Linux:
```console
16.933  ms
```
As you can see, `latency.max_latency()` returns the maximum latency of the `ECHO_REQUEST` sequence in milliseconds.
On windows thow, we lose precision below millisecond.
