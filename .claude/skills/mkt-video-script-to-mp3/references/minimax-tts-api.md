# MiniMax TTS API Reference (t2a_v2)

## Endpoint
`POST https://api.minimax.io/v1/t2a_v2`

## Authentication
`Authorization: Bearer <MINIMAX_API_KEY>`

## Request Body

```json
{
  "model": "speech-2.8-hd",
  "text": "Your text here",
  "stream": false,
  "voice_setting": {
    "voice_id": "moss_audio_c56d6120-ef9c-11f0-9649-8ee40147f116",
    "speed": 1.08,
    "vol": 1,
    "pitch": 0
  },
  "audio_setting": {
    "sample_rate": 32000,
    "bitrate": 128000,
    "format": "mp3",
    "channel": 1
  },
  "pronunciation_dict": {
    "tone": ["Omg/Oh my god"]
  },
  "language_boost": "Vietnamese",
  "voice_modify": {
    "pitch": 0,
    "intensity": 0,
    "timbre": 0,
    "sound_effects": "spacious_echo"
  },
  "output_format": "hex"
}
```

## Key Parameters

| Field | Values | Notes |
|-------|--------|-------|
| model | `speech-2.8-hd` | Latest HD model |
| speed | 0.5 – 2.0 | Default project speed: 1.08 |
| vol | 0 – 10 | Default: 1 |
| pitch | -12 – 12 | Default: 0 |
| format | `mp3`, `pcm`, `flac` | Default: mp3 |
| sample_rate | 8000, 16000, 22050, 24000, 32000, 44100 | Default: 32000 |
| bitrate | 32000, 64000, 128000, 256000 | Default: 128000 |
| channel | 1 (mono), 2 (stereo) | Default: 1 |
| output_format | `hex`, `url` | hex = inline audio data |
| language_boost | `Vietnamese`, `English`, `Chinese`, `auto`, etc. | |

## pronunciation_dict.tone
Map abbreviations or custom pronunciations: `"Omg/Oh my god"` makes TTS read "Omg" as "Oh my god".

## voice_modify (optional)
- `sound_effects`: `spacious_echo`, `bathroom_echo`, `bedroom_echo`, `machine_distortion`, etc.

## Response

```json
{
  "data": {
    "audio": "<hex encoded audio bytes>",
    "status": 2
  },
  "extra_info": {
    "audio_length": 11124,
    "audio_sample_rate": 32000,
    "audio_size": 179926,
    "bitrate": 128000,
    "usage_characters": 163,
    "audio_format": "mp3",
    "audio_channel": 1
  },
  "trace_id": "...",
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

Decode audio: `bytes.fromhex(data["data"]["audio"])` → write to .mp3 file.
