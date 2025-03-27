import streamlit as st
from job_generator import generate_jobs
from scheduler import Scheduler
import time

st.title("Disk Scheduling Simulator")  ##added streamlit functionality

st.sidebar.header("Request Generation Parameters")
num_jobs = st.sidebar.slider("Number of Requests", 1, 20, 5)
arrival_range = st.sidebar.slider("Arrival Time Range", 0, 100, (0, 50))
priority_range = st.sidebar.slider("Priority Range", 1, 10, (1, 5))
track_range = st.sidebar.slider("Track Range (0-199)", 0, 199, (0, 199))
context_switch = st.sidebar.slider("Context Switch Time", 0, 10, 0)
zone_size = st.sidebar.slider("APZS Zone Size", 10, 50, 20)
aging_factor = st.sidebar.slider("APZS Aging Factor", 0.0, 1.0, 0.1)
alpha = st.sidebar.slider("EMA Alpha (Prediction Smoothing)", 0.1, 0.9, 0.7)

if st.sidebar.button("Generate Requests"):
    jobs = generate_jobs(num_jobs, arrival_range, priority_range, track_range)
    st.session_state.jobs = jobs
    st.session_state.running = False

if "jobs" in st.session_state:
    algorithm = st.selectbox("Select Scheduling Algorithm", ["FCFS", "SSTF", "APZS"])
    if st.button("Start Simulation"):
        st.session_state.scheduler = Scheduler(algorithm, st.session_state.jobs, context_switch, zone_size, aging_factor, alpha)
        st.session_state.running = True

if "scheduler" in st.session_state and st.session_state.running:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("Next Step"):
            st.session_state.scheduler.step()
    with col2:
        speed = st.slider("Animation Speed", 0.1, 2.0, 1.0)
    with col3:
        if st.button("Next Change"):
            while st.session_state.scheduler.changes:
                st.session_state.scheduler.step()
                if not st.session_state.scheduler.changes:
                    break

    if st.checkbox("Enable Animation"):
        while st.session_state.running and (st.session_state.scheduler.ready_queue or st.session_state.scheduler.running):
            st.session_state.scheduler.step()
            time.sleep(1 / speed)
            st.rerun()

    st.subheader("Ready Queue")
    for job in st.session_state.scheduler.ready_queue:
        st.write(f"Request {job.pid} at track {job.track}, Priority: {job.priority:.2f}")
        st.progress(job.progress)

    st.subheader("Running Request")
    if st.session_state.scheduler.running:
        running_job = st.session_state.scheduler.running
        st.write(f"Request ID: {running_job.pid}, Track: {running_job.track}")
        st.progress(running_job.progress)

    st.subheader("Log")
    st.text_area("Log", "\n".join(st.session_state.scheduler.log), height=200)

    st.subheader("Changes")
    st.text_area("Changes", "\n".join(st.session_state.scheduler.changes), height=200)

    st.subheader("System Status")
    metrics = st.session_state.scheduler.get_metrics()
    st.write(f"Total Seek Time: {metrics['Total Seek Time']}")
    st.write(f"Throughput: {metrics['Throughput']:.2f} jobs/unit")
    st.write(f"Completed Jobs: {metrics['Completed Jobs']}")
    st.write(f"System Time: {metrics['System Time']}")
    st.write(f"Predicted Next Track: {metrics['Predicted Track']:.1f}")

    if st.button("Stop Simulation"):
        st.session_state.running = False

if "running" not in st.session_state:
    st.session_state.running = False