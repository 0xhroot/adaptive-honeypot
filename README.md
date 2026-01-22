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
        └─────────────────────────────────┘```



## 🔄 3. Attack Flow (End-to-End)

This section describes the **complete lifecycle of an attack**, from initial connection to adaptive deception and visualization.

---

### 🧨 Step-by-Step Flow

---

### 1️⃣ Attacker Connects
- Example:
  - SSH on port `2222`
- Attacker assumes:
  - A real server is running
  - Standard service configuration

---

### 2️⃣ Honeypot Service Responds
- Sends a realistic fake banner:
  - `OpenSSH_8.9p1`
- Accepts credentials but:
  - Always fails authentication **or**
  - Allows partial, controlled interaction
- No real system access is ever granted

---

### 3️⃣ Behavior Captured
The system observes and records:

- Username attempts
- Command strings
- Request frequency
- Time gaps between actions
- Session duration
- Protocol-specific metadata

---

### 4️⃣ Structured Logging
- Every interaction is converted into a **structured JSON event**
- Events include:
  - Session ID
  - Source IP
  - Action type
  - Timestamp
  - Raw payload (sanitized)
- Logs are stored in **SQLite** for durability and analysis

---

### 5️⃣ ML Engine Processes Data
- Runs:
  - Periodically **or**
  - In near real-time
- Extracts behavioral features such as:
  - Command entropy
  - Request rate
  - Known payload signatures
  - Timing variance

---

### 6️⃣ Attacker Classification
Based on learned behavior, attackers are classified into profiles such as:

- `bruteforce bot`
- `worm-like scanner`
- `human manual attacker`

These profiles are continuously refined as more data is collected.

---

### 7️⃣ Adaptive Response Triggered
The **Adaptive Response Engine** modifies system behavior dynamically:

- **Bots**
  - Slower responses
  - Artificial hangs
- **Human attackers**
  - Deeper fake filesystem
  - More believable interaction
- **Scanners**
  - Misleading HTTP headers
  - False service fingerprints

---

### 8️⃣ Dashboard Updates
The dashboard updates in real time with:

- Live attack feed
- Updated statistics
- Behavior cluster changes
- Session evolution timeline

---

## ⚖️ 4. Ethical & Legal Scope (Critical)

This project is designed **strictly for defensive security research**.

---

### 🚫 Explicit Boundaries
The system **does NOT** perform:

- ❌ Real exploitation
- ❌ Reverse shells
- ❌ Malware delivery
- ❌ Outbound scanning
- ❌ Retaliation of any kind

---

### ✅ Allowed Activities
The system **only performs**:

- ✔ Passive observation
- ✔ Deception via fake responses
- ✔ Synthetic, isolated environments
- ✔ Academic, hackathon, and research usage

---

### 🛡️ Design Safeguards
- No OS command execution
- No file writes outside the project directory
- No privilege escalation
- Clear warning banner in the README
- Default bind address: `127.0.0.1` (localhost)
- External exposure requires explicit configuration

These safeguards ensure the project remains **legal, ethical, and defensible**.

---

## 🧬 5. How Adaptability Works (Core Idea)

Adaptability in this system is **behavior-driven**, not signature-driven.

---

### 🔄 What Changes Dynamically?
- Protocol responses
- Timing delays
- Error messages
- Fake system state
- Depth of interaction

---

### ⏱️ When Does It Adapt?
- After sufficient data points per session
- When attacker behavior crosses defined thresholds
- When ML cluster confidence increases

---

### 🧠 Why This Works
- Bots expect consistency → broken by randomness
- Humans probe deeper → rewarded with fake depth
- Automated tools misclassify the environment

---

### 📊 Adaptive Response Examples

| Behavior Detected        | Adaptive Response                         |
|--------------------------|-------------------------------------------|
| SSH brute-force          | Add 2–5 second response delays             |
| Recon scanner            | Return misleading service banners          |
| Manual shell interaction | Fake `/etc/passwd`, fake running processes |
| Known exploit payload    | Simulated vulnerable response              |

The system **learns patterns, not exploits**, making it resilient to zero-day techniques.

---
