##
# CSC 216 (Spring 2018)
# Reliable Transport Protocols (Homework 3)
#
# Sender-receiver code for the RDP simulation program.  You should provide
# your implementation for the homework in this file.
#
# Your various Sender implementations should inherit from the BaseSender
# class which exposes the following important methods you should use in your
# implementations:
#
# - sender.send_to_network(seg): sends the given segment to network to be
#   delivered to the appropriate recipient.
# - sender.start_timer(interval): starts a timer that will fire once interval
#   steps have passed in the simulation.  When the timer expires, the sender's
#   on_interrupt() method is called (which should be overridden in subclasses
#   if timer functionality is desired)
#
# Your various Receiver implementations should also inherit from the
# BaseReceiver class which exposes thef ollowing important methouds you should
# use in your implementations:
#
# - sender.send_to_network(seg): sends the given segment to network to be
#   delivered to the appropriate recipient.
# - sender.send_to_app(msg): sends the given message to receiver's application
#   layer (such a message has successfully traveled from sender to receiver)
#
# Subclasses of both BaseSender and BaseReceiver must implement various methods.
# See the NaiveSender and NaiveReceiver implementations below for more details.
##

from sendrecvbase import BaseSender, BaseReceiver

import Queue

class Segment:
    def __init__(self, msg, dst):
        self.msg = msg
        self.dst = dst

class NaiveSender(BaseSender):
    def __init__(self, app_interval):
        super(NaiveSender, self).__init__(app_interval)

    def receive_from_app(self, msg):
        seg = Segment(msg, 'receiver')
        self.send_to_network(seg)

    def receive_from_network(self, seg):
        pass    # Nothing to do!

    def on_interrupt(self):
        pass    # Nothing to do!

class NaiveReceiver(BaseReceiver):
    def __init__(self):
        super(NaiveReceiver, self).__init__()

    def receive_from_client(self, seg):
        self.send_to_app(seg.msg)

class AltSender(BaseSender):
    def __init__(self, app_interval):
        super(AltSender, self).__init__(app_interval)
        self.state = False # true is state 1 and false is state 0
        self.curseg = None

    def receive_from_app(self, msg):
        if not self.custom_enabled:
            self.curseg = Segment(msg + str(int(self.state == True)), 'receiver')
            self.send_to_network(self.curseg)
            self.start_timer(10)

    def receive_from_network(self, seg):
        if seg.msg == 'ACK':
            self.custom_enabled = False
            self.state = not self.state
        else:
            self.send_to_network(self.curseg)

    def on_interrupt(self):
        self.send_to_network(self.curseg)

class AltReceiver(BaseReceiver):
    def __init__(self):
        super(AltReceiver, self).__init__()
        self.state = False # true is state 1 and false is state 0

    def receive_from_client(self, seg):
        if seg.msg == '<CORRUPTED>':
            self.send_to_network(Segment('NAK', "sender"))
        elif seg.msg.endswith(str(int(self.state == True))):
            self.send_to_network(Segment('ACK', "sender"))
            self.send_to_app(seg.msg[:-1])
            self.state = not self.state
        else:
            self.send_to_network(Segment('ACK', "sender"))

class GBNSender(BaseSender):
    def __init__(self, app_interval):
        super(GBNSender, self).__init__(app_interval)
        self.cursegs = []
        self.msgcounter = 0

    def receive_from_app(self, msg):
        seg = Segment(msg + str(self.msgcounter), "receiver")
        self.cursegs.append(seg)
        self.msgcounter += 1
        self.send_to_network(seg)

    def receive_from_network(self, seg):
        if seg.msg == '<CORRUPTED>' or seg.msg[:3] == 'NAK':
            self.start_timer(10)
            for segment in self.cursegs:
                self.send_to_network(segment)
        else:
            pass

    def on_interrupt(self):
        pass

class GBNReceiver(BaseReceiver):
    def __init__(self):
        super(GBNReceiver, self).__init__()

    def receive_from_client(self, seg):
        pass
