import bpy
import sys
import subprocess


def detect_gpu_brand():
    try:
        
        result = subprocess.run(
            ['wmic', 'path', 'win32_VideoController', 'get', 'Name'],
            capture_output=True, text=True, check=True
        )
        print ("result", {result})
        gpus = result.stdout.split('\n')
        gpu_names = [line.strip() for line in gpus if line.strip() and "Name" not in line]
        for gpu in gpu_names:
            name = gpu.upper()

            # Ignore iGPU / embedded / non-Cycles-compatible GPUs
            if "INTEL" in name:
                continue
            if "RADEON(TM)" in name:  # Often integrated
                continue
            if "VEGA" in name and "MOBILE" in name:
                continue

            if "NVIDIA" in name and "RTX" in name:
                return 'OPTIX'
            elif "AMD RADEON" in name:
                return 'HIP'
    except Exception as e:
        print(f"Erreur lors de la détection GPU: {e}")
        return 'CPU'

engine = detect_gpu_brand()
print(f"Le moteur conseillé est : {engine}")

if engine in ["OPTIX", "HIP"]:
    bpy.context.preferences.addons["cycles"].preferences.compute_device_type = engine
    for device in bpy.context.preferences.addons["cycles"].preferences.devices:
        print ("devices:",{device})
        device.use = False
        if device.type != 'CPU':
            print(f"Activation du GPU : {device.name}")
            device.use = True
        
else:
    # Mettre en CPU
    bpy.context.preferences.addons["cycles"].preferences.compute_device_type = "NONE"
    bpy.context.scene.cycles.device = "CPU"
