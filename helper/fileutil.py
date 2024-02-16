import os
import glob
import shutil
import zipfile


class Fileutil:
    def __init__(self):
        self.os_name = os.name

    def path_join(self, *splitted_dirtext):
        """Joins the partial path as a full path in current System Format
        If partial path includes delimiter of another system, it convertes them to current system
        Eg. path_join('mydrive', 'mydir', 'myfile')
            in darwin  => mydrive/mydir/myfile
            in windows => mydrive\\mydir\\myfile"""

        delimiter = os.path.sep
        full_path = os.path.join(*splitted_dirtext)
        full_path = full_path.replace("/" if self.os_name == "nt" else "\\", delimiter)
        return full_path

    # フォルダが存在しないとき作成
    def make_dir(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    # ファイルの有無を確認
    def is_file(self, file_path):
        return os.path.isfile(file_path)

    # フォルダの有無を確認
    def is_dir(self, dirname):
        return os.path.isdir(dirname)

    # ファイルの移動
    def move_file(self, file_path, move_file_path):
        shutil.move(file_path, move_file_path)

    # ファイルのコピー
    def copy_file(self, file_path, copy_file_path):
        shutil.copy(file_path, copy_file_path)

    # ファイルを削除
    def delete_file(self, filename):
        return os.remove(filename)

    # ディレクトリを削除
    def delete_dir(self, dir_path):
        if self.check_dir(dir_path):
            shutil.rmtree(dir_path)
        else:
            print(f"{dir_path} doesnot exists")

    # ファイルの読み込み(一行ずつ)
    def read_file_list(self, file_path, encoding="utf-8-sig"):
        with open(file_path, "r", encoding=encoding) as f:
            l = f.readlines()
        return l

    # ディレクトリ以下のファイルフルパスの一覧を取得
    def get_filename_list_from_path(self, dir_path, do_recursive=True):
        print(f"Searching files with Recursive Mode: {do_recursive} ")
        return glob.glob(dir_path + "\\**\\*", recursive=do_recursive)

    def split_names(self, path):
        if path:
            return os.path.split(path)

    def split_ext(self, fname):
        if fname:
            return os.path.splitext(fname)

    def change_extension(self, fpath, target_extension):
        if fpath:
            fname_only, extension = self.split_ext(fpath)
            return f"{fname_only}.{target_extension.replace('.', '')}"

    def get_parent(self, anypath, level=1):
        for i in range(level):
            anypath = os.path.dirname(anypath)
        return anypath

    # zip圧縮する
    def file_compression(self, filenamelist, zipfilename):
        with zipfile.ZipFile(zipfilename, "w", compression=zipfile.ZIP_DEFLATED) as new_zip:
            for filename in filenamelist:
                fdir, fname = os.path.split(filename)
                dirname = os.path.basename(fdir)
                new_zip.write(filename, f"{dirname}/{fname}")

    # zip圧縮して元ファイルを削除する(1つ目の引数は圧縮対象のリスト。ファイル・フォルダどちらも可。)
    def backup_zip(self, filenamelist, zipfilename_fullpath, delete_original=True):
        target_file_list = []
        for filename in filenamelist:
            if self.check_file(filename):
                target_file_list.append(filename)
            else:
                if self.check_dir(filename):
                    target_file_list += self.get_filename_list_from_path(filename)

        self.file_compression(target_file_list, zipfilename_fullpath)
        if delete_original:
            for filename in filenamelist:
                if self.check_file(filename):
                    self.delete_file(filename)
                else:
                    if self.check_dir(filename):
                        self.delete_dir(filename)
