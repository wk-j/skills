---
name: dotnet-db-performance
description: Review or write .NET code so it performs under production load and data volume, database and EF Core first. Use when adding or changing an EF Core, Dapper, or ADO.NET query, a SaveChanges or bulk write, an index or migration, a DbContext registration, a list or table in a server-rendered UI (Blazor Server, Razor Pages, MVC), an API endpoint, a background job, an outbound HTTP call, or a cache; when a page or endpoint hangs, times out, or slows down under load; when database load, deadlocks, connection-pool exhaustion, memory, or thread-pool starvation is a concern; or when the user asks for a performance review of .NET code. Do not use for client-side JavaScript or non-.NET code.
---

# .NET Database and Application Performance

Most production slowness in line-of-business .NET apps is not a slow algorithm. It is code that works
on the developer's forty rows and collapses on real volume or concurrency — and it usually starts at
the database. Review Part A first on any change that touches data access.

Ask three questions of every change:

- **If this set had a million rows, what would happen?** "Slower" is fine. "Out of memory", "never
  renders", or "connection drops" means the code is wrong, even if it passes today.
- **How many round trips, and does each one use an index?** One indexed query is cheap; the same
  query per row, or a table scan, is not — and neither shows on a dev database.
- **If a hundred requests hit this at once?** Anything that holds a thread, connection, or lock while
  waiting becomes a queue that never drains.

# Part A — Database and EF Core

## 1. Load only what the request needs

- **Aggregate in SQL** (`CountAsync`, `AnyAsync`, `SumAsync`, translated `GroupBy`). Existence is
  `AnyAsync`, not `CountAsync() > 0`.
- **Bound every `ToListAsync`** with a selective `Where`, a `Take`, or a page size. An unbounded one
  needs a comment stating the expected magnitude.
- **Stay `IQueryable` until the end.** `Take` after `ToListAsync`, an `IEnumerable<T>` parameter, or
  `AsEnumerable()` moves every later operator into memory over the full result.
- **Project** (`Select` into a DTO) instead of loading whole entities to read a few columns.
- **Check how local `Contains` translates** — it varies by provider and EF version (inlined constants
  in EF ≤7, one JSON parameter in EF 8–9 on SQL Server, one parameter per value in EF 10, an array in
  Npgsql). If the SQL is an `IN (...)` list that grows with the data, batch it; SQL Server rejects
  more than ~2,100 parameters.
- **Page with a key, not `Skip`,** over large tables and in batch loops — `Skip(n)` re-reads `n` rows
  per page. Always `OrderBy` a unique key before paging.
- **When the whole set is needed, stream it in batches** and fold each batch into running totals, so
  peak memory is one batch:

```csharp
var lastId = 0L;
while (true)
{
    var batch = await query.Where(x => x.Id > lastId).OrderBy(x => x.Id)
        .Take(BatchSize).ToListAsync(ct);
    if (batch.Count == 0) break;
    summary.Fold(batch);                    // update totals; the batch is then discarded
    lastId = batch[^1].Id;
}
```

## 2. Shape queries so the database does the work

- **Never query in a loop over rows.** One query returning N rows beats N queries. A lazy-loaded
  navigation inside a loop is the same N+1 defect.
- **Two or more collection `Include`s** multiply rows (cartesian explosion); use `AsSplitQuery()` or
  separate projections.
- **Keep predicates sargable.** A function on the column defeats its index: `x.Email.ToLower() == e`,
  `x.CreatedAt.Date == d` (use a range instead), `Contains`/`EndsWith` on strings (`LIKE '%…%'`), or a
  parameter type that mismatches the column (`nvarchar` vs `varchar` — set `IsUnicode` correctly).
- **EF Core throws on untranslatable expressions** except in the final `Select`, where they run
  client-side silently. Check `ToQueryString()` whenever the SQL shape is not obvious.
- **Parameterise.** `FromSql` / `FromSqlInterpolated` parameterise; concatenated `FromSqlRaw` breaks
  plan reuse and is SQL injection.

## 3. Tracking and `DbContext` lifetime

- **Read-only queries use `AsNoTracking()`** (or no-tracking as the context default). The change
  tracker costs memory and CPU per entity.
- **One `DbContext` per unit of work.** Scoped per request; in background jobs create one per unit
  with `IServiceScopeFactory` or `IDbContextFactory<T>`. In **Blazor Server** the scope is the whole
  circuit, so always use `IDbContextFactory<T>`. Never a singleton or static.
- **Never share a context across concurrent tasks** — it is not thread-safe.
- **Long loops that track entities** call `ChangeTracker.Clear()` between batches, or memory and
  `SaveChanges` cost grow with the total.
- `AddDbContextPool` helps high-throughput services; pooled contexts must not keep per-request state.

## 4. Writes

- **One `SaveChangesAsync` per unit of work,** not per entity; EF batches the statements.
- **Bulk changes don't load entities:** `ExecuteUpdateAsync` / `ExecuteDeleteAsync`, or the provider's
  bulk copy for large inserts. These bypass the change tracker and `ISaveChangesInterceptor` /
  `SavingChanges`, so audit, soft-delete, or timestamp logic there will not run.
- **Keep transactions short.** Never await HTTP, file I/O, or user input inside a transaction or lock.
- **Prefer optimistic concurrency** (rowversion) for user-edited data.
- **Deadlocks** come from inconsistent table order or missing indexes; fix those. `EnableRetryOnFailure`
  is a safety net, and requires user transactions to run inside the execution strategy.

## 5. Indexes and plans

- **Read the plan** for any new query over a large table before shipping (`EXPLAIN (ANALYZE, BUFFERS)`,
  or SQL Server's actual execution plan; get the SQL from `ToQueryString()`).
- **A scan in a hot path needs an index,** declared with `HasIndex` in the model. Equality columns
  first, then range/order columns; add included columns to make a hot query covering. Index foreign
  keys used in joins. Every index costs writes — add only what the plan justifies.
- **Large-table migrations can lock for minutes.** PostgreSQL `CREATE INDEX CONCURRENTLY` cannot run
  in a transaction — use `IsCreatedConcurrently()` or `suppressTransaction: true`. SQL Server
  `ONLINE = ON` needs Enterprise or Azure SQL. Flag it in the deployment plan.
- **Fast for some parameters, slow for others** suggests parameter sniffing; confirm with the plan.

## 6. Connections and diagnosis

- EF opens a connection per operation, so an idle `DbContext` holds none. An open transaction, an
  unfinished `AsAsyncEnumerable`, or an explicit `OpenConnectionAsync` holds one — never await slow
  I/O while one is held. Pool exhaustion looks like random timeouts while the database is idle.
- All database calls are async and take the request's `CancellationToken`. Raise command timeouts
  per operation, never globally to hide a slow query.
- **Diagnose before optimising.** Log EF commands with durations and count them per request (N+1
  shows as a repeated statement). In production use slow-command interceptors or telemetry, and
  `pg_stat_statements` / Query Store for the costliest queries in total. Test on production-sized
  data. A hanging page is often rendering, not the query — check which.

# Part B — The rest of the application

## 7. Bounded UI and API lists

- Page every list, or bound it and **show the true total** ("100 of 75,371"). Blazor Server sends
  every rendered node over SignalR; an unbounded table hangs the circuit. `Virtualize` with a paging
  `ItemsProvider` is fine.
- **A display bound never changes a count, total, or pass/fail** — those come from the full set.
- Lead with grouped counts; offer a streamed export for full-set needs. API list endpoints return a
  page and a continuation.

## 8. Long work runs in the background

- Anything over a few seconds runs in a `BackgroundService` (e.g. behind a `Channel`), with status in
  a singleton tracker keyed by run. The UI observes and polls; it does not own the work.
- **Component disposal must never cancel the work** — a `CancellationTokenSource` cancelled in
  `Dispose` kills the job when the user refreshes. Only an explicit user action cancels.
- Refuse a second start while one runs; tell the user the work continues after they leave.
- In-process queues are lost on restart and not shared across instances. Fine for re-runnable
  read-only work (say so in a comment). Work that writes needs a durable queue, recovery on startup,
  and a cross-instance guard against running twice.

## 9. Async, resources, and caching

- **Never block on async** (`.Result`, `.Wait()`, `GetAwaiter().GetResult()`); no `async void` outside
  event handlers. Use async I/O everywhere. Blocking starves the thread pool: idle CPU, timeouts.
- Bound concurrent fan-out over data-sized sets (`Parallel.ForEachAsync` with a max degree). Don't
  wrap I/O in `Task.Run`. Use `SemaphoreSlim`, not `lock`, around awaits.
- **`HttpClient` via `IHttpClientFactory`,** never `new` per call. Every outbound call has a timeout.
- No scoped services captured in singletons; dispose what you create.
- **Fix the query before caching it.** Every cache entry has an expiry, a size bound, and a stated
  invalidation rule; per-user data is keyed by user. `HybridCache` prevents stampedes. An unbounded
  `ConcurrentDictionary` cache is a memory leak.

## 10. Hot paths — only where a profiler points

Cached `JsonSerializerOptions` and static or `[GeneratedRegex]` regexes; structured log templates
(no interpolation) with `[LoggerMessage]` on hot paths; `StringBuilder` in loops; `Dictionary` /
`HashSet` instead of repeated list searches; `TryParse` instead of exceptions for expected failures;
stream large payloads instead of buffering. Leave GC and JIT settings at defaults unless measured.

Measure with the right tool: EF command log and query plan for the database; `dotnet-counters`
(thread-pool queue, GC heap, connection pool) for starvation or leaks; `dotnet-trace` for CPU;
`dotnet-gcdump` for memory (a heap full of entities means a long-lived `DbContext`); BenchmarkDotNet
for micro-changes; a load test at realistic concurrency and volume for everything else.

# Before calling it done

- [ ] No query or list is sized by the data rather than the request; bounds state the true total and
      never change a verdict.
- [ ] No query in a loop; read queries are no-tracking or projected.
- [ ] New queries over large tables use an index; the plan was checked on realistic data.
- [ ] Writes are batched or set-based; transactions never span slow I/O.
- [ ] Each `DbContext` lives for one unit of work and is never shared across threads.
- [ ] Long work survives refresh and disconnects; disposal cancels only UI polling.
- [ ] No blocking on async; outbound calls use pooled clients with timeouts; caches are bounded.
- [ ] Verified at realistic volume and concurrency — state the numbers.

When reporting, give measured figures — rows, command counts, timings, seek vs scan, percentiles —
not adjectives. "654 ms returning 75,369 rows, so the query was not the bottleneck" says something;
"optimised the query" does not. Name any limitation that remains.
