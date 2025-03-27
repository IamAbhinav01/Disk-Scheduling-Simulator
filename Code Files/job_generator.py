import random

class Job:
    def __init__(self, pid, arrival_time, priority, track):
        self.pid = pid
        self.arrival_time = arrival_time
        self.priority = priority
        self.track = track
        self.wait_time = 0
        self.progress = 0

    def __str__(self):
        return f"Request[{self.pid}]"

def generate_jobs(num_jobs, arrival_range, priority_range, track_range):
    jobs = []
    for pid in range(num_jobs):
        arrival_time = random.randint(arrival_range[0], arrival_range[1])
        priority = random.randint(priority_range[0], priority_range[1])
        track = random.randint(track_range[0], track_range[1]) ## added track_range
        jobs.append(Job(pid, arrival_time, priority, track))
    return jobs