import time
from collections import deque
import math

class DeltaTimeCounter:
    def __init__(self, sample_size=100):
        self.sample_size = sample_size
        self.frame_times = deque([0.0] * sample_size, maxlen=sample_size)
        self.running_sum = 0.0
        self.valid_samples = 0
        self.frame_index = 0
        self.last_frame_time = time.time()

    def Reset(self):
        self.frame_times.clear()
        self.frame_times.extend([0.0] * self.sample_size)
        self.running_sum = 0.0
        self.valid_samples = 0
        self.frame_index = 0
        self.last_frame_time = time.time()

    def Count(self):
        current_frame_time = time.time()
        delta = current_frame_time - self.last_frame_time
        self.last_frame_time = current_frame_time

        
        # remove the oldest value from running_sum
        self.running_sum -= self.frame_times[self.frame_index]
        
        # store the new frame time and add it to running_sum
        self.frame_times[self.frame_index] = delta
        self.running_sum += delta
        
        # increment frame index (circular buffer)
        self.frame_index = (self.frame_index + 1) % self.sample_size
        
        # increase valid_samples until it reaches sample_size
        if self.valid_samples < self.sample_size:
            self.valid_samples += 1


    def CountAndDisplay(self, x, y, what_counting):
        current_frame_time = time.time()
        delta = current_frame_time - self.last_frame_time
        
        # remove the oldest value from running_sum
        self.running_sum -= self.frame_times[self.frame_index]
        
        # store the new frame time and add it to running_sum
        self.frame_times[self.frame_index] = delta
        self.running_sum += delta
        
        # increment frame index (circular buffer)
        self.frame_index = (self.frame_index + 1) % self.sample_size
        
        # increase valid_samples until it reaches sample_size
        if self.valid_samples < self.sample_size:
            self.valid_samples += 1

        self.Display(x, y, what_counting)
        self.last_frame_time = time.time()

    def Display(self, x, y, what_counting):
        if self.valid_samples < self.sample_size:
            # displays how far till valid sample_size
            print(f"\033[{y};{x}H\033[2KLoading {what_counting}: {self.valid_samples}/{self.sample_size} samples", end='', flush=True)
        else:
            # display deltaTime average (ms)
            avg = self.GetDelta()
            print(f"\033[{y};{x}H\033[2KAverage {what_counting} Time: {avg * 1000.0:.2f} ms", end='\n', flush=True)

    def GetDelta(self):
        if self.valid_samples == 0:
            return 0.0
        return self.running_sum / self.sample_size