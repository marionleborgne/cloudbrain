<img src="https://raw.githubusercontent.com/cloudbrain/cloudbrain/master/docs/images/cb-logo-low-res.png" alt="Banner" style="width: 40px;"/>

# Status
[![Build Status](https://travis-ci.org/cloudbrain/cloudbrain.svg?branch=master)](https://travis-ci.org/cloudbrain/cloudbrain)

# Features
CloudBrain is a platform for real-time sensor data analysis and visualization.
- **Stream sensor data** in a unified format.
- **Store sensor data** in a central database.
- **Analyze sensor data** to find patterns.
- **Visualize sensor data** and patterns in real-time.

![features](https://raw.githubusercontent.com/cloudbrain/cloudbrain/master/docs/images/features.png)

# Using CloudBrain

## Setup
* Run: `pip install . --user`
* If you plan to *edit* the code, make sure to use the `-e` switch: `pip 
install -e . --user`

## Optional
Optional CloudBrain modules can be installed:
* Muse source module: `pip install .[muse] --user` (Python `3.*` only)

## Run the tests
```
python setup.py test

```

## Examples
See `README.md` in `cloudbrain/examples` for more information about how to use
 and chain CloudBrain modules.

## More docs
For more details on to setup and use CloudBrain, refer to the [wiki](https://github.com/cloudbrain/cloudbrain/wiki).

### License
[![License: AGPL-3](https://img.shields.io/badge/license-AGPL--3-blue.svg)](https://raw.githubusercontent.com/cloudbrain/cloudbrain/master/LICENSE.txt)
