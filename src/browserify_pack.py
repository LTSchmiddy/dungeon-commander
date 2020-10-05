import os, shutil
import util

browserify_dir = ".\\browserify\\"
output_dir = ".\\static\\browserify_pack\\"


util.mkdir_if_missing(output_dir)

for i in os.listdir(browserify_dir):
    if not i.endswith(".js"):
        print(f"Skipping {i}")
        continue

    bundle_name = i[:-3]
    bundle_dir = f"{output_dir}{bundle_name}"
    util.mkdir_if_missing(bundle_dir)

    js_file_path = f"{browserify_dir}{i}"
    js_file = open(js_file_path, 'r')
    js_cont = js_file.read()

    for line in js_cont.split("\n"):
        if line.startswith("//include:"):
            src_path = line[10:]

            if os.path.isdir(src_path):
                src_dir, src_name = os.path.split(os.path.abspath(src_path))
                dst_path = f"{bundle_dir}\\{src_name}"

                if os.path.isdir(dst_path):
                    shutil.rmtree(dst_path)
                shutil.copytree(src_path, f"{bundle_dir}\\{src_name}")

            else:
                src_dir, src_name = os.path.split(os.path.abspath(src_path))
                shutil.copy(src_path, f"{bundle_dir}")
    js_file.close()
    cmd = f"browserify {browserify_dir}{i} > {bundle_dir}\\{bundle_name}.bundle.js"
    print(cmd)
    os.system(cmd)