import subprocess
import sys

def install_package():
    cont = True
    while(cont):
       package = input("What package would you like to install?")
       try:
           print(f"Installing { package }...")
           subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
           subprocess.check_call([sys.executable, "-m", "pip", "install", package])
           if package == "playwright":
               subprocess.check_call([sys.executable, "-m", "playwright", "install"])
           elif package == "pandas":
               subprocess.check_call([sys.executable, "-m", "pip", "install", "jupyter"])
               subprocess.check_call([sys.executable, "-m", "jupyter", "notebook"])
           print(f"{package} installed successfully.")
       except subprocess.CalledProcessError as e:
           print("An error occurred during installation.")
           print(e)
       except Exception as ex:
           print("Unexpected error:", ex)
       cont = True if input("do you have more you would like to install?(y/n)").lower() == "y" else False
if __name__ == "__main__":
    install_package()