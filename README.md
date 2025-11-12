# 🧠 Blender GPU Auto-Configurator (Deadline Compatible)

This project provides an automated way to **configure Blender's render device settings based on GPU type**, and a files system through the network for the plugins. It can simplify the installation of your plugins and scripts Blender for your render farm.
It support environment switching (`DEV` vs `PROD`) and integration with **Thinkbox Deadline** render farms.

---

## 🚀 What It Does

- 🔍 Detects the machine's GPU at runtime (NVIDIA RTX or AMD)
- 🔧 Sets the Blender compute device to **OPTIX** (NVIDIA) or **HIP** (AMD) or **CPU** from **Dealine OPTION** (see https://github.com/FoligrafAurelien/DeadlineBlenderSubmission)
- ✅ Enables only the GPU(s) in the render device list
- ❌ Disables CPU rendering if a GPU is available and Deadline set to GPU
- 📁 Loads configuration dynamically from network folders to synchronize plugin and parameters
- 🧵 Compatible with **Blender 4.2+**
- ☁️ Works seamlessly with **Deadline render nodes** (see https://github.com/FoligrafAurelien/DeadlineBlenderSubmission)

---

## 📂 Folder Structure

```
/
├── Deadline10Repo\custom\Blender\BlenderBase\blenderconfig/
│   └── userpref.blend for collected plugins and scripts
├── Deadline10Repo\custom\Blender\BlenderBase\blenderscript/
│   └── BlenderForceGpuConfig.py   ← Blender GPU detection + setup
│   └── all yours scripts and plugins install through blender if you execute blender with .bat file.
├── config.env                                                       ← Environment flag (DEV or PROD) if needed
└── README.md
```

---

## 🧾 `config.env`

This file controls where Blender loads its config/scripts from:

```env
STATE = DEV
```


---

## 🐍 `BlenderForceGpuConfig.py`

This Python script:

- Uses `wmic` to detect GPU name(s)
- Chooses between:
  - `OPTIX` → NVIDIA RTX cards
  - `HIP` → AMD cards
  - `CPU` fallback
- Updates Cycles render preferences
- Enables only GPU devices (if found and Deadline configure in GPU)
- Leaves `userpref.blend` untouched (temporary session config only)

🔗 [View script](blenderconfig/BlenderForceGpuConfig.py)

---

## 🔗 Integration with Deadline

Example Deadline paths:
- Place the Python script in:  DEADLINE_REPOSITORY\custom\Blender\BlenderBase\blenderconfig\BlenderForceGpuConfig.py`
- Call it from a Deadline event plugin (see https://github.com/FoligrafAurelien/DeadlineBlenderSubmission) or via a **Pre Load Script** on Blender jobs.

---

## 🧪 Example GPU Detection Output

```
GPU detected: NVIDIA GeForce RTX 4070
Recommended engine: OPTIX
Activated: GPU device 0
Disabled: CPU
```

---


## ✅ Requirements

- Blender 4.2+
- Windows 10 or 11
- Deadline 10+
- A supported GPU:
  - NVIDIA RTX (for OPTIX)
  - AMD RDNA (for HIP)

---

## 📄 License

MIT — use freely in commercial or personal render pipelines.

---

## 🙌 Credits

Developed by **Aurélien Binauld for le Fresnoy**  
Optimized for scalability, simplicity, and render farm automation.
