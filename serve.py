#!/usr/bin/env python3
"""Static file server WITH HTTP Range support + threading.

Python's stock `http.server` answers every request with a full 200 and no
Accept-Ranges, so <video> reports seekable=[] and the scroll-flight engine
can't scrub — it falls back to downloading whole clips as blobs, which stalls.
This server answers `Range:` with 206 Partial Content, so video seeks natively
(exactly what a real host/CDN does), and serves each request on its own thread
so several clips can load at once.
"""
import os
import re
import functools
import http.server


class RangeHandler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"  # keep-alive + proper range handling

    def send_head(self):
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()
        try:
            f = open(path, "rb")
        except OSError:
            self.send_error(404, "File not found")
            return None
        try:
            fs = os.fstat(f.fileno())
            size = fs.st_size
            ctype = self.guess_type(path)
            rng = self.headers.get("Range")
            if not rng:
                self.send_response(200)
                self.send_header("Content-type", ctype)
                self.send_header("Content-Length", str(size))
                self.send_header("Accept-Ranges", "bytes")
                # dev server: revalidate so a stale cache from the old
                # (non-range) server can't keep a clip "unseekable"
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
                self.end_headers()
                return f

            m = re.match(r"bytes=(\d*)-(\d*)\s*$", rng.strip())
            if not m:
                self.send_error(400, "Invalid Range")
                f.close()
                return None
            g1, g2 = m.group(1), m.group(2)
            if g1 == "":
                length = int(g2) if g2 else 0
                start = max(0, size - length)
                end = size - 1
            else:
                start = int(g1)
                end = int(g2) if g2 else size - 1
            end = min(end, size - 1)
            if start > end or start >= size:
                self.send_response(416)
                self.send_header("Content-Range", "bytes */%d" % size)
                self.send_header("Content-Length", "0")
                self.end_headers()
                f.close()
                return None

            length = end - start + 1
            self.send_response(206)
            self.send_header("Content-type", ctype)
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Range", "bytes %d-%d/%d" % (start, end, size))
            self.send_header("Content-Length", str(length))
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            f.seek(start)
            return _LimitedReader(f, length)
        except Exception:
            f.close()
            raise


class _LimitedReader:
    """File wrapper that yields at most `length` bytes, so copyfile() sends
    exactly the requested range."""

    def __init__(self, fileobj, length):
        self._f = fileobj
        self._remaining = length

    def read(self, amt=-1):
        if self._remaining <= 0:
            return b""
        if amt is None or amt < 0 or amt > self._remaining:
            amt = self._remaining
        data = self._f.read(amt)
        self._remaining -= len(data)
        return data

    def close(self):
        self._f.close()


def main():
    port = int(os.environ.get("PORT", "4599"))
    root = os.path.dirname(os.path.abspath(__file__))
    handler = functools.partial(RangeHandler, directory=root)
    server = http.server.ThreadingHTTPServer(("", port), handler)
    print("Serving %s on port %d (Range + threading)" % (root, port), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
