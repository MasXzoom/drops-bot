# Auto Quest & Claim Bot

- Bot ini mengotomatisasi proses menyelesaikan quest dan klaim reward
- Bot ini mendukung banyak akun dan dapat memproses task untuk semua akun sebelum mengklaim reward secara otomatis.

## Fitur

- **Multi-Akun**: Bot mendukung banyak akun dengan membaca token dari file `token.txt`.
- **Otomatisasi Task**: Bot akan otomatis memverifikasi dan menyelesaikan quest baru untuk setiap akun.
- **Auto-Claim Reward**: Setelah semua task selesai, bot akan otomatis mengklaim reward untuk setiap akun.
- **Tunggu Sebelum Klaim**: Anda dapat mengatur waktu tunggu sebelum proses klaim dimulai.
- **Tampilkan Informasi Pengguna**: Bot menampilkan username dan saldo akun untuk setiap akun yang diproses.

## Instalasi

### Prasyarat

- **Python 3.6** atau lebih tinggi
- Install library Python yang dibutuhkan:

```bash
pip install requests colorama
