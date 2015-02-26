DROP KEYSPACE cloudbrain;
CREATE KEYSPACE cloudbrain WITH  replication = {'class': 'SimpleStrategy', 'replication_factor': 3 };
USE cloudbrain;
CREATE TABLE horseshoe (muse_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (muse_id, timestamp));
CREATE TABLE delta_absolute (muse_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (muse_id, timestamp));
CREATE TABLE mellow (muse_id text, timestamp timestamp, value_0 double,  PRIMARY KEY (muse_id, timestamp));
CREATE TABLE is_good (muse_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (muse_id, timestamp));
CREATE TABLE batt (muse_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (muse_id, timestamp));
CREATE TABLE gamma_absolute (muse_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (muse_id, timestamp));
CREATE TABLE jaw_clench (muse_id text, timestamp timestamp, value_0 double,  PRIMARY KEY (muse_id, timestamp));
CREATE TABLE blink (muse_id text, timestamp timestamp, value_0 double,  PRIMARY KEY (muse_id, timestamp));
CREATE TABLE theta_absolute (muse_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (muse_id, timestamp));
CREATE TABLE beta_absolute (muse_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (muse_id, timestamp));
CREATE TABLE alpha_absolute (muse_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (muse_id, timestamp));
CREATE TABLE concentration (muse_id text, timestamp timestamp, value_0 double,  PRIMARY KEY (muse_id, timestamp));
CREATE TABLE eeg (muse_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (muse_id, timestamp));


CREATE KEYSPACE users WITH  replication = {'class': 'SimpleStrategy', 'replication_factor': 3 };
USE users;
CREATE TABLE consent (muse_id text, timestamp timestamp, headset_number double, consent double, value_2 double, value_3 double,  PRIMARY KEY (muse_id, timestamp));
CREATE TABLE delta_absolute (muse_id text, timestamp timestamp, value_0 double, value_1 double, value_2 double, value_3 double,  PRIMARY KEY (muse_id, timestamp));
