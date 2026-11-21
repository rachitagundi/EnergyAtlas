import { useEffect, useRef, useState } from "react";
import type { FormEvent } from "react";
import { ArrowDown, ArrowUpRight, Bookmark, BookOpen, Check, ChevronRight, Database, ExternalLink, Layers3, Leaf, Plus, Search, Sun, Wind, X, Zap } from "lucide-react";
import { createSource, loadLibrary, saveSource } from "./api";
import type { EnergySource, Kind, Overview, Topic } from "./api";

const topics = ["Electricity", "Renewables", "Energy system"] as const;
const kinds = ["Data portal", "Overview", "Statistics"] as const;
const topicIcons = { Electricity: Zap, Renewables: Sun, "Energy system": Wind };

function AddSource({ onClose, onAdded }: { onClose: () => void; onAdded: () => void }) {
  const dialog = useRef<HTMLDialogElement>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  useEffect(() => { dialog.current?.showModal(); }, []);
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    setBusy(true); setError("");
    try {
      await createSource({
        title: String(form.get("title")),
        publisher: String(form.get("publisher")),
        url: String(form.get("url")),
        description: String(form.get("description")),
        topic: String(form.get("topic")) as Topic,
        kind: String(form.get("kind")) as Kind,
      });
      onAdded();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not add source.");
    } finally { setBusy(false); }
  }
  return <dialog ref={dialog} onCancel={onClose} aria-labelledby="new-source-title">
    <div className="dialog-top"><span className="eyebrow">GROW YOUR LIBRARY</span><button type="button" className="icon-button" onClick={onClose} aria-label="Close add source"><X size={20} /></button></div>
    <h2 id="new-source-title">Add an energy source</h2>
    <p className="muted">Save a link and its details. The page content stays at the original publisher.</p>
    <form onSubmit={submit}>
      <label>Title<input name="title" required minLength={3} maxLength={200} placeholder="What is this source called?" /></label>
      <label>Publisher<input name="publisher" required minLength={2} maxLength={120} placeholder="Organisation or author" /></label>
      <label>Source URL<input name="url" type="url" required maxLength={2000} placeholder="https://" /></label>
      <div className="form-row">
        <label>Topic<select name="topic">{topics.map(t => <option key={t}>{t}</option>)}</select></label>
        <label>Type<select name="kind">{kinds.map(t => <option key={t}>{t}</option>)}</select></label>
      </div>
      <label>Short description<textarea name="description" required minLength={10} maxLength={1000} rows={3} placeholder="What can you find here?" /></label>
      {error && <p role="alert" className="error">{error}</p>}
      <button type="submit" disabled={busy} className="primary full">{busy ? "Adding source…" : "Add to library"}<Plus size={17} /></button>
    </form>
  </dialog>;
}

export default function App() {
  const [mode, setMode] = useState<"all" | "saved">("all");
  const [query, setQuery] = useState("");
  const [topic, setTopic] = useState("");
  const [sources, setSources] = useState<EnergySource[]>([]);
  const [overview, setOverview] = useState<Overview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [revision, setRevision] = useState(0);
  const [pending, setPending] = useState<number | null>(null);
  const [adding, setAdding] = useState(false);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true); setError("");
    const timer = setTimeout(() => {
      loadLibrary(query, topic, mode === "saved", controller.signal)
        .then(data => { setSources(data.sources); setOverview(data.overview); })
        .catch(err => {
          if (!controller.signal.aborted) setError(err instanceof TypeError ? "Cannot reach the API. Start the FastAPI server on port 8010, then retry." : err.message);
        })
        .finally(() => { if (!controller.signal.aborted) setLoading(false); });
    }, 180);
    return () => { clearTimeout(timer); controller.abort(); };
  }, [query, topic, mode, revision]);

  useEffect(() => {
    if (!notice) return;
    const timer = setTimeout(() => setNotice(""), 2800);
    return () => clearTimeout(timer);
  }, [notice]);

  async function bookmark(source: EnergySource) {
    setPending(source.id);
    try {
      await saveSource(source.id, !source.saved);
      setRevision(v => v + 1);
      setNotice(source.saved ? "Removed from saved sources" : "Source saved to your library");
    } catch (err) { setError(err instanceof Error ? err.message : "Could not save source."); }
    finally { setPending(null); }
  }
  function clearFilters() { setQuery(""); setTopic(""); }

  return <div className="app-shell">
    <aside className="sidebar">
      <a className="brand" href="/"><span className="brand-icon"><Layers3 size={23} /></span><span>EnergyAtlas<span className="brand-caption">YOUR ENERGY RESEARCH SPACE</span></span></a>
      <div className="workspace"><span className="workspace-avatar">RG</span><div>Personal workspace<small>Energy research workspace</small></div><ChevronRight size={15} /></div>
      <div className="nav-label">WORKSPACE</div>
      <nav aria-label="Workspace">
        <button className={mode === "all" ? "nav-button active" : "nav-button"} onClick={() => { setMode("all"); clearFilters(); }}><BookOpen size={18} />Source library<span>{overview?.sources ?? "—"}</span></button>
        <button className={mode === "saved" ? "nav-button active" : "nav-button"} onClick={() => { setMode("saved"); clearFilters(); }}><Bookmark size={18} />Saved sources<span>{overview?.saved ?? "—"}</span></button>
      </nav>
      <div className="nav-label topic-label">EXPLORE TOPICS</div>
      <nav aria-label="Topics">{topics.map(t => {
        const Icon = topicIcons[t];
        return <button key={t} className={topic === t ? "nav-button active" : "nav-button"} onClick={() => { setMode("all"); setTopic(t); setQuery(""); }}><Icon size={17} />{t}</button>;
      })}</nav>
      <div className="sidebar-bottom">
        <div className="learning-card"><span className="tiny-icon"><Leaf size={17} /></span><strong>Built to understand energy.</strong><p>One reliable source.<br />One useful question at a time.</p><span className="phase"><i />CHECKPOINT 0C</span></div>
        <div className="local-note"><span className="status-dot" />Local research workspace</div>
      </div>
    </aside>
    <main>
      <header className="topbar"><span>Workspace <ChevronRight size={13} /> <strong>{mode === "saved" ? "Saved sources" : "Source library"}</strong></span><span className="checkpoint"><span className="status-dot" />Source catalogue</span></header>
      <div className="main-content">
        <section className="page-heading">
          <div><span className="eyebrow">GERMANY'S ENERGY TRANSITION, EXPLORED</span><h1>{mode === "saved" ? "Your reading shortlist." : "Good research starts here."}</h1><p>{mode === "saved" ? "The sources you want to come back to, all in one place." : "Find, organise and revisit public energy sources. Build your own picture."}</p></div>
          <button className="primary" onClick={() => setAdding(true)}><Plus size={18} />Add source</button>
        </section>
        <section className="intro-banner">
          <div className="banner-text"><span className="banner-tag"><Leaf size={13} />A CLEARER VIEW OF ENERGY</span><h2>Follow the evidence.<br />Understand the transition.</h2><p>A growing library of public data portals, research<br className="desktop-break" /> and energy statistics from original publishers.</p><a href="#library">Explore the library<ArrowDown size={15} /></a></div>
          <div className="landscape" aria-hidden="true"><div className="sun" /><div className="hill hill-back" /><div className="hill hill-front" /><div className="turbine one"><i /><b /><b /><b /></div><div className="turbine two"><i /><b /><b /><b /></div><div className="landscape-label">OPEN SOURCES. BETTER QUESTIONS.</div></div>
        </section>
        <section className="stats" aria-label="Library overview">
          <div><span className="stat-icon"><BookOpen size={20} /></span><div><strong>{overview?.sources ?? "—"}</strong><span>Sources in your library</span></div></div>
          <div><span className="stat-icon"><Layers3 size={20} /></span><div><strong>{overview?.publishers ?? "—"}</strong><span>Original publishers</span></div></div>
          <div><span className="stat-icon"><Bookmark size={20} /></span><div><strong>{overview?.saved ?? "—"}</strong><span>Saved for later</span></div></div>
        </section>
        <section id="library" className="library">
          <div className="library-heading"><h2>{mode === "saved" ? "Saved sources" : "Source library"}<span>{loading ? "…" : sources.length}</span></h2><span className="small muted">Curated links · Original publishers</span></div>
          <div className="filters">
            <label className="search-box"><Search size={18} /><span className="sr-only">Search sources</span><input value={query} onChange={e => setQuery(e.target.value)} maxLength={100} placeholder="Search by title, publisher or keyword…" />{query && <button type="button" className="icon-button" aria-label="Clear search" onClick={() => setQuery("")}><X size={15} /></button>}</label>
            <label className="filter-select"><span className="sr-only">Filter by topic</span><select value={topic} onChange={e => setTopic(e.target.value)}><option value="">All topics</option>{topics.map(t => <option key={t}>{t}</option>)}</select></label>
          </div>
          {error && <div className="error-panel" role="alert"><strong>Something needs attention</strong><p>{error}</p><button className="secondary" onClick={() => setRevision(v => v + 1)}>Retry</button></div>}
          {loading ? <div className="loading-state" role="status">Loading your sources…</div> : !error && sources.length === 0 ? <div className="empty-state"><Search size={25} /><h3>{mode === "saved" ? "Nothing saved here yet." : "No matching sources."}</h3><p>{mode === "saved" ? "Use the bookmark button on any source to keep it here." : "Try another keyword or clear your topic filter."}</p><button className="secondary" onClick={() => { clearFilters(); if (mode === "saved") setMode("all"); }}>Explore all sources</button></div> : !error && <div className="source-grid">{sources.map(source => {
            const Icon = topicIcons[source.topic];
            return <article className="source-card" key={source.id}>
              <div className="card-top"><span className={"source-icon topic-" + source.topic.split(" ")[0].toLowerCase()}><Icon size={24} strokeWidth={1.7} /></span><button disabled={pending !== null} type="button" className={source.saved ? "bookmark saved" : "bookmark"} aria-label={(source.saved ? "Unsave " : "Save ") + source.title} aria-pressed={source.saved} onClick={() => bookmark(source)}><Bookmark size={19} fill={source.saved ? "currentColor" : "none"} /></button></div>
              <div className="source-publisher">{source.publisher}</div><h3>{source.title}</h3><p>{source.description}</p>
              <div className="card-tags"><span>{source.topic}</span><span>{source.kind}</span></div>
              <a className="source-link" href={source.url} target="_blank" rel="noopener noreferrer">Visit original source<ArrowUpRight size={17} /></a>
            </article>;
          })}</div>}
        </section>
        <footer><span><Database size={14} />Saved in {overview?.database === "postgresql" ? "PostgreSQL" : overview?.database === "sqlite" ? "SQLite" : "your database"}</span><p>Metadata search only. Full-text retrieval and AI answers are future checkpoints.</p><a href="/api/docs" target="_blank" rel="noopener noreferrer">API docs<ExternalLink size={13} /></a></footer>
      </div>
    </main>
    {notice && <div className="toast" role="status"><Check size={17} />{notice}</div>}
    {adding && <AddSource onClose={() => setAdding(false)} onAdded={() => { setAdding(false); clearFilters(); setMode("all"); setRevision(v => v + 1); setNotice("New source added to your library"); }} />}
  </div>;
}
