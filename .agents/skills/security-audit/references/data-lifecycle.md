# Data Lifecycle: Backup, Restore, Deletion, Export, Retention

Open this file when the application creates copies of data or promises to remove it: backups, restores, exports and downloads, account or tenant deletion, retention rules, and data that moves between tenants. The short questions live in the "Data isolation and lifecycle" section of the [attack-surface checklists](attack-surfaces.md). Query scoping is in [authorization and tenancy](authz-and-tenancy.md); abuse of export and import as product features is in [business logic](business-logic.md).

## The invariant

Every copy of a record follows the rules of the original: who may read it, which tenant owns it, and when it must be gone. A copy that outlives a deletion, or is readable by someone the original was not, is a finding when a lower-trust principal can reach it.

## Stage questions

### Export and download

- Does the export query apply the same tenant and role scope as the list view? Exports often run as background jobs with an unscoped client.
- Does the artifact include hidden fields, deleted records, or columns above the requester's role?
- Where is the artifact stored? Is its path or object key guessable, and does it include the tenant?
- Do signed or shared download links expire, and are they bound to the requester? Can a removed member still download an earlier export?

### Backup

- Where do backups go, and who can read that location (bucket policy, file mode, CI artifacts)? Is the location defined in the repository?
- Are backups encrypted, and is the key stored apart from the backup?
- Do dump scripts include secrets, sessions, or tokens that the application never exposes?

### Restore and import

- Does restore re-apply current ownership and validation, or does it trust the tenant, owner, and role fields in the file?
- Can a tenant restore or import a file that names another tenant's IDs and overwrite their records?
- Does restore bring back users, permissions, or sessions that were revoked after the backup?

### Deletion

- Does account or tenant deletion reach every copy: caches, search indexes, object storage, analytics, logs with personal data, queues, replicas, and exports already generated?
- With soft delete, do all read paths filter deleted rows, including search, exports, admin views, and API list endpoints?
- Do sessions, API keys, OAuth grants, webhooks, and memberships stop working after deletion?

### Retention

- Is a stated retention period enforced in code (a scheduled purge), or only in a policy document?
- Do purges cover derived copies, or only the primary table?

## Search commands

```bash
rg -n -e 'pg_dump|mysqldump|mongodump|backup|snapshot|restore' -l
rg -n -e 'export|to_csv|to_excel|download_all|archive|zip' -g '!*.test.*' -l
rg -n -e 'deleted_at|is_deleted|SoftDeletes|paranoid|acts_as_paranoid|discard|with_deleted|withTrashed' -l
rg -n -e 'presign|generate_presigned_url|getSignedUrl|signed_url|SAS' -l
rg -n -e 'retention|purge|ttl|expire_after|cleanup' -l
```

## Harmless validation

- Export: two dummy tenants on a local instance. Export as tenant A and read the artifact for tenant B's dummy rows or hidden fields.
- Restore and import: craft a dummy file naming tenant B's IDs, import it as tenant A, and check B's dummy records.
- Deletion: delete a dummy account locally, then query each store the code writes to (cache, index, storage path) for its records, and replay its API key.
- Backup location and access rules that live outside the repository make the candidate `needs_validation`, naming the setting and a safe owner check (read the bucket policy; no download of real backups).

## False-positive traps

| Looks bad | Check before reporting |
|---|---|
| Soft-deleted rows still in the table | Expected by design. A finding needs a read path that returns them to someone who should not see them |
| Backups contain all tenants | Normal for operator backups. A finding needs a lower-trust reader of the backup location |
| Logs keep data past the retention period | A compliance gap, not a crossed boundary, unless a lower-trust principal can read those logs. Report as a hardening or compliance note |
| Export includes a field the UI hides | The requester may be allowed to see it through the API. Check the role's read permissions |

## Severity guidance

| Result | Typical severity |
|---|---|
| A tenant can export or restore into another tenant's data | High |
| Backups readable by any authenticated user or publicly | Critical to High, by content |
| Deleted users' sessions or API keys keep working | High |
| A removed member can download an export made before removal | Medium |
| Derived copies outlive deletion, readable only by operators | Hardening or compliance note |

Fix pattern: run exports and restores through the same scoped data layer as requests, put the tenant in every storage key, bind links to the requester with short expiry, rewrite ownership on import from the session, and make deletion a tracked job that covers every store.

Sources: class from cloudflare/security-audit-skill (MIT), rewritten; general practice.
