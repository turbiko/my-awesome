
Як правило це треба для Raspberry Pi, більшість з яких (крім топових пристроїв) **не має повноцінного USB-boot**, але існують **обхідні способи завантажити**, наприклад:

# **boot з microSD → rootfs на NVMe / USB SSD / USB Flash**

Це працює стабільно.

Тобто:

- microSD містить тільки `/boot`
- USB-диск містить `/` (root-файлова система)

### Як налаштувати:

1. На microSD встанови стандартний Raspberry Pi OS або Ubuntu.
2. Підключи USB-накопичувач.
3. Створи новий розділ ext4 на USB:

```bash
sudo mkfs.ext4 /dev/sda1
```

4. Скопіюй rootfs на USB:
```bash
sudo rsync -aAXv / --exclude={"/boot/*","/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found"} /mnt/usb/
```

5. Зміни `/boot/cmdline.txt`, додавши:
```
root=/dev/sda1 rootfstype=ext4 rootwait
```

6. Перезавантаж — система працюватиме з USB, SD використовується лише для boot.


