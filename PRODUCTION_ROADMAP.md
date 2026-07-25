# InkSmith AI — Production Roadmap

A step-by-step plan to take InkSmith AI from working prototype to production-grade application.
Each phase builds on the previous one. Complete them in order.

---

## Phase 1: Fix Remaining Bugs (Do First)

These are bugs in the current code that will cause issues in production.



### 1.2 No-image fallback writes to wrong directory
- **File:** `backend/app/agent/reducer_subraph/generate_place_images.py` lines 20-22
- **Problem:** When `image_specs` is empty, `Path(fileName).write_text(...)` writes to the current working directory instead of `settings.OUTPUT_DIR`. The file also doesn't get `mdFilePath` or `fileName` returned.
- **Fix:** Use the same `folder = Path(settings.OUTPUT_DIR)` logic for the no-image path. Return `fileName` and `mdFilePath` in both branches.

### 1.3 `reducer.py` is dead code but still uses hardcoded path
- **File:** `backend/app/agent/nodes/reducer.py`
- **Problem:** This file still has `Path("output")` hardcoded. Also, it's no longer used in the graph (the reducer subgraph replaced it), but it's still in the codebase.
- **Fix:** Delete this file if it's not used, or update it to use `settings.OUTPUT_DIR`.

### 1.4 `from datetime import datetime` inside function body
- **File:** `backend/app/agent/reducer_subraph/generate_place_images.py` line 59
- **Problem:** Import inside the function body. Move to top of file.

### 1.5 `assert` used for runtime validation
- **Files:** `generate_place_images.py` line 10, `decide_images.py` line 14
- **Problem:** `assert plan is not None` gets stripped with `python -O`. Not safe for production.
- **Fix:** Replace with `if plan is None: raise ValueError("Plan is required")`.

### 1.6 Unused imports in `state.py`
- **File:** `backend/app/agent/state.py` line 1
- **Problem:** `Optional` is imported but never used. `EvidencePack` model (line 13) is defined but never used.
- **Fix:** Remove both.

### 1.7 `/query` endpoint returns non-serializable state
- **File:** `backend/app/main.py` line 59
- **Problem:** `result = app.state.rag_agent.invoke(...)` returns the full LangGraph state which includes Pydantic models (`Plan`, `EvidenceItem`). FastAPI may fail to serialize these or leak internal data.
- **Fix:** Return only the fields the frontend needs: `final`, `fileName`, `md_url`, `pdf_url`.

---

## Phase 2: Backend Error Handling & Resilience

### 2.1 Add try/except to all LLM calls
- **Files:** `router.py`, `orchestrator.py`, `worker.py`, `decide_images.py`
- **Problem:** Any LLM call can fail (rate limit, timeout, invalid response). Currently, a single failure crashes the entire graph with an unhandled exception.
- **How to do it:**
  ```python
  # Option A: LangChain's built-in retry
  llm_with_retry = llm.with_retry(stop_after_attempt=3, wait_exponential_multiplier=1)

  # Option B: Manual try/except with logging
  try:
      result = llm.invoke(...)
  except Exception as e:
      logger.error(f"LLM call failed: {e}")
      raise
  ```

### 2.2 Add structured logging
- **What:** Replace all `print()` statements with Python's `logging` module.
- **How to do it:**
  1. Create `backend/app/logger.py`:
     ```python
     import logging
     logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
     def get_logger(name: str):
         return logging.getLogger(name)
     ```
  2. In each node file: `from app.logger import get_logger` then `logger = get_logger(__name__)`
  3. Log node entry/exit, LLM token usage, image generation status, file writes.

### 2.3 Add request timeout for `/query`
- **Problem:** Blog generation can take 2-5+ minutes. HTTP clients (browsers, proxies) may timeout.
- **Options:**
  - **Option A (simple):** Increase timeout on the frontend `fetch()` call.
  - **Option B (better):** Make `/query` async — return a `job_id` immediately, then poll `GET /jobs/{job_id}` for status. This is covered in Phase 5.

### 2.4 Add input validation
- **File:** `backend/app/main.py`
- **How to do it:**
  ```python
  class QueryRequest(BaseModel):
      title: str = Field(..., min_length=3, max_length=200)
      thread_id: Optional[str] = Field(default="default", max_length=100)
  ```
- This prevents empty strings, extremely long inputs, or injection-style prompts from reaching the LLM.

---

## Phase 3: Backend Architecture Cleanup

### 3.1 Rename `reducer_subraph` → `reducer_subgraph`
- **What:** Fix the typo in the folder name.
- **How to do it:**
  1. Rename `backend/app/agent/reducer_subraph/` to `backend/app/agent/reducer_subgraph/`
  2. Update all imports across the codebase (grep for `reducer_subraph`).

### 3.2 Extract file-writing into a utility
- **Problem:** File-writing logic (sanitization, timestamp dedup, directory creation) is duplicated.
- **How to do it:**
  1. Create `backend/app/services/file_writer.py`:
     ```python
     from pathlib import Path
     from datetime import datetime
     import re

     def write_output_file(content: str, title: str, output_dir: str, extension: str = ".md") -> Path:
         safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
         file_name = safe_title.lower().replace(" ", "_") + extension
         folder = Path(output_dir)
         folder.mkdir(exist_ok=True)
         output_path = folder / file_name
         if output_path.exists():
             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
             output_path = output_path.with_name(f"{output_path.stem}_{timestamp}{output_path.suffix}")
         output_path.write_text(content, encoding="utf-8")
         return output_path
     ```
  2. Use this in `generate_place_images.py` instead of inline logic.

### 3.3 Use consistent naming convention
- **Problem:** Mix of `camelCase` (`fileName`, `mdFilePath`) and `snake_case` (`image_specs`, `merged_md`) in state keys.
- **Fix:** Pick one (Python standard = `snake_case`) and rename all state keys. Update `State` TypedDict, all nodes, and the frontend API types.

### 3.4 Separate Pydantic response models
- **How to do it:** Create a response model so you control exactly what the API returns:
  ```python
  class BlogResponse(BaseModel):
      final: str
      file_name: str
      md_url: str | None
      pdf_url: str | None
  ```
  Then in the endpoint: `return BlogResponse(...)`.

---

## Phase 4: Frontend Improvements

### 4.1 Add a loading progress indicator
- **Problem:** Blog generation takes minutes. The user sees a spinner with no progress.
- **How to do it:**
  - Show a step-by-step progress indicator: "Routing → Researching → Planning → Writing → Generating Images → Creating PDF"
  - This requires streaming from the backend (see Phase 5).
  - For now, show an animated multi-step fake progress bar that estimates time.

### 4.2 Add a blog history page
- **What:** Show previously generated blogs.
- **How to do it:**
  1. Add a `GET /blogs` endpoint that lists files in `output/`.
  2. Create a `BlogHistory.tsx` component.
  3. Each entry links to the markdown preview and PDF download.

### 4.3 Error display improvements
- **What:** Show user-friendly error messages instead of raw server errors.
- **How to do it:** Map known error types (rate limit, timeout, validation) to friendly messages in the frontend.

### 4.4 Mobile responsive design
- **What:** Test and fix the layout on mobile screens.
- The current TailwindCSS layout should mostly work, but test the form and result views on small screens.

---

## Phase 5: Async Job System (Important for Production)

### 5.1 Why this matters
The `/query` endpoint currently blocks for the entire blog generation (2-5+ minutes). This causes:
- Browser timeouts
- Server thread starvation (can only handle a few concurrent requests)
- No progress feedback

### 5.2 How to implement it
1. **Add a job queue:**
   - Use `BackgroundTasks` (simple) or `celery`/`arq` (scalable).
   - `POST /query` returns a `job_id` immediately.
   - Background worker runs the graph.

2. **Add status endpoint:**
   ```python
   @app.get("/jobs/{job_id}")
   def get_job_status(job_id: str):
       # Return: pending, running, completed, failed
       # If completed, include md_url and pdf_url
   ```

3. **Frontend polling:**
   - After submitting, poll `GET /jobs/{job_id}` every 3 seconds.
   - Show progress based on which node is currently running.

4. **Bonus — Server-Sent Events (SSE):**
   - Use `StreamingResponse` to push node completion events.
   - Frontend uses `EventSource` to receive real-time updates.
   - More responsive than polling.

---

## Phase 6: Persistent Storage & Database

### 6.1 Switch from MemorySaver to persistent checkpointer
- **Problem:** `MemorySaver` loses all state on server restart.
- **How to do it:**
  ```bash
  pip install langgraph-checkpoint-sqlite
  ```
  ```python
  from langgraph.checkpoint.sqlite import SqliteSaver
  checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
  ```
  For multi-server: use `PostgresSaver` instead.

### 6.2 Add a database for blog metadata
- **What:** Store blog title, creation time, file paths, status in a database.
- **How to do it:**
  1. Install SQLModel: `pip install sqlmodel`
  2. Create a `Blog` model with fields: `id`, `title`, `status`, `md_path`, `pdf_path`, `created_at`
  3. Create CRUD functions in `backend/app/services/db.py`
  4. Update endpoints to read/write from DB.

### 6.3 Move files to cloud storage (optional)
- **What:** Instead of local `output/` and `images/` folders, upload to S3/R2/MinIO.
- **When:** Only needed if deploying to multiple servers or if local disk fills up.

---

## Phase 7: Security & Deployment

### 7.1 Add CORS middleware
- **File:** `backend/app/main.py`
- **How to do it:**
  ```python
  from fastapi.middleware.cors import CORSMiddleware
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:5173"],  # Frontend URL
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```
  In production, set `allow_origins` to your actual domain.

### 7.2 Add rate limiting
- **What:** Prevent abuse — each IP can only generate N blogs per hour.
- **How to do it:** Use `slowapi` library:
  ```bash
  pip install slowapi
  ```

### 7.3 Add API key authentication (optional)
- **What:** Require an API key to use the `/query` endpoint.
- **How to do it:** Use FastAPI's `Depends()` with a header-based API key check.

### 7.4 Dockerize the application
- **How to do it:**
  1. Create `backend/Dockerfile`
  2. Create `frontend/Dockerfile`
  3. Create `docker-compose.yml` at root
  4. This makes deployment to any cloud provider trivial.

### 7.5 Add health check endpoint
- **How to do it:**
  ```python
  @app.get("/health")
  def health():
      return {"status": "ok", "graph_loaded": hasattr(app.state, "rag_agent")}
  ```

---

## Phase 8: Testing

### 8.1 Unit tests for utility functions
- Test `file_writer.py`, `pdf_converter.py`, filename sanitization.
- Use `pytest`.

### 8.2 Integration tests for individual nodes
- Mock the LLM calls and test each node in isolation.
- Verify state transformations are correct.

### 8.3 End-to-end test
- Mock all external APIs (LLM, Tavily, HF).
- Run the full graph and verify the output markdown and PDF.

### 8.4 Frontend tests
- Use Vitest for component tests.
- Test form submission, error display, result rendering.

---

## Priority Order Summary

| Priority | Phase | Effort | Impact |
|----------|-------|--------|--------|
| 🔴 Do now | Phase 1: Fix bugs | 1-2 hours | Prevents crashes |
| 🔴 Do now | Phase 2: Error handling | 2-3 hours | Prevents data loss |
| 🟡 Next | Phase 3: Architecture cleanup | 2-3 hours | Maintainability |
| 🟡 Next | Phase 4: Frontend improvements | 3-4 hours | User experience |
| 🟠 Important | Phase 5: Async jobs | 4-6 hours | Scalability |
| 🟠 Important | Phase 6: Database | 3-4 hours | Persistence |
| 🔵 Before deploy | Phase 7: Security & deploy | 3-4 hours | Production safety |
| 🔵 Before deploy | Phase 8: Testing | 4-6 hours | Reliability |
