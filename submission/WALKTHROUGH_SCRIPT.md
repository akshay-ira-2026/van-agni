# Van Agni walkthrough (Stage 3)

Video: submission/WALKTHROUGH_VIDEO.mp4 (3 min 37 s, 1280x720, English and Hindi narration with word-by-word captions).

Voices: Microsoft Edge neural TTS (text-to-speech), en-IN Neerja and hi-IN Swara. Music: AI-generated underscore (declared in AI_DISCLOSURE.md). Every on-screen number comes from outputs/metrics.json, docs/replay_2024-04-22.json, docs/live.json or the VIIRS (Visible Infrared Imaging Radiometer Suite) archive in data/.

Rebuild: `python3 scripts/walkthrough/render.py` (needs the voice files from script.json and ffmpeg).

## Script

- 0:00 [en] April 2024. In just one week, NASA satellites picked up more than three thousand fire detections across Uttarakhand's forests.
- 0:12 [en] Every spring, the chir pine hills burn. And every spring, forest staff find out only after the smoke rises.
- 0:21 [en] This is Van Agni. It tells them where fire is likely next week, so the patrol gets there first.
- 0:30 [en] Every morning at six, a free GitHub job pulls NASA's latest satellite fire feed and the weather, and rescores 113 forest cells across Uttarakhand, each about 27 kilometres wide. The colour is the chance of fire in the next seven days.
- 0:49 (approx.) live map clip from DEMO_RECORDING.mp4, 9 s
- 0:58 [en] Now the real test. We rewind to the 22nd of April, 2024, and ask Van Agni for its top ten patrol list, using only what was known that morning. Then we play the next seven days of satellite fires on top.
- 1:17 [en] All ten burned. Ten out of ten.
- 1:22 [en] Every cell on the list comes with an alert in English and Hindi, and the reasons behind it. 49 days without rain. Humidity at 24 percent. 44 fire points nearby this week.
- 1:39 [hi] वन अग्नि: अगले सात दिन, अति उच्च आग जोखिम। केवल सलाह: बीट स्टाफ से पुष्टि करें।
- 1:49 [en] It is advice, not an order. The beat officer always decides.
- 1:56 [en] On 2025, a year the model never saw, Van Agni scores an area under the curve of 0.914. Its daily top ten catches 38.6 percent of the cells that burn, against 20.4 percent for the usual way of watching past hotspots. That's 89 percent more fires reached, with the same ten patrols.
- 2:23 [en] What drives it? The fire radiative power and satellite detections of the past week lead, then each cell's own fire history, the season, and ninety days of rain.
- 2:36 [en] And it's green by design. Training takes under five seconds on an ordinary laptop processor. That's 0.00023 kilowatt hours, about a sixth of a gram of carbon dioxide. Scoring a thousand cells costs six hundred-thousandths of a gram. No large language model runs at all.
- 3:01 [en] The code is open. Feature building, training with year by year splits, passing tests, and one script that reproduces every number in this video.
- 3:13 [en] It deploys four ways. Free cloud, Docker, on premise, or SMS at the edge, for forest beats with no internet. Next is a pilot, from February to June 2027, in Nainital or Almora.
- 3:31 [en] Van Agni. See the fire before it starts.
