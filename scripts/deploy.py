import shutil
import os

#QUARTZ_PATH = r"C:\Users\whs31\quartz"
QUARTZ_PATH = r"D:\share\quartz\quartz"

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
    os.system("npx quartz build")
    print("Build done.")
    shutil.rmtree(os.path.join(cwd, "..", "docs"))
    print("Removed docs folder.")
    # mkdir cwd/../docs
    os.makedirs(os.path.join(cwd, "..", "docs"))
    print("Created docs folder.")
    shutil.copytree(os.path.join(QUARTZ_PATH, "public"), os.path.join(cwd, "..", "docs", "public"))
    print("Copied public folder.")
    #unwrap cwd/../public/* to cwd/../docs/*
    for f in os.listdir(os.path.join(cwd, "..", "docs", "public")):
        shutil.move(os.path.join(cwd, "..", "docs","public", f), os.path.join(cwd, "..", "docs", f))
    print("Unwrapped public folder.")
    shutil.rmtree(os.path.join(cwd, "..", "docs", "public"))
    print("Done.")

if __name__ == "__main__":
    main()