import sys
import csv
import chardet

sys.path.append("../")
from helper.main import Main
from helper.static_data import all_codecs


class Encode(Main):
    def prepare_init(self) -> None:
        pass

    def get_encoding(self, fpath):
        with open(fpath, "rb") as input_file:
            for line in input_file.readlines():
                detect = chardet.detect(line)
                if detect["confidence"] > 0.8:
                    break
        encoding = detect["encoding"]
        self.log.info(f"{encoding} with confidence level {detect['confidence']}")
        return encoding

    def test_file_open(self, fpath, encoding):
        try:
            with open(fpath, "r", encoding=encoding) as input_file:
                csv_reader = csv.reader(input_file)
                for line in csv_reader:
                    pass
                return
        except Exception as e:
            return e

    def get_verified_encoding(self, fpath, expected_codec="utf-8", first_level=True):
        """First verify if the expected Encoding is Corerct or not.
        If Not then, try reading file with various encoding"""
        exception = self.test_file_open(fpath, expected_codec)
        if not exception:
            return expected_codec
        else:
            if "byte" in exception.reason:
                bytes_chunk = exception.object[exception.start : exception.end + 20]
                self.log.debug(bytes_chunk)
                for codec in all_codecs:
                    try:
                        decoded_byte = bytes_chunk.decode(codec)
                        encoded_byte = decoded_byte.encode(codec)
                        if encoded_byte == bytes_chunk:
                            exception = self.test_file_open(fpath, codec)
                            if not exception:
                                return codec
                            else:
                                bytes_chunk = exception.object[exception.start : exception.end + 10]
                    except:
                        pass
        return None


if __name__ == "__main__":
    # Testing
    from os import listdir, path
    from helper.config import Config

    encode = Encode("File_encoding")
    config = Config()
    sample_dir = config.sample_dir
    all_files = [f for f in listdir(sample_dir) if path.isfile(path.join(sample_dir, f))]
    for fname in all_files:
        fpath = path.join(sample_dir, fname)
        file_encoding = encode.get_verified_encoding(fpath)
        encode.log.info(f"{fname}, {file_encoding=}")
        with open(fpath, "r", encoding=file_encoding) as csv_file:
            csv_reader = csv.reader(csv_file)
            for idx, row in enumerate(csv_reader):
                pass
