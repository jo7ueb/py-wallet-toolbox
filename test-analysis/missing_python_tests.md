# Missing Python Test Cases

This table shows TypeScript test cases that don't have corresponding Python tests.

| Test Name | TS File Path | Proposed Python Test File Path |
|-----------|--------------|--------------------------------|
| should block usage of an admin-only protocol name if not called by admin | src/__tests/WalletPermissionsManager.initialization.test.ts | permissions/test_wallet_permissions_manager_initialization.py |
| should skip all permission checks if all relevant config flags are false (except admin-only baskets, etc.) | src/__tests/WalletPermissionsManager.initialization.test.ts | permissions/test_wallet_permissions_manager_initialization.py |
| 0 | src/monitor/__test/MonitorDaemon.man.test.ts | monitor/test_monitor.py |
| 11 post to TAAL for timeout | src/services/__tests/ARC.timeout.man.test.ts | universal/test_abortaction.py |
| 12 post to GorillaPool for timeout | src/services/__tests/ARC.timeout.man.test.ts | universal/test_abortaction.py |
| 2 postBeef | src/services/__tests/ArcGorillaPool.man.test.ts | storage/entities/test_tx_label_map.py |
| 0  | src/services/__tests/arcServices.test.ts | services/test_arc_services.py |
| 1  | src/services/__tests/bitrails.test.ts | utils/satoshi/test_bitrails.py |
| 0 | src/services/__tests/getMerklePath.test.ts | services/test_get_merkle_path.py |
| 0 | src/services/__tests/getRawTx.test.ts | services/test_get_raw_tx.py |
| 0_ | src/services/__tests/verifyBeef.test.ts | services/test_verify_beef.py |
| 1_ | src/services/__tests/verifyBeef.test.ts | services/test_verify_beef.py |
| 0 | src/services/chaintracker/chaintracks/Storage/__tests/ChaintracksStorageIdb.test.ts | chaintracks/test_chaintracks.py |
| 0 | src/services/chaintracker/chaintracks/Storage/__tests/ChaintracksStorageKnex.test.ts | chaintracks/test_chaintracks.py |
| 0 | src/services/chaintracker/chaintracks/__tests/createIdbChaintracks.test.ts | chaintracks/test_chaintracks.py |
| 1 headers from heights maxRetained 2 | src/services/chaintracker/chaintracks/util/__tests/BulkFileDataManager.test.ts | integration/test_bulk_file_data_manager.py |
| 1a headers from heights maxRetained 2 | src/services/chaintracker/chaintracks/util/__tests/BulkFileDataManager.test.ts | integration/test_bulk_file_data_manager.py |
| 2 ReValidate | src/services/chaintracker/chaintracks/util/__tests/BulkFileDataManager.test.ts | integration/test_bulk_file_data_manager.py |
| 3 exportHeadersToFs | src/services/chaintracker/chaintracks/util/__tests/BulkFileDataManager.test.ts | integration/test_bulk_file_data_manager.py |
| 4 add two incremental chunks overwrite by CDN | src/services/chaintracker/chaintracks/util/__tests/BulkFileDataManager.test.ts | integration/test_bulk_file_data_manager.py |
| 4a add two incremental chunks overwrite by CDN | src/services/chaintracker/chaintracks/util/__tests/BulkFileDataManager.test.ts | integration/test_bulk_file_data_manager.py |
| 5 add CDN incremental CDN incremental | src/services/chaintracker/chaintracks/util/__tests/BulkFileDataManager.test.ts | integration/test_bulk_file_data_manager.py |
| 5a add CDN incremental CDN incremental | src/services/chaintracker/chaintracks/util/__tests/BulkFileDataManager.test.ts | integration/test_bulk_file_data_manager.py |
| 0_ | src/services/chaintracker/chaintracks/util/__tests/SingleWriterMultiReaderLock.test.ts | integration/test_single_writer_multi_reader_lock.py |
| 0 | src/services/providers/__tests/exchangeRates.test.ts | services/test_exchange_rates.py |
| 0 | src/storage/__test/StorageIdb.test.ts | universal/test_signature_min.py |
| 1_runAsReader runAsWriter runAsSync interlock correctly | src/storage/__test/WalletStorageManager.test.ts | permissions/test_wallet_permissions_manager_flows.py |
| 1a_runAsReader runAsWriter runAsSync interlock correctly with low durations | src/storage/__test/WalletStorageManager.test.ts | permissions/test_wallet_permissions_manager_flows.py |
| 0 adminStats StorageKnex | src/storage/__test/adminStats.man.test.ts | services/test_transaction_status_min.py |
| 1 adminStats StorageServer via RPC | src/storage/__test/adminStats.man.test.ts | services/test_transaction_status_min.py |
| 0 ProtoStorage.getBeefForTxid | src/storage/__test/getBeefForTransaction.test.ts | storage/entities/test_transaction.py |
| 8 paramsText d5 d6 d7 d8 d9 d10 d11 d12 d13 d14 | src/storage/methods/__test/GenerateChange/generateChangeSdk.test.ts | utils/satoshi/test_generate_change_sdk.py |
| 0_inserts_new_sync_state | src/storage/schema/entities/__tests/SyncStateTests.test.ts | wallet/test_sync.py |
| 10_mergeNew_does_nothing | src/storage/schema/entities/__tests/SyncStateTests.test.ts | wallet/test_sync.py |
| 1_updates_existing_sync_state | src/storage/schema/entities/__tests/SyncStateTests.test.ts | wallet/test_sync.py |
| 2_merges_id_maps_correctly | src/storage/schema/entities/__tests/SyncStateTests.test.ts | wallet/test_sync.py |
| 3_throws_error_on_conflicting_mappings | src/storage/schema/entities/__tests/SyncStateTests.test.ts | wallet/test_sync.py |
| 4_processes_sync_chunk_correctly | src/storage/schema/entities/__tests/SyncStateTests.test.ts | wallet/test_sync.py |
| 6_equals_method_always_returns_false | src/storage/schema/entities/__tests/SyncStateTests.test.ts | wallet/test_sync.py |
| 8_derived_properties | src/storage/schema/entities/__tests/SyncStateTests.test.ts | wallet/test_sync.py |
| 9_id_entityName_entityTable | src/storage/schema/entities/__tests/SyncStateTests.test.ts | wallet/test_sync.py |
| can delete user | src/wab-client/__tests/WABClient.man.test.ts | chaintracks/test_client_api.py |
| should do Twilio phone flow | src/wab-client/__tests/WABClient.man.test.ts | chaintracks/test_client_api.py |
| should get server info | src/wab-client/__tests/WABClient.man.test.ts | chaintracks/test_client_api.py |
| should list linked methods | src/wab-client/__tests/WABClient.man.test.ts | chaintracks/test_client_api.py |
| should request faucet | src/wab-client/__tests/WABClient.man.test.ts | chaintracks/test_client_api.py |
| 1 backup to client | test/Wallet/StorageClient/storageClient.man.test.ts | chaintracks/test_service_client.py |
| 2 create storage client backup for test wallet | test/Wallet/StorageClient/storageClient.man.test.ts | chaintracks/test_service_client.py |
| 3 create storage client backup for main wallet | test/Wallet/StorageClient/storageClient.man.test.ts | chaintracks/test_service_client.py |
| 1_abort reference 49f878d8405589 | test/Wallet/action/abortAction.test.ts | wallet/test_abort_action.py |
| . | test/Wallet/action/createAction.test.ts | storage/entities/test_create_action.py |
| 3_Transaction with multiple outputs() | test/Wallet/action/createAction.test.ts | storage/entities/test_create_action.py |
| 4_Transaction with large number of outputs(50) and randomized | test/Wallet/action/createAction.test.ts | storage/entities/test_create_action.py |
|   | test/Wallet/action/createAction2.test.ts | storage/entities/test_create_action.py |
| 10_no-send transaction with malformed args (invalid destination) | test/Wallet/action/createAction2.test.ts | storage/entities/test_create_action.py |
| 11_transaction with OP_RETURN | test/Wallet/action/createAction2.test.ts | storage/entities/test_create_action.py |
| 12_high fee transaction | test/Wallet/action/createAction2.test.ts | storage/entities/test_create_action.py |
| 13_zero fee transaction | test/Wallet/action/createAction2.test.ts | storage/entities/test_create_action.py |
| 14_dust transaction | test/Wallet/action/createAction2.test.ts | storage/entities/test_create_action.py |
| 1_transaction with single output checked using toLogString | test/Wallet/action/createAction2.test.ts | storage/entities/test_create_action.py |
| 2_transaction with multiple outputs checked using toLogString | test/Wallet/action/createAction2.test.ts | storage/entities/test_create_action.py |
| 3_transaction with explicit change check also uses toLogString on the spend | test/Wallet/action/createAction2.test.ts | storage/entities/test_create_action.py |
| 4_transaction with custom options knownTxids and returnTXIDOnly false uses toLogString | test/Wallet/action/createAction2.test.ts | storage/entities/test_create_action.py |
| 5_transaction with custom options knownTxids and returnTXIDOnly true | test/Wallet/action/createAction2.test.ts | storage/entities/test_create_action.py |
| 6_transaction with custom options knownTxids check returned BeefParty txids | test/Wallet/action/createAction2.test.ts | storage/entities/test_create_action.py |
| 7_transaction with custom options knownTxids check returned BeefParty txids with additional spend | test/Wallet/action/createAction2.test.ts | storage/entities/test_create_action.py |
| 8_no-send transaction with zero satoshis output | test/Wallet/action/createAction2.test.ts | storage/entities/test_create_action.py |
| 9_no-send transaction without auth (should fail) | test/Wallet/action/createAction2.test.ts | storage/entities/test_create_action.py |
| . | test/Wallet/action/createActionToGenerateBeefs.man.test.ts | services/test_transaction_status_min.py |
| 1_send 2 txs in a beef | test/Wallet/action/createActionToGenerateBeefs.man.test.ts | services/test_transaction_status_min.py |
| 2_send 4 txs in a single beef  | test/Wallet/action/createActionToGenerateBeefs.man.test.ts | services/test_transaction_status_min.py |
| 3_test tranaction log | test/Wallet/action/createActionToGenerateBeefs.man.test.ts | services/test_transaction_status_min.py |
| 4_abort set of nosend transactions | test/Wallet/action/createActionToGenerateBeefs.man.test.ts | services/test_transaction_status_min.py |
| 5_abort a set of unsigned transactions | test/Wallet/action/createActionToGenerateBeefs.man.test.ts | services/test_transaction_status_min.py |
| 6_abort a set of unprocessed transactions | test/Wallet/action/createActionToGenerateBeefs.man.test.ts | services/test_transaction_status_min.py |
| 7_abort all transactions | test/Wallet/action/createActionToGenerateBeefs.man.test.ts | services/test_transaction_status_min.py |
| 2_default real basket insertion | test/Wallet/action/internalizeAction.a.test.ts | wallet/test_internalize_action.py |
| 1_internalize custom output in receiving wallet with checks | test/Wallet/action/internalizeAction.test.ts | wallet/test_internalize_action.py |
| 2_internalize 2 custom outputs in receiving wallet with checks | test/Wallet/action/internalizeAction.test.ts | wallet/test_internalize_action.py |
| 3_internalize wallet payment in receiving wallet with checks | test/Wallet/action/internalizeAction.test.ts | wallet/test_internalize_action.py |
| 4_internalize 2 wallet payments in receiving wallet with checks | test/Wallet/action/internalizeAction.test.ts | wallet/test_internalize_action.py |
| 5_internalize 2 wallet payments and 2 basket insertions in receiving wallet with checks | test/Wallet/action/internalizeAction.test.ts | wallet/test_internalize_action.py |
| 1_default | test/Wallet/action/relinquishOutput.test.ts | wallet/test_relinquish_output.py |
| if returned certificate count is bigger than limit, still only returns limit items but sets total using countCertificates | test/Wallet/certificate/listCertificates.test.ts | wallet/test_list_certificates.py |
| should call countCertificates when the returned certificates length is equal to limit | test/Wallet/certificate/listCertificates.test.ts | wallet/test_list_certificates.py |
| should handle scenario userId is undefined | test/Wallet/certificate/listCertificates.test.ts | wallet/test_list_certificates.py |
| should handle transaction failure by throwing an error | test/Wallet/certificate/listCertificates.test.ts | wallet/test_list_certificates.py |
| should return an empty result when no certificates are found | test/Wallet/certificate/listCertificates.test.ts | wallet/test_list_certificates.py |
| should return exactly the number of certificates if they are fewer than the limit | test/Wallet/certificate/listCertificates.test.ts | wallet/test_list_certificates.py |
| 0 | test/Wallet/construct/Wallet.constructor.test.ts | unit/test_wallet_constructor.py |
| 1 valid block height | test/Wallet/get/getHeaderForHeight.test.ts | universal/test_getheaderforheight.py |
| 2 unexpected service errors | test/Wallet/get/getHeaderForHeight.test.ts | universal/test_getheaderforheight.py |
| 3 valid block height always returns a header | test/Wallet/get/getHeaderForHeight.test.ts | universal/test_getheaderforheight.py |
| 0 valid height | test/Wallet/get/getHeight.test.ts | universal/test_getheight.py |
| 1 handles errors from services gracefully | test/Wallet/get/getHeight.test.ts | universal/test_getheight.py |
| 1 should add new known txids | test/Wallet/get/getKnownTxids.test.ts | unit/test_wallet_getknowntxids.py |
| 3 should return sorted txids | test/Wallet/get/getKnownTxids.test.ts | unit/test_wallet_getknowntxids.py |
| should return the correct network | test/Wallet/get/getNetwork.test.ts | universal/test_getnetwork.py |
| 10_includeInputs and unlock | test/Wallet/list/listActions.test.ts | wallet/test_list_actions.py |
| 11_includeInputs and lock | test/Wallet/list/listActions.test.ts | wallet/test_list_actions.py |
| 3_label babbage_protocol_perm | test/Wallet/list/listActions.test.ts | wallet/test_list_actions.py |
| 4_label babbage_protocol_perm | test/Wallet/list/listActions.test.ts | wallet/test_list_actions.py |
| 5_label babbage_protocol_perm or babbage_basket_access | test/Wallet/list/listActions.test.ts | wallet/test_list_actions.py |
| 6_label babbage_protocol_perm and babbage_basket_access | test/Wallet/list/listActions.test.ts | wallet/test_list_actions.py |
| 7_includeOutputs | test/Wallet/list/listActions.test.ts | wallet/test_list_actions.py |
| 8_includeOutputs and script | test/Wallet/list/listActions.test.ts | wallet/test_list_actions.py |
| 9_includeInputs | test/Wallet/list/listActions.test.ts | wallet/test_list_actions.py |
| 100_no labels (default) matched default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 101_label 1 matched default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 102_label 2 matched default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 103_no label matched default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 104_both labels matched default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 105_first label pair matches mode all | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 106_second label pair matches mode all | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 12_no labels default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 13_no labels any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 14_no labels all | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 15_empty label default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 16_label is space character default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 17_label does not exist default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 18_label min 1 character default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 19_label max 300 spaces default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 20_label max 300 normal characters default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 21_label min 1 emoji default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 22_label max length 75 emojis default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 23_label exceeding max length 76 emojis default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 24_normal label default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 25_normal label any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 26_normal label all | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 27_label mixed case default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 28_label special characters default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 29_label leading and trailing whitespace default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 30_label numeric default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 31_label alphanumeric default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 32_label contains default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 33_label different case lower any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 34_label different case upper any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 35_label with whitespace default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 36_label different case lower all | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 37_label different case upper all | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 38_label duplicated default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 39_label requested default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 40_label not requested default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 41_label partial match default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 42_label only one match default any | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 57_limit 0 | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 58_limit 10001 | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 62_offset is invalid | test/Wallet/list/listActions2.test.ts | wallet/test_list_actions.py |
| 1 certifier | test/Wallet/list/listCertificates.test.ts | wallet/test_list_certificates.py |
| 2 types | test/Wallet/list/listCertificates.test.ts | wallet/test_list_certificates.py |
| 10_tags for babbage-token-access any and limit | test/Wallet/list/listOutputs.test.ts | wallet/test_list_outputs.py |
| 11_tags babbage-protocol-permission any default limit | test/Wallet/list/listOutputs.test.ts | wallet/test_list_outputs.py |
| 12_tags babbage-token-access all | test/Wallet/list/listOutputs.test.ts | wallet/test_list_outputs.py |
| 13 offsets | test/Wallet/list/listOutputs.test.ts | wallet/test_list_outputs.py |
| 14 issue 50 | test/Wallet/list/listOutputs.test.ts | wallet/test_list_outputs.py |
| 2a default | test/Wallet/list/listOutputs.test.ts | wallet/test_list_outputs.py |
| 2b default with originators | test/Wallet/list/listOutputs.test.ts | wallet/test_list_outputs.py |
| 3_include basket tags labels customInstructions | test/Wallet/list/listOutputs.test.ts | wallet/test_list_outputs.py |
| 3a_include customInstructions when valid | test/Wallet/list/listOutputs.test.ts | wallet/test_list_outputs.py |
| 4_include locking | test/Wallet/list/listOutputs.test.ts | wallet/test_list_outputs.py |
| 5_basket | test/Wallet/list/listOutputs.test.ts | wallet/test_list_outputs.py |
| 6_non-existent basket | test/Wallet/list/listOutputs.test.ts | wallet/test_list_outputs.py |
| 7_tags | test/Wallet/list/listOutputs.test.ts | wallet/test_list_outputs.py |
| 8_BEEF | test/Wallet/list/listOutputs.test.ts | wallet/test_list_outputs.py |
| 9_labels for babbage_protocol_perm | test/Wallet/list/listOutputs.test.ts | wallet/test_list_outputs.py |
| 1 set change outputs spendable false if not valid utxos | test/Wallet/live/walletLive.man.test.ts | wallet/test_wallet_create_action.py |
| 2 review available change | test/Wallet/live/walletLive.man.test.ts | wallet/test_wallet_create_action.py |
| 5 pull out txid from BEEF | test/Wallet/live/walletLive.man.test.ts | wallet/test_wallet_create_action.py |
| 5z send a wallet payment from myCtx to second wallet | test/Wallet/live/walletLive.man.test.ts | wallet/test_wallet_create_action.py |
| 6 send a wallet payment from myCtx to second wallet | test/Wallet/live/walletLive.man.test.ts | wallet/test_wallet_create_action.py |
| 6a help setup my own wallet | test/Wallet/live/walletLive.man.test.ts | wallet/test_wallet_create_action.py |
| 6b run liveWallet Monitor once | test/Wallet/live/walletLive.man.test.ts | wallet/test_wallet_create_action.py |
| 6c send a wallet payment from live to your own wallet | test/Wallet/live/walletLive.man.test.ts | wallet/test_wallet_create_action.py |
| 6d make atomicBEEF for known txid | test/Wallet/live/walletLive.man.test.ts | wallet/test_wallet_create_action.py |
| 6e make atomicBEEF for txid from staging-dojo | test/Wallet/live/walletLive.man.test.ts | wallet/test_wallet_create_action.py |
| 7 test two client wallets | test/Wallet/live/walletLive.man.test.ts | wallet/test_wallet_create_action.py |
| 0 monitor runOnce | test/Wallet/local/localWallet.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 0a monitor runOnce call history | test/Wallet/local/localWallet.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 2 create 1 sat delayed | test/Wallet/local/localWallet.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 2a create 1 sat immediate | test/Wallet/local/localWallet.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 2b create 2 nosend and sendWith | test/Wallet/local/localWallet.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 3 return active to cloud client | test/Wallet/local/localWallet.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 5 review synchunk | test/Wallet/local/localWallet.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 6 backup | test/Wallet/local/localWallet.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 0 monitor runOnce | test/Wallet/local/localWallet2.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 0a abort nosend | test/Wallet/local/localWallet2.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 1 recover 1 sat outputs | test/Wallet/local/localWallet2.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 2 create 1 sat delayed | test/Wallet/local/localWallet2.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 2a create 1 sat immediate | test/Wallet/local/localWallet2.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 2c burn 1 sat output | test/Wallet/local/localWallet2.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 2d doubleSpend old change | test/Wallet/local/localWallet2.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 4 review change utxos | test/Wallet/local/localWallet2.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 5 review and release all production invalid change utxos | test/Wallet/local/localWallet2.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 6 review and unfail false doubleSpends | test/Wallet/local/localWallet2.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 7 review and unfail false invalids | test/Wallet/local/localWallet2.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 8 Beef verifier | test/Wallet/local/localWallet2.man.test.ts | integration/test_cwi_style_wallet_manager.py |
| 0 signature validity | test/Wallet/signAction/mountaintop.man.test.ts | utils/satoshi/test_contains_utxo.py |
| 0 wallet balance specOp | test/Wallet/specOps/specOps.man.test.ts | services/test_whats_on_chain.py |
| 0a wallet balance method | test/Wallet/specOps/specOps.man.test.ts | services/test_whats_on_chain.py |
| 0b wallet balanceAndUtxos method | test/Wallet/specOps/specOps.man.test.ts | services/test_whats_on_chain.py |
| 1 wallet invalid change outputs specOp | test/Wallet/specOps/specOps.man.test.ts | services/test_whats_on_chain.py |
| 1a wallet reviewSpendableOutputs method | test/Wallet/specOps/specOps.man.test.ts | services/test_whats_on_chain.py |
| 2 update default basket params specOp | test/Wallet/specOps/specOps.man.test.ts | services/test_whats_on_chain.py |
| 2a update default basket params specOp | test/Wallet/specOps/specOps.man.test.ts | services/test_whats_on_chain.py |
| 3 wallet listNoSendActions method | test/Wallet/specOps/specOps.man.test.ts | services/test_whats_on_chain.py |
| 4 wallet listFailedActions method | test/Wallet/specOps/specOps.man.test.ts | services/test_whats_on_chain.py |
| 5 Wallet specOpThrowReviewActions | test/Wallet/specOps/specOps.man.test.ts | services/test_whats_on_chain.py |
| 6 WalletClient specOpThrowReviewActions | test/Wallet/specOps/specOps.man.test.ts | services/test_whats_on_chain.py |
| 0 review utxos by identity key | test/Wallet/support/janitor.man.test.ts | monitor/test_monitor.py |
| 0 review and release all production invalid change utxos | test/Wallet/support/operations.man.test.ts | universal/test_abortaction.py |
| 1 review and unfail false doubleSpends | test/Wallet/support/operations.man.test.ts | universal/test_abortaction.py |
| 13 review use of outputs in all following transactions | test/Wallet/support/operations.man.test.ts | universal/test_abortaction.py |
| 14 review inputs of tx utxo status | test/Wallet/support/operations.man.test.ts | universal/test_abortaction.py |
| 2 review and unfail false invalids | test/Wallet/support/operations.man.test.ts | universal/test_abortaction.py |
| 1 review reqs history and final outcome | test/Wallet/support/reqErrorReview.2025.05.06.man.test.ts | - |
| 2 review deunmined reqs | test/Wallet/support/reqErrorReview.2025.05.06.man.test.ts | - |
| 0 syncToWriter initial-no changes-1 change | test/Wallet/sync/Wallet.sync.test.ts | unit/test_wallet_getversion.py |
| 0 sync staging dojo to local MySQL | test/Wallet/sync/Wallet.updateWalletLegacyTestData.man.test.ts | wallet/test_wallet_create_action.py |
| 8b run monitor mainnet | test/Wallet/sync/Wallet.updateWalletLegacyTestData.man.test.ts | wallet/test_wallet_create_action.py |
| 0 cycle active over three new sqlite wallets | test/Wallet/sync/setActive.test.ts | wallet/test_list_actions.py |
| 0 unencrypted Wallet | test/WalletClient/LocalKVStore.man.test.ts | integration/test_local_kv_store.py |
| 0a unencrypted WalletClient | test/WalletClient/LocalKVStore.man.test.ts | integration/test_local_kv_store.py |
| 1 unencrypted Wallet | test/WalletClient/LocalKVStore.man.test.ts | integration/test_local_kv_store.py |
| 1a unencrypted WalletClient | test/WalletClient/LocalKVStore.man.test.ts | integration/test_local_kv_store.py |
| 0 WERR_REVIEW_ACTIONS | test/WalletClient/WERR.man.test.ts | universal/test_encrypt_min.py |
| 4 promise test | test/bsv-ts-sdk/LocalKVStore.test.ts | integration/test_local_kv_store.py |
| 0 | test/examples/backup.man.test.ts | universal/test_hmac_min.py |
| 1 backup MY_TEST_IDENTITY | test/examples/backup.man.test.ts | universal/test_hmac_min.py |
| 2 backup MY_TEST_IDENTITY2 | test/examples/backup.man.test.ts | universal/test_hmac_min.py |
| 0 pushdrop | test/examples/pushdrop.test.ts | utils/satoshi/test_pushdrop.py |
| 0 getUtxoStatus | test/services/Services.test.ts | services/test_services.py |
| 0a getUtxoStatus hashLE | test/services/Services.test.ts | services/test_services.py |
| 0b getUtxoStatus hashBE | test/services/Services.test.ts | services/test_services.py |
| 0c getUtxoStatus hashOutputScript method | test/services/Services.test.ts | services/test_services.py |
| 0d getUtxoStatus outpoint | test/services/Services.test.ts | services/test_services.py |
| 0e getUtxoStatus invalid outpoint | test/services/Services.test.ts | services/test_services.py |
| 2 getFiatExchangeRate | test/services/Services.test.ts | services/test_services.py |
| 3 getChainTracker | test/services/Services.test.ts | services/test_services.py |
| 6 getScriptHashHistory | test/services/Services.test.ts | services/test_services.py |
| 0 migragte down | test/storage/KnexMigrations.test.ts | universal/test_signaction.py |
| 1 migragte to latest | test/storage/KnexMigrations.test.ts | universal/test_signaction.py |
| 2 getSettings | test/storage/KnexMigrations.test.ts | universal/test_signaction.py |
| 0 | test/storage/StorageMySQLDojoReader.man.test.ts | integration/test_single_writer_multi_reader_lock.py |
| 0 basket with no outputs | test/storage/idb/allocateChange.test.ts | utils/satoshi/test_generate_change_sdk.py |
| 1 exactSatoshis | test/storage/idb/allocateChange.test.ts | utils/satoshi/test_generate_change_sdk.py |
| 2 targetSatoshis exact | test/storage/idb/allocateChange.test.ts | utils/satoshi/test_generate_change_sdk.py |
| 2a targetSatoshis exact unproven | test/storage/idb/allocateChange.test.ts | utils/satoshi/test_generate_change_sdk.py |
| 2b targetSatoshis exact sending | test/storage/idb/allocateChange.test.ts | utils/satoshi/test_generate_change_sdk.py |
| 3 targetSatoshis high | test/storage/idb/allocateChange.test.ts | utils/satoshi/test_generate_change_sdk.py |
| 4 targetSatoshis low | test/storage/idb/allocateChange.test.ts | utils/satoshi/test_generate_change_sdk.py |
| 5 targetSatoshis above max | test/storage/idb/allocateChange.test.ts | utils/satoshi/test_generate_change_sdk.py |
| 0 copy legacy wallet | test/storage/idb/idbSpeed.test.ts | universal/test_isauthenticated.py |
| 0 unaborted case | test/storage/idb/transactionAbort.test.ts | services/test_transaction_status.py |
| 1 call abort case | test/storage/idb/transactionAbort.test.ts | services/test_transaction_status.py |
| 2 throw error case | test/storage/idb/transactionAbort.test.ts | services/test_transaction_status.py |
| 7a updateTransactionStatus | test/storage/idb/update.test.ts | storage/entities/test_update.py |
| 7a updateTransactionStatus | test/storage/update.test.ts | storage/entities/test_update.py |

**Total missing tests: 257**