from preprocessing.extract_keypoints import extract_video_keypoints
from classifier.predict import predict_keypoints
from llm.generate import generate_sentence


def process_video(video_path):
    """
    Pipeline utama AI Engine:

    Video
      ↓
    MediaPipe
      ↓
    LSTM
      ↓
    Kata BISINDO
      ↓
    Gemini
      ↓
    Kalimat
    """

    print("=== AI ENGINE ===")
    print(f"Video: {video_path}")

    # 1. Ekstraksi keypoints
    print("\n[1] Ekstraksi keypoints...")
    keypoints = extract_video_keypoints(video_path)

    print(f"Shape keypoints: {keypoints.shape}")

    # 2. Prediksi menggunakan LSTM
    print("\n[2] Prediksi LSTM...")
    predicted_id, predicted_word, confidence = predict_keypoints(
        keypoints
    )

    print(f"Predicted ID: {predicted_id}")
    print(f"Predicted Word: {predicted_word}")
    print(f"Confidence: {confidence:.2%}")

    # 3. Generate kalimat menggunakan Gemini
    print("\n[3] Generate kalimat...")
    sentence = generate_sentence(predicted_word)

    print(f"Generated Sentence: {sentence}")

    # 4. Hasil akhir
    return {
        "predicted_id": predicted_id,
        "word": predicted_word,
        "confidence": confidence,
        "sentence": sentence
    }


if __name__ == "__main__":
    video_path = "ai_engine/test_video.mp4"

    try:
        result = process_video(video_path)

        print("\n" + "=" * 50)
        print("HASIL AKHIR AI ENGINE")
        print("=" * 50)
        print(f"Kata       : {result['word']}")
        print(f"Confidence : {result['confidence']:.2%}")
        print(f"Kalimat    : {result['sentence']}")
        print("=" * 50)

    except Exception as e:
        print("\nERROR:")
        print(e)