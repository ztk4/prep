#!/usr/bin/python3

import unittest as ut
import random

#modifies
def selection_sort(l):
    for i in range(len(l)):
        min_ind = min(enumerate(l[i:], i), key=lambda x: x[1])[0]

        l[i], l[min_ind] = l[min_ind], l[i]

def insertion_sort(l):
    for i, val in enumerate(l[1:], 1):
        for j in range(i-1, -1, -1):
            if l[j] <= val:
                l[j+1] = val
                break

            l[j+1] = l[j]
        else:
            l[0] = val

def merge_sort(l):
    if len(l) == 1:
        return
    if len(l) == 2:
        if l[0] > l[1]:
            l[0], l[1] = l[1], l[0]
        return

    split = len(l) // 2
    low, high = l[:split], l[split:]
    merge_sort(low)
    merge_sort(high)

    low_ind, high_ind = 0, 0
    for i in range(len(l)):
        if high_ind >= len(high) or \
                low_ind < len(low) and low[low_ind] < high[high_ind]:
            l[i] = low[low_ind]
            low_ind += 1
        else:
            l[i] = high[high_ind]
            high_ind += 1

#low and high are inclusive
def quick_sort(l, low = 0, high = None):
    if high is None:
        high = len(l) - 1
    if high <= low:
        return

    mid = (high - low) // 2
    lv, mv, hv = l[low], l[mid], l[high]

    #median of 3
    if lv <= mv:
        if mv <= hv:
            p = mv
        elif hv <= lv:
            p = lv
        else: #lv < hv < mv
            p = hv
    else: #mv < lv
        if lv <= hv:
            p = lv
        elif hv <= mv:
            p = mv
        else: #mv < hv < lv
            p = hv

    #partition
    lp, hp = low, high
    while lp != hp:
        while l[lp] < p:
            lp += 1
        while l[hp] >= p and hp > lp:
            hp -= 1
        l[lp], l[hp] = l[hp], l[lp]

    #second "fat" partition
    fp, hp = hp, high #bounds of right partition, where all elements equal to p are
    while fp != hp:
        while l[hp] != p:
            hp -= 1
        while l[fp] == p and fp < hp:
            fp += 1
        l[fp], l[hp] = l[hp], l[fp]

    #print(p, low, lp, hp, high, *enumerate(l[low:high+1], low))

    #preform smaller partition first
    if lp - low < high - hp:
        quick_sort(l, low, lp - 1)
        quick_sort(l, hp + 1, high)
    else:
        quick_sort(l, hp + 1, high)
        quick_sort(l, low, lp - 1)

def heap_sort(l):
    end = len(l) - 1
    heapify(l, 0, end)

    for e in range(end, 0, -1):
        l[0], l[e] = l[e], l[0]

        sift_down(l, 0, e - 1)

#inclusive
#makes heap from s to e
def heapify(l, s, e):
    for tmp in range((e-1) // 2, -1, -1):
        sift_down(l, tmp, e)

#inclusive
#fixes heap rooted at s, assuming all children are fine
def sift_down(l, s, e):
    r = s
    swap = r

    while r*2 + 1 <= e:
        child = r*2 + 1

        if l[swap] < l[child]:
            swap = child
        if child + 1 <= e and l[swap] < l[child + 1]:
            swap = child + 1

        if swap == r:
            return
        l[swap], l[r] = l[r], l[swap]
        r = swap

#positive integers ONLY
def radix_sort(l):
    m = max(l)
    temp = [0] * len(l)
    count= [0] * 0x10001
    shift = 0

    while m > 0:                                        #stop when there is no signifigance of digits in higher four byte chunks
        for i in range(len(count)):                     #reset count
            count[i] = 0

        for n in l:                                     #count all the occurances in bucket (LS 2byte) + 1
            count[((n >> shift) & 0xFFFF) + 1] += 1
        for i in range(len(count) - 1):                 #sum count up the array to have a running sum
            count[i+1] += count[i]
        for n in l:                                     #place at index based on running sum, increase starting index for next one
            i = (n >> shift) & 0xFFFF
            temp[count[i]] = n
            count[i] += 1

        shift += 16                                     #shift over to next LS 2bytes

        for i in range(len(count)):                     #reset count
            count[i] = 0

        for n in temp:                                  #same as above, but from temp back to l
            count[((n >> shift) & 0xFFFF) + 1] += 1
        for i in range(len(count) - 1):
            count[i+1] += count[i]
        for n in temp:
            i = (n >> shift) & 0xFFFF
            l[count[i]] = n
            count[i] += 1

        shift += 16                                     #shift over to next LS 2bytes

        m >>= 32                                        #shift over largest integer 4 bytes

def test_sort(sort_func):
    def dec(test_func): #disregard test_func, (it should only have pass in the body anyhow)
        def f(self):
            sort_func(self.l)
            self.assertEqual(self.l, self.check)
        return f
    return dec

class SortTester(ut.TestCase):

    def setUp(self):
        self.l = [random.randint(0, 1000) for i in range(10000)]
        self.check = sorted(self.l)

    @test_sort(insertion_sort)
    def test_isort():
        pass

    @test_sort(selection_sort)
    def test_ssort():
        pass

    @test_sort(merge_sort)
    def test_msort():
        pass

    @test_sort(quick_sort)
    def test_qsort():
        pass


    @test_sort(heap_sort)
    def test_hsort():
        pass

    @test_sort(radix_sort)
    def test_rsort():
        pass

if __name__ == '__main__':
    suite = ut.TestLoader().loadTestsFromTestCase(SortTester)
    ut.TextTestRunner(verbosity=2).run(suite)

    arr = [random.randint(1 << 64, 1 << 1024) for i in range(100000)]
    check = sorted(arr)

    #print('[',*(arr + [']']), sep='\n')
    radix_sort(arr)
    #print('[',*(arr + [']']), sep='\n')

    print(arr == check)
