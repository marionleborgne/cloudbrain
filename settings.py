__author__ = 'marion'

#log directory
LOG_DIR = '/var/log/supervisor'

# IP of brainserver
EXPLO_BRAINSERVER_IP = '208.66.31.59'

# TagID => MuseID
TAGS = {
    "2b08d4ec": 5001,
    "dbbad4ec": 5002,
    "5ba8d4ec": 5003,
    "bb88d4ec": 5004,
    "2b14d4ec": 5005,
    "5b0fd4ec": 5006,
    "ab0ed6ec": 5007,
    "5b79d5ec": 5008,
    "19e8f635": 5009,
    "abe1d3ec": 5010,
    "ebdfd3ec": 5011,
    "9b68d5ec": 5012,
    "4b68d3ec": 5013,
    "5bb1d5ec": 5014,
    "5b0cd4ec": 5015,
    "6b69d5ec": 5016,
    "5b67d5ec": 5017,
    "dbaad4ec": 5018,
    "4b07d4ec": 5019,
    "ebdbd3ec": 5020,
    "4b68d5ec": 5021,
    "ce9686e5": 5008,
    "19e8f635": 5009,
    "abe1d3ec": 5010,
    "3153f935": 5011,
    "9b68d5ec": 5012,
    "82ecf735": 5013,
    "00b2f735": 5014,
    "7385368c": 5015,
    "ce9686e5": 5008,
    "5b64d6ec": 5009,
    "a52df735": 5010,
    "3153f935": 5011,
    "9b68d5ec": 5012,
    "82ecf735": 5013,
    "00b2f735": 5014,
    "7385368c": 5015
}

# Muse Port numbers

MUSE_PORTS = [
    5001,
    5002,
    5003,
    5004,
    5005,
    5006,
    5007,
    5008,
    5009,
    5010,
    5011,
    5012,
    5013,
    5014,
    5015,
    5016,
    5017,
    5018,
    5019,
    7777]

# CoreID => Booth Name
CORES = {
    "53ff6e065067544819260487": "muse-manager",
    "53ff68066667574815362067": "booth-1",
    "54ff6d066667515116121567": "booth-2",
    "54ff68066667515151331467": "booth-3",
    "54ff70066667515149111567": "booth-4",
    "53ff70066667574808432167": "booth-5",
    "53ff6d066667574823302067": "booth-6",
    "50ff6d065077494946390787": "booth-7",
    "54ff6c066667515150321467": "booth-8",
    "53ff6d066667574834382167": "booth-9",
    "53ff76066667574859372167": "booth-10",
    "53ff6a066667574841132167": "booth-11",
    "53ff72066667574858362167": "booth-12"
}

#Booth Name => {"ip" => IP Address}
BOOTHS = {
    "muse-manager": {"ip": "10.0.0.2"},
    "booth-1": {"ip": "10.0.0.201"},
    "booth-2": {"ip": "10.0.0.202"},
    "booth-3": {"ip": "10.0.0.203"},
    "booth-4": {"ip": "10.0.0.204"},
    "booth-5": {"ip": "10.0.0.205"},
    "booth-6": {"ip": "10.0.0.206"},
    "booth-7": {"ip": "10.0.0.207"},
    "booth-8": {"ip": "10.0.0.208"},
    "booth-9": {"ip": "10.0.0.209"},
    "booth-10": {"ip": "10.0.0.210"},
    "booth-11": {"ip": "10.0.0.211"},
    "booth-12": {"ip": "10.0.0.212"}
}

# cassandra spacebrew subscriber name
SPACEBREW_CASSANDRA_NAME = 'cassandra'
SPACEBREW_DATA_VIZ_NAME = 'data-visualization'
SPACEBREW_CASSANDRA_IP = '104.236.15.197'
SPACEBREW_BRAINSERVER_IP = '127.0.0.1'

# IP address of cassandra cluster
CASSANDRA_IP = '127.0.0.1'

# Metrics for Cassandra
CASSANDRA_METRICS = {
    "/muse/eeg": 4,
    #"/muse/eeg/quantization": 4,
    #"/muse/eeg/dropped_samples": 1,
    #"/muse/acc": 3,
    #"/muse/acc/dropped_samples": 1,
    "/muse/batt": 4,
    #"/muse/drlref": 2,
    #"/muse/elements/low_freqs_absolute": 4,
    "/muse/elements/delta_absolute": 4,
    "/muse/elements/theta_absolute": 4,
    "/muse/elements/alpha_absolute": 4,
    "/muse/elements/beta_absolute": 4,
    "/muse/elements/gamma_absolute": 4,
    #"/muse/elements/delta_relative": 4,
    #"/muse/elements/theta_relative": 4,
    #"/muse/elements/alpha_relative": 4,
    #"/muse/elements/beta_relative": 4,
    #"/muse/elements/gamma_relative": 4,
    #"/muse/elements/delta_session_score": 4,
    #"/muse/elements/theta_session_score": 4,
    #"/muse/elements/alpha_session_score": 4,
    #"/muse/elements/beta_session_score": 4,
    #"/muse/elements/gamma_session_score": 4,
    #"/muse/elements/touching_forehead": 1,
    "/muse/elements/horseshoe": 4,
    "/muse/elements/is_good": 4,
    "/muse/elements/blink": 1,
    "/muse/elements/jaw_clench": 1,
    "/muse/elements/experimental/concentration": 1,
    "/muse/elements/experimental/mellow": 1
}



# Metrics for data viz
DATA_VIZ_METRICS = { "/muse/elements/delta_absolute": 4,
    "/muse/elements/theta_absolute": 4,
    "/muse/elements/alpha_absolute": 4,
    "/muse/elements/beta_absolute": 4,
    "/muse/elements/gamma_absolute": 4}