from utils.env_utils import load_environment

load_environment()

from config import CONFIG
from core.orchestrator import AssistantOrchestrator
from utils.audio_utils import play_audio_file


STOP_WORDS = ["stop", "quitter", "fin"]


def should_stop(user_text: str) -> bool:
    text = user_text.lower().strip()
    return any(word in text for word in STOP_WORDS)


def main() -> None:
    orchestrator = AssistantOrchestrator()
    session_id = orchestrator.create_session(CONFIG.default_session_name)

    print("🚀 Assistant vocal pré-cloud activé.")
    print(f"🧠 Session créée : {session_id}")
    print("👉 Parle quand tu veux.")
    print("👉 Dis 'stop', 'quitter' ou 'fin' pour arrêter.\n")

    while True:
        result = orchestrator.run_once(session_id=session_id)

        if result is None:
            print("⚠️ Aucun résultat exploitable.\n")
            continue

        stt_result = result["stt_result"]
        brain_result = result["brain_result"]
        translation_result = result["translation_result"]
        response_text = result["response_text"]
        tts_result = result["tts_result"]

        print(f"\n📝 Toi : {stt_result.text}")

        if should_stop(stt_result.text):
            print("\n🛑 Mot d’arrêt détecté. Fermeture du programme.")
            break

        print(f"🧠 Intent détecté : {brain_result.intent}")
        print(f"🎭 Mode réponse : {brain_result.mode}")
        print(
            f"🌐 Web : {brain_result.use_web} | "
            f"🌍 Traduction : {brain_result.use_translation} | "
            f"❤️ Émotion : {brain_result.use_emotion}"
        )

        if translation_result is not None:
            print("🌍 Traduction déclenchée")
            print(f"🔤 Source : {translation_result.source_lang}")
            print(f"🎯 Cible : {translation_result.target_lang}")
            print(f"🧾 Texte traduit : {translation_result.translated_text}")

        print(f"🤖 Assistant : {response_text}")

        if tts_result.file_path:
            play_audio_file(tts_result.file_path)

        print()


if __name__ == "__main__":
    main()