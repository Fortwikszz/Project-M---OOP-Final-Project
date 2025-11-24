# Project M - OOP Final Project

Game project menggunakan Pygame-CE dan Python 3.12

## Prerequisites

- Python 3.10 atau lebih baru
- pip (Python package manager)

## Instalasi

1. **Clone atau download repository ini**
   ```bash
   git clone https://github.com/Fortwikszz/Project-M---OOP-Final-Project.git
   cd Project-M---OOP-Final-Project
   ```

2. **Install dependencies**
   
   Ada 2 cara:

   **Cara 1: Menggunakan pip langsung**
   ```bash
   pip install pygame-ce
   ```

   **Cara 2: Menggunakan requirements.txt**
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan game**
   
   Pastikan Anda berada di folder root project (bukan di folder `code`), lalu jalankan:
   
   ```bash
   python code/main.py
   ```

   Atau jika menggunakan Python 3 secara spesifik:
   ```bash
   python3 code/main.py
   ```

## Cara Bermain

- **Gerak**: Gunakan tombol Arrow Keys (↑↓←→) atau WASD
- **Attack**: Klik kiri mouse
- **Keluar**: Tutup window atau tekan tombol X

## Struktur Project

```
Project-M---OOP-Final-Project/
├── assets/              # Asset gambar dan sprites
│   ├── Tiny Swords (Free Pack)/
│   └── Tiny Swords (Update 010)/
├── code/                # Source code
│   ├── main.py         # Entry point
│   ├── level.py        # Level management
│   ├── player.py       # Player class
│   ├── tiled.py        # Tile class
│   └── settings.py     # Game settings
├── test/               # Test assets
├── requirements.txt    # Dependencies
└── README.md          # This file
```

## Troubleshooting

### Error: ModuleNotFoundError: No module named 'pygame'

Solusi: Install pygame-ce terlebih dahulu
```bash
pip install pygame-ce
```

### Error: No file '...' found

Solusi: Pastikan Anda menjalankan game dari **folder root** project (bukan dari folder `code`)
```bash
# Benar ✅
cd Project-M---OOP-Final-Project
python code/main.py

# Salah ❌
cd Project-M---OOP-Final-Project/code
python main.py
```

### Window tidak muncul atau langsung tertutup

- Pastikan tidak ada error di terminal
- Cek apakah window muncul di belakang window lain
- Lihat taskbar untuk window "Projeect M"

## Credits

- Assets: Tiny Swords by Pixel Frog
- Game Engine: Pygame Community Edition (pygame-ce)
