# waveshare 7.5 e-Paper HAT script
 - Follow [these](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_Manual#Python) instructions 
 - make a new file/overwrite contents of `epd_7in5_V2_test.py`
 - enter creds in `conn_info`
 - enter url in `weathurl` from [here](https://openweathermap.org/api)
 - throw your weather icons in the `pic` dir
   - might need to rename the files/vars, [weather id ref](https://openweathermap.org/weather-conditions)
 - `sudo python3 examples/whatever_you_named_this.py`
 - (optional) do your cron stuff

<img src="https://github.com/user-attachments/assets/bd464a0b-7544-46be-8674-ea1a413b7a24" width="420">
 - I already fixed the text overlap
 - 800 x 480 for main background image
