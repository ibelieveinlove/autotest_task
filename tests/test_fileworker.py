from fileworker import file_worker
import pytest

def test_file_read_write(tmp_path):
    # Создаем входной файл с URL
    input_file = tmp_path / "in.txt"
    input_file.write_text("https://ya.ru\nhttps://google.com\n")

    fw = file_worker(str(input_file))
    urls = fw.file_reader()
    assert urls == ["https://ya.ru", "https://google.com"]

    output_file = tmp_path / "out.txt"
    fw_out = file_worker(str(output_file))
    fw_out.file_writer(
        "https://ya.ru",
        {"Success": 1, "Failed": 0, "Error": 0, "Other": 0},
        {"Min": 0.1, "Max": 0.2, "Avg": 0.15},
        flag=True
    )

    assert output_file.exists()
    content = output_file.read_text()
    assert "https://ya.ru" in content