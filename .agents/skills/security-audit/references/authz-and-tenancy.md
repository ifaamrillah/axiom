# Authorization, IDOR, and Multi-Tenant Isolation

Open this file when an authenticated principal can name a resource (an ID in a path, body, query, header, file key, or GraphQL argument), when roles differ, or when the product hosts several tenants, organizations, or workspaces in shared storage. This is the most common class of high-impact finding in business software.

## Core rule

Authentication answers "who are you". Authorization answers "may **this** principal do **this** action to **this** resource". For each sensitive operation, find the check that binds all three, at the last trusted decision point, on **every** path to the same effect.

Questions to answer for each resource type:

1. Where does the resource ID come from, and where does the owner or tenant come from? The tenant must come from the authenticated session, never from the request.
2. Is the scope applied **in the query** (`WHERE tenant_id = :session_tenant`), or by a check after load? Both work; a check that runs only on some paths does not.
3. Do list, count, search, export, bulk, nested, and background paths apply the same scope as the single-item path?
4. Can a request body field override authority (`role`, `ownerId`, `tenantId`, `isAdmin`, `verified`, `price`)?

## Where to look

| Stack | Authorization mechanisms | Common gaps |
|---|---|---|
| Express / Node | Custom middleware (`requireRole`), CASL, `accesscontrol`, Prisma middleware or extensions for tenant scope | `findUnique({ where: { id } })` without owner; role checked but not ownership |
| NestJS | Guards (`@UseGuards`), `@Roles`, interceptors | Guard on controller class but a new method added with `@Public()`; guard checks role only |
| Django / DRF | `permission_classes`, `has_object_permission`, `get_queryset`, `django-guardian`, `django-rules` | `get_object()` overridden without `check_object_permissions`; `Model.objects.get(pk=pk)` in a view instead of `self.get_queryset()`; `has_object_permission` not called for list views |
| Flask | Decorators, Flask-Principal, manual checks | Decorator present for login only |
| Rails | Pundit (`authorize`, `policy_scope`), CanCanCan (`load_and_authorize_resource`), `current_user.posts.find(id)` | `Post.find(params[:id])` instead of `current_user.posts.find`; `after_action :verify_authorized` missing |
| Spring | `@PreAuthorize`, `@PostAuthorize`, method security, `SecurityFilterChain` | `@PreAuthorize("hasRole('USER')")` without owner expression; `repository.findById(id)` |
| Laravel | Policies, Gates, `$this->authorize()`, `can` middleware, global scopes | Route-model binding `Order $order` with no policy; `withoutGlobalScope` |
| Go | Handler-level checks, Casbin, OPA | Every handler hand-rolls the check; one forgets |
| GraphQL | Resolver-level checks, directives (`@auth`), DataLoader | Field resolvers on nested types (`order.customer.paymentMethods`) skip checks done at the root |

Search commands:

```bash
# Direct lookups by request-supplied id (then check for owner/tenant scope nearby)
rg -n -e 'findById\(|findByPk\(|findUnique\(\{\s*where:\s*\{\s*id' -e 'objects\.get\(pk=|objects\.get\(id=' -e '\.find\(params\[:id\]\)' -e 'findOrFail\(\$' -e 'First\(&\w+,\s*\w*[iI][dD]\)'
# Escape hatches from scoping
rg -n -e 'unscoped|withoutGlobalScope|all_objects|_base_manager|\.with_deleted|bypassRLS|SET row_security|service_role'
# Mass assignment
rg -n -e 'update\(req\.body\)|create\(req\.body\)|Object\.assign\(\w+,\s*req\.body' -e 'fields\s*=\s*.__all__.' -e 'permit!' -e '\$guarded\s*=\s*\[\]' -e '@RequestBody\s+\w+Entity'
# Tenant derived from the request
rg -n -e "headers\[.x-tenant|headers\.get\(.X-Tenant|req\.(body|query)\.(tenantId|orgId|workspaceId|accountId)"
```

## Classes and examples

### IDOR / BOLA (object-level)

```js
// Vulnerable: any logged-in user can read any invoice
app.get('/api/invoices/:id', requireAuth, async (req, res) => {
  res.json(await prisma.invoice.findUnique({ where: { id: req.params.id } }));
});
// Safe: scope in the query; respond 404 for both missing and foreign
app.get('/api/invoices/:id', requireAuth, async (req, res) => {
  const inv = await prisma.invoice.findFirst({ where: { id: req.params.id, orgId: req.user.orgId } });
  if (!inv) return res.sendStatus(404);
  res.json(inv);
});
```

```python
# Vulnerable (DRF): queryset not scoped; object permission never consulted
class DocView(generics.RetrieveUpdateAPIView):
    queryset = Document.objects.all()
    permission_classes = [IsAuthenticated]
# Safe
class DocView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Document.objects.filter(org=self.request.user.org)
```

```ruby
# Vulnerable
@project = Project.find(params[:id])
# Safe
@project = current_user.projects.find(params[:id])   # raises RecordNotFound for others
```

```go
// Vulnerable
db.First(&order, chi.URLParam(r, "id"))
// Safe
err := db.Where("id = ? AND tenant_id = ?", chi.URLParam(r, "id"), tenantFrom(r.Context())).First(&order).Error
```

UUIDs do not fix IDOR. They raise the cost of guessing, but IDs leak through URLs, logs, emails, shared links, and list endpoints. Report an IDOR on UUIDs at the full severity if any realistic path reveals other tenants' IDs; otherwise note the reduced likelihood.

### Function-level authorization

A regular user reaches an admin or staff operation. Look for admin routes protected only by being absent from the UI, `isAdmin` checks in the frontend only, role checks using a value from the JWT that the user can influence (self-service profile update writes `role`), and "internal" endpoints exposed on the public router.

### Mass assignment / over-posting

```js
// Vulnerable: body {"name":"x","role":"admin","orgId":"victim-org"}
await prisma.user.update({ where: { id: req.user.id }, data: req.body });
// Safe: explicit allowlist via schema
const Body = z.object({ name: z.string().max(100), avatarUrl: z.string().url().optional() }).strict();
await prisma.user.update({ where: { id: req.user.id }, data: Body.parse(req.body) });
```

Framework specifics: Rails `params.permit!` or `permit(:role)`; Django `ModelForm`/`ModelSerializer` with `fields = '__all__'` or missing `read_only_fields`; Laravel `$guarded = []` or `$fillable` including `role`/`is_admin`; Spring binding a JPA entity directly from `@RequestBody` or `@ModelAttribute` (use DTOs, or `@InitBinder setAllowedFields`); Go `json.Unmarshal` into the DB model struct.

### Multi-tenant isolation

Find the single source of the current tenant (subdomain, session, token claim) and verify:

- Every repository/ORM path applies it. Global scopes (Laravel), default managers (Django), Prisma extensions, Hibernate filters (`@Filter`), and Postgres row-level security are good centralizers. Then hunt for the **escape hatches** in the grep above.
- The tenant is not read from a header or body (`X-Tenant-Id`) unless the server checks membership.
- Cache keys, search index queries, object storage paths, queue messages, and file names include the tenant.
- Background jobs re-establish tenant context from the job record, not from a global that the previous job set.
- Postgres RLS: the app role is not a superuser or table owner (owners bypass RLS unless `FORCE ROW LEVEL SECURITY`), and `SET app.tenant_id` is per-transaction (`SET LOCAL`) in pooled connections. Supabase `service_role` keys bypass RLS entirely.
- Unique constraints and lookups by natural keys (`slug`, `email`, `invoice_number`) are composite with tenant.

### Indirect object references in nested and batch paths

- `POST /orders/:orderId/items/:itemId` checks the order belongs to the user, but loads the item by `itemId` alone (item from another order).
- Bulk endpoints (`ids=[1,2,3]`) check the first item only, or none.
- Export, report, and "download all" jobs select by filter with no tenant clause.
- GraphQL `node(id:)` global lookups.
- File download by storage key: `/files?key=tenantA/123.pdf` with no check that the key prefix belongs to the caller.

### Information disclosure through authorization side effects

Different status codes or messages for "exists but forbidden" (403) and "does not exist" (404) let an attacker probe for IDs. Low severity unless the existence itself is sensitive (for example, whether a person is a patient).

## Validate without harm

Use two dummy principals in the **same local test instance**: user A in tenant 1, user B in tenant 2. Create a record as A. As B, call the operation with A's record ID and observe the read or write. This is the standard proof and needs no destructive input. Prefer an existing integration-test harness (`supertest`, DRF `APIClient`, Rails request specs, `MockMvc`, Laravel `actingAs`, Go `httptest`).

For mass assignment, send one extra field (`role: "admin"`) as a dummy user and read the record back.

## False-positive traps

| Looks bad | Check before reporting |
|---|---|
| `findById(id)` with no owner check | The caller may scope later, a policy may run after load, or a DB-level RLS policy may filter. Read the whole handler and the data layer |
| Admin endpoint without a role check in the handler | A router group or gateway may require admin. Check route registration |
| Resource is meant to be public or shared | Read the product intent (public profiles, shared-link documents). Not a finding |
| ID belongs to an object the user already has read access to via another path | Same-principal access; not a boundary crossing |
| Laravel route-model binding | Binding resolves the model; it does not authorize. Check for a policy or `authorize()` call |
| Mass assignment field exists but the ORM ignores unknown or protected fields | Check `attr_protected`, `$fillable`, `read_only_fields`, DTO mapping |

## Severity guidance

| Result | Typical severity |
|---|---|
| Unauthenticated read or write of any tenant's data | Critical |
| Authenticated cross-tenant read or write of sensitive data; self-escalation to admin via mass assignment | High |
| Cross-user read of low-sensitivity data within a tenant; IDOR needing a leaked UUID with no known leak path | Medium |
| Existence oracle on non-sensitive objects | Low |

Fix pattern: derive tenant and owner from the session, scope in the query, use DTO allowlists for writes, centralize scoping, and add a two-tenant regression test.

Sources: adapted from cloudflare/security-audit-skill (MIT), addyosmani/agent-skills (MIT) and general practice.
