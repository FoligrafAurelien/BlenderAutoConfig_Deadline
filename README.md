# 🧠 Blender GPU Auto-Configurator (Deadline Compatible)

This project provides an automated way to **configure Blender's render device settings based on GPU type**, and a files system through the network for the plugins. It can simplify the installation of your plugins and scripts Blender for your render farm.
It support environment switching (`DEV` vs `PROD`) and integration with **Thinkbox Deadline** render farms.

---

## 🚀 What It Does

- 🔍 Detects the machine's GPU at runtime (NVIDIA RTX or AMD)
- 🔧 Sets the Blender compute device to **OPTIX** (NVIDIA) or **HIP** (AMD)
- ✅ Enables only the GPU(s) in the render device list
- ❌ Disables CPU rendering if a GPU is available
- 📁 Loads configuration dynamically from local or network folders, depending on environment if you launch blender with the bat file
- 🧵 Compatible with **Blender 4.2+**
- ☁️ Works seamlessly with **Deadline render nodes**

---

## 📂 Folder Structure

```
/
├── blenderconfig/
│   └── userpref.blend for collected plugins and scripts   ← Blender GPU detection + setup
├── blenderscript/
│   └── BlenderForceGpuConfig.py   ← Blender GPU detection + setup
│   └── all yours scripts and plugins install through blender if you execute blender with .bat file.
├── config.env                                                       ← Environment flag (DEV or PROD)
├── [launch_blender.bat](launch_blender.bat)                         ← Main launcher script
└── README.md
```

---

## 🧾 `config.env`

This file controls where Blender loads its config/scripts from:

```env
STATE = DEV
```

You can version this file per machine or configure via deployment tools.

---

## 🖥️ `launch_blender.bat`

This script does the following:

1. Reads `STATE` from `config.env`
2. Sets `BLENDER_USER_CONFIG` and `BLENDER_USER_SCRIPTS` accordingly
3. Detects the GPU type (`NVIDIA RTX`, `AMD`, or none)
4. Launches Blender and runs [`set_render_engine.py`](blenderconfig/set_render_engine.py) with the detected engine

```bat
:: Example usage
start "" "C:\Program Files\Blender Foundation\Blender 4.2\blender.exe" --python "%BLENDER_USER_CONFIG%\set_render_engine.py"
```

---

## 🐍 `set_render_engine.py`

This Python script:

- Uses `wmic` to detect GPU name(s)
- Chooses between:
  - `OPTIX` → NVIDIA RTX cards
  - `HIP` → AMD cards
  - `CPU` fallback
- Updates Cycles render preferences
- Enables only GPU devices (if found)
- Leaves `userpref.blend` untouched (temporary session config only)

🔗 [View script](blenderconfig/set_render_engine.py)

---

## 🔗 Integration with Deadline

You can call `launch_blender.bat` as a pre-render script or integrate it into your **Deadline job submission system** to ensure all render nodes configure themselves automatically.

Example Deadline paths:
- Place the Python script in:  DEADLINE_REPOSITORY\custom\blenderconfig\set_render_engine.py`
- Call it from a Deadline event plugin or via a **Pre Load Script** on Blender jobs.

---

## 🧪 Example GPU Detection Output

```
GPU detected: NVIDIA GeForce RTX 4070
Recommended engine: OPTIX
Activated: GPU device 0
Disabled: CPU
```

---

## 🖼️ Screenshots (Optional)

You can include:
- ✅ Screenshot of Blender → Preferences → System → Cycles Devices with GPU active
- 📁 Explorer view showing `config.env` and folder structure
- 🖥️ Render log output from Deadline with detection info

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
