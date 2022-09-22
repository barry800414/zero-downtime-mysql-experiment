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

