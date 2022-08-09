

import sqlparse
import os

sql = """
BEGIN;
--
-- Add field ghostText to account
--
ALTER TABLE `qganalyzedata_account` ADD COLUMN `ghostText` varchar(512) DEFAULT 'hello world' NOT NULL;
ALTER TABLE `qganalyzedata_account` ALTER COLUMN `ghostText` DROP DEFAULT;
--
-- Add field ghostDateTime to campaign
--
ALTER TABLE `qganalyzedata_campaign` ADD COLUMN `ghostDateTime` datetime(6) DEFAULT '2022-08-04 10:49:03.119198' NOT NULL;
ALTER TABLE `qganalyzedata_campaign` ALTER COLUMN `ghostDateTime` DROP DEFAULT;
--
-- Add field ghostFK to campaign
--
ALTER TABLE `qganalyzedata_campaign` ADD COLUMN `ghostFK_id` integer DEFAULT -1 NOT NULL;
ALTER TABLE `qganalyzedata_campaign` ALTER COLUMN `ghostFK_id` DROP DEFAULT;
--
-- Add field ghostText to historicalaccount
--
ALTER TABLE `qganalyzedata_historicalaccount` ADD COLUMN `ghostText` varchar(512) DEFAULT 'hello world' NOT NULL;
ALTER TABLE `qganalyzedata_historicalaccount` ALTER COLUMN `ghostText` DROP DEFAULT;
--
-- Add field ghostDateTime to historicalcampaign
--
ALTER TABLE `qganalyzedata_historicalcampaign` ADD COLUMN `ghostDateTime` datetime(6) DEFAULT '2022-08-04 10:49:03.233711' NOT NULL;
ALTER TABLE `qganalyzedata_historicalcampaign` ALTER COLUMN `ghostDateTime` DROP DEFAULT;
--
-- Add field ghostFK to historicalcampaign
--
ALTER TABLE `qganalyzedata_historicalcampaign` ADD COLUMN `ghostFK_id` integer DEFAULT -1 NULL;
ALTER TABLE `qganalyzedata_historicalcampaign` ALTER COLUMN `ghostFK_id` DROP DEFAULT;
--
-- Alter field identifier on customer
--
ALTER TABLE `qganalyzedata_customer` MODIFY `identifier` varchar(254) NOT NULL;
CREATE INDEX `qganalyzedata_campaign_ghostFK_id_a21edfa4` ON `qganalyzedata_campaign` (`ghostFK_id`);
CREATE INDEX `qganalyzedata_historicalcampaign_ghostFK_id_4289b555` ON `qganalyzedata_historicalcampaign` (`ghostFK_id`);
COMMIT;
"""

MASTER_ENDPOINT = "leader.io"
MASTER_PORT = 3306
REPLICA_ENDPOINT = "follower.io"
REPLICA_PORT = 3306
USRE_ID="user"
PASSWORD="password"
DATABASE="demo"

def genGhostCommend(table, command):
    result = f"""
    docker run -i -t bonty/gh-ost:latest \\
        --host="{REPLICA_ENDPOINT}" \\
        --port="{MASTER_PORT}" \\
        --initially-drop-old-table \\
        --initially-drop-ghost-table \\
        --max-load=Threads_running=25 \\
        --critical-load=Threads_running=1000 \\
        --chunk-size=1000 \\
        --max-lag-millis=1500 \\
        --user="{USRE_ID}" \\
        --password="{PASSWORD}" \\
        --database="{DATABASE}" \\
        --table="{table}" \\
        --verbose \\
        --alter="{command}" \\
        --assume-rbr \\
        --allow-master-master \\
        --cut-over=default \\
        --exact-rowcount \\
        --concurrent-rowcount \\
        --default-retries=120 \\
        --panic-flag-file=/tmp/ghost.panic.flag \\
        --assume-master-host="{REPLICA_ENDPOINT}:{REPLICA_PORT}" \\
        --execute
    """
    # --postpone-cut-over-flag-file=/tmp/ghost.postpone.flag \\
    return result

sql = sqlparse.format(sql, strip_comments=True).strip()
sql = sql.replace('`', '')
statements = sqlparse.parse(sql)
for s in statements[0:2]:
    type = s.get_type()
    if type == 'ALTER':
        query = str(s)
        tokens = query.strip().split(' ')
        table = tokens[2]
        command = ' '.join(tokens[3:])

        shell_command = genGhostCommend(table, command)
        print(shell_command)
        os.system(shell_command)

