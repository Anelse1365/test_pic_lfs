import os
import random
import shutil
from collections import defaultdict
from datetime import datetime

# กำหนดโฟลเดอร์ต้นทางหลัก
main_source_folder = r'E:\ipu'

# สร้างโฟลเดอร์ปลายทางใหม่ตามวันที่และเวลาปัจจุบัน
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
destination_folder = os.path.join(r'E:\test_pic_lfs', f'separated_images_{current_time}')
os.makedirs(destination_folder, exist_ok=True)

# รับเปอร์เซ็นต์ที่ต้องการจากผู้ใช้
try:
    sampling_percentage = float(input("กรุณาระบุเปอร์เซ็นต์ที่ต้องการสุ่ม (0-100): "))
    if sampling_percentage <= 0 or sampling_percentage > 100:
        raise ValueError("โปรดระบุค่าที่อยู่ระหว่าง 0 ถึง 100")
    sampling_percentage /= 100  # แปลงเป็นทศนิยม
except ValueError as e:
    print("ข้อผิดพลาด:", e)
    exit()

# ใช้ os.walk เพื่อเข้าถึงไฟล์ในโฟลเดอร์ต้นทางและสร้างกลุ่มจากเลข 8 ตัวแรกของชื่อไฟล์
all_groups = defaultdict(list)
for root, _, files in os.walk(main_source_folder):
    for file_name in files:
        # ดึงเลข 8 ตัวแรกจากชื่อไฟล์
        prefix = file_name[:8]
        # จัดกลุ่มไฟล์ตาม prefix
        all_groups[prefix].append(os.path.join(root, file_name))

# กรองเฉพาะกลุ่มที่มีมากกว่า 1 ภาพเท่านั้น
filtered_groups = {prefix: files for prefix, files in all_groups.items() if len(files) > 1}

# แสดงจำนวนภาพในแต่ละกลุ่มทั้งหมดก่อนทำการสุ่ม
print("จำนวนภาพในแต่ละกลุ่มที่มีการซ้ำ:")
for prefix, files in filtered_groups.items():
    print(f"กลุ่ม {prefix}: มี {len(files)} ภาพ")

# คำนวณขนาดตัวอย่างของกลุ่มโดยรวมทั้งหมด
total_groups = len(filtered_groups)
sampled_groups_count = max(1, int(total_groups * sampling_percentage))  # จำนวนกลุ่มที่จะสุ่ม

# เลือกกลุ่มที่ต้องการสุ่มแบบสุ่ม
selected_prefixes = random.sample(list(filtered_groups.keys()), sampled_groups_count)

# ตั้งค่าเปอร์เซ็นต์ไฟล์ที่จะสุ่มจากแต่ละกลุ่มที่เลือก (สามารถปรับได้)
file_sampling_ratio = 0.5  # เช่น ต้องการสุ่ม 50% ของไฟล์ในแต่ละกลุ่มที่ถูกเลือก

print("\nผลการสุ่มและการคัดลอกไฟล์:")
# คัดลอกไฟล์ในกลุ่มที่สุ่มเลือกไปยังโฟลเดอร์ปลายทาง โดยสุ่มบางส่วนจากแต่ละกลุ่ม
for prefix in selected_prefixes:
    group_files = filtered_groups[prefix]
    sampled_file_count = max(1, int(len(group_files) * file_sampling_ratio))  # จำนวนไฟล์ที่จะสุ่มในกลุ่มนี้
    sampled_files = random.sample(group_files, sampled_file_count)  # สุ่มเลือกไฟล์

    print(f"\nกลุ่ม {prefix} (สุ่มเลือก {sampled_file_count} จากทั้งหมด {len(group_files)} ภาพ):")
    for file_path in sampled_files:
        # คัดลอกไฟล์ที่อยู่ในกลุ่มเดียวกันไปยังโฟลเดอร์ปลายทาง
        shutil.copy(file_path, destination_folder)

