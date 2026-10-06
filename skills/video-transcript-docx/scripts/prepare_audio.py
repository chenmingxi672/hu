"""Probe a video for subtitles, or turn it into a 16 kHz mono wav for ASR.

Run with:
    uv run --with imageio-ffmpeg python prepare_audio.py <url-or-path> <workdir>
    uv run --with imageio-ffmpeg python prepare_audio.py <url> <workdir> --probe

Why this script exists: yt-dlp normally shells out to a system ffmpeg to
post-process audio, and this machine has none -- installing it needs admin
rights. imageio-ffmpeg ships a static ffmpeg binary inside a pip package, so we
borrow that instead. Same reason we never call yt-dlp's -x/--extract-audio:
downloading the raw audio stream needs no ffmpeg at all, and we do the
conversion ourselves with a binary we control.
"""
import argparse
import glob
import os
import subprocess
import sys


def log(msg):
    print(msg, flush=True)


def run(cmd):
    log("+ " + " ".join(str(c) for c in cmd))
    return subprocess.run(cmd)


def yt_dlp(args):
    # uvx resolves/caches yt-dlp itself, so the skill needs no global install.
    return run(["uvx", "yt-dlp", "--no-warnings", *args])


def ffmpeg_exe():
    import imageio_ffmpeg

    exe = imageio_ffmpeg.get_ffmpeg_exe()
    log("borrowed ffmpeg: " + exe)
    return exe


def probe(url):
    """Report whether the video carries real subtitles.

    Worth doing first: if the uploader provided subtitles, they beat ASR on both
    speed and accuracy, and no audio download is needed. Bilibili's *AI*
    subtitles require a logged-in cookie and will not show up here, so a
    "danmaku only" answer means "no usable subtitles" -- danmaku is scrolling
    audience comments, not a transcript.
    """
    log("== probing for subtitles ==")
    r = subprocess.run(
        ["uvx", "yt-dlp", "--no-warnings", "--skip-download", "--print",
         "%(id)s | %(title)s | %(duration)s sec | %(uploader)s", url],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    log((r.stdout or "").strip() or (r.stderr or "").strip())

    r = subprocess.run(
        ["uvx", "yt-dlp", "--no-warnings", "--list-subs", url],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (r.stdout or "") + (r.stderr or "")

    # yt-dlp prints a "Language  Formats" table, sometimes twice (manual
    # captions, then automatic ones). Parse the table rows -- substring-matching
    # the whole output is unreliable, because it also carries URLs, format
    # tables and warnings, and e.g. "ass" matches inside "pass"/"class".
    rows, in_table = [], False
    for line in out.splitlines():
        s = line.strip()
        if s.startswith("Language"):
            in_table = True
            continue
        if not in_table:
            continue
        if not s:
            in_table = False
            continue
        rows.append(s.split())
        log("  " + s)

    # "danmaku" is scrolling audience comments shipped as an xml track. It is
    # never a transcript, so a video whose only row is danmaku has no captions.
    usable = [row for row in rows if row and row[0].lower() != "danmaku"]
    log("")
    if usable:
        log("VERDICT: usable captions found (%s) -> fetch them, skip ASR"
            % ", ".join(row[0] for row in usable))
        return 0
    log("VERDICT: no usable captions (danmaku is not a transcript) -> run ASR")
    return 2


def fetch(url, workdir):
    os.makedirs(workdir, exist_ok=True)
    tmpl = os.path.join(workdir, "media_%(id)s.%(ext)s")
    # -f bestaudio gives a single raw stream; no ffmpeg post-processing needed.
    if yt_dlp(["-f", "bestaudio", "-o", tmpl, url]).returncode != 0:
        log("FAILED to download audio")
        return 1
    hits = [p for p in glob.glob(os.path.join(workdir, "media_*"))
            if not p.endswith(".wav")]
    if not hits:
        log("FAILED: yt-dlp reported success but produced no file")
        return 1
    src = max(hits, key=os.path.getmtime)
    log("downloaded: " + src)
    return to_wav(src, os.path.join(workdir, "audio16k.wav"))


def to_wav(src, dst):
    exe = ffmpeg_exe()
    r = run([exe, "-y", "-hide_banner", "-loglevel", "error",
             "-i", src, "-ac", "1", "-ar", "16000", "-vn", dst])
    if r.returncode != 0 or not os.path.exists(dst):
        log("FAILED to convert to 16 kHz mono wav")
        return 1
    log("wrote %s (%.1f MB)" % (dst, os.path.getsize(dst) / 1048576))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help="video URL, or a local audio/video file")
    ap.add_argument("workdir")
    ap.add_argument("--probe", action="store_true",
                    help="only report whether subtitles exist")
    ap.add_argument("--no-download", action="store_true",
                    help="treat source as an already-downloaded media file")
    args = ap.parse_args()

    os.makedirs(args.workdir, exist_ok=True)

    if args.probe:
        if not args.source.lower().startswith("http"):
            log("--probe only makes sense for a URL")
            return 2
        return probe(args.source)

    if args.no_download or not args.source.lower().startswith("http"):
        if not os.path.exists(args.source):
            log("no such file: " + args.source)
            return 1
        return to_wav(args.source, os.path.join(args.workdir, "audio16k.wav"))

    return fetch(args.source, args.workdir)


if __name__ == "__main__":
    sys.exit(main())
