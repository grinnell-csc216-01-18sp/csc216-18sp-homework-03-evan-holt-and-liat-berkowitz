# CSC 216 (Spring 2018) Homework 3

In this homework, you will implement the alternating-bit and go-back-N
reliable transport protocols discussed in class in the context of the
RTP simulation.

You should implement your protocols in `sendrecv.py`.  To run the
simulation, run `rtp.py`, *e.g.*,

~~~ {.console}
csc216-homework-03-starter $> python rtp.py -h
usage: rtp.py [-h] [--app-delay APP_DELAY] [--net-delay NET_DELAY]
              [--corr CORR_PROB] [--drop DROP_PROB]
              steps protocol

Simulates transportation layer network traffic.

positional arguments:
  steps                 number of steps to run the simulation
  protocol              protocol to use [naive|alt|gbn]

optional arguments:
  -h, --help            show this help message and exit
  --app-delay APP_DELAY
                        delay between application-level messages (default: 2)
  --net-delay NET_DELAY
                        network-level segment delay (default: 1
  --corr CORR_PROB      likelihood of segment corruption (default: 0.25)
  --drop DROP_PROB      likelihood of dropped packets (default: 0.0)
~~~

## Repository Information

* Evan Holt (holtevan) and Liat Berkowitz (berkowit)
* Used Python 2
* Resources: StackOverflow, Course Website, Python Documentation
* Notes: we did not pull the last change made to the started code because we had already begun our implementation. Thus, our code reacts differently to dropped packets than other programs may. 
