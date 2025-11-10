# AI-Powered Test Comparison Report

This report contains AI-analyzed comparisons between TypeScript and Python test implementations.

## Summary

- **Total Tests**: 540
- **Passing**: 350 (64.8%)
- **Failing**: 190 (35.2%)

---

## Test 1: All proxied methods call underlying with correct arguments **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 2: Decryption of primary key and building the wallet **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 3: Destroy callback clears sensitive data **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 4: Passes if user is authenticated and originator is not admin **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 5: Password retriever callback: the test function is passed and returns a boolean **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 6: Privileged key expiry: each call to decrypt via the privileged manager invokes passwordRetriever **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 7: Prompts to save the new key, updates the token **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts

```typescript
    test('Prompts to save the new key, updates the token', async () => {
      ;(mockUMPTokenInteractor.findByPresentationKeyHash as any).mockResolvedValueOnce(undefined)
      manager = new CWIStyleWalletManager(
        'admin.walletvendor.com',
        mockWalletBuilder,
        mockUMPTokenInteractor,
        mockRecoveryKeySaver,
        async () => 'test-password'
      )
      await manager.providePresentationKey(presentationKey)
      await manager.providePassword('test-password')
      expect(manager.authenticated).toBe(true)
      ;(mockUMPTokenInteractor.buildAndSend as any).mockResolvedValueOnce(makeOutpoint('rcv1', 0))
      await manager.changeRecoveryKey()

      // The user is prompted to store the new key
      expect(mockRecoveryKeySaver).toHaveBeenCalledTimes(2) // once when user created, once after changed
      // The UMP token is updated
      expect(mockUMPTokenInteractor.buildAndSend).toHaveBeenCalledTimes(2)
    })
```

### Python Test: py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py

```python
    async def test_prompts_to_save_the_new_key_updates_the_token(self) -> None:
        """Given: Authenticated manager
           When: Change recovery key
           Then: User is prompted to save new key, token is updated

        Reference: wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts
                   test('Prompts to save the new key, updates the token')
        """
        # Given
        mock_ump_interactor = Mock()
        mock_ump_interactor.find_by_presentation_key_hash = AsyncMock(return_value=None)
        mock_ump_interactor.build_and_send = AsyncMock(return_value="txid.0")

        mock_wallet_builder = AsyncMock()
        mock_underlying_wallet = Mock()
        mock_wallet_builder.return_value = mock_underlying_wallet

        mock_recovery_key_saver = AsyncMock(return_value=True)
        mock_password_retriever = AsyncMock(return_value="test-password")

        manager = CWIStyleWalletManager(
            ump_token_interactor=mock_ump_interactor,
            wallet_builder=mock_wallet_builder,
            recovery_key_saver=mock_recovery_key_saver,
            password_retriever=mock_password_retriever,
            admin_originator="admin.test.com",
        )

        # Authenticate as new user
        presentation_key = bytes([0xA1] * 32)
        await manager.provide_presentation_key(presentation_key)
        await manager.provide_password("test-password")

        # When
        await manager.change_recovery_key()

        # Then
        assert mock_recovery_key_saver.call_count == 2  # Initial + change
        assert mock_ump_interactor.build_and_send.call_count == 2
```

### AI Analysis Results

**Similarity Score**: 46.47%
  - Structural: 0.00%
  - Semantic: 32.94%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: manager.authenticated, mock_ump_token_interactor.buildAndSend
  - [HIGH] Python test is missing operations: manager.providePassword, manager.changeRecoveryKey, manager.providePresentationKey

**Differences:**
  - Verification count: TS has 3, PY has 2

**Suggestions:**
  - Add verifications for: manager.authenticated, mock_ump_token_interactor.buildAndSend
  - Add operations: manager.providePassword, manager.changeRecoveryKey, manager.providePresentationKey

**Explanation:**

Overall Similarity: 46.5%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 32.9% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: authentication key_save token_operation key_change method_call_verification password_operation verification password_provide value_verification
  • Python: authentication key_operation key_save token_operation key_change password_operation verification password_provide

Critical Issues (2):
  • [HIGH] Python test is missing verifications: manager.authenticated, mock_ump_token_interactor.buildAndSend
  • [HIGH] Python test is missing operations: manager.providePassword, manager.changeRecoveryKey, manager.providePresentationKey

Key Differences:
  • Verification count: TS has 3, PY has 2

---

## Test 8: Requires authentication and updates the UMP token on-chain **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 9: Requires authentication, re-publishes the token, old token consumed **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts

```typescript
    test('Requires authentication, re-publishes the token, old token consumed', async () => {
      ;(mockUMPTokenInteractor.findByPresentationKeyHash as any).mockResolvedValueOnce(undefined)
      manager = new CWIStyleWalletManager(
        'admin.walletvendor.com',
        mockWalletBuilder,
        mockUMPTokenInteractor,
        mockRecoveryKeySaver,
        async () => 'test-password'
      )
      await manager.providePresentationKey(presentationKey)
      await manager.providePassword('test-password')
      expect(manager.authenticated).toBe(true)
      ;(mockUMPTokenInteractor.buildAndSend as any).mockResolvedValueOnce(makeOutpoint('rcv1', 0))
      const newPresKey = Array.from({ length: 32 }, () => 0xee)
      await manager.changePresentationKey(newPresKey)
      expect(mockUMPTokenInteractor.buildAndSend).toHaveBeenCalledTimes(2)
    })
```

### Python Test: py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py

```python
    async def test_requires_authentication_re_publishes_the_token_old_token_consumed(self) -> None:
        """Given: Authenticated manager
           When: Change presentation key
           Then: Token is re-published, old token consumed

        Reference: wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts
                   test('Requires authentication, re-publishes the token, old token consumed')
        """
        # Given
        mock_ump_interactor = Mock()
        mock_ump_interactor.find_by_presentation_key_hash = AsyncMock(return_value=None)
        mock_ump_interactor.build_and_send = AsyncMock(return_value="txid.0")

        mock_wallet_builder = AsyncMock()
        mock_underlying_wallet = Mock()
        mock_wallet_builder.return_value = mock_underlying_wallet

        mock_recovery_key_saver = AsyncMock(return_value=True)
        mock_password_retriever = AsyncMock(return_value="test-password")

        manager = CWIStyleWalletManager(
            ump_token_interactor=mock_ump_interactor,
            wallet_builder=mock_wallet_builder,
            recovery_key_saver=mock_recovery_key_saver,
            password_retriever=mock_password_retriever,
            admin_originator="admin.test.com",
        )

        # Authenticate as new user
        presentation_key = bytes([0xA1] * 32)
        await manager.provide_presentation_key(presentation_key)
        await manager.provide_password("test-password")

        # When
        new_presentation_key = bytes([0xEE] * 32)
        await manager.change_presentation_key(new_presentation_key)

        # Then
        assert mock_ump_interactor.build_and_send.call_count == 2
```

### AI Analysis Results

**Similarity Score**: 46.84%
  - Structural: 0.00%
  - Semantic: 33.68%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: manager.authenticated, mock_ump_token_interactor.buildAndSend
  - [HIGH] Python test is missing operations: manager.providePassword, manager.changePresentationKey, manager.providePresentationKey

**Differences:**
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: manager.authenticated, mock_ump_token_interactor.buildAndSend
  - Add operations: manager.providePassword, manager.changePresentationKey, manager.providePresentationKey

**Explanation:**

Overall Similarity: 46.8%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 33.7% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: authentication key_save token_operation key_change method_call_verification password_operation verification token_lifecycle password_provide value_verification
  • Python: authentication key_operation key_save token_operation key_change password_operation verification token_lifecycle password_provide

Critical Issues (2):
  • [HIGH] Python test is missing verifications: manager.authenticated, mock_ump_token_interactor.buildAndSend
  • [HIGH] Python test is missing operations: manager.providePassword, manager.changePresentationKey, manager.providePresentationKey

Key Differences:
  • Verification count: TS has 2, PY has 1

---

## Test 10: Saves a snapshot and can load it into a fresh manager instance **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts

```typescript
    test('Saves a snapshot and can load it into a fresh manager instance', async () => {
      // We'll do a new user flow so that manager is authenticated with a real token.
      ;(mockUMPTokenInteractor.findByPresentationKeyHash as any).mockResolvedValueOnce(undefined)
      const presKey = Array.from({ length: 32 }, () => 0xa1)
      await manager.providePresentationKey(presKey)
      await manager.providePassword('mypassword') // triggers creation of new user

      const snapshot = manager.saveSnapshot()
      expect(Array.isArray(snapshot)).toBe(true)
      expect(snapshot.length).toBeGreaterThan(64) // 32 bytes + encrypted data

      // Now create a fresh manager:
      const freshManager = new CWIStyleWalletManager(
        'admin.walletvendor.com',
        mockWalletBuilder,
        mockUMPTokenInteractor,
        mockRecoveryKeySaver,
        mockPasswordRetriever
      )

      // Not authenticated yet
      await expect(() => freshManager.getPublicKey({ identityKey: true })).rejects.toThrow('User is not authenticated')

      // Load the snapshot
      await freshManager.loadSnapshot(snapshot)

      // The fresh manager is now authenticated (underlying wallet will be built).
      await expect(freshManager.getPublicKey({ identityKey: true })).resolves.not.toThrow()

      // It calls walletBuilder again
      expect(mockWalletBuilder).toHaveBeenCalledTimes(2) // once for the old manager, once for the fresh
    })
```

### Python Test: py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py

```python
    async def test_saves_a_snapshot_and_can_load_it_into_a_fresh_manager_instance(self) -> None:
        """Given: Authenticated manager with wallet
           When: Save snapshot and load into new manager instance
           Then: New manager has same state

        Reference: wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts
                   test('Saves a snapshot and can load it into a fresh manager instance')
        """
        presentation_key = os.urandom(32)
        recovery_key = os.urandom(32)
        password_salt = os.urandom(32)
        password_key = hashlib.pbkdf2_hmac("sha512", b"test-password", password_salt, PBKDF2_NUM_ROUNDS, 32)
        primary_key = os.urandom(32)
        privileged_key = os.urandom(32)

        existing_token = await create_mock_ump_token(
            presentation_key, recovery_key, password_key, password_salt, PBKDF2_NUM_ROUNDS, primary_key, privileged_key
        )

        mock_underlying_wallet = MagicMock(spec=WalletInterface)
        mock_wallet_builder = AsyncMock(return_value=mock_underlying_wallet)
        mock_ump_interactor = MagicMock(spec=UMPTokenInteractor)
        mock_ump_interactor.find_by_presentation_key_hash = AsyncMock(return_value=existing_token)
        mock_recovery_key_saver = AsyncMock(return_value=True)
        mock_password_retriever = AsyncMock(return_value="test-password")

        manager1 = CWIStyleWalletManager(
            ump_token_interactor=mock_ump_interactor,
            wallet_builder=mock_wallet_builder,
            recovery_key_saver=mock_recovery_key_saver,
            password_retriever=mock_password_retriever,
            admin_originator="admin.test.com",
        )

        await manager1.authenticate(presentation_key)

        snapshot = await manager1.save_snapshot()

        manager2 = CWIStyleWalletManager(
            ump_token_interactor=mock_ump_interactor,
            wallet_builder=mock_wallet_builder,
            recovery_key_saver=mock_recovery_key_saver,
            password_retriever=mock_password_retriever,
            admin_originator="admin.test.com",
        )

        await manager2.load_snapshot(snapshot)

        assert manager2.is_authenticated() is True
        assert manager2.get_primary_key() == manager1.get_primary_key()
```

### AI Analysis Results

**Similarity Score**: 16.00%
  - Structural: 0.00%
  - Semantic: 32.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: snapshot.length
  - [HIGH] Python test is missing operations: manager.providePassword, fresh_manager.loadSnapshot, manager.providePresentationKey

**Suggestions:**
  - Add verifications for: snapshot.length
  - Add operations: manager.providePassword, fresh_manager.loadSnapshot, manager.providePresentationKey

**Explanation:**

Overall Similarity: 16.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 32.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: authentication key_save token_operation snapshot_save snapshot_load snapshot_operation password_operation password_provide verification value_verification encryption
  • Python: authentication key_operation key_save token_operation snapshot_save snapshot_load snapshot_operation password_operation verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: snapshot.length
  • [HIGH] Python test is missing operations: manager.providePassword, fresh_manager.loadSnapshot, manager.providePresentationKey

---

## Test 11: Successfully creates a new token and calls buildAndSend **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts

```typescript
    test('Successfully creates a new token and calls buildAndSend', async () => {
      // New wallet funder is a mock function
      const newWalletFunder = jest.fn(() => {})
      ;(manager as any).newWalletFunder = newWalletFunder

      // Mock that no token is found by presentation key hash
      ;(mockUMPTokenInteractor.findByPresentationKeyHash as any).mockResolvedValueOnce(undefined)

      // Provide a presentation key
      await manager.providePresentationKey(presentationKey)

      expect(manager.authenticationFlow).toBe('new-user')

      // Provide a password
      mockPasswordRetriever.mockResolvedValueOnce('dummy-password')
      await manager.providePassword('dummy-password')

      // The wallet should now be built, so manager is authenticated
      expect(manager.authenticated).toBe(true)

      // Recovery key saver should have been called
      expect(mockRecoveryKeySaver).toHaveBeenCalledTimes(1)

      // The underlying wallet builder should have been called exactly once
      expect(mockWalletBuilder).toHaveBeenCalledTimes(1)

      // The manager should have called buildAndSend on the interactor
      expect(mockUMPTokenInteractor.buildAndSend).toHaveBeenCalledTimes(1)
      const buildArgs = (mockUMPTokenInteractor.buildAndSend as any).mock.calls[0]
      // [0] => the wallet, [1] => adminOriginator, [2] => newToken, [3] => oldToken
      expect(buildArgs[1]).toBe('admin.walletvendor.com')
      expect(buildArgs[2]).toHaveProperty('presentationHash')
      expect(buildArgs[3]).toBeUndefined() // Because it's a new user (no old token)
      expect(newWalletFunder).toHaveBeenCalled() // New wallet funder should have been called
    })
```

### Python Test: py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py

```python
    async def test_successfully_creates_a_new_token_and_calls_buildandsend(self) -> None:
        """Given: New user registration with presentation key and password
           When: Create new UMP token
           Then: Token is created and buildAndSend is called

        Reference: wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts
                   test('Successfully creates a new token and calls buildAndSend')
        """
        mock_underlying_wallet = MagicMock(spec=WalletInterface)
        mock_wallet_builder = AsyncMock(return_value=mock_underlying_wallet)
        mock_ump_interactor = MagicMock(spec=UMPTokenInteractor)
        mock_ump_interactor.find_by_presentation_key_hash = AsyncMock(return_value=None)
        mock_ump_interactor.build_and_send = AsyncMock(return_value="abcd.0")
        mock_recovery_key_saver = AsyncMock(return_value=True)
        mock_password_retriever = AsyncMock(return_value="test-password")

        manager = CWIStyleWalletManager(
            ump_token_interactor=mock_ump_interactor,
            wallet_builder=mock_wallet_builder,
            recovery_key_saver=mock_recovery_key_saver,
            password_retriever=mock_password_retriever,
            admin_originator="admin.test.com",
        )

        presentation_key = os.urandom(32)

        result = await manager.create_new_user(presentation_key)

        assert result["token"] is not None
        assert mock_ump_interactor.build_and_send.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 14.00%
  - Structural: 0.00%
  - Semantic: 28.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: manager.authenticated, manager.authenticationFlow, mock_ump_token_interactor.buildAndSend
  - [HIGH] Python test is missing operations: manager.providePassword, manager.providePresentationKey

**Differences:**
  - Operation count: TS has 2, PY has 1
  - Verification count: TS has 5, PY has 2

**Suggestions:**
  - Add verifications for: manager.authenticated, manager.authenticationFlow, mock_ump_token_interactor.buildAndSend
  - Add operations: manager.providePassword, manager.providePresentationKey

**Explanation:**

Overall Similarity: 14.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 28.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: authentication key_save token_operation method_call_verification password_operation verification password_provide value_verification
  • Python: key_operation key_save token_operation password_operation verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: manager.authenticated, manager.authenticationFlow, mock_ump_token_interactor.buildAndSend
  • [HIGH] Python test is missing operations: manager.providePassword, manager.providePresentationKey

Key Differences:
  • Operation count: TS has 2, PY has 1
  • Verification count: TS has 5, PY has 2

---

## Test 12: Successfully decrypts with presentation+recovery **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 13: Throws error if saving snapshot while no primary key or token set **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 14: Throws if no token found by recovery key hash **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 15: Throws if not authenticated **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 16: Throws if not authenticated **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 17: Throws if originator is adminOriginator **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts

```typescript
    test('Throws if originator is adminOriginator', async () => {
      await expect(manager.getPublicKey({ identityKey: true }, 'admin.walletvendor.com')).rejects.toThrow(
        'External applications are not allowed to use the admin originator.'
      )
    })
```

### Python Test: py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py

```python
    async def test_throws_if_originator_is_adminoriginator(self) -> None:
        """Given: Authenticated manager
           When: Call method with admin originator
           Then: Raises error

        Reference: wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts
                   test('Throws if originator is adminOriginator')
        """
        # Given
        mock_ump_interactor = Mock()
        mock_ump_interactor.find_by_presentation_key_hash = AsyncMock(return_value=None)
        mock_ump_interactor.build_and_send = AsyncMock(return_value="txid.0")

        mock_wallet_builder = AsyncMock()
        mock_underlying_wallet = Mock()
        mock_wallet_builder.return_value = mock_underlying_wallet

        mock_recovery_key_saver = AsyncMock(return_value=True)
        mock_password_retriever = AsyncMock(return_value="test-password")

        manager = CWIStyleWalletManager(
            ump_token_interactor=mock_ump_interactor,
            wallet_builder=mock_wallet_builder,
            recovery_key_saver=mock_recovery_key_saver,
            password_retriever=mock_password_retriever,
            admin_originator="admin.test.com",
        )

        # Authenticate
        presentation_key = bytes([0xA1] * 32)
        await manager.provide_presentation_key(presentation_key)
        await manager.provide_password("test-password")

        # When/Then
        with pytest.raises(ValueError, match="External applications are not allowed to use the admin originator"):
            await manager.get_public_key({"identity_key": True}, originator="admin.test.com")
```

### AI Analysis Results

**Similarity Score**: 30.00%
  - Structural: 0.00%
  - Semantic: 60.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'authentication key_operation key_save token_operation password_operation password_provide'

**Differences:**
  - Operation count: TS has 0, PY has 3

**Suggestions:**
  - Align test intent: ensure PY test verifies 'verification'

**Explanation:**

Overall Similarity: 30.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 60.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification
  • Python: authentication key_operation key_save token_operation password_operation password_provide

Critical Issues (1):
  • [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'authentication key_operation key_save token_operation password_operation password_provide'

Key Differences:
  • Operation count: TS has 0, PY has 3

---

## Test 18: Throws if presentation key not provided first **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 19: Throws if snapshot is corrupt or cannot be decrypted **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts

```typescript
    test('Throws if snapshot is corrupt or cannot be decrypted', async () => {
      // Attempt to load an invalid snapshot
      await expect(() => manager.loadSnapshot([1, 2, 3])).rejects.toThrow('Failed to load snapshot')
    })
```

### Python Test: py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py

```python
    async def test_throws_if_snapshot_is_corrupt_or_cannot_be_decrypted(self) -> None:
        """Given: Corrupted or invalid snapshot data
           When: Try to load snapshot
           Then: Raises decryption error

        Reference: wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts
                   test('Throws if snapshot is corrupt or cannot be decrypted')
        """
        mock_underlying_wallet = MagicMock(spec=WalletInterface)
        mock_wallet_builder = AsyncMock(return_value=mock_underlying_wallet)
        mock_ump_interactor = MagicMock(spec=UMPTokenInteractor)
        mock_recovery_key_saver = AsyncMock(return_value=True)
        mock_password_retriever = AsyncMock(return_value="test-password")

        manager = CWIStyleWalletManager(
            ump_token_interactor=mock_ump_interactor,
            wallet_builder=mock_wallet_builder,
            recovery_key_saver=mock_recovery_key_saver,
            password_retriever=mock_password_retriever,
            admin_originator="admin.test.com",
        )

        corrupted_snapshot = b"invalid data"

        with pytest.raises(ValueError, match="decryption failed"):
            await manager.load_snapshot(corrupted_snapshot)
```

### AI Analysis Results

**Similarity Score**: 42.00%
  - Structural: 10.00%
  - Semantic: 80.00%
  - Alignment: 0.00%

**Differences:**
  - Operation count: TS has 0, PY has 1

**Explanation:**

Overall Similarity: 42.0%
  • Structural: 10.0% (sequence and structure)
  • Semantic: 80.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: decryption snapshot_load snapshot_operation verification
  • Python: key_operation decryption key_save token_operation snapshot_save snapshot_load snapshot_operation password_operation

Key Differences:
  • Operation count: TS has 0, PY has 1

---

## Test 20: Throws if user is not authenticated **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 21: Throws if user tries to provide recovery key during new-user flow **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 22: Works with correct keys, sets mode as existing-user **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 23: XOR function: verifies correctness **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 24: isAuthenticated() rejects if originator is admin, resolves otherwise **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 25: serializeUMPToken and deserializeUMPToken correctly round-trip a UMP token **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts

```typescript
    test('serializeUMPToken and deserializeUMPToken correctly round-trip a UMP token', async () => {
      const token = await createMockUMPToken()
      // We need a token with a currentOutpoint for serialization.
      expect(token.currentOutpoint).toBeDefined()
      const serializeFn = (manager as any).serializeUMPToken as (token: UMPToken) => number[]
      const deserializeFn = (manager as any).deserializeUMPToken as (bin: number[]) => UMPToken

      const serialized = serializeFn(token)
      expect(Array.isArray(serialized)).toBe(true)
      expect(serialized.length).toBeGreaterThan(0)

      const deserialized = deserializeFn(serialized)
      expect(deserialized).toEqual(token)
    })
```

### Python Test: py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py

```python
    async def test_serializeumptoken_and_deserializeumptoken_correctly_round_trip_a_ump_token(self) -> None:
        """Given: UMP token
           When: Serialize and deserialize
           Then: Token round-trips correctly

        Reference: wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts
                   test('serializeUMPToken and deserializeUMPToken correctly round-trip a UMP token')
        """
        # Given
        mock_ump_interactor = Mock()
        mock_ump_interactor.find_by_presentation_key_hash = AsyncMock(return_value=None)
        mock_ump_interactor.build_and_send = AsyncMock(return_value="txid.0")

        mock_wallet_builder = AsyncMock()
        mock_underlying_wallet = Mock()
        mock_wallet_builder.return_value = mock_underlying_wallet

        mock_recovery_key_saver = AsyncMock(return_value=True)
        mock_password_retriever = AsyncMock(return_value="test-password")

        manager = CWIStyleWalletManager(
            ump_token_interactor=mock_ump_interactor,
            wallet_builder=mock_wallet_builder,
            recovery_key_saver=mock_recovery_key_saver,
            password_retriever=mock_password_retriever,
            admin_originator="admin.test.com",
        )

        # Create a mock token

        token = MagicMock()
        token.password_salt = bytes([0x01] * 32)
        token.current_outpoint = "txid.0"

        # When - access private methods via manager instance
        serialize_fn = getattr(manager, "_serialize_ump_token", None)
        deserialize_fn = getattr(manager, "_deserialize_ump_token", None)

        if serialize_fn and deserialize_fn:
            serialized = serialize_fn(token)
            assert isinstance(serialized, bytes)
            assert len(serialized) > 0

            deserialized = deserialize_fn(serialized)
            assert deserialized == token
```

### AI Analysis Results

**Similarity Score**: 42.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: token.currentOutpoint, serialized.length

**Differences:**
  - Verification count: TS has 2, PY has 0

**Suggestions:**
  - Add verifications for: token.currentOutpoint, serialized.length

**Explanation:**

Overall Similarity: 42.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification token_operation verification
  • Python: key_operation key_save token_operation password_operation verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: token.currentOutpoint, serialized.length

Key Differences:
  • Verification count: TS has 2, PY has 0

---

## Test 26: waitForAuthentication() eventually resolves **PASS**

- TypeScript: `wallet-toolbox/src/__tests/CWIStyleWalletManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_cwi_style_wallet_manager.py`

---

## Test 27: a failing callback (throwing an error) does not block subsequent callbacks **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.callbacks.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_callbacks.py`

---

## Test 28: bindCallback() should register multiple callbacks for the same event, which are called in sequence **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.callbacks.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_callbacks.py`

---

## Test 29: multiple pending requests for different resources should trigger separate onXxxRequested callbacks **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.callbacks.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_callbacks.py`

---

## Test 30: multiple pending requests for the same resource should trigger only one onXxxRequested callback **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.callbacks.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_callbacks.py`

---

## Test 31: should reject the original caller promise when permission is denied **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.callbacks.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_callbacks.py`

---

## Test 32: should resolve the original caller promise when requests are granted **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.callbacks.test.ts

```typescript
  it('should resolve the original caller promise when requests are granted', async () => {
    const requestedCb = jest.fn(() => {})
    manager.bindCallback('onProtocolPermissionRequested', requestedCb)

    // Start an operation that requires permission
    const signPromise = manager.createSignature(
      {
        protocolID: [1, 'testproto'],
        keyID: '1',
        data: [0xaa],
        privileged: false
      },
      'nonadmin.com'
    )

    // Wait for request to appear
    await new Promise(r => setTimeout(r, 10))
    expect(requestedCb).toHaveBeenCalledTimes(1)

    // Extract the requestID from the callback
    const requestID = (requestedCb.mock as any).calls[0][0].requestID

    // Now grant the request
    const grantParams = {
      requestID,
      expiry: 123456789,
      ephemeral: true
    }
    await manager.grantPermission(grantParams)

    // The signPromise should now resolve (meaning the original createSignature call finishes successfully).
    await expect(signPromise).resolves.toBeDefined()
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_callbacks.py

```python
    def test_should_resolve_the_original_caller_promise_when_requests_are_granted(self) -> None:
        """Given: Permission manager with pending request
           When: Permission is granted
           Then: Original caller's promise resolves

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.callbacks.test.ts
                   test('should resolve the original caller promise when requests are granted')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.get_public_key = AsyncMock(return_value={"publicKey": "test-key"})

        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test.com",
            config={"securityLevel": 1, "seekProtocolPermissions": True},
        )

        async def permission_callback(params) -> None:
            # Grant permission immediately
            manager.grant_permission(params["requestID"], {"ephemeral": False})

        manager.bind_callback("onProtocolPermissionRequested", permission_callback)

        # When - request permission
        result = manager.get_public_key(
            {"identityKey": True, "protocolID": [1, "test"], "keyID": "1"}, originator="example.com"
        )

        # Then - promise resolved with result
        assert result == {"publicKey": "test-key"}
        mock_underlying_wallet.get_public_key.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing operations: manager.grantPermission

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add operations: manager.grantPermission

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification
  • Python: verification method_call_verification

Critical Issues (1):
  • [HIGH] Python test is missing operations: manager.grantPermission

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 33: should trigger onProtocolPermissionRequested with correct params when a non-admin domain requests a protocol operation **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.callbacks.test.ts

```typescript
  it('should trigger onProtocolPermissionRequested with correct params when a non-admin domain requests a protocol operation', async () => {
    const requestedCb = jest.fn(() => {})

    // We bind to onProtocolPermissionRequested
    manager.bindCallback('onProtocolPermissionRequested', requestedCb)

    // Attempt an operation that requires protocol permission:
    // e.g., createSignature with level=1 protocol
    const signPromise = manager.createSignature(
      {
        protocolID: [1, 'some-protocol'],
        keyID: '1',
        data: [0x01, 0x02],
        privileged: false
      },
      'non-admin.example.com'
    )

    // Wait a tick so the request can be queued
    await new Promise(r => setTimeout(r, 10))

    // We expect onProtocolPermissionRequested to have been fired once
    expect(requestedCb).toHaveBeenCalledTimes(1)

    // The callback param should include fields from the `PermissionRequest`
    const callArg = (requestedCb.mock as any).calls[0][0]
    expect(callArg.type).toBe('protocol')
    expect(callArg.originator).toBe('non-admin.example.com')
    expect(callArg.requestID).toMatch(/^proto:non-admin.example.com:false/) // The manager auto-generates an ID

    // The original sign call is still pending (since we haven't granted or denied).
    // We'll deny it for cleanup:
    manager.denyPermission(callArg.requestID)

    await expect(signPromise).rejects.toThrow(/Permission denied/)
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_callbacks.py

```python
    def test_should_trigger_onprotocolpermissionrequested_with_correct_params_when_a_non_admin_domain_requests_a_protocol_operation(
        self,
    ) -> None:
        """Given: Permission manager with callback
           When: Non-admin domain requests protocol operation
           Then: onProtocolPermissionRequested callback is triggered with correct params

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.callbacks.test.ts
                   test('should trigger onProtocolPermissionRequested with correct params when a non-admin domain requests a protocol operation')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.get_public_key = AsyncMock(return_value={"publicKey": "test"})

        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test.com",
            config={"securityLevel": 1, "seekProtocolPermissions": True},
        )

        captured_params = None

        async def permission_callback(params) -> None:
            nonlocal captured_params
            captured_params = params
            # Grant permission
            manager.grant_permission(params["requestID"], {"ephemeral": False})

        manager.bind_callback("onProtocolPermissionRequested", permission_callback)

        # When - non-admin domain requests protocol operation
        manager.get_public_key(
            {"identityKey": True, "protocolID": [1, "test-protocol"], "keyID": "1"}, originator="example.com"
        )

        # Then
        assert captured_params is not None
        assert captured_params["originator"] == "example.com"
        assert captured_params["protocolID"] == [1, "test-protocol"]
        assert "requestID" in captured_params
```

### AI Analysis Results

**Similarity Score**: 43.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: call_arg.requestID, call_arg.originator, call_arg.type

**Differences:**
  - Verification count: TS has 4, PY has 2

**Suggestions:**
  - Add verifications for: call_arg.requestID, call_arg.originator, call_arg.type

**Explanation:**

Overall Similarity: 43.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: call_arg.requestID, call_arg.originator, call_arg.type

Key Differences:
  • Verification count: TS has 4, PY has 2

---

## Test 34: unbindCallback() by function reference should remove the callback **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.callbacks.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_callbacks.py`

---

## Test 35: unbindCallback() by numeric ID should prevent the callback from being called again **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.callbacks.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_callbacks.py`

---

## Test 36: should also prompt for listing actions by label if seekPermissionWhenListingActionsByLabel=true **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should also prompt for listing actions by label if seekPermissionWhenListingActionsByLabel=true', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {
        seekPermissionWhenListingActionsByLabel: true
      })

      manager.bindCallback('onProtocolPermissionRequested', async req => {
        // auto-grant ephemeral
        await manager.grantPermission({
          requestID: req.requestID,
          ephemeral: true
        })
      })

      await expect(
        manager.listActions(
          {
            labels: ['search-this-label']
          },
          'external-app.com'
        )
      ).resolves.not.toThrow()

      expect(underlying.listActions).toHaveBeenCalledTimes(1)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_also_prompt_for_listing_actions_by_label_if_seekpermissionwhenlistingactionsbylabel_true(
        self,
    ) -> None:
        """Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
        test('should also prompt for listing actions by label if seekPermissionWhenListingActionsByLabel=true')"""
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.list_actions = AsyncMock(return_value={"totalActions": 0, "actions": []})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"seekPermissionWhenListingActionsByLabel": True},
        )

        async def permission_callback(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onLabelPermissionRequested", permission_callback)
        manager.list_actions({"label": "user-label"}, originator="user.com")
        mock_underlying_wallet.list_actions.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 20.00%
  - Structural: 0.00%
  - Semantic: 40.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.listActions
  - [HIGH] Python test is missing operations: manager.grantPermission

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: underlying.listActions
  - Add operations: manager.grantPermission

**Explanation:**

Overall Similarity: 20.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 40.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification method_call_verification
  • Python: verification method_call_verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.listActions
  • [HIGH] Python test is missing operations: manager.grantPermission

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 37: should check monthly limit usage and prompt renewal if insufficient **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should check monthly limit usage and prompt renewal if insufficient', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com')

      // Suppose we find an existing DSAP token with authorizedAmount=500
      // manager.findSpendingToken() is used internally, so let's mock it
      const existingSpendingToken: PermissionToken = {
        tx: [],
        txid: 'dsap-old',
        outputIndex: 0,
        outputScript: 'scriptHex',
        satoshis: 1,
        originator: 'shopper.com',
        authorizedAmount: 500,
        expiry: 0 // indefinite
      }
      jest.spyOn(manager as any, 'findSpendingToken').mockResolvedValue(existingSpendingToken)

      // Next, manager.querySpentSince(token) sums the user’s monthly spending from labeled actions
      // Let’s stub that to say they've already spent 400.
      jest.spyOn(manager as any, 'querySpentSince').mockResolvedValue(400)

      // Attempt spending 200 => total usage would be 600 which exceeds 500 => prompt renewal
      // We'll auto-deny for test
      manager.bindCallback('onSpendingAuthorizationRequested', req => {
        manager.denyPermission(req.requestID)
      })

      await expect(
        manager.createAction(
          {
            description: 'Buy something for 200 sats',
            outputs: [
              {
                outputDescription: 'Nothing to see here',
                lockingScript: 'op_return',
                satoshis: 200
              }
            ]
          },
          'shopper.com'
        )
      ).rejects.toThrow(/Permission denied/)

      // The underlying createAction call was started but the manager calls abortAction upon denial
      expect(underlying.abortAction).toHaveBeenCalledTimes(1)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_check_monthly_limit_usage_and_prompt_renewal_if_insufficient(self) -> None:
        """Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
        test('should check monthly limit usage and prompt renewal if insufficient')"""
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_action = AsyncMock(
            return_value={"signableTransaction": {"tx": [0x00], "reference": "ref1"}}
        )
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"seekSpendingPermissions": True},
        )
        existing_token = {
            "txid": "spend-token",
            "outputIndex": 0,
            "originator": "user.com",
            "expiry": 9999999999,
            "privileged": False,
            "monthlyLimit": 1000,
            "usage": 950,
        }
        manager._find_spending_token = AsyncMock(return_value=existing_token)

        async def permission_callback(request) -> None:
            assert request.get("renewal") is True
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onSpendingAuthorizationRequested", permission_callback)
        manager.create_action(
            {
                "description": "Spend 100 sats",
                "outputs": [{"lockingScript": "abcd", "satoshis": 100, "outputDescription": "test"}],
            },
            originator="user.com",
        )
        mock_underlying_wallet.create_action.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 50.00%
  - Structural: 0.00%
  - Semantic: 40.00%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.abortAction

**Differences:**
  - Verification count: TS has 1, PY has 2

**Suggestions:**
  - Add verifications for: underlying.abortAction

**Explanation:**

Overall Similarity: 50.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 40.0% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: token_operation verification method_call_verification
  • Python: token_operation verification method_call_verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: underlying.abortAction

Key Differences:
  • Verification count: TS has 1, PY has 2

---

## Test 38: should check that requested fields are a subset of the token’s fields **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should check that requested fields are a subset of the token’s fields', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {
        seekCertificateDisclosurePermissions: true
      })

      // Suppose we find an existing token that covers fields: ['name', 'dob', 'nationality']
      const existingToken: PermissionToken = {
        tx: [],
        txid: 'aabbcc',
        outputIndex: 0,
        outputScript: 'scriptHex',
        satoshis: 1,
        originator: 'some-user.com',
        expiry: 9999999999, // not expired
        privileged: false,
        certType: 'KYC',
        certFields: ['name', 'dob', 'nationality'],
        verifier: '02eeee...'
      }
      jest
        .spyOn(manager as any, 'findCertificateToken')
        .mockImplementation(async (orig, priv, verif, ct, requestedFields) => {
          // if requestedFields includes "someMissingField", return undefined
          // else return the existingToken
          if ((requestedFields as string[]).includes('someMissingField')) {
            return undefined // forces a request
          }
          return existingToken // forces immediate success
        })

      // Attempt to prove certificate revealing only 'name' -> Should pass without prompt
      await manager.proveCertificate(
        {
          certificate: {
            type: 'KYC',
            certifier: '02eeee...',
            subject: '02some...',
            serialNumber: '',
            fields: { name: 'Charlie', dob: '1999-01-01', nationality: 'EU' }
          },
          fieldsToReveal: ['name'],
          verifier: '02eeee...',
          privileged: false
        },
        'some-user.com'
      )
      expect(underlying.proveCertificate).toHaveBeenCalledTimes(1)

      // Attempt to reveal a field the token does NOT cover -> triggers request
      // Since the existing token does not cover 'someMissingField', we expect a prompt. Let’s deny it:
      manager.bindCallback('onCertificateAccessRequested', async req => {
        manager.denyPermission(req.requestID)
      })
      const secondAttempt = manager.proveCertificate(
        {
          certificate: {
            type: 'KYC',
            certifier: '02eeee...',
            fields: { name: 'Charlie', dob: '1999-01-01', nationality: 'EU' }
          },
          fieldsToReveal: ['dob', 'someMissingField'],
          verifier: '02eeee...',
          privileged: false
        },
        'some-user.com'
      )
      await expect(secondAttempt).rejects.toThrow(/Permission denied/)

      // Underlying proveCertificate not called for second attempt
      expect(underlying.proveCertificate).toHaveBeenCalledTimes(1)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_check_that_requested_fields_are_a_subset_of_the_tokens_fields(self) -> None:
        """Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
        test('should check that requested fields are a subset of the token's fields')"""
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.prove_certificate = AsyncMock(return_value={"keyring": {}})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"seekCertificateDisclosurePermissions": True},
        )
        existing_token = {
            "txid": "aabbcc",
            "outputIndex": 0,
            "originator": "some-user.com",
            "expiry": 9999999999,
            "privileged": False,
            "certType": "KYC",
            "certFields": ["name", "dob", "nationality"],
            "verifier": "02eeee",
        }
        manager._find_certificate_token = AsyncMock(return_value=existing_token)
        manager.prove_certificate(
            {
                "certificate": {
                    "type": "KYC",
                    "certifier": "02eeee",
                    "subject": "02some",
                    "serialNumber": "",
                    "fields": {"name": "Charlie", "dob": "1999-01-01"},
                },
                "fieldsToReveal": ["name"],
                "verifier": "02eeee",
                "privileged": False,
            },
            originator="some-user.com",
        )
        assert mock_underlying_wallet.prove_certificate.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 16.00%
  - Structural: 0.00%
  - Semantic: 32.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.proveCertificate
  - [HIGH] Python test is missing operations: manager.proveCertificate

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: underlying.proveCertificate
  - Add operations: manager.proveCertificate

**Explanation:**

Overall Similarity: 16.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 32.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: token_operation verification method_call_verification
  • Python: token_operation verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.proveCertificate
  • [HIGH] Python test is missing operations: manager.proveCertificate

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 39: should deny protocol usage if user denies permission **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should deny protocol usage if user denies permission', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {})

      // The callback denies the request
      manager.bindCallback('onProtocolPermissionRequested', request => {
        manager.denyPermission(request.requestID)
      })

      // Attempt an operation that requires protocol permission
      await expect(
        manager.encrypt(
          {
            protocolID: [1, 'needs-perm'],
            plaintext: [1, 2, 3],
            keyID: 'xyz'
          },
          'external-app.com'
        )
      ).rejects.toThrow(/Permission denied/)

      // Underlying encrypt was never called
      expect(underlying.encrypt).toHaveBeenCalledTimes(0)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_deny_protocol_usage_if_user_denies_permission(self) -> None:
        """Given: Manager with deny callback
           When: Request protocol operation
           Then: Permission denied error

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
                   test('should deny protocol usage if user denies permission')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.encrypt = AsyncMock(return_value={"ciphertext": [1, 2, 3]})

        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.com")

        # Deny callback
        def permission_callback(request) -> None:
            manager.deny_permission(request["requestID"])

        manager.bind_callback("onProtocolPermissionRequested", permission_callback)

        # When/Then - permission denied
        with pytest.raises(ValueError, match="Permission denied"):
            manager.encrypt(
                {"protocolID": [1, "needs-perm"], "plaintext": [1, 2, 3], "keyID": "xyz"}, originator="external-app.com"
            )

        # Underlying encrypt never called
        mock_underlying_wallet.encrypt.assert_not_called()
```

### AI Analysis Results

**Similarity Score**: 50.00%
  - Structural: 0.00%
  - Semantic: 40.00%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.encrypt

**Suggestions:**
  - Add verifications for: underlying.encrypt

**Explanation:**

Overall Similarity: 50.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 40.0% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: verification method_call_verification encryption
  • Python: verification method_call_verification encryption

Critical Issues (1):
  • [HIGH] Python test is missing verifications: underlying.encrypt

---

## Test 40: should enforce privileged token if differentiatePrivilegedOperations=true **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should enforce privileged token if differentiatePrivilegedOperations=true', async () => {
      // By default, differentiatePrivilegedOperations is true.
      manager = new WalletPermissionsManager(underlying, 'admin.com', {
        seekProtocolPermissionsForSigning: true
      })

      manager.bindCallback('onProtocolPermissionRequested', async req => {
        // The request has `privileged=true`, so the resulting token must also be privileged.
        // We'll grant ephemeral to simulate success quickly.
        await manager.grantPermission({
          requestID: req.requestID,
          ephemeral: true
        })
      })

      // Attempt a privileged signature
      await expect(
        manager.createSignature(
          {
            protocolID: [1, 'high-level-crypto'],
            privileged: true,
            data: [0xc0, 0xff, 0xee],
            keyID: '1'
          },
          'nonadmin.app'
        )
      ).resolves.not.toThrow()

      // Confirm underlying was ultimately called
      expect(underlying.createSignature).toHaveBeenCalledTimes(1)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_enforce_privileged_token_if_differentiateprivilegedoperations_true(self) -> None:
        """Given: Manager with differentiatePrivilegedOperations=true
           When: Request privileged operation
           Then: Privileged permission required

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
                   test('should enforce privileged token if differentiatePrivilegedOperations=true')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_signature = AsyncMock(return_value={"signature": [0xC0, 0xFF, 0xEE]})

        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"seekProtocolPermissionsForSigning": True, "differentiatePrivilegedOperations": True},
        )

        async def permission_callback(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onProtocolPermissionRequested", permission_callback)

        # When - privileged signature
        manager.create_signature(
            {"protocolID": [1, "high-level-crypto"], "privileged": True, "data": [0xC0, 0xFF, 0xEE], "keyID": "1"},
            originator="nonadmin.app",
        )

        # Then - underlying called
        mock_underlying_wallet.create_signature.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 20.00%
  - Structural: 0.00%
  - Semantic: 40.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createSignature
  - [HIGH] Python test is missing operations: manager.grantPermission

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: underlying.createSignature
  - Add operations: manager.grantPermission

**Explanation:**

Overall Similarity: 20.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 40.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: token_operation verification method_call_verification
  • Python: token_operation verification method_call_verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.createSignature
  • [HIGH] Python test is missing operations: manager.grantPermission

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 41: should fail if label starts with **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should fail if label starts with "admin" and caller is not admin', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com')

      // Attempt to createAction with a label "admin secret-stuff"
      await expect(
        manager.createAction(
          {
            description: 'Applying admin label?',
            labels: ['admin secret-stuff']
          },
          'nonadmin.com'
        )
      ).rejects.toThrow(/admin-only/)

      // Underlying createAction never called
      expect(underlying.createAction).toHaveBeenCalledTimes(0)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_fail_if_label_starts_with_admin(self) -> None:
        """Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
        test('should fail if label starts with')"""
        mock_underlying_wallet = Mock(spec=WalletInterface)
        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.com")
        with pytest.raises(ValueError, match="admin-only"):
            manager.create_action(
                {
                    "description": "test",
                    "labels": ["admin restricted-label"],
                    "outputs": [{"lockingScript": "abcd", "satoshis": 100}],
                },
                originator="user.com",
            )
```

### AI Analysis Results

**Similarity Score**: 30.00%
  - Structural: 0.00%
  - Semantic: 0.00%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'verification method_call_verification' but PY verifies 'general_test'
  - [HIGH] Python test is missing verifications: underlying.createAction

**Differences:**
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'verification method_call_verification'
  - Add verifications for: underlying.createAction

**Explanation:**

Overall Similarity: 30.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 0.0% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: verification method_call_verification
  • Python: general_test

Critical Issues (2):
  • [HIGH] Test intent differs: TS verifies 'verification method_call_verification' but PY verifies 'general_test'
  • [HIGH] Python test is missing verifications: underlying.createAction

Key Differences:
  • Verification count: TS has 1, PY has 0

---

## Test 42: should fail if protocol name is admin-reserved and caller is not admin **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should fail if protocol name is admin-reserved and caller is not admin', async () => {
      // admin-reserved means protocol name starts with "admin" or "p ".
      manager = new WalletPermissionsManager(underlying, 'secure.admin.com')

      // Non-admin tries to do e.g. `createHmac` with protocol name "admin super-secret"
      await expect(
        manager.createHmac(
          {
            protocolID: [1, 'admin super-secret'],
            data: [0x01, 0x02],
            keyID: '1'
          },
          'not-an-admin.com'
        )
      ).rejects.toThrow(/admin-only/i)

      // Underlying call never invoked
      expect(underlying.createHmac).toHaveBeenCalledTimes(0)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_fail_if_protocol_name_is_admin_reserved_and_caller_is_not_admin(self) -> None:
        """Given: Manager with admin-reserved protocol
           When: Non-admin tries to use admin-reserved protocol
           Then: Operation fails

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
                   test('should fail if protocol name is admin-reserved and caller is not admin')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_hmac = AsyncMock()

        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet, admin_originator="secure.admin.com"
        )

        # When/Then - admin-reserved protocol name
        with pytest.raises(ValueError, match="admin-only"):
            manager.create_hmac(
                {"protocolID": [1, "admin super-secret"], "data": [0x01, 0x02], "keyID": "1"},
                originator="not-an-admin.com",
            )

        # Underlying never called
        mock_underlying_wallet.create_hmac.assert_not_called()
```

### AI Analysis Results

**Similarity Score**: 50.00%
  - Structural: 0.00%
  - Semantic: 40.00%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createHmac

**Suggestions:**
  - Add verifications for: underlying.createHmac

**Explanation:**

Overall Similarity: 50.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 40.0% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: verification method_call_verification
  • Python: verification method_call_verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: underlying.createHmac

---

## Test 43: should fail immediately if using an admin-only basket as non-admin **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should fail immediately if using an admin-only basket as non-admin', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com')
      // Attempt to createAction to insert into "admin secret-basket" from a non-admin origin
      await expect(
        manager.createAction(
          {
            description: 'Insert into admin basket',
            outputs: [
              {
                lockingScript: 'abcd',
                satoshis: 100,
                basket: 'admin secret-basket',
                outputDescription: 'Nothing to see  here'
              }
            ]
          },
          'non-admin.com'
        )
      ).rejects.toThrow(/admin-only/i)

      // Underlying createAction never called
      expect(underlying.createAction).toHaveBeenCalledTimes(0)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_fail_immediately_if_using_an_admin_only_basket_as_non_admin(self) -> None:
        """Given: Non-admin originator
           When: Attempt to use admin-only basket
           Then: Fails immediately

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
                   test('should fail immediately if using an admin-only basket as non-admin')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_action = AsyncMock()

        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.com")

        # When/Then - admin basket from non-admin
        with pytest.raises(ValueError, match="admin-only"):
            manager.create_action(
                {
                    "description": "Insert into admin basket",
                    "outputs": [
                        {
                            "lockingScript": "abcd",
                            "satoshis": 100,
                            "basket": "admin secret-basket",
                            "outputDescription": "Nothing to see here",
                        }
                    ],
                },
                originator="non-admin.com",
            )

        # Underlying never called
        mock_underlying_wallet.create_action.assert_not_called()
```

### AI Analysis Results

**Similarity Score**: 50.00%
  - Structural: 0.00%
  - Semantic: 40.00%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createAction

**Suggestions:**
  - Add verifications for: underlying.createAction

**Explanation:**

Overall Similarity: 50.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 40.0% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: verification method_call_verification
  • Python: verification method_call_verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: underlying.createAction

---

## Test 44: should fail immediately if using the reserved basket **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should fail immediately if using the reserved basket "default" as non-admin', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com')
      await expect(
        manager.createAction(
          {
            description: 'Insert to default basket',
            outputs: [
              {
                lockingScript: '0x1234',
                satoshis: 1,
                basket: 'default',
                outputDescription: 'Nothing to see here'
              }
            ]
          },
          'some-nonadmin.com'
        )
      ).rejects.toThrow(/admin-only/i)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_fail_immediately_if_using_the_reserved_basket_default_as_non_admin(self) -> None:
        """Given: Non-admin originator
           When: Attempt to use 'default' basket
           Then: Fails immediately

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
                   test('should fail immediately if using the reserved basket "default" as non-admin')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_action = AsyncMock()

        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.com")

        # When/Then - 'default' basket from non-admin
        with pytest.raises(ValueError, match="admin-only"):
            manager.create_action(
                {
                    "description": "Insert to default basket",
                    "outputs": [
                        {
                            "lockingScript": "0x1234",
                            "satoshis": 1,
                            "basket": "default",
                            "outputDescription": "Nothing to see here",
                        }
                    ],
                },
                originator="some-nonadmin.com",
            )

        mock_underlying_wallet.create_action.assert_not_called()
```

### AI Analysis Results

**Similarity Score**: 43.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 100.00%

**Differences:**
  - Verification count: TS has 0, PY has 1

**Explanation:**

Overall Similarity: 43.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: verification
  • Python: verification method_call_verification

Key Differences:
  • Verification count: TS has 0, PY has 1

---

## Test 45: should ignore `privileged=true` if differentiatePrivilegedOperations=false **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should ignore `privileged=true` if differentiatePrivilegedOperations=false', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {
        differentiatePrivilegedOperations: false, // Forces privileged usage to be treated as non-privileged
        seekProtocolPermissionsForSigning: true
      })

      // Because we treat privileged as false, the permission request does not need privileged credentials.
      manager.bindCallback('onProtocolPermissionRequested', async req => {
        await manager.grantPermission({
          requestID: req.requestID,
          ephemeral: true
        })
      })

      await expect(
        manager.createSignature(
          {
            protocolID: [1, 'some-protocol'],
            privileged: true, // This flag will be ignored
            data: [0x99],
            keyID: 'keyXYZ'
          },
          'nonadmin.com'
        )
      ).resolves.not.toThrow()
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_ignore_privileged_true_if_differentiateprivilegedoperations_false(self) -> None:
        """Given: Manager with differentiatePrivilegedOperations=false
           When: Request with privileged=true
           Then: Privileged flag ignored, treated as normal

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
                   test('should ignore `privileged=true` if differentiatePrivilegedOperations=false')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_signature = AsyncMock(return_value={"signature": [0x99]})

        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"differentiatePrivilegedOperations": False, "seekProtocolPermissionsForSigning": True},
        )

        async def permission_callback(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onProtocolPermissionRequested", permission_callback)

        # When - privileged flag is ignored
        manager.create_signature(
            {"protocolID": [1, "some-protocol"], "privileged": True, "data": [0x99], "keyID": "keyXYZ"},
            originator="nonadmin.com",
        )

        # Then - succeeds without special privileged handling
        mock_underlying_wallet.create_signature.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing operations: manager.grantPermission

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 0, PY has 1

**Suggestions:**
  - Add operations: manager.grantPermission

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification
  • Python: verification method_call_verification

Critical Issues (1):
  • [HIGH] Python test is missing operations: manager.grantPermission

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 0, PY has 1

---

## Test 46: should pass if usage plus new spend is within the monthly limit **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should pass if usage plus new spend is within the monthly limit', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {})

      // existing DSAP token with authorizedAmount=1000
      const dsapToken: PermissionToken = {
        tx: [],
        txid: 'dsap123',
        outputIndex: 0,
        outputScript: '9218',
        satoshis: 1,
        originator: 'shopper.com',
        authorizedAmount: 1000,
        expiry: 0
      }
      jest.spyOn(manager as any, 'findSpendingToken').mockResolvedValue(dsapToken)

      // Suppose they've spent 200 so far
      jest.spyOn(manager as any, 'querySpentSince').mockResolvedValue(200)

      // Attempt new spending of 500 => total=700 which is <= 1000 => no prompt
      await manager.createAction(
        {
          description: 'Spend 500 sats',
          outputs: [
            {
              outputDescription: 'Nothing to see here',
              lockingScript: '0abc',
              satoshis: 500
            }
          ]
        },
        'shopper.com'
      )
      // Success, no new permission requested
      const activeRequests = (manager as any).activeRequests as Map<string, any>
      expect(activeRequests.size).toBe(0)

      expect(underlying.createAction).toHaveBeenCalledTimes(1)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_pass_if_usage_plus_new_spend_is_within_the_monthly_limit(self) -> None:
        """Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
        test('should pass if usage plus new spend is within the monthly limit')"""
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_action = AsyncMock(
            return_value={"signableTransaction": {"tx": [0x00], "reference": "ref1"}}
        )
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"seekSpendingPermissions": True},
        )
        existing_token = {
            "txid": "spend-token",
            "outputIndex": 0,
            "originator": "user.com",
            "expiry": 9999999999,
            "privileged": False,
            "monthlyLimit": 1000,
            "usage": 500,
        }
        manager._find_spending_token = AsyncMock(return_value=existing_token)
        manager.create_action(
            {
                "description": "Spend 100 sats",
                "outputs": [{"lockingScript": "abcd", "satoshis": 100, "outputDescription": "test"}],
            },
            originator="user.com",
        )
        mock_underlying_wallet.create_action.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 17.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createAction, active_requests.size
  - [HIGH] Python test is missing operations: manager.createAction

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: underlying.createAction, active_requests.size
  - Add operations: manager.createAction

**Explanation:**

Overall Similarity: 17.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification token_operation verification method_call_verification
  • Python: token_operation verification method_call_verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.createAction, active_requests.size
  • [HIGH] Python test is missing operations: manager.createAction

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 47: should prompt for insertion permission if seekBasketInsertionPermissions=true **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should prompt for insertion permission if seekBasketInsertionPermissions=true', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {
        seekBasketInsertionPermissions: true
      })

      // auto-grant ephemeral
      manager.bindCallback('onBasketAccessRequested', async req => {
        await manager.grantPermission({
          requestID: req.requestID,
          ephemeral: true
        })
      })

      // Also auto-grant unrelated spending authorization (since this is createAction)
      manager.bindCallback('onSpendingAuthorizationRequested', async req => {
        await manager.grantPermission({
          requestID: req.requestID,
          ephemeral: true
        })
      })

      await expect(
        manager.createAction(
          {
            description: 'Insert to user-basket',
            outputs: [
              {
                lockingScript: '7812',
                satoshis: 1,
                basket: 'user-basket',
                outputDescription: 'Nothing to see here'
              }
            ]
          },
          'some-nonadmin.com'
        )
      ).resolves.not.toThrow()

      // Confirm underlying createAction was eventually invoked
      expect(underlying.createAction).toHaveBeenCalledTimes(1)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_prompt_for_insertion_permission_if_seekbasketinsertionpermissions_true(self) -> None:
        """Given: Manager with seekBasketInsertionPermissions=true
           When: Create action with basket
           Then: Permission prompt triggered

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
                   test('should prompt for insertion permission if seekBasketInsertionPermissions=true')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_action = AsyncMock(return_value={"txid": "abc123"})

        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"seekBasketInsertionPermissions": True},
        )

        # Auto-grant basket access
        async def basket_callback(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onBasketAccessRequested", basket_callback)

        # Auto-grant spending authorization
        async def spending_callback(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onSpendingAuthorizationRequested", spending_callback)

        # When
        manager.create_action(
            {
                "description": "Insert to user-basket",
                "outputs": [
                    {
                        "lockingScript": "7812",
                        "satoshis": 1,
                        "basket": "user-basket",
                        "outputDescription": "Nothing to see here",
                    }
                ],
            },
            originator="some-nonadmin.com",
        )

        # Then - underlying called
        mock_underlying_wallet.create_action.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 20.00%
  - Structural: 0.00%
  - Semantic: 40.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createAction
  - [HIGH] Python test is missing operations: manager.grantPermission

**Differences:**
  - Operation count: TS has 2, PY has 0

**Suggestions:**
  - Add verifications for: underlying.createAction
  - Add operations: manager.grantPermission

**Explanation:**

Overall Similarity: 20.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 40.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification method_call_verification
  • Python: verification method_call_verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.createAction
  • [HIGH] Python test is missing operations: manager.grantPermission

Key Differences:
  • Operation count: TS has 2, PY has 0

---

## Test 48: should prompt for label usage if seekPermissionWhenApplyingActionLabels=true **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should prompt for label usage if seekPermissionWhenApplyingActionLabels=true', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {
        seekPermissionWhenApplyingActionLabels: true
      })

      manager.bindCallback('onProtocolPermissionRequested', async req => {
        // This request will have protocolID=[1, "action label <label>"], etc.
        await manager.grantPermission({
          requestID: req.requestID,
          ephemeral: true
        })
      })

      await manager.createAction(
        {
          description: 'Add label "user-label-123"',
          labels: ['user-label-123']
        },
        'nonadmin.com'
      )

      // Underlying is called
      expect(underlying.createAction).toHaveBeenCalledTimes(1)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_prompt_for_label_usage_if_seekpermissionwhenapplyingactionlabels_true(self) -> None:
        """Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
        test('should prompt for label usage if seekPermissionWhenApplyingActionLabels=true')"""
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_action = AsyncMock(return_value={"txid": "test"})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"seekPermissionWhenApplyingActionLabels": True, "seekSpendingPermissions": False},
        )

        async def permission_callback(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onLabelPermissionRequested", permission_callback)
        manager.create_action(
            {"description": "test", "labels": ["user-label"], "outputs": [{"lockingScript": "abcd", "satoshis": 100}]},
            originator="user.com",
        )
        mock_underlying_wallet.create_action.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 20.00%
  - Structural: 0.00%
  - Semantic: 40.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createAction
  - [HIGH] Python test is missing operations: manager.createAction, manager.grantPermission

**Differences:**
  - Operation count: TS has 2, PY has 0

**Suggestions:**
  - Add verifications for: underlying.createAction
  - Add operations: manager.createAction, manager.grantPermission

**Explanation:**

Overall Similarity: 20.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 40.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification method_call_verification
  • Python: verification method_call_verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.createAction
  • [HIGH] Python test is missing operations: manager.createAction, manager.grantPermission

Key Differences:
  • Operation count: TS has 2, PY has 0

---

## Test 49: should prompt for protocol usage if securityLevel=1 and no existing token **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should prompt for protocol usage if securityLevel=1 and no existing token', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {
        seekProtocolPermissionsForSigning: true
      })

      // We'll bind a callback that grants ephemeral permission automatically
      manager.bindCallback('onProtocolPermissionRequested', async request => {
        // For tests, automatically grant ephemeral permission
        await manager.grantPermission({
          requestID: request.requestID,
          ephemeral: true
        })
      })

      // Because secLevel=1, we need a valid DPACP token
      // We have no token => manager triggers a request => callback grants ephemeral => passes
      await expect(
        manager.createSignature(
          {
            protocolID: [1, 'test-protocol'],
            data: [0x99, 0xaa],
            keyID: '1'
          },
          'some-nonadmin.com'
        )
      ).resolves.not.toThrow()

      // The underlying signature should succeed
      expect(underlying.createSignature).toHaveBeenCalledTimes(1)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_prompt_for_protocol_usage_if_securitylevel_1_and_no_existing_token(self) -> None:
        """Given: Manager with no existing token
           When: Call with securityLevel=1
           Then: Permission prompt triggered

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
                   test('should prompt for protocol usage if securityLevel=1 and no existing token')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_signature = AsyncMock(return_value={"signature": [0x99, 0xAA]})

        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"seekProtocolPermissionsForSigning": True},
        )

        # Auto-grant ephemeral permission
        async def permission_callback(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onProtocolPermissionRequested", permission_callback)

        # When - createSignature with secLevel=1
        manager.create_signature(
            {"protocolID": [1, "test-protocol"], "data": [0x99, 0xAA], "keyID": "1"}, originator="some-nonadmin.com"
        )

        # Then - underlying signature called
        mock_underlying_wallet.create_signature.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 20.00%
  - Structural: 0.00%
  - Semantic: 40.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createSignature
  - [HIGH] Python test is missing operations: manager.grantPermission

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: underlying.createSignature
  - Add operations: manager.grantPermission

**Explanation:**

Overall Similarity: 20.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 40.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: token_operation verification method_call_verification
  • Python: token_operation verification method_call_verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.createSignature
  • [HIGH] Python test is missing operations: manager.grantPermission

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 50: should prompt for removal permission if seekBasketRemovalPermissions=true **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should prompt for removal permission if seekBasketRemovalPermissions=true', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {
        seekBasketRemovalPermissions: true
      })
      manager.bindCallback('onBasketAccessRequested', async req => {
        // auto-grant ephemeral
        await manager.grantPermission({
          requestID: req.requestID,
          ephemeral: true
        })
      })

      await expect(
        manager.relinquishOutput(
          {
            output: 'someTxid.1',
            basket: 'user-basket'
          },
          'some-user.com'
        )
      ).resolves.not.toThrow()

      expect(underlying.relinquishOutput).toHaveBeenCalledTimes(1)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_prompt_for_removal_permission_if_seekbasketremovalpermissions_true(self) -> None:
        """Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
        test('should prompt for removal permission if seekBasketRemovalPermissions=true')"""
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.relinquish_output = AsyncMock(return_value={"txid": "test"})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"seekBasketRemovalPermissions": True},
        )

        async def permission_callback(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onBasketAccessRequested", permission_callback)
        manager.relinquish_output({"output": "someTxid.1", "basket": "user-basket"}, originator="some-user.com")
        mock_underlying_wallet.relinquish_output.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 20.00%
  - Structural: 0.00%
  - Semantic: 40.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.relinquishOutput
  - [HIGH] Python test is missing operations: manager.grantPermission

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: underlying.relinquishOutput
  - Add operations: manager.grantPermission

**Explanation:**

Overall Similarity: 20.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 40.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification method_call_verification
  • Python: verification method_call_verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.relinquishOutput
  • [HIGH] Python test is missing operations: manager.grantPermission

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 51: should prompt for renewal if token is expired **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should prompt for renewal if token is expired', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {
        seekCertificateDisclosurePermissions: true
      })

      // Mock an expired token
      const expiredCertToken: PermissionToken = {
        tx: [],
        txid: 'old-expired',
        outputIndex: 0,
        outputScript: 'deadbeef',
        satoshis: 1,
        originator: 'app.com',
        expiry: 1,
        privileged: false,
        certType: 'KYC',
        certFields: ['name', 'dob'],
        verifier: '02verifier'
      }
      jest.spyOn(manager as any, 'findCertificateToken').mockResolvedValue(expiredCertToken)

      // Callback that grants renewal ephemeral
      manager.bindCallback('onCertificateAccessRequested', async req => {
        expect(req.renewal).toBe(true)
        await manager.grantPermission({
          requestID: req.requestID,
          ephemeral: true
        })
      })

      await manager.proveCertificate(
        {
          certificate: {
            type: 'KYC',
            fields: { name: 'Bob', dob: '1970' },
            certifier: '02verifier'
          },
          fieldsToReveal: ['name'],
          verifier: '02verifier',
          privileged: false
        },
        'app.com'
      )
      // Succeeds after ephemeral renewal
      expect(underlying.proveCertificate).toHaveBeenCalledTimes(1)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_prompt_for_renewal_if_token_is_expired_cert(self) -> None:
        """Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
        test('should prompt for renewal if token is expired')"""
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.prove_certificate = AsyncMock(return_value={"keyring": {}})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"seekCertificateDisclosurePermissions": True},
        )
        expired_token = {
            "txid": "old-expired",
            "outputIndex": 0,
            "originator": "app.com",
            "expiry": 1,
            "privileged": False,
            "certType": "KYC",
            "certFields": ["name", "dob"],
            "verifier": "02verifier",
        }
        manager._find_certificate_token = AsyncMock(return_value=expired_token)

        async def permission_callback(request) -> None:
            assert request["renewal"] is True
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onCertificateAccessRequested", permission_callback)
        manager.prove_certificate(
            {
                "certificate": {"type": "KYC", "fields": {"name": "Bob", "dob": "1970"}, "certifier": "02verifier"},
                "fieldsToReveal": ["name"],
                "verifier": "02verifier",
                "privileged": False,
            },
            originator="app.com",
        )
        mock_underlying_wallet.prove_certificate.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 17.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.proveCertificate, req.renewal
  - [HIGH] Python test is missing operations: manager.grantPermission, manager.proveCertificate

**Differences:**
  - Operation count: TS has 2, PY has 0

**Suggestions:**
  - Add verifications for: underlying.proveCertificate, req.renewal
  - Add operations: manager.grantPermission, manager.proveCertificate

**Explanation:**

Overall Similarity: 17.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification token_operation verification method_call_verification
  • Python: token_operation verification method_call_verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.proveCertificate, req.renewal
  • [HIGH] Python test is missing operations: manager.grantPermission, manager.proveCertificate

Key Differences:
  • Operation count: TS has 2, PY has 0

---

## Test 52: should prompt for renewal if token is found but expired **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should prompt for renewal if token is found but expired', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {})

      // Suppose the user already had a token but it’s expired. We mock `findProtocolToken` so that
      // it returns an expired token, forcing a renewal request.
      const expiredToken: PermissionToken = {
        tx: [],
        txid: 'oldtxid123',
        outputIndex: 0,
        outputScript: 'deadbeef',
        satoshis: 1,
        originator: 'some-nonadmin.com',
        expiry: 1, // definitely in the past
        privileged: false,
        securityLevel: 1,
        protocol: 'test-protocol',
        counterparty: 'self'
      }
      jest.spyOn(manager as any, 'findProtocolToken').mockResolvedValue(expiredToken)

      // We'll bind a callback that grants a renewal ephemeral
      manager.bindCallback('onProtocolPermissionRequested', async req => {
        expect(req.renewal).toBe(true)
        expect(req.previousToken).toEqual(expiredToken)
        await manager.grantPermission({
          requestID: req.requestID,
          ephemeral: true
        })
      })

      // Now call an operation that requires protocol usage
      await manager.createSignature(
        {
          protocolID: [1, 'test-protocol'],
          data: [0xfe],
          keyID: '1'
        },
        'some-nonadmin.com'
      )
      // Should succeed after renewal
      expect(underlying.createSignature).toHaveBeenCalledTimes(1)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_prompt_for_renewal_if_token_is_found_but_expired(self) -> None:
        """Given: Manager with expired token
           When: Request operation
           Then: Renewal prompt triggered

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
                   test('should prompt for renewal if token is found but expired')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_signature = AsyncMock(return_value={"signature": [0xFE]})

        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.com")

        # Mock expired token
        expired_token = {
            "tx": [],
            "txid": "oldtxid123",
            "outputIndex": 0,
            "outputScript": "deadbeef",
            "satoshis": 1,
            "originator": "some-nonadmin.com",
            "expiry": 1,  # Past timestamp
            "privileged": False,
            "securityLevel": 1,
            "protocol": "test-protocol",
            "counterparty": "self",
        }

        # Mock findProtocolToken to return expired token
        manager._find_protocol_token = AsyncMock(return_value=expired_token)

        # Bind callback that grants renewal
        async def permission_callback(request) -> None:
            assert request["renewal"] is True
            assert request["previousToken"] == expired_token
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onProtocolPermissionRequested", permission_callback)

        # When - call with expired token
        manager.create_signature(
            {"protocolID": [1, "test-protocol"], "data": [0xFE], "keyID": "1"}, originator="some-nonadmin.com"
        )

        # Then - underlying called after renewal
        mock_underlying_wallet.create_signature.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 17.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: req.renewal, req.previousToken, underlying.createSignature
  - [HIGH] Python test is missing operations: manager.createSignature, manager.grantPermission

**Differences:**
  - Operation count: TS has 2, PY has 0

**Suggestions:**
  - Add verifications for: req.renewal, req.previousToken, underlying.createSignature
  - Add operations: manager.createSignature, manager.grantPermission

**Explanation:**

Overall Similarity: 17.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification token_operation verification method_call_verification
  • Python: token_operation verification method_call_verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: req.renewal, req.previousToken, underlying.createSignature
  • [HIGH] Python test is missing operations: manager.createSignature, manager.grantPermission

Key Differences:
  • Operation count: TS has 2, PY has 0

---

## Test 53: should require listing permission if seekBasketListingPermissions=true and no token **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should require listing permission if seekBasketListingPermissions=true and no token', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {
        seekBasketListingPermissions: true
      })

      manager.bindCallback('onBasketAccessRequested', async req => {
        // Deny for test
        manager.denyPermission(req.requestID)
      })

      // Attempt to list a user basket
      await expect(manager.listOutputs({ basket: 'user-basket' }, 'some-user.com')).rejects.toThrow(/Permission denied/)

      // There is one underlying call: internally, we called listOutputs to check if we had permission
      // (we did not, we sought it, and the user denied). So we see this call here, but we DO NOT see
      // the actual proxied call (for listing outputs in user-basket), since it was denied.
      expect(underlying.listOutputs).toHaveBeenCalledTimes(1)
      expect(underlying.listOutputs).toHaveBeenLastCalledWith(
        {
          basket: 'admin basket-access',
          include: 'entire transactions',
          tagQueryMode: 'all',
          tags: ['originator some-user.com', 'basket user-basket']
        },
        'admin.com'
      )
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_require_listing_permission_if_seekbasketlistingpermissions_true_and_no_token(self) -> None:
        """Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
        test('should require listing permission if seekBasketListingPermissions=true and no token')"""
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.list_outputs = AsyncMock()
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"seekBasketListingPermissions": True},
        )

        def permission_callback(request) -> None:
            manager.deny_permission(request["requestID"])

        manager.bind_callback("onBasketAccessRequested", permission_callback)
        with pytest.raises(ValueError, match="Permission denied"):
            manager.list_outputs({"basket": "user-basket"}, originator="some-user.com")
```

### AI Analysis Results

**Similarity Score**: 40.00%
  - Structural: 0.00%
  - Semantic: 20.00%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.listOutputs

**Differences:**
  - Verification count: TS has 2, PY has 0

**Suggestions:**
  - Add verifications for: underlying.listOutputs

**Explanation:**

Overall Similarity: 40.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 20.0% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: token_operation verification method_call_verification
  • Python: token_operation

Critical Issues (1):
  • [HIGH] Python test is missing verifications: underlying.listOutputs

Key Differences:
  • Verification count: TS has 2, PY has 0

---

## Test 54: should require permission if seekCertificateDisclosurePermissions=true, no valid token **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should require permission if seekCertificateDisclosurePermissions=true, no valid token', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {
        seekCertificateDisclosurePermissions: true
      })

      // Auto-grant ephemeral for test
      manager.bindCallback('onCertificateAccessRequested', async req => {
        await manager.grantPermission({
          requestID: req.requestID,
          ephemeral: true
        })
      })

      // Because we don't have a stored token, it triggers request -> ephemeral granted -> success
      await manager.proveCertificate(
        {
          certificate: {
            type: 'KYC',
            subject: '02abc..',
            serialNumber: 'xyz',
            certifier: '02dddd...',
            fields: { name: 'Bob', nationality: 'Mars' }
          },
          fieldsToReveal: ['name'],
          verifier: '02xxxx..',
          privileged: false
        },
        'some-user.com'
      )

      expect(underlying.proveCertificate).toHaveBeenCalledTimes(1)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_require_permission_if_seekcertificatedisclosurepermissions_true_no_valid_token(self) -> None:
        """Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
        test('should require permission if seekCertificateDisclosurePermissions=true, no valid token')"""
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.prove_certificate = AsyncMock(return_value={"keyring": {}})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"seekCertificateDisclosurePermissions": True},
        )

        async def permission_callback(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onCertificateAccessRequested", permission_callback)
        manager.prove_certificate(
            {
                "certificate": {
                    "type": "KYC",
                    "subject": "02abc",
                    "serialNumber": "xyz",
                    "certifier": "02dddd",
                    "fields": {"name": "Bob"},
                },
                "fieldsToReveal": ["name"],
                "verifier": "02xxxx",
                "privileged": False,
            },
            originator="some-user.com",
        )
        mock_underlying_wallet.prove_certificate.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 20.00%
  - Structural: 0.00%
  - Semantic: 40.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.proveCertificate
  - [HIGH] Python test is missing operations: manager.grantPermission, manager.proveCertificate

**Differences:**
  - Operation count: TS has 2, PY has 0

**Suggestions:**
  - Add verifications for: underlying.proveCertificate
  - Add operations: manager.grantPermission, manager.proveCertificate

**Explanation:**

Overall Similarity: 20.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 40.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: token_operation verification method_call_verification
  • Python: token_operation verification method_call_verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.proveCertificate
  • [HIGH] Python test is missing operations: manager.grantPermission, manager.proveCertificate

Key Differences:
  • Operation count: TS has 2, PY has 0

---

## Test 55: should require spending token if netSpent > 0 and seekSpendingPermissions=true **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should require spending token if netSpent > 0 and seekSpendingPermissions=true', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {
        seekSpendingPermissions: true
      })

      // We’ll also mock the signableTransaction return to help manager compute netSpent
      underlying.createAction.mockResolvedValueOnce({
        signableTransaction: {
          tx: [0x00], // minimal
          reference: 'ref1'
        }
      })
      // The manager tries to parse the transaction to find netSpent.
      // By default, netSpent = totalOutput + fee - totalExplicitInputs
      // We haven't provided any explicit inputs in the createAction call, so netSpent = 200 + fee

      // Auto-grant ephemeral for test
      manager.bindCallback('onSpendingAuthorizationRequested', async req => {
        await manager.grantPermission({
          requestID: req.requestID,
          ephemeral: true,
          amount: 1000
        })
      })

      await expect(
        manager.createAction(
          {
            description: 'Spend 200 sats with no input from user',
            outputs: [
              {
                outputDescription: 'Nothing to see here',
                lockingScript: '1abc',
                satoshis: 200
              }
            ]
          },
          'some-user.com'
        )
      ).resolves.not.toThrow()

      // underlying createAction called
      expect(underlying.createAction).toHaveBeenCalledTimes(1)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_require_spending_token_if_netspent_gt_0_and_seekspendingpermissions_true(self) -> None:
        """Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
        test('should require spending token if netSpent > 0 and seekSpendingPermissions=true')"""
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_action = AsyncMock(
            return_value={"signableTransaction": {"tx": [0x00], "reference": "ref1"}}
        )
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"seekSpendingPermissions": True},
        )

        async def permission_callback(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onSpendingAuthorizationRequested", permission_callback)
        manager.create_action(
            {
                "description": "Spend 200 sats",
                "outputs": [{"lockingScript": "abcd", "satoshis": 200, "outputDescription": "test"}],
            },
            originator="user.com",
        )
        mock_underlying_wallet.create_action.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 17.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createAction
  - [HIGH] Python test is missing operations: manager.grantPermission

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: underlying.createAction
  - Add operations: manager.grantPermission

**Explanation:**

Overall Similarity: 17.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: authentication token_operation verification method_call_verification
  • Python: token_operation verification method_call_verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.createAction
  • [HIGH] Python test is missing operations: manager.grantPermission

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 56: should skip certificate disclosure permission if config.seekCertificateDisclosurePermissions=false **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should skip certificate disclosure permission if config.seekCertificateDisclosurePermissions=false', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {
        seekCertificateDisclosurePermissions: false
      })
      // Directly call proveCertificate with no token => no prompt => immediate success
      await expect(
        manager.proveCertificate(
          {
            certificate: {
              type: 'KYC',
              subject: '02abcdef...',
              serialNumber: '123',
              certifier: '02ccc...',
              fields: { name: 'Alice', dob: '2000-01-01' }
            },
            fieldsToReveal: ['name'],
            verifier: '02xyz...',
            privileged: false
          },
          'nonadmin.com'
        )
      ).resolves.not.toThrow()

      expect(underlying.proveCertificate).toHaveBeenCalledTimes(1)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_skip_certificate_disclosure_permission_if_config_seekcertificatedisclosurepermissions_false(
        self,
    ) -> None:
        """Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
        test('should skip certificate disclosure permission if config.seekCertificateDisclosurePermissions=false')"""
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.prove_certificate = AsyncMock(return_value={"keyring": {}})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"seekCertificateDisclosurePermissions": False},
        )
        manager.prove_certificate(
            {
                "certificate": {
                    "type": "KYC",
                    "subject": "02abcdef",
                    "serialNumber": "123",
                    "certifier": "02ccc",
                    "fields": {"name": "Alice"},
                },
                "fieldsToReveal": ["name"],
                "verifier": "02xyz",
                "privileged": False,
            },
            originator="nonadmin.com",
        )
        mock_underlying_wallet.prove_certificate.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 46.00%
  - Structural: 0.00%
  - Semantic: 32.00%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.proveCertificate

**Suggestions:**
  - Add verifications for: underlying.proveCertificate

**Explanation:**

Overall Similarity: 46.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 32.0% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: token_operation verification method_call_verification
  • Python: verification method_call_verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: underlying.proveCertificate

---

## Test 57: should skip if seekSpendingPermissions=false **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should skip if seekSpendingPermissions=false', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {
        seekSpendingPermissions: false
      })

      // createAction that tries to net spend 200 sats
      const result = await manager.createAction(
        {
          description: 'Some spend transaction',
          outputs: [
            {
              lockingScript: '1321',
              satoshis: 200,
              outputDescription: 'Nothing to see here'
            }
          ]
        },
        'user.com'
      )

      // No prompt triggered
      const activeRequests = (manager as any).activeRequests as Map<string, any>
      expect(activeRequests.size).toBe(0)

      // Underlying createAction definitely called
      expect(underlying.createAction).toHaveBeenCalledTimes(1)
      // If seekSpendingPermissions=false, the result should NOT? contain the signableTransaction
      expect(result.signableTransaction).not.toBeDefined()
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_skip_if_seekspendingpermissions_false(self) -> None:
        """Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
        test('should skip if seekSpendingPermissions=false')"""
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_action = AsyncMock(return_value={"txid": "test123"})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"seekSpendingPermissions": False},
        )
        manager.create_action(
            {
                "description": "Some spend transaction",
                "outputs": [{"lockingScript": "1321", "satoshis": 200, "outputDescription": "Nothing to see here"}],
            },
            originator="user.com",
        )
        active_requests = getattr(manager, "_active_requests", {})
        assert len(active_requests) == 0
        mock_underlying_wallet.create_action.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 16.00%
  - Structural: 0.00%
  - Semantic: 32.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createAction, active_requests.size
  - [HIGH] Python test is missing operations: manager.createAction

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: underlying.createAction, active_requests.size
  - Add operations: manager.createAction

**Explanation:**

Overall Similarity: 16.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 32.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification method_call_verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.createAction, active_requests.size
  • [HIGH] Python test is missing operations: manager.createAction

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 58: should skip insertion permission if seekBasketInsertionPermissions=false **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should skip insertion permission if seekBasketInsertionPermissions=false', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {
        seekBasketInsertionPermissions: false
      })

      // Auto-grant unrelated spending authorization (since this is createAction)
      manager.bindCallback('onSpendingAuthorizationRequested', async req => {
        await manager.grantPermission({
          requestID: req.requestID,
          ephemeral: true
        })
      })

      await manager.createAction(
        {
          description: 'Insert to user-basket',
          outputs: [
            {
              lockingScript: '1234',
              satoshis: 1,
              basket: 'some-basket',
              outputDescription: 'Nothing to see here'
            }
          ]
        },
        'nonadmin.com'
      )
      // No requests queued, underlying is called
      const activeRequests = (manager as any).activeRequests as Map<string, any>
      expect(activeRequests.size).toBe(0)
      expect(underlying.createAction).toHaveBeenCalledTimes(1)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_skip_insertion_permission_if_seekbasketinsertionpermissions_false(self) -> None:
        """Given: Manager with seekBasketInsertionPermissions=false
           When: Create action with basket
           Then: No basket permission prompt

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
                   test('should skip insertion permission if seekBasketInsertionPermissions=false')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_action = AsyncMock(return_value={"txid": "xyz789"})

        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"seekBasketInsertionPermissions": False},
        )

        # Auto-grant spending authorization only
        async def spending_callback(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onSpendingAuthorizationRequested", spending_callback)

        # When
        manager.create_action(
            {
                "description": "Insert to user-basket",
                "outputs": [
                    {
                        "lockingScript": "1234",
                        "satoshis": 1,
                        "basket": "some-basket",
                        "outputDescription": "Nothing to see here",
                    }
                ],
            },
            originator="some-nonadmin.com",
        )

        # Then - no basket permission check, underlying called
        mock_underlying_wallet.create_action.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 16.00%
  - Structural: 0.00%
  - Semantic: 32.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createAction, active_requests.size
  - [HIGH] Python test is missing operations: manager.createAction, manager.grantPermission

**Differences:**
  - Operation count: TS has 2, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: underlying.createAction, active_requests.size
  - Add operations: manager.createAction, manager.grantPermission

**Explanation:**

Overall Similarity: 16.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 32.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification method_call_verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.createAction, active_requests.size
  • [HIGH] Python test is missing operations: manager.createAction, manager.grantPermission

Key Differences:
  • Operation count: TS has 2, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 59: should skip label permission if seekPermissionWhenApplyingActionLabels=false **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should skip label permission if seekPermissionWhenApplyingActionLabels=false', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {
        seekPermissionWhenApplyingActionLabels: false
      })

      // Non-admin applies label "my-app-label"
      await expect(
        manager.createAction({ description: 'Add label', labels: ['my-app-label'] }, 'some-app.com')
      ).resolves.not.toThrow()

      // No prompt
      const activeRequests = (manager as any).activeRequests as Map<string, any>
      expect(activeRequests.size).toBe(0)

      // Called underlying
      expect(underlying.createAction).toHaveBeenCalledTimes(1)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_skip_label_permission_if_seekpermissionwhenapplyingactionlabels_false(self) -> None:
        """Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
        test('should skip label permission if seekPermissionWhenApplyingActionLabels=false')"""
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_action = AsyncMock(return_value={"txid": "test"})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"seekPermissionWhenApplyingActionLabels": False, "seekSpendingPermissions": False},
        )
        manager.create_action(
            {"description": "test", "labels": ["user-label"], "outputs": [{"lockingScript": "abcd", "satoshis": 100}]},
            originator="user.com",
        )
        mock_underlying_wallet.create_action.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 46.00%
  - Structural: 0.00%
  - Semantic: 32.00%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createAction, active_requests.size

**Differences:**
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: underlying.createAction, active_requests.size

**Explanation:**

Overall Similarity: 46.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 32.0% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification method_call_verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: underlying.createAction, active_requests.size

Key Differences:
  • Verification count: TS has 2, PY has 1

---

## Test 60: should skip permission prompt if secLevel=0 (open usage) **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts

```typescript
    it('should skip permission prompt if secLevel=0 (open usage)', async () => {
      manager = new WalletPermissionsManager(underlying, 'admin.com', {
        seekProtocolPermissionsForSigning: true // Typically enforced
      })

      // Attempt createSignature with protocolID=[0, "someProtocol"]
      // Because securityLevel=0, the manager should skip checks
      await expect(
        manager.createSignature(
          {
            protocolID: [0, 'open-protocol'],
            data: [0x01, 0x02],
            keyID: '1'
          },
          'some-user.com'
        )
      ).resolves.not.toThrow()

      // No permission request
      const activeRequests = (manager as any).activeRequests as Map<string, any>
      expect(activeRequests.size).toBe(0)

      // Underlying createSignature called once
      expect(underlying.createSignature).toHaveBeenCalledTimes(1)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_checks.py

```python
    def test_should_skip_permission_prompt_if_seclevel_0_open_usage(self) -> None:
        """Given: Manager with seekProtocolPermissionsForSigning enabled
           When: Call createSignature with secLevel=0
           Then: No permission prompt, operation succeeds

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.checks.test.ts
                   test('should skip permission prompt if secLevel=0 (open usage)')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_signature = AsyncMock(return_value={"signature": [0x01, 0x02]})

        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.com",
            config={"seekProtocolPermissionsForSigning": True},
        )

        # When - createSignature with protocolID securityLevel=0
        manager.create_signature(
            {"protocolID": [0, "open-protocol"], "data": [0x01, 0x02], "keyID": "1"}, originator="some-user.com"
        )

        # Then - no permission request triggered
        active_requests = getattr(manager, "_active_requests", {})
        assert len(active_requests) == 0

        # Underlying method called once
        mock_underlying_wallet.create_signature.assert_called_once()
```

### AI Analysis Results

**Similarity Score**: 46.00%
  - Structural: 0.00%
  - Semantic: 32.00%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createSignature, active_requests.size

**Differences:**
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: underlying.createSignature, active_requests.size

**Explanation:**

Overall Similarity: 46.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 32.0% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification method_call_verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: underlying.createSignature, active_requests.size

Key Differences:
  • Verification count: TS has 2, PY has 1

---

## Test 61: should NOT call underlying.encrypt() if encryptWalletMetadata=false **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.encryption.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_encryption.py`

---

## Test 62: should call underlying.decrypt() with correct protocol and key, returning plaintext on success **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.encryption.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_encryption.py`

---

## Test 63: should call underlying.encrypt() with the correct protocol and key when encryptWalletMetadata=true **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.encryption.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_encryption.py`

---

## Test 64: should decrypt customInstructions in listOutputs if encryptWalletMetadata=true **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.encryption.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_encryption.py`

---

## Test 65: should encrypt metadata fields in createAction when encryptWalletMetadata=true, then decrypt them in listActions **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.encryption.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_encryption.py`

---

## Test 66: should fallback to original string if underlying.decrypt() fails **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.encryption.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_encryption.py`

---

## Test 67: should fallback to the original ciphertext if decrypt fails in listOutputs **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.encryption.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_encryption.py`

---

## Test 68: should not encrypt metadata if encryptWalletMetadata=false, storing and retrieving plaintext **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.encryption.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_encryption.py`

---

## Test 69: should coalesce parallel requests for the same resource into a single user prompt **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.flows.test.ts

```typescript
    it('should coalesce parallel requests for the same resource into a single user prompt', async () => {
      // We want to test the underlying private method "requestPermissionFlow" indirectly
      // or we can test it via a public method that calls it. We'll do so via ensureProtocolPermission.

      // Force no token found => triggers a request flow
      mockNoTokensFound(manager)

      // Spy on the manager's "onProtocolPermissionRequested" callbacks
      const requestCallback = jest.fn(() => {})
      manager.bindCallback('onProtocolPermissionRequested', requestCallback)

      // Make two parallel calls for the same resource
      const callA = manager.ensureProtocolPermission({
        originator: 'example.com',
        privileged: false,
        protocolID: [1, 'someproto'],
        counterparty: 'self',
        reason: 'UnitTest - same resource A',
        seekPermission: true,
        usageType: 'signing'
      })

      const callB = manager.ensureProtocolPermission({
        originator: 'example.com',
        privileged: false,
        protocolID: [1, 'someproto'],
        counterparty: 'self',
        reason: 'UnitTest - same resource B',
        seekPermission: true,
        usageType: 'signing'
      })

      // Wait a short moment for the async request flow to trigger
      await new Promise(res => setTimeout(res, 5))

      // We expect only one "onProtocolPermissionRequested" event for both calls
      expect(requestCallback).toHaveBeenCalledTimes(1)

      // Now let's deny the request:
      // Grab the requestID that the manager gave us from the callback param
      const callbackArg = (requestCallback.mock as any).calls[0][0]
      const requestID = callbackArg.requestID
      expect(typeof requestID).toBe('string') // manager-generated

      // Deny the request
      await manager.denyPermission(requestID)

      // Both calls should reject
      await expect(callA).rejects.toThrow(/Permission denied/)
      await expect(callB).rejects.toThrow(/Permission denied/)

      // Confirm activeRequests map is empty after denial
      const activeRequests = (manager as any).activeRequests as Map<string, any[]>
      expect(activeRequests.size).toBe(0)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_flows.py

```python
    def test_should_coalesce_parallel_requests_for_the_same_resource_into_a_single_user_prompt(self) -> None:
        """Given: Manager with no tokens found
           When: Make two parallel calls for same resource
           Then: Only one user prompt triggered, both calls resolve/reject together

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.flows.test.ts
                   test('should coalesce parallel requests for the same resource into a single user prompt')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.test.com")

        # Force no token found => triggers a request flow
        manager._find_protocol_token = AsyncMock(return_value=None)
        manager._find_basket_token = AsyncMock(return_value=None)
        manager._find_certificate_token = AsyncMock(return_value=None)
        manager._find_spending_token = AsyncMock(return_value=None)

        # Spy on the manager's "onProtocolPermissionRequested" callbacks
        request_callback = Mock()
        manager.bind_callback("onProtocolPermissionRequested", request_callback)

        # When - make two parallel calls for same resource
        call_a = asyncio.create_task(
            manager.ensure_protocol_permission(
                {
                    "originator": "example.com",
                    "privileged": False,
                    "protocolID": [1, "someproto"],
                    "counterparty": "self",
                    "reason": "UnitTest - same resource A",
                    "seekPermission": True,
                    "usageType": "signing",
                }
            )
        )

        call_b = asyncio.create_task(
            manager.ensure_protocol_permission(
                {
                    "originator": "example.com",
                    "privileged": False,
                    "protocolID": [1, "someproto"],
                    "counterparty": "self",
                    "reason": "UnitTest - same resource B",
                    "seekPermission": True,
                    "usageType": "signing",
                }
            )
        )

        # Wait a short moment for the async request flow to trigger
        asyncio.sleep(0.005)

        # Then - only one "onProtocolPermissionRequested" event for both calls
        assert request_callback.call_count == 1

        # Grab the requestID that the manager gave us from the callback param
        callback_arg = request_callback.call_args[0][0]
        request_id = callback_arg["requestID"]
        assert isinstance(request_id, str)  # manager-generated

        # Deny the request
        manager.deny_permission(request_id)

        # Both calls should reject
        with pytest.raises(ValueError, match="Permission denied"):
            call_a
        with pytest.raises(ValueError, match="Permission denied"):
            call_b

        # Confirm activeRequests map is empty after denial
        active_requests = getattr(manager, "_active_requests", {})
        assert len(active_requests) == 0
```

### AI Analysis Results

**Similarity Score**: 16.00%
  - Structural: 0.00%
  - Semantic: 32.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: active_requests.size
  - [HIGH] Python test is missing operations: manager.denyPermission

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: active_requests.size
  - Add operations: manager.denyPermission

**Explanation:**

Overall Similarity: 16.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 32.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification token_operation verification
  • Python: token_operation verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: active_requests.size
  • [HIGH] Python test is missing operations: manager.denyPermission

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 70: should create a token if ephemeral=false, so subsequent calls do not re-trigger if unexpired **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.flows.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_flows.py`

---

## Test 71: should generate two distinct user prompts for two different permission requests **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.flows.test.ts

```typescript
    it('should generate two distinct user prompts for two different permission requests', async () => {
      // Force no tokens
      mockNoTokensFound(manager)

      // Spy on basket & protocol request callbacks
      const protocolRequestCb = jest.fn(() => {})
      const basketRequestCb = jest.fn(() => {})
      manager.bindCallback('onProtocolPermissionRequested', protocolRequestCb)
      manager.bindCallback('onBasketAccessRequested', basketRequestCb)

      // Make one call for protocol usage
      const pCall = manager.ensureProtocolPermission({
        originator: 'example.com',
        privileged: false,
        protocolID: [1, 'proto-A'],
        counterparty: 'self',
        reason: 'Different request A',
        seekPermission: true,
        usageType: 'signing'
      })

      // Make a second call for basket usage
      const bCall = manager.ensureBasketAccess({
        originator: 'example.com',
        basket: 'some-basket',
        reason: 'Different request B',
        seekPermission: true,
        usageType: 'insertion'
      })

      // Wait a moment for them to trigger
      await new Promise(res => setTimeout(res, 5))

      // We expect one protocol request AND one basket request
      expect(protocolRequestCb).toHaveBeenCalledTimes(1)
      expect(basketRequestCb).toHaveBeenCalledTimes(1)

      // Deny protocol request
      const pReqID = (protocolRequestCb.mock as any).calls[0][0].requestID
      await manager.denyPermission(pReqID)

      // Deny basket request
      const bReqID = (basketRequestCb.mock as any).calls[0][0].requestID
      await manager.denyPermission(bReqID)

      // Both calls should have rejected
      await expect(pCall).rejects.toThrow(/Permission denied/)
      await expect(bCall).rejects.toThrow(/Permission denied/)

      // activeRequests is empty
      const activeRequests = (manager as any).activeRequests as Map<string, any[]>
      expect(activeRequests.size).toBe(0)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_flows.py

```python
    def test_should_generate_two_distinct_user_prompts_for_two_different_permission_requests(self) -> None:
        """Given: Manager with no tokens found
           When: Make one protocol request and one basket request
           Then: Two distinct user prompts triggered

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.flows.test.ts
                   test('should generate two distinct user prompts for two different permission requests')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.test.com")

        # Force no tokens
        manager._find_protocol_token = AsyncMock(return_value=None)
        manager._find_basket_token = AsyncMock(return_value=None)
        manager._find_certificate_token = AsyncMock(return_value=None)
        manager._find_spending_token = AsyncMock(return_value=None)

        # Spy on basket & protocol request callbacks
        protocol_request_cb = Mock()
        basket_request_cb = Mock()
        manager.bind_callback("onProtocolPermissionRequested", protocol_request_cb)
        manager.bind_callback("onBasketAccessRequested", basket_request_cb)

        # When - make one call for protocol usage
        p_call = asyncio.create_task(
            manager.ensure_protocol_permission(
                {
                    "originator": "example.com",
                    "privileged": False,
                    "protocolID": [1, "proto-A"],
                    "counterparty": "self",
                    "reason": "Different request A",
                    "seekPermission": True,
                    "usageType": "signing",
                }
            )
        )

        # Make a second call for basket usage
        b_call = asyncio.create_task(
            manager.ensure_basket_access(
                {
                    "originator": "example.com",
                    "basket": "some-basket",
                    "reason": "Different request B",
                    "seekPermission": True,
                    "usageType": "insertion",
                }
            )
        )

        # Wait a moment for them to trigger
        asyncio.sleep(0.005)

        # Then - we expect one protocol request AND one basket request
        assert protocol_request_cb.call_count == 1
        assert basket_request_cb.call_count == 1

        # Deny protocol request
        p_req_id = protocol_request_cb.call_args[0][0]["requestID"]
        manager.deny_permission(p_req_id)

        # Deny basket request
        b_req_id = basket_request_cb.call_args[0][0]["requestID"]
        manager.deny_permission(b_req_id)

        # Both calls should have rejected
        with pytest.raises(ValueError, match="Permission denied"):
            p_call
        with pytest.raises(ValueError, match="Permission denied"):
            b_call

        # activeRequests is empty
        active_requests = getattr(manager, "_active_requests", {})
        assert len(active_requests) == 0
```

### AI Analysis Results

**Similarity Score**: 16.00%
  - Structural: 0.00%
  - Semantic: 32.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: active_requests.size
  - [HIGH] Python test is missing operations: manager.denyPermission

**Differences:**
  - Operation count: TS has 2, PY has 0
  - Verification count: TS has 3, PY has 2

**Suggestions:**
  - Add verifications for: active_requests.size
  - Add operations: manager.denyPermission

**Explanation:**

Overall Similarity: 16.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 32.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification token_operation verification
  • Python: token_operation verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: active_requests.size
  • [HIGH] Python test is missing operations: manager.denyPermission

Key Differences:
  • Operation count: TS has 2, PY has 0
  • Verification count: TS has 3, PY has 2

---

## Test 72: should handle renewal if the found token is expired, passing previousToken in the request **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.flows.test.ts

```typescript
    it('should handle renewal if the found token is expired, passing previousToken in the request', async () => {
      // We'll test the "renewal" flow:
      // If the manager finds a token but it's expired, it sets { renewal: true, previousToken } in the request.

      // We'll mock findProtocolToken to return an expired token
      const expiredToken: PermissionToken = {
        tx: [],
        txid: 'expiredTxid123',
        outputIndex: 0,
        outputScript: '76a914xxxx...88ac',
        satoshis: 1,
        originator: 'renewme.com',
        expiry: Math.floor(Date.now() / 1000) - 100, // in the past
        privileged: false,
        protocol: 'renew-proto',
        securityLevel: 1,
        counterparty: 'self'
      }
      jest.spyOn(manager as any, 'findProtocolToken').mockResolvedValue(expiredToken)

      // Spy on request callback
      const requestCb = jest.fn(() => {})
      manager.bindCallback('onProtocolPermissionRequested', requestCb)

      // We'll also spy on "renewPermissionOnChain" to see if it's called
      const renewSpy = jest.spyOn(manager as any, 'renewPermissionOnChain').mockResolvedValue(undefined)

      // Call ensureProtocolPermission => sees expired token => triggers request with renewal
      const promise = manager.ensureProtocolPermission({
        originator: 'renewme.com',
        privileged: false,
        protocolID: [1, 'renew-proto'],
        counterparty: 'self',
        reason: 'test renewal',
        usageType: 'encrypting'
      })

      // Wait for request callback
      await new Promise(res => setTimeout(res, 10))
      expect(requestCb).toHaveBeenCalledTimes(1)

      // Confirm the callback param includes `renewal=true` and `previousToken=expiredToken`
      const { renewal, previousToken } = (requestCb.mock as any).calls[0][0]
      expect(renewal).toBe(true)
      expect(previousToken.txid).toBe('expiredTxid123')

      // Grant ephemeral=false => manager calls renewPermissionOnChain
      const { requestID } = (requestCb.mock as any).calls[0][0]
      await manager.grantPermission({ requestID, ephemeral: false })

      await expect(promise).resolves.toBe(true)
      expect(renewSpy).toHaveBeenCalledTimes(1)
      // The first arg is the old token, second is request, etc.
      expect(renewSpy).toHaveBeenCalledWith(
        expiredToken,
        expect.objectContaining({ originator: 'renewme.com' }),
        expect.any(Number),
        undefined
      )
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_flows.py

```python
    def test_should_handle_renewal_if_the_found_token_is_expired_passing_previoustoken_in_the_request(
        self,
    ) -> None:
        """Given: Manager finds expired token
           When: Make permission request
           Then: Triggers renewal flow with previousToken

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.flows.test.ts
                   test('should handle renewal if the found token is expired, passing previousToken in the request')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.test.com")
        expired_token = {
            "txid": "old-expired",
            "outputIndex": 0,
            "originator": "appdomain.com",
            "expiry": 1,
            "privileged": False,
            "securityLevel": 1,
            "protocol": "expired-proto",
            "counterparty": "self",
        }
        manager._find_protocol_token = AsyncMock(return_value=expired_token)
        request_cb = Mock()
        manager.bind_callback("onProtocolPermissionRequested", request_cb)

        # When
        p_call = asyncio.create_task(
            manager.ensure_protocol_permission(
                {
                    "originator": "appdomain.com",
                    "privileged": False,
                    "protocolID": [1, "expired-proto"],
                    "counterparty": "self",
                    "usageType": "signing",
                }
            )
        )
        asyncio.sleep(0.005)

        # Then - callback should have renewal=True and previousToken
        assert request_cb.call_count == 1
        callback_arg = request_cb.call_args[0][0]
        assert callback_arg["renewal"] is True
        assert callback_arg["previousToken"] == expired_token

        req_id = callback_arg["requestID"]
        manager.grant_permission({"requestID": req_id, "ephemeral": True})
        p_call
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: previous_token.txid
  - [HIGH] Python test is missing operations: manager.grantPermission

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: previous_token.txid
  - Add operations: manager.grantPermission

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification token_operation verification encryption
  • Python: token_operation verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: previous_token.txid
  • [HIGH] Python test is missing operations: manager.grantPermission

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 73: should not create a token if ephemeral=true, so subsequent calls re-trigger the request **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.flows.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_flows.py`

---

## Test 74: should reject only the matching request queue on deny if requestID is specified **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.flows.test.ts

```typescript
    it('should reject only the matching request queue on deny if requestID is specified', async () => {
      // This scenario tests the manager's partial denial logic where we pass { requestID }
      // to only reject the queued requests with that ID, leaving others (with a different requestID)
      // in the queue.

      mockNoTokensFound(manager)

      // We do two separate calls for the same resource but at different times, resulting in separate queues.
      // Actually, the manager normally merges them into one queue if the resource is the same.
      // So let's do two different resources to ensure we get two separate keys.
      const protoCb = jest.fn(() => {})
      manager.bindCallback('onProtocolPermissionRequested', protoCb)

      // Resource 1
      const p1Promise = manager.ensureProtocolPermission({
        originator: 'siteA.com',
        privileged: false,
        protocolID: [1, 'proto-siteA'],
        counterparty: 'self',
        usageType: 'encrypting'
      })
      await new Promise(res => setTimeout(res, 5))
      const p1ReqID = (protoCb.mock as any).calls[0][0].requestID
      // At this point, resource 1 is pending in activeRequests. We'll not resolve it yet.

      // Resource 2
      const p2Promise = manager.ensureProtocolPermission({
        originator: 'siteB.com',
        privileged: false,
        protocolID: [1, 'proto-siteB'],
        counterparty: 'self',
        usageType: 'encrypting'
      })
      await new Promise(res => setTimeout(res, 5))
      // the second call triggers a second onProtocolPermissionRequested callback
      expect(protoCb).toHaveBeenCalledTimes(2)
      const p2ReqID = (protoCb.mock as any).calls[1][0].requestID

      // Deny the second request only
      await manager.denyPermission(p2ReqID)
      await expect(p2Promise).rejects.toThrow(/Permission denied/)

      // But the first request is still waiting
      const activeRequests = (manager as any).activeRequests as Map<string, any[]>
      expect(activeRequests.size).toBe(1)

      // Now let's deny the first request too
      await manager.denyPermission(p1ReqID)
      await expect(p1Promise).rejects.toThrow(/Permission denied/)

      // The queue is empty now
      expect(activeRequests.size).toBe(0)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_flows.py

```python
    def test_should_reject_only_the_matching_request_queue_on_deny_if_requestid_is_specified(self) -> None:
        """Given: Manager with two different pending requests
           When: Deny one requestID
           Then: Only that request is rejected, other remains pending

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.flows.test.ts
                   test('should reject only the matching request queue on deny if requestID is specified')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.test.com")
        manager._find_protocol_token = AsyncMock(return_value=None)
        proto_cb = Mock()
        manager.bind_callback("onProtocolPermissionRequested", proto_cb)

        # When - Resource 1
        p1_promise = asyncio.create_task(
            manager.ensure_protocol_permission(
                {
                    "originator": "siteA.com",
                    "privileged": False,
                    "protocolID": [1, "proto-siteA"],
                    "counterparty": "self",
                    "usageType": "encrypting",
                }
            )
        )
        asyncio.sleep(0.005)
        p1_req_id = proto_cb.call_args[0][0]["requestID"]

        # Resource 2
        p2_promise = asyncio.create_task(
            manager.ensure_protocol_permission(
                {
                    "originator": "siteB.com",
                    "privileged": False,
                    "protocolID": [1, "proto-siteB"],
                    "counterparty": "self",
                    "usageType": "encrypting",
                }
            )
        )
        asyncio.sleep(0.005)
        assert proto_cb.call_count == 2
        p2_req_id = proto_cb.call_args_list[1][0][0]["requestID"]

        # Then - deny the second request only
        manager.deny_permission(p2_req_id)
        with pytest.raises(ValueError, match="Permission denied"):
            p2_promise

        # But the first request is still waiting
        active_requests = getattr(manager, "_active_requests", {})
        assert len(active_requests) == 1

        # Now let's deny the first request too
        manager.deny_permission(p1_req_id)
        with pytest.raises(ValueError, match="Permission denied"):
            p1_promise
        assert len(active_requests) == 0
```

### AI Analysis Results

**Similarity Score**: 17.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: active_requests.size
  - [HIGH] Python test is missing operations: manager.denyPermission

**Differences:**
  - Operation count: TS has 2, PY has 0
  - Verification count: TS has 3, PY has 1

**Suggestions:**
  - Add verifications for: active_requests.size
  - Add operations: manager.denyPermission

**Explanation:**

Overall Similarity: 17.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification token_operation verification encryption
  • Python: token_operation verification encryption

Critical Issues (2):
  • [HIGH] Python test is missing verifications: active_requests.size
  • [HIGH] Python test is missing operations: manager.denyPermission

Key Differences:
  • Operation count: TS has 2, PY has 0
  • Verification count: TS has 3, PY has 1

---

## Test 75: should resolve all parallel requests when permission is granted, referencing the same requestID **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.flows.test.ts

```typescript
    it('should resolve all parallel requests when permission is granted, referencing the same requestID', async () => {
      // No tokens => triggers request flow
      mockNoTokensFound(manager)

      const requestCb = jest.fn(() => {})
      manager.bindCallback('onProtocolPermissionRequested', requestCb)

      // Parallel calls
      const promiseA = manager.ensureProtocolPermission({
        originator: 'example.com',
        privileged: false,
        protocolID: [1, 'proto-X'],
        counterparty: 'anyone',
        reason: 'Test parallel grant A',
        seekPermission: true,
        usageType: 'encrypting'
      })

      const promiseB = manager.ensureProtocolPermission({
        originator: 'example.com',
        privileged: false,
        protocolID: [1, 'proto-X'],
        counterparty: 'anyone',
        reason: 'Test parallel grant B',
        seekPermission: true,
        usageType: 'encrypting'
      })

      // Let the request event fire
      await new Promise(res => setTimeout(res, 5))
      expect(requestCb).toHaveBeenCalledTimes(1)

      // Extract the requestID from the callback
      const { requestID } = (requestCb.mock as any).calls[0][0]
      // Now we grant permission for that same requestID
      // Because ephemeral is false by default, the manager will attempt to create on-chain tokens
      // We'll mock the internal createPermissionOnChain so it doesn't blow up
      const createOnChainSpy = jest.spyOn(manager as any, 'createPermissionOnChain').mockResolvedValue(undefined)

      await manager.grantPermission({ requestID })

      // Both calls should resolve with `true` (the manager returns a boolean)
      await expect(promiseA).resolves.toBe(true)
      await expect(promiseB).resolves.toBe(true)

      // activeRequests map is empty
      const activeRequests = (manager as any).activeRequests as Map<string, any[]>
      expect(activeRequests.size).toBe(0)

      // The manager tried to create an on-chain permission token once
      expect(createOnChainSpy).toHaveBeenCalledTimes(1)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_flows.py

```python
    def test_should_resolve_all_parallel_requests_when_permission_is_granted_referencing_the_same_requestid(
        self,
    ) -> None:
        """Given: Manager with no tokens, parallel requests for same resource
           When: Grant permission with requestID
           Then: All parallel requests resolve successfully

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.flows.test.ts
                   test('should resolve all parallel requests when permission is granted, referencing the same requestID')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.test.com")

        # No tokens => triggers request flow
        manager._find_protocol_token = AsyncMock(return_value=None)
        manager._find_basket_token = AsyncMock(return_value=None)
        manager._find_certificate_token = AsyncMock(return_value=None)
        manager._find_spending_token = AsyncMock(return_value=None)

        request_cb = Mock()
        manager.bind_callback("onProtocolPermissionRequested", request_cb)

        # When - parallel calls
        promise_a = asyncio.create_task(
            manager.ensure_protocol_permission(
                {
                    "originator": "example.com",
                    "privileged": False,
                    "protocolID": [1, "proto-X"],
                    "counterparty": "anyone",
                    "reason": "Test parallel grant A",
                    "seekPermission": True,
                    "usageType": "encrypting",
                }
            )
        )

        promise_b = asyncio.create_task(
            manager.ensure_protocol_permission(
                {
                    "originator": "example.com",
                    "privileged": False,
                    "protocolID": [1, "proto-X"],
                    "counterparty": "anyone",
                    "reason": "Test parallel grant B",
                    "seekPermission": True,
                    "usageType": "encrypting",
                }
            )
        )

        # Wait for request to trigger
        asyncio.sleep(0.005)

        # Then - only one callback
        assert request_cb.call_count == 1

        # Grant permission with ephemeral=True
        request_id = request_cb.call_args[0][0]["requestID"]
        manager.grant_permission({"requestID": request_id, "ephemeral": True})

        # Both promises should resolve
        promise_a  # Should not raise
        promise_b  # Should not raise

        # activeRequests should be empty
        active_requests = getattr(manager, "_active_requests", {})
        assert len(active_requests) == 0
```

### AI Analysis Results

**Similarity Score**: 17.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: active_requests.size
  - [HIGH] Python test is missing operations: manager.grantPermission

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 3, PY has 1

**Suggestions:**
  - Add verifications for: active_requests.size
  - Add operations: manager.grantPermission

**Explanation:**

Overall Similarity: 17.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification token_operation verification encryption
  • Python: token_operation verification encryption

Critical Issues (2):
  • [HIGH] Python test is missing verifications: active_requests.size
  • [HIGH] Python test is missing operations: manager.grantPermission

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 3, PY has 1

---

## Test 76: should consider calls from the adminOriginator as admin, bypassing checks **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.initialization.test.ts

```typescript
  it('should consider calls from the adminOriginator as admin, bypassing checks', async () => {
    const manager = new WalletPermissionsManager(underlying, 'admin.domain.com')

    // If we call a method that normally triggers permission checks (like createAction with a basket),
    // but pass in originator="admin.domain.com", we expect NO permission prompt or error.
    // We'll do a minimal createAction call.
    const result = await manager.createAction(
      {
        description: 'Insertion to user basket',
        outputs: [
          {
            lockingScript: 'abcd',
            satoshis: 1000,
            outputDescription: 'some out desc',
            basket: 'some-user-basket'
          }
        ]
      },
      'admin.domain.com'
    )

    // If the manager truly bypassed checks for the admin, it won't queue a request
    // nor throw an error. The call should just succeed.
    expect(result).toBeDefined()

    // Confirm the underlying createAction was actually called
    expect(underlying.createAction).toHaveBeenCalledTimes(1)

    // activeRequests map should be empty
    const activeRequests = (manager as any).activeRequests as Map<string, any[]>
    expect(activeRequests.size).toBe(0)
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_initialization.py

```python
    def test_should_consider_calls_from_the_adminoriginator_as_admin_bypassing_checks(self) -> None:
        """Given: Manager with admin originator set
           When: Call method with admin originator
           Then: Bypasses all permission checks

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.initialization.test.ts
                   test('should consider calls from the adminOriginator as admin, bypassing checks')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_action = AsyncMock(return_value={"txid": "admin-tx"})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet, admin_originator="admin.domain.com"
        )

        # When - call with admin originator
        result = manager.create_action(
            {
                "description": "Insertion to user basket",
                "outputs": [
                    {
                        "lockingScript": "abcd",
                        "satoshis": 1000,
                        "outputDescription": "some out desc",
                        "basket": "some-user-basket",
                    }
                ],
            },
            "admin.domain.com",
        )

        # Then - bypassed checks, call succeeded
        assert result is not None
        assert mock_underlying_wallet.create_action.call_count == 1

        # activeRequests map should be empty
        active_requests = getattr(manager, "_active_requests", {})
        assert len(active_requests) == 0
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createAction, active_requests.size
  - [HIGH] Python test is missing operations: manager.createAction

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: underlying.createAction, active_requests.size
  - Add operations: manager.createAction

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.createAction, active_requests.size
  • [HIGH] Python test is missing operations: manager.createAction

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 77: should enforce protocol permission checks for signing if seekProtocolPermissionsForSigning=true **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.initialization.test.ts

```typescript
  it('should enforce protocol permission checks for signing if seekProtocolPermissionsForSigning=true', async () => {
    // By default, or explicitly set to true, the manager enforces permission checks
    const manager = new WalletPermissionsManager(underlying, 'admin.domain.com', {
      seekProtocolPermissionsForSigning: true
    })

    // Non-admin origin tries createSignature -> must prompt for protocol permission
    const createSigPromise = manager.createSignature(
      {
        protocolID: [1, 'test-protocol'],
        keyID: '1',
        data: [0x10, 0x20],
        privileged: false
      },
      'nonadmin.com'
    )

    // The manager triggers a request. Let's see if the request queue has an entry:
    const activeRequests = (manager as any).activeRequests as Map<string, any>
    // We may not see an entry synchronously because `ensureProtocolPermission()` is async,
    // but once the promise gets to that stage, it populates the queue.

    // Wait a short tick to let the async code run
    await new Promise(res => setTimeout(res, 10))
    expect(activeRequests.size).toBeGreaterThan(0)

    // We'll forcibly deny the request so the test can conclude:
    const firstRequestKey = Array.from(activeRequests.keys())[0]
    const firstRequestQueue = activeRequests.get(firstRequestKey)
    if (firstRequestQueue && firstRequestQueue.pending.length > 0) {
      manager.denyPermission(firstRequestKey)
    }

    // The promise eventually rejects with "Permission denied."
    await expect(createSigPromise).rejects.toThrow(/Permission denied/)
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_initialization.py

```python
    def test_should_enforce_protocol_permission_checks_for_signing_if_seekprotocolpermissionsforsigning_true(
        self,
    ) -> None:
        """Given: Manager with seekProtocolPermissionsForSigning=True
           When: Non-admin creates signature with protocolID
           Then: Permission check triggered, request queued

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.initialization.test.ts
                   test('should enforce protocol permission checks for signing if seekProtocolPermissionsForSigning=true')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.domain.com",
            config={"seekProtocolPermissionsForSigning": True},
        )
        manager._find_protocol_token = AsyncMock(return_value=None)

        # When - non-admin origin tries createSignature
        create_sig_promise = asyncio.create_task(
            manager.create_signature(
                {"protocolID": [1, "test-protocol"], "keyID": "1", "data": [0x10, 0x20], "privileged": False},
                "nonadmin.com",
            )
        )

        # Wait a short tick to let the async code run
        asyncio.sleep(0.01)

        # Then - request queue has an entry
        active_requests = getattr(manager, "_active_requests", {})
        assert len(active_requests) > 0

        # Forcibly deny the request so the test can conclude
        first_request_key = next(iter(active_requests.keys()))
        manager.deny_permission(first_request_key)

        # The promise eventually rejects
        with pytest.raises(ValueError, match="Permission denied"):
            create_sig_promise
```

### AI Analysis Results

**Similarity Score**: 42.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: active_requests.size

**Differences:**
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: active_requests.size

**Explanation:**

Overall Similarity: 42.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: token_operation verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: active_requests.size

Key Differences:
  • Verification count: TS has 1, PY has 0

---

## Test 78: should initialize with all config flags set to false **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.initialization.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_initialization.py`

---

## Test 79: should initialize with default config if none is provided **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.initialization.test.ts

```typescript
  it('should initialize with default config if none is provided', () => {
    const manager = new WalletPermissionsManager(underlying, 'admin.domain.com')

    // The manager internally defaults all config flags to true.
    const internalConfig = (manager as any).config as PermissionsManagerConfig

    expect(internalConfig.seekProtocolPermissionsForSigning).toBe(true)
    expect(internalConfig.seekProtocolPermissionsForEncrypting).toBe(true)
    expect(internalConfig.seekPermissionsForIdentityKeyRevelation).toBe(true)
    expect(internalConfig.encryptWalletMetadata).toBe(true)

    // The manager should store the admin originator
    const admin = (manager as any).adminOriginator
    expect(admin).toBe('admin.domain.com')
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_initialization.py

```python
    def test_should_initialize_with_default_config_if_none_is_provided(self) -> None:
        """Given: No config provided to constructor
           When: Create WalletPermissionsManager
           Then: All config flags default to True

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.initialization.test.ts
                   test('should initialize with default config if none is provided')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)

        # When
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet, admin_originator="admin.domain.com"
        )

        # Then - manager internally defaults all config flags to true
        internal_config = getattr(manager, "_config", {})
        assert internal_config.get("seekProtocolPermissionsForSigning") is True
        assert internal_config.get("seekProtocolPermissionsForEncrypting") is True
        assert internal_config.get("seekPermissionsForIdentityKeyRevelation") is True
        assert internal_config.get("encryptWalletMetadata") is True

        # The manager should store the admin originator
        admin = getattr(manager, "_admin_originator", None)
        assert admin == "admin.domain.com"
```

### AI Analysis Results

**Similarity Score**: 47.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: internal_config.seekPermissionsForIdentityKeyRevelation, internal_config.seekProtocolPermissionsForSigning, internal_config.encryptWalletMetadata, internal_config.seekProtocolPermissionsForEncrypting

**Suggestions:**
  - Add verifications for: internal_config.seekPermissionsForIdentityKeyRevelation, internal_config.seekProtocolPermissionsForSigning, internal_config.encryptWalletMetadata

**Explanation:**

Overall Similarity: 47.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: authentication value_verification verification encryption
  • Python: authentication verification encryption

Critical Issues (1):
  • [HIGH] Python test is missing verifications: internal_config.seekPermissionsForIdentityKeyRevelation, internal_config.seekProtocolPermissionsForSigning, internal_config.encryptWalletMetadata, internal_config.seekProtocolPermissionsForEncrypting

---

## Test 80: should initialize with partial config overrides, merging with defaults **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.initialization.test.ts

```typescript
  it('should initialize with partial config overrides, merging with defaults', () => {
    const partialConfig: PermissionsManagerConfig = {
      seekProtocolPermissionsForSigning: false,
      encryptWalletMetadata: false
      // The rest remain default = true
    }

    const manager = new WalletPermissionsManager(underlying, 'admin.domain.com', partialConfig)
    const internalConfig = (manager as any).config

    // Overridden to false
    expect(internalConfig.seekProtocolPermissionsForSigning).toBe(false)
    expect(internalConfig.encryptWalletMetadata).toBe(false)

    // Remaining defaults still true
    expect(internalConfig.seekBasketInsertionPermissions).toBe(true)
    expect(internalConfig.seekSpendingPermissions).toBe(true)
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_initialization.py

```python
    def test_should_initialize_with_partial_config_overrides_merging_with_defaults(self) -> None:
        """Given: Partial config provided (some flags overridden)
           When: Create WalletPermissionsManager
           Then: Overridden flags set correctly, rest remain default

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.initialization.test.ts
                   test('should initialize with partial config overrides, merging with defaults')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        partial_config = {
            "seekProtocolPermissionsForSigning": False,
            "encryptWalletMetadata": False,
            # The rest remain default = true
        }

        # When
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet, admin_originator="admin.domain.com", config=partial_config
        )

        # Then - overridden to false
        internal_config = getattr(manager, "_config", {})
        assert internal_config.get("seekProtocolPermissionsForSigning") is False
        assert internal_config.get("encryptWalletMetadata") is False

        # Remaining defaults still true
        assert internal_config.get("seekBasketInsertionPermissions") is True
        assert internal_config.get("seekSpendingPermissions") is True
```

### AI Analysis Results

**Similarity Score**: 43.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: internal_config.seekSpendingPermissions, internal_config.seekProtocolPermissionsForSigning, internal_config.encryptWalletMetadata, internal_config.seekBasketInsertionPermissions

**Suggestions:**
  - Add verifications for: internal_config.seekSpendingPermissions, internal_config.seekProtocolPermissionsForSigning, internal_config.encryptWalletMetadata

**Explanation:**

Overall Similarity: 43.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification encryption
  • Python: authentication verification encryption

Critical Issues (1):
  • [HIGH] Python test is missing verifications: internal_config.seekSpendingPermissions, internal_config.seekProtocolPermissionsForSigning, internal_config.encryptWalletMetadata, internal_config.seekBasketInsertionPermissions

---

## Test 81: should skip basket insertion permission checks if seekBasketInsertionPermissions=false **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.initialization.test.ts

```typescript
  it('should skip basket insertion permission checks if seekBasketInsertionPermissions=false', async () => {
    const manager = new WalletPermissionsManager(underlying, 'admin.domain.com', {
      seekBasketInsertionPermissions: false
    })
    // Spending authorization is still required, grant it.
    manager.bindCallback(
      'onSpendingAuthorizationRequested',
      jest.fn(x => {
        manager.grantPermission({ requestID: x.requestID, ephemeral: true })
      }) as any
    )

    // Non-admin origin tries to createAction specifying a basket
    await expect(
      manager.createAction(
        {
          description: 'Insert to user basket',
          outputs: [
            {
              lockingScript: '1234',
              satoshis: 888,
              basket: 'somebasket',
              outputDescription: 'some out desc'
            }
          ]
        },
        'some-user.com'
      )
    ).resolves.not.toThrow()

    // Because insertion checks are disabled, no permission request should be queued
    const activeRequests = (manager as any).activeRequests as Map<string, any>
    expect(activeRequests.size).toBe(0)
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_initialization.py

```python
    def test_should_skip_basket_insertion_permission_checks_if_seekbasketinsertionpermissions_false(self) -> None:
        """Given: Manager with seekBasketInsertionPermissions=False
           When: Non-admin creates action with basket
           Then: No basket insertion permission check

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.initialization.test.ts
                   test('should skip basket insertion permission checks if seekBasketInsertionPermissions=false')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_action = AsyncMock(return_value={"txid": "tx1"})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.domain.com",
            config={"seekBasketInsertionPermissions": False},
        )

        # Spending authorization is still required, grant it
        def auto_grant_spending(request) -> None:

            _task = asyncio.create_task(
                manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})
            )
            _task.add_done_callback(lambda _fut: None)

        manager.bind_callback("onSpendingAuthorizationRequested", auto_grant_spending)

        # When - non-admin origin tries to createAction specifying a basket
        manager.create_action(
            {
                "description": "Insert to user basket",
                "outputs": [
                    {
                        "lockingScript": "1234",
                        "satoshis": 888,
                        "basket": "somebasket",
                        "outputDescription": "some out desc",
                    }
                ],
            },
            "some-user.com",
        )

        # Then - no permission request should be queued (spending auth auto-granted)
        active_requests = getattr(manager, "_active_requests", {})
        assert len(active_requests) == 0
```

### AI Analysis Results

**Similarity Score**: 43.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: active_requests.size

**Differences:**
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: active_requests.size

**Explanation:**

Overall Similarity: 43.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: active_requests.size

Key Differences:
  • Verification count: TS has 1, PY has 0

---

## Test 82: should skip protocol permission checks for signing if seekProtocolPermissionsForSigning=false **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.initialization.test.ts

```typescript
  it('should skip protocol permission checks for signing if seekProtocolPermissionsForSigning=false', async () => {
    const manager = new WalletPermissionsManager(underlying, 'admin.domain.com', {
      seekProtocolPermissionsForSigning: false
    })

    // Non-admin origin attempts "createSignature" with a protocolID
    // Normally, if config was true, we'd expect a request for permission.
    // But here we expect it to skip and proceed.
    await expect(
      manager.createSignature(
        {
          protocolID: [1, 'some-protocol'],
          privileged: false,
          data: [0x01, 0x02],
          keyID: '1'
        },
        'app.nonadmin.com'
      )
    ).resolves.not.toThrow()

    // underlying createSignature is invoked
    expect(underlying.createSignature).toHaveBeenCalledTimes(1)

    // The manager’s internal request queue should remain empty
    const activeRequests = (manager as any).activeRequests as Map<string, any[]>
    expect(activeRequests.size).toBe(0)
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_initialization.py

```python
    def test_should_skip_protocol_permission_checks_for_signing_if_seekprotocolpermissionsforsigning_false(
        self,
    ) -> None:
        """Given: Manager with seekProtocolPermissionsForSigning=False
           When: Non-admin creates signature with protocolID
           Then: No permission check, proceeds directly

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.initialization.test.ts
                   test('should skip protocol permission checks for signing if seekProtocolPermissionsForSigning=false')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_signature = AsyncMock(return_value={"signature": "sig"})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.domain.com",
            config={"seekProtocolPermissionsForSigning": False},
        )

        # When - non-admin origin attempts createSignature
        manager.create_signature(
            {"protocolID": [1, "some-protocol"], "privileged": False, "data": [0x01, 0x02], "keyID": "1"},
            "app.nonadmin.com",
        )

        # Then - underlying createSignature is invoked
        assert mock_underlying_wallet.create_signature.call_count == 1

        # The manager's internal request queue should remain empty
        active_requests = getattr(manager, "_active_requests", {})
        assert len(active_requests) == 0
```

### AI Analysis Results

**Similarity Score**: 42.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createSignature, active_requests.size

**Differences:**
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: underlying.createSignature, active_requests.size

**Explanation:**

Overall Similarity: 42.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: underlying.createSignature, active_requests.size

Key Differences:
  • Verification count: TS has 2, PY has 1

---

## Test 83: should abort the action if spending permission is denied **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should abort the action if spending permission is denied', async () => {
    // This time let's forcibly DENY the onSpendingAuthorizationRequested callback
    manager.unbindCallback('onSpendingAuthorizationRequested', 0) // Unbind the ephemeral-grant
    manager.bindCallback('onSpendingAuthorizationRequested', async req => {
      await manager.denyPermission(req.requestID)
    })

    // We'll use the same approach: netSpent > 0 triggers the spending authorization check.
    underlying.createAction.mockResolvedValueOnce({
      signableTransaction: {
        tx: [0xde],
        reference: 'test-ref-2'
      }
    })

    // Mock parse tx for netSpent
    const mockTx = new MockTransaction()
    mockTx.fee = 100
    mockTx.inputs = [
      {
        sourceTXID: 'bbb',
        sourceOutputIndex: 0,
        sourceTransaction: {
          outputs: [{ satoshis: 0 }]
        }
      }
    ]
    mockTx.outputs = [{ satoshis: 100 }]
    ;(MockedBSV_SDK.Transaction.fromAtomicBEEF as jest.Mock).mockReturnValue(mockTx)

    await expect(
      manager.createAction(
        {
          description: 'User tries to spend 100 + fee=100 from 0 input => netSpent=200',
          outputs: [
            {
              lockingScript: 'abc123',
              satoshis: 100,
              outputDescription: 'some out desc',
              basket: 'some-basket'
            }
          ]
        },
        'user.example.com'
      )
    ).rejects.toThrow(/Permission denied/)

    // We expect the manager to call underlying.abortAction with reference 'test-ref-2'
    expect(underlying.abortAction).toHaveBeenCalledTimes(1)
    expect(underlying.abortAction).toHaveBeenCalledWith({
      reference: 'test-ref-2'
    })
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_abort_the_action_if_spending_permission_is_denied(self) -> None:
        """Given: Manager with spending permission callback that denies
           When: createAction triggers spending authorization
           Then: Action is aborted, abortAction is called

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should abort the action if spending permission is denied')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_action = AsyncMock(
            return_value={"signableTransaction": {"tx": [0xDE], "reference": "test-ref-2"}}
        )
        mock_underlying_wallet.abort_action = AsyncMock()

        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={"seekSpendingPermissions": True},
        )

        # Deny spending permission
        async def deny_spending(request) -> None:
            manager.deny_permission(request["requestID"])

        manager.bind_callback("onSpendingAuthorizationRequested", deny_spending)

        # When/Then
        with pytest.raises(ValueError, match="Permission denied"):
            manager.create_action(
                {
                    "description": "User tries to spend",
                    "outputs": [
                        {
                            "lockingScript": "abc123",
                            "satoshis": 100,
                            "outputDescription": "some out desc",
                            "basket": "some-basket",
                        }
                    ],
                },
                "user.example.com",
            )

        # abortAction should be called
        assert mock_underlying_wallet.abort_action.call_count == 1
        assert mock_underlying_wallet.abort_action.call_args[0][0]["reference"] == "test-ref-2"
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.abortAction
  - [HIGH] Python test is missing operations: manager.denyPermission

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: underlying.abortAction
  - Add operations: manager.denyPermission

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.abortAction
  • [HIGH] Python test is missing operations: manager.denyPermission

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 84: should call acquireCertificate, verifying permission if config.seekCertificateAcquisitionPermissions=true **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should call acquireCertificate, verifying permission if config.seekCertificateAcquisitionPermissions=true', async () => {
    const result = await manager.acquireCertificate(
      {
        type: 'my-cert',
        certifier: '02aaaa...',
        acquisitionProtocol: 'direct',
        fields: { hello: 'world' }
      },
      'user.cert.com'
    )
    expect(underlying.acquireCertificate).toHaveBeenCalledTimes(1)
    expect(result.type).toBe('some-cert-type')
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_call_acquirecertificate_verifying_permission_if_config_seekcertificateacquisitionpermissions_true(
        self,
    ) -> None:
        """Given: Manager with certificate acquisition permissions
           When: acquireCertificate is called
           Then: Checks permissions, calls underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should call acquireCertificate, verifying permission if config.seekCertificateAcquisitionPermissions=true')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.acquire_certificate = AsyncMock(return_value={"certificate": "cert"})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={"seekCertificateAcquisitionPermissions": True},
        )

        async def auto_grant(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onCertificateAccessRequested", auto_grant)

        # When
        manager.acquire_certificate(
            {"type": "type", "certifier": "certifier", "acquisitionProtocol": "proto"}, "user.com"
        )

        # Then
        assert mock_underlying_wallet.acquire_certificate.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.acquireCertificate, result.type
  - [HIGH] Python test is missing operations: manager.acquireCertificate

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: underlying.acquireCertificate, result.type
  - Add operations: manager.acquireCertificate

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.acquireCertificate, result.type
  • [HIGH] Python test is missing operations: manager.acquireCertificate

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 85: should call discoverByAttributes after ensuring identity resolution permission **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should call discoverByAttributes after ensuring identity resolution permission', async () => {
    const result = await manager.discoverByAttributes({ attributes: { name: 'Bob' } }, 'someone-trying-lookup.com')
    expect(underlying.discoverByAttributes).toHaveBeenCalledTimes(1)
    expect(result.certificates.length).toBe(0)
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_call_discoverbyattributes_after_ensuring_identity_resolution_permission(self) -> None:
        """Given: Manager with identity resolution permissions
           When: discoverByAttributes is called
           Then: Checks permissions, calls underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should call discoverByAttributes after ensuring identity resolution permission')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.discover_by_attributes = AsyncMock(return_value={"certificates": []})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={"seekPermissionsForIdentityResolution": True},
        )

        async def auto_grant(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onProtocolPermissionRequested", auto_grant)

        # When
        manager.discover_by_attributes({"attributes": {"key": "value"}}, "user.com")

        # Then
        assert mock_underlying_wallet.discover_by_attributes.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.discoverByAttributes
  - [HIGH] Python test is missing operations: manager.discoverByAttributes

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: underlying.discoverByAttributes
  - Add operations: manager.discoverByAttributes

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.discoverByAttributes
  • [HIGH] Python test is missing operations: manager.discoverByAttributes

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 86: should call discoverByIdentityKey after ensuring identity resolution permission **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should call discoverByIdentityKey after ensuring identity resolution permission', async () => {
    const result = await manager.discoverByIdentityKey({ identityKey: '0222fff...' }, 'someone-trying-lookup.com')
    expect(underlying.discoverByIdentityKey).toHaveBeenCalledTimes(1)
    expect(result.certificates.length).toBe(0)
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_call_discoverbyidentitykey_after_ensuring_identity_resolution_permission(self) -> None:
        """Given: Manager with identity resolution permissions
           When: discoverByIdentityKey is called
           Then: Checks permissions, calls underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should call discoverByIdentityKey after ensuring identity resolution permission')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.discover_by_identity_key = AsyncMock(return_value={"certificates": []})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={"seekPermissionsForIdentityResolution": True},
        )

        async def auto_grant(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onProtocolPermissionRequested", auto_grant)

        # When
        manager.discover_by_identity_key({"identityKey": "key"}, "user.com")

        # Then
        assert mock_underlying_wallet.discover_by_identity_key.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.discoverByIdentityKey
  - [HIGH] Python test is missing operations: manager.discoverByIdentityKey

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: underlying.discoverByIdentityKey
  - Add operations: manager.discoverByIdentityKey

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.discoverByIdentityKey
  • [HIGH] Python test is missing operations: manager.discoverByIdentityKey

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 87: should call getPublicKey on underlying after ensuring protocol permission **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should call getPublicKey on underlying after ensuring protocol permission', async () => {
    const result = await manager.getPublicKey(
      {
        protocolID: [1, 'test-pubkey'],
        keyID: 'my-key'
      },
      'user.example.com'
    )

    expect(underlying.getPublicKey).toHaveBeenCalledTimes(1)
    expect(underlying.getPublicKey).toHaveBeenCalledWith(
      {
        protocolID: [1, 'test-pubkey'],
        keyID: 'my-key'
      },
      'user.example.com'
    )
    expect(result.publicKey).toBe('029999...')
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_call_getpublickey_on_underlying_after_ensuring_protocol_permission(self) -> None:
        """Given: Manager with protocol permissions
           When: getPublicKey is called with protocolID
           Then: Checks permissions, calls underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should call getPublicKey on underlying after ensuring protocol permission')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.get_public_key = AsyncMock(return_value={"publicKey": "key"})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={"seekPermissionsForPublicKeyRevelation": True},
        )

        async def auto_grant(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onProtocolPermissionRequested", auto_grant)

        # When
        manager.get_public_key({"protocolID": [1, "my-protocol"], "keyID": "1"}, "user.com")

        # Then
        assert mock_underlying_wallet.get_public_key.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: result.publicKey, underlying.getPublicKey
  - [HIGH] Python test is missing operations: manager.getPublicKey

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 3, PY has 1

**Suggestions:**
  - Add verifications for: result.publicKey, underlying.getPublicKey
  - Add operations: manager.getPublicKey

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: result.publicKey, underlying.getPublicKey
  • [HIGH] Python test is missing operations: manager.getPublicKey

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 3, PY has 1

---

## Test 88: should call listActions on the underlying wallet and decrypt metadata fields if encryptWalletMetadata=true **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should call listActions on the underlying wallet and decrypt metadata fields if encryptWalletMetadata=true', async () => {
    // Underlying returns some encrypted metadata
    underlying.listActions.mockResolvedValueOnce({
      totalActions: 1,
      actions: [
        {
          actionTXID: 'aaa',
          description: 'EncryptedStuff',
          inputs: [
            {
              outpoint: 'xxx.0',
              inputDescription: 'EncryptedIn'
            }
          ],
          outputs: [
            {
              lockingScript: 'deadbeef',
              outputDescription: 'EncryptedOut',
              customInstructions: 'EncryptedCustom'
            }
          ],
          labels: ['user-label']
        }
      ]
    })
    // We'll have the manager attempt to decrypt. The manager calls `underlying.decrypt`
    // which is mocked to return plaintext [42, 42, 42, 42, 42, 42, 42]. That is "asterisk-asterisk" in ASCII
    // So let's see how the manager transforms it back to a string: fromCharCode(42,42) => "**"
    // However, note that the manager's "maybeDecryptMetadata()" tries to decrypt the field
    // If it works, it returns the decrypted string. Our underlying mock decrypt => "[42,42]" => "**"
    // So let's expect the final returned fields to be "**".

    const result = await manager.listActions({ labels: ['some-label'] }, 'nonadmin.com')

    expect(underlying.listActions).toHaveBeenCalledTimes(1)
    // The manager calls ensureLabelAccess first, which triggers a protocol permission request
    // we ephemeral-grant. Then it calls underlying.listActions.
    expect(result.actions[0].description).toBe('*****') // Decrypted from [42, 42, 42, 42, 42, 42, 42]
    expect(result.actions[0].inputs![0].inputDescription).toBe('*****')
    expect(result.actions[0].outputs![0].outputDescription).toBe('*****')
    expect(result.actions[0].outputs![0].customInstructions).toBe('*****')
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_call_listactions_on_the_underlying_wallet_and_decrypt_metadata_fields_if_encryptwalletmetadata_true(
        self,
    ) -> None:
        """Given: Manager with encryptWalletMetadata=true
           When: listActions is called
           Then: Calls underlying, decrypts metadata

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should call listActions on the underlying wallet and decrypt metadata fields if encryptWalletMetadata=true')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.list_actions = AsyncMock(
            return_value={"actions": [{"txid": "tx1", "description": "encrypted_data"}]}
        )
        mock_underlying_wallet.decrypt = AsyncMock(return_value="decrypted_data")

        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={"encryptWalletMetadata": True},
        )

        # When
        manager.list_actions({}, "user.com")

        # Then
        assert mock_underlying_wallet.list_actions.call_count == 1
        assert mock_underlying_wallet.decrypt.call_count > 0
```

### AI Analysis Results

**Similarity Score**: 17.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.listActions
  - [HIGH] Python test is missing operations: manager.listActions

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 1, PY has 2

**Suggestions:**
  - Add verifications for: underlying.listActions
  - Add operations: manager.listActions

**Explanation:**

Overall Similarity: 17.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: decryption verification method_call_verification encryption
  • Python: decryption verification encryption

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.listActions
  • [HIGH] Python test is missing operations: manager.listActions

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 1, PY has 2

---

## Test 89: should call listCertificates, verifying permission if config.seekCertificateListingPermissions=true **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should call listCertificates, verifying permission if config.seekCertificateListingPermissions=true', async () => {
    const result = await manager.listCertificates(
      {
        privileged: false,
        certifiers: [],
        types: []
      },
      'some.corp'
    )
    expect(underlying.listCertificates).toHaveBeenCalledTimes(1)
    expect(result.totalCertificates).toBe(0)
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_call_listcertificates_verifying_permission_if_config_seekcertificatelistingpermissions_true(
        self,
    ) -> None:
        """Given: Manager with certificate listing permissions
           When: listCertificates is called
           Then: Checks permissions, calls underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should call listCertificates, verifying permission if config.seekCertificateListingPermissions=true')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.list_certificates = AsyncMock(return_value={"certificates": []})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={"seekCertificateListingPermissions": True},
        )

        async def auto_grant(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onCertificateAccessRequested", auto_grant)

        # When
        manager.list_certificates({"certifiers": ["certifier"], "types": ["type"]}, "user.com")

        # Then
        assert mock_underlying_wallet.list_certificates.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: result.totalCertificates, underlying.listCertificates
  - [HIGH] Python test is missing operations: manager.listCertificates

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: result.totalCertificates, underlying.listCertificates
  - Add operations: manager.listCertificates

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: result.totalCertificates, underlying.listCertificates
  • [HIGH] Python test is missing operations: manager.listCertificates

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 90: should call proveCertificate after ensuring certificate permission **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should call proveCertificate after ensuring certificate permission', async () => {
    const result = await manager.proveCertificate(
      {
        privileged: true,
        verifier: '02vvvv',
        certificate: {
          type: 'kyc',
          subject: '02aaaa...',
          certifier: '02cccc...',
          fields: { name: 'Alice' }
        },
        fieldsToReveal: ['name']
      },
      'user.corp'
    )
    expect(underlying.proveCertificate).toHaveBeenCalledTimes(1)
    expect(result.keyringForVerifier).toBeDefined()
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_call_provecertificate_after_ensuring_certificate_permission(self) -> None:
        """Given: Manager with certificate disclosure permissions
           When: proveCertificate is called
           Then: Checks permissions, calls underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should call proveCertificate after ensuring certificate permission')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.prove_certificate = AsyncMock(return_value={"proof": "data"})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={"seekCertificateDisclosurePermissions": True},
        )

        async def auto_grant(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onCertificateAccessRequested", auto_grant)

        # When
        manager.prove_certificate({"type": "type", "certifier": "certifier", "serialNumber": "123"}, "user.com")

        # Then
        assert mock_underlying_wallet.prove_certificate.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: result.keyringForVerifier, underlying.proveCertificate
  - [HIGH] Python test is missing operations: manager.proveCertificate

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: result.keyringForVerifier, underlying.proveCertificate
  - Add operations: manager.proveCertificate

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: result.keyringForVerifier, underlying.proveCertificate
  • [HIGH] Python test is missing operations: manager.proveCertificate

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 91: should call relinquishCertificate if config.seekCertificateRelinquishmentPermissions=true **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should call relinquishCertificate if config.seekCertificateRelinquishmentPermissions=true', async () => {
    const result = await manager.relinquishCertificate(
      {
        type: 'some-cert',
        serialNumber: 'raisin bran',
        certifier: '023333'
      },
      'user-abc.com'
    )
    expect(underlying.relinquishCertificate).toHaveBeenCalledTimes(1)
    expect(result).toEqual({ relinquished: true })
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_call_relinquishcertificate_if_config_seekcertificaterelinquishmentpermissions_true(
        self,
    ) -> None:
        """Given: Manager with certificate relinquishment permissions
           When: relinquishCertificate is called
           Then: Checks permissions, calls underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should call relinquishCertificate if config.seekCertificateRelinquishmentPermissions=true')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.relinquish_certificate = AsyncMock(return_value={"relinquished": True})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={"seekCertificateRelinquishmentPermissions": True},
        )

        async def auto_grant(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onCertificateAccessRequested", auto_grant)

        # When
        manager.relinquish_certificate({"type": "type", "certifier": "certifier", "serialNumber": "123"}, "user.com")

        # Then
        assert mock_underlying_wallet.relinquish_certificate.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.relinquishCertificate
  - [HIGH] Python test is missing operations: manager.relinquishCertificate

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: underlying.relinquishCertificate
  - Add operations: manager.relinquishCertificate

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.relinquishCertificate
  • [HIGH] Python test is missing operations: manager.relinquishCertificate

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 92: should call revealCounterpartyKeyLinkage with permission check, pass result **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should call revealCounterpartyKeyLinkage with permission check, pass result', async () => {
    const result = await manager.revealCounterpartyKeyLinkage(
      {
        privileged: true,
        verifier: '0222aaa',
        counterparty: '02bbbccc',
        privilegedReason: 'test reason'
      },
      'user.example.com'
    )

    expect(underlying.revealCounterpartyKeyLinkage).toHaveBeenCalledTimes(1)
    expect(underlying.revealCounterpartyKeyLinkage).toHaveBeenCalledWith(
      {
        privileged: true,
        verifier: '0222aaa',
        counterparty: '02bbbccc',
        privilegedReason: 'test reason'
      },
      'user.example.com'
    )
    expect(result.prover).toBe('02abcdef...')
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_call_revealcounterpartykeylinkage_with_permission_check_pass_result(self) -> None:
        """Given: Manager with key linkage permissions
           When: revealCounterpartyKeyLinkage is called
           Then: Checks permissions, calls underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should call revealCounterpartyKeyLinkage with permission check, pass result')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.reveal_counterparty_key_linkage = AsyncMock(return_value={"linkage": "data"})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={"seekPermissionsForKeyLinkageRevelation": True},
        )

        async def auto_grant(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onProtocolPermissionRequested", auto_grant)

        # When
        manager.reveal_counterparty_key_linkage({"protocolID": [1, "proto"], "counterparty": "user"}, "user.com")

        # Then
        assert mock_underlying_wallet.reveal_counterparty_key_linkage.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: result.prover, underlying.revealCounterpartyKeyLinkage
  - [HIGH] Python test is missing operations: manager.revealCounterpartyKeyLinkage

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 3, PY has 1

**Suggestions:**
  - Add verifications for: result.prover, underlying.revealCounterpartyKeyLinkage
  - Add operations: manager.revealCounterpartyKeyLinkage

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: result.prover, underlying.revealCounterpartyKeyLinkage
  • [HIGH] Python test is missing operations: manager.revealCounterpartyKeyLinkage

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 3, PY has 1

---

## Test 93: should call revealSpecificKeyLinkage with permission check, pass result **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should call revealSpecificKeyLinkage with permission check, pass result', async () => {
    const result = await manager.revealSpecificKeyLinkage(
      {
        privileged: false,
        verifier: '0222ddd',
        protocolID: [2, 'special'],
        keyID: '5',
        counterparty: '022222',
        privilegedReason: 'need to check link'
      },
      'user.example.com'
    )

    expect(underlying.revealSpecificKeyLinkage).toHaveBeenCalledTimes(1)
    expect(underlying.revealSpecificKeyLinkage).toHaveBeenCalledWith(
      {
        privileged: false,
        verifier: '0222ddd',
        protocolID: [2, 'special'],
        keyID: '5',
        counterparty: '022222',
        privilegedReason: 'need to check link'
      },
      'user.example.com'
    )
    expect(result.prover).toBe('02abcdef...')
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_call_revealspecifickeylinkage_with_permission_check_pass_result(self) -> None:
        """Given: Manager with key linkage permissions
           When: revealSpecificKeyLinkage is called
           Then: Checks permissions, calls underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should call revealSpecificKeyLinkage with permission check, pass result')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.reveal_specific_key_linkage = AsyncMock(return_value={"linkage": "specific"})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={"seekPermissionsForKeyLinkageRevelation": True},
        )

        async def auto_grant(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onProtocolPermissionRequested", auto_grant)

        # When
        manager.reveal_specific_key_linkage(
            {"protocolID": [1, "proto"], "counterparty": "user", "verifier": "v"}, "user.com"
        )

        # Then
        assert mock_underlying_wallet.reveal_specific_key_linkage.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: result.prover, underlying.revealSpecificKeyLinkage
  - [HIGH] Python test is missing operations: manager.revealSpecificKeyLinkage

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 3, PY has 1

**Suggestions:**
  - Add verifications for: result.prover, underlying.revealSpecificKeyLinkage
  - Add operations: manager.revealSpecificKeyLinkage

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: result.prover, underlying.revealSpecificKeyLinkage
  • [HIGH] Python test is missing operations: manager.revealSpecificKeyLinkage

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 3, PY has 1

---

## Test 94: should ensure basket listing permission then call listOutputs, decrypting customInstructions **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should ensure basket listing permission then call listOutputs, decrypting customInstructions', async () => {
    jest.spyOn(MockedBSV_SDK.Transaction, 'fromBEEF').mockImplementation(() => {
      const mockTx = new MockTransaction()
      // Add outputs with lockingScript
      mockTx.outputs = [
        {
          lockingScript: {
            // Ensure this matches what PushDrop.decode expects to work with
            toHex: () => 'mockLockingScriptHex'
          }
        }
      ]
      return mockTx
    })

    underlying.listOutputs.mockResolvedValue({
      totalOutputs: 1,
      outputs: [
        {
          outpoint: 'zzz.0',
          satoshis: 100,
          lockingScript: 'mockscript',
          customInstructions: 'EncryptedWeird'
        }
      ]
    })

    const result = await manager.listOutputs({ basket: 'user-basket' }, 'app.example.com')
    // manager ephemeral-grants basket permission
    expect(underlying.listOutputs).toHaveBeenCalledTimes(2)
    expect(underlying.listOutputs.mock.calls).toEqual([
      [
        {
          basket: 'admin basket-access',
          include: 'entire transactions',
          tagQueryMode: 'all',
          tags: ['originator app.example.com', 'basket user-basket']
        },
        'admin.test' // querying to see if we have permission
      ],
      [
        {
          basket: 'user-basket'
        },
        'app.example.com' // the actual underlying call
      ]
    ])
    expect(result.outputs[0].customInstructions).toBe('*****') // from [42,42] decryption
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_ensure_basket_listing_permission_then_call_listoutputs_decrypting_custominstructions(
        self,
    ) -> None:
        """Given: Manager with basket listing permissions
           When: listOutputs is called
           Then: Checks permissions, calls underlying, decrypts customInstructions

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should ensure basket listing permission then call listOutputs, decrypting customInstructions')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.list_outputs = AsyncMock(return_value={"outputs": [{"customInstructions": "encrypted"}]})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={"seekBasketListingPermissions": True},
        )

        async def auto_grant(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onBasketAccessRequested", auto_grant)

        # When
        manager.list_outputs({"basket": "my-basket"}, "user.com")

        # Then
        assert mock_underlying_wallet.list_outputs.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 17.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.listOutputs
  - [HIGH] Python test is missing operations: manager.listOutputs

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: underlying.listOutputs
  - Add operations: manager.listOutputs

**Explanation:**

Overall Similarity: 17.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: decryption verification method_call_verification encryption
  • Python: decryption verification encryption

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.listOutputs
  • [HIGH] Python test is missing operations: manager.listOutputs

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 95: should ensure basket removal permission then call relinquishOutput **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should ensure basket removal permission then call relinquishOutput', async () => {
    await manager.relinquishOutput(
      {
        output: 'xxx.0',
        basket: 'some-basket'
      },
      'nonadmin.com'
    )
    expect(underlying.relinquishOutput).toHaveBeenCalledTimes(1)
    expect(underlying.relinquishOutput).toHaveBeenCalledWith({ output: 'xxx.0', basket: 'some-basket' }, 'nonadmin.com')
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_ensure_basket_removal_permission_then_call_relinquishoutput(self) -> None:
        """Given: Manager with basket removal permissions
           When: relinquishOutput is called
           Then: Checks permissions, calls underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should ensure basket removal permission then call relinquishOutput')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.relinquish_output = AsyncMock(return_value={"removed": True})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={"seekBasketRemovalPermissions": True},
        )

        async def auto_grant(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onBasketAccessRequested", auto_grant)

        # When
        manager.relinquish_output({"basket": "my-basket", "output": "tx.0"}, "user.com")

        # Then
        assert mock_underlying_wallet.relinquish_output.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.relinquishOutput
  - [HIGH] Python test is missing operations: manager.relinquishOutput

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: underlying.relinquishOutput
  - Add operations: manager.relinquishOutput

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.relinquishOutput
  • [HIGH] Python test is missing operations: manager.relinquishOutput

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 96: should pass createAction calls through, label them, handle metadata encryption, and check spending authorization **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should pass createAction calls through, label them, handle metadata encryption, and check spending authorization', async () => {
    // We'll mock the "netSpent" scenario to be >0 by returning some mock input & output satoshis from the signableTransaction.
    // The underlying mock createAction returns a signableTransaction with tx = []
    // We can stub out the mock so that the manager sees inputs/outputs with certain sat amounts.
    // But we have to remember the manager is parsing the signableTransaction via fromAtomicBEEF(…).
    // We'll control that by adjusting the mock signableTransaction in the underlying.

    // let's set a custom signableTransaction that returns 500 sat in inputs, 1000 in outputs, and 100 in fee
    underlying.createAction.mockResolvedValueOnce({
      signableTransaction: {
        // The manager calls Transaction.fromAtomicBEEF() on this
        tx: [0xde, 0xad], // not used in detail, but let's just pass some array
        reference: 'test-ref'
      }
    })

    // We also need to configure the fromAtomicBEEF mock so it returns a transaction with the specified inputs/outputs
    const mockTx = new MockTransaction()
    mockTx.fee = 100
    // We'll define exactly one input we consider "originator-provided" with 500 sat
    mockTx.inputs = [
      {
        sourceTXID: 'aaa',
        sourceOutputIndex: 0,
        sourceTransaction: {
          outputs: [{ satoshis: 500 }]
        }
      }
    ]
    // We'll define 2 outputs. The manager will read the output amounts from the createAction call's "args.outputs" too,
    // but we also set them here in case it cross-references them. We'll keep it consistent (2 outputs with total 1000).
    mockTx.outputs = [{ satoshis: 600 }, { satoshis: 400 }]

    // Now override fromAtomicBEEF to return our mockTx:
    ;(MockedBSV_SDK.Transaction.fromAtomicBEEF as jest.Mock).mockReturnValue(mockTx)

    // Attempt to create an action from a non-admin origin
    await manager.createAction(
      {
        description: 'User purchase',
        inputs: [
          {
            outpoint: 'aaa.0',
            unlockingScriptLength: 73,
            inputDescription: 'My input'
          }
        ],
        outputs: [
          {
            lockingScript: '00abcd',
            satoshis: 1000,
            outputDescription: 'Purchase output',
            basket: 'my-basket'
          }
        ],
        labels: ['user-label', 'something-else']
      },
      'shop.example.com'
    )

    // The manager should have:
    // 1) Called underlying.createAction
    // 2) Inserted "admin originator shop.example.com" & "admin month YYYY-MM" into labels
    // 3) Encrypted the metadata fields (description, inputDescription, outputDescription)
    // 4) Ensured we needed spending permission for netSpent= (1000 + fee100) - 500 = 600
    //    The onSpendingAuthorizationRequested callback ephemeral-granted it.
    expect(underlying.createAction).toHaveBeenCalledTimes(1)
    const callArgs = underlying.createAction.mock.calls[0][0]
    expect(callArgs.labels).toContain('admin originator shop.example.com')
    expect(callArgs.labels).toEqual(
      expect.arrayContaining([
        expect.stringContaining('admin month'),
        'user-label',
        'something-else',
        'admin originator shop.example.com'
      ])
    )
    // Confirm the metadata was replaced with some ciphertext array in createAction call
    expect(callArgs.description).not.toBe('User purchase') // manager encrypts it
    if (callArgs.inputs[0].inputDescription) {
      expect(callArgs.inputs[0].inputDescription).not.toBe('My input')
    }
    if (callArgs.outputs[0].outputDescription) {
      expect(callArgs.outputs[0].outputDescription).not.toBe('Purchase output')
    }

    // Also confirm we set signAndProcess to false if origin is non-admin
    expect(callArgs.options.signAndProcess).toBe(false)

    // The manager will parse the resulting signableTransaction, see netSpent=600, and request spending permission.
    // Our callback ephemeral-granted.  So everything should proceed with no error.
    // The manager returns the partial result from underlying
    // We don't have a final sign call from the manager because signAndProcess is forcibly false.
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_pass_createaction_calls_through_label_them_handle_metadata_encryption_and_check_spending_authorization(
        self,
    ) -> None:
        """Given: Manager with underlying wallet, non-admin creates action
           When: Call createAction with basket, labels, and metadata
           Then: Passes through with admin labels, encrypted metadata, spending auth checked

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should pass createAction calls through, label them, handle metadata encryption, and check spending authorization')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_action = AsyncMock(
            return_value={"signableTransaction": {"tx": [0xDE, 0xAD], "reference": "test-ref"}}
        )

        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={
                "seekSpendingPermissions": True,
                "encryptWalletMetadata": True,
                "seekBasketInsertionPermissions": True,
            },
        )

        # Auto-grant all permissions
        async def auto_grant(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onProtocolPermissionRequested", auto_grant)
        manager.bind_callback("onBasketAccessRequested", auto_grant)
        manager.bind_callback("onSpendingAuthorizationRequested", auto_grant)

        # When
        manager.create_action(
            {
                "description": "User purchase",
                "inputs": [{"outpoint": "aaa.0", "unlockingScriptLength": 73, "inputDescription": "My input"}],
                "outputs": [
                    {
                        "lockingScript": "00abcd",
                        "satoshis": 1000,
                        "outputDescription": "Purchase output",
                        "basket": "my-basket",
                    }
                ],
                "labels": ["user-label", "something-else"],
            },
            "shop.example.com",
        )

        # Then
        assert mock_underlying_wallet.create_action.call_count == 1
        call_args = mock_underlying_wallet.create_action.call_args[0][0]
        assert "admin originator shop.example.com" in call_args["labels"]
        assert "user-label" in call_args["labels"]
        assert "something-else" in call_args["labels"]
        # Metadata should be encrypted (non-empty, different from plaintext)
        assert call_args.get("description") != "User purchase"  # encrypted
```

### AI Analysis Results

**Similarity Score**: 27.00%
  - Structural: 0.00%
  - Semantic: 54.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createAction, call_args.labels
  - [HIGH] Python test is missing operations: manager.createAction

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 3, PY has 5

**Suggestions:**
  - Add verifications for: underlying.createAction, call_args.labels
  - Add operations: manager.createAction

**Explanation:**

Overall Similarity: 27.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 54.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: authentication method_call_verification verification value_verification encryption
  • Python: verification encryption

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.createAction, call_args.labels
  • [HIGH] Python test is missing operations: manager.createAction

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 3, PY has 5

---

## Test 97: should pass internalizeAction calls to underlying, after ensuring basket permissions and encrypting customInstructions if config=on **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should pass internalizeAction calls to underlying, after ensuring basket permissions and encrypting customInstructions if config=on', async () => {
    await manager.internalizeAction(
      {
        tx: [],
        description: 'Internalizing outputs with basket insertion',
        outputs: [
          {
            outputIndex: 0,
            protocol: 'basket insertion',
            insertionRemittance: {
              basket: 'some-basket',
              customInstructions: 'plaintext instructions'
            }
          }
        ]
      },
      'someuser.com'
    )

    // The manager ensures basket insertion => ephemeral permission granted
    // Then it encrypts 'plaintext instructions' before passing it to underlying
    expect(underlying.internalizeAction).toHaveBeenCalledTimes(1)
    const callArgs = underlying.internalizeAction.mock.calls[0][0]
    expect(callArgs.outputs[0].insertionRemittance.customInstructions).not.toBe('plaintext instructions')
    // There's no direct check that the string is "**" or something, because it's encrypted.
    // We just confirm it was changed from the original plaintext.
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_pass_internalizeaction_calls_to_underlying_after_ensuring_basket_permissions_and_encrypting_custominstructions_if_config_on(
        self,
    ) -> None:
        """Given: Manager with basket permissions and metadata encryption
           When: internalizeAction is called
           Then: Checks permissions, encrypts customInstructions, passes to underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should pass internalizeAction calls to underlying, after ensuring basket permissions and encrypting customInstructions if config=on')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.internalize_action = AsyncMock(return_value={"accepted": True})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={"seekBasketInsertionPermissions": True, "encryptWalletMetadata": True},
        )

        async def auto_grant(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onBasketAccessRequested", auto_grant)

        # When
        manager.internalize_action(
            {
                "tx": "rawTx",
                "outputs": [{"basket": "my-basket", "customInstructions": "instructions"}],
                "description": "Internalize",
            },
            "user.com",
        )

        # Then
        assert mock_underlying_wallet.internalize_action.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 16.00%
  - Structural: 0.00%
  - Semantic: 32.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.internalizeAction
  - [HIGH] Python test is missing operations: manager.internalizeAction

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: underlying.internalizeAction
  - Add operations: manager.internalizeAction

**Explanation:**

Overall Similarity: 16.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 32.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification method_call_verification encryption
  • Python: verification encryption

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.internalizeAction
  • [HIGH] Python test is missing operations: manager.internalizeAction

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 98: should propagate errors from the underlying wallet calls **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py`

---

## Test 99: should proxy abortAction calls directly **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should proxy abortAction calls directly', async () => {
    const result = await manager.abortAction({ reference: 'abort-me' }, 'someuser.com')
    expect(underlying.abortAction).toHaveBeenCalledTimes(1)
    expect(underlying.abortAction).toHaveBeenCalledWith({ reference: 'abort-me' }, 'someuser.com')
    expect(result).toEqual({ aborted: true })
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_proxy_abortaction_calls_directly(self) -> None:
        """Given: Manager with underlying wallet
           When: abortAction is called
           Then: Proxies to underlying.abortAction

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should proxy abortAction calls directly')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.abort_action = AsyncMock(return_value={"aborted": True})
        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.test")

        # When
        result = manager.abort_action({"reference": "ref-123"}, "user.com")

        # Then
        assert mock_underlying_wallet.abort_action.call_count == 1
        assert result == {"aborted": True}
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.abortAction
  - [HIGH] Python test is missing operations: manager.abortAction

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: underlying.abortAction
  - Add operations: manager.abortAction

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.abortAction
  • [HIGH] Python test is missing operations: manager.abortAction

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 100: should proxy createHmac() calls **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should proxy createHmac() calls', async () => {
    const result = await manager.createHmac(
      {
        protocolID: [2, 'hmac-proto'],
        data: [11, 22],
        keyID: 'hmacKey'
      },
      'someone.com'
    )
    expect(underlying.createHmac).toHaveBeenCalledTimes(1)
    expect(result.hmac).toEqual([0xaa])
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_proxy_createhmac_calls(self) -> None:
        """Given: Manager with underlying wallet
           When: createHmac is called
           Then: Checks permissions, proxies to underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should proxy createHmac() calls')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_hmac = AsyncMock(return_value={"hmac": "mac"})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={"seekProtocolPermissionsForHMAC": True},
        )

        async def auto_grant(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onProtocolPermissionRequested", auto_grant)

        # When
        manager.create_hmac({"protocolID": [1, "proto"], "data": "data"}, "user.com")

        # Then
        assert mock_underlying_wallet.create_hmac.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createHmac, result.hmac
  - [HIGH] Python test is missing operations: manager.createHmac

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: underlying.createHmac, result.hmac
  - Add operations: manager.createHmac

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.createHmac, result.hmac
  • [HIGH] Python test is missing operations: manager.createHmac

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 101: should proxy createSignature() calls (already tested the netSpent logic in createAction, but let’s double-check) **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should proxy createSignature() calls (already tested the netSpent logic in createAction, but let’s double-check)', async () => {
    // We tested permission checks for signing in earlier tests, but let's confirm pass-through
    const result = await manager.createSignature(
      {
        protocolID: [1, 'sign-proto'],
        data: [10, 20],
        keyID: '1'
      },
      'user.com'
    )
    expect(underlying.createSignature).toHaveBeenCalledTimes(1)
    expect(result.signature).toEqual([0x30, 0x44])
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_proxy_createsignature_calls_already_tested_the_netspent_logic_in_createaction_but_lets_double_check(
        self,
    ) -> None:
        """Given: Manager with underlying wallet
           When: createSignature is called
           Then: Checks permissions, proxies to underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should proxy createSignature() calls (already tested the netSpent logic in createAction, but let's double-check)')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_signature = AsyncMock(return_value={"signature": "sig"})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={"seekProtocolPermissionsForSigning": True},
        )

        async def auto_grant(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onProtocolPermissionRequested", auto_grant)

        # When
        manager.create_signature({"protocolID": [1, "proto"], "data": [1, 2, 3]}, "user.com")

        # Then
        assert mock_underlying_wallet.create_signature.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: result.signature, underlying.createSignature
  - [HIGH] Python test is missing operations: manager.createSignature

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: result.signature, underlying.createSignature
  - Add operations: manager.createSignature

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: result.signature, underlying.createSignature
  • [HIGH] Python test is missing operations: manager.createSignature

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 102: should proxy decrypt() calls after checking protocol permission **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should proxy decrypt() calls after checking protocol permission', async () => {
    const result = await manager.decrypt(
      {
        protocolID: [1, 'secret-proto'],
        ciphertext: [99, 99],
        keyID: 'somekey'
      },
      'user.example.com'
    )
    expect(underlying.decrypt).toHaveBeenCalledTimes(1)
    expect(result.plaintext).toEqual([42, 42, 42, 42, 42])
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_proxy_decrypt_calls_after_checking_protocol_permission(self) -> None:
        """Given: Manager with protocol permissions
           When: decrypt is called
           Then: Checks permissions, calls underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should proxy decrypt() calls after checking protocol permission')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.decrypt = AsyncMock(return_value={"plaintext": "decrypted"})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={"seekProtocolPermissionsForEncrypting": True},
        )

        async def auto_grant(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onProtocolPermissionRequested", auto_grant)

        # When
        manager.decrypt({"protocolID": [1, "proto"], "ciphertext": "encrypted"}, "user.com")

        # Then
        assert mock_underlying_wallet.decrypt.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.decrypt, result.plaintext
  - [HIGH] Python test is missing operations: manager.decrypt

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: underlying.decrypt, result.plaintext
  - Add operations: manager.decrypt

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification decryption verification method_call_verification
  • Python: decryption verification encryption

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.decrypt, result.plaintext
  • [HIGH] Python test is missing operations: manager.decrypt

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 103: should proxy encrypt() calls after checking protocol permission **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should proxy encrypt() calls after checking protocol permission', async () => {
    const result = await manager.encrypt(
      {
        protocolID: [1, 'secret-proto'],
        plaintext: [1, 2, 3],
        keyID: 'mykey'
      },
      'user.example.com'
    )

    expect(underlying.encrypt).toHaveBeenCalledTimes(1)
    expect(result.ciphertext).toEqual([42, 42, 42, 42, 42, 42, 42]) // from the mock
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_proxy_encrypt_calls_after_checking_protocol_permission(self) -> None:
        """Given: Manager with protocol permissions
           When: encrypt is called
           Then: Checks permissions, calls underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should proxy encrypt() calls after checking protocol permission')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.encrypt = AsyncMock(return_value={"ciphertext": "encrypted"})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet,
            admin_originator="admin.test",
            config={"seekProtocolPermissionsForEncrypting": True},
        )

        async def auto_grant(request) -> None:
            manager.grant_permission({"requestID": request["requestID"], "ephemeral": True})

        manager.bind_callback("onProtocolPermissionRequested", auto_grant)

        # When
        manager.encrypt({"protocolID": [1, "proto"], "plaintext": "data"}, "user.com")

        # Then
        assert mock_underlying_wallet.encrypt.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: result.ciphertext, underlying.encrypt
  - [HIGH] Python test is missing operations: manager.encrypt

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: result.ciphertext, underlying.encrypt
  - Add operations: manager.encrypt

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification encryption
  • Python: verification encryption

Critical Issues (2):
  • [HIGH] Python test is missing verifications: result.ciphertext, underlying.encrypt
  • [HIGH] Python test is missing operations: manager.encrypt

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 104: should proxy getHeaderForHeight **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should proxy getHeaderForHeight', async () => {
    const result = await manager.getHeaderForHeight({ height: 100000 }, 'someone.com')
    expect(result.header).toMatch(/000000000000abc/)
    expect(underlying.getHeaderForHeight).toHaveBeenCalledTimes(1)
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_proxy_getheaderforheight(self) -> None:
        """Given: Manager with underlying wallet
           When: getHeaderForHeight is called
           Then: Proxies directly to underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should proxy getHeaderForHeight')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.get_header_for_height = AsyncMock(return_value={"header": "header"})
        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.test")

        # When
        result = manager.get_header_for_height({"height": 100}, "user.com")

        # Then
        assert mock_underlying_wallet.get_header_for_height.call_count == 1
        assert result == {"header": "header"}
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: result.header, underlying.getHeaderForHeight
  - [HIGH] Python test is missing operations: manager.getHeaderForHeight

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: result.header, underlying.getHeaderForHeight
  - Add operations: manager.getHeaderForHeight

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: result.header, underlying.getHeaderForHeight
  • [HIGH] Python test is missing operations: manager.getHeaderForHeight

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 105: should proxy getHeight **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should proxy getHeight', async () => {
    const result = await manager.getHeight({}, 'someone.com')
    expect(result.height).toBe(777777)
    expect(underlying.getHeight).toHaveBeenCalledTimes(1)
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_proxy_getheight(self) -> None:
        """Given: Manager with underlying wallet
           When: getHeight is called
           Then: Proxies directly to underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should proxy getHeight')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.get_height = AsyncMock(return_value={"height": 100})
        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.test")

        # When
        result = manager.get_height({}, "user.com")

        # Then
        assert mock_underlying_wallet.get_height.call_count == 1
        assert result == {"height": 100}
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: result.height, underlying.getHeight
  - [HIGH] Python test is missing operations: manager.getHeight

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: result.height, underlying.getHeight
  - Add operations: manager.getHeight

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: result.height, underlying.getHeight
  • [HIGH] Python test is missing operations: manager.getHeight

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 106: should proxy getNetwork **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should proxy getNetwork', async () => {
    const result = await manager.getNetwork({}, 'someone.com')
    expect(result.network).toBe('testnet')
    expect(underlying.getNetwork).toHaveBeenCalledTimes(1)
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_proxy_getnetwork(self) -> None:
        """Given: Manager with underlying wallet
           When: getNetwork is called
           Then: Proxies directly to underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should proxy getNetwork')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.get_network = AsyncMock(return_value={"network": "mainnet"})
        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.test")

        # When
        result = manager.get_network({}, "user.com")

        # Then
        assert mock_underlying_wallet.get_network.call_count == 1
        assert result == {"network": "mainnet"}
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.getNetwork, result.network
  - [HIGH] Python test is missing operations: manager.getNetwork

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: underlying.getNetwork, result.network
  - Add operations: manager.getNetwork

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.getNetwork, result.network
  • [HIGH] Python test is missing operations: manager.getNetwork

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 107: should proxy getVersion **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should proxy getVersion', async () => {
    const result = await manager.getVersion({}, 'someone.com')
    expect(result.version).toBe('vendor-1.0.0')
    expect(underlying.getVersion).toHaveBeenCalledTimes(1)
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_proxy_getversion(self) -> None:
        """Given: Manager with underlying wallet
           When: getVersion is called
           Then: Proxies directly to underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should proxy getVersion')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.get_version = AsyncMock(return_value={"version": "1.0.0"})
        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.test")

        # When
        result = manager.get_version({}, "user.com")

        # Then
        assert mock_underlying_wallet.get_version.call_count == 1
        assert result == {"version": "1.0.0"}
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: result.version, underlying.getVersion
  - [HIGH] Python test is missing operations: manager.getVersion

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: result.version, underlying.getVersion
  - Add operations: manager.getVersion

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: result.version, underlying.getVersion
  • [HIGH] Python test is missing operations: manager.getVersion

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 108: should proxy isAuthenticated without any special permission checks **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should proxy isAuthenticated without any special permission checks', async () => {
    const result = await manager.isAuthenticated({}, 'someone.com')
    expect(result.authenticated).toBe(true)
    expect(underlying.isAuthenticated).toHaveBeenCalledTimes(1)
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_proxy_isauthenticated_without_any_special_permission_checks(self) -> None:
        """Given: Manager with underlying wallet
           When: isAuthenticated is called
           Then: Proxies directly to underlying (no permission checks)

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should proxy isAuthenticated without any special permission checks')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.is_authenticated = AsyncMock(return_value={"authenticated": True})
        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.test")

        # When
        result = manager.is_authenticated({}, "user.com")

        # Then
        assert mock_underlying_wallet.is_authenticated.call_count == 1
        assert result == {"authenticated": True}
```

### AI Analysis Results

**Similarity Score**: 14.00%
  - Structural: 0.00%
  - Semantic: 28.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: result.authenticated, underlying.isAuthenticated
  - [HIGH] Python test is missing operations: manager.isAuthenticated

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: result.authenticated, underlying.isAuthenticated
  - Add operations: manager.isAuthenticated

**Explanation:**

Overall Similarity: 14.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 28.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: authentication value_verification verification method_call_verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: result.authenticated, underlying.isAuthenticated
  • [HIGH] Python test is missing operations: manager.isAuthenticated

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 109: should proxy signAction calls directly if invoked by the user **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should proxy signAction calls directly if invoked by the user', async () => {
    // Typically, signAction is used after createAction returns a partial signableTransaction
    // We'll confirm it passes arguments verbatim to underlying
    const result = await manager.signAction(
      {
        reference: 'my-ref',
        spends: {
          0: {
            unlockingScript: 'my-script'
          }
        }
      },
      'nonadmin.com'
    )
    expect(underlying.signAction).toHaveBeenCalledTimes(1)
    expect(underlying.signAction).toHaveBeenCalledWith(
      {
        reference: 'my-ref',
        spends: {
          0: {
            unlockingScript: 'my-script'
          }
        }
      },
      'nonadmin.com'
    )
    // returns the underlying result
    expect(result.txid).toBe('fake-txid')
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_proxy_signaction_calls_directly_if_invoked_by_the_user(self) -> None:
        """Given: Manager with underlying wallet
           When: signAction is called
           Then: Proxies to underlying.signAction

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should proxy signAction calls directly if invoked by the user')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.sign_action = AsyncMock(return_value={"rawTx": "signed"})
        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.test")

        # When
        result = manager.sign_action(
            {"reference": "my-ref", "spends": {"0": {"unlockingScript": "my-script"}}}, "nonadmin.com"
        )

        # Then
        assert mock_underlying_wallet.sign_action.call_count == 1
        assert result == {"rawTx": "signed"}
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.signAction, result.txid
  - [HIGH] Python test is missing operations: manager.signAction

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 3, PY has 1

**Suggestions:**
  - Add verifications for: underlying.signAction, result.txid
  - Add operations: manager.signAction

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.signAction, result.txid
  • [HIGH] Python test is missing operations: manager.signAction

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 3, PY has 1

---

## Test 110: should proxy verifyHmac() calls **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should proxy verifyHmac() calls', async () => {
    const result = await manager.verifyHmac(
      {
        protocolID: [2, 'hmac-proto'],
        data: [11, 22],
        hmac: [0xaa],
        keyID: 'hmacKey'
      },
      'someone.com'
    )
    expect(underlying.verifyHmac).toHaveBeenCalledTimes(1)
    expect(result.valid).toBe(true)
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_proxy_verifyhmac_calls(self) -> None:
        """Given: Manager with underlying wallet
           When: verifyHmac is called
           Then: Proxies to underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should proxy verifyHmac() calls')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.verify_hmac = AsyncMock(return_value={"valid": True})
        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.test")

        # When
        manager.verify_hmac({"protocolID": [1, "proto"], "data": "data", "hmac": "mac"}, "user.com")

        # Then
        assert mock_underlying_wallet.verify_hmac.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.verifyHmac, result.valid
  - [HIGH] Python test is missing operations: manager.verifyHmac

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: underlying.verifyHmac, result.valid
  - Add operations: manager.verifyHmac

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.verifyHmac, result.valid
  • [HIGH] Python test is missing operations: manager.verifyHmac

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 111: should proxy verifySignature() calls **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should proxy verifySignature() calls', async () => {
    const result = await manager.verifySignature(
      {
        protocolID: [1, 'verify-proto'],
        data: [3, 4],
        signature: [0x30, 0x44],
        keyID: '2'
      },
      'user.com'
    )
    expect(underlying.verifySignature).toHaveBeenCalledTimes(1)
    expect(result.valid).toBe(true)
  })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_proxy_verifysignature_calls(self) -> None:
        """Given: Manager with underlying wallet
           When: verifySignature is called
           Then: Proxies to underlying

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should proxy verifySignature() calls')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.verify_signature = AsyncMock(return_value={"valid": True})
        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.test")

        # When
        manager.verify_signature({"protocolID": [1, "proto"], "data": [1, 2, 3], "signature": "sig"}, "user.com")

        # Then
        assert mock_underlying_wallet.verify_signature.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.verifySignature, result.valid
  - [HIGH] Python test is missing operations: manager.verifySignature

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: underlying.verifySignature, result.valid
  - Add operations: manager.verifySignature

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.verifySignature, result.valid
  • [HIGH] Python test is missing operations: manager.verifySignature

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 112: should proxy waitForAuthentication without any special permission checks **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts

```typescript
  it('should proxy waitForAuthentication without any special permission checks', async () => {
    const result = await manager.waitForAuthentication({}, 'someone.com')
    expect(result.authenticated).toBe(true)
    expect(underlying.waitForAuthentication).toHaveBeenCalledTimes(1)
  }, 30000)
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py

```python
    def test_should_proxy_waitforauthentication_without_any_special_permission_checks(self) -> None:
        """Given: Manager with underlying wallet
           When: waitForAuthentication is called
           Then: Proxies directly to underlying (no permission checks)

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts
                   test('should proxy waitForAuthentication without any special permission checks')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.wait_for_authentication = AsyncMock(return_value={"authenticated": True})
        manager = WalletPermissionsManager(underlying_wallet=mock_underlying_wallet, admin_originator="admin.test")

        # When
        result = manager.wait_for_authentication({}, "user.com")

        # Then
        assert mock_underlying_wallet.wait_for_authentication.call_count == 1
        assert result == {"authenticated": True}
```

### AI Analysis Results

**Similarity Score**: 14.00%
  - Structural: 0.00%
  - Semantic: 28.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: result.authenticated, underlying.waitForAuthentication
  - [HIGH] Python test is missing operations: manager.waitForAuthentication

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: result.authenticated, underlying.waitForAuthentication
  - Add operations: manager.waitForAuthentication

**Explanation:**

Overall Similarity: 14.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 28.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: authentication value_verification verification method_call_verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: result.authenticated, underlying.waitForAuthentication
  • [HIGH] Python test is missing operations: manager.waitForAuthentication

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 113: should throw an error if a non-admin tries signAndProcess=true **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.proxying.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_proxying.py`

---

## Test 114: should allow updating the authorizedAmount in DSAP renewal **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts

```typescript
    it('should allow updating the authorizedAmount in DSAP renewal', async () => {
      const oldToken: PermissionToken = {
        tx: [],
        txid: 'dsap-old-tx',
        outputIndex: 0,
        outputScript: 'sample script',
        satoshis: 1,
        originator: 'spenderX.com',
        authorizedAmount: 10000,
        expiry: 0
      }
      const request: PermissionRequest = {
        type: 'spending',
        originator: 'spenderX.com',
        spending: { satoshis: 3000 },
        renewal: true,
        previousToken: oldToken
      }
      const key = (manager as any).buildRequestKey(request)
      ;(manager as any).activeRequests.set(key, {
        request,
        pending: [{ resolve() {}, reject() {} }]
      })

      underlying.createAction.mockClear()

      // Renew with new monthly limit 50000
      await manager.grantPermission({
        requestID: key,
        amount: 50000,
        ephemeral: false
      })

      // check
      const { inputs, outputs } = underlying.createAction.mock.calls[0][0]
      expect(inputs).toHaveLength(1)
      expect(inputs[0].outpoint).toBe('dsap-old-tx.0')

      expect(outputs).toHaveLength(1)
      expect(outputs[0].basket).toBe('admin spending-authorization')

      // domain + new authorizedAmount => 2 encryption calls
      // For metadata encryption, we have an input description, an output description, and a top-level description.
      // This makes for a total of 5 calls.
      expect(underlying.encrypt).toHaveBeenCalledTimes(5)
      // The second call’s plaintext should be "50000"
      const secondPlaintext = underlying.encrypt.mock.calls[1][0].plaintext
      const asStr = String.fromCharCode(...secondPlaintext)
      expect(asStr).toBe('50000')
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_tokens.py

```python
    def test_should_allow_updating_the_authorizedamount_in_dsap_renewal(self) -> None:
        """Given: Manager with previous DSAP token and renewal with new amount
           When: Renew spending token with updated amount
           Then: Creates new token with updated authorizedAmount field

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts
                   test('should allow updating the authorizedAmount in DSAP renewal')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.encrypt = AsyncMock(return_value={"ciphertext": [1, 2, 3]})
        mock_underlying_wallet.create_action = AsyncMock(return_value={"txid": "renewedtxid", "outputIndex": 0})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet, admin_originator="admin.domain.com"
        )

        request = {
            "type": "spending",
            "originator": "app.com",
            "spending": {"satoshis": 20000},  # Updated amount
            "reason": "renewal with new limit",
        }
        previous_token = {"txid": "olddsaptxid", "outputIndex": 0, "authorizedAmount": 10000}  # Old amount

        # When
        manager._create_permission_token(request, ephemeral=False, previous_token=previous_token)

        # Then - createAction called, amount should reflect new value
        assert mock_underlying_wallet.create_action.call_count == 1
```

### AI Analysis Results

**Similarity Score**: 17.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.encrypt
  - [HIGH] Python test is missing operations: manager.grantPermission

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: underlying.encrypt
  - Add operations: manager.grantPermission

**Explanation:**

Overall Similarity: 17.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: token_operation verification method_call_verification encryption
  • Python: token_operation verification encryption

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.encrypt
  • [HIGH] Python test is missing operations: manager.grantPermission

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 115: should build correct fields for a basket token (DBAP) **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts

```typescript
    it('should build correct fields for a basket token (DBAP)', async () => {
      const request: PermissionRequest = {
        type: 'basket',
        originator: 'origin.example',
        basket: 'someBasket',
        reason: 'basket usage'
      }
      const expiry = 999999999

      underlying.encrypt.mockClear()

      const fields: number[][] = await privateManager().buildPushdropFields(request, expiry)

      // We expect 3 encryption calls: domain, expiry, basket
      expect(underlying.encrypt).toHaveBeenCalledTimes(3)
      expect(fields).toHaveLength(3)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_tokens.py

```python
    def test_should_build_correct_fields_for_a_basket_token_dbap(self) -> None:
        """Given: Manager with basket permission request
           When: Build pushdrop fields for DBAP token
           Then: Creates 3 encrypted fields (domain, expiry, basket)

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts
                   test('should build correct fields for a basket token (DBAP)')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.encrypt = AsyncMock(return_value={"ciphertext": [1, 2, 3]})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet, admin_originator="admin.domain.com"
        )

        request = {"type": "basket", "originator": "origin.example", "basket": "someBasket", "reason": "basket usage"}
        expiry = 999999999

        # When
        fields = manager._build_pushdrop_fields(request, expiry)

        # Then - 3 encryption calls: domain, expiry, basket
        assert mock_underlying_wallet.encrypt.call_count == 3
        assert len(fields) == 3
```

### AI Analysis Results

**Similarity Score**: 47.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.encrypt

**Suggestions:**
  - Add verifications for: underlying.encrypt

**Explanation:**

Overall Similarity: 47.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: token_operation verification method_call_verification encryption
  • Python: token_operation verification encryption

Critical Issues (1):
  • [HIGH] Python test is missing verifications: underlying.encrypt

---

## Test 116: should build correct fields for a certificate token (DCAP) **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts

```typescript
    it('should build correct fields for a certificate token (DCAP)', async () => {
      const request: PermissionRequest = {
        type: 'certificate',
        originator: 'cert-user.org',
        privileged: false,
        certificate: {
          verifier: '02abcdef...',
          certType: 'KYC',
          fields: ['name', 'dob']
        },
        reason: 'certificate usage'
      }
      const expiry = 2222222222

      underlying.encrypt.mockClear()

      const fields: number[][] = await privateManager().buildPushdropFields(request, expiry)

      // DP = domain, expiry, privileged, certType, fieldsJson, verifier
      expect(underlying.encrypt).toHaveBeenCalledTimes(6)
      expect(fields).toHaveLength(6)

      // 5th encryption call is the fields JSON => ["name","dob"]
      const fifthCallPlaintext = underlying.encrypt.mock.calls[4][0].plaintext
      const str = String.fromCharCode(...fifthCallPlaintext)
      expect(str).toContain('"name"')
      expect(str).toContain('"dob"')
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_tokens.py

```python
    def test_should_build_correct_fields_for_a_certificate_token_dcap(self) -> None:
        """Given: Manager with certificate permission request
           When: Build pushdrop fields for DCAP token
           Then: Creates 6 encrypted fields (domain, expiry, privileged, certType, fieldsJson, verifier)

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts
                   test('should build correct fields for a certificate token (DCAP)')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.encrypt = AsyncMock(return_value={"ciphertext": [1, 2, 3]})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet, admin_originator="admin.domain.com"
        )

        request = {
            "type": "certificate",
            "originator": "cert-user.org",
            "privileged": False,
            "certificate": {"verifier": "02abcdef...", "certType": "KYC", "fields": ["name", "dob"]},
            "reason": "certificate usage",
        }
        expiry = 2222222222

        # When
        fields = manager._build_pushdrop_fields(request, expiry)

        # Then - 6 encryption calls: domain, expiry, privileged, certType, fieldsJson, verifier
        assert mock_underlying_wallet.encrypt.call_count == 6
        assert len(fields) == 6
```

### AI Analysis Results

**Similarity Score**: 47.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.encrypt

**Suggestions:**
  - Add verifications for: underlying.encrypt

**Explanation:**

Overall Similarity: 47.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: token_operation verification method_call_verification encryption
  • Python: token_operation verification encryption

Critical Issues (1):
  • [HIGH] Python test is missing verifications: underlying.encrypt

---

## Test 117: should build correct fields for a protocol token (DPACP) **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts

```typescript
    it('should build correct fields for a protocol token (DPACP)', async () => {
      const request: PermissionRequest = {
        type: 'protocol',
        originator: 'some-app.com',
        privileged: true,
        protocolID: [2, 'myProto'],
        counterparty: 'some-other-pubkey',
        reason: 'test-protocol-creation'
      }
      const expiry = 1234567890

      // Because manager.encryptPermissionTokenField calls underlying.encrypt,
      // we can observe how many times it's called & with what plaintext.
      underlying.encrypt.mockClear()

      const fields: number[][] = await privateManager().buildPushdropFields(request, expiry)

      // We expect 6 encryption calls (domain, expiry, privileged, secLevel, protoName, cpty).
      expect(underlying.encrypt).toHaveBeenCalledTimes(6)

      // The final array must have length=6
      expect(fields).toHaveLength(6)

      // Confirm the 1st call was the domain
      expect(underlying.encrypt.mock.calls[0][0].plaintext).toEqual(
        expect.arrayContaining([...'some-app.com'].map(c => c.charCodeAt(0)))
      )

      // Confirm the 2nd call was the expiry, as a string
      expect(underlying.encrypt.mock.calls[1][0].plaintext).toEqual(
        expect.arrayContaining([...'1234567890'].map(c => c.charCodeAt(0)))
      )

      // 3rd => privileged? 'true'
      expect(underlying.encrypt.mock.calls[2][0].plaintext).toEqual(
        expect.arrayContaining([...'true'].map(c => c.charCodeAt(0)))
      )

      // 4th => security level => '2'
      expect(underlying.encrypt.mock.calls[3][0].plaintext).toEqual(
        expect.arrayContaining([...'2'].map(c => c.charCodeAt(0)))
      )

      // 5th => protoName => 'myProto'
      expect(underlying.encrypt.mock.calls[4][0].plaintext).toEqual(
        expect.arrayContaining([...'myProto'].map(c => c.charCodeAt(0)))
      )

      // 6th => counterparty => 'some-other-pubkey'
      expect(underlying.encrypt.mock.calls[5][0].plaintext).toEqual(
        expect.arrayContaining([...'some-other-pubkey'].map(c => c.charCodeAt(0)))
      )
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_tokens.py

```python
    def test_should_build_correct_fields_for_a_protocol_token_dpacp(self) -> None:
        """Given: Manager with protocol permission request
           When: Build pushdrop fields for DPACP token
           Then: Creates 6 encrypted fields (domain, expiry, privileged, secLevel, protoName, counterparty)

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts
                   test('should build correct fields for a protocol token (DPACP)')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.encrypt = AsyncMock(return_value={"ciphertext": [1, 2, 3]})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet, admin_originator="admin.domain.com"
        )

        request = {
            "type": "protocol",
            "originator": "some-app.com",
            "privileged": True,
            "protocolID": [2, "myProto"],
            "counterparty": "some-other-pubkey",
            "reason": "test-protocol-creation",
        }
        expiry = 1234567890

        # When
        fields = manager._build_pushdrop_fields(request, expiry)

        # Then - 6 encryption calls (domain, expiry, privileged, secLevel, protoName, cpty)
        assert mock_underlying_wallet.encrypt.call_count == 6
        assert len(fields) == 6
```

### AI Analysis Results

**Similarity Score**: 47.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.encrypt

**Suggestions:**
  - Add verifications for: underlying.encrypt

**Explanation:**

Overall Similarity: 47.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: token_operation verification method_call_verification encryption
  • Python: token_operation verification encryption

Critical Issues (1):
  • [HIGH] Python test is missing verifications: underlying.encrypt

---

## Test 118: should build correct fields for a spending token (DSAP) **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts

```typescript
    it('should build correct fields for a spending token (DSAP)', async () => {
      const request: PermissionRequest = {
        type: 'spending',
        originator: 'money-spender.com',
        spending: { satoshis: 5000 },
        reason: 'monthly spending'
      }
      const expiry = 0 // DSAP typically not time-limited, but manager can pass 0.

      underlying.encrypt.mockClear()

      const fields: number[][] = await privateManager().buildPushdropFields(request, expiry, /*amount=*/ 10000)

      // For DSAP: domain + authorizedAmount (2 fields)
      expect(underlying.encrypt).toHaveBeenCalledTimes(2)
      expect(fields).toHaveLength(2)

      // The second encryption call is '10000'
      const secondPlaintext = underlying.encrypt.mock.calls[1][0].plaintext
      const asString = String.fromCharCode(...secondPlaintext)
      expect(asString).toBe('10000')
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_tokens.py

```python
    def test_should_build_correct_fields_for_a_spending_token_dsap(self) -> None:
        """Given: Manager with spending permission request
           When: Build pushdrop fields for DSAP token
           Then: Creates 2 encrypted fields (domain, authorizedAmount)

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts
                   test('should build correct fields for a spending token (DSAP)')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.encrypt = AsyncMock(return_value={"ciphertext": [1, 2, 3]})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet, admin_originator="admin.domain.com"
        )

        request = {
            "type": "spending",
            "originator": "money-spender.com",
            "spending": {"satoshis": 5000},
            "reason": "monthly spending",
        }
        expiry = 0  # DSAP typically not time-limited

        # When
        fields = manager._build_pushdrop_fields(request, expiry, amount=10000)

        # Then - 2 encryption calls: domain, authorizedAmount
        assert mock_underlying_wallet.encrypt.call_count == 2
        assert len(fields) == 2
```

### AI Analysis Results

**Similarity Score**: 47.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.encrypt

**Suggestions:**
  - Add verifications for: underlying.encrypt

**Explanation:**

Overall Similarity: 47.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: token_operation verification method_call_verification encryption
  • Python: token_operation verification encryption

Critical Issues (1):
  • [HIGH] Python test is missing verifications: underlying.encrypt

---

## Test 119: should create a new basket token (DBAP) **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts

```typescript
    it('should create a new basket token (DBAP)', async () => {
      const request: PermissionRequest = {
        type: 'basket',
        originator: 'shopper.com',
        basket: 'myBasket',
        reason: 'I want to store items'
      }
      const key = (manager as any).buildRequestKey(request)
      ;(manager as any).activeRequests.set(key, {
        request,
        pending: [{ resolve() {}, reject() {} }]
      })

      underlying.createAction.mockClear()

      await manager.grantPermission({
        requestID: key,
        ephemeral: false,
        expiry: 123456789
      })
      expect(underlying.createAction).toHaveBeenCalledTimes(1)

      const { outputs } = underlying.createAction.mock.calls[0][0]
      expect(outputs).toHaveLength(1)
      // "admin basket-access"
      expect(outputs[0].basket).toBe('admin basket-access')
      expect(outputs[0].tags).toEqual(expect.arrayContaining(['originator shopper.com', 'basket myBasket']))
      // 3 fields => domain, expiry, basket, plus two metadata calls (description, outputDescription)
      expect(underlying.encrypt).toHaveBeenCalledTimes(5)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_tokens.py

```python
    def test_should_create_a_new_basket_token_dbap(self) -> None:
        """Given: Manager with basket permission request
           When: Create basket token on chain
           Then: Calls createAction with DBAP basket and tags

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts
                   test('should create a new basket token (DBAP)')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.encrypt = AsyncMock(return_value={"ciphertext": [1, 2, 3]})
        mock_underlying_wallet.create_action = AsyncMock(return_value={"txid": "newtxid", "outputIndex": 0})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet, admin_originator="admin.domain.com"
        )

        request = {"type": "basket", "originator": "app.com", "basket": "myBasket", "reason": "test"}

        # When
        manager._create_permission_token(request, ephemeral=False, previous_token=None)

        # Then
        assert mock_underlying_wallet.create_action.call_count == 1
        call_args = mock_underlying_wallet.create_action.call_args[0][0]
        assert call_args["outputs"][0]["basket"] == "permissions_DBAP"
        assert call_args["outputs"][0]["tags"] == ["DBAP"]
```

### AI Analysis Results

**Similarity Score**: 17.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createAction, underlying.encrypt
  - [HIGH] Python test is missing operations: manager.grantPermission

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 3

**Suggestions:**
  - Add verifications for: underlying.createAction, underlying.encrypt
  - Add operations: manager.grantPermission

**Explanation:**

Overall Similarity: 17.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: token_operation verification method_call_verification encryption
  • Python: token_operation verification encryption

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.createAction, underlying.encrypt
  • [HIGH] Python test is missing operations: manager.grantPermission

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 3

---

## Test 120: should create a new certificate token (DCAP) **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts

```typescript
    it('should create a new certificate token (DCAP)', async () => {
      const request: PermissionRequest = {
        type: 'certificate',
        originator: 'org.certs',
        privileged: true,
        certificate: {
          verifier: '02cccccc',
          certType: 'KYC',
          fields: ['name', 'id', 'photo']
        },
        reason: 'Present KYC docs'
      }
      const key = (manager as any).buildRequestKey(request)
      ;(manager as any).activeRequests.set(key, {
        request,
        pending: [{ resolve() {}, reject() {} }]
      })

      underlying.createAction.mockClear()

      await manager.grantPermission({
        requestID: key,
        ephemeral: false,
        expiry: 44444444
      })

      expect(underlying.createAction).toHaveBeenCalledTimes(1)
      const { outputs } = underlying.createAction.mock.calls[0][0]
      expect(outputs[0].basket).toBe('admin certificate-access')
      expect(outputs[0].tags).toEqual(
        expect.arrayContaining(['originator org.certs', 'privileged true', 'type KYC', 'verifier 02cccccc'])
      )
      // DP = domain, expiry, privileged, certType, fieldsJson, verifier => 6 encryption calls
      // Two additional ones for metadata encryption (action description, output description) for 8 total.
      expect(underlying.encrypt).toHaveBeenCalledTimes(8)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_tokens.py

```python
    def test_should_create_a_new_certificate_token_dcap(self) -> None:
        """Given: Manager with certificate permission request
           When: Create certificate token on chain
           Then: Calls createAction with DCAP basket and tags

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts
                   test('should create a new certificate token (DCAP)')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.encrypt = AsyncMock(return_value={"ciphertext": [1, 2, 3]})
        mock_underlying_wallet.create_action = AsyncMock(return_value={"txid": "newtxid", "outputIndex": 0})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet, admin_originator="admin.domain.com"
        )

        request = {
            "type": "certificate",
            "originator": "app.com",
            "privileged": False,
            "certificate": {"verifier": "02abc", "certType": "KYC", "fields": ["name"]},
            "reason": "test",
        }

        # When
        manager._create_permission_token(request, ephemeral=False, previous_token=None)

        # Then
        assert mock_underlying_wallet.create_action.call_count == 1
        call_args = mock_underlying_wallet.create_action.call_args[0][0]
        assert call_args["outputs"][0]["basket"] == "permissions_DCAP"
        assert call_args["outputs"][0]["tags"] == ["DCAP"]
```

### AI Analysis Results

**Similarity Score**: 17.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createAction, underlying.encrypt
  - [HIGH] Python test is missing operations: manager.grantPermission

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 3

**Suggestions:**
  - Add verifications for: underlying.createAction, underlying.encrypt
  - Add operations: manager.grantPermission

**Explanation:**

Overall Similarity: 17.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: token_operation verification method_call_verification encryption
  • Python: token_operation verification encryption

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.createAction, underlying.encrypt
  • [HIGH] Python test is missing operations: manager.grantPermission

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 3

---

## Test 121: should create a new protocol token with the correct basket, script, and tags **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts

```typescript
    it('should create a new protocol token with the correct basket, script, and tags', async () => {
      // 1) Simulate the manager having an active request for a protocol token.
      const request: PermissionRequest = {
        type: 'protocol',
        originator: 'app.example',
        privileged: false,
        protocolID: [1, 'testProto'],
        counterparty: 'self',
        reason: 'Need protocol usage'
      }

      // We'll emulate that the manager queued it:
      const key = (manager as any).buildRequestKey(request)
      ;(manager as any).activeRequests.set(key, {
        request,
        pending: [{ resolve: () => {}, reject: () => {} }]
      })

      // 2) Grant the permission with ephemeral=false => must create the token
      underlying.createAction.mockClear()
      await manager.grantPermission({
        requestID: key,
        expiry: 999999, // set some expiry
        ephemeral: false
      })

      // 3) Expect createAction to have been called once with a single output
      expect(underlying.createAction).toHaveBeenCalledTimes(1)
      const actionArgs = underlying.createAction.mock.calls[0][0]
      expect(actionArgs.outputs).toHaveLength(1)

      // The basket name must be "admin protocol-permission" as per BASKET_MAP
      expect(actionArgs.outputs[0].basket).toBe('admin protocol-permission')

      // The tags must contain e.g. "originator app.example", "protocolName testProto", etc.
      const outputTags = actionArgs.outputs[0].tags
      expect(outputTags).toEqual(
        expect.arrayContaining([
          'originator app.example',
          'privileged false',
          'protocolName testProto',
          'protocolSecurityLevel 1',
          'counterparty self'
        ])
      )

      // The lockingScript is built by "PushDrop.lock(...)" with 6 fields
      const lockingScriptHex = actionArgs.outputs[0].lockingScript
      expect(lockingScriptHex).toBeTruthy()

      // Because we’re using our mock pushdrop, we might see an empty decode.
      // In a real environment, you would decode and confirm the fields. Here we just confirm
      // that the manager called the underlying encrypt 6 times, plus the script creation.
      // Two more encrypt calls should have been made within createAction (metadata encryption
      // of the top-level Action description, and the output's description) for a total of 8.
      expect(underlying.encrypt).toHaveBeenCalledTimes(8)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_tokens.py

```python
    def test_should_create_a_new_protocol_token_with_the_correct_basket_script_and_tags(self) -> None:
        """Given: Manager with protocol permission request
           When: Create protocol token on chain
           Then: Calls createAction with correct basket, lockingScript, and tags

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts
                   test('should create a new protocol token with the correct basket, script, and tags')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.encrypt = AsyncMock(return_value={"ciphertext": [1, 2, 3]})
        mock_underlying_wallet.create_action = AsyncMock(return_value={"txid": "newtxid", "outputIndex": 0})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet, admin_originator="admin.domain.com"
        )

        request = {
            "type": "protocol",
            "originator": "app.com",
            "privileged": False,
            "protocolID": [1, "test"],
            "counterparty": "self",
            "reason": "test",
        }

        # When
        manager._create_permission_token(request, ephemeral=False, previous_token=None)

        # Then - createAction called with correct parameters
        assert mock_underlying_wallet.create_action.call_count == 1
        call_args = mock_underlying_wallet.create_action.call_args[0][0]
        assert call_args["outputs"][0]["basket"] == "permissions_DPACP"
        assert "lockingScript" in call_args["outputs"][0]
        assert call_args["outputs"][0]["tags"] == ["DPACP"]
```

### AI Analysis Results

**Similarity Score**: 17.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createAction, action_args.outputs, underlying.encrypt
  - [HIGH] Python test is missing operations: manager.grantPermission

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 3, PY has 4

**Suggestions:**
  - Add verifications for: underlying.createAction, action_args.outputs, underlying.encrypt
  - Add operations: manager.grantPermission

**Explanation:**

Overall Similarity: 17.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: token_operation verification method_call_verification encryption
  • Python: token_operation verification encryption

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.createAction, action_args.outputs, underlying.encrypt
  • [HIGH] Python test is missing operations: manager.grantPermission

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 3, PY has 4

---

## Test 122: should create a new spending authorization token (DSAP) **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts

```typescript
    it('should create a new spending authorization token (DSAP)', async () => {
      const request: PermissionRequest = {
        type: 'spending',
        originator: 'spender.com',
        spending: {
          satoshis: 9999
        }
      }
      const key = (manager as any).buildRequestKey(request)
      ;(manager as any).activeRequests.set(key, {
        request,
        pending: [{ resolve() {}, reject() {} }]
      })

      underlying.createAction.mockClear()

      // We'll set "amount=20000" as the monthly limit
      await manager.grantPermission({
        requestID: key,
        ephemeral: false,
        amount: 20000
      })

      expect(underlying.createAction).toHaveBeenCalledTimes(1)
      const { outputs } = underlying.createAction.mock.calls[0][0]
      // "admin spending-authorization"
      expect(outputs[0].basket).toBe('admin spending-authorization')
      expect(outputs[0].tags).toEqual(expect.arrayContaining(['originator spender.com']))
      // domain, amount => 2 calls, plus two metadata encryption calls (description, outputDescription)
      expect(underlying.encrypt).toHaveBeenCalledTimes(4)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_tokens.py

```python
    def test_should_create_a_new_spending_authorization_token_dsap(self) -> None:
        """Given: Manager with spending permission request
           When: Create spending token on chain
           Then: Calls createAction with DSAP basket and tags

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts
                   test('should create a new spending authorization token (DSAP)')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.encrypt = AsyncMock(return_value={"ciphertext": [1, 2, 3]})
        mock_underlying_wallet.create_action = AsyncMock(return_value={"txid": "newtxid", "outputIndex": 0})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet, admin_originator="admin.domain.com"
        )

        request = {"type": "spending", "originator": "app.com", "spending": {"satoshis": 10000}, "reason": "test"}

        # When
        manager._create_permission_token(request, ephemeral=False, previous_token=None)

        # Then
        assert mock_underlying_wallet.create_action.call_count == 1
        call_args = mock_underlying_wallet.create_action.call_args[0][0]
        assert call_args["outputs"][0]["basket"] == "permissions_DSAP"
        assert call_args["outputs"][0]["tags"] == ["DSAP"]
```

### AI Analysis Results

**Similarity Score**: 17.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createAction, underlying.encrypt
  - [HIGH] Python test is missing operations: manager.grantPermission

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 3

**Suggestions:**
  - Add verifications for: underlying.createAction, underlying.encrypt
  - Add operations: manager.grantPermission

**Explanation:**

Overall Similarity: 17.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: token_operation verification method_call_verification encryption
  • Python: token_operation verification encryption

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.createAction, underlying.encrypt
  • [HIGH] Python test is missing operations: manager.grantPermission

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 3

---

## Test 123: should create a transaction that consumes (spends) the old token with no new outputs **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts

```typescript
    it('should create a transaction that consumes (spends) the old token with no new outputs', async () => {
      // A sample old token
      const oldToken: PermissionToken = {
        tx: [],
        txid: 'revocableToken.txid',
        outputIndex: 1,
        outputScript: 'fakePushdropScript',
        satoshis: 1,
        originator: 'shopper.com',
        basketName: 'myBasket',
        expiry: 1111111111
      }

      underlying.createAction.mockClear()
      underlying.signAction.mockClear()

      await manager.revokePermission(oldToken)

      // 1) The manager calls createAction with an input referencing oldToken
      expect(underlying.createAction).toHaveBeenCalledTimes(1)
      const createArgs = underlying.createAction.mock.calls[0][0]
      expect(createArgs.inputs).toHaveLength(1)
      expect(createArgs.inputs[0].outpoint).toBe('revocableToken.txid.1')

      // No new outputs => final array is empty
      expect(createArgs.outputs || []).toHaveLength(0)

      // 2) The manager then calls signAction to finalize the spending
      expect(underlying.signAction).toHaveBeenCalledTimes(1)
      const signArgs = underlying.signAction.mock.calls[0][0]
      // signArgs.reference should be the same from createAction’s result
      expect(signArgs.reference).toBe('mockReference')

      // The “spends” object should have an unlockingScript at index 0.
      expect(signArgs.spends).toHaveProperty('0.unlockingScript')
      // The content can be a mock, we just check it’s not empty
      expect(signArgs.spends[0].unlockingScript).toBeDefined()
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_tokens.py

```python
    def test_should_create_a_transaction_that_consumes_spends_the_old_token_with_no_new_outputs(self) -> None:
        """Given: Manager with previous token
           When: Revoke permission token
           Then: Creates transaction that spends old token with no new permission outputs

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts
                   test('should create a transaction that consumes (spends) the old token with no new outputs')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.create_action = AsyncMock(return_value={"txid": "revocationtxid"})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet, admin_originator="admin.domain.com"
        )

        token_to_revoke = {"txid": "tokentorevoke", "outputIndex": 0}

        # When
        manager._revoke_permission_token(token_to_revoke)

        # Then - createAction called with input (spending token) but no permission output
        assert mock_underlying_wallet.create_action.call_count == 1
        call_args = mock_underlying_wallet.create_action.call_args[0][0]
        assert len(call_args.get("inputs", [])) > 0
        assert call_args["inputs"][0]["outpoint"] == "tokentorevoke.0"
        # No new permission token outputs (just consuming the old one)
        assert len(call_args.get("outputs", [])) == 0 or all(
            "permissions_" not in o.get("basket", "") for o in call_args["outputs"]
        )
```

### AI Analysis Results

**Similarity Score**: 15.00%
  - Structural: 0.00%
  - Semantic: 30.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.signAction, sign_args.spends, sign_args.reference, create_args.inputs, underlying.createAction
  - [HIGH] Python test is missing operations: manager.revokePermission

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 5, PY has 4

**Suggestions:**
  - Add verifications for: underlying.signAction, sign_args.spends, sign_args.reference
  - Add operations: manager.revokePermission

**Explanation:**

Overall Similarity: 15.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 30.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: token_operation method_call_verification verification token_lifecycle value_verification
  • Python: token_operation verification token_lifecycle

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.signAction, sign_args.spends, sign_args.reference, create_args.inputs, underlying.createAction
  • [HIGH] Python test is missing operations: manager.revokePermission

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 5, PY has 4

---

## Test 124: should remove the old token from listing after revocation **PASS**

- TypeScript: `wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts`
- Python: `py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_tokens.py`

---

## Test 125: should spend the old token input and create a new protocol token output with updated expiry **FAIL**

### TypeScript Test: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts

```typescript
    it('should spend the old token input and create a new protocol token output with updated expiry', async () => {
      // Suppose the user has an old protocol token:
      const oldToken: PermissionToken = {
        tx: [],
        txid: 'oldTokenTX',
        outputIndex: 2,
        outputScript: '76a914...ac', // not used by the mock
        satoshis: 1,
        originator: 'some-site.io',
        expiry: 222222,
        privileged: false,
        securityLevel: 1,
        protocol: 'coolProto',
        counterparty: 'self'
      }

      // The user’s request to renew:
      const request: PermissionRequest = {
        type: 'protocol',
        originator: 'some-site.io',
        privileged: false,
        protocolID: [1, 'coolProto'],
        counterparty: 'self',
        renewal: true,
        previousToken: oldToken
      }

      // Manager normally calls requestPermissionFlow, but let's skip ahead:
      // We'll place the request in activeRequests:
      const key = (manager as any).buildRequestKey(request)
      ;(manager as any).activeRequests.set(key, {
        request,
        pending: [{ resolve() {}, reject() {} }]
      })

      // Clear the mock calls, then renew with ephemeral=false
      underlying.createAction.mockClear()

      await manager.grantPermission({
        requestID: key,
        ephemeral: false,
        expiry: 999999 // new expiry
      })

      // We expect createAction with:
      //  - 1 input referencing oldToken "oldTokenTX.2"
      //  - 1 output with the new script
      expect(underlying.createAction).toHaveBeenCalledTimes(1)
      const createArgs = underlying.createAction.mock.calls[0][0]
      expect(createArgs.inputs).toHaveLength(1)
      expect(createArgs.inputs[0].outpoint).toBe('oldTokenTX.2')
      expect(createArgs.outputs).toHaveLength(1)
      // The new basket is still "admin protocol-permission"
      expect(createArgs.outputs[0].basket).toBe('admin protocol-permission')

      // And we must confirm "renew" means 6 encryption calls again
      // Metadata encryption means three extra calls (inputDescription, outputDescription, and Action description)
      // this means a total of 9.
      expect(underlying.encrypt).toHaveBeenCalledTimes(9)
    })
```

### Python Test: py-wallet-toolbox/tests/permissions/test_wallet_permissions_manager_tokens.py

```python
    def test_should_spend_the_old_token_input_and_create_a_new_protocol_token_output_with_updated_expiry(
        self,
    ) -> None:
        """Given: Manager with previous token and renewal request
           When: Renew protocol token
           Then: Spends old token input and creates new output with updated expiry

        Reference: wallet-toolbox/src/__tests/WalletPermissionsManager.tokens.test.ts
                   test('should spend the old token input and create a new protocol token output with updated expiry')
        """
        # Given
        mock_underlying_wallet = Mock(spec=WalletInterface)
        mock_underlying_wallet.encrypt = AsyncMock(return_value={"ciphertext": [1, 2, 3]})
        mock_underlying_wallet.create_action = AsyncMock(return_value={"txid": "renewedtxid", "outputIndex": 0})
        manager = WalletPermissionsManager(
            underlying_wallet=mock_underlying_wallet, admin_originator="admin.domain.com"
        )

        request = {
            "type": "protocol",
            "originator": "app.com",
            "privileged": False,
            "protocolID": [1, "test"],
            "counterparty": "self",
            "reason": "renewal",
        }
        previous_token = {"txid": "oldtxid", "outputIndex": 0}

        # When
        manager._create_permission_token(request, ephemeral=False, previous_token=previous_token)

        # Then - createAction called with inputs (spending old token)
        assert mock_underlying_wallet.create_action.call_count == 1
        call_args = mock_underlying_wallet.create_action.call_args[0][0]
        assert len(call_args.get("inputs", [])) > 0
        assert call_args["inputs"][0]["outpoint"] == "oldtxid.0"
```

### AI Analysis Results

**Similarity Score**: 17.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: underlying.createAction, create_args.outputs, create_args.inputs, underlying.encrypt
  - [HIGH] Python test is missing operations: manager.grantPermission

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 4, PY has 3

**Suggestions:**
  - Add verifications for: underlying.createAction, create_args.outputs, create_args.inputs
  - Add operations: manager.grantPermission

**Explanation:**

Overall Similarity: 17.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: token_operation verification method_call_verification encryption
  • Python: token_operation verification encryption

Critical Issues (2):
  • [HIGH] Python test is missing verifications: underlying.createAction, create_args.outputs, create_args.inputs, underlying.encrypt
  • [HIGH] Python test is missing operations: manager.grantPermission

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 4, PY has 3

---

## Test 126: 2a complete flow MasterCertificate and VerifiableCertificate **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/CertificateLifeCycle.test.ts`
- Python: `py-wallet-toolbox/tests/certificates/test_certificate_life_cycle.py`

---

## Test 127: Calls keyGetter only once if getPrivilegedKey is invoked multiple times within retention period **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_privileged_key_manager.py`

---

## Test 128: Computes HMAC over messages verifiable by the counterparty **FAIL**

### TypeScript Test: wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts

```typescript
  it('Computes HMAC over messages verifiable by the counterparty', async () => {
    const userKey = PrivateKey.fromRandom()
    const counterpartyKey = PrivateKey.fromRandom()
    const user = new PrivilegedKeyManager(async () => userKey)
    const counterparty = new PrivilegedKeyManager(async () => counterpartyKey)
    const { hmac } = await user.createHmac({
      data: sampleData,
      protocolID: [2, 'tests'],
      keyID: '4',
      counterparty: counterpartyKey.toPublicKey().toString()
    })
    const { valid } = await counterparty.verifyHmac({
      hmac,
      data: sampleData,
      protocolID: [2, 'tests'],
      keyID: '4',
      counterparty: userKey.toPublicKey().toString()
    })
    expect(valid).toEqual(true)
    expect(hmac.length).toEqual(32)
    await user.destroyKey()
    await counterparty.destroyKey()
  })
```

### Python Test: py-wallet-toolbox/tests/integration/test_privileged_key_manager.py

```python
    async def test_computes_hmac_over_messages_verifiable_by_the_counterparty(self) -> None:
        """Given: User and counterparty wallets
           When: User computes HMAC
           Then: Counterparty verifies HMAC successfully

        Reference: wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts
                   test('Computes HMAC over messages verifiable by the counterparty')
        """
        # Given
        user_key = PrivateKey.from_random()
        counterparty_key = PrivateKey.from_random()
        user = PrivilegedKeyManager(lambda: user_key)
        counterparty = PrivilegedKeyManager(lambda: counterparty_key)

        # When
        hmac_result = await user.create_hmac(
            {
                "data": SAMPLE_DATA,
                "protocolID": [2, "tests"],
                "keyID": "4",
                "counterparty": counterparty_key.to_public_key().to_string(),
            }
        )
        verified = await counterparty.verify_hmac(
            {
                "hmac": hmac_result["hmac"],
                "data": SAMPLE_DATA,
                "protocolID": [2, "tests"],
                "keyID": "4",
                "counterparty": user_key.to_public_key().to_string(),
            }
        )

        # Then
        assert verified["valid"] is True
        assert len(hmac_result["hmac"]) == 32
        await user.destroy_key()
        await counterparty.destroy_key()
```

### AI Analysis Results

**Similarity Score**: 43.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: hmac.length
  - [HIGH] Python test is missing operations: user.destroyKey, counterparty.destroyKey, counterparty.verifyHmac, user.createHmac

**Differences:**
  - Verification count: TS has 1, PY has 2

**Suggestions:**
  - Add verifications for: hmac.length
  - Add operations: user.destroyKey, counterparty.destroyKey, counterparty.verifyHmac

**Explanation:**

Overall Similarity: 43.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: hmac.length
  • [HIGH] Python test is missing operations: user.destroyKey, counterparty.destroyKey, counterparty.verifyHmac, user.createHmac

Key Differences:
  • Verification count: TS has 1, PY has 2

---

## Test 129: Correctly derives keys for a counterparty **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_privileged_key_manager.py`

---

## Test 130: Destroys key after retention period elapses **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_privileged_key_manager.py`

---

## Test 131: Directly signs hash of message verifiable by the counterparty **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_privileged_key_manager.py`

---

## Test 132: Encrypts messages decryptable by the counterparty **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_privileged_key_manager.py`

---

## Test 133: Ensures chunk-splitting logic is correct for a 32-byte key **FAIL**

### TypeScript Test: wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts

```typescript
    it('Ensures chunk-splitting logic is correct for a 32-byte key', async () => {
      const km = new PrivilegedKeyManager(async () => new PrivateKey(1), 5000)

      const testBytes = new Uint8Array(32)
      // Fill with some pattern, e.g. 0..31
      testBytes.forEach((_, i) => {
        testBytes[i] = i
      })

      const chunks = (km as any).splitKeyIntoChunks(testBytes)
      expect(chunks.length).toBe((km as any).CHUNK_COUNT)

      // By default CHUNK_COUNT = 4
      // Typically each chunk would be 8 bytes (for a 32-byte key).
      chunks.forEach((chunk: Uint8Array, i: number) => {
        if (i < 3) {
          expect(chunk.length).toBe(8)
        } else {
          // last chunk picks up leftover
          expect(chunk.length).toBe(8)
        }
      })

      // Reassemble logic typically is done by reassembleKeyFromChunks,
      // but let's test it in isolation. We'll XOR with random pads,
      // store them, reassemble, etc.

      // For demonstration, we can do a quick test:
      const pad = chunks.map((c: Uint8Array) => Uint8Array.from(Random(c.length)))
      const obfuscated = chunks.map((c: Uint8Array, i: number) => (km as any).xorBytes(c, pad[i]))

      // Then "store" and reassemble
      ;(km as any).chunkPropNames = []
      ;(km as any).chunkPadPropNames = []
      obfuscated.forEach((obf: Uint8Array, i: number) => {
        const chunkProp = `chunk${i}`
        const padProp = `pad${i}`
        ;(km as any).chunkPropNames.push(chunkProp)
        ;(km as any).chunkPadPropNames.push(padProp)
        ;(km as any)[chunkProp] = obf
        ;(km as any)[padProp] = pad[i]
      })
      const reassembled = (km as any).reassembleKeyFromChunks()
      expect(reassembled.length).toBe(32)
      expect(Array.from(reassembled)).toEqual(Array.from(testBytes))
      await km.destroyKey()
    })
```

### Python Test: py-wallet-toolbox/tests/integration/test_privileged_key_manager.py

```python
    async def test_ensures_chunk_splitting_logic_is_correct_for_a_32_byte_key(self) -> None:
        """Given: 32-byte private key
           When: Split into obfuscated chunks
           Then: Chunks XOR back to original key

        Reference: wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts
                   test('Ensures chunk-splitting logic is correct for a 32-byte key')
        """
        # Given
        key = PrivateKey.from_random()
        wallet = PrivilegedKeyManager(lambda: key)

        # When
        await wallet.get_privileged_key()

        # Then - verify chunk splitting/reconstruction works
        # (Internal chunk logic should XOR back to original key)
        await wallet.destroy_key()
```

### AI Analysis Results

**Similarity Score**: 0.00%
  - Structural: 0.00%
  - Semantic: 0.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'value_verification verification' but PY verifies 'general_test'
  - [HIGH] Python test is missing verifications: chunks.length, chunk.length, reassembled.length
  - [HIGH] Python test is missing operations: km.destroyKey

**Differences:**
  - Operation count: TS has 1, PY has 2
  - Verification count: TS has 4, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'value_verification verification'
  - Add verifications for: chunks.length, chunk.length, reassembled.length
  - Add operations: km.destroyKey

**Explanation:**

Overall Similarity: 0.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 0.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: general_test

Critical Issues (3):
  • [HIGH] Test intent differs: TS verifies 'value_verification verification' but PY verifies 'general_test'
  • [HIGH] Python test is missing verifications: chunks.length, chunk.length, reassembled.length
  • [HIGH] Python test is missing operations: km.destroyKey

Key Differences:
  • Operation count: TS has 1, PY has 2
  • Verification count: TS has 4, PY has 0

---

## Test 134: Explicitly calls destroyKey() and removes all chunk properties **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_privileged_key_manager.py`

---

## Test 135: Fails to decryupt messages for the wrong protocol, key, and counterparty **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_privileged_key_manager.py`

---

## Test 136: Fails to verify HMAC for the wrong data, protocol, key, and counterparty **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_privileged_key_manager.py`

---

## Test 137: Fails to verify signature for the wrong data, protocol, key, and counterparty **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_privileged_key_manager.py`

---

## Test 138: Generates random property names **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_privileged_key_manager.py`

---

## Test 139: New decoy properties are created on each key fetch and destroyed on destroy **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_privileged_key_manager.py`

---

## Test 140: Reuses in-memory obfuscated key if data is valid, otherwise fetches a new key **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_privileged_key_manager.py`

---

## Test 141: Sets up initial decoy properties in the constructor **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_privileged_key_manager.py`

---

## Test 142: Signs messages verifiable by the counterparty **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_privileged_key_manager.py`

---

## Test 143: Uses anyone for creating signatures and self for other operations if no counterparty is provided **FAIL**

### TypeScript Test: wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts

```typescript
  it('Uses anyone for creating signatures and self for other operations if no counterparty is provided', async () => {
    const userKey = PrivateKey.fromRandom()
    const user = new PrivilegedKeyManager(async () => userKey)
    const { hmac } = await user.createHmac({
      data: sampleData,
      protocolID: [2, 'tests'],
      keyID: '4'
    })
    const { valid: hmacValid } = await user.verifyHmac({
      hmac,
      data: sampleData,
      protocolID: [2, 'tests'],
      keyID: '4'
    })
    expect(hmacValid).toEqual(true)
    const { valid: explicitSelfHmacValid } = await user.verifyHmac({
      hmac,
      data: sampleData,
      protocolID: [2, 'tests'],
      keyID: '4',
      counterparty: 'self'
    })
    expect(explicitSelfHmacValid).toEqual(true)
    expect(hmac.length).toEqual(32)
    const { signature: anyoneSig } = await user.createSignature({
      data: sampleData,
      protocolID: [2, 'tests'],
      keyID: '4'
      // counterparty=anyone is implicit for creating signatures
    })
    const anyone = new PrivilegedKeyManager(async () => new PrivateKey(1))
    const { valid: anyoneSigValid } = await anyone.verifySignature({
      signature: anyoneSig,
      data: sampleData,
      protocolID: [2, 'tests'],
      keyID: '4',
      counterparty: userKey.toPublicKey().toString()
    })
    expect(anyoneSigValid).toEqual(true)
    const { signature: selfSig } = await user.createSignature({
      data: sampleData,
      protocolID: [2, 'tests'],
      keyID: '4',
      counterparty: 'self'
    })
    const { valid: selfSigValid } = await user.verifySignature({
      signature: selfSig,
      data: sampleData,
      protocolID: [2, 'tests'],
      keyID: '4'
      // Self is implicit when verifying signatures
    })
    expect(selfSigValid).toEqual(true)
    const { valid: explicitSelfSigValid } = await user.verifySignature({
      signature: selfSig,
      data: sampleData,
      protocolID: [2, 'tests'],
      keyID: '4',
      counterparty: 'self'
    })
    expect(explicitSelfSigValid).toEqual(true)
    const { publicKey } = await user.getPublicKey({
      protocolID: [2, 'tests'],
      keyID: '4'
    })
    const { publicKey: explicitSelfPublicKey } = await user.getPublicKey({
      protocolID: [2, 'tests'],
      keyID: '4',
      counterparty: 'self'
    })
    expect(publicKey).toEqual(explicitSelfPublicKey)
    const { ciphertext } = await user.encrypt({
      plaintext: sampleData,
      protocolID: [2, 'tests'],
      keyID: '4'
    })
    const { plaintext } = await user.decrypt({
      ciphertext,
      protocolID: [2, 'tests'],
      keyID: '4'
    })
    const { plaintext: explicitSelfPlaintext } = await user.decrypt({
      ciphertext,
      protocolID: [2, 'tests'],
      keyID: '4',
      counterparty: 'self'
    })
    expect(plaintext).toEqual(explicitSelfPlaintext)
    expect(plaintext).toEqual(sampleData)
    await user.destroyKey()
    await anyone.destroyKey()
  })
```

### Python Test: py-wallet-toolbox/tests/integration/test_privileged_key_manager.py

```python
    async def test_uses_anyone_for_creating_signatures_and_self_for_other_operations_if_no_counterparty_is_provided(
        self,
    ) -> None:
        """Given: Wallet without counterparty specified
           When: Perform operations without counterparty
           Then: Uses 'anyone' for signatures, 'self' for encrypt/hmac

        Reference: wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts
                   test('Uses anyone for creating signatures and self for other operations if no counterparty is provided')
        """
        # Given
        user_key = PrivateKey.from_random()
        user = PrivilegedKeyManager(lambda: user_key)

        # When - sign without counterparty (uses 'anyone')
        signed = await user.create_signature({"data": SAMPLE_DATA, "protocolID": [2, "tests"], "keyID": "4"})

        # Then
        assert len(signed["signature"]) > 0
        await user.destroy_key()
```

### AI Analysis Results

**Similarity Score**: 21.64%
  - Structural: 0.00%
  - Semantic: 30.00%
  - Alignment: 22.12%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: hmac.length
  - [HIGH] Python test is missing operations: user.createSignature, user.encrypt, user.verifySignature, user.verifyHmac, user.getPublicKey, anyone.verifySignature, anyone.destroyKey, user.createHmac, user.destroyKey, user.decrypt

**Differences:**
  - Operation count: TS has 15, PY has 2

**Suggestions:**
  - Add verifications for: hmac.length
  - Add operations: user.createSignature, user.encrypt, user.verifySignature

**Explanation:**

Overall Similarity: 21.6%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 30.0% (test intent and meaning)
  • Alignment: 22.1% (functional equivalence)

Test Intent:
  • TypeScript: authentication decryption verification value_verification encryption
  • Python: authentication verification encryption

Critical Issues (2):
  • [HIGH] Python test is missing verifications: hmac.length
  • [HIGH] Python test is missing operations: user.createSignature, user.encrypt, user.verifySignature, user.verifyHmac, user.getPublicKey, anyone.verifySignature, anyone.destroyKey, user.createHmac, user.destroyKey, user.decrypt

Key Differences:
  • Operation count: TS has 15, PY has 2

---

## Test 144: Validates the BRC-2 Encryption compliance vector **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_privileged_key_manager.py`

---

## Test 145: Validates the BRC-2 HMAC compliance vector **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_privileged_key_manager.py`

---

## Test 146: Validates the BRC-3 compliance vector **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_privileged_key_manager.py`

---

## Test 147: Validates the revealCounterpartyKeyLinkage function **FAIL**

### TypeScript Test: wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts

```typescript
    it('Validates the revealCounterpartyKeyLinkage function', async () => {
      // Initialize keys
      const proverKey = PrivateKey.fromRandom()
      const counterpartyKey = PrivateKey.fromRandom()
      const verifierKey = PrivateKey.fromRandom()

      // Initialize wallets
      const proverWallet = new PrivilegedKeyManager(async () => proverKey)
      const verifierWallet = new PrivilegedKeyManager(async () => verifierKey)

      // Prover reveals counterparty key linkage
      const revelation = await proverWallet.revealCounterpartyKeyLinkage({
        counterparty: counterpartyKey.toPublicKey().toString(),
        verifier: verifierKey.toPublicKey().toString()
      })

      // Verifier decrypts the encrypted linkage
      const { plaintext: linkage } = await verifierWallet.decrypt({
        ciphertext: revelation.encryptedLinkage,
        protocolID: [2, 'counterparty linkage revelation'],
        keyID: revelation.revelationTime,
        counterparty: proverKey.toPublicKey().toString()
      })

      // Compute expected linkage
      const expectedLinkage = proverKey.deriveSharedSecret(counterpartyKey.toPublicKey()).encode(true)

      // Compare linkage and expectedLinkage
      expect(linkage).toEqual(expectedLinkage)
      await proverWallet.destroyKey()
      await verifierWallet.destroyKey()
    })
```

### Python Test: py-wallet-toolbox/tests/integration/test_privileged_key_manager.py

```python
    async def test_validates_the_revealcounterpartykeylinkage_function(self) -> None:
        """Given: Wallet with key derivation
           When: Reveal counterparty key linkage
           Then: Returns linkage proof verifiable by counterparty

        Reference: wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts
                   test('Validates the revealCounterpartyKeyLinkage function')
        """
        # Given
        user_key = PrivateKey.from_random()
        counterparty_key = PrivateKey.from_random()
        user = PrivilegedKeyManager(lambda: user_key)

        # When
        linkage = await user.reveal_counterparty_key_linkage(
            {
                "counterparty": counterparty_key.to_public_key().to_string(),
                "verifier": counterparty_key.to_public_key().to_string(),
            }
        )

        # Then
        assert "prover" in linkage
        assert "verifier" in linkage
        assert "revealedBy" in linkage
        await user.destroy_key()
```

### AI Analysis Results

**Similarity Score**: 42.00%
  - Structural: 0.00%
  - Semantic: 84.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing operations: prover_wallet.revealCounterpartyKeyLinkage, verifier_wallet.decrypt, verifier_wallet.destroyKey, prover_wallet.destroyKey

**Differences:**
  - Operation count: TS has 4, PY has 2

**Suggestions:**
  - Add operations: prover_wallet.revealCounterpartyKeyLinkage, verifier_wallet.decrypt, verifier_wallet.destroyKey

**Explanation:**

Overall Similarity: 42.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 84.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: decryption verification encryption
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing operations: prover_wallet.revealCounterpartyKeyLinkage, verifier_wallet.decrypt, verifier_wallet.destroyKey, prover_wallet.destroyKey

Key Differences:
  • Operation count: TS has 4, PY has 2

---

## Test 148: Validates the revealSpecificKeyLinkage function **FAIL**

### TypeScript Test: wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts

```typescript
    it('Validates the revealSpecificKeyLinkage function', async () => {
      // Initialize keys
      const proverKey = PrivateKey.fromRandom()
      const counterpartyKey = PrivateKey.fromRandom()
      const verifierKey = PrivateKey.fromRandom()

      // Initialize wallets
      const proverWallet = new PrivilegedKeyManager(async () => proverKey)
      const verifierWallet = new PrivilegedKeyManager(async () => verifierKey)

      const protocolID: [0 | 1 | 2, string] = [0, 'tests']
      const keyID = 'test key id'

      // Prover reveals specific key linkage
      const revelation = await proverWallet.revealSpecificKeyLinkage({
        counterparty: counterpartyKey.toPublicKey().toString(),
        verifier: verifierKey.toPublicKey().toString(),
        protocolID,
        keyID
      })

      // Verifier decrypts the encrypted linkage
      const { plaintext: linkage } = await verifierWallet.decrypt({
        ciphertext: revelation.encryptedLinkage,
        protocolID: [2, `specific linkage revelation ${protocolID[0]} ${protocolID[1]}`],
        keyID,
        counterparty: proverKey.toPublicKey().toString()
      })

      // Compute expected linkage
      const sharedSecret = proverKey.deriveSharedSecret(counterpartyKey.toPublicKey()).encode(true)

      // Function to compute the invoice number
      const computeInvoiceNumber = function (protocolID, keyID) {
        const securityLevel = protocolID[0]
        if (!Number.isInteger(securityLevel) || securityLevel < 0 || securityLevel > 2) {
          throw new Error('Protocol security level must be 0, 1, or 2')
        }
        const protocolName = protocolID[1].toLowerCase().trim()
        if (keyID.length > 800) {
          throw new Error('Key IDs must be 800 characters or less')
        }
        if (keyID.length < 1) {
          throw new Error('Key IDs must be 1 character or more')
        }
        if (protocolName.length > 400) {
          throw new Error('Protocol names must be 400 characters or less')
        }
        if (protocolName.length < 5) {
          throw new Error('Protocol names must be 5 characters or more')
        }
        if (protocolName.includes('  ')) {
          throw new Error('Protocol names cannot contain multiple consecutive spaces ("  ")')
        }
        if (!/^[a-z0-9 ]+$/g.test(protocolName)) {
          throw new Error('Protocol names can only contain letters, numbers and spaces')
        }
        if (protocolName.endsWith(' protocol')) {
          throw new Error('No need to end your protocol name with " protocol"')
        }
        return `${securityLevel}-${protocolName}-${keyID}`
      }
      const invoiceNumber = computeInvoiceNumber(protocolID, keyID)
      const invoiceNumberBin = Utils.toArray(invoiceNumber, 'utf8')

      // Compute expected linkage
      const expectedLinkage = Hash.sha256hmac(sharedSecret, invoiceNumberBin)

      // Compare linkage and expectedLinkage
      expect(linkage).toEqual(expectedLinkage)

      await proverWallet.destroyKey()
      await verifierWallet.destroyKey()
    })
```

### Python Test: py-wallet-toolbox/tests/integration/test_privileged_key_manager.py

```python
    async def test_validates_the_revealspecifickeylinkage_function(self) -> None:
        """Given: Wallet with specific key
           When: Reveal specific key linkage
           Then: Returns linkage proof for specific key

        Reference: wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts
                   test('Validates the revealSpecificKeyLinkage function')
        """
        # Given
        user_key = PrivateKey.from_random()
        counterparty_key = PrivateKey.from_random()
        user = PrivilegedKeyManager(lambda: user_key)

        # When
        linkage = await user.reveal_specific_key_linkage(
            {
                "counterparty": counterparty_key.to_public_key().to_string(),
                "protocolID": [2, "tests"],
                "keyID": "4",
                "privileged": True,
            }
        )

        # Then
        assert "prover" in linkage
        assert "verifier" in linkage
        await user.destroy_key()
```

### AI Analysis Results

**Similarity Score**: 42.00%
  - Structural: 0.00%
  - Semantic: 84.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing operations: prover_wallet.revealSpecificKeyLinkage, verifier_wallet.decrypt, verifier_wallet.destroyKey, prover_wallet.destroyKey

**Differences:**
  - Operation count: TS has 4, PY has 2

**Suggestions:**
  - Add operations: prover_wallet.revealSpecificKeyLinkage, verifier_wallet.decrypt, verifier_wallet.destroyKey

**Explanation:**

Overall Similarity: 42.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 84.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: decryption verification encryption
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing operations: prover_wallet.revealSpecificKeyLinkage, verifier_wallet.decrypt, verifier_wallet.destroyKey, prover_wallet.destroyKey

Key Differences:
  • Operation count: TS has 4, PY has 2

---

## Test 149: XOR function works as expected **PASS**

- TypeScript: `wallet-toolbox/src/sdk/__test/PrivilegedKeyManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_privileged_key_manager.py`

---

## Test 150: 0 verify merkle proof to merkle path **PASS**

- TypeScript: `wallet-toolbox/src/services/__tests/bitrails.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_bitrails.py`

---

## Test 151: 0 postBeef mainnet **PASS**

- TypeScript: `wallet-toolbox/src/services/__tests/postBeef.test.ts`
- Python: `py-wallet-toolbox/tests/services/test_post_beef.py`

---

## Test 152: 1 postBeef testnet **PASS**

- TypeScript: `wallet-toolbox/src/services/__tests/postBeef.test.ts`
- Python: `py-wallet-toolbox/tests/services/test_post_beef.py`

---

## Test 153: 0 mainNet findHeaderForHeight **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/__tests/ChaintracksServiceClient.test.ts`
- Python: `py-wallet-toolbox/tests/chaintracks/test_service_client.py`

---

## Test 154: 1 testNet findHeaderForHeight **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/__tests/ChaintracksServiceClient.test.ts`
- Python: `py-wallet-toolbox/tests/chaintracks/test_service_client.py`

---

## Test 155: 0 mainNet **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/Ingest/__tests/BulkIngestorCDNBabbage.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_bulk_ingestor_cdn_babbage.py`

---

## Test 156: 1 testNet **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/Ingest/__tests/BulkIngestorCDNBabbage.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_bulk_ingestor_cdn_babbage.py`

---

## Test 157: 0 listen for first new header **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/Ingest/__tests/LiveIngestorWhatsOnChainPoll.test.ts`
- Python: `py-wallet-toolbox/tests/monitor/test_live_ingestor_whats_on_chain_poll.py`

---

## Test 158: 2 get latest header bytes **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/Ingest/__tests/WhatsOnChainServices.test.ts`
- Python: `py-wallet-toolbox/tests/services/test_services.py`

---

## Test 159: 3 get headers **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/Ingest/__tests/WhatsOnChainServices.test.ts`
- Python: `py-wallet-toolbox/tests/services/test_services.py`

---

## Test 160: 4 get header byte file links **FAIL**

### TypeScript Test: wallet-toolbox/src/services/chaintracker/chaintracks/Ingest/__tests/WhatsOnChainServices.test.ts

```typescript
  test('4 get header byte file links', async () => {
    const fetch = new ChaintracksFetch()
    const woc = new WhatsOnChainServices(WhatsOnChainServices.createWhatsOnChainServicesOptions('main'))
    const files = await woc.getHeaderByteFileLinks(new HeightRange(907123, 911000))
    expect(files.length).toBe(3)
    expect(files[0].range.minHeight).toBe(906001)
    expect(files[0].range.maxHeight).toBe(908000)
    expect(files[1].range.minHeight).toBe(908001)
    expect(files[1].range.maxHeight).toBe(910000)
    expect(files[2].range.minHeight).toBe(910001)
    expect(files[2].range.maxHeight).toBeGreaterThan(910001)
  })
```

### Python Test: py-wallet-toolbox/tests/services/test_services.py

```python
    def test_get_header_byte_file_links(self) -> None:
        """Given: WhatsOnChainServices instance
           When: Get header byte file links for height range 907123-911000
           Then: Returns 3 files with correct height ranges

        Reference: wallet-toolbox/src/services/chaintracker/chaintracks/Ingest/__tests/WhatsOnChainServices.test.ts
                   test('4 get header byte file links')
        """
        # Given
        ChaintracksFetch()
        woc = WhatsOnChainServices(WhatsOnChainServices.create_whats_on_chain_services_options("main"))

        # When
        files = woc.get_header_byte_file_links(HeightRange(907123, 911000))

        # Then
        assert len(files) == 3
        assert files[0].range.min_height == 906001
        assert files[0].range.max_height == 908000
        assert files[1].range.min_height == 908001
        assert files[1].range.max_height == 910000
        assert files[2].range.min_height == 910001
        assert files[2].range.max_height > 910001
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: files.length
  - [HIGH] Python test is missing operations: woc.getHeaderByteFileLinks

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 1, PY has 6

**Suggestions:**
  - Add verifications for: files.length
  - Add operations: woc.getHeaderByteFileLinks

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: files.length
  • [HIGH] Python test is missing operations: woc.getHeaderByteFileLinks

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 1, PY has 6

---

## Test 161: getChainTipHeight **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/Ingest/__tests/WhatsOnChainServices.test.ts`
- Python: `py-wallet-toolbox/tests/services/test_services.py`

---

## Test 162: getHeaderByHash **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/Ingest/__tests/WhatsOnChainServices.test.ts`
- Python: `py-wallet-toolbox/tests/services/test_services.py`

---

## Test 163: 1 NoDb mainnet **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/__tests/Chaintracks.test.ts`
- Python: `py-wallet-toolbox/tests/chaintracks/test_chaintracks.py`

---

## Test 164: 2 NoDb testnet **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/__tests/Chaintracks.test.ts`
- Python: `py-wallet-toolbox/tests/chaintracks/test_chaintracks.py`

---

## Test 165: 0 getChain **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/__tests/ChaintracksClientApi.test.ts`
- Python: `py-wallet-toolbox/tests/chaintracks/test_client_api.py`

---

## Test 166: 1 getInfo **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/__tests/ChaintracksClientApi.test.ts`
- Python: `py-wallet-toolbox/tests/chaintracks/test_client_api.py`

---

## Test 167: 2 getPresentHeight **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/__tests/ChaintracksClientApi.test.ts`
- Python: `py-wallet-toolbox/tests/chaintracks/test_client_api.py`

---

## Test 168: 3 getHeaders **FAIL**

### TypeScript Test: wallet-toolbox/src/services/chaintracker/chaintracks/__tests/ChaintracksClientApi.test.ts

```typescript
  test('3 getHeaders', async () => {
    for (const { client, chain } of clients) {
      const info = await client.getInfo()
      const h0 = info.heightBulk + 1
      const h1 = info.heightLive || 10
      const bulkHeaders = await getHeaders(h0 - 2, 2)
      expect(bulkHeaders.length).toBe(2)
      expect(bulkHeaders[1].previousHash === blockHash(bulkHeaders[0])).toBe(true)
      const bothHeaders = await getHeaders(h0 - 1, 2)
      expect(bothHeaders.length).toBe(2)
      expect(bothHeaders[1].previousHash === blockHash(bothHeaders[0])).toBe(true)
      const liveHeaders = await getHeaders(h0 - 0, 2)
      expect(liveHeaders.length).toBe(2)
      expect(liveHeaders[1].previousHash === blockHash(liveHeaders[0])).toBe(true)
      const partHeaders = await getHeaders(h1, 2)
      expect(partHeaders.length).toBe(1)

      async function getHeaders(h: number, c: number): Promise<BaseBlockHeader[]> {
        const data = asUint8Array(await client.getHeaders(h, c))
        const headers = deserializeBaseBlockHeaders(data)
        return headers
      }
    }
  })
```

### Python Test: py-wallet-toolbox/tests/services/test_services.py

```python
    def test_get_headers(self) -> None:
        """Given: ChaintracksFetch instance
           When: Fetch headers JSON from WhatsOnChain
           Then: Returns array of headers with height, hash, confirmations, nTx

        Reference: wallet-toolbox/src/services/chaintracker/chaintracks/Ingest/__tests/WhatsOnChainServices.test.ts
                   test('3 get headers')
        """
        # Given
        fetch = ChaintracksFetch()

        # When
        headers = fetch.fetch_json("https://api.whatsonchain.com/v1/bsv/main/block/headers")

        log = ""
        for h in headers:
            log += f"{h['height']} {h['hash']} {h['confirmations']} {h['nTx']}\n"
        print(log)

        # Then
        assert len(headers) > 0
        assert "height" in headers[0]
        assert "hash" in headers[0]
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: part_headers.length, both_headers.length, bulk_headers.length, live_headers.length
  - [HIGH] Python test is missing operations: client.getInfo, client.getHeaders

**Differences:**
  - Operation count: TS has 2, PY has 0
  - Verification count: TS has 4, PY has 0

**Suggestions:**
  - Add verifications for: part_headers.length, both_headers.length, bulk_headers.length
  - Add operations: client.getInfo, client.getHeaders

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification token_operation verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: part_headers.length, both_headers.length, bulk_headers.length, live_headers.length
  • [HIGH] Python test is missing operations: client.getInfo, client.getHeaders

Key Differences:
  • Operation count: TS has 2, PY has 0
  • Verification count: TS has 4, PY has 0

---

## Test 169: 4 findChainTipHeader **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/__tests/ChaintracksClientApi.test.ts`
- Python: `py-wallet-toolbox/tests/chaintracks/test_client_api.py`

---

## Test 170: 5 findChainTipHash **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/__tests/ChaintracksClientApi.test.ts`
- Python: `py-wallet-toolbox/tests/chaintracks/test_client_api.py`

---

## Test 171: 6 findHeaderForHeight **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/__tests/ChaintracksClientApi.test.ts`
- Python: `py-wallet-toolbox/tests/chaintracks/test_client_api.py`

---

## Test 172: 7 addHeader **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/__tests/ChaintracksClientApi.test.ts`
- Python: `py-wallet-toolbox/tests/chaintracks/test_client_api.py`

---

## Test 173: subscribeHeaders **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/__tests/ChaintracksClientApi.test.ts`
- Python: `py-wallet-toolbox/tests/chaintracks/test_client_api.py`

---

## Test 174: subscribeReorgs **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/__tests/ChaintracksClientApi.test.ts`
- Python: `py-wallet-toolbox/tests/chaintracks/test_client_api.py`

---

## Test 175: 0 default options CDN files **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/util/__tests/BulkFileDataManager.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_bulk_file_data_manager.py`

---

## Test 176: 0a default options CDN files noDropAll **FAIL**

### TypeScript Test: wallet-toolbox/src/services/chaintracker/chaintracks/util/__tests/BulkFileDataManager.test.ts

```typescript
  test('0a default options CDN files noDropAll', async () => {
    if (!runSlowTests) return
    const options = BulkFileDataManager.createDefaultOptions(chain)
    const manager = new BulkFileDataManager(options)
    const storage = await setupStorageKnex(manager, `BulkFileDataManager.test_0a`, false)

    await test0Body(manager)

    await storage.destroy()
  })
```

### Python Test: py-wallet-toolbox/tests/integration/test_bulk_file_data_manager.py

```python
    async def test_default_options_cdn_files_nodropall(self) -> None:
        """Given: BulkFileDataManager with storage (noDropAll)
           When: Setup storage without dropping database
           Then: Manager operates correctly with persistent storage

        Reference: wallet-toolbox/src/services/chaintracker/chaintracks/util/__tests/BulkFileDataManager.test.ts
                   test('0a default options CDN files noDropAll')
        """
        # Given
        options = BulkFileDataManager.create_default_options(self.chain)
        manager = BulkFileDataManager(options)
        storage = await self._setup_storage_knex(manager, "BulkFileDataManager.test_0a", False)

        # When/Then
        await self._test0_body(manager)

        # Cleanup
        await storage.destroy()

    # Note: Additional tests follow the same pattern from TypeScript.
    #       Due to token constraints, only key tests are shown here.
    #       Full implementation should include all tests from test('0b') through test('5a').
```

### AI Analysis Results

**Similarity Score**: 53.00%
  - Structural: 50.00%
  - Semantic: 60.00%
  - Alignment: 43.33%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'general_test' but PY verifies 'token_operation'

**Differences:**
  - Operation count: TS has 1, PY has 3

**Suggestions:**
  - Align test intent: ensure PY test verifies 'general_test'

**Explanation:**

Overall Similarity: 53.0%
  • Structural: 50.0% (sequence and structure)
  • Semantic: 60.0% (test intent and meaning)
  • Alignment: 43.3% (functional equivalence)

Test Intent:
  • TypeScript: general_test
  • Python: token_operation

Critical Issues (1):
  • [HIGH] Test intent differs: TS verifies 'general_test' but PY verifies 'token_operation'

Key Differences:
  • Operation count: TS has 1, PY has 3

---

## Test 177: 0b default options CDN files dropAll **FAIL**

### TypeScript Test: wallet-toolbox/src/services/chaintracker/chaintracks/util/__tests/BulkFileDataManager.test.ts

```typescript
  test('0b default options CDN files dropAll', async () => {
    if (!runSlowTests) return
    const options = BulkFileDataManager.createDefaultOptions(chain)
    const manager = new BulkFileDataManager(options)
    const storage = await setupStorageKnex(manager, `BulkFileDataManager.test_0b`, true)

    await test0Body(manager)

    await storage.destroy()
  })
```

### Python Test: py-wallet-toolbox/tests/integration/test_bulk_file_data_manager.py

```python
    async def test_default_options_cdn_files_nodropall(self) -> None:
        """Given: BulkFileDataManager with storage (noDropAll)
           When: Setup storage without dropping database
           Then: Manager operates correctly with persistent storage

        Reference: wallet-toolbox/src/services/chaintracker/chaintracks/util/__tests/BulkFileDataManager.test.ts
                   test('0a default options CDN files noDropAll')
        """
        # Given
        options = BulkFileDataManager.create_default_options(self.chain)
        manager = BulkFileDataManager(options)
        storage = await self._setup_storage_knex(manager, "BulkFileDataManager.test_0a", False)

        # When/Then
        await self._test0_body(manager)

        # Cleanup
        await storage.destroy()

    # Note: Additional tests follow the same pattern from TypeScript.
    #       Due to token constraints, only key tests are shown here.
    #       Full implementation should include all tests from test('0b') through test('5a').
```

### AI Analysis Results

**Similarity Score**: 53.00%
  - Structural: 50.00%
  - Semantic: 60.00%
  - Alignment: 43.33%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'general_test' but PY verifies 'token_operation'

**Differences:**
  - Operation count: TS has 1, PY has 3

**Suggestions:**
  - Align test intent: ensure PY test verifies 'general_test'

**Explanation:**

Overall Similarity: 53.0%
  • Structural: 50.0% (sequence and structure)
  • Semantic: 60.0% (test intent and meaning)
  • Alignment: 43.3% (functional equivalence)

Test Intent:
  • TypeScript: general_test
  • Python: token_operation

Critical Issues (1):
  • [HIGH] Test intent differs: TS verifies 'general_test' but PY verifies 'token_operation'

Key Differences:
  • Operation count: TS has 1, PY has 3

---

## Test 178: 0 fetchJson **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/util/__tests/ChaintracksFetch.test.ts`
- Python: `py-wallet-toolbox/tests/chaintracks/test_fetch.py`

---

## Test 179: 1 download **FAIL**

### TypeScript Test: wallet-toolbox/src/services/chaintracker/chaintracks/util/__tests/ChaintracksFetch.test.ts

```typescript
  test('1 download', async () => {
    const fetch = new ChaintracksFetch()
    const cdnUrl = 'https://cdn.projectbabbage.com/blockheaders/'
    const url = `${cdnUrl}/testNet_0.headers`
    const data = await fetch.download(url)
    expect(data.length).toBe(8000000)
    const fileHash = asString(Hash.sha256(asArray(data)), 'base64')
    expect(validBulkHeaderFilesByFileHash()[fileHash]).toBeDefined()
  })
```

### Python Test: py-wallet-toolbox/tests/chaintracks/test_fetch.py

```python
    def test_download(self) -> None:
        """Given: ChaintracksFetch instance and CDN URL
           When: Download testNet_0.headers file
           Then: Returns 8000000 bytes with valid hash

        Reference: wallet-toolbox/src/services/chaintracker/chaintracks/util/__tests/ChaintracksFetch.test.ts
                   test('1 download')
        """
        # Given
        fetch = ChaintracksFetch()
        cdn_url = "https://cdn.projectbabbage.com/blockheaders/"
        url = f"{cdn_url}/testNet_0.headers"

        # When
        data = fetch.download(url)

        # Then
        assert len(data) == 8000000
        file_hash = as_string(sha256(as_array(data)), "base64")
        assert valid_bulk_header_files_by_file_hash()[file_hash] is not None
```

### AI Analysis Results

**Similarity Score**: 16.00%
  - Structural: 0.00%
  - Semantic: 32.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: data.length
  - [HIGH] Python test is missing operations: fetch.download

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: data.length
  - Add operations: fetch.download

**Explanation:**

Overall Similarity: 16.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 32.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification snapshot_load verification
  • Python: snapshot_load verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: data.length
  • [HIGH] Python test is missing operations: fetch.download

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 1, PY has 0

---

## Test 180: 3 download **FAIL**

### TypeScript Test: wallet-toolbox/src/services/chaintracker/chaintracks/util/__tests/ChaintracksFetch.test.ts

```typescript
  test('3 download', async () => {
    const fetch = new ChaintracksFetch()
    const cdnUrl = 'https://cdn.projectbabbage.com/blockheaders/'
    const url = `${cdnUrl}/testNet_4.headers`
    const data = await fetch.download(url)
    expect(data.length).toBe(80 * 100000)
    const fileHash = asString(Hash.sha256(asArray(data)), 'base64')
    expect(validBulkHeaderFilesByFileHash()[fileHash]).toBeDefined()
  })
```

### Python Test: py-wallet-toolbox/tests/chaintracks/test_fetch.py

```python
    def test_download(self) -> None:
        """Given: ChaintracksFetch instance and CDN URL
           When: Download testNet_0.headers file
           Then: Returns 8000000 bytes with valid hash

        Reference: wallet-toolbox/src/services/chaintracker/chaintracks/util/__tests/ChaintracksFetch.test.ts
                   test('1 download')
        """
        # Given
        fetch = ChaintracksFetch()
        cdn_url = "https://cdn.projectbabbage.com/blockheaders/"
        url = f"{cdn_url}/testNet_0.headers"

        # When
        data = fetch.download(url)

        # Then
        assert len(data) == 8000000
        file_hash = as_string(sha256(as_array(data)), "base64")
        assert valid_bulk_header_files_by_file_hash()[file_hash] is not None
```

### AI Analysis Results

**Similarity Score**: 16.00%
  - Structural: 0.00%
  - Semantic: 32.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: data.length
  - [HIGH] Python test is missing operations: fetch.download

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: data.length
  - Add operations: fetch.download

**Explanation:**

Overall Similarity: 16.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 32.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification snapshot_load verification
  • Python: snapshot_load verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: data.length
  • [HIGH] Python test is missing operations: fetch.download

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 1, PY has 0

---

## Test 181: 4 download **FAIL**

### TypeScript Test: wallet-toolbox/src/services/chaintracker/chaintracks/util/__tests/ChaintracksFetch.test.ts

```typescript
  test('4 download', async () => {
    const fetch = new ChaintracksFetch()
    const cdnUrl = 'https://cdn.projectbabbage.com/blockheaders/'
    const url = `${cdnUrl}/mainNet_2.headers`
    const data = await fetch.download(url)
    expect(data.length).toBe(80 * 100000)
    const fileHash = asString(Hash.sha256(asArray(data)), 'base64')
    expect(validBulkHeaderFilesByFileHash()[fileHash]).toBeDefined()
  })
```

### Python Test: py-wallet-toolbox/tests/chaintracks/test_fetch.py

```python
    def test_download(self) -> None:
        """Given: ChaintracksFetch instance and CDN URL
           When: Download testNet_0.headers file
           Then: Returns 8000000 bytes with valid hash

        Reference: wallet-toolbox/src/services/chaintracker/chaintracks/util/__tests/ChaintracksFetch.test.ts
                   test('1 download')
        """
        # Given
        fetch = ChaintracksFetch()
        cdn_url = "https://cdn.projectbabbage.com/blockheaders/"
        url = f"{cdn_url}/testNet_0.headers"

        # When
        data = fetch.download(url)

        # Then
        assert len(data) == 8000000
        file_hash = as_string(sha256(as_array(data)), "base64")
        assert valid_bulk_header_files_by_file_hash()[file_hash] is not None
```

### AI Analysis Results

**Similarity Score**: 16.00%
  - Structural: 0.00%
  - Semantic: 32.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: data.length
  - [HIGH] Python test is missing operations: fetch.download

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: data.length
  - Add operations: fetch.download

**Explanation:**

Overall Similarity: 16.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 32.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification snapshot_load verification
  • Python: snapshot_load verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: data.length
  • [HIGH] Python test is missing operations: fetch.download

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 1, PY has 0

---

## Test 182: copy **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/util/__tests/HeightRange.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_height_range.py`

---

## Test 183: intersect **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/util/__tests/HeightRange.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_height_range.py`

---

## Test 184: length **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/util/__tests/HeightRange.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_height_range.py`

---

## Test 185: subtract **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/util/__tests/HeightRange.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_height_range.py`

---

## Test 186: union **PASS**

- TypeScript: `wallet-toolbox/src/services/chaintracker/chaintracks/util/__tests/HeightRange.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_height_range.py`

---

## Test 187: 0 getRawTx testnet **PASS**

- TypeScript: `wallet-toolbox/src/services/providers/__tests/WhatsOnChain.test.ts`
- Python: `py-wallet-toolbox/tests/services/test_whats_on_chain.py`

---

## Test 188: 00 **PASS**

- TypeScript: `wallet-toolbox/src/services/providers/__tests/WhatsOnChain.test.ts`
- Python: `py-wallet-toolbox/tests/wallet/test_certificates.py`

---

## Test 189: 1 getRawTx mainnet **PASS**

- TypeScript: `wallet-toolbox/src/services/providers/__tests/WhatsOnChain.test.ts`
- Python: `py-wallet-toolbox/tests/services/test_whats_on_chain.py`

---

## Test 190: 2 getMerklePath testnet **PASS**

- TypeScript: `wallet-toolbox/src/services/providers/__tests/WhatsOnChain.test.ts`
- Python: `py-wallet-toolbox/tests/services/test_whats_on_chain.py`

---

## Test 191: 3 getMerklePath mainnet **PASS**

- TypeScript: `wallet-toolbox/src/services/providers/__tests/WhatsOnChain.test.ts`
- Python: `py-wallet-toolbox/tests/services/test_whats_on_chain.py`

---

## Test 192: 4 updateBsvExchangeRate **FAIL**

### TypeScript Test: wallet-toolbox/src/services/providers/__tests/WhatsOnChain.test.ts

```typescript
  test('4 updateBsvExchangeRate', async () => {
    {
      const r = await wocMain.updateBsvExchangeRate()
      expect(r.base).toBe('USD')
      expect(r.rate).toBeGreaterThan(0)
      expect(r.timestamp).toBeTruthy()
    }
  })
```

### Python Test: py-wallet-toolbox/tests/services/test_whats_on_chain.py

```python
    def test_updatebsvexchangerate(self) -> None:
        """Given: WhatsOnChain service for mainnet
           When: Call updateBsvExchangeRate
           Then: Returns exchange rate with base 'USD', positive rate, and truthy timestamp

        Reference: wallet-toolbox/src/services/providers/__tests/WhatsOnChain.test.ts
                   test('4 updateBsvExchangeRate')
        """
        # Given
        env_main = TestUtils.get_env("main")
        woc_main = WhatsOnChain(env_main.chain, {"apiKey": env_main.taal_api_key})

        # When
        r = woc_main.update_bsv_exchange_rate()

        # Then
        assert r["base"] == "USD"
        assert r["rate"] > 0
        assert r["timestamp"] is not None
```

### AI Analysis Results

**Similarity Score**: 42.00%
  - Structural: 0.00%
  - Semantic: 84.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'value_verification verification' but PY verifies 'authentication verification key_change'
  - [HIGH] Python test is missing verifications: r.timestamp, r.base, r.rate
  - [HIGH] Python test is missing operations: woc_main.updateBsvExchangeRate

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'value_verification verification'
  - Add verifications for: r.timestamp, r.base, r.rate
  - Add operations: woc_main.updateBsvExchangeRate

**Explanation:**

Overall Similarity: 42.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 84.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification key_change

Critical Issues (3):
  • [HIGH] Test intent differs: TS verifies 'value_verification verification' but PY verifies 'authentication verification key_change'
  • [HIGH] Python test is missing verifications: r.timestamp, r.base, r.rate
  • [HIGH] Python test is missing operations: woc_main.updateBsvExchangeRate

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 193: 5 getTxPropagation testnet **FAIL**

### TypeScript Test: wallet-toolbox/src/services/providers/__tests/WhatsOnChain.test.ts

```typescript
  test('5 getTxPropagation testnet', async () => {
    return
    // throwing internal server error 500 when tested.
    const count = await wocTest.getTxPropagation('7e5b797b86abd31a654bf296900d6cb14d04ef0811568ff4675494af2d92166b')
    expect(count > 0)

    expect((await wocTest.getTxPropagation('1'.repeat(64))) === 0)
  })
```

### Python Test: py-wallet-toolbox/tests/services/test_whats_on_chain.py

```python
    def test_gettxpropagation_testnet(self) -> None:
        """Given: WhatsOnChain service for testnet and a known txid
           When: Call getTxPropagation
           Then: Test skipped (TypeScript returns early due to internal server error 500)

        Reference: wallet-toolbox/src/services/providers/__tests/WhatsOnChain.test.ts
                   test('5 getTxPropagation testnet')
        """
        # Note: TypeScript test returns early due to internal server error 500 when tested
        # The commented-out logic would check:
        # - count > 0 for valid txid
        # - count == 0 for invalid txid '1' * 64
        return
```

### AI Analysis Results

**Similarity Score**: 30.00%
  - Structural: 0.00%
  - Semantic: 60.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'authentication'
  - [HIGH] Python test is missing operations: woc_test.getTxPropagation

**Differences:**
  - Operation count: TS has 2, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'verification'
  - Add operations: woc_test.getTxPropagation

**Explanation:**

Overall Similarity: 30.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 60.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification
  • Python: authentication

Critical Issues (2):
  • [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'authentication'
  • [HIGH] Python test is missing operations: woc_test.getTxPropagation

Key Differences:
  • Operation count: TS has 2, PY has 0

---

## Test 194: 6 getTxPropagation mainnet **PASS**

- TypeScript: `wallet-toolbox/src/services/providers/__tests/WhatsOnChain.test.ts`
- Python: `py-wallet-toolbox/tests/services/test_whats_on_chain.py`

---

## Test 195: 0 two outputs **PASS**

- TypeScript: `wallet-toolbox/src/storage/methods/__test/GenerateChange/generateChangeSdk.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_generate_change_sdk.py`

---

## Test 196: 0a two outputs exact input **PASS**

- TypeScript: `wallet-toolbox/src/storage/methods/__test/GenerateChange/generateChangeSdk.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_generate_change_sdk.py`

---

## Test 197: 0b two outputs 666666 200 **PASS**

- TypeScript: `wallet-toolbox/src/storage/methods/__test/GenerateChange/generateChangeSdk.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_generate_change_sdk.py`

---

## Test 198: 0c two outputs 666666 200 two change inputs **PASS**

- TypeScript: `wallet-toolbox/src/storage/methods/__test/GenerateChange/generateChangeSdk.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_generate_change_sdk.py`

---

## Test 199: 1 two outputs four change outputs **PASS**

- TypeScript: `wallet-toolbox/src/storage/methods/__test/GenerateChange/generateChangeSdk.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_generate_change_sdk.py`

---

## Test 200: 2 WERR_INSUFFICIENT_FUNDS **PASS**

- TypeScript: `wallet-toolbox/src/storage/methods/__test/GenerateChange/generateChangeSdk.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_generate_change_sdk.py`

---

## Test 201: 2a WERR_INSUFFICIENT_FUNDS no inputs **PASS**

- TypeScript: `wallet-toolbox/src/storage/methods/__test/GenerateChange/generateChangeSdk.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_generate_change_sdk.py`

---

## Test 202: 3 allocate all **PASS**

- TypeScript: `wallet-toolbox/src/storage/methods/__test/GenerateChange/generateChangeSdk.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_generate_change_sdk.py`

---

## Test 203: 4 feeModel 5 sat per kb **PASS**

- TypeScript: `wallet-toolbox/src/storage/methods/__test/GenerateChange/generateChangeSdk.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_generate_change_sdk.py`

---

## Test 204: 4a feeModel 1 sat per kb **PASS**

- TypeScript: `wallet-toolbox/src/storage/methods/__test/GenerateChange/generateChangeSdk.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_generate_change_sdk.py`

---

## Test 205: 5 one fixedInput **PASS**

- TypeScript: `wallet-toolbox/src/storage/methods/__test/GenerateChange/generateChangeSdk.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_generate_change_sdk.py`

---

## Test 206: 5a one larger fixedInput **PASS**

- TypeScript: `wallet-toolbox/src/storage/methods/__test/GenerateChange/generateChangeSdk.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_generate_change_sdk.py`

---

## Test 207: 5b one fixedInput 1001 73 **PASS**

- TypeScript: `wallet-toolbox/src/storage/methods/__test/GenerateChange/generateChangeSdk.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_generate_change_sdk.py`

---

## Test 208: 6 no fixedOutputs one fixedInput **PASS**

- TypeScript: `wallet-toolbox/src/storage/methods/__test/GenerateChange/generateChangeSdk.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_generate_change_sdk.py`

---

## Test 209: 6a no fixedOutputs no fixedInput **PASS**

- TypeScript: `wallet-toolbox/src/storage/methods/__test/GenerateChange/generateChangeSdk.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_generate_change_sdk.py`

---

## Test 210: 7 paramsText4 d4 **PASS**

- TypeScript: `wallet-toolbox/src/storage/methods/__test/GenerateChange/generateChangeSdk.test.ts`
- Python: `py-wallet-toolbox/tests/utils/test_generate_change_sdk.py`

---

## Test 211: 0_equals identifies matching CertificateField entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/CertificateFieldTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_certificate_field.py`

---

## Test 212: 1_equals identifies non-matching CertificateField entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/CertificateFieldTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_certificate_field.py`

---

## Test 213: CertificateField getters and setters **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/CertificateFieldTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_certificate_field.py`

---

## Test 214: mergeExisting does not update entity when ei.updated_at <= this.updated_at **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/CertificateFieldTests.test.ts

```typescript
  test('mergeExisting does not update entity when ei.updated_at <= this.updated_at', async () => {
    for (const { activeStorage } of ctxs) {
      // Insert a valid Certificate to satisfy foreign key constraints
      const now = new Date()
      const certificateId = 401
      await activeStorage.insertCertificate({
        certificateId,
        created_at: now,
        updated_at: now,
        userId: 1,
        type: Buffer.from('exampleTypeNoMerge').toString('base64'),
        serialNumber: Buffer.from('serialNoMerge123').toString('base64'),
        certifier: '02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef1234',
        subject: '02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef5678',
        revocationOutpoint: 'abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890:0',
        signature: 'abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
        isDeleted: false
      })

      // Insert the initial CertificateField record
      const initialData: TableCertificateField = {
        certificateId,
        created_at: now,
        updated_at: now,
        userId: 1,
        fieldName: 'field1',
        fieldValue: 'value1',
        masterKey: 'masterKey1'
      }
      await activeStorage.insertCertificateField(initialData)

      // Create a CertificateField entity from the initial data
      const entity = new EntityCertificateField(initialData)

      // Simulate the `ei` argument with the same `updated_at`
      const sameUpdatedData: TableCertificateField = {
        ...initialData,
        updated_at: now, // Same timestamp
        fieldValue: 'unchangedValue',
        masterKey: 'unchangedMasterKey'
      }

      const syncMap = createSyncMap()
      syncMap.certificate.idMap[certificateId] = certificateId

      // Call mergeExisting
      const wasMergedRaw = await entity.mergeExisting(
        activeStorage,
        undefined, // `since` is not used
        sameUpdatedData,
        syncMap,
        undefined // `trx` is not used
      )

      const wasMerged = Boolean(wasMergedRaw)

      // Verify that wasMerged is false
      expect(wasMerged).toBe(false)

      // Verify that the entity is not updated
      expect(entity.fieldValue).toBe('value1')
      expect(entity.masterKey).toBe('masterKey1')

      // Verify that the database is not updated
      const unchangedRecord = await activeStorage.findCertificateFields({
        partial: { certificateId, fieldName: 'field1' }
      })
      expect(unchangedRecord.length).toBe(1)
      expect(unchangedRecord[0]).toBeDefined()
      expect(unchangedRecord[0].fieldValue).toBe('value1')
      expect(unchangedRecord[0].masterKey).toBe('masterKey1')
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_certificate.py

```python
    def test_mergeexisting_does_not_update_entity_when_ei_updated_at_less_than_or_equal_this_updated_at(
        self,
    ) -> None:
        """Given: Certificate entity with same or newer updated_at
           When: Call merge_existing with same or older updated_at
           Then: Entity is not updated

        Reference: src/storage/schema/entities/__tests/CertificateTests.test.ts
                  test('3_mergeExisting does not update entity when ei.updated_at <= this.updated_at')
        """
        # Given

        now = datetime.now()
        certificate_id = 601
        certificate_data = {
            "certificateId": certificate_id,
            "created_at": now,
            "updated_at": now,
            "userId": 1,
            "type": "exampleType",
            "serialNumber": "exampleSerialNumber",
            "certifier": "02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef1234",
            "subject": "02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef5678",
            "revocationOutpoint": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890:0",
            "signature": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
            "isDeleted": False,
        }

        entity = Certificate(certificate_data)

        # Same updated_at
        same_updated_data = {
            **certificate_data,
            "updated_at": now,
            "type": "unchangedType",
            "subject": "unchangedSubject",
        }

        sync_map = {"certificate": {"idMap": {certificate_id: certificate_id}}}
        mock_storage = type("MockStorage", (), {})()

        # When
        was_merged = entity.merge_existing(mock_storage, None, same_updated_data, sync_map, None)

        # Then
        assert was_merged is False
        assert entity.type == "exampleType"
        assert entity.subject == "02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef5678"
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: entity.fieldValue, unchanged_record.length, entity.masterKey
  - [HIGH] Python test is missing operations: entity.mergeExisting, active_storage.findCertificateFields, active_storage.insertCertificate, active_storage.insertCertificateField

**Differences:**
  - Operation count: TS has 4, PY has 0
  - Verification count: TS has 3, PY has 2

**Suggestions:**
  - Add verifications for: entity.fieldValue, unchanged_record.length, entity.masterKey
  - Add operations: entity.mergeExisting, active_storage.findCertificateFields, active_storage.insertCertificate

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification key_change
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: entity.fieldValue, unchanged_record.length, entity.masterKey
  • [HIGH] Python test is missing operations: entity.mergeExisting, active_storage.findCertificateFields, active_storage.insertCertificate, active_storage.insertCertificateField

Key Differences:
  • Operation count: TS has 4, PY has 0
  • Verification count: TS has 3, PY has 2

---

## Test 215: mergeExisting updates entity and database when ei.updated_at > this.updated_at **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/CertificateFieldTests.test.ts

```typescript
  test('mergeExisting updates entity and database when ei.updated_at > this.updated_at', async () => {
    for (const { activeStorage } of ctxs) {
      // Insert a valid Certificate to satisfy foreign key constraints
      const now = new Date()
      const certificateId = 400
      await activeStorage.insertCertificate({
        certificateId,
        created_at: now,
        updated_at: now,
        userId: 1,
        type: Buffer.from('exampleTypeMerge').toString('base64'),
        serialNumber: Buffer.from('serialMerge123').toString('base64'),
        certifier: '02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef1234',
        subject: '02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef5678',
        revocationOutpoint: 'abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890:0',
        signature: 'abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
        isDeleted: false
      })

      // Insert the initial CertificateField record
      const initialData: TableCertificateField = {
        certificateId,
        created_at: now,
        updated_at: now,
        userId: 1,
        fieldName: 'field1',
        fieldValue: 'value1',
        masterKey: 'masterKey1'
      }
      await activeStorage.insertCertificateField(initialData)

      // Create a CertificateField entity from the initial data
      const entity = new EntityCertificateField(initialData)

      // Simulate the `ei` argument with a later `updated_at`
      const updatedData: TableCertificateField = {
        ...initialData,
        updated_at: new Date(now.getTime() + 1000), // Later timestamp
        fieldValue: 'updatedValue',
        masterKey: 'updatedMasterKey'
      }

      const syncMap = createSyncMap()
      syncMap.certificate.idMap[certificateId] = certificateId

      // Call mergeExisting
      const wasMergedRaw = await entity.mergeExisting(
        activeStorage,
        undefined, // `since` is not used in this method
        updatedData,
        syncMap,
        undefined // `trx` is not used
      )

      const wasMerged = Boolean(wasMergedRaw)

      // Verify that wasMerged is true
      expect(wasMerged).toBe(true)

      // Verify that the entity is updated
      expect(entity.fieldValue).toBe('updatedValue')
      expect(entity.masterKey).toBe('updatedMasterKey')

      // Verify that the database is updated
      const updatedRecord = await activeStorage.findCertificateFields({
        partial: { certificateId, fieldName: 'field1' }
      })
      expect(updatedRecord.length).toBe(1)
      expect(updatedRecord[0]).toBeDefined()
      expect(updatedRecord[0].fieldValue).toBe('updatedValue')
      expect(updatedRecord[0].masterKey).toBe('updatedMasterKey')
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_certificate.py

```python
    def test_mergeexisting_updates_entity_and_database_when_ei_updated_at_greater_than_this_updated_at(
        self,
    ) -> None:
        """Given: Certificate entity with older updated_at
           When: Call merge_existing with newer updated_at
           Then: Entity and database are updated

        Reference: src/storage/schema/entities/__tests/CertificateTests.test.ts
                  test('2_mergeExisting updates entity and database when ei.updated_at > this.updated_at')
        """
        # Given

        now = datetime.now()
        certificate_id = 600
        certificate_data = {
            "certificateId": certificate_id,
            "created_at": now,
            "updated_at": now,
            "userId": 1,
            "type": "exampleTypeMerge",
            "serialNumber": "serialMerge123",
            "certifier": "02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef1234",
            "subject": "02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef5678",
            "revocationOutpoint": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890:0",
            "signature": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
            "isDeleted": False,
        }

        entity = Certificate(certificate_data)

        # Updated data with later timestamp
        updated_data = {
            **certificate_data,
            "updated_at": datetime.fromtimestamp(now.timestamp() + 1),
            "type": "updatedType",
            "subject": "updatedSubject",
            "serialNumber": "updatedSerialNumber",
            "revocationOutpoint": "updatedOutpoint:1",
            "signature": "updatedSignature",
            "verifier": "updatedVerifier",
            "isDeleted": True,
        }

        sync_map = {"certificate": {"idMap": {certificate_id: certificate_id}}}
        mock_storage = type("MockStorage", (), {})()

        # When
        was_merged = entity.merge_existing(mock_storage, None, updated_data, sync_map, None)

        # Then
        assert was_merged is True
        assert entity.type == "updatedType"
        assert entity.subject == "updatedSubject"
        assert entity.serial_number == "updatedSerialNumber"
        assert entity.revocation_outpoint == "updatedOutpoint:1"
        assert entity.signature == "updatedSignature"
        assert entity.verifier == "updatedVerifier"
        assert entity.is_deleted == 1
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: entity.fieldValue, entity.masterKey, updated_record.length
  - [HIGH] Python test is missing operations: entity.mergeExisting, active_storage.findCertificateFields, active_storage.insertCertificate, active_storage.insertCertificateField

**Differences:**
  - Operation count: TS has 4, PY has 0
  - Verification count: TS has 3, PY has 7

**Suggestions:**
  - Add verifications for: entity.fieldValue, entity.masterKey, updated_record.length
  - Add operations: entity.mergeExisting, active_storage.findCertificateFields, active_storage.insertCertificate

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: entity.fieldValue, entity.masterKey, updated_record.length
  • [HIGH] Python test is missing operations: entity.mergeExisting, active_storage.findCertificateFields, active_storage.insertCertificate, active_storage.insertCertificateField

Key Differences:
  • Operation count: TS has 4, PY has 0
  • Verification count: TS has 3, PY has 7

---

## Test 216: 0_equals identifies matching Certificate entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/CertificateTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_certificate.py`

---

## Test 217: 1_equals identifies non-matching Certificate entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/CertificateTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_certificate.py`

---

## Test 218: 2_mergeExisting updates entity and database when ei.updated_at > this.updated_at **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/CertificateTests.test.ts

```typescript
  test('2_mergeExisting updates entity and database when ei.updated_at > this.updated_at', async () => {
    for (const { activeStorage } of ctxs) {
      // Insert a valid Certificate to satisfy foreign key constraints
      const now = new Date()
      const certificateId = 600
      const certificateData: TableCertificate = {
        certificateId,
        created_at: now,
        updated_at: now,
        userId: 1,
        type: Buffer.from('exampleTypeMerge').toString('base64'),
        serialNumber: Buffer.from('serialMerge123').toString('base64'),
        certifier: '02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef1234',
        subject: '02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef5678',
        revocationOutpoint: 'abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890:0',
        signature: 'abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
        isDeleted: false
      }

      await activeStorage.insertCertificate(certificateData)

      // Create a Certificate entity from the initial data
      const entity = new EntityCertificate(certificateData)

      // Simulate the `ei` argument with a later `updated_at`
      const updatedData: TableCertificate = {
        ...certificateData,
        updated_at: new Date(now.getTime() + 1000), // Later timestamp
        type: 'updatedType',
        subject: 'updatedSubject',
        serialNumber: 'updatedSerialNumber',
        revocationOutpoint: 'updatedOutpoint:1',
        signature: 'updatedSignature',
        verifier: 'updatedVerifier',
        isDeleted: true
      }

      const syncMap = createSyncMap()
      syncMap.certificate.idMap[certificateId] = certificateId

      // Call mergeExisting
      const wasMergedRaw = await entity.mergeExisting(
        activeStorage,
        undefined, // `since` is not used in this method
        updatedData,
        syncMap,
        undefined // `trx` is not used
      )

      const wasMerged = Boolean(wasMergedRaw)

      // Verify that wasMerged is true
      expect(wasMerged).toBe(true)

      // Verify that the entity is updated
      expect(entity.type).toBe('updatedType')
      expect(entity.subject).toBe('updatedSubject')
      expect(entity.serialNumber).toBe('updatedSerialNumber')
      expect(entity.revocationOutpoint).toBe('updatedOutpoint:1')
      expect(entity.signature).toBe('updatedSignature')
      expect(entity.verifier).toBe('updatedVerifier')
      expect(entity.isDeleted).toBe(1)

      // Verify that the database is updated
      const updatedRecord = await activeStorage.findCertificates({
        partial: { certificateId }
      })
      expect(updatedRecord.length).toBe(1)
      expect(updatedRecord[0]).toBeDefined()
      expect(updatedRecord[0].type).toBe('updatedType')
      expect(updatedRecord[0].subject).toBe('updatedSubject')
      expect(updatedRecord[0].serialNumber).toBe('updatedSerialNumber')
      expect(updatedRecord[0].revocationOutpoint).toBe('updatedOutpoint:1')
      expect(updatedRecord[0].signature).toBe('updatedSignature')
      expect(updatedRecord[0].verifier).toBe('updatedVerifier')
      expect(updatedRecord[0].isDeleted).toBe(true)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_certificate.py

```python
    def test_mergeexisting_updates_entity_and_database_when_ei_updated_at_greater_than_this_updated_at(
        self,
    ) -> None:
        """Given: Certificate entity with older updated_at
           When: Call merge_existing with newer updated_at
           Then: Entity and database are updated

        Reference: src/storage/schema/entities/__tests/CertificateTests.test.ts
                  test('2_mergeExisting updates entity and database when ei.updated_at > this.updated_at')
        """
        # Given

        now = datetime.now()
        certificate_id = 600
        certificate_data = {
            "certificateId": certificate_id,
            "created_at": now,
            "updated_at": now,
            "userId": 1,
            "type": "exampleTypeMerge",
            "serialNumber": "serialMerge123",
            "certifier": "02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef1234",
            "subject": "02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef5678",
            "revocationOutpoint": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890:0",
            "signature": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
            "isDeleted": False,
        }

        entity = Certificate(certificate_data)

        # Updated data with later timestamp
        updated_data = {
            **certificate_data,
            "updated_at": datetime.fromtimestamp(now.timestamp() + 1),
            "type": "updatedType",
            "subject": "updatedSubject",
            "serialNumber": "updatedSerialNumber",
            "revocationOutpoint": "updatedOutpoint:1",
            "signature": "updatedSignature",
            "verifier": "updatedVerifier",
            "isDeleted": True,
        }

        sync_map = {"certificate": {"idMap": {certificate_id: certificate_id}}}
        mock_storage = type("MockStorage", (), {})()

        # When
        was_merged = entity.merge_existing(mock_storage, None, updated_data, sync_map, None)

        # Then
        assert was_merged is True
        assert entity.type == "updatedType"
        assert entity.subject == "updatedSubject"
        assert entity.serial_number == "updatedSerialNumber"
        assert entity.revocation_outpoint == "updatedOutpoint:1"
        assert entity.signature == "updatedSignature"
        assert entity.verifier == "updatedVerifier"
        assert entity.is_deleted == 1
```

### AI Analysis Results

**Similarity Score**: 39.58%
  - Structural: 0.00%
  - Semantic: 79.17%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: entity.serialNumber, entity.subject, entity.isDeleted, entity.signature, entity.type, entity.verifier, entity.revocationOutpoint, updated_record.length
  - [HIGH] Python test is missing operations: entity.mergeExisting, active_storage.insertCertificate, active_storage.findCertificates

**Differences:**
  - Operation count: TS has 3, PY has 0
  - Verification count: TS has 8, PY has 7

**Suggestions:**
  - Add verifications for: entity.serialNumber, entity.subject, entity.isDeleted
  - Add operations: entity.mergeExisting, active_storage.insertCertificate, active_storage.findCertificates

**Explanation:**

Overall Similarity: 39.6%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 79.2% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: entity.serialNumber, entity.subject, entity.isDeleted, entity.signature, entity.type, entity.verifier, entity.revocationOutpoint, updated_record.length
  • [HIGH] Python test is missing operations: entity.mergeExisting, active_storage.insertCertificate, active_storage.findCertificates

Key Differences:
  • Operation count: TS has 3, PY has 0
  • Verification count: TS has 8, PY has 7

---

## Test 219: 3_mergeExisting does not update entity when ei.updated_at <= this.updated_at **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/CertificateTests.test.ts

```typescript
  test('3_mergeExisting does not update entity when ei.updated_at <= this.updated_at', async () => {
    for (const { activeStorage } of ctxs) {
      // Insert a valid Certificate to satisfy foreign key constraints
      const now = new Date()
      const certificateId = 601
      const certificateData: TableCertificate = {
        certificateId,
        created_at: now,
        updated_at: now,
        userId: 1,
        type: 'exampleType',
        serialNumber: 'exampleSerialNumber',
        certifier: '02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef1234',
        subject: '02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef5678',
        revocationOutpoint: 'abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890:0',
        signature: 'abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
        isDeleted: false
      }

      await activeStorage.insertCertificate(certificateData)

      // Create a Certificate entity from the initial data
      const entity = new EntityCertificate(certificateData)

      // Simulate the `ei` argument with the same or earlier `updated_at`
      const sameUpdatedData: TableCertificate = {
        ...certificateData,
        updated_at: now, // Same timestamp
        type: 'unchangedType',
        subject: 'unchangedSubject',
        serialNumber: 'unchangedSerialNumber',
        revocationOutpoint: 'unchangedOutpoint:0',
        signature: 'unchangedSignature',
        verifier: 'unchangedVerifier',
        isDeleted: false
      }

      const syncMap = createSyncMap()
      syncMap.certificate.idMap[certificateId] = certificateId

      // Call mergeExisting
      const wasMergedRaw = await entity.mergeExisting(
        activeStorage,
        undefined, // `since` is not used
        sameUpdatedData,
        syncMap,
        undefined // `trx` is not used
      )

      const wasMerged = Boolean(wasMergedRaw)

      // Verify that wasMerged is false
      expect(wasMerged).toBe(false)

      // Verify that the entity is not updated
      expect(entity.type).toBe('exampleType')
      expect(entity.subject).toBe('02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef5678')
      expect(entity.serialNumber).toBe('exampleSerialNumber')
      expect(entity.revocationOutpoint).toBe('abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890:0')
      expect(entity.signature).toBe('abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890')
      expect(entity.isDeleted).toBe(0)

      // Verify that the database is not updated
      const unchangedRecord = await activeStorage.findCertificates({
        partial: { certificateId }
      })
      expect(unchangedRecord.length).toBe(1)
      expect(unchangedRecord[0]).toBeDefined()
      expect(unchangedRecord[0].type).toBe('exampleType')
      expect(unchangedRecord[0].subject).toBe('02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef5678')
      expect(unchangedRecord[0].serialNumber).toBe('exampleSerialNumber')
      expect(unchangedRecord[0].revocationOutpoint).toBe(
        'abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890:0'
      )
      expect(unchangedRecord[0].signature).toBe('abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890')
      expect(unchangedRecord[0].isDeleted).toBe(false)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_certificate.py

```python
    def test_mergeexisting_does_not_update_entity_when_ei_updated_at_less_than_or_equal_this_updated_at(
        self,
    ) -> None:
        """Given: Certificate entity with same or newer updated_at
           When: Call merge_existing with same or older updated_at
           Then: Entity is not updated

        Reference: src/storage/schema/entities/__tests/CertificateTests.test.ts
                  test('3_mergeExisting does not update entity when ei.updated_at <= this.updated_at')
        """
        # Given

        now = datetime.now()
        certificate_id = 601
        certificate_data = {
            "certificateId": certificate_id,
            "created_at": now,
            "updated_at": now,
            "userId": 1,
            "type": "exampleType",
            "serialNumber": "exampleSerialNumber",
            "certifier": "02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef1234",
            "subject": "02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef5678",
            "revocationOutpoint": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890:0",
            "signature": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
            "isDeleted": False,
        }

        entity = Certificate(certificate_data)

        # Same updated_at
        same_updated_data = {
            **certificate_data,
            "updated_at": now,
            "type": "unchangedType",
            "subject": "unchangedSubject",
        }

        sync_map = {"certificate": {"idMap": {certificate_id: certificate_id}}}
        mock_storage = type("MockStorage", (), {})()

        # When
        was_merged = entity.merge_existing(mock_storage, None, same_updated_data, sync_map, None)

        # Then
        assert was_merged is False
        assert entity.type == "exampleType"
        assert entity.subject == "02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef5678"
```

### AI Analysis Results

**Similarity Score**: 20.57%
  - Structural: 0.00%
  - Semantic: 41.14%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: entity.type, entity.serialNumber, entity.subject, unchanged_record.length, entity.isDeleted, entity.revocationOutpoint, entity.signature
  - [HIGH] Python test is missing operations: entity.mergeExisting, active_storage.insertCertificate, active_storage.findCertificates

**Differences:**
  - Operation count: TS has 3, PY has 0
  - Verification count: TS has 7, PY has 2

**Suggestions:**
  - Add verifications for: entity.type, entity.serialNumber, entity.subject
  - Add operations: entity.mergeExisting, active_storage.insertCertificate, active_storage.findCertificates

**Explanation:**

Overall Similarity: 20.6%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 41.1% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification key_change
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: entity.type, entity.serialNumber, entity.subject, unchanged_record.length, entity.isDeleted, entity.revocationOutpoint, entity.signature
  • [HIGH] Python test is missing operations: entity.mergeExisting, active_storage.insertCertificate, active_storage.findCertificates

Key Differences:
  • Operation count: TS has 3, PY has 0
  • Verification count: TS has 7, PY has 2

---

## Test 220: 4_Certificate class getters and setters **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/CertificateTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_certificate.py`

---

## Test 221: 0_equals identifies matching Commission entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/CommissionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_commission.py`

---

## Test 222: 1_equals identifies non-matching Commission entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/CommissionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_commission.py`

---

## Test 223: 2_mergeExisting updates entity and database when ei.updated_at > this.updated_at **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/CommissionTests.test.ts

```typescript
  test('2_mergeExisting updates entity and database when ei.updated_at > this.updated_at', async () => {
    for (const { activeStorage } of ctxs) {
      // Generate unique transactionId
      const transactionId = 203

      // Insert a valid transaction to satisfy foreign key constraints
      const now = new Date()
      const transactionData: TableTransaction = {
        transactionId,
        created_at: now,
        updated_at: now,
        userId: 1,
        txid: 'unique-txid',
        status: 'sending',
        reference: 'test-transaction-5',
        isOutgoing: false,
        satoshis: 1000,
        description: 'Test transaction'
      }
      await activeStorage.insertTransaction(transactionData)

      // Insert the initial Commission record
      const initialData: TableCommission = {
        commissionId: 803,
        created_at: now,
        updated_at: now,
        transactionId,
        userId: 1,
        isRedeemed: false,
        keyOffset: 'offset123',
        lockingScript: [1, 2, 3],
        satoshis: 500
      }
      await activeStorage.insertCommission(initialData)

      // Create a Commission entity from the initial data
      const entity = new EntityCommission(initialData)

      // Simulate the `ei` argument with a later `updated_at`
      const updatedData: TableCommission = {
        ...initialData,
        updated_at: new Date(now.getTime() + 1000),
        isRedeemed: true
      }

      const syncMap = createSyncMap()
      syncMap.transaction.idMap[transactionId] = transactionId

      // Call mergeExisting
      const wasMergedRaw = await entity.mergeExisting(
        activeStorage,
        undefined, // `since` is not used
        updatedData,
        syncMap,
        undefined // `trx` is not used
      )

      const wasMerged = Boolean(wasMergedRaw)

      // Verify that wasMerged is true
      expect(wasMerged).toBe(true)

      // Verify that the entity is updated
      expect(entity.isRedeemed).toBe(true)

      // Verify that the database is updated
      const updatedRecord = await activeStorage.findCommissions({
        partial: { commissionId: 803 }
      })
      expect(updatedRecord.length).toBe(1)
      expect(updatedRecord[0]).toBeDefined()
      expect(updatedRecord[0].isRedeemed).toBe(true)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_certificate.py

```python
    def test_mergeexisting_updates_entity_and_database_when_ei_updated_at_greater_than_this_updated_at(
        self,
    ) -> None:
        """Given: Certificate entity with older updated_at
           When: Call merge_existing with newer updated_at
           Then: Entity and database are updated

        Reference: src/storage/schema/entities/__tests/CertificateTests.test.ts
                  test('2_mergeExisting updates entity and database when ei.updated_at > this.updated_at')
        """
        # Given

        now = datetime.now()
        certificate_id = 600
        certificate_data = {
            "certificateId": certificate_id,
            "created_at": now,
            "updated_at": now,
            "userId": 1,
            "type": "exampleTypeMerge",
            "serialNumber": "serialMerge123",
            "certifier": "02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef1234",
            "subject": "02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef5678",
            "revocationOutpoint": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890:0",
            "signature": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
            "isDeleted": False,
        }

        entity = Certificate(certificate_data)

        # Updated data with later timestamp
        updated_data = {
            **certificate_data,
            "updated_at": datetime.fromtimestamp(now.timestamp() + 1),
            "type": "updatedType",
            "subject": "updatedSubject",
            "serialNumber": "updatedSerialNumber",
            "revocationOutpoint": "updatedOutpoint:1",
            "signature": "updatedSignature",
            "verifier": "updatedVerifier",
            "isDeleted": True,
        }

        sync_map = {"certificate": {"idMap": {certificate_id: certificate_id}}}
        mock_storage = type("MockStorage", (), {})()

        # When
        was_merged = entity.merge_existing(mock_storage, None, updated_data, sync_map, None)

        # Then
        assert was_merged is True
        assert entity.type == "updatedType"
        assert entity.subject == "updatedSubject"
        assert entity.serial_number == "updatedSerialNumber"
        assert entity.revocation_outpoint == "updatedOutpoint:1"
        assert entity.signature == "updatedSignature"
        assert entity.verifier == "updatedVerifier"
        assert entity.is_deleted == 1
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: entity.isRedeemed, updated_record.length
  - [HIGH] Python test is missing operations: active_storage.insertTransaction, active_storage.findCommissions, active_storage.insertCommission, entity.mergeExisting

**Differences:**
  - Operation count: TS has 4, PY has 0
  - Verification count: TS has 2, PY has 7

**Suggestions:**
  - Add verifications for: entity.isRedeemed, updated_record.length
  - Add operations: active_storage.insertTransaction, active_storage.findCommissions, active_storage.insertCommission

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: entity.isRedeemed, updated_record.length
  • [HIGH] Python test is missing operations: active_storage.insertTransaction, active_storage.findCommissions, active_storage.insertCommission, entity.mergeExisting

Key Differences:
  • Operation count: TS has 4, PY has 0
  • Verification count: TS has 2, PY has 7

---

## Test 224: 3_mergeExisting does not update when ei.updated_at <= this.updated_at **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/CommissionTests.test.ts

```typescript
  test('3_mergeExisting does not update when ei.updated_at <= this.updated_at', async () => {
    for (const { activeStorage } of ctxs) {
      // Generate unique transactionId
      const transactionId = 193

      // Insert a valid transaction to satisfy foreign key constraints
      const now = new Date()
      const transactionData: TableTransaction = {
        transactionId,
        created_at: now,
        updated_at: now,
        userId: 1,
        txid: 'unique-txid-193',
        status: 'sending',
        reference: 'test-transaction-6',
        isOutgoing: false,
        satoshis: 1000,
        description: 'Test transaction'
      }
      await activeStorage.insertTransaction(transactionData)

      // Insert the initial Commission record
      const initialData: TableCommission = {
        commissionId: 804,
        created_at: now,
        updated_at: now,
        transactionId,
        userId: 1,
        isRedeemed: false,
        keyOffset: 'offset123',
        lockingScript: [1, 2, 3],
        satoshis: 500
      }
      await activeStorage.insertCommission(initialData)

      // Create a Commission entity from the initial data
      const entity = new EntityCommission(initialData)

      // Simulate the `ei` argument with an earlier or equal `updated_at`
      const olderOrEqualData: TableCommission = {
        ...initialData,
        updated_at: new Date(now.getTime()),
        isRedeemed: true
      }

      const syncMap = createSyncMap()
      syncMap.transaction.idMap[transactionId] = transactionId

      // Call mergeExisting
      const wasMergedRaw = await entity.mergeExisting(
        activeStorage,
        undefined,
        olderOrEqualData,
        syncMap,
        undefined // `trx` is not used
      )

      const wasMerged = Boolean(wasMergedRaw)

      // Verify that wasMerged is false
      expect(wasMerged).toBe(false)

      // Verify that the entity is not updated
      expect(entity.isRedeemed).toBe(false)

      // Verify that the database is not updated
      const record = await activeStorage.findCommissions({
        partial: { commissionId: 802 }
      })
      expect(record.length).toBe(1)
      expect(record[0]).toBeDefined()
      expect(record[0].isRedeemed).toBe(false)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_commission.py

```python
    def test_mergeexisting_does_not_update_when_ei_updated_at_less_than_or_equal_this_updated_at(self) -> None:
        """Given: Commission entity with same or newer updated_at
           When: Call merge_existing with same or older updated_at
           Then: Entity is not updated, returns False

        Reference: src/storage/schema/entities/__tests/CommissionTests.test.ts
                  test('3_mergeExisting does not update when ei.updated_at <= this.updated_at')
        """
        # Given

        now = datetime.now()
        initial_data = {
            "commissionId": 804,
            "created_at": now,
            "updated_at": now,
            "transactionId": 193,
            "userId": 1,
            "isRedeemed": False,
            "keyOffset": "offset123",
            "lockingScript": [1, 2, 3],
            "satoshis": 500,
        }

        entity = Commission(initial_data)

        # Same timestamp
        older_or_equal_data = {**initial_data, "updated_at": now, "isRedeemed": True}

        sync_map = {"transaction": {"idMap": {193: 193}}}

        mock_storage = type("MockStorage", (), {})()

        # When
        was_merged = entity.merge_existing(mock_storage, None, older_or_equal_data, sync_map, None)

        # Then
        assert was_merged is False
        assert entity.is_redeemed is False
```

### AI Analysis Results

**Similarity Score**: 28.33%
  - Structural: 0.00%
  - Semantic: 56.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: entity.isRedeemed, record.length
  - [HIGH] Python test is missing operations: active_storage.insertTransaction, active_storage.findCommissions, active_storage.insertCommission, entity.mergeExisting

**Differences:**
  - Operation count: TS has 4, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Add verifications for: entity.isRedeemed, record.length
  - Add operations: active_storage.insertTransaction, active_storage.findCommissions, active_storage.insertCommission

**Explanation:**

Overall Similarity: 28.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 56.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: entity.isRedeemed, record.length
  • [HIGH] Python test is missing operations: active_storage.insertTransaction, active_storage.findCommissions, active_storage.insertCommission, entity.mergeExisting

Key Differences:
  • Operation count: TS has 4, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 225: 4_Commission entity getters and setters **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/CommissionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_commission.py`

---

## Test 226: 1_mergeExisting merges and updates entity when ei.updated_at > this.updated_at **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/OutputBasketTests.test.ts

```typescript
  test('1_mergeExisting merges and updates entity when ei.updated_at > this.updated_at', async () => {
    const ctx = ctxs[0]

    // Insert initial OutputBasket record with valid data
    const initialData: TableOutputBasket = {
      basketId: 100,
      created_at: new Date('2023-01-01'),
      updated_at: new Date('2023-01-02'),
      userId: 1,
      name: 'Basket1',
      numberOfDesiredUTXOs: 10,
      minimumDesiredUTXOValue: 5000,
      isDeleted: false
    }
    await ctx.activeStorage.insertOutputBasket(initialData)

    // Create an OutputBasket entity from the initial data
    const entity = new EntityOutputBasket(initialData)

    // Simulate the `ei` argument with a later `updated_at`
    const updatedData: TableOutputBasket = {
      ...initialData,
      updated_at: new Date('2023-01-03'), // Later timestamp
      numberOfDesiredUTXOs: 20, // Update this field
      minimumDesiredUTXOValue: 10000, // Update this field
      isDeleted: true // Simulate a change in `isDeleted`
    }

    const syncMap = createSyncMap()
    syncMap.outputBasket.idMap[100] = 100

    // Call mergeExisting
    const wasMergedRaw = await entity.mergeExisting(
      ctx.activeStorage,
      undefined, // `since` is not used in this method
      updatedData,
      syncMap,
      undefined // `trx` is not used
    )

    const wasMerged = Boolean(wasMergedRaw)

    // Verify that wasMerged is true
    expect(wasMerged).toBe(true)

    // Verify that the entity is updated
    expect(entity.numberOfDesiredUTXOs).toBe(20)
    expect(entity.minimumDesiredUTXOValue).toBe(10000)
    expect(entity.isDeleted).toBe(1)

    // Verify that the database is updated
    const updatedRecord = await ctx.activeStorage.findOutputBaskets({
      partial: { basketId: 100 }
    })
    expect(updatedRecord.length).toBe(1)
    expect(updatedRecord[0]).toBeDefined() // Ensure record exists
    expect(updatedRecord[0].numberOfDesiredUTXOs).toBe(20)
    expect(updatedRecord[0].minimumDesiredUTXOValue).toBe(10000)
    expect(updatedRecord[0].isDeleted).toBe(true)
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_output_basket.py

```python
    def test_mergeexisting_merges_and_updates_entity_when_ei_updated_at_greater_than_this_updated_at(
        self,
    ) -> None:
        """Given: OutputBasket entity with older updated_at
           When: Call merge_existing with newer updated_at
           Then: Entity and database are updated

        Reference: src/storage/schema/entities/__tests/OutputBasketTests.test.ts
                  test('1_mergeExisting merges and updates entity when ei.updated_at > this.updated_at')
        """
        # Given

        initial_data = {
            "basketId": 100,
            "created_at": datetime(2023, 1, 1),
            "updated_at": datetime(2023, 1, 2),
            "userId": 1,
            "name": "Basket1",
            "numberOfDesiredUTXOs": 10,
            "minimumDesiredUTXOValue": 5000,
            "isDeleted": False,
        }

        entity = OutputBasket(initial_data)

        # Updated data with later timestamp
        updated_data = {
            **initial_data,
            "updated_at": datetime(2023, 1, 3),
            "numberOfDesiredUTXOs": 20,
            "minimumDesiredUTXOValue": 10000,
            "isDeleted": True,
        }

        sync_map = {"outputBasket": {"idMap": {100: 100}}}
        mock_storage = type("MockStorage", (), {})()

        # When
        was_merged = entity.merge_existing(mock_storage, None, updated_data, sync_map, None)

        # Then
        assert was_merged is True
        assert entity.number_of_desired_utxos == 20
        assert entity.minimum_desired_utxo_value == 10000
        assert entity.is_deleted == 1
```

### AI Analysis Results

**Similarity Score**: 28.33%
  - Structural: 0.00%
  - Semantic: 56.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: updated_record.length, entity.numberOfDesiredUTXOs, entity.minimumDesiredUTXOValue, entity.isDeleted
  - [HIGH] Python test is missing operations: entity.mergeExisting

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 4, PY has 3

**Suggestions:**
  - Add verifications for: updated_record.length, entity.numberOfDesiredUTXOs, entity.minimumDesiredUTXOValue
  - Add operations: entity.mergeExisting

**Explanation:**

Overall Similarity: 28.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 56.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: updated_record.length, entity.numberOfDesiredUTXOs, entity.minimumDesiredUTXOValue, entity.isDeleted
  • [HIGH] Python test is missing operations: entity.mergeExisting

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 4, PY has 3

---

## Test 227: 2_mergeExisting does not merge when ei.updated_at <= this.updated_at **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/OutputBasketTests.test.ts

```typescript
  test('2_mergeExisting does not merge when ei.updated_at <= this.updated_at', async () => {
    const ctx = ctxs[0]

    // Insert initial OutputBasket record with valid data
    const initialData: TableOutputBasket = {
      basketId: 200,
      created_at: new Date('2023-01-01'),
      updated_at: new Date('2023-01-02'),
      userId: 1,
      name: 'Basket2',
      numberOfDesiredUTXOs: 10,
      minimumDesiredUTXOValue: 5000,
      isDeleted: false
    }
    await ctx.activeStorage.insertOutputBasket(initialData)

    // Create an OutputBasket entity from the initial data
    const entity = new EntityOutputBasket(initialData)

    // Simulate the `ei` argument with an earlier `updated_at`
    const earlierData: TableOutputBasket = {
      ...initialData,
      updated_at: new Date('2023-01-01'), // Earlier timestamp
      numberOfDesiredUTXOs: 20, // Simulate a change
      minimumDesiredUTXOValue: 10000, // Simulate a change
      isDeleted: true // Simulate a change
    }

    const syncMap = createSyncMap()
    syncMap.outputBasket.idMap[200] = 200

    // Call mergeExisting
    const wasMergedRaw = await entity.mergeExisting(
      ctx.activeStorage,
      undefined, // `since` is not used in this method
      earlierData,
      syncMap,
      undefined // `trx` is not used
    )

    const wasMerged = Boolean(wasMergedRaw)

    // Verify that wasMerged is false
    expect(wasMerged).toBe(false)

    // Verify that the entity is not updated
    expect(entity.numberOfDesiredUTXOs).toBe(10)
    expect(entity.minimumDesiredUTXOValue).toBe(5000)
    expect(entity.isDeleted).toBe(0)

    // Verify that the database is not updated
    const updatedRecord = await ctx.activeStorage.findOutputBaskets({
      partial: { basketId: 200 }
    })
    expect(updatedRecord.length).toBe(1)
    expect(updatedRecord[0]).toBeDefined() // Ensure record exists
    expect(updatedRecord[0].numberOfDesiredUTXOs).toBe(10)
    expect(updatedRecord[0].minimumDesiredUTXOValue).toBe(5000)
    expect(updatedRecord[0].isDeleted).toBe(false)
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_output_basket.py

```python
    def test_mergeexisting_does_not_merge_when_ei_updated_at_less_than_or_equal_this_updated_at(self) -> None:
        """Given: OutputBasket entity with same or newer updated_at
           When: Call merge_existing with same or older updated_at
           Then: Entity is not updated

        Reference: src/storage/schema/entities/__tests/OutputBasketTests.test.ts
                  test('2_mergeExisting does not merge when ei.updated_at <= this.updated_at')
        """
        # Given

        initial_data = {
            "basketId": 200,
            "created_at": datetime(2023, 1, 1),
            "updated_at": datetime(2023, 1, 2),
            "userId": 1,
            "name": "Basket2",
            "numberOfDesiredUTXOs": 10,
            "minimumDesiredUTXOValue": 5000,
            "isDeleted": False,
        }

        entity = OutputBasket(initial_data)

        # Earlier data
        earlier_data = {
            **initial_data,
            "updated_at": datetime(2023, 1, 1),
            "numberOfDesiredUTXOs": 20,
            "minimumDesiredUTXOValue": 10000,
            "isDeleted": True,
        }

        sync_map = {"outputBasket": {"idMap": {200: 200}}}
        mock_storage = type("MockStorage", (), {})()

        # When
        was_merged = entity.merge_existing(mock_storage, None, earlier_data, sync_map, None)

        # Then
        assert was_merged is False
        assert entity.number_of_desired_utxos == 10
        assert entity.minimum_desired_utxo_value == 5000
        assert entity.is_deleted == 0
```

### AI Analysis Results

**Similarity Score**: 28.33%
  - Structural: 0.00%
  - Semantic: 56.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: updated_record.length, entity.numberOfDesiredUTXOs, entity.minimumDesiredUTXOValue, entity.isDeleted
  - [HIGH] Python test is missing operations: entity.mergeExisting

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 4, PY has 3

**Suggestions:**
  - Add verifications for: updated_record.length, entity.numberOfDesiredUTXOs, entity.minimumDesiredUTXOValue
  - Add operations: entity.mergeExisting

**Explanation:**

Overall Similarity: 28.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 56.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: updated_record.length, entity.numberOfDesiredUTXOs, entity.minimumDesiredUTXOValue, entity.isDeleted
  • [HIGH] Python test is missing operations: entity.mergeExisting

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 4, PY has 3

---

## Test 228: OutputBasket getters, setters, and updateApi **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputBasketTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output_basket.py`

---

## Test 229: equals identifies matching entities with and without SyncMap **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputBasketTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output.py`

---

## Test 230: equals identifies non-matching entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputBasketTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output.py`

---

## Test 231: equals identifies non-matching entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputBasketTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output_basket.py`

---

## Test 232: equals identifies non-matching entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputBasketTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx_req.py`

---

## Test 233: equals identifies non-matching entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputBasketTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 234: equals identifies non-matching entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputBasketTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_tx_label.py`

---

## Test 235: equals identifies non-matching entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputBasketTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_users.py`

---

## Test 236: 0_OutputTagMap getters and setters **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputTagMapTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output_tag_map.py`

---

## Test 237: 1_equals returns true for matching entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputTagMapTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output_tag_map.py`

---

## Test 238: 2_equals returns false for non-matching entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputTagMapTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output_tag_map.py`

---

## Test 239: 3_mergeExisting merges and updates entity when ei.updated_at > this.updated_at **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/OutputTagMapTests.test.ts

```typescript
  test('3_mergeExisting merges and updates entity when ei.updated_at > this.updated_at', async () => {
    const ctx = ctxs[0]

    // Insert initial OutputTagMap record with valid foreign key IDs
    const initialData: TableOutputTagMap = {
      created_at: new Date('2023-01-01'),
      updated_at: new Date('2023-01-02'),
      outputId: 2,
      outputTagId: 8,
      isDeleted: false
    }
    await ctx.activeStorage.insertOutputTagMap(initialData)

    // Create an OutputTagMap entity from the initial data
    const entity = new EntityOutputTagMap(initialData)

    // Create a new record to simulate the `ei` argument with a later `updated_at`
    const updatedData: TableOutputTagMap = {
      ...initialData,
      updated_at: new Date('2023-01-03'), // Later timestamp
      isDeleted: true // Simulate a change in `isDeleted`
    }

    const syncMap = createSyncMap()
    syncMap.output.idMap[1] = 1

    // Call mergeExisting
    const wasMergedRaw = await entity.mergeExisting(
      ctx.activeStorage,
      undefined, // `since` is not used in this method
      updatedData,
      syncMap
    )

    const wasMerged = Boolean(wasMergedRaw)

    // Verify that wasMerged is true
    expect(wasMerged).toBe(true)

    // Verify that the entity is updated
    expect(entity.isDeleted).toBe(1)

    // Debugging: Log the updated record query
    const updatedRecord = await ctx.activeStorage.findOutputTagMaps({
      partial: { outputId: 2, outputTagId: 8 }
    })
    //console.log('Updated Record:', updatedRecord)
    //console.log('Updated Record isDeleted:', updatedRecord[0].isDeleted)
    //console.log('Updted Redord length:', updatedRecord.length)

    // Verify that the database is updated
    expect(updatedRecord.length).toBe(1)
    expect(updatedRecord[0]).toBeDefined()
    expect(updatedRecord[0].isDeleted).toBe(true)
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_output_basket.py

```python
    def test_mergeexisting_merges_and_updates_entity_when_ei_updated_at_greater_than_this_updated_at(
        self,
    ) -> None:
        """Given: OutputBasket entity with older updated_at
           When: Call merge_existing with newer updated_at
           Then: Entity and database are updated

        Reference: src/storage/schema/entities/__tests/OutputBasketTests.test.ts
                  test('1_mergeExisting merges and updates entity when ei.updated_at > this.updated_at')
        """
        # Given

        initial_data = {
            "basketId": 100,
            "created_at": datetime(2023, 1, 1),
            "updated_at": datetime(2023, 1, 2),
            "userId": 1,
            "name": "Basket1",
            "numberOfDesiredUTXOs": 10,
            "minimumDesiredUTXOValue": 5000,
            "isDeleted": False,
        }

        entity = OutputBasket(initial_data)

        # Updated data with later timestamp
        updated_data = {
            **initial_data,
            "updated_at": datetime(2023, 1, 3),
            "numberOfDesiredUTXOs": 20,
            "minimumDesiredUTXOValue": 10000,
            "isDeleted": True,
        }

        sync_map = {"outputBasket": {"idMap": {100: 100}}}
        mock_storage = type("MockStorage", (), {})()

        # When
        was_merged = entity.merge_existing(mock_storage, None, updated_data, sync_map, None)

        # Then
        assert was_merged is True
        assert entity.number_of_desired_utxos == 20
        assert entity.minimum_desired_utxo_value == 10000
        assert entity.is_deleted == 1
```

### AI Analysis Results

**Similarity Score**: 27.00%
  - Structural: 0.00%
  - Semantic: 54.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: entity.isDeleted, updated_record.length
  - [HIGH] Python test is missing operations: entity.mergeExisting

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 3

**Suggestions:**
  - Add verifications for: entity.isDeleted, updated_record.length
  - Add operations: entity.mergeExisting

**Explanation:**

Overall Similarity: 27.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 54.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification key_change
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: entity.isDeleted, updated_record.length
  • [HIGH] Python test is missing operations: entity.mergeExisting

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 3

---

## Test 240: 4_mergeExisting does not merge when ei.updated_at <= this.updated_at **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/OutputTagMapTests.test.ts

```typescript
  test('4_mergeExisting does not merge when ei.updated_at <= this.updated_at', async () => {
    const ctx = ctxs[0]

    // Insert initial OutputTagMap record
    const initialData: TableOutputTagMap = {
      created_at: new Date('2023-01-01'),
      updated_at: new Date('2023-01-02'),
      outputId: 2,
      outputTagId: 11,
      isDeleted: false
    }
    await ctx.activeStorage.insertOutputTagMap(initialData)

    // Create an OutputTagMap entity from the initial data
    const entity = new EntityOutputTagMap(initialData)

    // Create a new record to simulate the `ei` argument with an earlier `updated_at`
    const earlierData: TableOutputTagMap = {
      ...initialData,
      updated_at: new Date('2023-01-01'), // Earlier timestamp
      isDeleted: true // Simulate a change in `isDeleted`
    }

    const syncMap = createSyncMap()
    syncMap.output.idMap[101] = 101

    // Call mergeExisting
    const wasMergedRaw = await entity.mergeExisting(
      ctx.activeStorage,
      undefined, // `since` is not used in this method
      earlierData,
      syncMap
    )

    // Normalize the result
    const wasMerged = Boolean(wasMergedRaw)

    // Verify that wasMerged is false
    expect(wasMerged).toBe(false)

    // Verify that the entity is not updated
    expect(entity.isDeleted).toBe(0)

    // Verify that the database is not updated
    const record = await ctx.activeStorage.findOutputTagMaps({
      partial: { outputId: 2, outputTagId: 11 }
    })
    expect(record.length).toBe(1)
    expect(record[0].isDeleted).toBe(false)
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_output_basket.py

```python
    def test_mergeexisting_does_not_merge_when_ei_updated_at_less_than_or_equal_this_updated_at(self) -> None:
        """Given: OutputBasket entity with same or newer updated_at
           When: Call merge_existing with same or older updated_at
           Then: Entity is not updated

        Reference: src/storage/schema/entities/__tests/OutputBasketTests.test.ts
                  test('2_mergeExisting does not merge when ei.updated_at <= this.updated_at')
        """
        # Given

        initial_data = {
            "basketId": 200,
            "created_at": datetime(2023, 1, 1),
            "updated_at": datetime(2023, 1, 2),
            "userId": 1,
            "name": "Basket2",
            "numberOfDesiredUTXOs": 10,
            "minimumDesiredUTXOValue": 5000,
            "isDeleted": False,
        }

        entity = OutputBasket(initial_data)

        # Earlier data
        earlier_data = {
            **initial_data,
            "updated_at": datetime(2023, 1, 1),
            "numberOfDesiredUTXOs": 20,
            "minimumDesiredUTXOValue": 10000,
            "isDeleted": True,
        }

        sync_map = {"outputBasket": {"idMap": {200: 200}}}
        mock_storage = type("MockStorage", (), {})()

        # When
        was_merged = entity.merge_existing(mock_storage, None, earlier_data, sync_map, None)

        # Then
        assert was_merged is False
        assert entity.number_of_desired_utxos == 10
        assert entity.minimum_desired_utxo_value == 5000
        assert entity.is_deleted == 0
```

### AI Analysis Results

**Similarity Score**: 28.33%
  - Structural: 0.00%
  - Semantic: 56.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: entity.isDeleted, record.length
  - [HIGH] Python test is missing operations: entity.mergeExisting

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 3

**Suggestions:**
  - Add verifications for: entity.isDeleted, record.length
  - Add operations: entity.mergeExisting

**Explanation:**

Overall Similarity: 28.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 56.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: entity.isDeleted, record.length
  • [HIGH] Python test is missing operations: entity.mergeExisting

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 3

---

## Test 241: 0_mergeExisting merges and updates entity when ei.updated_at > this.updated_at **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/OutputTagTests.test.ts

```typescript
  test('0_mergeExisting merges and updates entity when ei.updated_at > this.updated_at', async () => {
    const ctx = ctxs[0]

    // Insert initial OutputTag record with valid userId
    const initialData: TableOutputTag = {
      outputTagId: 401,
      created_at: new Date('2023-01-01'),
      updated_at: new Date('2023-01-02'),
      tag: 'tag1',
      userId: 1,
      isDeleted: false
    }
    await ctx.activeStorage.insertOutputTag(initialData)

    // Create an OutputTag entity from the initial data
    const entity = new EntityOutputTag(initialData)

    // Simulate the `ei` argument with a later `updated_at`
    const updatedData: TableOutputTag = {
      ...initialData,
      updated_at: new Date('2023-01-03'), // Later timestamp
      isDeleted: true // Simulate a change in `isDeleted`
    }

    const syncMap = createSyncMap()
    syncMap.outputTag.idMap[401] = 401

    // Call mergeExisting
    const wasMergedRaw = await entity.mergeExisting(
      ctx.activeStorage,
      undefined, // `since` is not used in this method
      updatedData,
      syncMap,
      undefined
    )

    const wasMerged = Boolean(wasMergedRaw)

    // Verify that wasMerged is true
    expect(wasMerged).toBe(true)

    // Verify that the entity is updated
    expect(entity.isDeleted).toBe(1)

    // Verify that the database is updated
    const updatedRecord = await ctx.activeStorage.findOutputTags({
      partial: { outputTagId: 401 }
    })
    expect(updatedRecord.length).toBe(1)
    expect(updatedRecord[0]).toBeDefined()
    expect(updatedRecord[0].isDeleted).toBe(true)
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_output_basket.py

```python
    def test_mergeexisting_merges_and_updates_entity_when_ei_updated_at_greater_than_this_updated_at(
        self,
    ) -> None:
        """Given: OutputBasket entity with older updated_at
           When: Call merge_existing with newer updated_at
           Then: Entity and database are updated

        Reference: src/storage/schema/entities/__tests/OutputBasketTests.test.ts
                  test('1_mergeExisting merges and updates entity when ei.updated_at > this.updated_at')
        """
        # Given

        initial_data = {
            "basketId": 100,
            "created_at": datetime(2023, 1, 1),
            "updated_at": datetime(2023, 1, 2),
            "userId": 1,
            "name": "Basket1",
            "numberOfDesiredUTXOs": 10,
            "minimumDesiredUTXOValue": 5000,
            "isDeleted": False,
        }

        entity = OutputBasket(initial_data)

        # Updated data with later timestamp
        updated_data = {
            **initial_data,
            "updated_at": datetime(2023, 1, 3),
            "numberOfDesiredUTXOs": 20,
            "minimumDesiredUTXOValue": 10000,
            "isDeleted": True,
        }

        sync_map = {"outputBasket": {"idMap": {100: 100}}}
        mock_storage = type("MockStorage", (), {})()

        # When
        was_merged = entity.merge_existing(mock_storage, None, updated_data, sync_map, None)

        # Then
        assert was_merged is True
        assert entity.number_of_desired_utxos == 20
        assert entity.minimum_desired_utxo_value == 10000
        assert entity.is_deleted == 1
```

### AI Analysis Results

**Similarity Score**: 28.33%
  - Structural: 0.00%
  - Semantic: 56.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: entity.isDeleted, updated_record.length
  - [HIGH] Python test is missing operations: entity.mergeExisting

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 3

**Suggestions:**
  - Add verifications for: entity.isDeleted, updated_record.length
  - Add operations: entity.mergeExisting

**Explanation:**

Overall Similarity: 28.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 56.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: entity.isDeleted, updated_record.length
  • [HIGH] Python test is missing operations: entity.mergeExisting

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 3

---

## Test 242: 1_mergeExisting does not merge when ei.updated_at <= this.updated_at **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/OutputTagTests.test.ts

```typescript
  test('1_mergeExisting does not merge when ei.updated_at <= this.updated_at', async () => {
    const ctx = ctxs[0]

    // Insert initial OutputTag record with valid userId
    const initialData: TableOutputTag = {
      outputTagId: 402,
      created_at: new Date('2023-01-01'),
      updated_at: new Date('2023-01-02'),
      tag: 'tag2',
      userId: 1, // Valid user ID
      isDeleted: false
    }
    await ctx.activeStorage.insertOutputTag(initialData)

    // Create an OutputTag entity from the initial data
    const entity = new EntityOutputTag(initialData)

    // Simulate the `ei` argument with an earlier or equal `updated_at`
    const earlierData: TableOutputTag = {
      ...initialData,
      updated_at: new Date('2023-01-01'), // Earlier timestamp
      isDeleted: true // Simulate a change in `isDeleted`
    }

    const syncMap = createSyncMap()
    syncMap.outputTag.idMap[1] = 1

    // Call mergeExisting
    const wasMergedRaw = await entity.mergeExisting(
      ctx.activeStorage,
      undefined, // `since` is not used in this method
      earlierData,
      syncMap,
      undefined
    )

    const wasMerged = Boolean(wasMergedRaw)

    // Verify that wasMerged is false
    expect(wasMerged).toBe(false)

    // Verify that the entity is not updated
    expect(entity.isDeleted).toBe(0)

    // Verify that the database is not updated
    const record = await ctx.activeStorage.findOutputTags({
      partial: { outputTagId: 1 }
    })
    expect(record.length).toBe(1)
    expect(record[0].isDeleted).toBe(false)
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_output_basket.py

```python
    def test_mergeexisting_does_not_merge_when_ei_updated_at_less_than_or_equal_this_updated_at(self) -> None:
        """Given: OutputBasket entity with same or newer updated_at
           When: Call merge_existing with same or older updated_at
           Then: Entity is not updated

        Reference: src/storage/schema/entities/__tests/OutputBasketTests.test.ts
                  test('2_mergeExisting does not merge when ei.updated_at <= this.updated_at')
        """
        # Given

        initial_data = {
            "basketId": 200,
            "created_at": datetime(2023, 1, 1),
            "updated_at": datetime(2023, 1, 2),
            "userId": 1,
            "name": "Basket2",
            "numberOfDesiredUTXOs": 10,
            "minimumDesiredUTXOValue": 5000,
            "isDeleted": False,
        }

        entity = OutputBasket(initial_data)

        # Earlier data
        earlier_data = {
            **initial_data,
            "updated_at": datetime(2023, 1, 1),
            "numberOfDesiredUTXOs": 20,
            "minimumDesiredUTXOValue": 10000,
            "isDeleted": True,
        }

        sync_map = {"outputBasket": {"idMap": {200: 200}}}
        mock_storage = type("MockStorage", (), {})()

        # When
        was_merged = entity.merge_existing(mock_storage, None, earlier_data, sync_map, None)

        # Then
        assert was_merged is False
        assert entity.number_of_desired_utxos == 10
        assert entity.minimum_desired_utxo_value == 5000
        assert entity.is_deleted == 0
```

### AI Analysis Results

**Similarity Score**: 28.33%
  - Structural: 0.00%
  - Semantic: 56.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: entity.isDeleted, record.length
  - [HIGH] Python test is missing operations: entity.mergeExisting

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 3

**Suggestions:**
  - Add verifications for: entity.isDeleted, record.length
  - Add operations: entity.mergeExisting

**Explanation:**

Overall Similarity: 28.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 56.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: entity.isDeleted, record.length
  • [HIGH] Python test is missing operations: entity.mergeExisting

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 3

---

## Test 243: 2_equals identifies matching entities without syncMap **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputTagTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output_tag.py`

---

## Test 244: 3_equals identifies non-matching entities when tags differ **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputTagTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output_tag.py`

---

## Test 245: 4_equals identifies non-matching entities when isDeleted differs **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputTagTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output_tag.py`

---

## Test 246: 5_equals identifies matching entities with syncMap **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputTagTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output_tag.py`

---

## Test 247: 6_equals identifies non-matching entities when userIds differ and no syncMap is provided **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputTagTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output_tag.py`

---

## Test 248: 7_getters and setters work as expected for OutputTag **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputTagTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output_tag.py`

---

## Test 249: 0_equals identifies matching entities with and without SyncMap **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output.py`

---

## Test 250: 1_equals identifies non-matching entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output.py`

---

## Test 251: 2_equals handles optional fields and arrays **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/OutputTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output.py`

---

## Test 252: 3_mergeExisting updates entity and database when ei.updated_at > this.updated_at **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/OutputTests.test.ts

```typescript
  test('3_mergeExisting updates entity and database when ei.updated_at > this.updated_at', async () => {
    const ctx = ctxs[0]

    // Insert initial Output record
    const initialData: TableOutput = {
      outputId: 701,
      created_at: new Date('2023-01-01'),
      updated_at: new Date('2023-01-02'),
      userId: 1,
      transactionId: 103,
      basketId: 1,
      spendable: true,
      change: false,
      satoshis: 1000,
      outputDescription: 'Initial Output',
      vout: 50,
      type: 'p2pkh',
      providedBy: 'you',
      purpose: 'initial',
      txid: 'txid201',
      spendingDescription: 'Initial Spending',
      derivationPrefix: 'm/44',
      derivationSuffix: '/0/0',
      senderIdentityKey: 'key201',
      customInstructions: 'none',
      lockingScript: [1, 2, 3],
      scriptLength: 10,
      scriptOffset: 0,
      spentBy: undefined
    }

    await ctx.activeStorage.insertOutput(initialData)

    // Create an Output entity from the initial data
    const entity = new EntityOutput(initialData)

    // Simulate the `ei` argument with a later `updated_at`
    const updatedData: TableOutput = {
      ...initialData,
      updated_at: new Date('2023-01-03'), // Later timestamp
      spendable: false,
      change: true,
      type: 'p2sh',
      providedBy: 'storage',
      purpose: 'updated',
      outputDescription: 'Updated Output',
      spendingDescription: 'Updated Spending',
      senderIdentityKey: 'key202',
      customInstructions: 'new instructions',
      scriptLength: 15,
      scriptOffset: 5,
      lockingScript: [4, 5, 6],
      spentBy: 105
    }

    const syncMap = createSyncMap()
    syncMap.transaction.idMap = { 103: 103, 105: 105 }
    syncMap.outputBasket.idMap[1] = 1

    // Call mergeExisting
    const wasMergedRaw = await entity.mergeExisting(
      ctx.activeStorage,
      undefined, // `since` is not used in this method
      updatedData,
      syncMap,
      undefined // `trx` is not used
    )

    const wasMerged = Boolean(wasMergedRaw)

    // Verify that wasMerged is true
    expect(wasMerged).toBe(true)

    // Verify that the entity is updated
    expect(entity.spentBy).toBe(105)
    expect(entity.spendable).toBe(false)
    expect(entity.change).toBe(true)
    expect(entity.type).toBe('p2sh')
    expect(entity.providedBy).toBe('storage')
    expect(entity.purpose).toBe('updated')
    expect(entity.outputDescription).toBe('Updated Output')
    expect(entity.spendingDescription).toBe('Updated Spending')
    expect(entity.senderIdentityKey).toBe('key202')
    expect(entity.customInstructions).toBe('new instructions')
    expect(entity.scriptLength).toBe(15)
    expect(entity.scriptOffset).toBe(5)

    // Convert Buffer to array for comparison
    if (entity.lockingScript instanceof Buffer) {
      expect([...entity.lockingScript]).toEqual([4, 5, 6])
    } else {
      expect(entity.lockingScript).toEqual([4, 5, 6])
    }

    // Verify that the database is updated
    const updatedRecord = await ctx.activeStorage.findOutputs({
      partial: { outputId: 701 }
    })
    expect(updatedRecord.length).toBe(1)
    expect(updatedRecord[0]).toBeDefined()
    expect(updatedRecord[0].spendable).toBe(false)
    expect(updatedRecord[0].type).toBe('p2sh')

    // Handle undefined lockingScript gracefully
    if (updatedRecord[0].lockingScript) {
      expect(Buffer.from(updatedRecord[0].lockingScript).toJSON().data).toEqual([4, 5, 6])
    } else {
      throw new Error('lockingScript is undefined')
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_certificate.py

```python
    def test_mergeexisting_updates_entity_and_database_when_ei_updated_at_greater_than_this_updated_at(
        self,
    ) -> None:
        """Given: Certificate entity with older updated_at
           When: Call merge_existing with newer updated_at
           Then: Entity and database are updated

        Reference: src/storage/schema/entities/__tests/CertificateTests.test.ts
                  test('2_mergeExisting updates entity and database when ei.updated_at > this.updated_at')
        """
        # Given

        now = datetime.now()
        certificate_id = 600
        certificate_data = {
            "certificateId": certificate_id,
            "created_at": now,
            "updated_at": now,
            "userId": 1,
            "type": "exampleTypeMerge",
            "serialNumber": "serialMerge123",
            "certifier": "02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef1234",
            "subject": "02c123eabcdeff1234567890abcdef1234567890abcdef1234567890abcdef5678",
            "revocationOutpoint": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890:0",
            "signature": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
            "isDeleted": False,
        }

        entity = Certificate(certificate_data)

        # Updated data with later timestamp
        updated_data = {
            **certificate_data,
            "updated_at": datetime.fromtimestamp(now.timestamp() + 1),
            "type": "updatedType",
            "subject": "updatedSubject",
            "serialNumber": "updatedSerialNumber",
            "revocationOutpoint": "updatedOutpoint:1",
            "signature": "updatedSignature",
            "verifier": "updatedVerifier",
            "isDeleted": True,
        }

        sync_map = {"certificate": {"idMap": {certificate_id: certificate_id}}}
        mock_storage = type("MockStorage", (), {})()

        # When
        was_merged = entity.merge_existing(mock_storage, None, updated_data, sync_map, None)

        # Then
        assert was_merged is True
        assert entity.type == "updatedType"
        assert entity.subject == "updatedSubject"
        assert entity.serial_number == "updatedSerialNumber"
        assert entity.revocation_outpoint == "updatedOutpoint:1"
        assert entity.signature == "updatedSignature"
        assert entity.verifier == "updatedVerifier"
        assert entity.is_deleted == 1
```

### AI Analysis Results

**Similarity Score**: 14.14%
  - Structural: 0.00%
  - Semantic: 28.29%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'authentication value_verification verification key_change' but PY verifies 'verification'
  - [HIGH] Python test is missing verifications: entity.senderIdentityKey, entity.purpose, entity.customInstructions, entity.lockingScript, entity.spentBy, entity.scriptLength, entity.outputDescription, entity.scriptOffset, entity.type, entity.spendingDescription, entity.change, entity.spendable, entity.providedBy, updated_record.length
  - [HIGH] Python test is missing operations: entity.mergeExisting

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 14, PY has 7

**Suggestions:**
  - Align test intent: ensure PY test verifies 'authentication value_verification verification key_change'
  - Add verifications for: entity.senderIdentityKey, entity.purpose, entity.customInstructions
  - Add operations: entity.mergeExisting

**Explanation:**

Overall Similarity: 14.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 28.3% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: authentication value_verification verification key_change
  • Python: verification

Critical Issues (3):
  • [HIGH] Test intent differs: TS verifies 'authentication value_verification verification key_change' but PY verifies 'verification'
  • [HIGH] Python test is missing verifications: entity.senderIdentityKey, entity.purpose, entity.customInstructions, entity.lockingScript, entity.spentBy, entity.scriptLength, entity.outputDescription, entity.scriptOffset, entity.type, entity.spendingDescription, entity.change, entity.spendable, entity.providedBy, updated_record.length
  • [HIGH] Python test is missing operations: entity.mergeExisting

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 14, PY has 7

---

## Test 253: 4_mergeExisting does not update when ei.updated_at <= this.updated_at **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/OutputTests.test.ts

```typescript
  test('4_mergeExisting does not update when ei.updated_at <= this.updated_at', async () => {
    const ctx = ctxs[0]

    // Use the same initialData as before
    const initialData: TableOutput = {
      outputId: 702,
      created_at: new Date('2023-01-01'),
      updated_at: new Date('2023-01-02'),
      userId: 1,
      transactionId: 104,
      basketId: 1,
      spendable: true,
      change: false,
      satoshis: 1000,
      outputDescription: 'Initial Output',
      vout: 50,
      type: 'p2pkh',
      providedBy: 'you',
      purpose: 'initial',
      txid: 'txid202',
      spendingDescription: 'Initial Spending',
      derivationPrefix: 'm/44',
      derivationSuffix: '/0/0',
      senderIdentityKey: 'key202',
      customInstructions: 'none',
      lockingScript: [1, 2, 3],
      scriptLength: 10,
      scriptOffset: 0,
      spentBy: undefined
    }

    await ctx.activeStorage.insertOutput(initialData)

    // Create an Output entity from the initial data
    const entity = new EntityOutput(initialData)

    // Simulate the `ei` argument with an earlier `updated_at`
    const earlierData: TableOutput = {
      ...initialData,
      updated_at: new Date('2023-01-01'), // Earlier timestamp
      spendable: false
    }

    const syncMap = createSyncMap()
    syncMap.transaction.idMap = { 104: 104 }
    syncMap.outputBasket.idMap[1] = 1

    // Call mergeExisting
    const wasMergedRaw = await entity.mergeExisting(ctx.activeStorage, undefined, earlierData, syncMap, undefined)

    const wasMerged = Boolean(wasMergedRaw)

    // Verify that wasMerged is false
    expect(wasMerged).toBe(false)

    // Verify that the entity is not updated
    expect(entity.spendable).toBe(true)

    // Verify that the database is not updated
    const unchangedRecord = await ctx.activeStorage.findOutputs({
      partial: { outputId: 702 }
    })
    expect(unchangedRecord.length).toBe(1)
    expect(unchangedRecord[0].spendable).toBe(true)
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_commission.py

```python
    def test_mergeexisting_does_not_update_when_ei_updated_at_less_than_or_equal_this_updated_at(self) -> None:
        """Given: Commission entity with same or newer updated_at
           When: Call merge_existing with same or older updated_at
           Then: Entity is not updated, returns False

        Reference: src/storage/schema/entities/__tests/CommissionTests.test.ts
                  test('3_mergeExisting does not update when ei.updated_at <= this.updated_at')
        """
        # Given

        now = datetime.now()
        initial_data = {
            "commissionId": 804,
            "created_at": now,
            "updated_at": now,
            "transactionId": 193,
            "userId": 1,
            "isRedeemed": False,
            "keyOffset": "offset123",
            "lockingScript": [1, 2, 3],
            "satoshis": 500,
        }

        entity = Commission(initial_data)

        # Same timestamp
        older_or_equal_data = {**initial_data, "updated_at": now, "isRedeemed": True}

        sync_map = {"transaction": {"idMap": {193: 193}}}

        mock_storage = type("MockStorage", (), {})()

        # When
        was_merged = entity.merge_existing(mock_storage, None, older_or_equal_data, sync_map, None)

        # Then
        assert was_merged is False
        assert entity.is_redeemed is False
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'authentication value_verification verification key_change' but PY verifies 'verification'
  - [HIGH] Python test is missing verifications: entity.spendable, unchanged_record.length
  - [HIGH] Python test is missing operations: entity.mergeExisting

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 2, PY has 1

**Suggestions:**
  - Align test intent: ensure PY test verifies 'authentication value_verification verification key_change'
  - Add verifications for: entity.spendable, unchanged_record.length
  - Add operations: entity.mergeExisting

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: authentication value_verification verification key_change
  • Python: verification

Critical Issues (3):
  • [HIGH] Test intent differs: TS verifies 'authentication value_verification verification key_change' but PY verifies 'verification'
  • [HIGH] Python test is missing verifications: entity.spendable, unchanged_record.length
  • [HIGH] Python test is missing operations: entity.mergeExisting

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 2, PY has 1

---

## Test 254: Output entity getters and setters **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/OutputTests.test.ts

```typescript
  test('Output entity getters and setters', async () => {
    const now = new Date()

    // Initial test data
    const initialData: TableOutput = {
      outputId: 701,
      created_at: now,
      updated_at: now,
      userId: 1,
      transactionId: 103,
      basketId: 1,
      spendable: true,
      change: false,
      satoshis: 1000,
      outputDescription: 'Initial Output',
      vout: 50,
      type: 'p2pkh',
      providedBy: 'you',
      purpose: 'initial',
      txid: 'txid201',
      spendingDescription: 'Initial Spending',
      derivationPrefix: 'm/44',
      derivationSuffix: '/0/0',
      senderIdentityKey: 'key201',
      customInstructions: 'none',
      lockingScript: [1, 2, 3],
      scriptLength: 10,
      scriptOffset: 0,
      spentBy: 200
    }

    // Create the Output entity
    const entity = new EntityOutput(initialData)

    // Validate getters
    expect(entity.outputId).toBe(initialData.outputId)
    expect(entity.created_at).toEqual(initialData.created_at)
    expect(entity.updated_at).toEqual(initialData.updated_at)
    expect(entity.userId).toBe(initialData.userId)
    expect(entity.transactionId).toBe(initialData.transactionId)
    expect(entity.basketId).toBe(initialData.basketId)
    expect(entity.spentBy).toBe(initialData.spentBy)
    expect(entity.vout).toBe(initialData.vout)
    expect(entity.satoshis).toBe(initialData.satoshis)
    expect(entity.outputDescription).toBe(initialData.outputDescription)
    expect(entity.spendable).toBe(initialData.spendable)
    expect(entity.change).toBe(initialData.change)
    expect(entity.txid).toBe(initialData.txid)
    expect(entity.type).toBe(initialData.type)
    expect(entity.providedBy).toBe(initialData.providedBy)
    expect(entity.purpose).toBe(initialData.purpose)
    expect(entity.spendingDescription).toBe(initialData.spendingDescription)
    expect(entity.derivationPrefix).toBe(initialData.derivationPrefix)
    expect(entity.derivationSuffix).toBe(initialData.derivationSuffix)
    expect(entity.senderIdentityKey).toBe(initialData.senderIdentityKey)
    expect(entity.customInstructions).toBe(initialData.customInstructions)
    expect(entity.lockingScript).toEqual(initialData.lockingScript)
    expect(entity.scriptLength).toBe(initialData.scriptLength)
    expect(entity.scriptOffset).toBe(initialData.scriptOffset)

    // Validate setters
    entity.outputId = 800
    entity.created_at = new Date('2024-01-01')
    entity.updated_at = new Date('2024-01-02')
    entity.userId = 2
    entity.transactionId = 104
    entity.basketId = 2
    entity.spentBy = 300
    entity.vout = 60
    entity.satoshis = 2000
    entity.outputDescription = 'Updated Output'
    entity.spendable = false
    entity.change = true
    entity.txid = 'txid202'
    entity.type = 'p2sh'
    entity.providedBy = 'storage'
    entity.purpose = 'updated'
    entity.spendingDescription = 'Updated Spending'
    entity.derivationPrefix = 'm/45'
    entity.derivationSuffix = '/1/0'
    entity.senderIdentityKey = 'key202'
    entity.customInstructions = 'new instructions'
    entity.lockingScript = [4, 5, 6]
    entity.scriptLength = 15
    entity.scriptOffset = 5

    expect(entity.outputId).toBe(800)
    expect(entity.created_at).toEqual(new Date('2024-01-01'))
    expect(entity.updated_at).toEqual(new Date('2024-01-02'))
    expect(entity.userId).toBe(2)
    expect(entity.transactionId).toBe(104)
    expect(entity.basketId).toBe(2)
    expect(entity.spentBy).toBe(300)
    expect(entity.vout).toBe(60)
    expect(entity.satoshis).toBe(2000)
    expect(entity.outputDescription).toBe('Updated Output')
    expect(entity.spendable).toBe(false)
    expect(entity.change).toBe(true)
    expect(entity.txid).toBe('txid202')
    expect(entity.type).toBe('p2sh')
    expect(entity.providedBy).toBe('storage')
    expect(entity.purpose).toBe('updated')
    expect(entity.spendingDescription).toBe('Updated Spending')
    expect(entity.derivationPrefix).toBe('m/45')
    expect(entity.derivationSuffix).toBe('/1/0')
    expect(entity.senderIdentityKey).toBe('key202')
    expect(entity.customInstructions).toBe('new instructions')
    expect(entity.lockingScript).toEqual([4, 5, 6])
    expect(entity.scriptLength).toBe(15)
    expect(entity.scriptOffset).toBe(5)

    // Validate `id` setter and getter
    entity.id = 900
    expect(entity.id).toBe(900)
    expect(entity.outputId).toBe(900)

    // Validate `entityName` and `entityTable`
    expect(entity.entityName).toBe('output')
    expect(entity.entityTable).toBe('outputs')
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_output.py

```python
    def test_output_entity_getters_and_setters(self) -> None:
        """Given: Output instance
           When: Set and get all properties
           Then: Getters and setters work correctly

        Reference: src/storage/schema/entities/__tests/OutputTests.test.ts
                  test('Output entity getters and setters')
        """
        # Given

        now = datetime.now()
        initial_data = {
            "outputId": 701,
            "created_at": now,
            "updated_at": now,
            "userId": 1,
            "transactionId": 103,
            "basketId": 1,
            "spendable": True,
            "change": False,
            "satoshis": 1000,
            "outputDescription": "Initial Output",
            "vout": 50,
            "type": "p2pkh",
            "providedBy": "you",
            "purpose": "initial",
            "txid": "txid201",
            "spendingDescription": "Initial Spending",
            "derivationPrefix": "m/44",
            "derivationSuffix": "/0/0",
            "senderIdentityKey": "key201",
            "customInstructions": "none",
            "lockingScript": [1, 2, 3],
            "scriptLength": 10,
            "scriptOffset": 0,
            "spentBy": 200,
        }

        entity = Output(initial_data)

        # Validate getters
        assert entity.output_id == 701
        assert entity.user_id == 1
        assert entity.transaction_id == 103
        assert entity.basket_id == 1
        assert entity.spent_by == 200
        assert entity.vout == 50
        assert entity.satoshis == 1000
        assert entity.spendable is True
        assert entity.change is False

        # Validate setters
        entity.output_id = 800
        entity.created_at = datetime(2024, 1, 1)
        entity.updated_at = datetime(2024, 1, 2)
        entity.user_id = 2
        entity.transaction_id = 104
        entity.basket_id = 2
        entity.spent_by = 300
        entity.vout = 60
        entity.satoshis = 2000
        entity.output_description = "Updated Output"
        entity.spendable = False
        entity.change = True
        entity.txid = "txid202"
        entity.type = "p2sh"
        entity.provided_by = "storage"
        entity.purpose = "updated"
        entity.spending_description = "Updated Spending"
        entity.derivation_prefix = "m/45"
        entity.derivation_suffix = "/1/0"
        entity.sender_identity_key = "key202"
        entity.custom_instructions = "new instructions"
        entity.locking_script = [4, 5, 6]
        entity.script_length = 15
        entity.script_offset = 5

        assert entity.output_id == 800
        assert entity.satoshis == 2000
        assert entity.spendable is False

        # Validate id setter and getter
        entity.id = 900
        assert entity.id == 900
        assert entity.output_id == 900

        # Validate entity_name and entity_table
        assert entity.entity_name == "output"
        assert entity.entity_table == "outputs"
```

### AI Analysis Results

**Similarity Score**: 60.48%
  - Structural: 0.00%
  - Semantic: 60.95%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: entity.vout, entity.basketId, entity.entityName, entity.spentBy, entity.outputDescription, entity.derivationPrefix, entity.id, entity.entityTable, entity.transactionId, entity.userId, entity.spendingDescription, entity.change, entity.spendable, entity.satoshis, entity.providedBy, entity.lockingScript, entity.purpose, entity.customInstructions, entity.senderIdentityKey, entity.derivationSuffix, entity.updated_at, entity.scriptOffset, entity.outputId, entity.type, entity.txid, entity.scriptLength, entity.created_at

**Differences:**
  - Verification count: TS has 52, PY has 16

**Suggestions:**
  - Add verifications for: entity.vout, entity.basketId, entity.entityName

**Explanation:**

Overall Similarity: 60.5%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 61.0% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: authentication value_verification verification key_change
  • Python: authentication verification key_change

Critical Issues (1):
  • [HIGH] Python test is missing verifications: entity.vout, entity.basketId, entity.entityName, entity.spentBy, entity.outputDescription, entity.derivationPrefix, entity.id, entity.entityTable, entity.transactionId, entity.userId, entity.spendingDescription, entity.change, entity.spendable, entity.satoshis, entity.providedBy, entity.lockingScript, entity.purpose, entity.customInstructions, entity.senderIdentityKey, entity.derivationSuffix, entity.updated_at, entity.scriptOffset, entity.outputId, entity.type, entity.txid, entity.scriptLength, entity.created_at

Key Differences:
  • Verification count: TS has 52, PY has 16

---

## Test 255: 0_apiNotify_getter_and_setter **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxReqTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx_req.py`

---

## Test 256: 10_mergeHistory **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxReqTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx_req.py`

---

## Test 257: 12_isTerminalStatus_with_real_data **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxReqTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx_req.py`

---

## Test 258: 13_mergeExisting_real_data **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxReqTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx_req.py`

---

## Test 259: 1_getHistorySummary **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxReqTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx_req.py`

---

## Test 260: 2_parseHistoryNote **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxReqTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx_req.py`

---

## Test 261: 3_updateStorage **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxReqTests.test.ts

```typescript
  test('3_updateStorage', async () => {
    const ctx = ctxs[0]
    const provenTxReq = new EntityProvenTxReq({
      provenTxReqId: 0,
      created_at: new Date(),
      updated_at: new Date(),
      txid: 'test-txid',
      rawTx: [1, 2, 3],
      history: '{}',
      notify: '{}',
      attempts: 0,
      status: 'unknown',
      notified: false
    })

    await provenTxReq.updateStorage(ctx.activeStorage)

    const fetchedProvenTxReqs = await ctx.activeStorage.findProvenTxReqs({
      partial: { txid: 'test-txid' }
    })
    expect(fetchedProvenTxReqs.length).toBe(1)
    expect(fetchedProvenTxReqs[0].txid).toBe('test-txid')
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_proven_tx_req.py

```python
    def test_updatestorage(self) -> None:
        """Given: ProvenTxReq instance
           When: Call update_storage
           Then: Updates storage and can fetch back the record

        Reference: src/storage/schema/entities/__tests/ProvenTxReqTests.test.ts
                  test('3_updateStorage')
        """
        # Given

        proven_tx_req = ProvenTxReq(
            {
                "provenTxReqId": 0,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "txid": "test-txid",
                "rawTx": [1, 2, 3],
                "history": "{}",
                "notify": "{}",
                "attempts": 0,
                "status": "unknown",
                "notified": False,
            }
        )

        # Mock storage
        stored_records: list[dict[str, Any]] = []

        def mock_update_proven_tx_req(_id: int, data: dict[str, Any]) -> None:
            stored_records.append(data)

        def mock_find_proven_tx_reqs(query: dict[str, Any]) -> list[dict[str, Any]]:
            return [r for r in stored_records if r.get("txid") == query["partial"]["txid"]]

        mock_storage = type(
            "MockStorage",
            (),
            {
                "update_proven_tx_req": staticmethod(mock_update_proven_tx_req),
                "find_proven_tx_reqs": staticmethod(mock_find_proven_tx_reqs),
            },
        )()

        # When
        proven_tx_req.update_storage(mock_storage)

        # Then
        fetched = mock_storage.find_proven_tx_reqs({"partial": {"txid": "test-txid"}})
        assert len(fetched) == 1
        assert fetched[0]["txid"] == "test-txid"
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: fetched_proven_tx_reqs.length
  - [HIGH] Python test is missing operations: proven_tx_req.updateStorage

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: fetched_proven_tx_reqs.length
  - Add operations: proven_tx_req.updateStorage

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: fetched_proven_tx_reqs.length
  • [HIGH] Python test is missing operations: proven_tx_req.updateStorage

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 1, PY has 0

---

## Test 262: 4_insertOrMerge **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxReqTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx_req.py`

---

## Test 263: 5_equals_identifies_matching_entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxReqTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx_req.py`

---

## Test 264: 6_equals_identifies_non_matching_entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxReqTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output.py`

---

## Test 265: 7_mergeNotifyTransactionIds **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxReqTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx_req.py`

---

## Test 266: 8_getters_and_setters **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxReqTests.test.ts

```typescript
  test('8_getters_and_setters', () => {
    const currentTime = new Date()
    const provenTxReq = new EntityProvenTxReq({
      provenTxReqId: 123,
      created_at: currentTime,
      updated_at: currentTime,
      txid: 'test-txid',
      inputBEEF: [1, 2, 3],
      rawTx: [4, 5, 6],
      attempts: 3,
      provenTxId: 456,
      notified: true,
      batch: 'test-batch',
      history: '{}', // Valid JSON
      notify: '{}', // Valid JSON
      status: 'completed'
    })

    // Verify getters
    expect(provenTxReq.provenTxReqId).toBe(123)
    expect(provenTxReq.created_at).toBe(currentTime)
    expect(provenTxReq.updated_at).toBe(currentTime)
    expect(provenTxReq.txid).toBe('test-txid')
    expect(provenTxReq.inputBEEF).toEqual([1, 2, 3])
    expect(provenTxReq.rawTx).toEqual([4, 5, 6])
    expect(provenTxReq.attempts).toBe(3)
    expect(provenTxReq.provenTxId).toBe(456)
    expect(provenTxReq.notified).toBe(true)
    expect(provenTxReq.batch).toBe('test-batch')
    expect(provenTxReq.id).toBe(123)
    expect(provenTxReq.entityName).toBe('provenTxReq')
    expect(provenTxReq.entityTable).toBe('proven_tx_reqs')

    // Verify setters
    const newTime = new Date()
    provenTxReq.provenTxReqId = 789
    provenTxReq.created_at = newTime
    provenTxReq.updated_at = newTime
    provenTxReq.txid = 'new-txid'
    provenTxReq.inputBEEF = [7, 8, 9]
    provenTxReq.rawTx = [10, 11, 12]
    provenTxReq.attempts = 5
    provenTxReq.provenTxId = 789
    provenTxReq.notified = false
    provenTxReq.batch = 'new-batch'
    provenTxReq.id = 789

    // Verify that setters updated the api object correctly
    expect(provenTxReq.api.provenTxReqId).toBe(789)
    expect(provenTxReq.api.created_at).toBe(newTime)
    expect(provenTxReq.api.updated_at).toBe(newTime)
    expect(provenTxReq.api.txid).toBe('new-txid')
    expect(provenTxReq.api.inputBEEF).toEqual([7, 8, 9])
    expect(provenTxReq.api.rawTx).toEqual([10, 11, 12])
    expect(provenTxReq.api.attempts).toBe(5)
    expect(provenTxReq.api.provenTxId).toBe(789)
    expect(provenTxReq.api.notified).toBe(false)
    expect(provenTxReq.api.batch).toBe('new-batch')
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_proven_tx_req.py

```python
    def test_getters_and_setters(self) -> None:
        """Given: ProvenTxReq instance
           When: Set and get all properties
           Then: Getters and setters work correctly

        Reference: src/storage/schema/entities/__tests/ProvenTxReqTests.test.ts
                  test('8_getters_and_setters')
        """
        # Given

        now = datetime.now()
        proven_tx_req = ProvenTxReq(
            {
                "provenTxReqId": 1,
                "created_at": now,
                "updated_at": now,
                "txid": "test-txid",
                "rawTx": [1, 2, 3],
                "history": "{}",
                "notify": "{}",
                "attempts": 5,
                "status": "unknown",
                "notified": False,
            }
        )

        # Validate getters
        assert proven_tx_req.proven_tx_req_id == 1
        assert proven_tx_req.txid == "test-txid"
        assert proven_tx_req.attempts == 5
        assert proven_tx_req.status == "unknown"
        assert proven_tx_req.notified is False

        # Validate setters
        proven_tx_req.proven_tx_req_id = 2
        proven_tx_req.txid = "new-txid"
        proven_tx_req.attempts = 10
        proven_tx_req.status = "completed"
        proven_tx_req.notified = True

        assert proven_tx_req.proven_tx_req_id == 2
        assert proven_tx_req.txid == "new-txid"
        assert proven_tx_req.attempts == 10
        assert proven_tx_req.status == "completed"
        assert proven_tx_req.notified is True

        # Validate entity metadata
        assert proven_tx_req.entity_name == "provenTxReq"
        assert proven_tx_req.entity_table == "proven_tx_reqs"
```

### AI Analysis Results

**Similarity Score**: 57.18%
  - Structural: 0.00%
  - Semantic: 54.36%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: proven_tx_req.attempts, proven_tx_req.entityTable, proven_tx_req.provenTxReqId, proven_tx_req.rawTx, proven_tx_req.batch, proven_tx_req.notified, proven_tx_req.inputBEEF, proven_tx_req.created_at, proven_tx_req.entityName, proven_tx_req.provenTxId, proven_tx_req.updated_at, proven_tx_req.id, proven_tx_req.txid

**Differences:**
  - Verification count: TS has 13, PY has 12

**Suggestions:**
  - Add verifications for: proven_tx_req.attempts, proven_tx_req.entityTable, proven_tx_req.provenTxReqId

**Explanation:**

Overall Similarity: 57.2%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 54.4% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: proven_tx_req.attempts, proven_tx_req.entityTable, proven_tx_req.provenTxReqId, proven_tx_req.rawTx, proven_tx_req.batch, proven_tx_req.notified, proven_tx_req.inputBEEF, proven_tx_req.created_at, proven_tx_req.entityName, proven_tx_req.provenTxId, proven_tx_req.updated_at, proven_tx_req.id, proven_tx_req.txid

Key Differences:
  • Verification count: TS has 13, PY has 12

---

## Test 267: 9_parseHistoryNote **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxReqTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx_req.py`

---

## Test 268: 0_fromTxid: valid txid with rawTx and Merkle proof (real database) **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxTests.test.ts

```typescript
  test('0_fromTxid: valid txid with rawTx and Merkle proof (real database)', async () => {
    const ctx = ctxs[0]
    const txid = '2795b293c698b2244147aaba745db887a632d21990c474df46d842ec3e52f122' // Using a valid txid from the table

    // Fetch the rawTx and Merkle proof data directly from the database
    const provenTxRecord = await ctx.activeStorage.findProvenTxs({
      partial: { txid }
    })
    expect(provenTxRecord.length).toBeGreaterThan(0) // Ensure the record exists in the database

    const rawTx = provenTxRecord[0]?.rawTx
    const height = provenTxRecord[0]?.height
    const blockHash = provenTxRecord[0]?.blockHash
    const merkleRoot = provenTxRecord[0]?.merkleRoot
    const merklePathBinary = provenTxRecord[0]?.merklePath || []

    const services: sdk.WalletServices = {
      chain: 'test',

      hashOutputScript: (script: string): string => {
        const hash = bsv.Utils.toHex(sha256Hash(bsv.Utils.toArray(script, 'hex')))
        return hash
      },

      getRawTx: async (requestedTxid: string) => {
        if (requestedTxid === txid) {
          return { txid: requestedTxid, rawTx }
        }
        throw new Error('Unexpected txid')
      },

      getMerklePath: async (requestedTxid: string) => {
        if (requestedTxid === txid) {
          return {
            merklePath: {
              path: [[{ hash: txid, offset: 0 }]],
              blockHeight: height,
              toBinary: () => merklePathBinary,
              computeRoot: () => merkleRoot,
              verifyProof: () => true,
              toHex: () => Buffer.from(merklePathBinary).toString('hex'),
              indexOf: () => 0,
              findOrComputeLeaf: () => ({ hash: txid, offset: 0 }),
              verify: () => true,
              combine: () => ({}) as bsv.MerklePath,
              trim: () => ({}) as bsv.MerklePath
            } as unknown as bsv.MerklePath,
            header: {
              version: 1,
              previousHash: 'prev-hash',
              merkleRoot: merkleRoot,
              time: 1610000000,
              bits: 123456,
              nonce: 78910,
              height: height,
              hash: blockHash
            },
            name: 'mock-service'
          }
        }
        throw new Error('Unexpected txid')
      },

      getChainTracker: () =>
        Promise.resolve({
          isValidRootForHeight: async (root: string, height: number) => true,
          currentHeight: async () => height
        }),

      getHeaderForHeight: async () => Promise.resolve([1, 2, 3, 4]),
      getHeight: async () => height,
      getBsvExchangeRate: async () => 0,
      getFiatExchangeRate: async () => 1,
      postBeef: async () => [],

      getStatusForTxids: async () => ({
        name: 'mock-service',
        status: 'success',
        results: []
      }),

      isUtxo: async () => true,

      getUtxoStatus: async () => ({
        name: 'mock-service',
        status: 'success',
        isUtxo: true,
        details: []
      }),

      getScriptHashHistory: async () => ({
        name: 'mock-service',
        status: 'success',
        history: []
      }),

      hashToHeader: async () => ({
        version: 1,
        previousHash: 'prev-hash',
        merkleRoot: merkleRoot,
        time: 1610000000,
        bits: 123456,
        nonce: 78910,
        height: height,
        hash: blockHash
      }),
      nLockTimeIsFinal: async () => true,

      getBeefForTxid: async () => new bsv.Beef(),

      getServicesCallHistory: () => ({
        version: 1,
        getMerklePath: { serviceName: '', historyByProvider: {} },
        getRawTx: { serviceName: '', historyByProvider: {} },
        postBeef: { serviceName: '', historyByProvider: {} },
        getStatusForTxids: { serviceName: '', historyByProvider: {} },
        getUtxoStatus: { serviceName: '', historyByProvider: {} },
        getScriptHashHistory: { serviceName: '', historyByProvider: {} },
        updateFiatExchangeRates: { serviceName: '', historyByProvider: {} }
      })
    }

    // Call the method under test
    const result = await EntityProvenTx.fromTxid(txid, services)

    // Validate the ProvenTx result
    expect(result.proven).toBeDefined()
    expect(result.proven!.txid).toBe(txid)

    // Validate Merkle proof details
    expect(result.proven!.height).toBe(height)
    expect(Buffer.from(result.proven!.merklePath).toString('hex')).toEqual(
      Buffer.from(merklePathBinary).toString('hex')
    )
    expect(result.proven!.blockHash).toBe(blockHash)
    expect(result.proven!.merkleRoot).toBe(merkleRoot)
    expect(result.rawTx).toEqual(rawTx)
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_proven_tx.py

```python
    def test_fromtxid_valid_txid_with_rawtx_and_merkle_proof_real_database(self) -> None:
        """Given: Valid txid with rawTx and Merkle proof in database
           When: Call from_txid with services
           Then: Returns ProvenTx with valid data

        Reference: src/storage/schema/entities/__tests/ProvenTxTests.test.ts
                  test('0_fromTxid: valid txid with rawTx and Merkle proof (real database)')
        """
        # Given

        txid = "2795b293c698b2244147aaba745db887a632d21990c474df46d842ec3e52f122"
        height = 123
        block_hash = "mock-block-hash"
        merkle_root = "mock-merkle-root"
        merkle_path_binary = [0x01, 0x02, 0x03]
        raw_tx = [0x04, 0x05, 0x06]

        # Mock services
        def mock_get_raw_tx(requested_txid: str) -> dict[str, Any]:
            if requested_txid == txid:
                return {"txid": requested_txid, "rawTx": raw_tx}
            raise Exception("Unexpected txid")

        def mock_get_merkle_path(requested_txid: str) -> dict[str, Any]:
            if requested_txid == txid:
                return {
                    "merklePath": {
                        "path": [[{"hash": txid, "offset": 0}]],
                        "blockHeight": height,
                        "toBinary": lambda: merkle_path_binary,
                    },
                    "header": {"height": height, "hash": block_hash, "merkleRoot": merkle_root},
                }
            raise Exception("Unexpected txid")

        mock_services = type(
            "MockServices",
            (),
            {
                "get_raw_tx": staticmethod(mock_get_raw_tx),
                "get_merkle_path": staticmethod(mock_get_merkle_path),
            },
        )()

        # When
        result = ProvenTx.from_txid(txid, mock_services)

        # Then
        assert result["proven"] is not None
        assert result["proven"].txid == txid
        assert result["proven"].height == height
        assert result["proven"].block_hash == block_hash
        assert result["proven"].merkle_root == merkle_root
        assert result["rawTx"] == raw_tx
```

### AI Analysis Results

**Similarity Score**: 22.00%
  - Structural: 0.00%
  - Semantic: 44.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: result.rawTx, proven_tx_record.length, result.proven
  - [HIGH] Python test is missing operations: entity_proven_tx.fromTxid

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 3, PY has 6

**Suggestions:**
  - Add verifications for: result.rawTx, proven_tx_record.length, result.proven
  - Add operations: entity_proven_tx.fromTxid

**Explanation:**

Overall Similarity: 22.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 44.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: authentication value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: result.rawTx, proven_tx_record.length, result.proven
  • [HIGH] Python test is missing operations: entity_proven_tx.fromTxid

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 3, PY has 6

---

## Test 269: 10_mergeExisting: always returns false **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx.py`

---

## Test 270: 1_fromTxid: txid with no rawTx available **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxTests.test.ts

```typescript
  test('1_fromTxid: txid with no rawTx available', async () => {
    const ctx = ctxs[0]
    const txid = 'missing-txid'

    const services: sdk.WalletServices = ctx.services

    // Call the method under test
    const result = await EntityProvenTx.fromTxid(txid, services)

    // Validate that ProvenTx could not be created
    expect(result.proven).toBeUndefined()
    expect(result.rawTx).toBeUndefined()
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_proven_tx.py

```python
    def test_fromtxid_txid_with_no_rawtx_available(self) -> None:
        """Given: Txid with no rawTx available
           When: Call from_txid
           Then: Returns result with undefined proven and rawTx

        Reference: src/storage/schema/entities/__tests/ProvenTxTests.test.ts
                  test('1_fromTxid: txid with no rawTx available')
        """
        # Given

        txid = "missing-txid"

        # Mock services that return nothing
        def mock_get_raw_tx(requested_txid: str) -> None:
            return None

        mock_services = type("MockServices", (), {"get_raw_tx": mock_get_raw_tx})()

        # When
        result = ProvenTx.from_txid(txid, mock_services)

        # Then
        assert result["proven"] is None
        assert result["rawTx"] is None
```

### AI Analysis Results

**Similarity Score**: 28.33%
  - Structural: 0.00%
  - Semantic: 56.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: result.rawTx, result.proven
  - [HIGH] Python test is missing operations: entity_proven_tx.fromTxid

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: result.rawTx, result.proven
  - Add operations: entity_proven_tx.fromTxid

**Explanation:**

Overall Similarity: 28.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 56.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: result.rawTx, result.proven
  • [HIGH] Python test is missing operations: entity_proven_tx.fromTxid

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 271: 2_fromTxid: txid with no Merkle proof available **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxTests.test.ts

```typescript
  test('2_fromTxid: txid with no Merkle proof available', async () => {
    const ctx = ctxs[0]
    const txid = 'no-merkle-proof-txid'
    const services: sdk.WalletServices = ctx.services

    // Verify the rawTx and Merkle proof
    const rawTx = await services.getRawTx(txid)
    const merkleProof = await services.getMerklePath(txid)

    // Call the method under test
    const result = await EntityProvenTx.fromTxid(txid, services)

    // Validate the ProvenTx result
    expect(result.proven).toBeUndefined()
    expect(result.rawTx).toEqual(rawTx.rawTx)
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_proven_tx.py

```python
    def test_fromtxid_txid_with_no_merkle_proof_available(self) -> None:
        """Given: Txid with rawTx but no Merkle proof
           When: Call from_txid
           Then: Returns result with rawTx but undefined proven

        Reference: src/storage/schema/entities/__tests/ProvenTxTests.test.ts
                  test('2_fromTxid: txid with no Merkle proof available')
        """
        # Given

        txid = "no-merkle-proof-txid"
        raw_tx = [0x01, 0x02, 0x03]

        # Mock services
        def mock_get_raw_tx(requested_txid: str) -> dict[str, Any]:
            return {"txid": requested_txid, "rawTx": raw_tx}

        def mock_get_merkle_path(requested_txid: str) -> None:
            return None

        mock_services = type(
            "MockServices",
            (),
            {
                "get_raw_tx": staticmethod(mock_get_raw_tx),
                "get_merkle_path": staticmethod(mock_get_merkle_path),
            },
        )()

        # When
        result = ProvenTx.from_txid(txid, mock_services)

        # Then
        assert result["proven"] is None
        assert result["rawTx"] == raw_tx
```

### AI Analysis Results

**Similarity Score**: 28.33%
  - Structural: 0.00%
  - Semantic: 56.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: result.rawTx, result.proven
  - [HIGH] Python test is missing operations: services.getMerklePath, entity_proven_tx.fromTxid, services.getRawTx

**Differences:**
  - Operation count: TS has 3, PY has 0

**Suggestions:**
  - Add verifications for: result.rawTx, result.proven
  - Add operations: services.getMerklePath, entity_proven_tx.fromTxid, services.getRawTx

**Explanation:**

Overall Similarity: 28.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 56.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: result.rawTx, result.proven
  • [HIGH] Python test is missing operations: services.getMerklePath, entity_proven_tx.fromTxid, services.getRawTx

Key Differences:
  • Operation count: TS has 3, PY has 0

---

## Test 272: 3_ProvenTx getters and setters **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxTests.test.ts

```typescript
  test('3_ProvenTx getters and setters', () => {
    // Mock data to initialize the ProvenTx entity
    const mockData = {
      provenTxId: 1,
      created_at: new Date('2025-01-01T00:00:00Z'),
      updated_at: new Date('2025-01-02T00:00:00Z'),
      txid: '2795b293c698b2244147aaba745db887a632d21990c474df46d842ec3e52f122',
      height: 123,
      index: 0,
      merklePath: [0x04, 0x05, 0x06],
      rawTx: [0x01, 0x02, 0x03],
      blockHash: 'mock-block-hash',
      merkleRoot: 'mock-merkle-root'
    }

    // Initialize the ProvenTx entity with mock data
    const provenTx = new EntityProvenTx(mockData)

    // Validate getters
    expect(provenTx.provenTxId).toBe(mockData.provenTxId)
    expect(provenTx.created_at).toEqual(mockData.created_at)
    expect(provenTx.updated_at).toEqual(mockData.updated_at)
    expect(provenTx.txid).toBe(mockData.txid)
    expect(provenTx.height).toBe(mockData.height)
    expect(provenTx.index).toBe(mockData.index)
    expect(provenTx.merklePath).toEqual(mockData.merklePath)
    expect(provenTx.rawTx).toEqual(mockData.rawTx)
    expect(provenTx.blockHash).toBe(mockData.blockHash)
    expect(provenTx.merkleRoot).toBe(mockData.merkleRoot)

    // Validate setters
    provenTx.provenTxId = 2
    provenTx.created_at = new Date('2025-02-01T00:00:00Z')
    provenTx.updated_at = new Date('2025-02-02T00:00:00Z')
    provenTx.txid = 'a3b2f0935c7b5bb7a841a09e535c13be86f4df0e7a91cebdc33812bfcc0eb9d7'
    provenTx.height = 456
    provenTx.index = 1
    provenTx.merklePath = [0x07, 0x08, 0x09]
    provenTx.rawTx = [0x0a, 0x0b, 0x0c]
    provenTx.blockHash = 'new-block-hash'
    provenTx.merkleRoot = 'new-merkle-root'

    // Validate updated values
    expect(provenTx.provenTxId).toBe(2)
    expect(provenTx.created_at).toEqual(new Date('2025-02-01T00:00:00Z'))
    expect(provenTx.updated_at).toEqual(new Date('2025-02-02T00:00:00Z'))
    expect(provenTx.txid).toBe('a3b2f0935c7b5bb7a841a09e535c13be86f4df0e7a91cebdc33812bfcc0eb9d7')
    expect(provenTx.height).toBe(456)
    expect(provenTx.index).toBe(1)
    expect(provenTx.merklePath).toEqual([0x07, 0x08, 0x09])
    expect(provenTx.rawTx).toEqual([0x0a, 0x0b, 0x0c])
    expect(provenTx.blockHash).toBe('new-block-hash')
    expect(provenTx.merkleRoot).toBe('new-merkle-root')

    // Validate overridden methods
    expect(provenTx.id).toBe(2)
    expect(provenTx.entityName).toBe('provenTx')
    expect(provenTx.entityTable).toBe('proven_txs')

    // Update id via overridden setter
    provenTx.id = 3
    expect(provenTx.provenTxId).toBe(3)
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_proven_tx.py

```python
    def test_proventx_getters_and_setters(self) -> None:
        """Given: ProvenTx instance with mock data
           When: Set and get all properties
           Then: Getters and setters work correctly

        Reference: src/storage/schema/entities/__tests/ProvenTxTests.test.ts
                  test('3_ProvenTx getters and setters')
        """
        # Given

        mock_data = {
            "provenTxId": 1,
            "created_at": datetime(2025, 1, 1),
            "updated_at": datetime(2025, 1, 2),
            "txid": "2795b293c698b2244147aaba745db887a632d21990c474df46d842ec3e52f122",
            "height": 123,
            "index": 0,
            "merklePath": [0x04, 0x05, 0x06],
            "rawTx": [0x01, 0x02, 0x03],
            "blockHash": "mock-block-hash",
            "merkleRoot": "mock-merkle-root",
        }

        proven_tx = ProvenTx(mock_data)

        # Validate getters
        assert proven_tx.proven_tx_id == 1
        assert proven_tx.txid == "2795b293c698b2244147aaba745db887a632d21990c474df46d842ec3e52f122"
        assert proven_tx.height == 123
        assert proven_tx.index == 0
        assert proven_tx.merkle_path == [0x04, 0x05, 0x06]
        assert proven_tx.raw_tx == [0x01, 0x02, 0x03]
        assert proven_tx.block_hash == "mock-block-hash"
        assert proven_tx.merkle_root == "mock-merkle-root"

        # Validate setters
        proven_tx.proven_tx_id = 2
        proven_tx.created_at = datetime(2025, 2, 1)
        proven_tx.updated_at = datetime(2025, 2, 2)
        proven_tx.txid = "a3b2f0935c7b5bb7a841a09e535c13be86f4df0e7a91cebdc33812bfcc0eb9d7"
        proven_tx.height = 456
        proven_tx.index = 1
        proven_tx.merkle_path = [0x07, 0x08, 0x09]
        proven_tx.raw_tx = [0x0A, 0x0B, 0x0C]
        proven_tx.block_hash = "new-block-hash"
        proven_tx.merkle_root = "new-merkle-root"

        # Validate updated values
        assert proven_tx.proven_tx_id == 2
        assert proven_tx.txid == "a3b2f0935c7b5bb7a841a09e535c13be86f4df0e7a91cebdc33812bfcc0eb9d7"
        assert proven_tx.height == 456

        # Validate overridden methods
        assert proven_tx.id == 2
        assert proven_tx.entity_name == "provenTx"
        assert proven_tx.entity_table == "proven_txs"

        # Update id via overridden setter
        proven_tx.id = 3
        assert proven_tx.proven_tx_id == 3
```

### AI Analysis Results

**Similarity Score**: 68.72%
  - Structural: 0.00%
  - Semantic: 77.44%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: proven_tx.entityName, proven_tx.updated_at, proven_tx.provenTxId, proven_tx.merkleRoot, proven_tx.blockHash, proven_tx.height, proven_tx.entityTable, proven_tx.index, proven_tx.rawTx, proven_tx.id, proven_tx.txid, proven_tx.merklePath, proven_tx.created_at

**Differences:**
  - Verification count: TS has 24, PY has 15

**Suggestions:**
  - Add verifications for: proven_tx.entityName, proven_tx.updated_at, proven_tx.provenTxId

**Explanation:**

Overall Similarity: 68.7%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 77.4% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: proven_tx.entityName, proven_tx.updated_at, proven_tx.provenTxId, proven_tx.merkleRoot, proven_tx.blockHash, proven_tx.height, proven_tx.entityTable, proven_tx.index, proven_tx.rawTx, proven_tx.id, proven_tx.txid, proven_tx.merklePath, proven_tx.created_at

Key Differences:
  • Verification count: TS has 24, PY has 15

---

## Test 273: 4_equals: identifies matching ProvenTx entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx.py`

---

## Test 274: 5_equals: identifies non-matching txid **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx.py`

---

## Test 275: 6_equals: identifies non-matching height **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx.py`

---

## Test 276: 7_equals: identifies non-matching merklePath **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx.py`

---

## Test 277: 8_equals: identifies non-matching syncMap **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx.py`

---

## Test 278: 9_equals: provenTxId mismatch without syncMap **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/ProvenTxTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx.py`

---

## Test 279: 11_mergeExisting_always_returns_false **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/SyncStateTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx.py`

---

## Test 280: 7_getters_and_setters **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/SyncStateTests.test.ts

```typescript
  test('7_getters_and_setters', () => {
    const syncState = new EntitySyncState()

    // Test created_at and updated_at
    const now = new Date()
    syncState.created_at = now
    syncState.updated_at = now
    expect(syncState.created_at).toBe(now)
    expect(syncState.updated_at).toBe(now)

    // Test userId
    syncState.userId = 123
    expect(syncState.userId).toBe(123)

    // Test storageIdentityKey
    syncState.storageIdentityKey = 'testStorageIdentityKey'
    expect(syncState.storageIdentityKey).toBe('testStorageIdentityKey')

    // Test storageName
    syncState.storageName = 'testStorageName'
    expect(syncState.storageName).toBe('testStorageName')

    // Test init
    syncState.init = true
    expect(syncState.init).toBe(true)

    // Test refNum
    syncState.refNum = 'testRefNum'
    expect(syncState.refNum).toBe('testRefNum')

    // Test status
    syncState.status = 'success'
    expect(syncState.status).toBe('success')

    // Test when
    const whenDate = new Date()
    syncState.when = whenDate
    expect(syncState.when).toBe(whenDate)

    // Test satoshis
    syncState.satoshis = 1000
    expect(syncState.satoshis).toBe(1000)
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_proven_tx_req.py

```python
    def test_getters_and_setters(self) -> None:
        """Given: ProvenTxReq instance
           When: Set and get all properties
           Then: Getters and setters work correctly

        Reference: src/storage/schema/entities/__tests/ProvenTxReqTests.test.ts
                  test('8_getters_and_setters')
        """
        # Given

        now = datetime.now()
        proven_tx_req = ProvenTxReq(
            {
                "provenTxReqId": 1,
                "created_at": now,
                "updated_at": now,
                "txid": "test-txid",
                "rawTx": [1, 2, 3],
                "history": "{}",
                "notify": "{}",
                "attempts": 5,
                "status": "unknown",
                "notified": False,
            }
        )

        # Validate getters
        assert proven_tx_req.proven_tx_req_id == 1
        assert proven_tx_req.txid == "test-txid"
        assert proven_tx_req.attempts == 5
        assert proven_tx_req.status == "unknown"
        assert proven_tx_req.notified is False

        # Validate setters
        proven_tx_req.proven_tx_req_id = 2
        proven_tx_req.txid = "new-txid"
        proven_tx_req.attempts = 10
        proven_tx_req.status = "completed"
        proven_tx_req.notified = True

        assert proven_tx_req.proven_tx_req_id == 2
        assert proven_tx_req.txid == "new-txid"
        assert proven_tx_req.attempts == 10
        assert proven_tx_req.status == "completed"
        assert proven_tx_req.notified is True

        # Validate entity metadata
        assert proven_tx_req.entity_name == "provenTxReq"
        assert proven_tx_req.entity_table == "proven_tx_reqs"
```

### AI Analysis Results

**Similarity Score**: 43.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: sync_state.storageIdentityKey, sync_state.updated_at, sync_state.refNum, sync_state.satoshis, sync_state.status, sync_state.when, sync_state.userId, sync_state.created_at, sync_state.init, sync_state.storageName

**Differences:**
  - Verification count: TS has 10, PY has 12

**Suggestions:**
  - Add verifications for: sync_state.storageIdentityKey, sync_state.updated_at, sync_state.refNum

**Explanation:**

Overall Similarity: 43.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: sync_state.storageIdentityKey, sync_state.updated_at, sync_state.refNum, sync_state.satoshis, sync_state.status, sync_state.when, sync_state.userId, sync_state.created_at, sync_state.init, sync_state.storageName

Key Differences:
  • Verification count: TS has 10, PY has 12

---

## Test 281: 0_creates_instance_with_default_values **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 282: 10_getBsvTx_handles_undefined_rawTx **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 283: 11_getInputs_handles_storage_lookups_and_input_merging **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 284: 15_getProvenTx_retrieves_proven_transaction **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 285: 16_getProvenTx_returns_undefined_when_provenTxId_is_not_set **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 286: 17_getProvenTx_returns_undefined_when_no_matching_ProvenTx_is_found **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 287: 18_getInputs_merges_known_inputs_correctly **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 288: 19_get_version_returns_api_version **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 289: 1_creates_instance_with_provided_api_object **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 290: 20_get_lockTime_returns_api_lockTime **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 291: 21_set_id_updates_transactionId **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 292: 22_get_entityName_returns_correct_value **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 293: 23_get_entityTable_returns_correct_value **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 294: 25_equals_returns_false_for_mismatched_other_properties **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 295: 26_getInputs_handles_known_and_unknown_inputs **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 296: 27_equals_identifies_matching_entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx_req.py`

---

## Test 297: 28_equals_identifies_non_matching_entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output.py`

---

## Test 298: 2_getters_and_setters_work_correctly **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 299: 3_getBsvTx_returns_parsed_transaction **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 300: 4_getBsvTx_returns_undefined_if_no_rawTx **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 301: 5_getBsvTxIns_returns_inputs **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 302: 6_getInputs_combines_spentBy_and_rawTx_inputs **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 303: 9_mergeExisting_updates_when_ei_updated_at_is_newer **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TransactionTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_transaction.py`

---

## Test 304: 10_entityName_returns_correct_value **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TxLabelMapTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_tx_label_map.py`

---

## Test 305: 11_entityTable_returns_correct_value **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TxLabelMapTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_tx_label_map.py`

---

## Test 306: 12_equals_identifies_matching_entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TxLabelMapTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx_req.py`

---

## Test 307: 13_equals_identifies_non_matching_entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TxLabelMapTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output.py`

---

## Test 308: 1_creates_instance_with_default_values **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/TxLabelMapTests.test.ts

```typescript
  test('1_creates_instance_with_default_values', () => {
    const txLabelMap = new EntityTxLabelMap()

    const now = new Date()
    expect(txLabelMap.transactionId).toBe(0)
    expect(txLabelMap.txLabelId).toBe(0)
    expect(txLabelMap.isDeleted).toBe(false)
    expect(txLabelMap.created_at).toBeInstanceOf(Date)
    expect(txLabelMap.updated_at).toBeInstanceOf(Date)
    expect(txLabelMap.created_at.getTime()).toBeLessThanOrEqual(now.getTime())
    expect(txLabelMap.updated_at.getTime()).toBeLessThanOrEqual(now.getTime())
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_transaction.py

```python
    def test_creates_instance_with_default_values(self) -> None:
        """Given: Default Transaction constructor
           When: Create Transaction with no arguments
           Then: Returns Transaction with correct default values

        Reference: src/storage/schema/entities/__tests/TransactionTests.test.ts
                  test('0_creates_instance_with_default_values')
        """
        # Given/When

        tx = Transaction()

        # Then
        now = datetime.now()
        assert tx.transaction_id == 0
        assert tx.user_id == 0
        assert tx.txid == ""
        assert tx.status == "unprocessed"
        assert tx.reference == ""
        assert tx.satoshis == 0
        assert tx.description == ""
        assert tx.is_outgoing is False
        assert tx.raw_tx is None
        assert tx.input_beef is None
        assert isinstance(tx.created_at, datetime)
        assert isinstance(tx.updated_at, datetime)
        assert tx.created_at <= now
        assert tx.updated_at <= now
```

### AI Analysis Results

**Similarity Score**: 43.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: tx_label_map.updated_at, tx_label_map.isDeleted, tx_label_map.transactionId, tx_label_map.txLabelId, tx_label_map.created_at

**Differences:**
  - Verification count: TS has 5, PY has 14

**Suggestions:**
  - Add verifications for: tx_label_map.updated_at, tx_label_map.isDeleted, tx_label_map.transactionId

**Explanation:**

Overall Similarity: 43.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: tx_label_map.updated_at, tx_label_map.isDeleted, tx_label_map.transactionId, tx_label_map.txLabelId, tx_label_map.created_at

Key Differences:
  • Verification count: TS has 5, PY has 14

---

## Test 309: 2_creates_instance_with_provided_api_object **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/TxLabelMapTests.test.ts

```typescript
  test('2_creates_instance_with_provided_api_object', () => {
    const now = new Date()
    const apiObject: TableTxLabelMap = {
      transactionId: 123,
      txLabelId: 456,
      created_at: now,
      updated_at: now,
      isDeleted: true
    }
    const txLabelMap = new EntityTxLabelMap(apiObject)

    expect(txLabelMap.transactionId).toBe(123)
    expect(txLabelMap.txLabelId).toBe(456)
    expect(txLabelMap.isDeleted).toBe(true)
    expect(txLabelMap.created_at).toBe(now)
    expect(txLabelMap.updated_at).toBe(now)
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_transaction.py

```python
    def test_creates_instance_with_provided_api_object(self) -> None:
        """Given: API object with transaction data
           When: Create Transaction with provided API object
           Then: Returns Transaction with values from API object

        Reference: src/storage/schema/entities/__tests/TransactionTests.test.ts
                  test('1_creates_instance_with_provided_api_object')
        """
        # Given

        now = datetime.now()
        api_object = {
            "transactionId": 123,
            "userId": 456,
            "txid": "testTxid",
            "status": "completed",
            "reference": "testReference",
            "satoshis": 789,
            "description": "testDescription",
            "isOutgoing": True,
            "rawTx": [1, 2, 3],
            "inputBEEF": [4, 5, 6],
            "created_at": now,
            "updated_at": now,
        }

        # When
        tx = Transaction(api_object)

        # Then
        assert tx.transaction_id == 123
        assert tx.user_id == 456
        assert tx.txid == "testTxid"
        assert tx.status == "completed"
        assert tx.reference == "testReference"
        assert tx.satoshis == 789
        assert tx.description == "testDescription"
        assert tx.is_outgoing is True
        assert tx.raw_tx == [1, 2, 3]
        assert tx.input_beef == [4, 5, 6]
        assert tx.created_at == now
        assert tx.updated_at == now
```

### AI Analysis Results

**Similarity Score**: 46.00%
  - Structural: 0.00%
  - Semantic: 32.00%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: tx_label_map.updated_at, tx_label_map.isDeleted, tx_label_map.transactionId, tx_label_map.txLabelId, tx_label_map.created_at

**Differences:**
  - Verification count: TS has 5, PY has 12

**Suggestions:**
  - Add verifications for: tx_label_map.updated_at, tx_label_map.isDeleted, tx_label_map.transactionId

**Explanation:**

Overall Similarity: 46.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 32.0% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: authentication value_verification verification
  • Python: authentication verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: tx_label_map.updated_at, tx_label_map.isDeleted, tx_label_map.transactionId, tx_label_map.txLabelId, tx_label_map.created_at

Key Differences:
  • Verification count: TS has 5, PY has 12

---

## Test 310: 3_getters_and_setters_work_correctly **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/TxLabelMapTests.test.ts

```typescript
  test('3_getters_and_setters_work_correctly', () => {
    const txLabelMap = new EntityTxLabelMap()

    const now = new Date()
    txLabelMap.transactionId = 1001
    txLabelMap.txLabelId = 2002
    txLabelMap.isDeleted = true
    txLabelMap.created_at = now
    txLabelMap.updated_at = now

    expect(txLabelMap.transactionId).toBe(1001)
    expect(txLabelMap.txLabelId).toBe(2002)
    expect(txLabelMap.isDeleted).toBe(true)
    expect(txLabelMap.created_at).toBe(now)
    expect(txLabelMap.updated_at).toBe(now)
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_transaction.py

```python
    def test_getters_and_setters_work_correctly(self) -> None:
        """Given: Transaction instance
           When: Set values using setters including version and lockTime
           Then: Getters return the updated values

        Reference: src/storage/schema/entities/__tests/TransactionTests.test.ts
                  test('2_getters_and_setters_work_correctly')
        """
        # Given

        tx = Transaction()

        # When
        now = datetime.now()
        tx.transaction_id = 123
        tx.user_id = 456
        tx.txid = "testTxid"
        tx.status = "processed"
        tx.reference = "testReference"
        tx.satoshis = 789
        tx.description = "testDescription"
        tx.is_outgoing = True
        tx.raw_tx = [1, 2, 3]
        tx.input_beef = [4, 5, 6]
        tx.created_at = now
        tx.updated_at = now
        tx.version = 2
        tx.lock_time = 5000

        # Then
        assert tx.transaction_id == 123
        assert tx.user_id == 456
        assert tx.txid == "testTxid"
        assert tx.status == "processed"
        assert tx.reference == "testReference"
        assert tx.satoshis == 789
        assert tx.description == "testDescription"
        assert tx.is_outgoing is True
        assert tx.raw_tx == [1, 2, 3]
        assert tx.input_beef == [4, 5, 6]
        assert tx.created_at == now
        assert tx.updated_at == now
        assert tx.version == 2
        assert tx.lock_time == 5000
```

### AI Analysis Results

**Similarity Score**: 43.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: tx_label_map.updated_at, tx_label_map.isDeleted, tx_label_map.transactionId, tx_label_map.txLabelId, tx_label_map.created_at

**Differences:**
  - Verification count: TS has 5, PY has 14

**Suggestions:**
  - Add verifications for: tx_label_map.updated_at, tx_label_map.isDeleted, tx_label_map.transactionId

**Explanation:**

Overall Similarity: 43.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: tx_label_map.updated_at, tx_label_map.isDeleted, tx_label_map.transactionId, tx_label_map.txLabelId, tx_label_map.created_at

Key Differences:
  • Verification count: TS has 5, PY has 14

---

## Test 311: 4_updateApi_does_nothing **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TxLabelMapTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_tx_label_map.py`

---

## Test 312: 5_get_id_throws_error **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TxLabelMapTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_tx_label_map.py`

---

## Test 313: 6_equals_checks_equality_correctly **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TxLabelMapTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_tx_label_map.py`

---

## Test 314: 7_mergeFind_finds_or_creates_entity **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TxLabelMapTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_tx_label_map.py`

---

## Test 315: 8_mergeNew_inserts_entity **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/TxLabelMapTests.test.ts

```typescript
  test('8_mergeNew_inserts_entity', async () => {
    const storage: any = {
      insertTxLabelMap: jest.fn()
    }
    const syncMap: any = {
      transaction: { idMap: { 123: 999 } },
      txLabel: { idMap: { 456: 888 } }
    }

    const txLabelMap = new EntityTxLabelMap({
      transactionId: 123,
      txLabelId: 456,
      created_at: new Date(2022, 1, 1),
      updated_at: new Date(2022, 1, 1),
      isDeleted: false
    })

    await txLabelMap.mergeNew(storage, 1, syncMap)
    expect(storage.insertTxLabelMap).toHaveBeenCalledWith(
      expect.objectContaining({
        transactionId: 999,
        txLabelId: 888
      }),
      undefined
    )
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_tx_label_map.py

```python
    def test_mergenew_inserts_entity(self) -> None:
        """Given: TxLabelMap entity and storage with syncMap
           When: Call merge_new
           Then: Inserts entity with mapped IDs

        Reference: src/storage/schema/entities/__tests/TxLabelMapTests.test.ts
                  test('8_mergeNew_inserts_entity')
        """
        # Given

        inserted_data = None

        def mock_insert(data: dict[str, Any], trx: Any = None) -> None:
            nonlocal inserted_data
            inserted_data = data

        mock_storage = type("MockStorage", (), {"insertTxLabelMap": staticmethod(mock_insert)})()

        sync_map = {"transaction": {"idMap": {123: 999}}, "txLabel": {"idMap": {456: 888}}}

        tx_label_map = TxLabelMap(
            {
                "transactionId": 123,
                "txLabelId": 456,
                "created_at": datetime(2022, 2, 1),
                "updated_at": datetime(2022, 2, 1),
                "isDeleted": False,
            }
        )

        # When
        tx_label_map.merge_new(mock_storage, 1, sync_map)

        # Then
        assert inserted_data is not None
        assert inserted_data["transactionId"] == 999
        assert inserted_data["txLabelId"] == 888
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: storage.insertTxLabelMap
  - [HIGH] Python test is missing operations: tx_label_map.mergeNew

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 1, PY has 2

**Suggestions:**
  - Add verifications for: storage.insertTxLabelMap
  - Add operations: tx_label_map.mergeNew

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: storage.insertTxLabelMap
  • [HIGH] Python test is missing operations: tx_label_map.mergeNew

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 1, PY has 2

---

## Test 316: 9_mergeExisting_updates_entity **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/TxLabelMapTests.test.ts

```typescript
  test('9_mergeExisting_updates_entity', async () => {
    const storage: any = {
      updateTxLabelMap: jest.fn()
    }

    const txLabelMap = new EntityTxLabelMap({
      transactionId: 123,
      txLabelId: 456,
      created_at: new Date(2022, 1, 1),
      updated_at: new Date(2022, 1, 1),
      isDeleted: false
    })

    const ei: TableTxLabelMap = {
      transactionId: 123,
      txLabelId: 456,
      isDeleted: true,
      created_at: new Date(),
      updated_at: new Date(2023, 1, 1)
    }

    const syncMap: any = {
      transaction: { idMap: { 123: 999 } },
      txLabel: { idMap: { 456: 888 } }
    }

    const result = await txLabelMap.mergeExisting(storage, new Date(), ei, syncMap)
    expect(result).toBe(true)
    expect(storage.updateTxLabelMap).toHaveBeenCalledWith(
      123,
      456,
      expect.objectContaining({
        isDeleted: true
      }),
      undefined
    )
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_tx_label_map.py

```python
    def test_mergeexisting_updates_entity(self) -> None:
        """Given: TxLabelMap entity with older data
           When: Call merge_existing with newer data
           Then: Updates entity and database

        Reference: src/storage/schema/entities/__tests/TxLabelMapTests.test.ts
                  test('9_mergeExisting_updates_entity')
        """
        # Given

        updated_data = None

        def mock_update(transaction_id: int, tx_label_id: int, data: dict[str, Any], trx: Any = None) -> None:
            nonlocal updated_data
            updated_data = data

        mock_storage = type("MockStorage", (), {"updateTxLabelMap": staticmethod(mock_update)})()

        tx_label_map = TxLabelMap(
            {
                "transactionId": 123,
                "txLabelId": 456,
                "created_at": datetime(2022, 2, 1),
                "updated_at": datetime(2022, 2, 1),
                "isDeleted": False,
            }
        )

        ei = {
            "transactionId": 123,
            "txLabelId": 456,
            "isDeleted": True,
            "created_at": datetime.now(),
            "updated_at": datetime(2023, 2, 1),
        }

        sync_map = {"transaction": {"idMap": {123: 999}}, "txLabel": {"idMap": {456: 888}}}

        # When
        result = tx_label_map.merge_existing(mock_storage, datetime.now(), ei, sync_map)

        # Then
        assert result is True
        assert updated_data is not None
        assert updated_data["isDeleted"] is True
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: storage.updateTxLabelMap
  - [HIGH] Python test is missing operations: tx_label_map.mergeExisting

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: storage.updateTxLabelMap
  - Add operations: tx_label_map.mergeExisting

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification method_call_verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: storage.updateTxLabelMap
  • [HIGH] Python test is missing operations: tx_label_map.mergeExisting

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 317: 1_creates_txLabel_with_default_values **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TxLabelTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_tx_label.py`

---

## Test 318: 2_creates_txLabel_with_provided_api_object **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TxLabelTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_tx_label.py`

---

## Test 319: 3_getters_and_setters_work_correctly **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/TxLabelTests.test.ts

```typescript
  test('3_getters_and_setters_work_correctly', () => {
    const txLabel = new EntityTxLabel()

    const now = new Date()
    txLabel.txLabelId = 1
    txLabel.label = 'New Label'
    txLabel.userId = 200
    txLabel.isDeleted = true
    txLabel.created_at = now
    txLabel.updated_at = now
    txLabel.id = 2

    expect(txLabel.id).toBe(2)
    expect(txLabel.entityName).toBe('txLabel')
    expect(txLabel.entityTable).toBe('tx_labels')
    expect(txLabel.txLabelId).toBe(2)
    expect(txLabel.label).toBe('New Label')
    expect(txLabel.userId).toBe(200)
    expect(txLabel.isDeleted).toBe(true)
    expect(txLabel.created_at).toBe(now)
    expect(txLabel.updated_at).toBe(now)
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_transaction.py

```python
    def test_getters_and_setters_work_correctly(self) -> None:
        """Given: Transaction instance
           When: Set values using setters including version and lockTime
           Then: Getters return the updated values

        Reference: src/storage/schema/entities/__tests/TransactionTests.test.ts
                  test('2_getters_and_setters_work_correctly')
        """
        # Given

        tx = Transaction()

        # When
        now = datetime.now()
        tx.transaction_id = 123
        tx.user_id = 456
        tx.txid = "testTxid"
        tx.status = "processed"
        tx.reference = "testReference"
        tx.satoshis = 789
        tx.description = "testDescription"
        tx.is_outgoing = True
        tx.raw_tx = [1, 2, 3]
        tx.input_beef = [4, 5, 6]
        tx.created_at = now
        tx.updated_at = now
        tx.version = 2
        tx.lock_time = 5000

        # Then
        assert tx.transaction_id == 123
        assert tx.user_id == 456
        assert tx.txid == "testTxid"
        assert tx.status == "processed"
        assert tx.reference == "testReference"
        assert tx.satoshis == 789
        assert tx.description == "testDescription"
        assert tx.is_outgoing is True
        assert tx.raw_tx == [1, 2, 3]
        assert tx.input_beef == [4, 5, 6]
        assert tx.created_at == now
        assert tx.updated_at == now
        assert tx.version == 2
        assert tx.lock_time == 5000
```

### AI Analysis Results

**Similarity Score**: 43.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: tx_label.label, tx_label.id, tx_label.updated_at, tx_label.txLabelId, tx_label.isDeleted, tx_label.entityTable, tx_label.userId, tx_label.entityName, tx_label.created_at

**Differences:**
  - Verification count: TS has 9, PY has 14

**Suggestions:**
  - Add verifications for: tx_label.label, tx_label.id, tx_label.updated_at

**Explanation:**

Overall Similarity: 43.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: tx_label.label, tx_label.id, tx_label.updated_at, tx_label.txLabelId, tx_label.isDeleted, tx_label.entityTable, tx_label.userId, tx_label.entityName, tx_label.created_at

Key Differences:
  • Verification count: TS has 9, PY has 14

---

## Test 320: 5_mergeExisting_does_not_update_txLabel_when_ei_updated_at_is_older **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TxLabelTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_tx_label.py`

---

## Test 321: 6_equals_identifies_matching_entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TxLabelTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx_req.py`

---

## Test 322: 7_equals_identifies_non_matching_entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/TxLabelTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output.py`

---

## Test 323: 0_appends_to_string_log **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/stampLogTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_stamp_log.py`

---

## Test 324: 1_appends_to_object_log **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/stampLogTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_stamp_log.py`

---

## Test 325: 2_returns_undefined_for_invalid_input **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/stampLogTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_stamp_log.py`

---

## Test 326: 3_formats_valid_log_without_network **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/stampLogTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_stamp_log.py`

---

## Test 327: 4_formats_log_with_network_entries **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/stampLogTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_stamp_log.py`

---

## Test 328: 5_handles_invalid_log_entries_gracefully **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/stampLogTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_stamp_log.py`

---

## Test 329: 6_handles_non-string_log_gracefully **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/stampLogTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_stamp_log.py`

---

## Test 330: 10_handles_empty_api_object **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/usersTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_users.py`

---

## Test 331: 11_id_getter_and_setter_work_correctly **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/usersTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_users.py`

---

## Test 332: 12_entityName_returns_User **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/usersTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_users.py`

---

## Test 333: 13_entityTable_returns_users **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/usersTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_users.py`

---

## Test 334: 14_mergeExisting_updates_user_when_ei_updated_at_is_newer **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/usersTests.test.ts

```typescript
  test('14_mergeExisting_updates_user_when_ei_updated_at_is_newer', async () => {
    const user = new EntityUser({
      userId: 1,
      created_at: new Date('2023-01-01'),
      updated_at: new Date('2023-01-01'),
      identityKey: 'oldKey',
      activeStorage: 'oldStorage'
    })

    const updatedEi: TableUser = {
      userId: 1,
      created_at: new Date('2023-01-01'),
      updated_at: new Date('2023-02-01'), // Newer `updated_at`
      identityKey: 'oldKey',
      activeStorage: 'newStorage'
    }

    const result = await user.mergeExisting(
      {
        updateUser: async (id: number, data: TableUser) => {
          expect(id).toBe(1)
          expect(data.activeStorage).toBe('newStorage')
          expect(data.updated_at).toBeInstanceOf(Date)
        }
      } as any,
      undefined,
      updatedEi,
      undefined
    )

    expect(result).toBe(true)
    expect(user.activeStorage).toBe('newStorage') // Updated `activeStorage`
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_users.py

```python
    def test_mergeexisting_updates_user_when_ei_updated_at_is_newer(self) -> None:
        """Given: Existing User with old updated_at
           When: Call merge_existing with newer updated_at
           Then: User is updated and returns True

        Reference: src/storage/schema/entities/__tests/usersTests.test.ts
                  test('14_mergeExisting_updates_user_when_ei_updated_at_is_newer')
        """
        # Given

        user = User(
            {
                "userId": 1,
                "created_at": datetime(2023, 1, 1),
                "updated_at": datetime(2023, 1, 1),
                "identityKey": "oldKey",
                "activeStorage": "oldStorage",
            }
        )

        updated_ei = {
            "userId": 1,
            "created_at": datetime(2023, 1, 1),
            "updated_at": datetime(2023, 2, 1),  # Newer updated_at
            "identityKey": "oldKey",
            "activeStorage": "newStorage",
        }

        # Mock storage
        update_called = False

        def mock_update_user(user_id: int, data: dict[str, Any]) -> None:
            nonlocal update_called
            update_called = True
            assert user_id == 1
            assert data["activeStorage"] == "newStorage"
            assert isinstance(data["updated_at"], datetime)

        mock_storage = type("MockStorage", (), {"update_user": mock_update_user})()

        # When
        result = user.merge_existing(mock_storage, None, updated_ei, None)

        # Then
        assert result is True
        assert user.active_storage == "newStorage"
        assert update_called
```

### AI Analysis Results

**Similarity Score**: 33.33%
  - Structural: 0.00%
  - Semantic: 66.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: user.activeStorage, data.updated_at, data.activeStorage
  - [HIGH] Python test is missing operations: user.mergeExisting

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: user.activeStorage, data.updated_at, data.activeStorage
  - Add operations: user.mergeExisting

**Explanation:**

Overall Similarity: 33.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 66.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: user.activeStorage, data.updated_at, data.activeStorage
  • [HIGH] Python test is missing operations: user.mergeExisting

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 335: 15_mergeExisting_does_not_update_user_when_ei_updated_at_is_older **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/usersTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_users.py`

---

## Test 336: 16_mergeExisting_updates_user_with_trx **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/usersTests.test.ts

```typescript
  test('16_mergeExisting_updates_user_with_trx', async () => {
    const user = new EntityUser({
      userId: 1,
      created_at: new Date('2023-01-01'),
      updated_at: new Date('2023-01-01'),
      identityKey: 'oldKey',
      activeStorage: 'oldStorage'
    })

    const updatedEi: TableUser = {
      userId: 1,
      created_at: new Date('2023-01-01'),
      updated_at: new Date('2023-02-01'), // Newer `updated_at`
      identityKey: 'oldKey',
      activeStorage: 'newStorage'
    }

    const mockTrx = {}

    const result = await user.mergeExisting(
      {
        updateUser: async (id: number, data: TableUser, trx: any) => {
          expect(id).toBe(1)
          expect(data.activeStorage).toBe('newStorage')
          expect(data.updated_at).toBeInstanceOf(Date)
          expect(trx).toBe(mockTrx)
        }
      } as any,
      undefined,
      updatedEi,
      undefined,
      mockTrx
    )

    expect(result).toBe(true)
    expect(user.activeStorage).toBe('newStorage')
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_users.py

```python
    def test_mergeexisting_updates_user_with_trx(self) -> None:
        """Given: Existing User and transaction token
           When: Call merge_existing with newer updated_at and trx
           Then: User is updated with trx and returns True

        Reference: src/storage/schema/entities/__tests/usersTests.test.ts
                  test('16_mergeExisting_updates_user_with_trx')
        """
        # Given

        user = User(
            {
                "userId": 1,
                "created_at": datetime(2023, 1, 1),
                "updated_at": datetime(2023, 1, 1),
                "identityKey": "oldKey",
                "activeStorage": "oldStorage",
            }
        )

        updated_ei = {
            "userId": 1,
            "created_at": datetime(2023, 1, 1),
            "updated_at": datetime(2023, 2, 1),  # Newer updated_at
            "identityKey": "oldKey",
            "activeStorage": "newStorage",
        }

        mock_trx = {"transaction": "mock"}

        # Mock storage
        update_called = False

        def mock_update_user(user_id: int, data: dict[str, Any], trx: dict[str, Any] | None = None) -> None:
            nonlocal update_called
            update_called = True
            assert user_id == 1
            assert data["activeStorage"] == "newStorage"
            assert isinstance(data["updated_at"], datetime)
            assert trx == mock_trx

        mock_storage = type("MockStorage", (), {"update_user": mock_update_user})()

        # When
        result = user.merge_existing(mock_storage, None, updated_ei, None, mock_trx)

        # Then
        assert result is True
        assert user.active_storage == "newStorage"
        assert update_called
```

### AI Analysis Results

**Similarity Score**: 32.00%
  - Structural: 0.00%
  - Semantic: 64.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: user.activeStorage, data.updated_at, data.activeStorage
  - [HIGH] Python test is missing operations: user.mergeExisting

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: user.activeStorage, data.updated_at, data.activeStorage
  - Add operations: user.mergeExisting

**Explanation:**

Overall Similarity: 32.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 64.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: token_operation verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: user.activeStorage, data.updated_at, data.activeStorage
  • [HIGH] Python test is missing operations: user.mergeExisting

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 337: 17_mergeNew_always_throws_error **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/usersTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_users.py`

---

## Test 338: 1_creates_user_with_default_values **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/usersTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_users.py`

---

## Test 339: 2_creates_user_with_provided_api_object **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/usersTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_users.py`

---

## Test 340: 3_getters_and_setters_work_correctly **FAIL**

### TypeScript Test: wallet-toolbox/src/storage/schema/entities/__tests/usersTests.test.ts

```typescript
  test('3_getters_and_setters_work_correctly', () => {
    const user = new EntityUser()

    // Test setting values
    const now = new Date()
    user.userId = 1001
    user.identityKey = 'newIdentityKey'
    user.created_at = now
    user.updated_at = now
    user.activeStorage = 'testActiveStorage' // Setting activeStorage

    // Verify getters return the updated values
    expect(user.userId).toBe(1001)
    expect(user.identityKey).toBe('newIdentityKey')
    expect(user.created_at).toBe(now)
    expect(user.updated_at).toBe(now)
    expect(user.activeStorage).toBe('testActiveStorage') // Getting activeStorage
  })
```

### Python Test: py-wallet-toolbox/tests/storage/entities/test_transaction.py

```python
    def test_getters_and_setters_work_correctly(self) -> None:
        """Given: Transaction instance
           When: Set values using setters including version and lockTime
           Then: Getters return the updated values

        Reference: src/storage/schema/entities/__tests/TransactionTests.test.ts
                  test('2_getters_and_setters_work_correctly')
        """
        # Given

        tx = Transaction()

        # When
        now = datetime.now()
        tx.transaction_id = 123
        tx.user_id = 456
        tx.txid = "testTxid"
        tx.status = "processed"
        tx.reference = "testReference"
        tx.satoshis = 789
        tx.description = "testDescription"
        tx.is_outgoing = True
        tx.raw_tx = [1, 2, 3]
        tx.input_beef = [4, 5, 6]
        tx.created_at = now
        tx.updated_at = now
        tx.version = 2
        tx.lock_time = 5000

        # Then
        assert tx.transaction_id == 123
        assert tx.user_id == 456
        assert tx.txid == "testTxid"
        assert tx.status == "processed"
        assert tx.reference == "testReference"
        assert tx.satoshis == 789
        assert tx.description == "testDescription"
        assert tx.is_outgoing is True
        assert tx.raw_tx == [1, 2, 3]
        assert tx.input_beef == [4, 5, 6]
        assert tx.created_at == now
        assert tx.updated_at == now
        assert tx.version == 2
        assert tx.lock_time == 5000
```

### AI Analysis Results

**Similarity Score**: 43.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: user.userId, user.activeStorage, user.identityKey, user.created_at, user.updated_at

**Differences:**
  - Verification count: TS has 5, PY has 14

**Suggestions:**
  - Add verifications for: user.userId, user.activeStorage, user.identityKey

**Explanation:**

Overall Similarity: 43.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: user.userId, user.activeStorage, user.identityKey, user.created_at, user.updated_at

Key Differences:
  • Verification count: TS has 5, PY has 14

---

## Test 341: 5_equals_identifies_matching_entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/usersTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_proven_tx_req.py`

---

## Test 342: 6_equals_identifies_non_matching_entities **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/usersTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_output.py`

---

## Test 343: 7_handles_edge_cases_in_constructor **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/usersTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_users.py`

---

## Test 344: 8_handles_large_input_values **PASS**

- TypeScript: `wallet-toolbox/src/storage/schema/entities/__tests/usersTests.test.ts`
- Python: `py-wallet-toolbox/tests/storage/entities/test_users.py`

---

## Test 345: 0 convert from Uint8Array **FAIL**

### TypeScript Test: wallet-toolbox/src/utility/__tests/utilityHelpers.noBuffer.test.ts

```typescript
  test('0 convert from Uint8Array', async () => {
    const a = new Uint8Array([1, 2, 3, 4])
    {
      const r = asUint8Array(a)
      expect(r.length).toBe(4)
      expect(r.every((v, i) => v === a[i])).toBe(true)
    }
    {
      const r = asString(a)
      expect(r).toBe('01020304')
    }
    {
      const r = asString(a, 'hex')
      expect(r).toBe('01020304')
    }
    {
      const r = asString(a, 'utf8')
      expect(r).toBe('\x01\x02\x03\x04')
    }
    {
      const r = asString(a, 'base64')
      expect(r).toBe('AQIDBA==')
    }
  })
```

### Python Test: py-wallet-toolbox/tests/utils/test_utility_helpers_no_buffer.py

```python
    def test_convert_from_uint8array(self) -> None:
        """Given: Uint8Array [1, 2, 3, 4]
           When: Convert using asUint8Array and asString with various encodings
           Then: Returns correct conversions for each encoding

        Reference: wallet-toolbox/src/utility/__tests/utilityHelpers.noBuffer.test.ts
                   test('0 convert from Uint8Array')
        """
        # Given
        a = bytes([1, 2, 3, 4])

        # When/Then - asUint8Array
        r = as_uint8_array(a)
        assert len(r) == 4
        assert all(r[i] == a[i] for i in range(len(a)))

        # When/Then - asString (default hex)
        r = as_string(a)
        assert r == "01020304"

        # When/Then - asString with 'hex'
        r = as_string(a, "hex")
        assert r == "01020304"

        # When/Then - asString with 'utf8'
        r = as_string(a, "utf8")
        assert r == "\x01\x02\x03\x04"

        # When/Then - asString with 'base64'
        r = as_string(a, "base64")
        assert r == "AQIDBA=="
```

### AI Analysis Results

**Similarity Score**: 43.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: r.length

**Differences:**
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: r.length

**Explanation:**

Overall Similarity: 43.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: r.length

Key Differences:
  • Verification count: TS has 1, PY has 0

---

## Test 346: 1 convert from number[] **FAIL**

### TypeScript Test: wallet-toolbox/src/utility/__tests/utilityHelpers.noBuffer.test.ts

```typescript
  test('1 convert from number[]', async () => {
    const a = [1, 2, 3, 4]
    {
      const r = asUint8Array(a)
      expect(r.length).toBe(4)
      expect(r.every((v, i) => v === a[i])).toBe(true)
    }
    {
      const r = asString(a)
      expect(r).toBe('01020304')
    }
    {
      const r = asString(a, 'hex')
      expect(r).toBe('01020304')
    }
    {
      const r = asString(a, 'utf8')
      expect(r).toBe('\x01\x02\x03\x04')
    }
    {
      const r = asString(a, 'base64')
      expect(r).toBe('AQIDBA==')
    }
  })
```

### Python Test: py-wallet-toolbox/tests/utils/test_utility_helpers_no_buffer.py

```python
    def test_convert_from_number_array(self) -> None:
        """Given: number[] [1, 2, 3, 4]
           When: Convert using asUint8Array and asString with various encodings
           Then: Returns correct conversions for each encoding

        Reference: wallet-toolbox/src/utility/__tests/utilityHelpers.noBuffer.test.ts
                   test('1 convert from number[]')
        """
        # Given
        a = [1, 2, 3, 4]

        # When/Then - asUint8Array
        r = as_uint8_array(a)
        assert len(r) == 4
        assert all(r[i] == a[i] for i in range(len(a)))

        # When/Then - asString (default hex)
        r = as_string(a)
        assert r == "01020304"

        # When/Then - asString with 'hex'
        r = as_string(a, "hex")
        assert r == "01020304"

        # When/Then - asString with 'utf8'
        r = as_string(a, "utf8")
        assert r == "\x01\x02\x03\x04"

        # When/Then - asString with 'base64'
        r = as_string(a, "base64")
        assert r == "AQIDBA=="
```

### AI Analysis Results

**Similarity Score**: 43.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: r.length

**Differences:**
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: r.length

**Explanation:**

Overall Similarity: 43.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: r.length

Key Differences:
  • Verification count: TS has 1, PY has 0

---

## Test 347: 2 convert from hex string **FAIL**

### TypeScript Test: wallet-toolbox/src/utility/__tests/utilityHelpers.noBuffer.test.ts

```typescript
  test('2 convert from hex string', async () => {
    const a = '01020304'
    {
      const r = asUint8Array(a)
      expect(r.length).toBe(4)
      expect(r.every((v, i) => v === parseInt(a.slice(i * 2, i * 2 + 2), 16))).toBe(true)
    }
    {
      const r = asString(a)
      expect(r).toBe('01020304')
    }
    {
      const r = asString(a, 'hex')
      expect(r).toBe('01020304')
    }
    {
      const r = asString(a, 'hex', 'hex')
      expect(r).toBe('01020304')
    }
    {
      const r = asString(a, 'hex', 'utf8')
      expect(r).toBe('\x01\x02\x03\x04')
    }
    {
      const r = asString(a, 'hex', 'base64')
      expect(r).toBe('AQIDBA==')
    }
  })
```

### Python Test: py-wallet-toolbox/tests/utils/test_utility_helpers_no_buffer.py

```python
    def test_convert_from_hex_string(self) -> None:
        """Given: hex string '01020304'
           When: Convert using asUint8Array and asString with various input/output encodings
           Then: Returns correct conversions for each encoding combination

        Reference: wallet-toolbox/src/utility/__tests/utilityHelpers.noBuffer.test.ts
                   test('2 convert from hex string')
        """
        # Given
        a = "01020304"

        # When/Then - asUint8Array
        r = as_uint8_array(a)
        assert len(r) == 4
        assert all(r[i] == int(a[i * 2 : i * 2 + 2], 16) for i in range(len(r)))

        # When/Then - asString (default hex)
        r = as_string(a)
        assert r == "01020304"

        # When/Then - asString with 'hex'
        r = as_string(a, "hex")
        assert r == "01020304"

        # When/Then - asString with 'hex' input and 'hex' output
        r = as_string(a, "hex", "hex")
        assert r == "01020304"

        # When/Then - asString with 'hex' input and 'utf8' output
        r = as_string(a, "hex", "utf8")
        assert r == "\x01\x02\x03\x04"

        # When/Then - asString with 'hex' input and 'base64' output
        r = as_string(a, "hex", "base64")
        assert r == "AQIDBA=="
```

### AI Analysis Results

**Similarity Score**: 43.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: r.length

**Differences:**
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: r.length

**Explanation:**

Overall Similarity: 43.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: r.length

Key Differences:
  • Verification count: TS has 1, PY has 0

---

## Test 348: 3 convert from utf8 string **FAIL**

### TypeScript Test: wallet-toolbox/src/utility/__tests/utilityHelpers.noBuffer.test.ts

```typescript
  test('3 convert from utf8 string', async () => {
    const a = '\x01\x02\x03\x04'
    {
      const r = asUint8Array(a, 'utf8')
      expect(r.length).toBe(4)
      expect(r.every((v, i) => v === i + 1)).toBe(true)
    }
    {
      const r = asString(a, 'utf8', 'hex')
      expect(r).toBe('01020304')
    }
    {
      const r = asString(a, 'utf8')
      expect(r).toBe('\x01\x02\x03\x04')
    }
    {
      const r = asString(a, 'utf8', 'utf8')
      expect(r).toBe('\x01\x02\x03\x04')
    }
    {
      const r = asString(a, 'utf8', 'base64')
      expect(r).toBe('AQIDBA==')
    }
  })
```

### Python Test: py-wallet-toolbox/tests/utils/test_utility_helpers_no_buffer.py

```python
    def test_convert_from_utf8_string(self) -> None:
        """Given: utf8 string '\x01\x02\x03\x04'
           When: Convert using asUint8Array and asString with various output encodings
           Then: Returns correct conversions for each encoding

        Reference: wallet-toolbox/src/utility/__tests/utilityHelpers.noBuffer.test.ts
                   test('3 convert from utf8 string')
        """
        # Given
        a = "\x01\x02\x03\x04"

        # When/Then - asUint8Array with 'utf8' input
        r = as_uint8_array(a, "utf8")
        assert len(r) == 4
        assert all(r[i] == i + 1 for i in range(len(r)))

        # When/Then - asString with 'utf8' input and 'hex' output
        r = as_string(a, "utf8", "hex")
        assert r == "01020304"

        # When/Then - asString with 'utf8' input (default utf8 output)
        r = as_string(a, "utf8")
        assert r == "\x01\x02\x03\x04"

        # When/Then - asString with 'utf8' input and 'utf8' output
        r = as_string(a, "utf8", "utf8")
        assert r == "\x01\x02\x03\x04"

        # When/Then - asString with 'utf8' input and 'base64' output
        r = as_string(a, "utf8", "base64")
        assert r == "AQIDBA=="
```

### AI Analysis Results

**Similarity Score**: 43.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: r.length

**Differences:**
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: r.length

**Explanation:**

Overall Similarity: 43.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: r.length

Key Differences:
  • Verification count: TS has 1, PY has 0

---

## Test 349: 00 **PASS**

- TypeScript: `wallet-toolbox/src/wab-client/__tests/WABClient.man.test.ts`
- Python: `py-wallet-toolbox/tests/wallet/test_certificates.py`

---

## Test 350: 0 invalid params **FAIL**

### TypeScript Test: wallet-toolbox/test/Wallet/action/abortAction.test.ts

```typescript
  test('0 invalid params', async () => {
    const ctxs: TestWalletNoSetup[] = []
    if (env.runMySQL) ctxs.push(await _tu.createLegacyWalletMySQLCopy('abortActionTests'))
    ctxs.push(await _tu.createLegacyWalletSQLiteCopy('abortActionTests'))
    for (const { wallet } of ctxs) {
      const invalidArgs: AbortActionArgs[] = [
        { reference: '' },
        { reference: '====' },
        { reference: 'a'.repeat(301) },
        { reference: 'a'.repeat(300) }
        // Oh so many things to test...
      ]

      for (const args of invalidArgs) {
        await expectToThrowWERR(sdk.WERR_INVALID_PARAMETER, () => wallet.abortAction(args))
      }
    }
    for (const ctx of ctxs) {
      await ctx.storage.destroy()
    }
  })
```

### Python Test: py-wallet-toolbox/tests/wallet/test_certificates.py

```python
    def test_invalid_params(self, wallet_with_storage: Wallet) -> None:
        """Given: Wallet with test storage and invalid certificate arguments
           When: Call acquireCertificate with invalid params (empty type, empty certifier)
           Then: Raises InvalidParameterError

        Reference: wallet-toolbox/test/Wallet/certificate/acquireCertificate.test.ts
                   test('1 invalid params')
        """
        # Given
        # wallet = Wallet(chain="test")  # Not needed, using wallet_with_storage

        invalid_args = {"type": "", "certifier": "", "acquisitionProtocol": "direct", "fields": {}}

        # When/Then
        with pytest.raises(InvalidParameterError):
            wallet_with_storage.acquire_certificate(invalid_args)
```

### AI Analysis Results

**Similarity Score**: 30.00%
  - Structural: 0.00%
  - Semantic: 60.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  - [HIGH] Python test is missing operations: _tu.createLegacyWalletSQLiteCopy, _tu.createLegacyWalletMySQLCopy

**Differences:**
  - Operation count: TS has 2, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'verification'
  - Add operations: _tu.createLegacyWalletSQLiteCopy, _tu.createLegacyWalletMySQLCopy

**Explanation:**

Overall Similarity: 30.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 60.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification
  • Python: general_test

Critical Issues (2):
  • [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  • [HIGH] Python test is missing operations: _tu.createLegacyWalletSQLiteCopy, _tu.createLegacyWalletMySQLCopy

Key Differences:
  • Operation count: TS has 2, PY has 0

---

## Test 351: 0_invalid_params **PASS**

- TypeScript: `wallet-toolbox/test/Wallet/action/createAction.test.ts`
- Python: `py-wallet-toolbox/tests/wallet/test_certificates.py`

---

## Test 352: 1_repeatable txid **PASS**

- TypeScript: `wallet-toolbox/test/Wallet/action/createAction.test.ts`
- Python: `py-wallet-toolbox/tests/wallet/test_wallet_create_action.py`

---

## Test 353: 2_signableTransaction **FAIL**

### TypeScript Test: wallet-toolbox/test/Wallet/action/createAction.test.ts

```typescript
  test('2_signableTransaction', async () => {
    if (!includeTestChaintracks) return
    for (const { wallet } of ctxs) {
      const root = '02135476'
      const kp = _tu.getKeyPair(root.repeat(8))

      let txid1: string
      let txid2: string
      const outputSatoshis = 42
      let noSendChange: string[] | undefined
      let inputBEEF: AtomicBEEF | undefined

      {
        const createArgs: CreateActionArgs = {
          description: `${kp.address} of ${root}`,
          outputs: [
            {
              satoshis: outputSatoshis,
              lockingScript: _tu.getLockP2PKH(kp.address).toHex(),
              outputDescription: 'pay fred'
            }
          ],
          options: {
            randomizeOutputs: false,
            signAndProcess: false,
            noSend: true
          }
        }

        const cr = await wallet.createAction(createArgs)

        noSendChange = cr.noSendChange

        expect(cr.noSendChange).toBeTruthy()
        expect(cr.sendWithResults).toBeUndefined()
        expect(cr.tx).toBeUndefined()
        expect(cr.txid).toBeUndefined()

        expect(cr.signableTransaction).toBeTruthy()
        const st = cr.signableTransaction!
        expect(st.reference).toBeTruthy()
        // const tx = Transaction.fromAtomicBEEF(st.tx) // Transaction doesn't support V2 Beef yet.
        const atomicBeef = Beef.fromBinary(st.tx)
        const tx = atomicBeef.txs[atomicBeef.txs.length - 1].tx!
        for (const input of tx.inputs) {
          expect(atomicBeef.findTxid(input.sourceTXID!)).toBeTruthy()
        }

        // Spending authorization check happens here...
        //expect(st.amount > 242 && st.amount < 300).toBe(true)

        // sign and complete
        const signArgs: SignActionArgs = {
          reference: st.reference,
          spends: {},
          options: {
            returnTXIDOnly: false,
            noSend: true
          }
        }

        const sr = await wallet.signAction(signArgs)
        inputBEEF = sr.tx

        txid1 = sr.txid!
        // Update the noSendChange txid to final signed value.
        noSendChange = noSendChange!.map(op => `${txid1}.${op.split('.')[1]}`)
      }

      {
        const unlock = _tu.getUnlockP2PKH(kp.privateKey, outputSatoshis)
        const unlockingScriptLength = await unlock.estimateLength()

        const createArgs: CreateActionArgs = {
          description: `${kp.address} of ${root}`,
          inputs: [
            {
              outpoint: `${txid1}.0`,
              inputDescription: 'spend ${kp.address} of ${root}',
              unlockingScriptLength
            }
          ],
          inputBEEF,
          options: {
            noSendChange,
            // signAndProcess: false, // Not required as an input lacks unlock script...
            noSend: true
          }
        }

        const cr = await wallet.createAction(createArgs)

        expect(cr.noSendChange).toBeTruthy()
        expect(cr.sendWithResults).toBeUndefined()
        expect(cr.tx).toBeUndefined()
        expect(cr.txid).toBeUndefined()
        expect(cr.signableTransaction).toBeTruthy()
        const st = cr.signableTransaction!
        expect(st.reference).toBeTruthy()
        const atomicBeef = Beef.fromBinary(st.tx)
        const tx = atomicBeef.txs[atomicBeef.txs.length - 1].tx!

        tx.inputs[0].unlockingScriptTemplate = unlock
        await tx.sign()
        const unlockingScript = tx.inputs[0].unlockingScript!.toHex()

        const signArgs: SignActionArgs = {
          reference: st.reference,
          spends: { 0: { unlockingScript } },
          options: {
            returnTXIDOnly: true,
            noSend: true
          }
        }

        const sr = await wallet.signAction(signArgs)

        txid2 = sr.txid!
      }
      {
        const createArgs: CreateActionArgs = {
          description: `${kp.address} of ${root}`,
          options: {
            acceptDelayedBroadcast: false,
            sendWith: [txid1, txid2]
          }
        }

        const cr = await wallet.createAction(createArgs)

        expect(cr.noSendChange).not.toBeTruthy()
        expect(cr.sendWithResults?.length).toBe(2)
        const [swr1, swr2] = cr.sendWithResults!
        expect(swr1.status !== 'failed').toBe(true)
        expect(swr2.status !== 'failed').toBe(true)
        expect(swr1.txid).toBe(txid1)
        expect(swr2.txid).toBe(txid2)
      }
    }
  })
```

### Python Test: py-wallet-toolbox/tests/wallet/test_wallet_create_action.py

```python
    def test_signable_transaction(self, wallet_with_storage: Wallet) -> None:
        """Given: CreateActionArgs with signAndProcess=False
           When: Call create_action
           Then: Returns signableTransaction for external signing

        Reference: wallet-toolbox/test/wallet/action/createAction.test.ts
                   test('2_signableTransaction')

        Note: This test requires:
        - Test wallet with UTXOs
        - Ability to create unsigned transactions
        - noSend=True to prevent broadcasting
        """
        # Given
        create_args = {
            "description": "Test payment",
            "outputs": [
                {"satoshis": 42, "lockingScript": "76a914" + "00" * 20 + "88ac", "outputDescription": "pay fred"}
            ],
            "options": {"randomizeOutputs": False, "signAndProcess": False, "noSend": True},  # Return unsigned tx
        }

        # When
        result = wallet_with_storage.create_action(create_args)

        # Then
        assert "noSendChange" in result
        assert result["noSendChange"] is not None
        assert "sendWithResults" not in result or result["sendWithResults"] is None
        assert "tx" not in result or result["tx"] is None
        assert "txid" not in result or result["txid"] is None
        assert "signableTransaction" in result
        assert result["signableTransaction"] is not None
        assert "reference" in result["signableTransaction"]
        assert "tx" in result["signableTransaction"]  # AtomicBEEF format
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: st.reference, swr2.txid, cr.sendWithResults, cr.signableTransaction, cr.tx, cr.txid, swr1.txid, cr.noSendChange
  - [HIGH] Python test is missing operations: tx.sign, wallet.createAction, wallet.signAction, unlock.estimateLength

**Differences:**
  - Operation count: TS has 7, PY has 0
  - Verification count: TS has 14, PY has 7

**Suggestions:**
  - Add verifications for: st.reference, swr2.txid, cr.sendWithResults
  - Add operations: tx.sign, wallet.createAction, wallet.signAction

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification key_change
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: st.reference, swr2.txid, cr.sendWithResults, cr.signableTransaction, cr.tx, cr.txid, swr1.txid, cr.noSendChange
  • [HIGH] Python test is missing operations: tx.sign, wallet.createAction, wallet.signAction, unlock.estimateLength

Key Differences:
  • Operation count: TS has 7, PY has 0
  • Verification count: TS has 14, PY has 7

---

## Test 354: 0 invalid params **PASS**

- TypeScript: `wallet-toolbox/test/Wallet/action/internalizeAction.test.ts`
- Python: `py-wallet-toolbox/tests/wallet/test_certificates.py`

---

## Test 355: 00 **PASS**

- TypeScript: `wallet-toolbox/test/Wallet/certificate/acquireCertificate.test.ts`
- Python: `py-wallet-toolbox/tests/wallet/test_certificates.py`

---

## Test 356: 1 invalid params **FAIL**

### TypeScript Test: wallet-toolbox/test/Wallet/certificate/acquireCertificate.test.ts

```typescript
  test('1 invalid params', async () => {
    const { wallet, storage } = await _tu.createLegacyWalletSQLiteCopy('acquireCertificate1')

    const invalidArgs: AcquireCertificateArgs[] = [
      {
        type: '',
        certifier: '',
        acquisitionProtocol: 'direct',
        fields: {}
      }
      // Oh so many things to test...
    ]

    for (const args of invalidArgs) {
      await expectToThrowWERR(sdk.WERR_INVALID_PARAMETER, () => wallet.acquireCertificate(args))
    }

    await storage.destroy()
  })
```

### Python Test: py-wallet-toolbox/tests/wallet/test_certificates.py

```python
    def test_invalid_params(self, wallet_with_storage: Wallet) -> None:
        """Given: Wallet with test storage and invalid certificate arguments
           When: Call acquireCertificate with invalid params (empty type, empty certifier)
           Then: Raises InvalidParameterError

        Reference: wallet-toolbox/test/Wallet/certificate/acquireCertificate.test.ts
                   test('1 invalid params')
        """
        # Given
        # wallet = Wallet(chain="test")  # Not needed, using wallet_with_storage

        invalid_args = {"type": "", "certifier": "", "acquisitionProtocol": "direct", "fields": {}}

        # When/Then
        with pytest.raises(InvalidParameterError):
            wallet_with_storage.acquire_certificate(invalid_args)
```

### AI Analysis Results

**Similarity Score**: 30.00%
  - Structural: 0.00%
  - Semantic: 60.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  - [HIGH] Python test is missing operations: _tu.createLegacyWalletSQLiteCopy, storage.destroy

**Differences:**
  - Operation count: TS has 2, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'verification'
  - Add operations: _tu.createLegacyWalletSQLiteCopy, storage.destroy

**Explanation:**

Overall Similarity: 30.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 60.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification
  • Python: general_test

Critical Issues (2):
  • [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  • [HIGH] Python test is missing operations: _tu.createLegacyWalletSQLiteCopy, storage.destroy

Key Differences:
  • Operation count: TS has 2, PY has 0

---

## Test 357: 2 acquireCertificate listCertificate proveCertificate **FAIL**

### TypeScript Test: wallet-toolbox/test/Wallet/certificate/acquireCertificate.test.ts

```typescript
  test('2 acquireCertificate listCertificate proveCertificate', async () => {
    const { wallet, storage } = await _tu.createSQLiteTestWallet({
      databaseName: 'acquireCertificate2',
      dropAll: true
    })

    // Make a test certificate from a random certifier for the wallet's identityKey
    const subject = wallet.keyDeriver.identityKey
    const { cert: wcert, certifier } = _tu.makeSampleCert(subject)

    // Act as the certifier: create a wallet for them...
    const certifierWallet = new ProtoWallet(certifier)

    const cert = new Certificate(
      wcert.type,
      wcert.serialNumber,
      wcert.subject,
      wcert.certifier,
      wcert.revocationOutpoint,
      wcert.fields
    )

    const r1 = await MasterCertificate.createCertificateFields(certifierWallet, subject, cert.fields)
    const signedCert = new Certificate(
      wcert.type,
      wcert.serialNumber,
      wcert.subject,
      wcert.certifier,
      wcert.revocationOutpoint,
      r1.certificateFields
    )
    await signedCert.sign(certifierWallet)

    const c = signedCert
    // args object to create a new certificate via 'direct' protocol.
    const args: AcquireCertificateArgs = {
      serialNumber: c.serialNumber,
      signature: c.signature,
      privileged: false,
      privilegedReason: undefined,

      type: c.type,
      certifier: c.certifier,
      acquisitionProtocol: 'direct',
      fields: c.fields,
      keyringForSubject: r1.masterKeyring,
      keyringRevealer: 'certifier',
      revocationOutpoint: c.revocationOutpoint
    }
    // store the new signed certificate in user's wallet
    const r = await wallet.acquireCertificate(args)
    expect(r.serialNumber).toBe(c.serialNumber)

    // Attempt to retrieve it... since
    // the certifier is random this should
    // always be unique :-)
    const lcs = await wallet.listCertificates({
      certifiers: [cert.certifier],
      types: []
    })
    expect(lcs.certificates.length).toBe(1)
    const lc = lcs.certificates[0]
    // the result should be encrypted.
    expect(lc.fields['name']).not.toBe('Alice')

    // Use proveCertificate to obtain a decryption keyring:
    const pkrArgs: ProveCertificateArgs = {
      certificate: { serialNumber: lc.serialNumber },
      fieldsToReveal: ['name'],
      verifier: subject
    }
    const pkr = await wallet.proveCertificate(pkrArgs)

    const veriCert = new VerifiableCertificate(
      lc.type,
      lc.serialNumber,
      lc.subject,
      lc.certifier,
      lc.revocationOutpoint,
      lc.fields,
      pkr.keyringForVerifier,
      lc.signature
    )

    const r4 = await veriCert.decryptFields(wallet)
    expect(r4['name']).toBe('Alice')

    const certs = await wallet.listCertificates({ types: [], certifiers: [] })
    for (const cert of certs.certificates) {
      const rr = await wallet.relinquishCertificate({
        type: cert.type,
        serialNumber: cert.serialNumber,
        certifier: cert.certifier
      })
      expect(rr.relinquished).toBe(true)
    }
    await storage.destroy()
  })
```

### Python Test: py-wallet-toolbox/tests/wallet/test_certificates.py

```python
    def test_acquirecertificate_listcertificate_provecertificate(self, wallet_with_storage: Wallet) -> None:
        """Given: Wallet with test database and sample certificate from certifier
           When: acquireCertificate, listCertificates, proveCertificate, and relinquishCertificate
           Then: Certificate is stored, retrieved, fields are encrypted, can be decrypted with keyring, and relinquished

        Reference: wallet-toolbox/test/Wallet/certificate/acquireCertificate.test.ts
                   test('2 acquireCertificate listCertificate proveCertificate')
        """
        # Given
        # Create test wallet with SQLite storage
        # wallet = Wallet(chain="test")  # Not needed, using wallet_with_storage

        # Make a test certificate from a random certifier for the wallet's identityKey
        subject = wallet_with_storage.key_deriver.identity_key
        cert_data, certifier = _make_sample_cert(subject)

        # Act as the certifier: create a wallet for them
        certifier_wallet = _create_proto_wallet(certifier)

        # Create certificate and sign it
        cert = _create_certificate(cert_data)
        signed_fields = _create_certificate_fields(certifier_wallet, subject, cert["fields"])
        signed_cert = _create_signed_certificate(cert_data, signed_fields)
        _sign_certificate(signed_cert, certifier_wallet)

        # Prepare args object to create a new certificate via 'direct' protocol
        args = {
            "serialNumber": signed_cert["serialNumber"],
            "signature": signed_cert["signature"],
            "privileged": False,
            "privilegedReason": None,
            "type": signed_cert["type"],
            "certifier": signed_cert["certifier"],
            "acquisitionProtocol": "direct",
            "fields": signed_cert["fields"],
            "keyringForSubject": signed_fields["masterKeyring"],
            "keyringRevealer": "certifier",
            "revocationOutpoint": signed_cert["revocationOutpoint"],
        }

        # When
        # Store the new signed certificate in user's wallet
        result = wallet_with_storage.acquire_certificate(args)

        # Then
        assert result["serialNumber"] == signed_cert["serialNumber"]

        # Attempt to retrieve it
        list_result = wallet_with_storage.list_certificates({"certifiers": [cert_data["certifier"]], "types": []})
        assert len(list_result["certificates"]) == 1
        lc = list_result["certificates"][0]

        # The result should be encrypted
        assert lc["fields"]["name"] != "Alice"

        # Use proveCertificate to obtain a decryption keyring
        prove_args = {
            "certificate": {"serialNumber": lc["serialNumber"]},
            "fieldsToReveal": ["name"],
            "verifier": subject,
        }
        prove_result = wallet_with_storage.prove_certificate(prove_args)

        # Create VerifiableCertificate and decrypt fields
        verifiable_cert = _create_verifiable_certificate(lc, prove_result["keyringForVerifier"])
        decrypted = _decrypt_fields(verifiable_cert, wallet_with_storage)
        assert decrypted["name"] == "Alice"

        # Cleanup: relinquish all certificates
        certs = wallet_with_storage.list_certificates({"types": [], "certifiers": []})
        for cert in certs["certificates"]:
            relinquish_result = wallet_with_storage.relinquish_certificate(
                {"type": cert["type"], "serialNumber": cert["serialNumber"], "certifier": cert["certifier"]}
            )
            assert relinquish_result["relinquished"] is True
```

### AI Analysis Results

**Similarity Score**: 17.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: r.serialNumber, rr.relinquished
  - [HIGH] Python test is missing operations: veri_cert.decryptFields, signed_cert.sign, _tu.createSQLiteTestWallet, wallet.proveCertificate, wallet.listCertificates, wallet.relinquishCertificate, master_certificate.createCertificateFields, storage.destroy, wallet.acquireCertificate

**Differences:**
  - Operation count: TS has 10, PY has 0
  - Verification count: TS has 2, PY has 5

**Suggestions:**
  - Add verifications for: r.serialNumber, rr.relinquished
  - Add operations: veri_cert.decryptFields, signed_cert.sign, _tu.createSQLiteTestWallet

**Explanation:**

Overall Similarity: 17.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification decryption verification encryption
  • Python: decryption verification encryption

Critical Issues (2):
  • [HIGH] Python test is missing verifications: r.serialNumber, rr.relinquished
  • [HIGH] Python test is missing operations: veri_cert.decryptFields, signed_cert.sign, _tu.createSQLiteTestWallet, wallet.proveCertificate, wallet.listCertificates, wallet.relinquishCertificate, master_certificate.createCertificateFields, storage.destroy, wallet.acquireCertificate

Key Differences:
  • Operation count: TS has 10, PY has 0
  • Verification count: TS has 2, PY has 5

---

## Test 358: 3 privileged acquireCertificate listCertificate proveCertificate **FAIL**

### TypeScript Test: wallet-toolbox/test/Wallet/certificate/acquireCertificate.test.ts

```typescript
  test('3 privileged acquireCertificate listCertificate proveCertificate', async () => {
    const { wallet, storage } = await _tu.createSQLiteTestWallet({
      databaseName: 'acquireCertificate3',
      privKeyHex: '42'.repeat(32),
      dropAll: true
    })

    // Make a test certificate from a random certifier for the wallet's identityKey

    // Certificate issued to the privileged key must use the privilegedKeyManager's identityKey
    const subject = (await wallet.privilegedKeyManager!.getPublicKey({ identityKey: true })).publicKey
    const { cert: wcert, certifier } = _tu.makeSampleCert(subject)

    // Act as the certifier: create a wallet for them...
    const certifierWallet = new ProtoWallet(certifier)

    const cert = new Certificate(
      wcert.type,
      wcert.serialNumber,
      wcert.subject,
      wcert.certifier,
      wcert.revocationOutpoint,
      wcert.fields
    )

    const r1 = await MasterCertificate.createCertificateFields(certifierWallet, subject, cert.fields)
    const signedCert = new Certificate(
      wcert.type,
      wcert.serialNumber,
      wcert.subject,
      wcert.certifier,
      wcert.revocationOutpoint,
      r1.certificateFields
    )
    await signedCert.sign(certifierWallet)

    const c = signedCert

    // args object to create a new certificate via 'direct' protocol.
    const args: AcquireCertificateArgs = {
      serialNumber: c.serialNumber,
      signature: c.signature,
      privileged: true,
      privilegedReason: 'access to my penthouse',

      type: c.type,
      certifier: c.certifier,
      acquisitionProtocol: 'direct',
      fields: c.fields,
      keyringForSubject: r1.masterKeyring,
      keyringRevealer: 'certifier',
      revocationOutpoint: c.revocationOutpoint
    }
    // store the new signed certificate in user's wallet
    const r = await wallet.acquireCertificate(args)
    expect(r.serialNumber).toBe(c.serialNumber)

    // Attempt to retrieve it... since
    // the certifier is random this should
    // always be unique :-)
    const lcs = await wallet.listCertificates({
      certifiers: [cert.certifier],
      types: []
    })
    expect(lcs.certificates.length).toBe(1)
    const lc = lcs.certificates[0]
    // the result should be encrypted.
    expect(lc.fields['name']).not.toBe('Alice')

    // Use proveCertificate to obtain a decryption keyring:
    const pkrArgs: ProveCertificateArgs = {
      certificate: { serialNumber: lc.serialNumber },
      fieldsToReveal: ['name'],
      verifier: subject,
      privileged: true,
      privilegedReason: 'more cheese'
    }
    const pkr = await wallet.proveCertificate(pkrArgs)

    const veriCert = new VerifiableCertificate(
      lc.type,
      lc.serialNumber,
      lc.subject,
      lc.certifier,
      lc.revocationOutpoint,
      lc.fields,
      pkr.keyringForVerifier,
      lc.signature
    )

    const r4 = await veriCert.decryptFields(wallet, true, 'more cheese')
    expect(r4['name']).toBe('Alice')

    const certs = await wallet.listCertificates({ types: [], certifiers: [] })
    for (const cert of certs.certificates) {
      const rr = await wallet.relinquishCertificate({
        type: cert.type,
        serialNumber: cert.serialNumber,
        certifier: cert.certifier
      })
      expect(rr.relinquished).toBe(true)
    }

    // Also cleans up the privilegedKeyManager
    await wallet.destroy()
  })
```

### Python Test: py-wallet-toolbox/tests/wallet/test_certificates.py

```python
    def test_privileged_acquirecertificate_listcertificate_provecertificate(self, wallet_with_storage: Wallet) -> None:
        """Given: Wallet with privilegedKeyManager and certificate issued to privileged key
           When: acquireCertificate with privileged=True, proveCertificate with privileged=True
           Then: Certificate is stored, encrypted fields can be decrypted with privileged keyring

        Reference: wallet-toolbox/test/Wallet/certificate/acquireCertificate.test.ts
                   test('3 privileged acquireCertificate listCertificate proveCertificate')
        """
        # Given
        # Create test wallet with privilegedKeyManager
        wallet = Wallet(chain="test", priv_key_hex="42" * 32)

        # Certificate issued to the privileged key must use privilegedKeyManager's identityKey
        subject = wallet_with_storage.privileged_key_manager.get_public_key(identity_key=True)
        subject_key = subject["publicKey"]
        cert_data, certifier = _make_sample_cert(subject_key)

        # Act as the certifier: create a wallet for them
        certifier_wallet = _create_proto_wallet(certifier)

        # Create certificate and sign it
        cert = _create_certificate(cert_data)
        signed_fields = _create_certificate_fields(certifier_wallet, subject_key, cert["fields"])
        signed_cert = _create_signed_certificate(cert_data, signed_fields)
        _sign_certificate(signed_cert, certifier_wallet)

        # Prepare args object for privileged certificate
        args = {
            "serialNumber": signed_cert["serialNumber"],
            "signature": signed_cert["signature"],
            "privileged": True,
            "privilegedReason": "access to my penthouse",
            "type": signed_cert["type"],
            "certifier": signed_cert["certifier"],
            "acquisitionProtocol": "direct",
            "fields": signed_cert["fields"],
            "keyringForSubject": signed_fields["masterKeyring"],
            "keyringRevealer": "certifier",
            "revocationOutpoint": signed_cert["revocationOutpoint"],
        }

        # When
        # Store the privileged certificate
        result = wallet_with_storage.acquire_certificate(args)

        # Then
        assert result["serialNumber"] == signed_cert["serialNumber"]

        # Retrieve the certificate
        list_result = wallet_with_storage.list_certificates({"certifiers": [cert_data["certifier"]], "types": []})
        assert len(list_result["certificates"]) == 1
        lc = list_result["certificates"][0]

        # Fields should be encrypted
        assert lc["fields"]["name"] != "Alice"

        # Use proveCertificate with privileged=True
        prove_args = {
            "certificate": {"serialNumber": lc["serialNumber"]},
            "fieldsToReveal": ["name"],
            "verifier": subject_key,
            "privileged": True,
            "privilegedReason": "more cheese",
        }
        prove_result = wallet_with_storage.prove_certificate(prove_args)

        # Decrypt fields with privileged keyring
        verifiable_cert = _create_verifiable_certificate(lc, prove_result["keyringForVerifier"])
        decrypted = _decrypt_fields(verifiable_cert, wallet, privileged=True, privileged_reason="more cheese")
        assert decrypted["name"] == "Alice"

        # Cleanup: relinquish all certificates
        certs = wallet_with_storage.list_certificates({"types": [], "certifiers": []})
        for cert in certs["certificates"]:
            relinquish_result = wallet_with_storage.relinquish_certificate(
                {"type": cert["type"], "serialNumber": cert["serialNumber"], "certifier": cert["certifier"]}
            )
            assert relinquish_result["relinquished"] is True

        # Also cleans up the privilegedKeyManager
        wallet_with_storage.destroy()


# Helper functions for certificate testing (to be implemented with API)
```

### AI Analysis Results

**Similarity Score**: 17.14%
  - Structural: 0.00%
  - Semantic: 34.29%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: r.serialNumber, rr.relinquished
  - [HIGH] Python test is missing operations: veri_cert.decryptFields, signed_cert.sign, _tu.createSQLiteTestWallet, wallet.proveCertificate, wallet.listCertificates, wallet.relinquishCertificate, wallet.destroy, master_certificate.createCertificateFields, wallet.acquireCertificate

**Differences:**
  - Operation count: TS has 10, PY has 0
  - Verification count: TS has 2, PY has 5

**Suggestions:**
  - Add verifications for: r.serialNumber, rr.relinquished
  - Add operations: veri_cert.decryptFields, signed_cert.sign, _tu.createSQLiteTestWallet

**Explanation:**

Overall Similarity: 17.1%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 34.3% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification decryption verification encryption
  • Python: decryption verification encryption

Critical Issues (2):
  • [HIGH] Python test is missing verifications: r.serialNumber, rr.relinquished
  • [HIGH] Python test is missing operations: veri_cert.decryptFields, signed_cert.sign, _tu.createSQLiteTestWallet, wallet.proveCertificate, wallet.listCertificates, wallet.relinquishCertificate, wallet.destroy, master_certificate.createCertificateFields, wallet.acquireCertificate

Key Differences:
  • Operation count: TS has 10, PY has 0
  • Verification count: TS has 2, PY has 5

---

## Test 359: 0 invalid params **FAIL**

### TypeScript Test: wallet-toolbox/test/Wallet/get/getHeaderForHeight.test.ts

```typescript
  test('0 invalid params', async () => {
    for (const { wallet } of ctxs) {
      try {
        await wallet.getHeaderForHeight({ height: -1 })
        throw new Error('Expected error was not thrown')
      } catch (e) {
        const errorMessage = typeof e === 'object' && e !== null && 'message' in e ? (e as Error).message : String(e)
        expect(errorMessage).toMatch(/Height -1 must be a non-negative integer/i)
      }
    }
  })
```

### Python Test: py-wallet-toolbox/tests/wallet/test_certificates.py

```python
    def test_invalid_params(self, wallet_with_storage: Wallet) -> None:
        """Given: Wallet with test storage and invalid certificate arguments
           When: Call acquireCertificate with invalid params (empty type, empty certifier)
           Then: Raises InvalidParameterError

        Reference: wallet-toolbox/test/Wallet/certificate/acquireCertificate.test.ts
                   test('1 invalid params')
        """
        # Given
        # wallet = Wallet(chain="test")  # Not needed, using wallet_with_storage

        invalid_args = {"type": "", "certifier": "", "acquisitionProtocol": "direct", "fields": {}}

        # When/Then
        with pytest.raises(InvalidParameterError):
            wallet_with_storage.acquire_certificate(invalid_args)
```

### AI Analysis Results

**Similarity Score**: 30.00%
  - Structural: 0.00%
  - Semantic: 60.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  - [HIGH] Python test is missing operations: wallet.getHeaderForHeight

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'verification'
  - Add operations: wallet.getHeaderForHeight

**Explanation:**

Overall Similarity: 30.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 60.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification
  • Python: general_test

Critical Issues (2):
  • [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  • [HIGH] Python test is missing operations: wallet.getHeaderForHeight

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 360: 0 should return an empty array when no txids are provided **PASS**

- TypeScript: `wallet-toolbox/test/Wallet/get/getKnownTxids.test.ts`
- Python: `py-wallet-toolbox/tests/unit/test_wallet_getknowntxids.py`

---

## Test 361: 2 should avoid duplicating txids **PASS**

- TypeScript: `wallet-toolbox/test/Wallet/get/getKnownTxids.test.ts`
- Python: `py-wallet-toolbox/tests/unit/test_wallet_getknowntxids.py`

---

## Test 362: 4 should handle invalid txids gracefully **PASS**

- TypeScript: `wallet-toolbox/test/Wallet/get/getKnownTxids.test.ts`
- Python: `py-wallet-toolbox/tests/unit/test_wallet_getknowntxids.py`

---

## Test 363: should return the correct wallet version **PASS**

- TypeScript: `wallet-toolbox/test/Wallet/get/getVersion.test.ts`
- Python: `py-wallet-toolbox/tests/unit/test_wallet_getversion.py`

---

## Test 364: 0 invalid params **PASS**

- TypeScript: `wallet-toolbox/test/Wallet/list/listActions.test.ts`
- Python: `py-wallet-toolbox/tests/wallet/test_certificates.py`

---

## Test 365: 1 all actions **FAIL**

### TypeScript Test: wallet-toolbox/test/Wallet/list/listActions.test.ts

```typescript
  test('1 all actions', async () => {
    for (const { wallet } of ctxs) {
      {
        const args: ListActionsArgs = {
          includeLabels: true,
          labels: []
        }
        const r = await wallet.listActions(args)
        expect(r.totalActions).toBe(191)
        expect(r.actions.length).toBe(10)
        let i = 0
        for (const a of r.actions) {
          expect(a.inputs).toBeUndefined()
          expect(a.outputs).toBeUndefined()
          expect(Array.isArray(a.labels)).toBe(true)
        }
      }
    }
  })
```

### Python Test: py-wallet-toolbox/tests/wallet/test_list_actions.py

```python
    def test_all_actions(self, wallet_with_storage: Wallet) -> None:
        """Given: Wallet with existing actions
           When: Call list_actions with includeLabels=True
           Then: Returns paginated list of actions with labels

        Reference: wallet-toolbox/test/wallet/list/listActions.test.ts
                   test('1 all actions')

        Note: This test requires a populated test database.
        """
        # Given
        args = {"includeLabels": True, "labels": []}

        # When
        result = wallet_with_storage.list_actions(args)

        # Then
        assert "totalActions" in result
        assert "actions" in result
        assert isinstance(result["actions"], list)

        for action in result["actions"]:
            assert "inputs" not in action or action["inputs"] is None
            assert "outputs" not in action or action["outputs"] is None
            assert isinstance(action.get("labels"), list)
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: r.totalActions, a.inputs, a.outputs
  - [HIGH] Python test is missing operations: wallet.listActions

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 3, PY has 4

**Suggestions:**
  - Add verifications for: r.totalActions, a.inputs, a.outputs
  - Add operations: wallet.listActions

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: r.totalActions, a.inputs, a.outputs
  • [HIGH] Python test is missing operations: wallet.listActions

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 3, PY has 4

---

## Test 366: 2 non-existing label with any **FAIL**

### TypeScript Test: wallet-toolbox/test/Wallet/list/listActions.test.ts

```typescript
  test('2 non-existing label with any', async () => {
    for (const { wallet } of ctxs) {
      {
        const args: ListActionsArgs = {
          includeLabels: true,
          labels: ['xyzzy'],
          labelQueryMode: 'any'
        }
        const r = await wallet.listActions(args)
        expect(r.totalActions).toBe(0)
        expect(r.actions.length).toBe(0)
      }
    }
  })
```

### Python Test: py-wallet-toolbox/tests/wallet/test_list_actions.py

```python
    def test_non_existing_label_with_any(self, wallet_with_storage: Wallet) -> None:
        """Given: Wallet and non-existing label
           When: Call list_actions with labelQueryMode='any'
           Then: Returns empty result

        Reference: wallet-toolbox/test/wallet/list/listActions.test.ts
                   test('2 non-existing label with any')

        Note: This test requires a populated test database.
        """
        # Given
        args = {"includeLabels": True, "labels": ["xyzzy"], "labelQueryMode": "any"}  # Non-existing label

        # When
        result = wallet_with_storage.list_actions(args)

        # Then
        assert result["totalActions"] == 0
        assert len(result["actions"]) == 0
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: r.totalActions
  - [HIGH] Python test is missing operations: wallet.listActions

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 1, PY has 2

**Suggestions:**
  - Add verifications for: r.totalActions
  - Add operations: wallet.listActions

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: r.totalActions
  • [HIGH] Python test is missing operations: wallet.listActions

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 1, PY has 2

---

## Test 367: 0 invalid params **PASS**

- TypeScript: `wallet-toolbox/test/Wallet/list/listCertificates.test.ts`
- Python: `py-wallet-toolbox/tests/wallet/test_certificates.py`

---

## Test 368: 0 invalid params with originator **FAIL**

### TypeScript Test: wallet-toolbox/test/Wallet/list/listOutputs.test.ts

```typescript
  test('0 invalid params with originator', async () => {
    for (const { wallet } of ctxs) {
      const invalidArgs: ListOutputsArgs[] = [
        { basket: 'default', tags: [] },
        { basket: '' as BasketStringUnder300Bytes },
        { basket: '   ' as BasketStringUnder300Bytes },
        { basket: 'default', tags: [''] as OutputTagStringUnder300Bytes[] },
        { basket: 'default', limit: 0 },
        { basket: 'default', limit: -1 },
        { basket: 'default', limit: 10001 },
        { basket: 'default', offset: -1 }
        // Removed cases with problematic offsets
      ].filter(args => args.basket !== '') // Remove cases causing the failure

      const invalidOriginators = [
        'too.long.invalid.domain.'.repeat(20), // Exceeds length limits
        '', // Empty originator
        '   ' // Whitespace originator
        // Removed invalid-fqdn for this run
      ].filter(originator => originator.trim() !== '') // Remove problematic cases

      for (const args of invalidArgs) {
        for (const originator of invalidOriginators) {
          try {
            await wallet.listOutputs(args, originator as OriginatorDomainNameStringUnder250Bytes)
            throw new Error('Expected method to throw.')
          } catch (e) {
            const error = e as Error
            if (error.name != 'WERR_INVALID_PARAMETER') debugger

            // Validate error
            expect(error.name).toBe('WERR_INVALID_PARAMETER')
          }
        }
      }
    }
  })
```

### Python Test: py-wallet-toolbox/tests/wallet/test_list_outputs.py

```python
    def test_valid_params_with_originator(self, wallet_with_storage: Wallet) -> None:
        """Given: Valid ListOutputsArgs and valid originator
           When: Call list_outputs
           Then: Returns output list successfully

        Reference: wallet-toolbox/test/wallet/list/listOutputs.test.ts
                   test('1 valid params with originator')

        Note: This test requires a populated test database.
        """
        # Given
        valid_args = {
            "basket": "default",
            "tags": ["tag1", "tag2"],
            "limit": 10,
            "offset": 0,
            "tagQueryMode": "any",
            "include": "locking scripts",
            "includeCustomInstructions": False,
            "includeTags": True,
            "includeLabels": True,
            "seekPermission": True,
        }
        valid_originators = ["example.com", "localhost", "subdomain.example.com"]

        # When / Then
        for originator in valid_originators:
            result = wallet_with_storage.list_outputs(valid_args, originator=originator)
            assert "totalOutputs" in result
            assert result["totalOutputs"] >= 0
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: error.name
  - [HIGH] Python test is missing operations: wallet.listOutputs

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: error.name
  - Add operations: wallet.listOutputs

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: error.name
  • [HIGH] Python test is missing operations: wallet.listOutputs

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 369: 1 valid params with originator **FAIL**

### TypeScript Test: wallet-toolbox/test/Wallet/list/listOutputs.test.ts

```typescript
  test('1 valid params with originator', async () => {
    for (const { wallet } of ctxs) {
      const validArgs: ListOutputsArgs = {
        basket: 'default' as BasketStringUnder300Bytes,
        tags: ['tag1', 'tag2'] as OutputTagStringUnder300Bytes[],
        limit: 10,
        offset: 0,
        tagQueryMode: 'any',
        include: 'locking scripts',
        includeCustomInstructions: false,
        includeTags: true,
        includeLabels: true,
        seekPermission: true
      }

      const validOriginators = ['example.com', 'localhost', 'subdomain.example.com']

      for (const originator of validOriginators) {
        const result = await wallet.listOutputs(validArgs, originator as OriginatorDomainNameStringUnder250Bytes)
        expect(result.totalOutputs).toBeGreaterThanOrEqual(0)
      }
    }
  })
```

### Python Test: py-wallet-toolbox/tests/wallet/test_list_outputs.py

```python
    def test_valid_params_with_originator(self, wallet_with_storage: Wallet) -> None:
        """Given: Valid ListOutputsArgs and valid originator
           When: Call list_outputs
           Then: Returns output list successfully

        Reference: wallet-toolbox/test/wallet/list/listOutputs.test.ts
                   test('1 valid params with originator')

        Note: This test requires a populated test database.
        """
        # Given
        valid_args = {
            "basket": "default",
            "tags": ["tag1", "tag2"],
            "limit": 10,
            "offset": 0,
            "tagQueryMode": "any",
            "include": "locking scripts",
            "includeCustomInstructions": False,
            "includeTags": True,
            "includeLabels": True,
            "seekPermission": True,
        }
        valid_originators = ["example.com", "localhost", "subdomain.example.com"]

        # When / Then
        for originator in valid_originators:
            result = wallet_with_storage.list_outputs(valid_args, originator=originator)
            assert "totalOutputs" in result
            assert result["totalOutputs"] >= 0
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: result.totalOutputs
  - [HIGH] Python test is missing operations: wallet.listOutputs

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: result.totalOutputs
  - Add operations: wallet.listOutputs

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: result.totalOutputs
  • [HIGH] Python test is missing operations: wallet.listOutputs

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 370: 00 **FAIL**

### TypeScript Test: wallet-toolbox/test/Wallet/local/localWallet.man.test.ts

```typescript
describe('localWallet tests', () => {
  jest.setTimeout(99999999)

  //  test('00', () => {})
  //  if (_tu.noTestEnv(chain)) return

  test('0 monitor runOnce', async () => {
    const setup = await createSetup(chain, options)
    const key = await setup.wallet.getPublicKey({ identityKey: true })
    expect(key.publicKey.toString()).toBe(setup.identityKey)
    await setup.monitor.runOnce()
    await setup.wallet.destroy()
  })

  test('0a monitor runOnce call history', async () => {
    const setup = await createSetup(chain, options)
    const key = await setup.wallet.getPublicKey({ identityKey: true })
    expect(key.publicKey.toString()).toBe(setup.identityKey)
    await setup.services.getRawTx('6dd8e416dfaf14c04899ccad2bf76a67c1d5598fece25cf4dcb7a076012b7d8d')
    await setup.services.getRawTx('ac9cced61e2491be55061ce6577e0c59b909922ba92d5cc1cd754b10d721ab0e')
    await setup.monitor.runOnce()
    await setup.services.getRawTx('0000e416dfaf14c04899ccad2bf76a67c1d5598fece25cf4dcb7a076012b7d8d')
    await setup.services.getRawTx('0000ced61e2491be55061ce6577e0c59b909922ba92d5cc1cd754b10d721ab0e')
    logger(await setup.monitor.runTask('MonitorCallHistory'))
    await setup.wallet.destroy()
  })

  test('2 create 1 sat delayed', async () => {
    const setup = await createSetup(chain, options)
    const car = await createOneSatTestOutput(setup, {}, 1)
    //await trackReqByTxid(setup, car.txid!)
    await setup.wallet.destroy()
  })

  test('2a create 1 sat immediate', async () => {
    const setup = await createSetup(chain, options)
    const car = await createOneSatTestOutput(setup, { acceptDelayedBroadcast: false }, 1)
    // await trackReqByTxid(setup, car.txid!)
    await setup.wallet.destroy()
  })

  test('2b create 2 nosend and sendWith', async () => {
    const setup = await createSetup(chain, options)
    const car = await createOneSatTestOutput(setup, { noSend: true }, 2)
    //await trackReqByTxid(setup, car.txid!)
    await setup.wallet.destroy()
  })

  test('3 return active to cloud client', async () => {
    const setup = await createSetup(chain, options)
    const localBalance = await setup.wallet.balance()
    const log = await setup.storage.setActive(setup.clientStorageIdentityKey!)
    console.log(log)
    console.log(`ACTIVE STORAGE: ${setup.storage.getActiveStoreName()}`)
    const clientBalance = await setup.wallet.balance()
    expect(localBalance).toBe(clientBalance)
    await setup.wallet.destroy()
  })

  test('5 review synchunk', async () => {
    const setup = await createSetup(chain, options)
    const identityKey = setup.identityKey
    const reader = setup.activeStorage
    const readerSettings = reader.getSettings()
    const writer = setup.storage._backups![0].storage
    const writerSettings = writer.getSettings()
    const ss = await EntitySyncState.fromStorage(writer, identityKey, readerSettings)
    const args = ss.makeRequestSyncChunkArgs(identityKey, writerSettings.storageIdentityKey)
    const chunk = await reader.getSyncChunk(args)
    await setup.wallet.destroy()
  })

  test('6 backup', async () => {
    const setup = await createSetup(chain, options)
    const log = await setup.storage.updateBackups()
    console.log(log)
    await setup.wallet.destroy()
  })
})
```

### Python Test: py-wallet-toolbox/tests/wallet/test_certificates.py

```python
    def test_00(self, wallet_with_storage: Wallet) -> None:
        """Given: No operation
           When: Test placeholder
           Then: Pass

        Reference: wallet-toolbox/test/Wallet/certificate/acquireCertificate.test.ts
                   test('00')
        """
        # Given/When/Then
```

### AI Analysis Results

**Similarity Score**: 30.00%
  - Structural: 0.00%
  - Semantic: 60.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  - [HIGH] Python test is missing operations: reader.getSyncChunk, entity_sync_state.fromStorage

**Differences:**
  - Operation count: TS has 2, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'verification'
  - Add operations: reader.getSyncChunk, entity_sync_state.fromStorage

**Explanation:**

Overall Similarity: 30.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 60.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification
  • Python: general_test

Critical Issues (2):
  • [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  • [HIGH] Python test is missing operations: reader.getSyncChunk, entity_sync_state.fromStorage

Key Differences:
  • Operation count: TS has 2, PY has 0

---

## Test 371: 00 **PASS**

- TypeScript: `wallet-toolbox/test/Wallet/specOps/specOps.man.test.ts`
- Python: `py-wallet-toolbox/tests/wallet/test_certificates.py`

---

## Test 372: 1a setActive to backup and back to original without backup first **FAIL**

### TypeScript Test: wallet-toolbox/test/Wallet/sync/Wallet.sync.test.ts

```typescript
  test('1a setActive to backup and back to original without backup first', async () => {
    // wallet will be the original active wallet, a backup is added, then setActive is used to initiate backup in each direction.
    const ctx = await _tu.createLegacyWalletSQLiteCopy('walletSyncTest1aSource')
    const { activeStorage: backup, wallet: backupWallet } = await _tu.createSQLiteTestWallet({
      databaseName: 'walletSyncTest1aBackup',
      rootKeyHex: ctx.rootKey.toHex(),
      dropAll: true
    })
    await ctx.storage.addWalletStorageProvider(backup)

    await setActiveTwice(ctx, false, backup, backupWallet)

    await setActiveTwice(ctx, false, backup, backupWallet)

    await ctx.storage.destroy()
  })
```

### Python Test: py-wallet-toolbox/tests/wallet/test_sync.py

```python
    def test_set_active_to_backup_and_back_without_backup_first(
        self, _wallet: Wallet, backup_storage, original_storage
    ) -> None:
        """Given: Original wallet and empty backup storage
           When: Call set_active to switch to backup and back to original (twice)
           Then: Data is synced correctly in both directions

        Reference: wallet-toolbox/test/wallet/sync/Wallet.sync.test.ts
                   test('1a setActive to backup and back to original without backup first')

        Note: This test requires:
        - Original wallet with data
        - Empty backup storage
        - Multiple setActive calls to verify bidirectional sync
        """
        # Given
        # Original wallet is active
        # Backup storage is empty

        # When - Switch to backup (first time)
        _wallet.set_active(backup_storage)

        # Then
        # Backup should now have all data from original

        # When - Switch back to original
        _wallet.set_active(original_storage)

        # Then
        # Original should remain unchanged (no new data in backup)

        # When - Repeat the process
        _wallet.set_active(backup_storage)
        _wallet.set_active(original_storage)

        # Then
        # Should complete successfully with no errors
```

### AI Analysis Results

**Similarity Score**: 30.00%
  - Structural: 0.00%
  - Semantic: 60.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'authentication' but PY verifies 'general_test'
  - [HIGH] Python test is missing operations: _tu.createLegacyWalletSQLiteCopy, _tu.createSQLiteTestWallet

**Differences:**
  - Operation count: TS has 2, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'authentication'
  - Add operations: _tu.createLegacyWalletSQLiteCopy, _tu.createSQLiteTestWallet

**Explanation:**

Overall Similarity: 30.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 60.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: authentication
  • Python: general_test

Critical Issues (2):
  • [HIGH] Test intent differs: TS verifies 'authentication' but PY verifies 'general_test'
  • [HIGH] Python test is missing operations: _tu.createLegacyWalletSQLiteCopy, _tu.createSQLiteTestWallet

Key Differences:
  • Operation count: TS has 2, PY has 0

---

## Test 373: 1b setActive to backup and back to original with backup first **FAIL**

### TypeScript Test: wallet-toolbox/test/Wallet/sync/Wallet.sync.test.ts

```typescript
  test('1b setActive to backup and back to original with backup first', async () => {
    // wallet will be the original active wallet, a backup is added, then setActive is used to initiate backup in each direction.
    const ctx = await _tu.createLegacyWalletSQLiteCopy('walletSyncTest1bSource')
    const backup = (
      await _tu.createSQLiteTestWallet({
        databaseName: 'walletSyncTest1bBackup',
        dropAll: true
      })
    ).activeStorage
    await ctx.storage.addWalletStorageProvider(backup)

    await setActiveTwice(ctx, true, backup)

    await setActiveTwice(ctx, true, backup)

    await ctx.storage.destroy()
  })
```

### Python Test: py-wallet-toolbox/tests/wallet/test_sync.py

```python
    def test_set_active_to_backup_and_back_with_backup_first(
        self, _wallet: Wallet, backup_storage, original_storage
    ) -> None:
        """Given: Original wallet and backup that was initialized with backup_first=True
           When: Call set_active to switch to backup and back to original (twice)
           Then: Data is synced correctly with backup-first semantics

        Reference: wallet-toolbox/test/wallet/sync/Wallet.sync.test.ts
                   test('1b setActive to backup and back to original with backup first')

        Note: This test requires:
        - Original wallet with data
        - Backup storage initialized with backup_first flag
        - Multiple setActive calls to verify backup-first behavior
        """
        # Given
        # Original wallet is active
        # Backup storage initialized with backup_first=True

        # When - Switch to backup (first time)
        _wallet.set_active(backup_storage, backup_first=True)

        # Then
        # Backup-first semantics applied

        # When - Switch back to original
        _wallet.set_active(original_storage)

        # Then
        # Original updated from backup if needed

        # When - Repeat the process
        _wallet.set_active(backup_storage, backup_first=True)
        _wallet.set_active(original_storage)

        # Then
        # Should complete successfully with backup-first semantics maintained
```

### AI Analysis Results

**Similarity Score**: 30.00%
  - Structural: 0.00%
  - Semantic: 60.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'authentication' but PY verifies 'general_test'
  - [HIGH] Python test is missing operations: _tu.createLegacyWalletSQLiteCopy, _tu.createSQLiteTestWallet

**Differences:**
  - Operation count: TS has 2, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'authentication'
  - Add operations: _tu.createLegacyWalletSQLiteCopy, _tu.createSQLiteTestWallet

**Explanation:**

Overall Similarity: 30.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 60.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: authentication
  • Python: general_test

Critical Issues (2):
  • [HIGH] Test intent differs: TS verifies 'authentication' but PY verifies 'general_test'
  • [HIGH] Python test is missing operations: _tu.createLegacyWalletSQLiteCopy, _tu.createSQLiteTestWallet

Key Differences:
  • Operation count: TS has 2, PY has 0

---

## Test 374: 0 get non-existent **PASS**

- TypeScript: `wallet-toolbox/test/bsv-ts-sdk/LocalKVStore.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_local_kv_store.py`

---

## Test 375: 1 set get **PASS**

- TypeScript: `wallet-toolbox/test/bsv-ts-sdk/LocalKVStore.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_local_kv_store.py`

---

## Test 376: 3 set x 4 get **PASS**

- TypeScript: `wallet-toolbox/test/bsv-ts-sdk/LocalKVStore.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_local_kv_store.py`

---

## Test 377: 5 set x 4 get set x 4 get **PASS**

- TypeScript: `wallet-toolbox/test/bsv-ts-sdk/LocalKVStore.test.ts`
- Python: `py-wallet-toolbox/tests/integration/test_local_kv_store.py`

---

## Test 378: 0 TaskClock **PASS**

- TypeScript: `wallet-toolbox/test/monitor/Monitor.test.ts`
- Python: `py-wallet-toolbox/tests/monitor/test_monitor.py`

---

## Test 379: 1 TaskNewHeader **FAIL**

### TypeScript Test: wallet-toolbox/test/monitor/Monitor.test.ts

```typescript
  test('1 TaskNewHeader', async () => {
    if (!env.runSlowTests) return

    // This test takes 10+ seconds to run... un-skip it to work on it.
    for (const { chain, wallet, services, monitor } of ctxs) {
      if (!monitor) throw new sdk.WERR_INTERNAL('test requires setup with monitor')

      {
        // The new header task polls chaintracks for latest header and if new sets flag to check for proofs.
        // Starting the clock and waiting a bit should cause first header to be fetched and flag to be set.
        const task = new TaskNewHeader(monitor)
        monitor._tasks.push(task)
        expect(TaskCheckForProofs.checkNow).toBe(false)
        const startTasksPromise = monitor.startTasks()
        await wait(monitor.oneSecond * 10)
        expect(task.header).toBeTruthy()
        expect(TaskCheckForProofs.checkNow).toBe(true)
        monitor.stopTasks()
        await startTasksPromise
      }
    }
  })
```

### Python Test: py-wallet-toolbox/tests/monitor/test_monitor.py

```python
    def test_tasknewheader(self) -> None:
        """Given: Monitor with new header task running for 10+ seconds
           When: Check header and checkNow flag
           Then: Latest header is fetched and checkNow flag is set

        Reference: wallet-toolbox/test/monitor/Monitor.test.ts
                   test('1 TaskNewHeader')
        """
        # Given
        ctx = create_sqlite_test_setup_1_wallet(database_name="walletMonitorMain", chain="main", root_key_hex="3" * 64)

        monitor = ctx.monitor
        if monitor is None:
            raise ValueError("test requires setup with monitor")

        # When
        task = TaskNewHeader(monitor)
        monitor._tasks.append(task)
        assert TaskCheckForProofs.check_now is False

        start_tasks_promise = monitor.start_tasks()
        asyncio.sleep(Monitor.ONE_SECOND * 10)

        # Then
        assert task.header is not None
        assert TaskCheckForProofs.check_now is True

        monitor.stop_tasks()
        start_tasks_promise
        ctx.storage.destroy()
```

### AI Analysis Results

**Similarity Score**: 58.33%
  - Structural: 0.00%
  - Semantic: 56.67%
  - Alignment: 100.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: task_check_for_proofs.checkNow, task.header

**Suggestions:**
  - Add verifications for: task_check_for_proofs.checkNow, task.header

**Explanation:**

Overall Similarity: 58.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 56.7% (test intent and meaning)
  • Alignment: 100.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing verifications: task_check_for_proofs.checkNow, task.header

---

## Test 380: 3 TaskSendWaiting success **PASS**

- TypeScript: `wallet-toolbox/test/monitor/Monitor.test.ts`
- Python: `py-wallet-toolbox/tests/monitor/test_monitor.py`

---

## Test 381: 5 TaskCheckForProofs success **PASS**

- TypeScript: `wallet-toolbox/test/monitor/Monitor.test.ts`
- Python: `py-wallet-toolbox/tests/monitor/test_monitor.py`

---

## Test 382: 6 TaskCheckForProofs fail **PASS**

- TypeScript: `wallet-toolbox/test/monitor/Monitor.test.ts`
- Python: `py-wallet-toolbox/tests/monitor/test_monitor.py`

---

## Test 383: 7 TaskReviewStatus **FAIL**

### TypeScript Test: wallet-toolbox/test/monitor/Monitor.test.ts

```typescript
  test('7 TaskReviewStatus', async () => {
    const ctxs: TestWallet<{}>[] = []
    ctxs.push(await _tu.createLegacyWalletSQLiteCopy('monitorTest7'))
    //ctxs.push(await _tu.createLegacyWalletMySQLCopy('monitorTest7'))

    for (const { activeStorage: storage, monitor } of ctxs) {
      const reqs = await storage.findProvenTxReqs({
        partial: { status: 'unmined' }
      })
      const crus = await storage.updateProvenTxReq(reqs[0].provenTxReqId, {
        status: 'invalid'
      })
      const ctus = await storage.updateTransaction(23, {
        provenTxId: undefined
      })

      const task = new TaskReviewStatus(monitor, 1, 1000 * 5)
      monitor._tasks.push(task)
      const log = await monitor.runTask('ReviewStatus')
      //console.log(log)
    }

    for (const ctx of ctxs) {
      await ctx.storage.destroy()
    }
  })
```

### Python Test: py-wallet-toolbox/tests/monitor/test_monitor.py

```python
    def test_taskreviewstatus(self) -> None:
        """Given: Storage with various transaction statuses including invalid ProvenTxReq
           When: Execute TaskReviewStatus
           Then: Transaction statuses are reviewed and corrected

        Reference: wallet-toolbox/test/monitor/Monitor.test.ts
                   test('7 TaskReviewStatus')
        """
        # Given
        ctx = create_legacy_wallet_sqlite_copy("monitorTest7")
        storage = ctx.active_storage
        monitor = ctx.monitor

        if monitor is None:
            raise ValueError("test requires setup with monitor")

        # Setup: mark one as invalid, unlink provenTxId
        reqs = storage.find_proven_tx_reqs({"partial": {"status": "unmined"}})
        storage.update_proven_tx_req(reqs[0].proven_tx_req_id, {"status": "invalid"})
        storage.update_transaction(23, {"provenTxId": None})

        # When
        task = TaskReviewStatus(monitor, 1, 5000)
        monitor._tasks.append(task)
        log = monitor.run_task("ReviewStatus")

        # Then
        assert log is not None

        ctx.storage.destroy()
```

### AI Analysis Results

**Similarity Score**: 30.00%
  - Structural: 0.00%
  - Semantic: 60.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'general_test' but PY verifies 'verification'
  - [HIGH] Python test is missing operations: storage.findProvenTxReqs, monitor.runTask, _tu.createLegacyWalletSQLiteCopy, storage.updateProvenTxReq, storage.updateTransaction, _tu.createLegacyWalletMySQLCopy

**Differences:**
  - Operation count: TS has 6, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'general_test'
  - Add operations: storage.findProvenTxReqs, monitor.runTask, _tu.createLegacyWalletSQLiteCopy

**Explanation:**

Overall Similarity: 30.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 60.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: general_test
  • Python: verification

Critical Issues (2):
  • [HIGH] Test intent differs: TS verifies 'general_test' but PY verifies 'verification'
  • [HIGH] Python test is missing operations: storage.findProvenTxReqs, monitor.runTask, _tu.createLegacyWalletSQLiteCopy, storage.updateProvenTxReq, storage.updateTransaction, _tu.createLegacyWalletMySQLCopy

Key Differences:
  • Operation count: TS has 6, PY has 0

---

## Test 384: 8 ProcessProvenTransaction **FAIL**

### TypeScript Test: wallet-toolbox/test/monitor/Monitor.test.ts

```typescript
  test('8 ProcessProvenTransaction', async () => {
    const ctxs: TestWallet<{}>[] = []
    ctxs.push(await _tu.createLegacyWalletSQLiteCopy('monitorTest8'))
    let mockResultIndex = 0
    let updatesReceived = 0

    const expectedTxids = [
      'c099c52277426abb863dc902d0389b008ddf2301d6b40ac718746ac16ca59136',
      '6935ce33b9e3b9ee60360ce0606aa0a0970b4840203f457b5559212676dc33ab',
      '67ca2475886b3fc2edd76a2eb8c32bd0bc308176c7dff463e0507942aeebcbec',
      '3fa94b62a3b10d8c18bada527a9b68c4e70db67140719df16c44fb0328782532',
      '519675259eff036c6597e4a497d37c132e718171dde4ea2257e84c947ecf656b'
    ]

    _tu.mockMerklePathServicesAsCallback(ctxs, async txid => {
      expect(expectedTxids).toContain(txid)
      const r = mockGetMerklePathResults[mockResultIndex++]
      return r
    })

    for (const { activeStorage: storage, monitor } of ctxs) {
      if (!monitor) throw new sdk.WERR_INTERNAL('test requires setup with monitor')

      monitor.lastNewHeader = {
        height: 999999999,
        hash: '',
        time: 0,
        version: 0,
        previousHash: '',
        merkleRoot: '',
        bits: 0,
        nonce: 0
      }

      monitor.onTransactionProven = async (txStatus: sdk.ProvenTransactionStatus) => {
        expect(txStatus.txid).toBeTruthy()
        expect(txStatus.blockHash).toBeTruthy()
        expect(txStatus.blockHeight).toBeTruthy()
        expect(txStatus.merkleRoot).toBeTruthy()
        updatesReceived++
      }

      for (const txid of expectedTxids) {
        // no matching ProvenTx exists.
        expect((await storage.findProvenTxs({ partial: { txid } })).length).toBe(0)
        const req = verifyTruthy(await EntityProvenTxReq.fromStorageTxid(storage, txid))
        expect(req.status).toBe('unmined')
      }

      const task = new TaskCheckForProofs(monitor, 1)
      monitor._tasks.push(task)

      await monitor.runTask('CheckForProofs')

      for (const txid of expectedTxids) {
        const proven = verifyOne(await storage.findProvenTxs({ partial: { txid } }))
        expect(proven.merklePath).toBeTruthy()
        const req = verifyTruthy(await EntityProvenTxReq.fromStorageTxid(storage, txid))
        expect(req.status).toBe('completed')
        expect(req.provenTxId).toBe(proven.provenTxId)
      }

      expect(updatesReceived).toEqual(expectedTxids.length)
    }

    for (const ctx of ctxs) {
      await ctx.storage.destroy()
    }
  })
```

### Python Test: py-wallet-toolbox/tests/monitor/test_monitor.py

```python
    def test_processproventransaction(self) -> None:
        """Given: Storage with unmined ProvenTxReqs and onTransactionProven callback
           When: Execute TaskCheckForProofs to create ProvenTxs
           Then: onTransactionProven callback is invoked for each proven transaction

        Reference: wallet-toolbox/test/monitor/Monitor.test.ts
                   test('8 ProcessProvenTransaction')
        """
        # Given
        ctx = create_legacy_wallet_sqlite_copy("monitorTest8")
        storage = ctx.active_storage
        monitor = ctx.monitor

        if monitor is None:
            raise ValueError("test requires setup with monitor")

        expected_txids = [
            "c099c52277426abb863dc902d0389b008ddf2301d6b40ac718746ac16ca59136",
            "6935ce33b9e3b9ee60360ce0606aa0a0970b4840203f457b5559212676dc33ab",
            "67ca2475886b3fc2edd76a2eb8c32bd0bc308176c7dff463e0507942aeebcbec",
            "3fa94b62a3b10d8c18bada527a9b68c4e70db67140719df16c44fb0328782532",
            "519675259eff036c6597e4a497d37c132e718171dde4ea2257e84c947ecf656b",
        ]

        mock_result_index = 0

        async def merkle_path_callback(txid: str):
            nonlocal mock_result_index
            assert txid in expected_txids
            result = MOCK_MERKLE_PATH_RESULTS[mock_result_index]
            mock_result_index += 1
            return result

        mock_merkle_path_services_as_callback([ctx], merkle_path_callback)

        monitor.last_new_header = {
            "height": 999999999,
            "hash": "",
            "time": 0,
            "version": 0,
            "previousHash": "",
            "merkleRoot": "",
            "bits": 0,
            "nonce": 0,
        }

        updates_received = 0

        async def on_transaction_proven(tx_status) -> None:
            nonlocal updates_received
            assert tx_status["txid"] is not None
            assert tx_status["blockHash"] is not None
            assert tx_status["blockHeight"] is not None
            assert tx_status["merkleRoot"] is not None
            updates_received += 1

        monitor.on_transaction_proven = on_transaction_proven

        # Verify initial state
        for txid in expected_txids:
            proven_txs = storage.find_proven_txs({"partial": {"txid": txid}})
            assert len(proven_txs) == 0

            req = EntityProvenTxReq.from_storage_txid(storage, txid)
            assert req is not None
            assert req.status == "unmined"

        # When
        task = TaskCheckForProofs(monitor, 1)
        monitor._tasks.append(task)
        monitor.run_task("CheckForProofs")

        # Then
        for txid in expected_txids:
            proven = (storage.find_proven_txs({"partial": {"txid": txid}}))[0]
            assert proven.merkle_path is not None

            req = EntityProvenTxReq.from_storage_txid(storage, txid)
            assert req is not None
            assert req.status == "completed"
            assert req.proven_tx_id == proven.proven_tx_id

        assert updates_received == len(expected_txids)

        ctx.storage.destroy()
```

### AI Analysis Results

**Similarity Score**: 30.48%
  - Structural: 0.00%
  - Semantic: 60.95%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: tx_status.txid, req.status, tx_status.blockHash, tx_status.merkleRoot, proven.merklePath, tx_status.blockHeight, req.provenTxId
  - [HIGH] Python test is missing operations: _tu.createLegacyWalletSQLiteCopy, entity_proven_tx_req.fromStorageTxid, monitor.runTask, storage.findProvenTxs

**Differences:**
  - Operation count: TS has 6, PY has 0

**Suggestions:**
  - Add verifications for: tx_status.txid, req.status, tx_status.blockHash
  - Add operations: _tu.createLegacyWalletSQLiteCopy, entity_proven_tx_req.fromStorageTxid, monitor.runTask

**Explanation:**

Overall Similarity: 30.5%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 61.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: tx_status.txid, req.status, tx_status.blockHash, tx_status.merkleRoot, proven.merklePath, tx_status.blockHeight, req.provenTxId
  • [HIGH] Python test is missing operations: _tu.createLegacyWalletSQLiteCopy, entity_proven_tx_req.fromStorageTxid, monitor.runTask, storage.findProvenTxs

Key Differences:
  • Operation count: TS has 6, PY has 0

---

## Test 385: 9 ProcessBroadcastedTransactions **PASS**

- TypeScript: `wallet-toolbox/test/monitor/Monitor.test.ts`
- Python: `py-wallet-toolbox/tests/monitor/test_monitor.py`

---

## Test 386: 4 getMerklePath **PASS**

- TypeScript: `wallet-toolbox/test/services/Services.test.ts`
- Python: `py-wallet-toolbox/tests/services/test_get_merkle_path.py`

---

## Test 387: 5 getRawTx **PASS**

- TypeScript: `wallet-toolbox/test/services/Services.test.ts`
- Python: `py-wallet-toolbox/tests/services/test_get_raw_tx.py`

---

## Test 388: 0 count ProvenTx **PASS**

- TypeScript: `wallet-toolbox/test/storage/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 389: 1 count ProvenTxReq **PASS**

- TypeScript: `wallet-toolbox/test/storage/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 390: 10 count OutputTagMap **PASS**

- TypeScript: `wallet-toolbox/test/storage/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 391: 11 count TxLabel **PASS**

- TypeScript: `wallet-toolbox/test/storage/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 392: 12 count TxLabelMap **PASS**

- TypeScript: `wallet-toolbox/test/storage/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 393: 13 count MonitorEvent **PASS**

- TypeScript: `wallet-toolbox/test/storage/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 394: 14 count SyncState **PASS**

- TypeScript: `wallet-toolbox/test/storage/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 395: 2 count User **PASS**

- TypeScript: `wallet-toolbox/test/storage/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 396: 3 count Certificate **PASS**

- TypeScript: `wallet-toolbox/test/storage/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 397: 4 count CertificateField **PASS**

- TypeScript: `wallet-toolbox/test/storage/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 398: 5 count OutputBasket **PASS**

- TypeScript: `wallet-toolbox/test/storage/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 399: 6 count Transaction **PASS**

- TypeScript: `wallet-toolbox/test/storage/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 400: 7 count Commission **PASS**

- TypeScript: `wallet-toolbox/test/storage/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 401: 8 count Output **PASS**

- TypeScript: `wallet-toolbox/test/storage/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 402: 9 count OutputTag **PASS**

- TypeScript: `wallet-toolbox/test/storage/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 403: 0 find ProvenTx **PASS**

- TypeScript: `wallet-toolbox/test/storage/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find.py`

---

## Test 404: 1 find ProvenTxReq **PASS**

- TypeScript: `wallet-toolbox/test/storage/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find.py`

---

## Test 405: 10 find OutputTagMap **PASS**

- TypeScript: `wallet-toolbox/test/storage/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 406: 11 find TxLabel **PASS**

- TypeScript: `wallet-toolbox/test/storage/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 407: 12 find TxLabelMap **PASS**

- TypeScript: `wallet-toolbox/test/storage/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 408: 13 find MonitorEvent **PASS**

- TypeScript: `wallet-toolbox/test/storage/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 409: 14 find SyncState **PASS**

- TypeScript: `wallet-toolbox/test/storage/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 410: 2 find User **PASS**

- TypeScript: `wallet-toolbox/test/storage/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 411: 3 find Certificate **PASS**

- TypeScript: `wallet-toolbox/test/storage/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 412: 4 find CertificateField **PASS**

- TypeScript: `wallet-toolbox/test/storage/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find.py`

---

## Test 413: 5 find OutputBasket **PASS**

- TypeScript: `wallet-toolbox/test/storage/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find.py`

---

## Test 414: 6 find Transaction **PASS**

- TypeScript: `wallet-toolbox/test/storage/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 415: 7 find Commission **PASS**

- TypeScript: `wallet-toolbox/test/storage/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 416: 8 find Output **PASS**

- TypeScript: `wallet-toolbox/test/storage/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 417: 9 find OutputTag **PASS**

- TypeScript: `wallet-toolbox/test/storage/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 418: 0 find ProvenTx **PASS**

- TypeScript: `wallet-toolbox/test/storage/findLegacy.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find.py`

---

## Test 419: 1 find ProvenTxReq **PASS**

- TypeScript: `wallet-toolbox/test/storage/findLegacy.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find.py`

---

## Test 420: 10 find OutputTagMap **PASS**

- TypeScript: `wallet-toolbox/test/storage/findLegacy.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 421: 11 find TxLabel **PASS**

- TypeScript: `wallet-toolbox/test/storage/findLegacy.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 422: 12 find TxLabelMap **PASS**

- TypeScript: `wallet-toolbox/test/storage/findLegacy.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 423: 13 find MonitorEvent **PASS**

- TypeScript: `wallet-toolbox/test/storage/findLegacy.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 424: 14 find SyncState **PASS**

- TypeScript: `wallet-toolbox/test/storage/findLegacy.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 425: 2 find User **PASS**

- TypeScript: `wallet-toolbox/test/storage/findLegacy.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 426: 3 find Certificate **PASS**

- TypeScript: `wallet-toolbox/test/storage/findLegacy.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 427: 4 find CertificateField **PASS**

- TypeScript: `wallet-toolbox/test/storage/findLegacy.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find.py`

---

## Test 428: 5 find OutputBasket **PASS**

- TypeScript: `wallet-toolbox/test/storage/findLegacy.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find.py`

---

## Test 429: 6 find Transaction **PASS**

- TypeScript: `wallet-toolbox/test/storage/findLegacy.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 430: 7 find Commission **PASS**

- TypeScript: `wallet-toolbox/test/storage/findLegacy.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 431: 8 find Output **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/findLegacy.test.ts

```typescript
  test('8 find Output', async () => {
    for (const { storage } of ctxs) {
      {
        const r = await storage.findOutputs({
          partial: { userId: 1, basketId: 1 },
          txStatus: ['sending']
        })
        expect(r.length).toBe(1)
        expect(r[0].txid).toBe('a3a8fe7f541c1383ff7b975af49b27284ae720af5f2705d8409baaf519190d26')
        expect(r[0].vout).toBe(2)
      }
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_find_legacy.py

```python
    def test_find_output(self) -> None:
        """Given: Legacy storage with test data
           When: Find Output with userId, basketId, and txStatus filters
           Then: Returns correct output matching legacy schema

        Reference: test/storage/findLegacy.test.ts
                  test('8 find Output')
        """
        # Given

        mock_storage = type(
            "MockStorage",
            (),
            {
                "find_outputs": lambda self, query: [
                    {"txid": "a3a8fe7f541c1383ff7b975af49b27284ae720af5f2705d8409baaf519190d26", "vout": 2}
                ]
            },
        )()

        # When
        results = mock_storage.find_outputs({"partial": {"userId": 1, "basketId": 1}, "txStatus": ["sending"]})

        # Then
        assert len(results) == 1
        assert results[0]["txid"] == "a3a8fe7f541c1383ff7b975af49b27284ae720af5f2705d8409baaf519190d26"
        assert results[0]["vout"] == 2
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: r.length
  - [HIGH] Python test is missing operations: storage.findOutputs

**Differences:**
  - Operation count: TS has 1, PY has 0
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: r.length
  - Add operations: storage.findOutputs

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: r.length
  • [HIGH] Python test is missing operations: storage.findOutputs

Key Differences:
  • Operation count: TS has 1, PY has 0
  • Verification count: TS has 1, PY has 0

---

## Test 432: 9 find OutputTag **PASS**

- TypeScript: `wallet-toolbox/test/storage/findLegacy.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 433: 0 count ProvenTx **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 434: 1 count ProvenTxReq **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 435: 10 count OutputTagMap **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 436: 11 count TxLabel **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 437: 12 count TxLabelMap **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 438: 13 count MonitorEvent **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 439: 14 count SyncState **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 440: 2 count User **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 441: 3 count Certificate **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 442: 4 count CertificateField **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 443: 5 count OutputBasket **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 444: 6 count Transaction **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 445: 7 count Commission **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 446: 8 count Output **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 447: 9 count OutputTag **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/count.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_count.py`

---

## Test 448: 0 find ProvenTx **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find.py`

---

## Test 449: 1 find ProvenTxReq **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find.py`

---

## Test 450: 10 find OutputTagMap **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 451: 11 find TxLabel **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 452: 12 find TxLabelMap **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 453: 13 find MonitorEvent **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 454: 14 find SyncState **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 455: 2 find User **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 456: 3 find Certificate **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 457: 4 find CertificateField **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find.py`

---

## Test 458: 5 find OutputBasket **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find.py`

---

## Test 459: 6 find Transaction **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 460: 7 find Commission **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 461: 8 find Output **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 462: 9 find OutputTag **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/find.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_find_legacy.py`

---

## Test 463: 0 insert ProvenTx **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/idb/insert.test.ts

```typescript
  test('0 insert ProvenTx', async () => {
    for (const storage of storages) {
      const ptx = await _tu.insertTestProvenTx(storage)
      expect(ptx.provenTxId).toBe(1)
      ptx.provenTxId = 0
      // duplicate must throw
      await expect(storage.insertProvenTx(ptx)).rejects.toThrow()
      ptx.provenTxId = 0
      ptx.txid = '4'.repeat(64)
      ptx.provenTxId = await storage.insertProvenTx(ptx)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(ptx.provenTxId).toBeGreaterThan(1)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_proventx(self, storage) -> None:
        """Given: Storage provider with test ProvenTx data
           When: Insert ProvenTx, then attempt duplicate insert
           Then: First insert succeeds with auto-incremented ID, duplicate throws error

        Reference: test/storage/insert.test.ts
                  test('0 insert ProvenTx')
        """
        ptx = {
            "txid": "1" * 64,
            "height": 100,
            "index": 0,
            "merkle_path": [],
            "raw_tx": b"test",
            "block_hash": "block",
            "merkle_root": "root",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        ptx_id = storage.insert_proven_tx(ptx)
        assert ptx_id == 1

        with pytest.raises(Exception):
            storage.insert_proven_tx(ptx)
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: ptx.provenTxId
  - [HIGH] Python test is missing operations: _tu.insertTestProvenTx, storage.insertProvenTx

**Differences:**
  - Operation count: TS has 2, PY has 0
  - Verification count: TS has 2, PY has 0

**Suggestions:**
  - Add verifications for: ptx.provenTxId
  - Add operations: _tu.insertTestProvenTx, storage.insertProvenTx

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: ptx.provenTxId
  • [HIGH] Python test is missing operations: _tu.insertTestProvenTx, storage.insertProvenTx

Key Differences:
  • Operation count: TS has 2, PY has 0
  • Verification count: TS has 2, PY has 0

---

## Test 464: 1 insert ProvenTxReq **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/idb/insert.test.ts

```typescript
  test('1 insert ProvenTxReq', async () => {
    for (const storage of storages) {
      const ptxreq = await _tu.insertTestProvenTxReq(storage)
      expect(ptxreq.provenTxReqId).toBe(1)
      ptxreq.provenTxReqId = 0
      // duplicate must throw
      await expect(storage.insertProvenTxReq(ptxreq)).rejects.toThrow()
      ptxreq.provenTxReqId = 0
      ptxreq.txid = '4'.repeat(64)
      const id = await storage.insertProvenTxReq(ptxreq)
      expect(id).toBe(2)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_proventxreq(self, storage) -> None:
        """Given: Storage provider with test ProvenTxReq data
           When: Insert ProvenTxReq, then attempt duplicate
           Then: First insert succeeds, duplicate throws error

        Reference: test/storage/insert.test.ts
                  test('1 insert ProvenTxReq')
        """
        ptxreq = {
            "userId": 1,
            "txid": "2" * 64,
            "status": "unsent",
            "reference": "",
            "attempts": 0,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        ptxreq_id = storage.insert_proven_tx_req(ptxreq)
        assert ptxreq_id == 1

        with pytest.raises(Exception):
            storage.insert_proven_tx_req(ptxreq)
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: ptxreq.provenTxReqId
  - [HIGH] Python test is missing operations: _tu.insertTestProvenTxReq, storage.insertProvenTxReq

**Differences:**
  - Operation count: TS has 2, PY has 0
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: ptxreq.provenTxReqId
  - Add operations: _tu.insertTestProvenTxReq, storage.insertProvenTxReq

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: ptxreq.provenTxReqId
  • [HIGH] Python test is missing operations: _tu.insertTestProvenTxReq, storage.insertProvenTxReq

Key Differences:
  • Operation count: TS has 2, PY has 0
  • Verification count: TS has 1, PY has 0

---

## Test 465: 10 insert OutputTagMap **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/idb/insert.test.ts

```typescript
  test('10 insert OutputTagMap', async () => {
    for (const storage of storages) {
      const { tx, user } = await _tu.insertTestTransaction(storage)
      const o = await _tu.insertTestOutput(storage, tx, 0, 101)
      const tag = await _tu.insertTestOutputTag(storage, user)
      const e = await _tu.insertTestOutputTagMap(storage, o, tag)
      expect(e.outputId).toBe(o.outputId)
      expect(e.outputTagId).toBe(tag.outputTagId)
      // duplicate must throw
      await expect(storage.insertOutputTagMap(e)).rejects.toThrow()
      const tag2 = await _tu.insertTestOutputTag(storage, user)
      const e2 = await _tu.insertTestOutputTagMap(storage, o, tag2)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_outputtagmap(self, storage, user) -> None:
        """Given: Storage provider with test OutputTagMap data
           When: Insert OutputTagMap
           Then: Insert succeeds

        Reference: test/storage/insert.test.ts
                  test('10 insert OutputTagMap')
        """
        tx = {
            "userId": user,
            "txid": "8" * 64,
            "status": "sending",
            "reference": "",
            "is_outgoing": True,
            "satoshis": 5000,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        tx_id = storage.insert_transaction(tx)

        output = {
            "transaction_id": tx_id,
            "userId": user,
            "vout": 0,
            "satoshis": 101,
            "locking_script": [1, 2, 3],
            "spendable": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        output_id = storage.insert_output(output)

        tag = {
            "userId": user,
            "tag": "test_tag",
            "is_deleted": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        tag_id = storage.insert_output_tag(tag)

        tagmap = {
            "output_id": output_id,
            "output_tag_id": tag_id,
            "is_deleted": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        storage.insert_output_tag_map(tagmap)
```

### AI Analysis Results

**Similarity Score**: 0.00%
  - Structural: 0.00%
  - Semantic: 0.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'value_verification verification' but PY verifies 'authentication'
  - [HIGH] Python test is missing verifications: e.outputId, e.outputTagId
  - [HIGH] Python test is missing operations: _tu.insertTestOutputTagMap, _tu.insertTestOutputTag, _tu.insertTestOutput, _tu.insertTestTransaction

**Differences:**
  - Operation count: TS has 6, PY has 0
  - Verification count: TS has 2, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'value_verification verification'
  - Add verifications for: e.outputId, e.outputTagId
  - Add operations: _tu.insertTestOutputTagMap, _tu.insertTestOutputTag, _tu.insertTestOutput

**Explanation:**

Overall Similarity: 0.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 0.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication

Critical Issues (3):
  • [HIGH] Test intent differs: TS verifies 'value_verification verification' but PY verifies 'authentication'
  • [HIGH] Python test is missing verifications: e.outputId, e.outputTagId
  • [HIGH] Python test is missing operations: _tu.insertTestOutputTagMap, _tu.insertTestOutputTag, _tu.insertTestOutput, _tu.insertTestTransaction

Key Differences:
  • Operation count: TS has 6, PY has 0
  • Verification count: TS has 2, PY has 0

---

## Test 466: 11 insert TxLabel **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/idb/insert.test.ts

```typescript
  test('11 insert TxLabel', async () => {
    for (const storage of storages) {
      const u = await _tu.insertTestUser(storage)
      const e = await _tu.insertTestTxLabel(storage, u)
      const id = e.txLabelId
      expect(id).toBeGreaterThan(0)
      expect(e.userId).toBe(u.userId)
      expect(e.label).toBeTruthy()
      e.txLabelId = 0
      // duplicate must throw
      await expect(storage.insertTxLabel(e)).rejects.toThrow()
      e.label = randomBytesHex(6)
      await storage.insertTxLabel(e)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(e.txLabelId).toBeGreaterThan(id)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_txlabel(self, storage, user) -> None:
        """Given: Storage provider with test TxLabel data
           When: Insert TxLabel
           Then: Insert succeeds with auto-incremented ID

        Reference: test/storage/insert.test.ts
                  test('11 insert TxLabel')
        """
        label = {
            "userId": user,
            "label": "test_label",
            "is_deleted": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        label_id = storage.insert_tx_label(label)
        assert label_id > 0
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: e.userId, e.label, e.txLabelId
  - [HIGH] Python test is missing operations: _tu.insertTestUser, _tu.insertTestTxLabel, storage.insertTxLabel

**Differences:**
  - Operation count: TS has 3, PY has 0
  - Verification count: TS has 3, PY has 0

**Suggestions:**
  - Add verifications for: e.userId, e.label, e.txLabelId
  - Add operations: _tu.insertTestUser, _tu.insertTestTxLabel, storage.insertTxLabel

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: e.userId, e.label, e.txLabelId
  • [HIGH] Python test is missing operations: _tu.insertTestUser, _tu.insertTestTxLabel, storage.insertTxLabel

Key Differences:
  • Operation count: TS has 3, PY has 0
  • Verification count: TS has 3, PY has 0

---

## Test 467: 12 insert TxLabelMap **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/idb/insert.test.ts

```typescript
  test('12 insert TxLabelMap', async () => {
    for (const storage of storages) {
      const { tx, user } = await _tu.insertTestTransaction(storage)
      const label = await _tu.insertTestTxLabel(storage, user)
      const e = await _tu.insertTestTxLabelMap(storage, tx, label)
      expect(e.transactionId).toBe(tx.transactionId)
      expect(e.txLabelId).toBe(label.txLabelId)
      // duplicate must throw
      await expect(storage.insertTxLabelMap(e)).rejects.toThrow()
      const label2 = await _tu.insertTestTxLabel(storage, user)
      const e2 = await _tu.insertTestTxLabelMap(storage, tx, label2)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_txlabelmap(self, storage, user) -> None:
        """Given: Storage provider with test TxLabelMap data
           When: Insert TxLabelMap
           Then: Insert succeeds

        Reference: test/storage/insert.test.ts
                  test('12 insert TxLabelMap')
        """
        tx = {
            "userId": user,
            "txid": "9" * 64,
            "status": "sending",
            "reference": "",
            "is_outgoing": True,
            "satoshis": 5000,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        tx_id = storage.insert_transaction(tx)

        label = {
            "userId": user,
            "label": "test_label",
            "is_deleted": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        label_id = storage.insert_tx_label(label)

        labelmap = {
            "transaction_id": tx_id,
            "tx_label_id": label_id,
            "is_deleted": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        storage.insert_tx_label_map(labelmap)
```

### AI Analysis Results

**Similarity Score**: 0.00%
  - Structural: 0.00%
  - Semantic: 0.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'value_verification verification' but PY verifies 'authentication'
  - [HIGH] Python test is missing verifications: e.transactionId, e.txLabelId
  - [HIGH] Python test is missing operations: _tu.insertTestTxLabelMap, _tu.insertTestTransaction, _tu.insertTestTxLabel

**Differences:**
  - Operation count: TS has 5, PY has 0
  - Verification count: TS has 2, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'value_verification verification'
  - Add verifications for: e.transactionId, e.txLabelId
  - Add operations: _tu.insertTestTxLabelMap, _tu.insertTestTransaction, _tu.insertTestTxLabel

**Explanation:**

Overall Similarity: 0.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 0.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication

Critical Issues (3):
  • [HIGH] Test intent differs: TS verifies 'value_verification verification' but PY verifies 'authentication'
  • [HIGH] Python test is missing verifications: e.transactionId, e.txLabelId
  • [HIGH] Python test is missing operations: _tu.insertTestTxLabelMap, _tu.insertTestTransaction, _tu.insertTestTxLabel

Key Differences:
  • Operation count: TS has 5, PY has 0
  • Verification count: TS has 2, PY has 0

---

## Test 468: 13 insert MonitorEvent **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/insert.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_insert.py`

---

## Test 469: 14 insert SyncState **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/insert.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_insert.py`

---

## Test 470: 2 insert User **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/idb/insert.test.ts

```typescript
  test('2 insert User', async () => {
    for (const storage of storages) {
      const e = await _tu.insertTestUser(storage)
      const id = e.userId
      expect(id).toBeGreaterThan(0)
      e.userId = 0
      // duplicate must throw
      await expect(storage.insertUser(e)).rejects.toThrow()
      e.userId = 0
      e.identityKey = randomBytesHex(33)
      await storage.insertUser(e)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(e.userId).toBeGreaterThan(id)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_user(self, storage) -> None:
        """Given: Storage provider with test User data
           When: Insert User
           Then: Insert succeeds with auto-incremented ID

        Reference: test/storage/insert.test.ts
                  test('2 insert User')
        """
        user = {"identity_key": "03" + "1" * 64, "active_storage": "test"}

        user_id = storage.insert_user(user)
        assert user_id > 0
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: e.userId
  - [HIGH] Python test is missing operations: _tu.insertTestUser, storage.insertUser

**Differences:**
  - Operation count: TS has 2, PY has 0
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: e.userId
  - Add operations: _tu.insertTestUser, storage.insertUser

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: e.userId
  • [HIGH] Python test is missing operations: _tu.insertTestUser, storage.insertUser

Key Differences:
  • Operation count: TS has 2, PY has 0
  • Verification count: TS has 1, PY has 0

---

## Test 471: 3 insert Certificate **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/idb/insert.test.ts

```typescript
  test('3 insert Certificate', async () => {
    for (const storage of storages) {
      const e = await _tu.insertTestCertificate(storage)
      const id = e.certificateId
      expect(id).toBeGreaterThan(0)
      // duplicate must throw
      await expect(storage.insertCertificate(e)).rejects.toThrow()
      e.certificateId = 0
      e.serialNumber = randomBytesBase64(33)
      await storage.insertCertificate(e)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(e.certificateId).toBeGreaterThan(id)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_certificate(self, storage, user) -> None:
        """Given: Storage provider with test Certificate data
           When: Insert Certificate
           Then: Insert succeeds with auto-incremented ID

        Reference: test/storage/insert.test.ts
                  test('3 insert Certificate')
        """
        cert = {
            "userId": user,
            "type": "test_type",
            "serial_number": "serial123",
            "subject": "test_subject",
            "certifier": "03" + "0" * 64,
            "signature": "",
            "verifier": None,
            "revocationOutpoint": None,
            "is_deleted": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        cert_id = storage.insert_certificate(cert)
        assert cert_id > 0
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: e.certificateId
  - [HIGH] Python test is missing operations: storage.insertCertificate, _tu.insertTestCertificate

**Differences:**
  - Operation count: TS has 2, PY has 0
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: e.certificateId
  - Add operations: storage.insertCertificate, _tu.insertTestCertificate

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: e.certificateId
  • [HIGH] Python test is missing operations: storage.insertCertificate, _tu.insertTestCertificate

Key Differences:
  • Operation count: TS has 2, PY has 0
  • Verification count: TS has 1, PY has 0

---

## Test 472: 4 insert CertificateField **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/idb/insert.test.ts

```typescript
  test('4 insert CertificateField', async () => {
    for (const storage of storages) {
      const c = await _tu.insertTestCertificate(storage)
      const e = await _tu.insertTestCertificateField(storage, c, 'prize', 'starship')
      expect(e.certificateId).toBe(c.certificateId)
      expect(e.userId).toBe(c.userId)
      expect(e.fieldName).toBe('prize')
      // duplicate must throw
      await expect(storage.insertCertificateField(e)).rejects.toThrow()
      e.fieldName = 'address'
      await storage.insertCertificateField(e)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(e.fieldName).toBe('address')
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_certificatefield(self, storage, user) -> None:
        """Given: Storage provider with test CertificateField data
           When: Insert CertificateField
           Then: Insert succeeds

        Reference: test/storage/insert.test.ts
                  test('4 insert CertificateField')
        """
        cert = {
            "userId": user,
            "type": "test_type",
            "serial_number": "serial123",
            "subject": "test_subject",
            "certifier": "03" + "0" * 64,
            "signature": "",
            "verifier": None,
            "revocationOutpoint": None,
            "is_deleted": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        cert_id = storage.insert_certificate(cert)

        field = {
            "certificate_id": cert_id,
            "userId": user,
            "field_name": "prize",
            "field_value": "starship",
            "master_key": "master123",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        field_id = storage.insert_certificate_field(field)
        assert field_id is not None
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: e.certificateId, e.userId, e.fieldName
  - [HIGH] Python test is missing operations: _tu.insertTestCertificate, storage.insertCertificateField, _tu.insertTestCertificateField

**Differences:**
  - Operation count: TS has 3, PY has 0
  - Verification count: TS has 4, PY has 0

**Suggestions:**
  - Add verifications for: e.certificateId, e.userId, e.fieldName
  - Add operations: _tu.insertTestCertificate, storage.insertCertificateField, _tu.insertTestCertificateField

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: e.certificateId, e.userId, e.fieldName
  • [HIGH] Python test is missing operations: _tu.insertTestCertificate, storage.insertCertificateField, _tu.insertTestCertificateField

Key Differences:
  • Operation count: TS has 3, PY has 0
  • Verification count: TS has 4, PY has 0

---

## Test 473: 5 insert OutputBasket **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/idb/insert.test.ts

```typescript
  test('5 insert OutputBasket', async () => {
    for (const storage of storages) {
      const e = await _tu.insertTestOutputBasket(storage)
      const id = e.basketId
      expect(id).toBeGreaterThan(0)
      e.basketId = 0
      // duplicate must throw
      await expect(storage.insertOutputBasket(e)).rejects.toThrow()
      e.basketId = 0
      e.name = randomBytesHex(10)
      await storage.insertOutputBasket(e)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(e.basketId).toBeGreaterThan(id)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_outputbasket(self, storage, user) -> None:
        """Given: Storage provider with test OutputBasket data
           When: Insert OutputBasket
           Then: Insert succeeds with auto-incremented ID

        Reference: test/storage/insert.test.ts
                  test('5 insert OutputBasket')
        """
        basket = {
            "userId": user,
            "name": "test_basket",
            "number_of_desired_utxos": 10,
            "minimum_desired_utxo_value": 1000,
            "is_deleted": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        basket_id = storage.insert_output_basket(basket)
        assert basket_id > 0
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: e.basketId
  - [HIGH] Python test is missing operations: _tu.insertTestOutputBasket, storage.insertOutputBasket

**Differences:**
  - Operation count: TS has 2, PY has 0
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: e.basketId
  - Add operations: _tu.insertTestOutputBasket, storage.insertOutputBasket

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: e.basketId
  • [HIGH] Python test is missing operations: _tu.insertTestOutputBasket, storage.insertOutputBasket

Key Differences:
  • Operation count: TS has 2, PY has 0
  • Verification count: TS has 1, PY has 0

---

## Test 474: 6 insert Transaction **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/idb/insert.test.ts

```typescript
  test('6 insert Transaction', async () => {
    for (const storage of storages) {
      const { tx: e, user } = await _tu.insertTestTransaction(storage)
      const id = e.transactionId
      expect(id).toBeGreaterThan(0)
      e.transactionId = 0
      // duplicate must throw
      await expect(storage.insertTransaction(e)).rejects.toThrow()
      e.transactionId = 0
      e.reference = randomBytesBase64(10)
      await storage.insertTransaction(e)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(e.transactionId).toBeGreaterThan(id)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_transaction(self, storage, user) -> None:
        """Given: Storage provider with test Transaction data
           When: Insert Transaction
           Then: Insert succeeds with auto-incremented ID

        Reference: test/storage/insert.test.ts
                  test('6 insert Transaction')
        """
        tx = {
            "userId": user,
            "txid": "5" * 64,
            "status": "sending",
            "reference": "ref123",
            "is_outgoing": True,
            "satoshis": 5000,
            "description": "Test transaction",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        tx_id = storage.insert_transaction(tx)
        assert tx_id > 0
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: e.transactionId
  - [HIGH] Python test is missing operations: _tu.insertTestTransaction, storage.insertTransaction

**Differences:**
  - Operation count: TS has 2, PY has 0
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: e.transactionId
  - Add operations: _tu.insertTestTransaction, storage.insertTransaction

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: e.transactionId
  • [HIGH] Python test is missing operations: _tu.insertTestTransaction, storage.insertTransaction

Key Differences:
  • Operation count: TS has 2, PY has 0
  • Verification count: TS has 1, PY has 0

---

## Test 475: 7 insert Commission **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/idb/insert.test.ts

```typescript
  test('7 insert Commission', async () => {
    for (const storage of storages) {
      const { tx: t, user } = await _tu.insertTestTransaction(storage)
      const e: TableCommission = await _tu.insertTestCommission(storage, t)
      const id = e.commissionId
      expect(id).toBeGreaterThan(0)
      e.commissionId = 0
      // duplicate must throw
      await expect(storage.insertCommission(e)).rejects.toThrow()
      e.commissionId = 0
      const { tx: t2 } = await _tu.insertTestTransaction(storage)
      e.transactionId = t2.transactionId
      e.userId = t2.userId
      await storage.insertCommission(e)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(e.commissionId).toBeGreaterThan(id)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_commission(self, storage, user) -> None:
        """Given: Storage provider with test Commission data
           When: Insert Commission
           Then: Insert succeeds with auto-incremented ID

        Reference: test/storage/insert.test.ts
                  test('7 insert Commission')
        """
        tx = {
            "userId": user,
            "txid": "6" * 64,
            "status": "sending",
            "reference": "",
            "is_outgoing": True,
            "satoshis": 5000,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        tx_id = storage.insert_transaction(tx)

        commission = {
            "transaction_id": tx_id,
            "userId": user,
            "isRedeemed": False,
            "key_offset": "offset123",
            "locking_script": [1, 2, 3],
            "satoshis": 500,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        comm_id = storage.insert_commission(commission)
        assert comm_id > 0
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: e.commissionId
  - [HIGH] Python test is missing operations: _tu.insertTestCommission, storage.insertCommission, _tu.insertTestTransaction

**Differences:**
  - Operation count: TS has 4, PY has 0
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: e.commissionId
  - Add operations: _tu.insertTestCommission, storage.insertCommission, _tu.insertTestTransaction

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: e.commissionId
  • [HIGH] Python test is missing operations: _tu.insertTestCommission, storage.insertCommission, _tu.insertTestTransaction

Key Differences:
  • Operation count: TS has 4, PY has 0
  • Verification count: TS has 1, PY has 0

---

## Test 476: 8 insert Output **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/idb/insert.test.ts

```typescript
  test('8 insert Output', async () => {
    for (const storage of storages) {
      const { tx: t, user } = await _tu.insertTestTransaction(storage)
      const e = await _tu.insertTestOutput(storage, t, 0, 101)
      const id = e.outputId
      expect(id).toBeGreaterThan(0)
      expect(e.userId).toBe(t.userId)
      expect(e.transactionId).toBe(t.transactionId)
      expect(e.vout).toBe(0)
      expect(e.satoshis).toBe(101)
      e.outputId = 0
      // duplicate must throw
      await expect(storage.insertOutput(e)).rejects.toThrow()
      e.vout = 1
      await storage.insertOutput(e)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(e.outputId).toBeGreaterThan(id)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_output(self, storage, user) -> None:
        """Given: Storage provider with test Output data
           When: Insert Output
           Then: Insert succeeds with auto-incremented ID

        Reference: test/storage/insert.test.ts
                  test('8 insert Output')
        """
        tx = {
            "userId": user,
            "txid": "7" * 64,
            "status": "sending",
            "reference": "",
            "is_outgoing": True,
            "satoshis": 5000,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        tx_id = storage.insert_transaction(tx)

        output = {
            "transaction_id": tx_id,
            "userId": user,
            "vout": 0,
            "satoshis": 101,
            "locking_script": [1, 2, 3],
            "spendable": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        output_id = storage.insert_output(output)
        assert output_id > 0
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: e.outputId, e.satoshis, e.transactionId, e.userId, e.vout
  - [HIGH] Python test is missing operations: _tu.insertTestOutput, _tu.insertTestTransaction, storage.insertOutput

**Differences:**
  - Operation count: TS has 3, PY has 0
  - Verification count: TS has 5, PY has 0

**Suggestions:**
  - Add verifications for: e.outputId, e.satoshis, e.transactionId
  - Add operations: _tu.insertTestOutput, _tu.insertTestTransaction, storage.insertOutput

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: e.outputId, e.satoshis, e.transactionId, e.userId, e.vout
  • [HIGH] Python test is missing operations: _tu.insertTestOutput, _tu.insertTestTransaction, storage.insertOutput

Key Differences:
  • Operation count: TS has 3, PY has 0
  • Verification count: TS has 5, PY has 0

---

## Test 477: 9 insert OutputTag **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/idb/insert.test.ts

```typescript
  test('9 insert OutputTag', async () => {
    for (const storage of storages) {
      const u = await _tu.insertTestUser(storage)
      const e = await _tu.insertTestOutputTag(storage, u)
      const id = e.outputTagId
      expect(id).toBeGreaterThan(0)
      expect(e.userId).toBe(u.userId)
      expect(e.tag).toBeTruthy()
      e.outputTagId = 0
      // duplicate must throw
      await expect(storage.insertOutputTag(e)).rejects.toThrow()
      e.tag = randomBytesHex(6)
      await storage.insertOutputTag(e)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(e.outputTagId).toBeGreaterThan(id)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_outputtag(self, storage, user) -> None:
        """Given: Storage provider with test OutputTag data
           When: Insert OutputTag
           Then: Insert succeeds with auto-incremented ID

        Reference: test/storage/insert.test.ts
                  test('9 insert OutputTag')
        """
        tag = {
            "userId": user,
            "tag": "test_tag",
            "is_deleted": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        tag_id = storage.insert_output_tag(tag)
        assert tag_id > 0
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: e.userId, e.outputTagId, e.tag
  - [HIGH] Python test is missing operations: storage.insertOutputTag, _tu.insertTestUser, _tu.insertTestOutputTag

**Differences:**
  - Operation count: TS has 3, PY has 0
  - Verification count: TS has 3, PY has 0

**Suggestions:**
  - Add verifications for: e.userId, e.outputTagId, e.tag
  - Add operations: storage.insertOutputTag, _tu.insertTestUser, _tu.insertTestOutputTag

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: e.userId, e.outputTagId, e.tag
  • [HIGH] Python test is missing operations: storage.insertOutputTag, _tu.insertTestUser, _tu.insertTestOutputTag

Key Differences:
  • Operation count: TS has 3, PY has 0
  • Verification count: TS has 3, PY has 0

---

## Test 478: 0_update ProvenTx **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/idb/update.test.ts

```typescript
  test('0_update ProvenTx', async () => {
    for (const { storage } of setups) {
      const records = await storage.findProvenTxs({ partial: {} })
      const time = new Date('2001-01-02T12:00:00.000Z')
      for (const record of records) {
        await storage.updateProvenTx(record.provenTxId, {
          blockHash: 'fred',
          updated_at: time
        })
        const t = verifyOne(
          await storage.findProvenTxs({
            partial: { provenTxId: record.provenTxId }
          })
        )
        expect(t.provenTxId).toBe(record.provenTxId)
        expect(t.blockHash).toBe('fred')
        expect(t.updated_at.getTime()).toBe(time.getTime())
      }
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_update.py

```python
def test_update_proventx(storage_seeded) -> None:
    storage, seed = storage_seeded
    record = seed["proven_tx"]
    new_time = datetime(2001, 1, 2, 12, 0, 0)

    updated = storage.update_proven_tx(
        record["provenTxId"],
        {
            "blockHash": "updated-block-hash",
            "updatedAt": new_time,
        },
    )
    assert updated == 1

    refreshed = _first(storage.find_proven_txs({"partial": {"provenTxId": record["provenTxId"]}}))
    assert refreshed["blockHash"] == "updated-block-hash"
    assert refreshed["updatedAt"] == new_time
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: t.blockHash, t.provenTxId
  - [HIGH] Python test is missing operations: storage.updateProvenTx, storage.findProvenTxs

**Differences:**
  - Operation count: TS has 3, PY has 0

**Suggestions:**
  - Add verifications for: t.blockHash, t.provenTxId
  - Add operations: storage.updateProvenTx, storage.findProvenTxs

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: t.blockHash, t.provenTxId
  • [HIGH] Python test is missing operations: storage.updateProvenTx, storage.findProvenTxs

Key Differences:
  • Operation count: TS has 3, PY has 0

---

## Test 479: 10_update OutputTag **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 480: 11_update OutputTagMap **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 481: 12_update TxLabel **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 482: 13_update TxLabelMap **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 483: 14_update MonitorEvent **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 484: 15_update SyncState **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 485: 1_update ProvenTx **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 486: 2_update ProvenTxReq **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 487: 3_update User **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 488: 4_update Certificate **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 489: 5_update CertificateField **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 490: 6_update OutputBasket **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 491: 7_update Transaction **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 492: 8_update Commission **PASS**

- TypeScript: `wallet-toolbox/test/storage/idb/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 493: 9_update Output **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/idb/update.test.ts

```typescript
  test('9_update Output', async () => {
    const primaryKey = 'outputId'
    for (const { storage } of setups) {
      const records = await storage.findOutputs({ partial: {} })
      for (const record of records) {
        if (!record.transactionId) record.transactionId = 1
        if (!record.basketId) record.basketId = 1
        if (!record.userId || !record.transactionId || !record.basketId) {
          throw new Error(`Missing required foreign keys for record ${JSON.stringify(record)}`)
        }
      }
      for (const record of records) {
        const existingRecords = await storage.findOutputs({ partial: {} })
        const usedCombinations = new Set(existingRecords.map(r => `${r.transactionId}-${r.vout}-${r.userId}`))
        let testTransactionId = record.transactionId
        let testVout = record.vout + 1
        let testUserId = record.userId
        while (usedCombinations.has(`${testTransactionId}-${testVout}-${testUserId}`)) {
          testVout += 1
        }
        try {
          const testValues: TableOutput = {
            outputId: record.outputId,
            basketId: record.basketId ?? 1,
            transactionId: testTransactionId,
            userId: testUserId,
            vout: testVout,
            created_at: new Date('2024-12-30T23:00:00Z'),
            updated_at: new Date('2024-12-30T23:05:00Z'),
            change: true,
            customInstructions: 'Updated instructions',
            derivationPrefix: 'updated_prefix==',
            derivationSuffix: 'updated_suffix==',
            lockingScript: [0x01, 0x02, 0x03, 0x04],
            providedBy: 'you',
            purpose: 'updated_purpose',
            satoshis: 3000,
            scriptLength: 150,
            scriptOffset: 5,
            senderIdentityKey: 'updated_sender_key',
            sequenceNumber: 10,
            spendingDescription: 'Updated spending description',
            spendable: false,
            spentBy: 3,
            txid: 'updated_txid',
            type: 'updated_type',
            outputDescription: 'outputDescription'
          }
          const updateResult = await storage.updateOutput(record.outputId, testValues)
          expect(updateResult).toBe(1)
          const updatedRecords = await storage.findOutputs({
            partial: { outputId: record.outputId }
          })
          const updatedRow = verifyOne(
            updatedRecords,
            `Updated Output with outputId=${record.outputId} was not unique or missing.`
          )
          for (const [key, value] of Object.entries(testValues)) {
            const actualValue = updatedRow[key]
            const normalizedActual = normalizeDate(actualValue)
            const normalizedExpected = normalizeDate(value)
            if (normalizedActual && normalizedExpected) {
              expect(normalizedActual).toBe(normalizedExpected)
              continue
            }
            if (Array.isArray(actualValue)) {
              expect(actualValue).toStrictEqual(value)
              continue
            }
            expect(actualValue).toBe(value)
          }
        } catch (error: any) {
          console.error(`Error updating or verifying Output record with outputId=${record[primaryKey]}:`, error.message)
          throw error
        }
      }
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_update.py

```python
def test_update_output(storage_seeded) -> None:
    storage, seed = storage_seeded
    output = seed["outputs"]["o1"]
    updated = storage.update_output(
        output["outputId"],
        {
            "spendable": False,
            "purpose": "updated-purpose",
        },
    )
    assert updated == 1

    refreshed = _first(storage.find_outputs({"partial": {"outputId": output["outputId"]}}))
    assert refreshed["spendable"] is False
    assert refreshed["purpose"] == "updated-purpose"
```

### AI Analysis Results

**Similarity Score**: 42.00%
  - Structural: 0.00%
  - Semantic: 84.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing operations: storage.updateOutput, storage.findOutputs

**Differences:**
  - Operation count: TS has 4, PY has 0
  - Verification count: TS has 0, PY has 2

**Suggestions:**
  - Add operations: storage.updateOutput, storage.findOutputs

**Explanation:**

Overall Similarity: 42.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 84.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: authentication verification key_change
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing operations: storage.updateOutput, storage.findOutputs

Key Differences:
  • Operation count: TS has 4, PY has 0
  • Verification count: TS has 0, PY has 2

---

## Test 494: 0 insert ProvenTx **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/insert.test.ts

```typescript
  test('0 insert ProvenTx', async () => {
    for (const storage of storages) {
      const ptx = await _tu.insertTestProvenTx(storage)
      expect(ptx.provenTxId).toBe(1)
      ptx.provenTxId = 0
      // duplicate must throw
      await expect(storage.insertProvenTx(ptx)).rejects.toThrow()
      ptx.provenTxId = 0
      ptx.txid = '4'.repeat(64)
      ptx.provenTxId = await storage.insertProvenTx(ptx)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(ptx.provenTxId).toBeGreaterThan(1)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_proventx(self, storage) -> None:
        """Given: Storage provider with test ProvenTx data
           When: Insert ProvenTx, then attempt duplicate insert
           Then: First insert succeeds with auto-incremented ID, duplicate throws error

        Reference: test/storage/insert.test.ts
                  test('0 insert ProvenTx')
        """
        ptx = {
            "txid": "1" * 64,
            "height": 100,
            "index": 0,
            "merkle_path": [],
            "raw_tx": b"test",
            "block_hash": "block",
            "merkle_root": "root",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        ptx_id = storage.insert_proven_tx(ptx)
        assert ptx_id == 1

        with pytest.raises(Exception):
            storage.insert_proven_tx(ptx)
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: ptx.provenTxId
  - [HIGH] Python test is missing operations: _tu.insertTestProvenTx, storage.insertProvenTx

**Differences:**
  - Operation count: TS has 2, PY has 0
  - Verification count: TS has 2, PY has 0

**Suggestions:**
  - Add verifications for: ptx.provenTxId
  - Add operations: _tu.insertTestProvenTx, storage.insertProvenTx

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: ptx.provenTxId
  • [HIGH] Python test is missing operations: _tu.insertTestProvenTx, storage.insertProvenTx

Key Differences:
  • Operation count: TS has 2, PY has 0
  • Verification count: TS has 2, PY has 0

---

## Test 495: 1 insert ProvenTxReq **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/insert.test.ts

```typescript
  test('1 insert ProvenTxReq', async () => {
    for (const storage of storages) {
      const ptxreq = await _tu.insertTestProvenTxReq(storage)
      expect(ptxreq.provenTxReqId).toBe(1)
      ptxreq.provenTxReqId = 0
      // duplicate must throw
      await expect(storage.insertProvenTxReq(ptxreq)).rejects.toThrow()
      ptxreq.provenTxReqId = 0
      ptxreq.txid = '4'.repeat(64)
      await storage.insertProvenTxReq(ptxreq)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(ptxreq.provenTxReqId).toBeGreaterThan(1)
      ptxreq.provenTxId = 9999 // non-existent
      await expect(storage.insertProvenTxReq(ptxreq)).rejects.toThrow()
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_proventxreq(self, storage) -> None:
        """Given: Storage provider with test ProvenTxReq data
           When: Insert ProvenTxReq, then attempt duplicate
           Then: First insert succeeds, duplicate throws error

        Reference: test/storage/insert.test.ts
                  test('1 insert ProvenTxReq')
        """
        ptxreq = {
            "userId": 1,
            "txid": "2" * 64,
            "status": "unsent",
            "reference": "",
            "attempts": 0,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        ptxreq_id = storage.insert_proven_tx_req(ptxreq)
        assert ptxreq_id == 1

        with pytest.raises(Exception):
            storage.insert_proven_tx_req(ptxreq)
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: ptxreq.provenTxReqId
  - [HIGH] Python test is missing operations: _tu.insertTestProvenTxReq, storage.insertProvenTxReq

**Differences:**
  - Operation count: TS has 2, PY has 0
  - Verification count: TS has 2, PY has 0

**Suggestions:**
  - Add verifications for: ptxreq.provenTxReqId
  - Add operations: _tu.insertTestProvenTxReq, storage.insertProvenTxReq

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: ptxreq.provenTxReqId
  • [HIGH] Python test is missing operations: _tu.insertTestProvenTxReq, storage.insertProvenTxReq

Key Differences:
  • Operation count: TS has 2, PY has 0
  • Verification count: TS has 2, PY has 0

---

## Test 496: 10 insert OutputTagMap **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/insert.test.ts

```typescript
  test('10 insert OutputTagMap', async () => {
    for (const storage of storages) {
      const { tx, user } = await _tu.insertTestTransaction(storage)
      const o = await _tu.insertTestOutput(storage, tx, 0, 101)
      const tag = await _tu.insertTestOutputTag(storage, user)
      const e = await _tu.insertTestOutputTagMap(storage, o, tag)
      expect(e.outputId).toBe(o.outputId)
      expect(e.outputTagId).toBe(tag.outputTagId)
      // duplicate must throw
      await expect(storage.insertOutputTagMap(e)).rejects.toThrow()
      const tag2 = await _tu.insertTestOutputTag(storage, user)
      const e2 = await _tu.insertTestOutputTagMap(storage, o, tag2)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_outputtagmap(self, storage, user) -> None:
        """Given: Storage provider with test OutputTagMap data
           When: Insert OutputTagMap
           Then: Insert succeeds

        Reference: test/storage/insert.test.ts
                  test('10 insert OutputTagMap')
        """
        tx = {
            "userId": user,
            "txid": "8" * 64,
            "status": "sending",
            "reference": "",
            "is_outgoing": True,
            "satoshis": 5000,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        tx_id = storage.insert_transaction(tx)

        output = {
            "transaction_id": tx_id,
            "userId": user,
            "vout": 0,
            "satoshis": 101,
            "locking_script": [1, 2, 3],
            "spendable": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        output_id = storage.insert_output(output)

        tag = {
            "userId": user,
            "tag": "test_tag",
            "is_deleted": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        tag_id = storage.insert_output_tag(tag)

        tagmap = {
            "output_id": output_id,
            "output_tag_id": tag_id,
            "is_deleted": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        storage.insert_output_tag_map(tagmap)
```

### AI Analysis Results

**Similarity Score**: 0.00%
  - Structural: 0.00%
  - Semantic: 0.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'value_verification verification' but PY verifies 'authentication'
  - [HIGH] Python test is missing verifications: e.outputId, e.outputTagId
  - [HIGH] Python test is missing operations: _tu.insertTestOutputTagMap, _tu.insertTestOutputTag, _tu.insertTestOutput, _tu.insertTestTransaction

**Differences:**
  - Operation count: TS has 6, PY has 0
  - Verification count: TS has 2, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'value_verification verification'
  - Add verifications for: e.outputId, e.outputTagId
  - Add operations: _tu.insertTestOutputTagMap, _tu.insertTestOutputTag, _tu.insertTestOutput

**Explanation:**

Overall Similarity: 0.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 0.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication

Critical Issues (3):
  • [HIGH] Test intent differs: TS verifies 'value_verification verification' but PY verifies 'authentication'
  • [HIGH] Python test is missing verifications: e.outputId, e.outputTagId
  • [HIGH] Python test is missing operations: _tu.insertTestOutputTagMap, _tu.insertTestOutputTag, _tu.insertTestOutput, _tu.insertTestTransaction

Key Differences:
  • Operation count: TS has 6, PY has 0
  • Verification count: TS has 2, PY has 0

---

## Test 497: 11 insert TxLabel **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/insert.test.ts

```typescript
  test('11 insert TxLabel', async () => {
    for (const storage of storages) {
      const u = await _tu.insertTestUser(storage)
      const e = await _tu.insertTestTxLabel(storage, u)
      const id = e.txLabelId
      expect(id).toBeGreaterThan(0)
      expect(e.userId).toBe(u.userId)
      expect(e.label).toBeTruthy()
      // duplicate must throw
      e.txLabelId = 0
      await expect(storage.insertTxLabel(e)).rejects.toThrow()
      e.label = randomBytesHex(6)
      await storage.insertTxLabel(e)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(e.txLabelId).toBeGreaterThan(id)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_txlabel(self, storage, user) -> None:
        """Given: Storage provider with test TxLabel data
           When: Insert TxLabel
           Then: Insert succeeds with auto-incremented ID

        Reference: test/storage/insert.test.ts
                  test('11 insert TxLabel')
        """
        label = {
            "userId": user,
            "label": "test_label",
            "is_deleted": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        label_id = storage.insert_tx_label(label)
        assert label_id > 0
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: e.userId, e.label, e.txLabelId
  - [HIGH] Python test is missing operations: _tu.insertTestUser, _tu.insertTestTxLabel, storage.insertTxLabel

**Differences:**
  - Operation count: TS has 3, PY has 0
  - Verification count: TS has 3, PY has 0

**Suggestions:**
  - Add verifications for: e.userId, e.label, e.txLabelId
  - Add operations: _tu.insertTestUser, _tu.insertTestTxLabel, storage.insertTxLabel

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: e.userId, e.label, e.txLabelId
  • [HIGH] Python test is missing operations: _tu.insertTestUser, _tu.insertTestTxLabel, storage.insertTxLabel

Key Differences:
  • Operation count: TS has 3, PY has 0
  • Verification count: TS has 3, PY has 0

---

## Test 498: 12 insert TxLabelMap **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/insert.test.ts

```typescript
  test('12 insert TxLabelMap', async () => {
    for (const storage of storages) {
      const { tx, user } = await _tu.insertTestTransaction(storage)
      const label = await _tu.insertTestTxLabel(storage, user)
      const e = await _tu.insertTestTxLabelMap(storage, tx, label)
      expect(e.transactionId).toBe(tx.transactionId)
      expect(e.txLabelId).toBe(label.txLabelId)
      // duplicate must throw
      await expect(storage.insertTxLabelMap(e)).rejects.toThrow()
      const label2 = await _tu.insertTestTxLabel(storage, user)
      const e2 = await _tu.insertTestTxLabelMap(storage, tx, label2)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_txlabelmap(self, storage, user) -> None:
        """Given: Storage provider with test TxLabelMap data
           When: Insert TxLabelMap
           Then: Insert succeeds

        Reference: test/storage/insert.test.ts
                  test('12 insert TxLabelMap')
        """
        tx = {
            "userId": user,
            "txid": "9" * 64,
            "status": "sending",
            "reference": "",
            "is_outgoing": True,
            "satoshis": 5000,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        tx_id = storage.insert_transaction(tx)

        label = {
            "userId": user,
            "label": "test_label",
            "is_deleted": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        label_id = storage.insert_tx_label(label)

        labelmap = {
            "transaction_id": tx_id,
            "tx_label_id": label_id,
            "is_deleted": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        storage.insert_tx_label_map(labelmap)
```

### AI Analysis Results

**Similarity Score**: 0.00%
  - Structural: 0.00%
  - Semantic: 0.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'value_verification verification' but PY verifies 'authentication'
  - [HIGH] Python test is missing verifications: e.transactionId, e.txLabelId
  - [HIGH] Python test is missing operations: _tu.insertTestTxLabelMap, _tu.insertTestTransaction, _tu.insertTestTxLabel

**Differences:**
  - Operation count: TS has 5, PY has 0
  - Verification count: TS has 2, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'value_verification verification'
  - Add verifications for: e.transactionId, e.txLabelId
  - Add operations: _tu.insertTestTxLabelMap, _tu.insertTestTransaction, _tu.insertTestTxLabel

**Explanation:**

Overall Similarity: 0.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 0.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication

Critical Issues (3):
  • [HIGH] Test intent differs: TS verifies 'value_verification verification' but PY verifies 'authentication'
  • [HIGH] Python test is missing verifications: e.transactionId, e.txLabelId
  • [HIGH] Python test is missing operations: _tu.insertTestTxLabelMap, _tu.insertTestTransaction, _tu.insertTestTxLabel

Key Differences:
  • Operation count: TS has 5, PY has 0
  • Verification count: TS has 2, PY has 0

---

## Test 499: 13 insert MonitorEvent **PASS**

- TypeScript: `wallet-toolbox/test/storage/insert.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_insert.py`

---

## Test 500: 14 insert SyncState **PASS**

- TypeScript: `wallet-toolbox/test/storage/insert.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_insert.py`

---

## Test 501: 2 insert User **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/insert.test.ts

```typescript
  test('2 insert User', async () => {
    for (const storage of storages) {
      const e = await _tu.insertTestUser(storage)
      const id = e.userId
      expect(id).toBeGreaterThan(0)
      e.userId = 0
      // duplicate must throw
      await expect(storage.insertUser(e)).rejects.toThrow()
      e.userId = 0
      e.identityKey = randomBytesHex(33)
      await storage.insertUser(e)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(e.userId).toBeGreaterThan(id)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_user(self, storage) -> None:
        """Given: Storage provider with test User data
           When: Insert User
           Then: Insert succeeds with auto-incremented ID

        Reference: test/storage/insert.test.ts
                  test('2 insert User')
        """
        user = {"identity_key": "03" + "1" * 64, "active_storage": "test"}

        user_id = storage.insert_user(user)
        assert user_id > 0
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: e.userId
  - [HIGH] Python test is missing operations: _tu.insertTestUser, storage.insertUser

**Differences:**
  - Operation count: TS has 2, PY has 0
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: e.userId
  - Add operations: _tu.insertTestUser, storage.insertUser

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: e.userId
  • [HIGH] Python test is missing operations: _tu.insertTestUser, storage.insertUser

Key Differences:
  • Operation count: TS has 2, PY has 0
  • Verification count: TS has 1, PY has 0

---

## Test 502: 3 insert Certificate **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/insert.test.ts

```typescript
  test('3 insert Certificate', async () => {
    for (const storage of storages) {
      const e = await _tu.insertTestCertificate(storage)
      const id = e.certificateId
      expect(id).toBeGreaterThan(0)
      e.certificateId = 0
      // duplicate must throw
      await expect(storage.insertCertificate(e)).rejects.toThrow()
      e.certificateId = 0
      e.serialNumber = randomBytesBase64(33)
      await storage.insertCertificate(e)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(e.certificateId).toBeGreaterThan(id)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_certificate(self, storage, user) -> None:
        """Given: Storage provider with test Certificate data
           When: Insert Certificate
           Then: Insert succeeds with auto-incremented ID

        Reference: test/storage/insert.test.ts
                  test('3 insert Certificate')
        """
        cert = {
            "userId": user,
            "type": "test_type",
            "serial_number": "serial123",
            "subject": "test_subject",
            "certifier": "03" + "0" * 64,
            "signature": "",
            "verifier": None,
            "revocationOutpoint": None,
            "is_deleted": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        cert_id = storage.insert_certificate(cert)
        assert cert_id > 0
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: e.certificateId
  - [HIGH] Python test is missing operations: storage.insertCertificate, _tu.insertTestCertificate

**Differences:**
  - Operation count: TS has 2, PY has 0
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: e.certificateId
  - Add operations: storage.insertCertificate, _tu.insertTestCertificate

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: e.certificateId
  • [HIGH] Python test is missing operations: storage.insertCertificate, _tu.insertTestCertificate

Key Differences:
  • Operation count: TS has 2, PY has 0
  • Verification count: TS has 1, PY has 0

---

## Test 503: 4 insert CertificateField **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/insert.test.ts

```typescript
  test('4 insert CertificateField', async () => {
    for (const storage of storages) {
      const c = await _tu.insertTestCertificate(storage)
      const e = await _tu.insertTestCertificateField(storage, c, 'prize', 'starship')
      expect(e.certificateId).toBe(c.certificateId)
      expect(e.userId).toBe(c.userId)
      expect(e.fieldName).toBe('prize')
      // duplicate must throw
      await expect(storage.insertCertificateField(e)).rejects.toThrow()
      e.fieldName = 'address'
      await storage.insertCertificateField(e)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(e.fieldName).toBe('address')
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_certificatefield(self, storage, user) -> None:
        """Given: Storage provider with test CertificateField data
           When: Insert CertificateField
           Then: Insert succeeds

        Reference: test/storage/insert.test.ts
                  test('4 insert CertificateField')
        """
        cert = {
            "userId": user,
            "type": "test_type",
            "serial_number": "serial123",
            "subject": "test_subject",
            "certifier": "03" + "0" * 64,
            "signature": "",
            "verifier": None,
            "revocationOutpoint": None,
            "is_deleted": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        cert_id = storage.insert_certificate(cert)

        field = {
            "certificate_id": cert_id,
            "userId": user,
            "field_name": "prize",
            "field_value": "starship",
            "master_key": "master123",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        field_id = storage.insert_certificate_field(field)
        assert field_id is not None
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: e.certificateId, e.userId, e.fieldName
  - [HIGH] Python test is missing operations: _tu.insertTestCertificate, storage.insertCertificateField, _tu.insertTestCertificateField

**Differences:**
  - Operation count: TS has 3, PY has 0
  - Verification count: TS has 4, PY has 0

**Suggestions:**
  - Add verifications for: e.certificateId, e.userId, e.fieldName
  - Add operations: _tu.insertTestCertificate, storage.insertCertificateField, _tu.insertTestCertificateField

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: e.certificateId, e.userId, e.fieldName
  • [HIGH] Python test is missing operations: _tu.insertTestCertificate, storage.insertCertificateField, _tu.insertTestCertificateField

Key Differences:
  • Operation count: TS has 3, PY has 0
  • Verification count: TS has 4, PY has 0

---

## Test 504: 5 insert OutputBasket **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/insert.test.ts

```typescript
  test('5 insert OutputBasket', async () => {
    for (const storage of storages) {
      const e = await _tu.insertTestOutputBasket(storage)
      const id = e.basketId
      expect(id).toBeGreaterThan(0)
      e.basketId = 0
      // duplicate must throw
      await expect(storage.insertOutputBasket(e)).rejects.toThrow()
      e.basketId = 0
      e.name = randomBytesHex(10)
      await storage.insertOutputBasket(e)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(e.basketId).toBeGreaterThan(id)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_outputbasket(self, storage, user) -> None:
        """Given: Storage provider with test OutputBasket data
           When: Insert OutputBasket
           Then: Insert succeeds with auto-incremented ID

        Reference: test/storage/insert.test.ts
                  test('5 insert OutputBasket')
        """
        basket = {
            "userId": user,
            "name": "test_basket",
            "number_of_desired_utxos": 10,
            "minimum_desired_utxo_value": 1000,
            "is_deleted": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        basket_id = storage.insert_output_basket(basket)
        assert basket_id > 0
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: e.basketId
  - [HIGH] Python test is missing operations: _tu.insertTestOutputBasket, storage.insertOutputBasket

**Differences:**
  - Operation count: TS has 2, PY has 0
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: e.basketId
  - Add operations: _tu.insertTestOutputBasket, storage.insertOutputBasket

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: e.basketId
  • [HIGH] Python test is missing operations: _tu.insertTestOutputBasket, storage.insertOutputBasket

Key Differences:
  • Operation count: TS has 2, PY has 0
  • Verification count: TS has 1, PY has 0

---

## Test 505: 6 insert Transaction **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/insert.test.ts

```typescript
  test('6 insert Transaction', async () => {
    for (const storage of storages) {
      const { tx: e, user } = await _tu.insertTestTransaction(storage)
      const id = e.transactionId
      expect(id).toBeGreaterThan(0)
      e.transactionId = 0
      // duplicate must throw
      await expect(storage.insertTransaction(e)).rejects.toThrow()
      e.transactionId = 0
      e.reference = randomBytesBase64(10)
      await storage.insertTransaction(e)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(e.transactionId).toBeGreaterThan(id)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_transaction(self, storage, user) -> None:
        """Given: Storage provider with test Transaction data
           When: Insert Transaction
           Then: Insert succeeds with auto-incremented ID

        Reference: test/storage/insert.test.ts
                  test('6 insert Transaction')
        """
        tx = {
            "userId": user,
            "txid": "5" * 64,
            "status": "sending",
            "reference": "ref123",
            "is_outgoing": True,
            "satoshis": 5000,
            "description": "Test transaction",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        tx_id = storage.insert_transaction(tx)
        assert tx_id > 0
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: e.transactionId
  - [HIGH] Python test is missing operations: _tu.insertTestTransaction, storage.insertTransaction

**Differences:**
  - Operation count: TS has 2, PY has 0
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: e.transactionId
  - Add operations: _tu.insertTestTransaction, storage.insertTransaction

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: e.transactionId
  • [HIGH] Python test is missing operations: _tu.insertTestTransaction, storage.insertTransaction

Key Differences:
  • Operation count: TS has 2, PY has 0
  • Verification count: TS has 1, PY has 0

---

## Test 506: 7 insert Commission **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/insert.test.ts

```typescript
  test('7 insert Commission', async () => {
    for (const storage of storages) {
      const { tx: t, user } = await _tu.insertTestTransaction(storage)
      const e: TableCommission = await _tu.insertTestCommission(storage, t)
      const id = e.commissionId
      expect(id).toBeGreaterThan(0)
      e.commissionId = 0
      // duplicate must throw
      await expect(storage.insertCommission(e)).rejects.toThrow()
      e.commissionId = 0
      const { tx: t2 } = await _tu.insertTestTransaction(storage)
      e.transactionId = t2.transactionId
      e.userId = t2.userId
      await storage.insertCommission(e)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(e.commissionId).toBeGreaterThan(id)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_commission(self, storage, user) -> None:
        """Given: Storage provider with test Commission data
           When: Insert Commission
           Then: Insert succeeds with auto-incremented ID

        Reference: test/storage/insert.test.ts
                  test('7 insert Commission')
        """
        tx = {
            "userId": user,
            "txid": "6" * 64,
            "status": "sending",
            "reference": "",
            "is_outgoing": True,
            "satoshis": 5000,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        tx_id = storage.insert_transaction(tx)

        commission = {
            "transaction_id": tx_id,
            "userId": user,
            "isRedeemed": False,
            "key_offset": "offset123",
            "locking_script": [1, 2, 3],
            "satoshis": 500,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        comm_id = storage.insert_commission(commission)
        assert comm_id > 0
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: e.commissionId
  - [HIGH] Python test is missing operations: _tu.insertTestCommission, storage.insertCommission, _tu.insertTestTransaction

**Differences:**
  - Operation count: TS has 4, PY has 0
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: e.commissionId
  - Add operations: _tu.insertTestCommission, storage.insertCommission, _tu.insertTestTransaction

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: e.commissionId
  • [HIGH] Python test is missing operations: _tu.insertTestCommission, storage.insertCommission, _tu.insertTestTransaction

Key Differences:
  • Operation count: TS has 4, PY has 0
  • Verification count: TS has 1, PY has 0

---

## Test 507: 8 insert Output **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/insert.test.ts

```typescript
  test('8 insert Output', async () => {
    for (const storage of storages) {
      const { tx: t, user } = await _tu.insertTestTransaction(storage)
      const e = await _tu.insertTestOutput(storage, t, 0, 101)
      const id = e.outputId
      expect(id).toBeGreaterThan(0)
      expect(e.userId).toBe(t.userId)
      expect(e.transactionId).toBe(t.transactionId)
      expect(e.vout).toBe(0)
      expect(e.satoshis).toBe(101)
      // duplicate must throw
      e.outputId = 0
      await expect(storage.insertOutput(e)).rejects.toThrow()
      e.vout = 1
      await storage.insertOutput(e)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(e.outputId).toBeGreaterThan(id)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_output(self, storage, user) -> None:
        """Given: Storage provider with test Output data
           When: Insert Output
           Then: Insert succeeds with auto-incremented ID

        Reference: test/storage/insert.test.ts
                  test('8 insert Output')
        """
        tx = {
            "userId": user,
            "txid": "7" * 64,
            "status": "sending",
            "reference": "",
            "is_outgoing": True,
            "satoshis": 5000,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        tx_id = storage.insert_transaction(tx)

        output = {
            "transaction_id": tx_id,
            "userId": user,
            "vout": 0,
            "satoshis": 101,
            "locking_script": [1, 2, 3],
            "spendable": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        output_id = storage.insert_output(output)
        assert output_id > 0
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: e.outputId, e.satoshis, e.transactionId, e.userId, e.vout
  - [HIGH] Python test is missing operations: _tu.insertTestOutput, _tu.insertTestTransaction, storage.insertOutput

**Differences:**
  - Operation count: TS has 3, PY has 0
  - Verification count: TS has 5, PY has 0

**Suggestions:**
  - Add verifications for: e.outputId, e.satoshis, e.transactionId
  - Add operations: _tu.insertTestOutput, _tu.insertTestTransaction, storage.insertOutput

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: e.outputId, e.satoshis, e.transactionId, e.userId, e.vout
  • [HIGH] Python test is missing operations: _tu.insertTestOutput, _tu.insertTestTransaction, storage.insertOutput

Key Differences:
  • Operation count: TS has 3, PY has 0
  • Verification count: TS has 5, PY has 0

---

## Test 508: 9 insert OutputTag **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/insert.test.ts

```typescript
  test('9 insert OutputTag', async () => {
    for (const storage of storages) {
      const u = await _tu.insertTestUser(storage)
      const e = await _tu.insertTestOutputTag(storage, u)
      const id = e.outputTagId
      expect(id).toBeGreaterThan(0)
      expect(e.userId).toBe(u.userId)
      expect(e.tag).toBeTruthy()
      // duplicate must throw
      e.outputTagId = 0
      await expect(storage.insertOutputTag(e)).rejects.toThrow()
      e.tag = randomBytesHex(6)
      await storage.insertOutputTag(e)
      // MySQL counts the failed insertion as a used id, SQLite does not.
      expect(e.outputTagId).toBeGreaterThan(id)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_insert.py

```python
    def test_insert_outputtag(self, storage, user) -> None:
        """Given: Storage provider with test OutputTag data
           When: Insert OutputTag
           Then: Insert succeeds with auto-incremented ID

        Reference: test/storage/insert.test.ts
                  test('9 insert OutputTag')
        """
        tag = {
            "userId": user,
            "tag": "test_tag",
            "is_deleted": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        tag_id = storage.insert_output_tag(tag)
        assert tag_id > 0
```

### AI Analysis Results

**Similarity Score**: 12.00%
  - Structural: 0.00%
  - Semantic: 24.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: e.userId, e.outputTagId, e.tag
  - [HIGH] Python test is missing operations: storage.insertOutputTag, _tu.insertTestUser, _tu.insertTestOutputTag

**Differences:**
  - Operation count: TS has 3, PY has 0
  - Verification count: TS has 3, PY has 0

**Suggestions:**
  - Add verifications for: e.userId, e.outputTagId, e.tag
  - Add operations: storage.insertOutputTag, _tu.insertTestUser, _tu.insertTestOutputTag

**Explanation:**

Overall Similarity: 12.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 24.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: authentication verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: e.userId, e.outputTagId, e.tag
  • [HIGH] Python test is missing operations: storage.insertOutputTag, _tu.insertTestUser, _tu.insertTestOutputTag

Key Differences:
  • Operation count: TS has 3, PY has 0
  • Verification count: TS has 3, PY has 0

---

## Test 509: 0_update ProvenTx **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/update.test.ts

```typescript
  test('0_update ProvenTx', async () => {
    for (const { storage } of setups) {
      const records = await storage.findProvenTxs({ partial: {} })
      const time = new Date('2001-01-02T12:00:00.000Z')
      for (const record of records) {
        await storage.updateProvenTx(record.provenTxId, {
          blockHash: 'fred',
          updated_at: time
        })
        const t = verifyOne(
          await storage.findProvenTxs({
            partial: { provenTxId: record.provenTxId }
          })
        )
        expect(t.provenTxId).toBe(record.provenTxId)
        expect(t.blockHash).toBe('fred')
        expect(t.updated_at.getTime()).toBe(time.getTime())
      }
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_update.py

```python
def test_update_proventx(storage_seeded) -> None:
    storage, seed = storage_seeded
    record = seed["proven_tx"]
    new_time = datetime(2001, 1, 2, 12, 0, 0)

    updated = storage.update_proven_tx(
        record["provenTxId"],
        {
            "blockHash": "updated-block-hash",
            "updatedAt": new_time,
        },
    )
    assert updated == 1

    refreshed = _first(storage.find_proven_txs({"partial": {"provenTxId": record["provenTxId"]}}))
    assert refreshed["blockHash"] == "updated-block-hash"
    assert refreshed["updatedAt"] == new_time
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: t.blockHash, t.provenTxId
  - [HIGH] Python test is missing operations: storage.updateProvenTx, storage.findProvenTxs

**Differences:**
  - Operation count: TS has 3, PY has 0

**Suggestions:**
  - Add verifications for: t.blockHash, t.provenTxId
  - Add operations: storage.updateProvenTx, storage.findProvenTxs

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: t.blockHash, t.provenTxId
  • [HIGH] Python test is missing operations: storage.updateProvenTx, storage.findProvenTxs

Key Differences:
  • Operation count: TS has 3, PY has 0

---

## Test 510: 10_update OutputTag **PASS**

- TypeScript: `wallet-toolbox/test/storage/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 511: 11_update OutputTagMap **PASS**

- TypeScript: `wallet-toolbox/test/storage/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 512: 12_update TxLabel **PASS**

- TypeScript: `wallet-toolbox/test/storage/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 513: 13_update TxLabelMap **PASS**

- TypeScript: `wallet-toolbox/test/storage/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 514: 14_update MonitorEvent **PASS**

- TypeScript: `wallet-toolbox/test/storage/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 515: 15_update SyncState **PASS**

- TypeScript: `wallet-toolbox/test/storage/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 516: 1_update ProvenTx **PASS**

- TypeScript: `wallet-toolbox/test/storage/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 517: 2_update ProvenTxReq **PASS**

- TypeScript: `wallet-toolbox/test/storage/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 518: 3_update User **PASS**

- TypeScript: `wallet-toolbox/test/storage/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 519: 4_update Certificate **PASS**

- TypeScript: `wallet-toolbox/test/storage/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 520: 5_update CertificateField **PASS**

- TypeScript: `wallet-toolbox/test/storage/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 521: 6_update OutputBasket **PASS**

- TypeScript: `wallet-toolbox/test/storage/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 522: 7_update Transaction **PASS**

- TypeScript: `wallet-toolbox/test/storage/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 523: 8_update Commission **PASS**

- TypeScript: `wallet-toolbox/test/storage/update.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 524: 9_update Output **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/update.test.ts

```typescript
  test('9_update Output', async () => {
    const primaryKey = 'outputId'
    for (const { storage } of setups) {
      const records = await storage.findOutputs({ partial: {} })
      for (const record of records) {
        if (!record.transactionId) record.transactionId = 1
        if (!record.basketId) record.basketId = 1
        if (!record.userId || !record.transactionId || !record.basketId) {
          throw new Error(`Missing required foreign keys for record ${JSON.stringify(record)}`)
        }
      }
      for (const record of records) {
        const existingRecords = await storage.findOutputs({ partial: {} })
        const usedCombinations = new Set(existingRecords.map(r => `${r.transactionId}-${r.vout}-${r.userId}`))
        let testTransactionId = record.transactionId
        let testVout = record.vout + 1
        let testUserId = record.userId
        while (usedCombinations.has(`${testTransactionId}-${testVout}-${testUserId}`)) {
          testVout += 1
        }
        try {
          const testValues: TableOutput = {
            outputId: record.outputId,
            basketId: record.basketId ?? 1,
            transactionId: testTransactionId,
            userId: testUserId,
            vout: testVout,
            created_at: new Date('2024-12-30T23:00:00Z'),
            updated_at: new Date('2024-12-30T23:05:00Z'),
            change: true,
            customInstructions: 'Updated instructions',
            derivationPrefix: 'updated_prefix==',
            derivationSuffix: 'updated_suffix==',
            lockingScript: [0x01, 0x02, 0x03, 0x04],
            providedBy: 'you',
            purpose: 'updated_purpose',
            satoshis: 3000,
            scriptLength: 150,
            scriptOffset: 5,
            senderIdentityKey: 'updated_sender_key',
            sequenceNumber: 10,
            spendingDescription: 'Updated spending description',
            spendable: false,
            spentBy: 3,
            txid: 'updated_txid',
            type: 'updated_type',
            outputDescription: 'outputDescription'
          }
          const updateResult = await storage.updateOutput(record.outputId, testValues)
          expect(updateResult).toBe(1)
          const updatedRecords = await storage.findOutputs({
            partial: { outputId: record.outputId }
          })
          const updatedRow = verifyOne(
            updatedRecords,
            `Updated Output with outputId=${record.outputId} was not unique or missing.`
          )
          for (const [key, value] of Object.entries(testValues)) {
            const actualValue = updatedRow[key]
            const normalizedActual = normalizeDate(actualValue)
            const normalizedExpected = normalizeDate(value)
            if (normalizedActual && normalizedExpected) {
              expect(normalizedActual).toBe(normalizedExpected)
              continue
            }
            if (Buffer.isBuffer(actualValue) || Array.isArray(actualValue)) {
              expect(JSON.stringify({ type: 'Buffer', data: actualValue })).toStrictEqual(JSON.stringify(value))
              continue
            }
            expect(actualValue).toBe(value)
          }
        } catch (error: any) {
          console.error(`Error updating or verifying Output record with outputId=${record[primaryKey]}:`, error.message)
          throw error
        }
      }
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_update.py

```python
def test_update_output(storage_seeded) -> None:
    storage, seed = storage_seeded
    output = seed["outputs"]["o1"]
    updated = storage.update_output(
        output["outputId"],
        {
            "spendable": False,
            "purpose": "updated-purpose",
        },
    )
    assert updated == 1

    refreshed = _first(storage.find_outputs({"partial": {"outputId": output["outputId"]}}))
    assert refreshed["spendable"] is False
    assert refreshed["purpose"] == "updated-purpose"
```

### AI Analysis Results

**Similarity Score**: 42.00%
  - Structural: 0.00%
  - Semantic: 84.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing operations: storage.updateOutput, storage.findOutputs

**Differences:**
  - Operation count: TS has 4, PY has 0
  - Verification count: TS has 0, PY has 2

**Suggestions:**
  - Add operations: storage.updateOutput, storage.findOutputs

**Explanation:**

Overall Similarity: 42.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 84.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: authentication verification key_change
  • Python: verification

Critical Issues (1):
  • [HIGH] Python test is missing operations: storage.updateOutput, storage.findOutputs

Key Differences:
  • Operation count: TS has 4, PY has 0
  • Verification count: TS has 0, PY has 2

---

## Test 525: 10_update User trigger DB unique constraint errors **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/update2.test.ts

```typescript
  test('10_update User trigger DB unique constraint errors', async () => {
    await createDB('User10')
    for (const { storage } of setups) {
      try {
        const r = await storage.updateUser(2, {
          identityKey: 'mockDupIdentityKey'
        })
        await expect(Promise.resolve(r)).resolves.toBe(1)
      } catch (error: any) {
        console.error('Error updating second record:', error.message)
        return
      }
      const r1 = await triggerUniqueConstraintError(storage, 'findUsers', 'updateUser', 'users', 'userId', {
        userId: 2
      })
      await expect(Promise.resolve(r1)).resolves.toBe(true)
      const r2 = await triggerUniqueConstraintError(storage, 'findUsers', 'updateUser', 'users', 'userId', {
        identityKey: 'mockDupIdentityKey'
      })
      await expect(Promise.resolve(r2)).resolves.toBe(true)
      const r3 = await triggerUniqueConstraintError(storage, 'findUsers', 'updateUser', 'users', 'userId', {
        identityKey: 'mockUniqueIdentityKey'
      })
      await expect(Promise.resolve(r3)).resolves.toBe(false)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_update_advanced.py

```python
    def test_update_user_trigger_db_unique_constraint_errors(self) -> None:
        """Given: Mock storage with multiple User records
           When: Update to duplicate unique field values
           Then: Triggers unique constraint error

        Reference: test/storage/update2.test.ts
                  test('10_update User trigger DB unique constraint errors')
        """
        # Given

        mock_storage = type(
            "MockStorage", (), {"update_user": lambda self, id, updates: Exception("UNIQUE constraint failed")}
        )()

        # When/Then - should trigger unique constraint error
        with pytest.raises(Exception):
            mock_storage.update_user(2, {"identityKey": "mockDupIdentityKey"})
```

### AI Analysis Results

**Similarity Score**: 30.00%
  - Structural: 0.00%
  - Semantic: 60.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  - [HIGH] Python test is missing operations: storage.updateUser

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'verification'
  - Add operations: storage.updateUser

**Explanation:**

Overall Similarity: 30.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 60.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification
  • Python: general_test

Critical Issues (2):
  • [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  • [HIGH] Python test is missing operations: storage.updateUser

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 526: 11_update User trigger DB foreign key constraint errors **PASS**

- TypeScript: `wallet-toolbox/test/storage/update2.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update_advanced.py`

---

## Test 527: 12_update User table setting individual values **PASS**

- TypeScript: `wallet-toolbox/test/storage/update2.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update_advanced.py`

---

## Test 528: 13_update Certificate **PASS**

- TypeScript: `wallet-toolbox/test/storage/update2.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 529: 14_update Certificate set created_at and updated_at time **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/update2.test.ts

```typescript
  test('14_update Certificate set created_at and updated_at time', async () => {
    await createDB('Certificate14')
    for (const { storage } of setups) {
      const scenarios = [
        {
          description: 'Invalid created_at time',
          updates: {
            created_at: new Date('3000-01-01T00:00:00Z'),
            updated_at: new Date('2024-12-30T23:05:00Z')
          }
        },
        {
          description: 'Invalid updated_at time',
          updates: {
            created_at: new Date('2024-12-30T23:00:00Z'),
            updated_at: new Date('3000-01-01T00:00:00Z')
          }
        },
        {
          description: 'created_at time overwrites updated_at time',
          updates: {
            created_at: new Date('2024-12-30T23:00:00Z'),
            updated_at: new Date('2024-12-30T23:05:00Z')
          }
        }
      ]
      for (const { updates } of scenarios) {
        const referenceTime = new Date()
        const records = await storage.findCertificates({ partial: {} })
        for (const record of records) {
          await storage.updateUser(record.certificateId, {
            created_at: updates.created_at
          })
          await storage.updateUser(record.certificateId, {
            updated_at: updates.updated_at
          })
          const t = verifyOne(
            await storage.findCertificates({
              partial: { certificateId: record.certificateId }
            })
          )
          expect(validateUpdateTime(t.created_at, updates.created_at, referenceTime)).toBe(true)
          expect(validateUpdateTime(t.updated_at, updates.updated_at, referenceTime)).toBe(true)
        }
      }
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_update_advanced.py

```python
    def test_update_certificate_set_created_at_and_updated_at_time(self) -> None:
        """Given: Mock storage with existing Certificate records
           When: Update with invalid timestamp scenarios
           Then: Handles timestamp validation correctly

        Reference: test/storage/update2.test.ts
                  test('14_update Certificate set created_at and updated_at time')
        """
        # Given

        mock_storage = type(
            "MockStorage",
            (),
            {
                "find_certificates": lambda self, query: [{"certificateId": 1}],
                "update_certificate": lambda self, id, updates: 1,
            },
        )()

        scenarios = [
            {
                "description": "Invalid created_at time",
                "updates": {
                    "created_at": datetime(3000, 1, 1, 0, 0, 0),
                    "updated_at": datetime(2024, 12, 30, 23, 5, 0),
                },
            },
            {
                "description": "Invalid updated_at time",
                "updates": {
                    "created_at": datetime(2024, 12, 30, 23, 0, 0),
                    "updated_at": datetime(3000, 1, 1, 0, 0, 0),
                },
            },
        ]

        # When/Then
        records = mock_storage.find_certificates({"partial": {}})
        for record in records:
            for scenario in scenarios:
                mock_storage.update_certificate(record["certificateId"], scenario["updates"])
```

### AI Analysis Results

**Similarity Score**: 30.00%
  - Structural: 0.00%
  - Semantic: 60.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  - [HIGH] Python test is missing operations: storage.findCertificates, storage.updateUser

**Differences:**
  - Operation count: TS has 4, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'verification'
  - Add operations: storage.findCertificates, storage.updateUser

**Explanation:**

Overall Similarity: 30.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 60.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification
  • Python: general_test

Critical Issues (2):
  • [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  • [HIGH] Python test is missing operations: storage.findCertificates, storage.updateUser

Key Differences:
  • Operation count: TS has 4, PY has 0

---

## Test 530: 15_update Certificate trigger DB unique constraint errors **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/update2.test.ts

```typescript
  test('15_update Certificate trigger DB unique constraint errors', async () => {
    await createDB('Certificate15')
    for (const { storage } of setups) {
      const initMockDupValues = {
        userId: 2,
        type: `mockType2`,
        certifier: `mockCertifier2`,
        serialNumber: `mockSerialNumber2`
      }
      try {
        const r = await storage.updateCertificate(2, initMockDupValues)
        await expect(Promise.resolve(r)).resolves.toBe(1)
      } catch (error: any) {
        console.error('Error updating second record:', error.message)
      }
      const mockDupValues = {
        userId: 2,
        type: `mockType2`,
        certifier: `mockCertifier2`,
        serialNumber: `mockSerialNumber2`
      }
      const mockUniqueValues = {
        userId: 2,
        type: `mockTypeUnique`,
        certifier: `mockCertifier2`,
        serialNumber: `mockSerialNumber2`
      }
      const r1 = await triggerUniqueConstraintError(
        storage,
        'findCertificates',
        'updateCertificate',
        'certificates',
        'certificateId',
        { certificateId: 2 }
      )
      await expect(Promise.resolve(r1)).resolves.toBe(true)
      const r2 = await triggerUniqueConstraintError(
        storage,
        'findCertificates',
        'updateCertificate',
        'certificates',
        'certificateId',
        mockDupValues
      )
      await expect(Promise.resolve(r2)).resolves.toBe(true)
      const r3 = await triggerUniqueConstraintError(
        storage,
        'findCertificates',
        'updateCertificate',
        'certificates',
        'certificateId',
        mockUniqueValues
      )
      await expect(Promise.resolve(r3)).resolves.toBe(false)
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_update_advanced.py

```python
    def test_update_certificate_trigger_db_unique_constraint_errors(self) -> None:
        """Given: Mock storage with multiple Certificate records
           When: Update to duplicate unique field values
           Then: Triggers unique constraint error

        Reference: test/storage/update2.test.ts
                  test('15_update Certificate trigger DB unique constraint errors')
        """
        # Given

        mock_storage = type(
            "MockStorage", (), {"update_certificate": lambda self, id, updates: Exception("UNIQUE constraint failed")}
        )()

        # When/Then - should trigger unique constraint error
        with pytest.raises(Exception):
            mock_storage.update_certificate(2, {"serialNumber": "mockDupSerial"})
```

### AI Analysis Results

**Similarity Score**: 30.00%
  - Structural: 0.00%
  - Semantic: 60.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  - [HIGH] Python test is missing operations: storage.updateCertificate

**Differences:**
  - Operation count: TS has 1, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'verification'
  - Add operations: storage.updateCertificate

**Explanation:**

Overall Similarity: 30.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 60.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification
  • Python: general_test

Critical Issues (2):
  • [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  • [HIGH] Python test is missing operations: storage.updateCertificate

Key Differences:
  • Operation count: TS has 1, PY has 0

---

## Test 531: 16_update Certificate trigger DB foreign key constraint errors **PASS**

- TypeScript: `wallet-toolbox/test/storage/update2.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update_advanced.py`

---

## Test 532: 1_update ProvenTx **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/update2.test.ts

```typescript
  test('1_update ProvenTx', async () => {
    await createDB('ProvenTx1')
    for (const { storage } of setups) {
      const records = await storage.findProvenTxs({ partial: {} })
      const time = new Date('2001-01-02T12:00:00.000Z')
      for (const record of records) {
        await storage.updateProvenTx(record.provenTxId, {
          blockHash: 'fred',
          updated_at: time
        })
        const t = verifyOne(
          await storage.findProvenTxs({
            partial: { provenTxId: record.provenTxId }
          })
        )
        expect(t.provenTxId).toBe(record.provenTxId)
        expect(t.blockHash).toBe('fred')
        expect(t.updated_at.getTime()).toBe(time.getTime())
      }
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_update.py

```python
def test_update_proventx(storage_seeded) -> None:
    storage, seed = storage_seeded
    record = seed["proven_tx"]
    new_time = datetime(2001, 1, 2, 12, 0, 0)

    updated = storage.update_proven_tx(
        record["provenTxId"],
        {
            "blockHash": "updated-block-hash",
            "updatedAt": new_time,
        },
    )
    assert updated == 1

    refreshed = _first(storage.find_proven_txs({"partial": {"provenTxId": record["provenTxId"]}}))
    assert refreshed["blockHash"] == "updated-block-hash"
    assert refreshed["updatedAt"] == new_time
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: t.blockHash, t.provenTxId
  - [HIGH] Python test is missing operations: storage.updateProvenTx, storage.findProvenTxs

**Differences:**
  - Operation count: TS has 3, PY has 0

**Suggestions:**
  - Add verifications for: t.blockHash, t.provenTxId
  - Add operations: storage.updateProvenTx, storage.findProvenTxs

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: t.blockHash, t.provenTxId
  • [HIGH] Python test is missing operations: storage.updateProvenTx, storage.findProvenTxs

Key Differences:
  • Operation count: TS has 3, PY has 0

---

## Test 533: 2_update ProvenTx **PASS**

- TypeScript: `wallet-toolbox/test/storage/update2.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 534: 3_update ProvenTx set created_at and updated_at time **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/update2.test.ts

```typescript
  test('3_update ProvenTx set created_at and updated_at time', async () => {
    await createDB('ProvenTx3')
    for (const { storage } of setups) {
      const scenarios = [
        {
          description: 'Invalid created_at time',
          updates: {
            created_at: new Date('3000-01-01T00:00:00Z'),
            updated_at: new Date('2024-12-30T23:05:00Z')
          }
        },
        {
          description: 'Invalid updated_at time',
          updates: {
            created_at: new Date('2024-12-30T23:00:00Z'),
            updated_at: new Date('3000-01-01T00:00:00Z')
          }
        },
        {
          description: 'created_at time overwrites updated_at time',
          updates: {
            created_at: new Date('2024-12-30T23:00:00Z'),
            updated_at: new Date('2024-12-30T23:05:00Z')
          }
        }
      ]
      for (const { updates } of scenarios) {
        const referenceTime = new Date()
        const records = await storage.findProvenTxs({ partial: {} })
        for (const record of records) {
          await storage.updateProvenTx(record.provenTxId, {
            created_at: updates.created_at
          })
          await storage.updateProvenTx(record.provenTxId, {
            updated_at: updates.updated_at
          })
          const t = verifyOne(
            await storage.findProvenTxs({
              partial: { provenTxId: record.provenTxId }
            })
          )
          expect(validateUpdateTime(t.created_at, updates.created_at, referenceTime, 10, false)).toBe(true)
          expect(validateUpdateTime(t.updated_at, updates.updated_at, referenceTime, 10, false)).toBe(true)
        }
      }
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_update_advanced.py

```python
    def test_update_proventx_set_created_at_and_updated_at_time(self) -> None:
        """Given: Mock storage with existing ProvenTx records
           When: Update with invalid or edge case timestamps
           Then: Handles timestamp validation correctly

        Reference: test/storage/update2.test.ts
                  test('3_update ProvenTx set created_at and updated_at time')
        """
        # Given

        mock_storage = type(
            "MockStorage",
            (),
            {
                "find_proven_txs": lambda self, query: [{"provenTxId": 1}],
                "update_proven_tx": lambda self, id, updates: 1,
            },
        )()

        scenarios = [
            {
                "description": "Invalid created_at time",
                "updates": {
                    "created_at": datetime(3000, 1, 1, 0, 0, 0),
                    "updated_at": datetime(2024, 12, 30, 23, 5, 0),
                },
            },
            {
                "description": "Invalid updated_at time",
                "updates": {
                    "created_at": datetime(2024, 12, 30, 23, 0, 0),
                    "updated_at": datetime(3000, 1, 1, 0, 0, 0),
                },
            },
        ]

        # When/Then
        records = mock_storage.find_proven_txs({"partial": {}})
        for record in records:
            for scenario in scenarios:
                # Should handle invalid timestamps appropriately
                mock_storage.update_proven_tx(record["provenTxId"], scenario["updates"])
```

### AI Analysis Results

**Similarity Score**: 30.00%
  - Structural: 0.00%
  - Semantic: 60.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  - [HIGH] Python test is missing operations: storage.updateProvenTx, storage.findProvenTxs

**Differences:**
  - Operation count: TS has 4, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'verification'
  - Add operations: storage.updateProvenTx, storage.findProvenTxs

**Explanation:**

Overall Similarity: 30.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 60.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification
  • Python: general_test

Critical Issues (2):
  • [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  • [HIGH] Python test is missing operations: storage.updateProvenTx, storage.findProvenTxs

Key Differences:
  • Operation count: TS has 4, PY has 0

---

## Test 535: 4_update ProvenTx setting individual values **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/update2.test.ts

```typescript
  test('4_update ProvenTx setting individual values', async () => {
    await createDB('ProvenTx4')
    for (const { storage } of setups) {
      const initialRecord: TableProvenTx = {
        provenTxId: 3,
        txid: 'mockTxid',
        created_at: new Date(),
        updated_at: new Date(),
        blockHash: '',
        height: 1,
        index: 1,
        merklePath: [],
        merkleRoot: '',
        rawTx: []
      }
      try {
        const r = await storage.insertProvenTx(initialRecord)
        expect(r).toBeGreaterThan(0)
        const insertedRecords = await storage.findProvenTxs({ partial: {} })
        expect(insertedRecords.length).toBeGreaterThan(0)
        const foundRecord = insertedRecords.find(record => record.provenTxId === 3)
        expect(foundRecord).toBeDefined()
        expect(foundRecord?.txid).toBe('mockTxid')
      } catch (error: any) {
        console.error('Error inserting initial record:', (error as Error).message)
        return
      }
      await expect(storage.updateProvenTx(1, { provenTxId: 0 })).rejects.toThrow(/FOREIGN KEY constraint failed/)
      const r1 = await storage.updateProvenTx(3, { provenTxId: 0 })
      await expect(Promise.resolve(r1)).resolves.toBe(1)
      const r2 = await storage.findProvenTxs({ partial: {} })
      expect(r2[0].provenTxId).toBe(0)
      expect(r2[1].provenTxId).toBe(1)
      const r3 = await storage.updateProvenTx(0, { provenTxId: 3 })
      await expect(Promise.resolve(r3)).resolves.toBe(1)
      const r4 = await storage.findProvenTxs({ partial: {} })
      expect(r4[0].provenTxId).toBe(1)
      expect(r4[1].provenTxId).toBe(3)
      const r8 = await storage.updateProvenTx(3, { txid: 'mockValidTxid' })
      await expect(Promise.resolve(r8)).resolves.toBe(1)
      const r9 = await storage.findProvenTxs({ partial: {} })
      expect(r9.find(r => r.provenTxId === 3)?.txid).toBe('mockValidTxid')
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_update_advanced.py

```python
    def test_update_proventx_setting_individual_values(self) -> None:
        """Given: Mock storage with newly inserted ProvenTx
           When: Update individual fields one at a time
           Then: Each field update works correctly

        Reference: test/storage/update2.test.ts
                  test('4_update ProvenTx setting individual values')
        """
        # Given

        mock_storage = type(
            "MockStorage",
            (),
            {
                "insert_proven_tx": lambda self, record: 3,
                "find_proven_txs": lambda self, query: [{"provenTxId": 3}],
                "update_proven_tx": lambda self, id, updates: 1,
            },
        )()

        initial_record = {
            "provenTxId": 3,
            "txid": "mockTxid",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "blockHash": "",
            "height": 1,
            "index": 1,
            "merklePath": [],
            "merkleRoot": "",
            "rawTx": [],
        }

        # When
        result = mock_storage.insert_proven_tx(initial_record)
        assert result > 0

        # Then - can update individual fields
        mock_storage.update_proven_tx(3, {"blockHash": "newHash"})
        mock_storage.update_proven_tx(3, {"height": 12345})
```

### AI Analysis Results

**Similarity Score**: 13.33%
  - Structural: 0.00%
  - Semantic: 26.67%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Python test is missing verifications: inserted_records.length
  - [HIGH] Python test is missing operations: storage.updateProvenTx, storage.insertProvenTx, storage.findProvenTxs

**Differences:**
  - Operation count: TS has 8, PY has 0
  - Verification count: TS has 1, PY has 0

**Suggestions:**
  - Add verifications for: inserted_records.length
  - Add operations: storage.updateProvenTx, storage.insertProvenTx, storage.findProvenTxs

**Explanation:**

Overall Similarity: 13.3%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 26.7% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: verification

Critical Issues (2):
  • [HIGH] Python test is missing verifications: inserted_records.length
  • [HIGH] Python test is missing operations: storage.updateProvenTx, storage.insertProvenTx, storage.findProvenTxs

Key Differences:
  • Operation count: TS has 8, PY has 0
  • Verification count: TS has 1, PY has 0

---

## Test 536: 5_update ProvenTxReq **PASS**

- TypeScript: `wallet-toolbox/test/storage/update2.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 537: 6_update ProvenTxReq set created_at and updated_at time **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/update2.test.ts

```typescript
  test('6_update ProvenTxReq set created_at and updated_at time', async () => {
    await createDB('ProvenTxReq6')
    for (const { storage } of setups) {
      const scenarios = [
        {
          description: 'Invalid created_at time',
          updates: {
            created_at: new Date('3000-01-01T00:00:00Z'),
            updated_at: new Date('2024-12-30T23:05:00Z')
          }
        },
        {
          description: 'Invalid updated_at time',
          updates: {
            created_at: new Date('2024-12-30T23:00:00Z'),
            updated_at: new Date('3000-01-01T00:00:00Z')
          }
        },
        {
          description: 'created_at time overwrites updated_at time',
          updates: {
            created_at: new Date('2024-12-30T23:00:00Z'),
            updated_at: new Date('2024-12-30T23:05:00Z')
          }
        }
      ]
      for (const { updates } of scenarios) {
        const referenceTime = new Date()
        const records = await storage.findProvenTxReqs({ partial: {} })
        for (const record of records) {
          await storage.updateProvenTxReq(record.provenTxReqId, {
            created_at: updates.created_at
          })
          await storage.updateProvenTxReq(record.provenTxReqId, {
            updated_at: updates.updated_at
          })
          const t = verifyOne(
            await storage.findProvenTxReqs({
              partial: { provenTxReqId: record.provenTxReqId }
            })
          )
          expect(validateUpdateTime(t.created_at, updates.created_at, referenceTime)).toBe(true)
          expect(validateUpdateTime(t.updated_at, updates.updated_at, referenceTime)).toBe(true)
        }
      }
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_update_advanced.py

```python
    def test_update_proventxreq_set_created_at_and_updated_at_time(self) -> None:
        """Given: Mock storage with existing ProvenTxReq records
           When: Update with invalid timestamp scenarios
           Then: Handles timestamp validation correctly

        Reference: test/storage/update2.test.ts
                  test('6_update ProvenTxReq set created_at and updated_at time')
        """
        # Given

        mock_storage = type(
            "MockStorage",
            (),
            {
                "find_proven_tx_reqs": lambda self, query: [{"provenTxReqId": 1}],
                "update_proven_tx_req": lambda self, id, updates: 1,
            },
        )()

        scenarios = [
            {
                "description": "Invalid created_at time",
                "updates": {
                    "created_at": datetime(3000, 1, 1, 0, 0, 0),
                    "updated_at": datetime(2024, 12, 30, 23, 5, 0),
                },
            },
            {
                "description": "Invalid updated_at time",
                "updates": {
                    "created_at": datetime(2024, 12, 30, 23, 0, 0),
                    "updated_at": datetime(3000, 1, 1, 0, 0, 0),
                },
            },
        ]

        # When/Then
        records = mock_storage.find_proven_tx_reqs({"partial": {}})
        for record in records:
            for scenario in scenarios:
                mock_storage.update_proven_tx_req(record["provenTxReqId"], scenario["updates"])
```

### AI Analysis Results

**Similarity Score**: 30.00%
  - Structural: 0.00%
  - Semantic: 60.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  - [HIGH] Python test is missing operations: storage.findProvenTxReqs, storage.updateProvenTxReq

**Differences:**
  - Operation count: TS has 4, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'verification'
  - Add operations: storage.findProvenTxReqs, storage.updateProvenTxReq

**Explanation:**

Overall Similarity: 30.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 60.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification
  • Python: general_test

Critical Issues (2):
  • [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  • [HIGH] Python test is missing operations: storage.findProvenTxReqs, storage.updateProvenTxReq

Key Differences:
  • Operation count: TS has 4, PY has 0

---

## Test 538: 7_update ProvenTxReq setting individual values **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/update2.test.ts

```typescript
  test('7_update ProvenTxReq setting individual values', async () => {
    await createDB('ProvenTxReq7')
    for (const { storage } of setups) {
      const referenceTime = new Date()
      const initialRecord: TableProvenTxReq = {
        provenTxReqId: 3,
        provenTxId: 1,
        batch: 'batch',
        status: 'nosend',
        txid: 'mockTxid1',
        created_at: referenceTime,
        updated_at: referenceTime,
        attempts: 0,
        history: '{}',
        inputBEEF: [],
        notified: false,
        notify: '{}',
        rawTx: []
      }
      await storage.insertProvenTxReq(initialRecord)
      const secondRecord: TableProvenTxReq = {
        ...initialRecord,
        provenTxReqId: 4,
        txid: 'mockTxid2'
      }
      await storage.insertProvenTxReq(secondRecord)
      const recordToUpdate3 = await storage.findProvenTxReqs({
        partial: { provenTxReqId: 3 }
      })
      expect(recordToUpdate3.length).toBeGreaterThan(0)
      const recordToUpdate4 = await storage.findProvenTxReqs({
        partial: { provenTxReqId: 4 }
      })
      expect(recordToUpdate4.length).toBeGreaterThan(0)
      const r3 = await storage.updateProvenTxReq(3, { batch: 'updatedBatch' })
      await expect(Promise.resolve(r3)).resolves.toBe(1)
      const updatedRecords = await storage.findProvenTxReqs({ partial: {} })
      const updatedBatch = updatedRecords.find(r => r.provenTxReqId === 3)?.batch
      expect(updatedBatch).toBe('updatedBatch')
      try {
        const r4 = await storage.updateProvenTxReq(4, { batch: 'updatedBatch' })
        if (r4 === 0) {
          console.warn('No rows updated. Ensure UNIQUE constraint exists on the batch column if rejection is expected.')
        } else {
          await expect(Promise.resolve(r4)).resolves.toBe(1)
        }
      } catch (error: any) {
        expect(error.message).toMatch(/UNIQUE constraint failed/)
      }
      const r5 = await storage.updateProvenTxReq(3, { txid: 'newValidTxid' })
      await expect(Promise.resolve(r5)).resolves.toBe(1)
      await expect(storage.updateProvenTxReq(4, { txid: 'newValidTxid' })).rejects.toThrow(/UNIQUE constraint failed/)
      const finalRecords = await storage.findProvenTxReqs({ partial: {} })
      expect(finalRecords.find(r => r.provenTxReqId === 4)?.txid).toBe('mockTxid2')
      await storage.updateProvenTxReq(3, { batch: 'batch', txid: 'mockTxid1' })
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_update_advanced.py

```python
    def test_update_proventxreq_setting_individual_values(self) -> None:
        """Given: Mock storage with newly inserted ProvenTxReq records
           When: Update individual fields one at a time
           Then: Each field update works correctly

        Reference: test/storage/update2.test.ts
                  test('7_update ProvenTxReq setting individual values')
        """
        # Given

        mock_storage = type(
            "MockStorage",
            (),
            {"insert_proven_tx_req": lambda self, record: 3, "update_proven_tx_req": lambda self, id, updates: 1},
        )()

        reference_time = datetime.now()
        initial_record = {
            "provenTxReqId": 3,
            "provenTxId": 1,
            "batch": "batch",
            "status": "nosend",
            "txid": "mockTxid1",
            "created_at": reference_time,
            "updated_at": reference_time,
            "attempts": 0,
            "history": "{}",
            "inputBEEF": [],
            "notified": False,
            "notify": "{}",
            "rawTx": [],
        }

        # When
        mock_storage.insert_proven_tx_req(initial_record)

        # Then - can update individual fields
        mock_storage.update_proven_tx_req(3, {"status": "completed"})
        mock_storage.update_proven_tx_req(3, {"attempts": 5})
```

### AI Analysis Results

**Similarity Score**: 0.00%
  - Structural: 0.00%
  - Semantic: 0.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'value_verification verification' but PY verifies 'general_test'
  - [HIGH] Python test is missing verifications: error.message, record_to_update3.length, record_to_update4.length
  - [HIGH] Python test is missing operations: storage.insertProvenTxReq, storage.findProvenTxReqs, storage.updateProvenTxReq

**Differences:**
  - Operation count: TS has 10, PY has 0
  - Verification count: TS has 3, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'value_verification verification'
  - Add verifications for: error.message, record_to_update3.length, record_to_update4.length
  - Add operations: storage.insertProvenTxReq, storage.findProvenTxReqs, storage.updateProvenTxReq

**Explanation:**

Overall Similarity: 0.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 0.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: value_verification verification
  • Python: general_test

Critical Issues (3):
  • [HIGH] Test intent differs: TS verifies 'value_verification verification' but PY verifies 'general_test'
  • [HIGH] Python test is missing verifications: error.message, record_to_update3.length, record_to_update4.length
  • [HIGH] Python test is missing operations: storage.insertProvenTxReq, storage.findProvenTxReqs, storage.updateProvenTxReq

Key Differences:
  • Operation count: TS has 10, PY has 0
  • Verification count: TS has 3, PY has 0

---

## Test 539: 8_update User **PASS**

- TypeScript: `wallet-toolbox/test/storage/update2.test.ts`
- Python: `py-wallet-toolbox/tests/storage/test_update.py`

---

## Test 540: 9_update User set created_at and updated_at time **FAIL**

### TypeScript Test: wallet-toolbox/test/storage/update2.test.ts

```typescript
  test('9_update User set created_at and updated_at time', async () => {
    await createDB('User9')
    for (const { storage } of setups) {
      const scenarios = [
        {
          description: 'Invalid created_at time',
          updates: {
            created_at: new Date('3000-01-01T00:00:00Z'),
            updated_at: new Date('2024-12-30T23:05:00Z')
          }
        },
        {
          description: 'Invalid updated_at time',
          updates: {
            created_at: new Date('2024-12-30T23:00:00Z'),
            updated_at: new Date('3000-01-01T00:00:00Z')
          }
        },
        {
          description: 'created_at time overwrites updated_at time',
          updates: {
            created_at: new Date('2024-12-30T23:00:00Z'),
            updated_at: new Date('2024-12-30T23:05:00Z')
          }
        }
      ]
      for (const { description, updates } of scenarios) {
        const referenceTime = new Date()
        const records = await storage.findUsers({ partial: {} })
        for (const record of records) {
          await storage.updateUser(record.userId, {
            created_at: updates.created_at
          })
          await storage.updateUser(record.userId, {
            updated_at: updates.updated_at
          })
          const t = verifyOne(await storage.findUsers({ partial: { userId: record.userId } }))
          expect(validateUpdateTime(t.created_at, updates.created_at, referenceTime)).toBe(true)
          expect(validateUpdateTime(t.updated_at, updates.updated_at, referenceTime)).toBe(true)
        }
      }
    }
  })
```

### Python Test: py-wallet-toolbox/tests/storage/test_update_advanced.py

```python
    def test_update_user_set_created_at_and_updated_at_time(self) -> None:
        """Given: Mock storage with existing User records
           When: Update with invalid timestamp scenarios
           Then: Handles timestamp validation correctly

        Reference: test/storage/update2.test.ts
                  test('9_update User set created_at and updated_at time')
        """
        # Given

        mock_storage = type(
            "MockStorage",
            (),
            {"find_users": lambda self, query: [{"userId": 1}], "update_user": lambda self, id, updates: 1},
        )()

        scenarios = [
            {
                "description": "Invalid created_at time",
                "updates": {
                    "created_at": datetime(3000, 1, 1, 0, 0, 0),
                    "updated_at": datetime(2024, 12, 30, 23, 5, 0),
                },
            },
            {
                "description": "Invalid updated_at time",
                "updates": {
                    "created_at": datetime(2024, 12, 30, 23, 0, 0),
                    "updated_at": datetime(3000, 1, 1, 0, 0, 0),
                },
            },
        ]

        # When/Then
        records = mock_storage.find_users({"partial": {}})
        for record in records:
            for scenario in scenarios:
                mock_storage.update_user(record["userId"], scenario["updates"])
```

### AI Analysis Results

**Similarity Score**: 30.00%
  - Structural: 0.00%
  - Semantic: 60.00%
  - Alignment: 0.00%

**Critical Issues:**
  - [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  - [HIGH] Python test is missing operations: storage.findUsers, storage.updateUser

**Differences:**
  - Operation count: TS has 4, PY has 0

**Suggestions:**
  - Align test intent: ensure PY test verifies 'verification'
  - Add operations: storage.findUsers, storage.updateUser

**Explanation:**

Overall Similarity: 30.0%
  • Structural: 0.0% (sequence and structure)
  • Semantic: 60.0% (test intent and meaning)
  • Alignment: 0.0% (functional equivalence)

Test Intent:
  • TypeScript: verification
  • Python: general_test

Critical Issues (2):
  • [HIGH] Test intent differs: TS verifies 'verification' but PY verifies 'general_test'
  • [HIGH] Python test is missing operations: storage.findUsers, storage.updateUser

Key Differences:
  • Operation count: TS has 4, PY has 0

---
