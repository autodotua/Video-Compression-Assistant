
encoder_infos = {
    "H.265": {"crf": {"max": 51, "default": 28},
              "lib": "libx265","ext":"mp4"},
    "H.264": {"crf": {"max": 51, "default": 23},
              "lib": "libx264","ext":"mp4"},
    "VP9": {"crf": {"max": 63, "default": 30},
              "lib": "libvpx-vp9","ext":"webm"},
}

presets = {
    -5: {"code": "ultrafast", "desc": "最快"},
    - 4: {"code": "superfast", "desc": "超快"},
    - 3: {"code": "veryfast", "desc": "很快"},
    - 2: {"code": "faster", "desc": "快"},
    - 1: {"code": "fast", "desc": "较快"},
    0: {"code": "medium", "desc": "平衡"},
    1: {"code": "slow", "desc": "较慢"},
    2: {"code": "slower", "desc": "慢"},
    3: {"code": "veryslow", "desc": "最慢"}
}
