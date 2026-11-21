#!/usr/bin/env python3
"""
ALLALONE SDR bridge — streams an RTL-SDR Blog V4 into the ALLALONE app.

The app (SOURCE page) connects to  ws://<this-host>:8765  and receives live
spectrum frames; it can send tune/scan commands back. Works with any
librtlsdr device, but written and tested against the RTL-SDR Blog V4.

Run:  python3 allalone-bridge.py  [--freq 100e6] [--rate 2.4e6] [--gain auto]
"""
import argparse, asyncio, json, sys
import numpy as np

try:
    import websockets
    from rtlsdr import RtlSdr
except ImportError:
    sys.exit("Install deps first:  pip install -r requirements.txt")

NBINS = 64
clients = set()

def build_sdr(args):
    sdr = RtlSdr()
    sdr.sample_rate = float(args.rate)
    sdr.center_freq = float(args.freq)
    sdr.gain = args.gain if args.gain == 'auto' else float(args.gain)
    # RTL-SDR Blog V4 notes:
    #  - needs the rtl-sdr-blog driver fork (see README) — the old Osmocom
    #    build will NOT enumerate the V4 correctly.
    #  - HF (<24 MHz) works via the V4's built-in path; enable only if needed:
    # sdr.set_direct_sampling(0)
    #  - bias-tee for powering an LNA (careful — don't short it):
    # try: sdr.set_bias_tee(args.bias)
    # except Exception: pass
    return sdr

def read_spectrum(sdr):
    s = sdr.read_samples(16384)
    win = np.hanning(len(s))
    sp = np.fft.fftshift(np.fft.fft(s * win))
    pw = 20 * np.log10(np.abs(sp) + 1e-9)
    usable = (len(pw) // NBINS) * NBINS
    return pw[:usable].reshape(NBINS, -1).mean(axis=1).tolist()

async def streamer(sdr):
    loop = asyncio.get_event_loop()
    while True:
        if clients:
            bins = await loop.run_in_executor(None, read_spectrum, sdr)
            msg = json.dumps({"t": "spectrum", "f0": sdr.center_freq,
                              "bw": sdr.sample_rate, "bins": bins})
            await asyncio.gather(*[c.send(msg) for c in list(clients)],
                                 return_exceptions=True)
        await asyncio.sleep(0.05)

def make_handler(sdr):
    async def handler(ws):
        clients.add(ws)
        print(f"client connected ({len(clients)} total)")
        await ws.send(json.dumps({"t": "status", "msg": "RTL-SDR Blog V4 bridge online"}))
        try:
            async for raw in ws:
                try:
                    m = json.loads(raw)
                except Exception:
                    continue
                cmd = m.get("cmd")
                if cmd == "tune":
                    if m.get("freq"):
                        f = float(m["freq"])
                        if f > 1.766e9:
                            await ws.send(json.dumps({"t": "status",
                                "msg": "V4 tops out near 1.766 GHz — can't tune 2.4/5 GHz"}))
                        else:
                            sdr.center_freq = f
                    if m.get("bw"):
                        sdr.sample_rate = float(m["bw"])
                    if m.get("gain") is not None:
                        g = m["gain"]; sdr.gain = 'auto' if g in ('auto', -1) else float(g)
                    await ws.send(json.dumps({"t": "ack", "of": "tune"}))
                elif cmd == "scan":
                    band = m.get("band")
                    centers = {"2.4": 2.437e9, "5": 5.2e9, "sub": 433.9e6}
                    f = centers.get(band)
                    if f and f <= 1.766e9:
                        sdr.center_freq = f
                    await ws.send(json.dumps({"t": "status",
                        "msg": f"scan {band} (note: V4 range 24 MHz–1.766 GHz)"}))
                elif cmd in ("sos", "lora-tx", "beacon", "bloom", "tx", "inject"):
                    # RX-only dongle: forward these to your TX/LoRa hardware here.
                    print(f"[forward] {cmd}: {m}")
                    await ws.send(json.dumps({"t": "ack", "of": cmd}))
        finally:
            clients.discard(ws)
            print(f"client gone ({len(clients)} total)")
    return handler

async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--freq", default="100e6")
    ap.add_argument("--rate", default="2.4e6")
    ap.add_argument("--gain", default="auto")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    sdr = build_sdr(args)
    print(f"ALLALONE bridge: RTL-SDR Blog V4  @ {sdr.center_freq/1e6:.3f} MHz, "
          f"{sdr.sample_rate/1e6:.2f} Msps")
    async with websockets.serve(make_handler(sdr), "0.0.0.0", args.port):
        print(f"WebSocket up on  ws://0.0.0.0:{args.port}  — enter that in the app's SOURCE page")
        await streamer(sdr)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nbye")
