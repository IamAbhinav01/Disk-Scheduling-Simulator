class Scheduler:
    def __init__(self, algorithm, jobs, context_switch=0, zone_size=20, aging_factor=0.1, alpha=0.7):
        self.algorithm = algorithm
        self.jobs = sorted(jobs, key=lambda x: x.arrival_time)
        self.context_switch = context_switch
        self.zone_size = zone_size
        self.aging_factor = aging_factor
        self.alpha = alpha  # Smoothing factor for EMA (0 < alpha < 1)
        self.ready_queue = []
        self.running = None
        self.head_position = 50  # Initial head position
        self.predicted_track = 50  # Initial EMA prediction
        self.system_time = 0
        self.total_seek_time = 0
        self.completed_jobs = 0
        self.log = []
        self.changes = []

    def update_queues(self):
        while self.jobs and self.jobs[0].arrival_time <= self.system_time:
            job = self.jobs.pop(0)
            self.ready_queue.append(job)
            self.log.append(f"{job} arrived at track {job.track}")

    def fcfs(self):
        if not self.running and self.ready_queue:
            self.running = self.ready_queue.pop(0)
            self.log.append(f"{self.running} started at head {self.head_position}")

    def sstf(self):
        if not self.running and self.ready_queue:
            self.ready_queue.sort(key=lambda job: abs(job.track - self.head_position))
            self.running = self.ready_queue.pop(0)
            self.log.append(f"{self.running} started (SSTF) at head {self.head_position}")

    def apzs(self):
        if not self.running and self.ready_queue:
            # Update wait time and priority for all jobs
            for job in self.ready_queue:
                job.wait_time += 1
                job.priority += job.wait_time * self.aging_factor  # Age-based priority boost

            # Define zones based on head position
            inner_zone = [job for job in self.ready_queue if abs(job.track - self.head_position) <= self.zone_size]
            outer_zone = [job for job in self.ready_queue if job not in inner_zone]

            # AI: Calculate priority with EMA prediction
            for job in self.ready_queue:
                # Boost priority if job is near predicted track
                distance_to_predicted = abs(job.track - self.predicted_track)
                prediction_bonus = max(0, 50 - distance_to_predicted) / 50  # Normalize bonus (0-1)
                job.priority += prediction_bonus * 2  # Weight prediction in priority

            # Select next job (inner zone first, then outer)
            if inner_zone:
                inner_zone.sort(key=lambda job: (abs(job.track - self.head_position) / (job.priority + 1)))
                self.running = inner_zone[0]
                self.ready_queue.remove(self.running)
            elif outer_zone:
                outer_zone.sort(key=lambda job: (abs(job.track - self.head_position) / (job.priority + 1)))
                self.running = outer_zone[0]
                self.ready_queue.remove(self.running)
            self.log.append(f"{self.running} started (APZS) at head {self.head_position}, priority {self.running.priority:.2f}, predicted track {self.predicted_track:.1f}")

    def step(self):
        self.update_queues()
        if self.running:
            self.running.progress += 1
            seek_distance = abs(self.head_position - self.running.track)
            self.total_seek_time += seek_distance
            self.head_position = self.running.track  # Move head
            self.changes.append(f"Head moved to {self.head_position}, seek distance: {seek_distance}")
            
            # AI: Update EMA prediction after servicing
            self.predicted_track = (self.alpha * self.head_position) + (1 - self.alpha) * self.predicted_track

            if self.running.progress >= 1:  # Service complete
                self.log.append(f"{self.running} completed at track {self.running.track}")
                self.completed_jobs += 1
                self.running = None
        else:
            if self.algorithm == "FCFS":
                self.fcfs()
            elif self.algorithm == "SSTF":
                self.sstf()
            elif self.algorithm == "APZS":
                self.apzs()
        
        self.system_time += 1

    def get_metrics(self):
        throughput = self.completed_jobs / self.system_time if self.system_time > 0 else 0
        return {
            "Total Seek Time": self.total_seek_time,
            "Throughput": throughput,
            "Completed Jobs": self.completed_jobs,
            "System Time": self.system_time,
            "Predicted Track": self.predicted_track
        }