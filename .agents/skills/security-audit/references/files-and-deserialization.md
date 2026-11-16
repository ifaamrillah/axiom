# File Handling, Path Traversal, Uploads, XXE, and Deserialization

Open this file when untrusted data names a file path, an upload lands on disk or in object storage, the code extracts archives, parses XML, or deserializes bytes into objects (pickle, Java serialization, YAML, PHP `unserialize`, .NET `BinaryFormatter`, polymorphic JSON).

## Path traversal

### Core rule

A path is safe only if the **resolved** path stays under an allowed root. Compare after normalization and symlink resolution, never on the raw string. Removing `../` once is not enough (`....//` becomes `../`).

### Where to look

| Stack | Sinks that take a path |
|---|---|
| Node | `fs.readFile`, `createReadStream`, `res.sendFile`, `res.download`, `path.join(base, input)`, `express.static` with custom roots, `require(input)` |
| Python | `open`, `send_file`, `send_from_directory` (safe), `os.path.join(base, input)` (absolute input discards `base`), `FileResponse`, `shutil` |
| Ruby / Rails | `File.read`, `send_file`, `render file:`, `File.join`, `Pathname#join` |
| Java / Spring | `new File(base, input)`, `Paths.get(base, input)`, `Files.readAllBytes`, `ResourceLoader.getResource("file:" + x)`, `FileSystemResource` |
| PHP / Laravel | `include`/`require` with input (local file inclusion), `file_get_contents`, `fopen`, `readfile`, `Storage::get($input)`, `response()->download` |
| Go | `os.Open(filepath.Join(base, input))`, `http.ServeFile` (rejects `..` in the URL path, not in your own argument), `http.Dir` |

Join pitfalls: Python `os.path.join("/srv", "/etc/passwd")` returns `/etc/passwd`. Node `path.join` normalizes `..`; `path.resolve` with an absolute second argument discards the base. Java `Paths.get(base).resolve(abs)` returns `abs`.

```js
// Vulnerable
app.get('/files', (req, res) => res.sendFile(path.join(UPLOADS, req.query.name)));
// Safe: resolve, then check containment with a separator
const ROOT = path.resolve(UPLOADS);
const target = path.resolve(ROOT, String(req.query.name));
if (!target.startsWith(ROOT + path.sep)) return res.sendStatus(400);
res.sendFile(target);
```

```python
# Safe (Python 3.9+)
root = Path(UPLOADS).resolve()
target = (root / name).resolve()
if not target.is_relative_to(root):
    abort(400)
```

```go
// Go 1.20+: filepath.IsLocal rejects absolute, "..", and reserved names
if !filepath.IsLocal(name) { http.Error(w, "bad path", 400); return }
// Go 1.24+: os.OpenRoot(dir) then root.Open(name) confines access, including symlinks
```

`startsWith(ROOT)` without the separator accepts `/srv/uploads-evil/`. Symlinks inside the root still escape unless you resolve them (`realpath`) or open with no-follow semantics.

### Archive extraction (zip slip)

Entries named `../../app/config.py` or absolute paths write outside the destination. Also check symlink entries and hard links in tar files.

- Python: `tarfile.extractall` without `filter="data"` (Python 3.12+ default warning; 3.14 default is `data`). `zipfile.extractall` sanitizes names, but custom loops over `namelist()` with `open(dest/name)` do not.
- Java: loops over `ZipEntry.getName()` without a canonical-path check.
- Node: `adm-zip`, `unzipper`, `tar` (node-tar has had several traversal CVEs; check version).
- Go: `archive/zip` loops writing `filepath.Join(dst, f.Name)` with no check.

Also bound decompressed size and entry count (zip bombs). See the resource-exhaustion items in the attack-surface checklist.

## File uploads

| Risk | What to check |
|---|---|
| Stored XSS via upload | Files served from the app origin with a browser-renderable type (`text/html`, `image/svg+xml`, `application/xhtml+xml`). Fix: serve from a separate origin, set `Content-Disposition: attachment`, `X-Content-Type-Options: nosniff`, and a fixed content type |
| Server-side execution | Uploads written into a web root that executes scripts (PHP, JSP, ASPX, CGI). Check for extension allowlists **and** that the upload dir does not execute |
| Path control | User-supplied filename used as the storage path. Fix: generate a random key; keep the original name only as metadata |
| Type confusion | Trusting `Content-Type` or extension. Check magic bytes for formats that matter, and re-encode images when practical |
| Parser exploits | ImageMagick, Ghostscript, ExifTool, LibreOffice, FFmpeg processing untrusted files. Check versions and policies (ImageMagick `policy.xml` disabling coders like `MVG`, `MSL`, `URL`, `PS`, `PDF` where unneeded) |
| Overwrite | Predictable keys let one user overwrite another's file. Include tenant and random IDs |
| Size | Missing limits (`multer` `limits.fileSize`, Django `DATA_UPLOAD_MAX_MEMORY_SIZE`, Spring `max-file-size`, PHP `upload_max_filesize`) |

Presigned object-storage uploads: check that the server binds the key, content type, and size in the signature (S3 POST policy conditions), and that the key includes the tenant.

## XML External Entities (XXE)

XML parsers that resolve DTDs and external entities let input read local files or trigger SSRF.

| Stack | Unsafe default or pattern | Safe |
|---|---|---|
| Java | `DocumentBuilderFactory`, `SAXParserFactory`, `XMLInputFactory`, `TransformerFactory`, `SchemaFactory` with default settings | `dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)`; `XMLInputFactory.SUPPORT_DTD=false` |
| Python | `lxml.etree.XMLParser(resolve_entities=True)` (default before lxml 5), `xml.dom.pulldom`/`sax` with external entities enabled | `defusedxml`, or `XMLParser(resolve_entities=False, no_network=True)` |
| PHP | `libxml_disable_entity_loader(false)` on PHP < 8, `LIBXML_NOENT` flag | No `LIBXML_NOENT`; PHP 8+ disables external entity loading by default |
| .NET | `XmlDocument` with `XmlResolver` set on old frameworks | `XmlResolver = null` (default in .NET 4.5.2+) |
| Node | `libxmljs` with `noent: true` | Do not set `noent` |
| Go | `encoding/xml` | Does not resolve external entities |

Hidden XML: SVG uploads, DOCX/XLSX/PPTX (zipped XML), SAML, SOAP, RSS imports, and Office-to-PDF converters.

Python's standard `xml.etree.ElementTree` does not fetch external entities, but older versions are vulnerable to entity-expansion (billion laughs). Use `defusedxml` for untrusted input.

## Insecure deserialization

Deserializers that reconstruct arbitrary types can run code during loading. The question is whether untrusted bytes reach them.

| Stack | Dangerous with untrusted input | Safer alternative |
|---|---|---|
| Python | `pickle.loads`, `cPickle`, `dill`, `joblib.load`, `torch.load` (before `weights_only=True` default in 2.6), `numpy.load(allow_pickle=True)`, `yaml.load` / `yaml.unsafe_load` / `yaml.load(Loader=yaml.Loader)`, `shelve`, `jsonpickle` | `json`, `yaml.safe_load`, `torch.load(weights_only=True)`, safetensors |
| Java | `ObjectInputStream.readObject`, `XMLDecoder`, XStream without allowlist, Jackson `enableDefaultTyping()` / `@JsonTypeInfo(use = Id.CLASS)`, SnakeYAML `new Yaml()` before 2.0, Kryo without registration | JSON to DTOs; `ObjectInputFilter` allowlist (Java 9+); SnakeYAML `SafeConstructor` |
| Ruby | `Marshal.load`, `YAML.load` on Psych < 4 (Psych 4 makes `load` safe), `YAML.unsafe_load`, `Oj.load` in object mode | `JSON.parse`, `YAML.safe_load` |
| PHP | `unserialize($input)` (POP chains via `__wakeup`, `__destruct`), `phar://` paths reaching file functions (PHP < 8) | `json_decode`; `unserialize($x, ['allowed_classes' => false])` |
| .NET | `BinaryFormatter`, `NetDataContractSerializer`, `LosFormatter`, Json.NET `TypeNameHandling` other than `None` | `System.Text.Json`, `TypeNameHandling.None` |
| Node | `node-serialize` `unserialize`, `funcster`, `serialize-javascript` output passed to `eval` | `JSON.parse` |
| Go | `encoding/gob` into interface types is constrained; risk is mostly in custom reflection-based decoders | Typed structs |

Where untrusted bytes hide: cookies and "remember me" tokens (Java, PHP), cache entries an attacker can write (shared Redis/memcached), message queues fed by other tenants, uploaded model files (`.pkl`, `.pt`, `.joblib`), session stores, ViewState, and import files.

Signed blobs are safe to deserialize only if the signature check happens **before** deserialization and the key is secret. Rails cookies signed with a leaked `secret_key_base` and Marshal serializer are an RCE path.

```python
# Vulnerable: cache shared with lower-trust writers
obj = pickle.loads(redis.get(key))
# Safe
obj = json.loads(redis.get(key))
```

## Search commands

```bash
rg -n -e 'sendFile\(|res\.download\(|send_file\(|readFile(Sync)?\(.*req\.|File\.read\(.*params|new File\(.*,\s*\w*(name|path)' -e 'extractall\(|ZipEntry|getNextEntry|adm-zip|unzipper'
rg -n -e 'pickle\.loads?|joblib\.load|torch\.load|yaml\.load\(|yaml\.unsafe_load|Marshal\.load|YAML\.load\(|unserialize\(|ObjectInputStream|readObject\(|XMLDecoder|enableDefaultTyping|TypeNameHandling|BinaryFormatter'
rg -n -e 'DocumentBuilderFactory|SAXParserFactory|XMLInputFactory|resolve_entities|LIBXML_NOENT|noent'
rg -n -i -e 'multer|upload|FileField|MultipartFile|\$_FILES|FormFile\('
```

## Validate without harm

- Path traversal: in a local instance with a fixture tree, request `../` + a **canary file you created** in scratch (for example `scratch/canary.txt`). Do not read `/etc/shadow`, keys, or real config.
- Zip slip: build a tiny archive with an entry `../canary.txt` and extract it with the target code into a scratch directory. Check that the canary lands outside the destination but still inside scratch.
- XXE: parse a document with an entity pointing at a scratch canary file. Do not reference network URLs.
- Deserialization: prove reachability (untrusted bytes reach `pickle.loads`) and, if execution is allowed, use a payload whose only effect is creating a scratch marker file. Do not use public gadget-chain tools against anything but the local fixture, and stop at the marker.

## False-positive traps

| Looks bad | Check before reporting |
|---|---|
| `pickle.load` / `torch.load` | Only a finding if a lower-trust principal supplies the bytes. Loading your own build artifacts is not |
| `yaml.load` in Ruby | Psych 4 (Ruby 3.1+) made `load` safe by default. Check the version |
| `send_from_directory` (Flask) | Uses `safe_join`; traversal is blocked |
| `path.join` with input | Still traversable, but check whether input was already restricted to `[a-z0-9-]` or a UUID |
| XML parsing in Go or modern .NET | External entities are not resolved by default |
| Upload of HTML served with `Content-Disposition: attachment` from a separate domain | Not stored XSS on the app origin |

## Severity guidance

| Result | Typical severity |
|---|---|
| Unauthenticated deserialization RCE; unauthenticated arbitrary file write into an executable location | Critical |
| Authenticated deserialization or upload RCE; arbitrary file read of secrets (keys, `.env`) | High |
| File read limited to non-secret application files; XXE blind with SSRF only; stored XSS via SVG upload on the app origin | Medium to High (XSS rules apply) |
| Traversal limited to a public directory; zip bomb on an authenticated, rate-limited endpoint | Low |

Sources: adapted from cloudflare/security-audit-skill (MIT), addyosmani/agent-skills (MIT) and general practice.
