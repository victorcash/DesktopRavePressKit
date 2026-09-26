# Recording Desktop Rave

[Press-kit home](../README.md) · [Existing video downloads](../Trailer/README.md) · [Technical help](Contact.md#technical-help)

For a quick illustration, use the supplied [12-second silent MP4](https://github.com/victorcash/DesktopRavePressKit/raw/refs/heads/main/Trailer/desktop-rave-audio-reactive-12s-silent.mp4). It is 1280 × 720 at 30 fps and has no audio track.

## OBS starting setup on Windows

**These steps are a suggested setup, not a tested Desktop Rave / OBS configuration.** Record and inspect a short sample on your own machine before committing to a longer take.

1. Arrange the club against the desktop background you want in the recording. Close unrelated windows and keep private notifications out of the shot.
2. In an OBS scene, add **Display Capture** and choose the display containing the club. OBS documents this source as a capture of the entire monitor, so the desktop and any overlapping windows will be included.
3. Check the OBS preview: the club, toolbar and intended background should all be visible. Keep OBS off the captured display or minimize it before recording to avoid a repeated-screen effect.
4. Set an output resolution and frame rate appropriate to your source and machine. **1920 × 1080 at 30 fps** is a useful starting target for a landscape clip; preserve the aspect ratio and do not upscale a smaller capture as if it were native 1080p.
5. For a silent clip, mute or disable every OBS audio source/track that would enter the recording, including microphone and desktop audio. Audio can still play through Windows to drive the game; excluding it from OBS keeps it out of the recorded file. Check the exported sample to confirm it is silent.
6. Record a short sample, then play it back. Check framing, visible UI, motion and audio. OBS recommends recording to **MKV** and provides **File → Remux Recordings** to make an MP4 afterward.

Official references: [OBS Display Capture](https://obsproject.com/kb/display-capture-sources) and [OBS recording / remux guide](https://obsproject.com/kb/standard-recording-output-guide).

## Showing the audio reaction

Play audio through the Windows output device the game is listening to. For a fixed beat without external audio, use **Settings → Audio → Use synthetic audio**. Turn that option off to demonstrate reactions to real system audio again. If a clip demonstrates synthetic mode, identify it that way in its caption.

## If the capture is wrong

- **Desktop visible but club missing:** check that you selected the display containing the club and inspect your capture-source settings. If you tried Window Capture or Game Capture, try the Display Capture starting setup above.
- **OBS repeats inside the recording:** move or minimize OBS on the captured display before recording.
- **Unwanted music or microphone audio:** inspect all audio sources and recording tracks, then make and play back a new silent sample.
- **Club does not react:** verify that audio is playing through the intended Windows output device, or try synthetic mode to compare behavior.

If that does not solve it, [contact 28 Ducks](Contact.md#technical-help) with your Build ID, Windows version, OBS version, capture source and audio device. A specific setup report helps more than assuming one capture method works on every machine.

## Music and publication

Game footage can be used in monetized coverage under the [press-kit license](../LICENSE). External playlist links do not grant permission to publish the music they play. Use audio your outlet is entitled to publish or provide a silent clip. See the [reviewer guide](Reviewer%20Guide.md#recording-and-music) for the existing music guidance.
