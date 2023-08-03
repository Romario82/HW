from pathlib import Path
from shutil import copyfile
from threading import Thread


def search(path : Path):
    list_dir = []
    list_dir.append(path)
    for i_dir in path.iterdir():
        if i_dir.is_dir():
            list_dir.append(i_dir)
            search(i_dir)
        return list_dir

def copy_file(path : Path):
    for f in path.iterdir():
        if f.is_file():
            extension = f.suffix
            new_dir = out_dir / extension
            new_dir.mkdir(exist_ok=True, parents=True)
            copyfile(f, new_dir / f.name)
#----------------------------------------------------
try:
    in_dir = Path(input("Копіювати файли з -> "))
    out_dir = Path(input("Копіювати файли в -> "))
    res_dir = search(in_dir)

    streams = []
    for folder in res_dir:
        st = Thread(target=copy_file, args=(folder,))
        st.start()
        streams.append(st)

    [st.join() for st in streams]
except FileNotFoundError:
    print(f"Немає такої папки - {in_dir}!")

print('OK')