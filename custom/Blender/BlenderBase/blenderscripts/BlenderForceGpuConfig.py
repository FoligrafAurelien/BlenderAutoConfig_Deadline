import bpy
import subprocess

def is_valid_gpu_name(name: str) -> bool:
    name = name.upper()
    if "INTEL" in name:
        return False
    if "RADEON(TM)" in name:
        return False
    if "VEGA" in name and "MOBILE" in name:
        return False
    return True

def detect_gpu_brand():
    try:
        result = subprocess.run(
            ['wmic', 'path', 'win32_VideoController', 'get', 'Name'],
            capture_output=True, text=True, check=True
        )
        gpu_names = [
            line.strip() for line in result.stdout.split('\n')
            if line.strip() and "Name" not in line
        ]
        for gpu in gpu_names:
            if not is_valid_gpu_name(gpu):
                continue
            if "NVIDIA" in gpu.upper() and "RTX" in gpu.upper():
                return 'OPTIX'
            elif "AMD RADEON" in gpu.upper():
                return 'HIP'
    except Exception as e:
        print(f"Erreur lors de la détection GPU: {e}")
    return 'CPU'

# === Main logic ===
engine = detect_gpu_brand()
print(f"[INFO] Detected engine: {engine}")

prefs = bpy.context.preferences.addons["cycles"].preferences
prefs.compute_device_type = engine
prefs.get_devices()

# Disable all devices first
for device in prefs.devices:
    device.use = False

# Enable only valid GPUs
if engine in ["OPTIX", "HIP"]:
    for device in prefs.devices:
        if device.type != 'CPU' and is_valid_gpu_name(device.name):
            print(f"[INFO] Enabled GPU: {device.name}")
            device.use = True
else:
    print("[INFO] Fallback to CPU.")
