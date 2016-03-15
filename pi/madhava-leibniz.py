#! /usr/bin/env python

"""
Calculate Pi by adding and subtracting the infinite series of all odd fractions.

The "Leibniz series" or "Madhava-Leibniz series" 
1/1 - 1/3 + 1/5 - 1/7 + 1/9 ... = pi/4

Inspired by Matt Parker's Pi Day video:
https://www.youtube.com/watch?v=HrRMnzANHHs

# Findings:
Matched 1 digit  of pi after 20 iterations: 3.1
Matched 2 digits of pi after 120 iterations: 3.14
Matched 3 digits of pi after 1,689 iterations: 3.141
Matched 4 digits of pi after 10,795 iterations: 3.1415
Matched 5 digits of pi after 136,122 iterations: 3.14159
Matched 6 digits of pi after 1,530,001 iterations: 3.141592
Matched 7 digits of pi after 18,658,565 iterations: 3.1415926
Matched 8 digits of pi after 156,094,710 iterations: 3.14159265
Matched 9 digits of pi after 1,686,377,316 iterations: 3.141592653
Wikipedia says it will take about 5,000,000,000 to get to 10 digits.
"""

from __future__ import print_function

from math import pi
import sys
import logging
import datetime



logging.basicConfig(
        level=logging.INFO,
        #format="%(asctime)s %(levelname)s %(funcName)s(): %(message)s")
        format="%(levelname)s: %(message)s")
log = logging

is_even = lambda x: (x % 2) == 0
is_odd = lambda x: (x & 1) == 1 # bitwise method



class PiSearch(object):
    last_operation = 'add' # or 'sub'
    total = 0
    iterations = 0
    num_digits_found = 0
    start_time = None
    time = 0


    def find_pi(self, max_time=None):

        self.start_time = datetime.datetime.now()
        operation = 'add' # or 'sub'

        i = 0
        while True:
            i += 1 

            if not is_odd(i):
                continue

            denominator = i

            if operation == 'add':
                nominator = 1
                operation = 'sub'
            else:
                nominator = -1
                operation = 'add'

            n = self.next_term(nominator, denominator)
            self.total += n
            self.iterations += 1
            self.time = (
                    datetime.datetime.now()-self.start_time).total_seconds()
            self.last_fraction = (nominator, denominator)
            self._append_history(self.last_fraction)

            log.debug(self.status())

            match, num_places = self.test_against_pi(
                    self.last_result(), self.num_digits_found)

            if match and (num_places > self.num_digits_found):
                self.num_digits_found = num_places
                log.debug("**********************")
                log.info(
                        "Matched {:d} digits of pi "
                        "after {:,d} iterations "
                        "and {:.2f} seconds: \n"
                        "{} vs. \n{}".format(
                        num_places,
                        self.iterations,
                        self.time,
                        self.last_result(),
                        pi)
                )
                log.debug("**********************")


    def next_term(self, nominator, denominator):
        # nominator is either 1 or -1 depending if we are adding or subtracting
        # denominator is the next odd number in the series.

        assert( nominator == 1 or nominator == -1)
        assert( denominator > 0 )
        assert( is_odd(denominator) )

        # Python 2.x compatability, make sure we have at least 1 float
        result = float(nominator) / denominator

        log.debug("{}/{} : {}".format(nominator, denominator, result))

        return result


    def test_against_pi(self, n, min_places=1):
        """
        Test if `n` matches any part of pi
        @TODO speed this up. Can we search for just the next
        digit? Subtract the 2 numbers and compare instead
        of converting to strings?

        >>> ps = PiSearch()
        >>> ps.test_against_pi(3.140000, min_places=3)
        (False, 2)
        >>> ps.test_against_pi(3.140000, min_places=2)
        (True, 2)
        >>> ps.test_against_pi(3.141599)
        (True, 5)
        >>> ps.test_against_pi(3.555555)
        (False, 0)
        """
        pi_str = str(pi).split('.')[-1]

        # Make sure we keep as many trailing zeros as our copy of pi has: 
        n_str = "{:.{prec}f}".format(n, prec=len(pi_str))
        remainder_str = n_str.split('.')[-1]

        for i in range(len(remainder_str))[min_places:]:
            k = len(remainder_str) - i
            log.debug("Testing {} places: {} ".format(
                        k, remainder_str[:k]))
            if pi_str.startswith(remainder_str[:k]):
                if k >= min_places:
                    return (True, k)
                else: 
                    return (False, k)

        return (False, 0)


    def last_result(self):
        return self.total * 4


    def status(self):
        return (
            self.iterations,
            "{:d}/{:d}".format(*self.last_fraction), 
            "{:.2f} seconds".format(self.time),
            self.last_result(),
        )


    def recent_history(self, num=10):
        # Format last `n` fraction series nicely
        history_str = "..."
        for nom, denom in self._history[:num]:
            fraction_str = "{:d}/{:d}".format(nom, denom)
            if nom > 0:
                history_str += (" + " + fraction_str)
            else:
                history_str += (" - " + fraction_str.lstrip('-'))
        return history_str
        

    def _append_history(self, val):
        max_history = 100
        if not hasattr(self, '_history'):
            self._history = []
        if len(self._history) > max_history:
            del self._history[0]
        self._history.append(val)


    def print_summary(self):

        print("\nSummary:\n")
        print("The closest we got after {:,d} iterations is: \n"
              "{} vs. \n{} (that's pi)".format(
               self.iterations, 
               self.last_result(), 
               pi))

        print("\nLast few fractions in series: \n{}".format(
            self.recent_history(num=5)))

        print("\nTotal operation took {:,.2f} seconds "
              "(that's {:,.2f} minutes "
              "or {:,.4f} hours)".format(
                  self.time, self.time/60, self.time/60/60))


if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #     max_iterations = int(sys.argv[1])
    #     max_time...
    # else:
    #     max_iterations = 1700000 # ~6 decimal places of pie in ~2 minutes
    #     max_time...

    search = PiSearch()
    try:
        search.find_pi()
    except KeyboardInterrupt:
        search.print_summary()
        sys.exit(0)

    search.print_summary()
