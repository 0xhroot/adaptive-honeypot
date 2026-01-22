# Adaptive Honeypot That Learns Attack Patterns Live

⚠️ Research & defensive security only.

An async, Python-based adaptive honeypot that observes, learns, and dynamically deceives attackers.

Built for:
- Security research
- Hackathons
- Learning adversarial behavior


# 🛡️ Adaptive Honeypot Architecture

This project is an **event-driven, asynchronous honeypot platform** designed for cybersecurity research and hackathon demonstrations.  
It emulates real services, observes attacker behavior, learns patterns in real time, and dynamically adapts its deception strategies.

---

## 🧠 1. High-Level Architecture (Simple but Technical)

At a high level, the system is composed of multiple **loosely coupled layers**, each responsible for a specific security function.

### 🔹 Core Layers Overview

---

### 🌐 Network Deception Layer
- Fake services implemented using **asyncio**
- Supported protocols:
  - SSH
  - HTTP
  - FTP
- Mimics real protocol behavior to attract attackers
- **Never executes real commands**
- Completely isolated from the host OS

---

### 👁️ Observation & Telemetry Layer
Captures detailed attacker activity, including:
- Source IP and port
- Timestamps
- Commands / payloads
- Request sequences
- Timing between actions

All data is emitted as **structured JSON events** for consistency and analysis.

---

### 💾 Persistence Layer
- Lightweight **SQLite** database
- Append-only design (for forensic integrity)
- Optimized for **read-heavy analytics**
- Stores both raw events and extracted features

---

### 🤖 Learning Layer (ML / Behavior Engine)
- Consumes historical and live attack data
- Extracts behavioral features
- Performs:
  - Clustering
  - Anomaly detection
- Generates attacker **behavior profiles**

---

### 🎭 Adaptive Response Engine
Uses learned behavior profiles to dynamically:
- Change service banners
- Introduce artificial delays
- Inject fake errors
- Modify virtual filesystem views
- Escalate deception depth over time

The goal is to **confuse attackers while gathering intelligence**.

---

### 📊 Visualization & Control Layer
- Flask-based web dashboard
- Read-only interface for safety
- Provides:
  - Live attack feed
  - Pattern summaries
  - Behavior evolution over time

---

## 🗺️ 2. Text-Based Architecture Diagram

```text
                ┌────────────────────┐
                │     Attacker        │
                │ (SSH / HTTP / FTP)  │
                └─────────┬──────────┘
                          │
                          ▼
        ┌─────────────────────────────────┐
        │      Async Honeypot Services     │
        │ ┌────────┐ ┌────────┐ ┌──────┐ │
        │ │  SSH   │ │ HTTP   │ │ FTP  │ │
        │ └────────┘ └────────┘ └──────┘ │
        └─────────┬──────────────────────┘
                  │ (events)
                  ▼
        ┌─────────────────────────────────┐
        │ Structured Event Logger (JSON)   │
        └─────────┬──────────────────────┘
                  │
                  ▼
        ┌─────────────────────────────────┐
        │        SQLite Database           │
        │  - sessions                     │
        │  - commands                     │
        │  - requests                     │
        │  - behavior_features            │
        └─────────┬──────────────────────┘
                  │
                  ▼
        ┌─────────────────────────────────┐
        │     ML / Behavior Analyzer       │
        │  - clustering                   │
        │  - anomaly detection            │
        └─────────┬──────────────────────┘
                  │ (profiles)
                  ▼
        ┌─────────────────────────────────┐
        │ Adaptive Response Engine         │
        │  - deception strategy            │
        │  - protocol mutation             │
        └─────────┬──────────────────────┘
                  │
                  ▼
        ┌─────────────────────────────────┐
        │ Flask Dashboard (Read-only)      │
        │  - live feed                     │
        │  - charts                        │
        │  - behavior clusters             │
        └─────────────────────────────────┘
