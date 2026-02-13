import os
import subprocess
import webbrowser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EDL_PATH = os.path.join(BASE_DIR, "tools", "edl", "edlclient", "edl.py")
MTK_PATH = os.path.join(BASE_DIR, "tools", "mtk", "mtk.py")
ADB_PATH = os.path.join(BASE_DIR, "bin", "adb.exe")

def check_tools_status():
    return {
        "Qualcomm 9008 Engine": os.path.exists(EDL_PATH),
        "MediaTek BROM Engine": os.path.exists(MTK_PATH),
        "ADB/Fastboot System": os.path.exists(ADB_PATH)
    }

def get_online_links(query):
    q = query.replace(" ", "+")
    return [
        {"name": f"☁ SamFW: {query}", "url": f"https://samfw.com/firmware/{q}"},
        {"name": f"☁ MIUI: {query}", "url": f"https://miui.org/?s={q}"}
    ]

def run_command(tool, action, log_func):
    # Здесь ты можешь добавить реальный вызов subprocess
    log_func(f"Executing {action} via {tool} backend...")
    # Пример: subprocess.Popen(["python", MTK_PATH, "printgpt"])