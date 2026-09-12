# dataset/preprocess.py

from ultralytics import YOLO
import cv2, csv, os, time
from label_mapping import label_to_kata

def proses_semua_video(path_dataset, path_output):
    model = YOLO('yolov8n-pose.pt')
    os.makedirs(path_output, exist_ok=True)

    semua_video = [f for f in os.listdir(path_dataset) if f.endswith('.mp4')]
    print(f"Total video: {len(semua_video)}")

    total_video = 0
    total_gagal = 0
    waktu_mulai = time.time()

    for i, video_file in enumerate(sorted(semua_video)):
        parts = video_file.split('_')
        label = parts[1]
        kata  = label_to_kata.get(label, label)

        folder_kata = os.path.join(path_output, kata)
        os.makedirs(folder_kata, exist_ok=True)

        path_video = os.path.join(path_dataset, video_file)
        path_csv   = os.path.join(folder_kata, video_file.replace('.mp4', '.csv'))

        if os.path.exists(path_csv):
            print(f"[{i+1}] SKIP: {video_file}")
            total_video += 1
            continue

        cap          = cv2.VideoCapture(path_video)
        semua_baris  = []
        total_frames = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            total_frames += 1
            hasil = model(frame, verbose=False)
            if hasil[0].keypoints is not None and len(hasil[0].keypoints.data) > 0:
                kp    = hasil[0].keypoints.data[0].cpu().numpy()
                baris = [coord for titik in kp for coord in [float(titik[0]), float(titik[1]), float(titik[2])]]
                semua_baris.append(baris)

        cap.release()
        total_video += 1

        if semua_baris:
            with open(path_csv, 'w', newline='') as f:
                writer = csv.writer(f)
                header = [f'{c}{i}' for i in range(len(semua_baris[0])//3) for c in ['x','y','conf']]
                writer.writerow(header)
                writer.writerows(semua_baris)
            pct = len(semua_baris)/total_frames*100
            print(f"[{i+1}] ✅ {kata:<15} {video_file} — {len(semua_baris)}/{total_frames} ({pct:.0f}%)")
        else:
            total_gagal += 1
            print(f"[{i+1}] ❌ GAGAL: {video_file}")

    durasi = (time.time() - waktu_mulai) / 60
    print(f"\nSELESAI! {total_video - total_gagal}/{total_video} berhasil — {durasi:.1f} menit")