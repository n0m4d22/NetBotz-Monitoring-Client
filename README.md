# NetBotz Monitoring Client
Custom NetBotz telemetry & monitoring client with real-time visual and audio alerts for Data Center operators.

---
## Contents
* [Description](#description)
* [Problem](#problem)
* [Features](#features)
* [Installation](#installation)
   * [Precompiled Binary](#precompiled-executable)
   * [Run from Source](#run-from-source)
* [Usage](#usage)
* [Compilation](#compilation)
* [License](#license)

---

## Description
This program is a custom **lightweight** monitoring client for APC/Schneider NetBotz appliances. By utilizing HTTP `GET` requests and direct XML scraping, it provides real-time environmental telemetry without relying on complex SNMP setups or heavy external dependencies.

The core purpose of this tool is to provide **customizable, real-time visual and audible warnings** to Data Center operators during critical sensor shifts (such as temperature spikes or humidity drops). By alerting operators to early indications of environmental instability, it helps prevent hardware downtime and costly Service Level Agreement (SLA) violations.

---

## Problem
Legacy APC/Schneider NetBotz appliances (such as the NetBotz 150 series) rely primarily on passive monitoring via web consoles or asynchronous notifications (Email/SNMP traps). 

Native web interfaces (e.g. NetBotz Rack Monitor 450) for these legacy units **do not support active browser-based audio alarms or persistent visual pop-up warnings** for active operators. As a result:
* Operators must continuously and manually monitor static dashboard panels.
* Early thermal fluctuations or humidity spikes can easily go unnoticed between notification polling cycles.
* Reaction time during critical environmental events is delayed, increasing the risk of SLA violations and thermal throttling.

---

## Features
* **Zero External Binaries:** Extracts clean telemetry directly via native HTTP XML endpoints, without the need of external binaries.
* **Multi-Node Support:** Seamlessly polls standalone IP appliances (e.g., Room Monitor 150) and parent units (Rack Monitor 450) in parallel.
* **Customizable Alerts:** Configurable audio and visual indicators for early warning thresholds.
* **Lightweight & Portable:** Designed to run in restricted environments with zero local setup friction.

---

## Installation

#### Precompiled Binary
The repository includes a standalone MS Windows executable compiled via PyInstaller for immediate deployment in operator workstations:

1. Download the latest release executable from the **Releases** section.
2. Run `NetBotzMonitor.exe` (no Python environment required).

#### Run from Source
Make sure you have the necessary requirements:
* **Python 3.13+**

Then:
1. Clone the repository:
   ```bash
   git clone https://github.com/n0m4d22/netbotz-monitoring-client.git
   cd netbotz-monitoring-client
   ```
2. Install the necessary libraries.
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

---

## Usage
Upon execution, the program presents a menu. Specifically, the user must configure the NetBotz Nodes by entering the **Setup** section. 

The configuration consists of two parameters:
 * **Nodes** 
 * **Credentials**
 
 The user is required to provide for each Node, basic information such as **label**, **local IP Address**.
 Login credentials are also required for query authentication. 
 
 Upon successful configuration the user can enable the monitoring **daemon**, a subprocess which actively monitors each Node and reports warnings/alarms on the root window.

---

## Compilation
To build the standalone single-file executable yourself using PyInstaller:
```bash
pyinstaller --onefile --name NetBotzMonitor main.py
```

---

## License
Distributed under the MIT License. See LICENSE for more information.