import time
from collections import deque
import statistics

class DeltaTimeCounter:
    def __init__(self, sample_size=100):
        self.sample_size = sample_size
        self.frame_times = deque([0.0] * sample_size, maxlen=sample_size)
        self.average_delta = 0.0
        self.valid_samples = 0
        self.last_frame_time = time.time()

    def Reset(self):
        self.frame_times.clear()
        self.frame_times.extend([0.0] * self.sample_size)
        self.average_delta = 0.0
        self.valid_samples = 0
        self.last_frame_time = time.time()

    def Count(self):
        current_frame_time = time.time()
        delta = current_frame_time - self.last_frame_time
        self.last_frame_time = current_frame_time

        self.frame_times.append(delta)
        self.valid_samples = min(self.valid_samples + 1, self.sample_size)

        # calculate average delta time
        if self.valid_samples > 0:
            self.average_delta = statistics.mean(self.frame_times)

    def Display(self, x, y, what_counting):
        if self.valid_samples < self.sample_size:
            # displays how far till valid sample_size
            print(f"\033[{y};{x}H\033[2KLoading {what_counting}: {self.valid_samples}/{self.sample_size} samples", end='', flush=True)
        else:
            # display deltaTime average (ms)
            print(f"\033[{y};{x}H\033[2KAverage {what_counting} Time: {self.average_delta * 1000.0:.2f} ms", end='\n', flush=True)

    def GetDelta(self):
        if self.valid_samples < self.sample_size:
            return float('nan')  # return NaN when not enough samples
        return self.average_delta