import pytest
from src.models import Mahasiswa, DaftarMahasiswa


class TestMahasiswa:
    def test_buat_mahasiswa_valid(self):
        mhs = Mahasiswa("2024SI001", "Andi Pratama", "Sistem Informasi", 2024, 3.50)
        assert mhs.nim == "2024SI001"
        assert mhs.ipk == 3.50

    def test_nim_tidak_valid(self):
        with pytest.raises(ValueError):
            Mahasiswa("abc", "Test", "SI", 2024, 3.0)

    def test_nim_kosong(self):
        with pytest.raises(ValueError):
            Mahasiswa("", "Test", "SI", 2024, 3.0)

    def test_ipk_diluar_range(self):
        with pytest.raises(ValueError):
            Mahasiswa("2024SI002", "Test", "SI", 2024, 5.0)

    def test_ipk_boundary(self):
        assert Mahasiswa("2024SI003", "A", "SI", 2024, 0.0).ipk == 0.0
        assert Mahasiswa("2024SI004", "B", "SI", 2024, 4.0).ipk == 4.0

    def test_nama_sangat_panjang(self):
        mhs = Mahasiswa("2024SI005", "A" * 200, "SI", 2024, 3.0)
        assert len(mhs.nama) == 200


class TestDaftarMahasiswa:
    def test_tambah_dan_cari(self):
        db = DaftarMahasiswa()
        mhs = Mahasiswa("2024SI001", "Andi", "SI", 2024)
        db.tambah(mhs)
        assert db.cari("2024SI001") == mhs
        assert db.jumlah == 1

    def test_nim_duplikat(self):
        db = DaftarMahasiswa()
        db.tambah(Mahasiswa("2024SI001", "Andi", "SI", 2024))
        with pytest.raises(ValueError):
            db.tambah(Mahasiswa("2024SI001", "Budi", "SI", 2024))

    def test_hapus_nim_tidak_ada(self):
        assert DaftarMahasiswa().hapus("999999") is False

    def test_cari_nim_tidak_ada(self):
        assert DaftarMahasiswa().cari("999999") is None

    def test_edit_ipk(self):
        db = DaftarMahasiswa()
        db.tambah(Mahasiswa("2024SI001", "Andi", "SI", 2024, 3.0))
        assert db.edit_ipk("2024SI001", 3.8) is True
        assert db.cari("2024SI001").ipk == 3.8
        with pytest.raises(ValueError):
            db.edit_ipk("2024SI001", 4.5)