# store-locking

## Purpose

Advisory file locking that serializes concurrent writes to the task store, preventing data loss when multiple processes (e.g. simultaneous agent invocations) modify tasks.csv at the same time.

## Requirements

### Requirement: Exclusive lock on all store mutations
Every operation that reads and then writes `tasks.csv` (add, update, delete, migrate) SHALL acquire an exclusive advisory lock on a dedicated lock file (`tasks.csv.lock` in the data directory) before reading, hold the lock through the write, and release it after the atomic rename. Read-only operations (load_tasks, list) SHALL NOT be required to acquire the lock.

#### Scenario: Concurrent writes are serialized
- **WHEN** two processes call a mutating store function simultaneously
- **THEN** one blocks until the other completes and no rows are lost or duplicated

#### Scenario: Lock file is created automatically
- **WHEN** a mutating store function is called and `tasks.csv.lock` does not exist
- **THEN** the lock file is created transparently before the lock is acquired

#### Scenario: Read-only load does not block on a held lock
- **WHEN** one process holds the exclusive write lock
- **THEN** another process calling `load_tasks` (read-only) is not blocked

### Requirement: Lock timeout
The lock acquisition SHALL time out after 10 seconds. If the lock cannot be acquired within that window the system SHALL raise a `StoreLockedError` with a message indicating the lock file path.

#### Scenario: Timeout raises StoreLockedError
- **WHEN** a lock is held by another process and a second process attempts acquisition
- **AND** 10 seconds elapse without the lock being released
- **THEN** a `StoreLockedError` is raised in the second process

### Requirement: Lock release on error
If an exception is raised while the lock is held (e.g. during the CSV write), the lock SHALL still be released before the exception propagates.

#### Scenario: Lock released on exception
- **WHEN** an exception occurs during `save_tasks` while the lock is held
- **THEN** the lock is released and a subsequent call to the same store function succeeds
