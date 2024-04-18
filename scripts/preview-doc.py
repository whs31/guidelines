import shutil
import os

QUARTZ_PATH = r"C:\Users\whs31\quartz"

def main():
    if not os.path.exists(QUARTZ_PATH):
        print(f"Error: {QUARTZ_PATH} does not exist")
        return
    if not os.path.exists(r"..\code-style"):
        print(f"Error: {r'..\code-style'} does not exist")
        print("Please, launch the script from the scripts folder")
        return
    shutil.rmtree(os.path.join(QUARTZ_PATH, "content"))
    shutil.copytree(r"..\code-style", os.path.join(QUARTZ_PATH, "content"))
    cwd = os.getcwd()
    os.chdir(QUARTZ_PATH)
    os.system("npx quartz build --serve")
    print("Done.")

if __name__ == "__main__":
    main()