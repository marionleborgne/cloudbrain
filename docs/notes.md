## Cloudbrain data structure when publishing and subscribing:
```
[
  {timestmap, channel_0, ..., channel_N},
    ...
  {timestmap, channel_0, ..., channel_N}
]
```

## Cloudbrain style guide
* 4 space indents
* 100 characters per line max
* package names should all be lower case
* limit number of classes to 1 per package if possible
* stick to underscore for module names, repo names, config files, etc. Try to avoid hyphens. Camel case is for class names.

## TODO HTB
[ ] Deploy new notch filter
[x] FrequencyBandTransformer module
[ ] Discuss FFT vs STFT w/ manual chunking with pierre (fft_test.py VS stft_test.py)
[ ] better subsampling in RT server
[x] publish / subscribe tutorials
[x] bring back the timestamps in FrequencyBandTransformer module
[ ] band pass that makes sure to avoid the 60Hz freq
[ ] StdoutSink
[ ] PyPlotSink


## TODO later
[ ] Update or rename PipePublisher. Right now it's just a stdout publisher and it's unlikely 
that we'll go down the named pipe route.
[ ] websocket publisher and subscriber
[ ] rest source (for label input)
[ ] lsl publisher and subscribers
[ ] 2 filter modules: bandstop and highpass
[ ] Rename FrequencyBandModule to FFTModule?
[ ] Make a sink module that is plotting the chart
[ ] Add the simple threshold classifier


