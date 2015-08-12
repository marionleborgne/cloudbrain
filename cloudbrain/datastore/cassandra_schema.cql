DROP KEYSPACE openbci;
CREATE KEYSPACE openbci WITH  replication = {'class': 'SimpleStrategy', 'replication_factor': 3 };
USE openbci;
CREATE TABLE eeg (user_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double, value_4 double, value_5 double, value_6 double, value_7 double,  PRIMARY KEY (user_id, timestamp)); 

DROP KEYSPACE muse;
CREATE KEYSPACE muse WITH  replication = {'class': 'SimpleStrategy', 'replication_factor': 3 };
USE muse;
CREATE TABLE eeg (user_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE horseshoe (user_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE concentration (user_id text, timestamp timestamp, value_0 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE mellow (user_id text, timestamp timestamp, value_0 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE acc (user_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE delta_absolute (user_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE theta_absolute (user_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE beta_absolute (user_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE alpha_absolute (user_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE gamma_absolute (user_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE delta_relative (user_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE theta_relative (user_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE beta_relative (user_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE alpha_relative (user_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE gamma_relative (user_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE is_good (user_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE blink (user_id text, timestamp timestamp, value_0 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE jaw_clench (user_id text, timestamp timestamp, value_0 double,  PRIMARY KEY (user_id, timestamp)); 

DROP KEYSPACE neurosky;
CREATE KEYSPACE neurosky WITH  replication = {'class': 'SimpleStrategy', 'replication_factor': 3 };
USE neurosky;
CREATE TABLE concentration (user_id text, timestamp timestamp, value_0 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE meditation (user_id text, timestamp timestamp, value_0 double,  PRIMARY KEY (user_id, timestamp)); 
CREATE TABLE signal_strength (user_id text, timestamp timestamp, value_0 double,  PRIMARY KEY (user_id, timestamp)); 

DROP KEYSPACE pulsesensor;
CREATE KEYSPACE pulsesensor WITH  replication = {'class': 'SimpleStrategy', 'replication_factor': 3 };
USE pulsesensor;
CREATE TABLE raw (user_id text, timestamp timestamp, value_0 double,  PRIMARY KEY (user_id, timestamp)); 


DROP KEYSPACE users;
CREATE KEYSPACE users WITH  replication = {'class': 'SimpleStrategy', 'replication_factor': 3 };
USE users;
CREATE TABLE consent (user_id text, timestamp timestamp, consent text, age double, gender text,  PRIMARY KEY (user_id, timestamp));
