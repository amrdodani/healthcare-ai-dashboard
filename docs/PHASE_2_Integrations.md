
# Phase 2: Communications & Multimodal Integrations

## WhatsApp via Twilio
- Add your Twilio SID, Auth Token, and WhatsApp number to `whatsapp_sender.py`
- Use after GPT generates a high-priority insight (e.g., overcapacity)

## Email via SMTP
- Works with Gmail App Passwords
- Update sender credentials in `email_sender.py`

## Voice Input
- Use `voice_input.py` to transcribe `.wav` or `.mp3` using Whisper

## Text to Speech
- Use `text_to_speech.py` to read GPT outputs aloud
