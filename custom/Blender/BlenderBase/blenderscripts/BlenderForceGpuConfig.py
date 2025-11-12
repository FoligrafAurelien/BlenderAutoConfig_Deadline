import bpy
import subprocess
import socket
import datetime
import os

# =========================
# CONFIGURATION DU LOG
# =========================
# Nom du fichier de log basé sur le hostname

# machine_name = socket.gethostname()
# log_dir = r"\\SRVDEADLINE\DeadlineRepository10\custom\Blender\Blender 4.4\logs"
# log_path = os.path.join(log_dir, f"{machine_name}.log")

# Crée le dossier de log si inexistant
# os.makedirs(log_dir, exist_ok=True)

# Petite fonction utilitaire
# def write_log(message: str):
    # """Écrit une ligne dans le log horodaté."""
    # timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # with open(log_path, "a", encoding="utf-8") as log_file:
        # log_file.write(f"{timestamp} / {message}\n")
    # print(f"[LOG] {message}")

# =========================
# LANCEMENT DU SCRIPT
# =========================
mode = bpy.context.scene.cycles.device.upper()
# write_log(f"Render Mode: {mode}")

# =========================
# GPU MODE
# =========================
if mode == "GPU":
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
            valid_gpus = []
            for gpu in gpu_names:
                if not is_valid_gpu_name(gpu):
                    continue
                valid_gpus.append(gpu)
                if "NVIDIA" in gpu.upper() and "RTX" in gpu.upper():
                    return 'OPTIX', valid_gpus
                elif "AMD RADEON" in gpu.upper():
                    return 'HIP', valid_gpus
            # Aucun GPU compatible trouvé
            return 'CPU', valid_gpus
        except Exception as e:
            error_msg = f"Erreur lors de la détection GPU: {e}"
            # write_log(error_msg)
            print(error_msg)
            return 'CPU', []

    engine, gpu_list = detect_gpu_brand()
    # write_log(f"Detected Engine: {engine}")
    # if gpu_list:
        # for gpu in gpu_list:
            # write_log(f"Detected GPU: {gpu}")
    # else:
        # write_log("No valid GPU detected.")

    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = engine
    prefs.get_devices()

    # Désactivation de tous les devices
    for device in prefs.devices:
        device.use = False

    # Activation des GPU valides
    if engine in ["OPTIX", "HIP"]:
        for device in prefs.devices:
            if device.type != 'CPU' and is_valid_gpu_name(device.name):
                device.use = True
                log_line = f"Enabled GPU: {device.name}"
                print(f"[INFO] {log_line}")
                # write_log(log_line)
    # else:
        # write_log("[INFO] Fallback to CPU (no GPU found).")

# =========================
# CPU MODE
# =========================
else:
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "NONE"
    prefs.get_devices()

    for device in prefs.devices:
        if device.type != 'CPU' and device.use:
            device.use = False
            msg = f"[INFO] Disabled GPU: {device.name}"
            print(msg)
            # write_log(msg)

    for device in prefs.devices:
        if device.type == 'CPU':
            device.use = True
            msg = f"[INFO] Enabled CPU device: {device.name}"
            print(msg)
            # write_log(msg)

    # write_log("[INFO] Compute device type set to CPU (NONE)")
