"""Transcribe a 16 kHz mono wav with FunASR, writing text + sentence timestamps.

Run with (this exact command line matters -- see references/pitfalls.md):
    uv run --no-project --python 3.10 --with funasr --with modelscope \
      --with "transformers>=4.40,<5" --with "numpy<2" \
      --with torch --with torchaudio \
      python run_asr.py <audio16k.wav> <out.txt> <out.json> [--hotwords "a b c"]

Model choice: SeACo-Paraformer rather than plain paraformer-large, because only
the SeACo variant accepts a hotword list. VAD (FSMN) splits the long recording
into speech segments and the CT-Transformer adds punctuation; both come from
ModelScope and cache after the first run.
"""
import argparse
import json
import sys
import time

ASR_MODEL = "iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
VAD_MODEL = "iic/speech_fsmn_vad_zh-cn-16k-common-pytorch"
PUNC_MODEL = "iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("out_txt")
    ap.add_argument("out_json")
    ap.add_argument("--hotwords", default="",
                    help="space separated; only helps for words already in the "
                         "model vocabulary (see references/corrections.md)")
    ap.add_argument("--batch-size-s", type=int, default=300)
    args = ap.parse_args()

    from funasr import AutoModel

    t0 = time.time()
    print("[1/2] loading models (first run downloads from ModelScope)...", flush=True)
    model = AutoModel(
        model=ASR_MODEL,
        vad_model=VAD_MODEL,
        punc_model=PUNC_MODEL,
        disable_update=True,
    )
    print("[1/2] ready in %.1fs" % (time.time() - t0), flush=True)

    kwargs = dict(input=args.audio, batch_size_s=args.batch_size_s,
                  sentence_timestamp=True)
    if args.hotwords.strip():
        kwargs["hotword"] = args.hotwords.strip()
        print("[info] hotwords: " + args.hotwords.strip(), flush=True)

    print("[2/2] transcribing...", flush=True)
    res = model.generate(**kwargs)
    item = res[0]

    with open(args.out_txt, "w", encoding="utf-8") as f:
        f.write(item["text"])

    def clean(o):
        if isinstance(o, dict):
            return {k: clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [clean(v) for v in o]
        if hasattr(o, "tolist"):
            return o.tolist()
        return o

    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(clean(res), f, ensure_ascii=False, indent=1)

    n = len(item.get("sentence_info", []))
    print("[done] %.1fs | chars=%d | segments=%d"
          % (time.time() - t0, len(item["text"]), n), flush=True)
    print("PREVIEW: " + item["text"][:300], flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
