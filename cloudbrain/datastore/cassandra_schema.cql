DROP KEYSPACE sensor_data;
CREATE KEYSPACE sensor_data WITH  replication = {'class': 'SimpleStrategy', 'replication_factor': 3 };
USE sensor_data;

CREATE TABLE openbci_eeg (device_id text, timestamp timestamp, channel_0 double, channel_1 double, channel_2 double, channel_3 double, channel_4 double, channel_5 double, channel_6 double, channel_7 double,  PRIMARY KEY (device_id, timestamp)); 

CREATE TABLE muse_eeg (device_id text, timestamp timestamp, channel_0 double, channel_1 double, channel_2 double, channel_3 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE muse_horseshoe (device_id text, timestamp timestamp, channel_0 double, channel_1 double, channel_2 double, channel_3 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE muse_concentration (device_id text, timestamp timestamp, channel_0 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE muse_mellow (device_id text, timestamp timestamp, channel_0 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE muse_acc (device_id text, timestamp timestamp, channel_0 double, channel_1 double, channel_2 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE muse_delta_absolute (device_id text, timestamp timestamp, channel_0 double, channel_1 double, channel_2 double, channel_3 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE muse_theta_absolute (device_id text, timestamp timestamp, channel_0 double, channel_1 double, channel_2 double, channel_3 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE muse_beta_absolute (device_id text, timestamp timestamp, channel_0 double, channel_1 double, channel_2 double, channel_3 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE muse_alpha_absolute (device_id text, timestamp timestamp, channel_0 double, channel_1 double, channel_2 double, channel_3 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE muse_gamma_absolute (device_id text, timestamp timestamp, channel_0 double, channel_1 double, channel_2 double, channel_3 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE muse_delta_relative (device_id text, timestamp timestamp, channel_0 double, channel_1 double, channel_2 double, channel_3 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE muse_theta_relative (device_id text, timestamp timestamp, channel_0 double, channel_1 double, channel_2 double, channel_3 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE muse_beta_relative (device_id text, timestamp timestamp, channel_0 double, channel_1 double, channel_2 double, channel_3 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE muse_alpha_relative (device_id text, timestamp timestamp, channel_0 double, channel_1 double, channel_2 double, channel_3 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE muse_gamma_relative (device_id text, timestamp timestamp, channel_0 double, channel_1 double, channel_2 double, channel_3 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE muse_is_good (device_id text, timestamp timestamp, channel_0 double, channel_1 double, channel_2 double, channel_3 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE muse_blink (device_id text, timestamp timestamp, channel_0 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE muse_jaw_clench (device_id text, timestamp timestamp, channel_0 double,  PRIMARY KEY (device_id, timestamp)); 

CREATE TABLE neurosky_concentration (device_id text, timestamp timestamp, channel_0 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE neurosky_meditation (device_id text, timestamp timestamp, channel_0 double,  PRIMARY KEY (device_id, timestamp)); 
CREATE TABLE neurosky_signal_strength (device_id text, timestamp timestamp, channel_0 double,  PRIMARY KEY (device_id, timestamp)); 

CREATE TABLE pulsesensor_raw (device_id text, timestamp timestamp, channel_0 double,  PRIMARY KEY (device_id, timestamp)); 


DROP KEYSPACE users;
CREATE KEYSPACE users WITH  replication = {'class': 'SimpleStrategy', 'replication_factor': 3 };
USE users;
CREATE TABLE consent (user_id text, timestamp timestamp, consent text, age double, gender text,  PRIMARY KEY (user_id, timestamp));
