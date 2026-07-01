/**
 * AI Space Weekly Intelligence — 9-page slide deck
 * Usage: node slide_builder.js <report.json> <output.pptx>
 *
 * Pages:
 *  1  Title
 *  2  Executive Summary
 *  3  Top Videos
 *  4  Top Channels
 *  5  Engagement
 *  6  Trending Topics
 *  7  Posting Patterns
 *  8  Recommendations
 *  9  Closing / Thank You
 */

const PptxGenJS = require("pptxgenjs");
const fs = require("fs");

const PRIMARY   = "1B3A6B";
const ACCENT    = "4A9EDB";
const WHITE     = "FFFFFF";
const LIGHT     = "E8F4FD";
const DARK_BG   = "0F2347";
const CARD_BG   = "162D55";
const DEEP_CARD = "0A1E3D";
const GRAY      = "8B9BB4";

const reportPath = process.argv[2];
const outputPath = process.argv[3];
if (!reportPath || !outputPath) {
  console.error("Usage: node slide_builder.js <report.json> <output.pptx>");
  process.exit(1);
}

const report = JSON.parse(fs.readFileSync(reportPath, "utf8"));
const pptx = new PptxGenJS();
pptx.layout  = "LAYOUT_WIDE";
pptx.title   = `AI Space Weekly Report — ${report.week_label}`;
pptx.subject = "AI & Automation YouTube Intelligence";
pptx.author  = "Eitan Adar — @eitanadar.ai";

function slide() {
  const s = pptx.addSlide();
  s.background = { color: DARK_BG };
  return s;
}

// Branded header bar + accent underline
function header(s, title, sub) {
  s.addShape(pptx.ShapeType.rect, { x:0, y:0, w:"100%", h:0.85, fill:{ color: PRIMARY } });
  s.addShape(pptx.ShapeType.rect, { x:0, y:0.83, w:"100%", h:0.05, fill:{ color: ACCENT } });
  s.addText(title, { x:0.4, y:0.07, w:"88%", h:0.56, fontSize:21, bold:true, color:WHITE, fontFace:"Arial" });
  if (sub) s.addText(sub, { x:0.4, y:0.63, w:"88%", h:0.22, fontSize:9, color:ACCENT, fontFace:"Arial" });
}

function chartOrFallback(s, chartKey, fallbackFn) {
  const p = report.charts && report.charts[chartKey];
  if (p && fs.existsSync(p)) {
    s.addImage({ path: p, x:0.3, y:1.0, w:9.1, h:4.1 });
  } else {
    fallbackFn(s);
  }
}

function fmt(n) {
  if (n >= 1e6) return (n/1e6).toFixed(1)+"M";
  if (n >= 1e3) return (n/1e3).toFixed(0)+"K";
  return String(n);
}

// ── PAGE 1: Title ────────────────────────────────────────────────────────────
{
  const s = slide();
  // Full-bleed primary background
  s.addShape(pptx.ShapeType.rect, { x:0, y:0, w:"100%", h:"100%", fill:{ color: PRIMARY } });
  // Accent bar
  s.addShape(pptx.ShapeType.rect, { x:0, y:3.6, w:"100%", h:0.07, fill:{ color: ACCENT } });
  // Brand mark — left vertical bar
  s.addShape(pptx.ShapeType.rect, { x:0.5, y:0.7, w:0.08, h:2.55, fill:{ color: ACCENT } });
  // Headline
  s.addText("AI SPACE", {
    x:0.75, y:0.65, w:8.5, h:1.15,
    fontSize:58, bold:true, color:WHITE, fontFace:"Arial",
  });
  s.addText("Weekly Intelligence Report", {
    x:0.75, y:1.75, w:8.5, h:0.72,
    fontSize:26, color:ACCENT, fontFace:"Arial",
  });
  s.addText(`Week of ${report.week_label}`, {
    x:0.75, y:2.55, w:8.5, h:0.42,
    fontSize:15, color:LIGHT, fontFace:"Arial", italic:true,
  });
  // Footer
  s.addText(`Generated ${report.generated_at}  ·  @eitanadar.ai  ·  AI & Automation Intelligence`, {
    x:0.5, y:4.82, w:9.0, h:0.3,
    fontSize:9, color:GRAY, fontFace:"Arial",
  });
}

// ── PAGE 2: Executive Summary ────────────────────────────────────────────────
{
  const s = slide();
  header(s, "Executive Summary", `Top insights from the AI & automation space — week of ${report.week_label}`);
  const items = (report.key_takeaways || []).slice(0, 5);
  items.forEach((item, i) => {
    const y = 1.05 + i * 0.76;
    // Numbered pill
    s.addShape(pptx.ShapeType.rect, { x:0.35, y, w:0.38, h:0.52, fill:{ color: ACCENT } });
    s.addText(String(i + 1), {
      x:0.35, y:y+0.02, w:0.38, h:0.48,
      fontSize:17, bold:true, color:WHITE, align:"center", fontFace:"Arial",
    });
    // Item text
    s.addText(item, {
      x:0.88, y:y+0.05, w:8.65, h:0.48,
      fontSize:12, color:WHITE, fontFace:"Arial",
    });
  });
}

// ── PAGE 3: Top Videos ───────────────────────────────────────────────────────
{
  const s = slide();
  header(s, "Top 10 Videos This Week", "Ranked by view count — past 7 days");
  chartOrFallback(s, "top_videos", (s) => {
    (report.top_videos || []).slice(0, 8).forEach((v, i) => {
      s.addText(`${i+1}.  ${v.title}  —  ${v.channel}  (${fmt(v.views)} views)`, {
        x:0.4, y:1.05 + i*0.5, w:9.1, h:0.42,
        fontSize:11, color:WHITE, fontFace:"Arial",
      });
    });
  });
}

// ── PAGE 4: Top Channels ─────────────────────────────────────────────────────
{
  const s = slide();
  header(s, "Top Channels in the AI Space", "Ranked by subscriber count");
  chartOrFallback(s, "channels", (s) => {
    (report.top_channels || []).slice(0, 5).forEach((ch, i) => {
      s.addText(`${i+1}.  ${ch.name}  —  ${fmt(ch.subscribers)} subscribers`, {
        x:0.4, y:1.1 + i*0.7, w:9.1, h:0.55,
        fontSize:12, color:WHITE, fontFace:"Arial",
      });
    });
  });
}

// ── PAGE 5: Engagement ───────────────────────────────────────────────────────
{
  const s = slide();
  header(s, "Engagement Analysis", "Views vs. like rate — bubble size = comment volume");
  chartOrFallback(s, "engagement", (s) => {
    s.addText("Engagement chart unavailable — no data returned.", {
      x:0.4, y:2.5, w:9.1, h:0.5,
      fontSize:12, color:GRAY, fontFace:"Arial", italic:true, align:"center",
    });
  });
  // Footer note
  s.addText("High-right = high views + high engagement. Ideal quadrant for content inspiration.", {
    x:0.4, y:4.85, w:9.1, h:0.25,
    fontSize:8, color:GRAY, fontFace:"Arial", italic:true,
  });
}

// ── PAGE 6: Trending Topics ──────────────────────────────────────────────────
{
  const s = slide();
  header(s, "Trending Topics", "Trend score = video count × avg views (thousands)");
  chartOrFallback(s, "trending_topics", (s) => {
    (report.themes || []).slice(0, 7).forEach((t, i) => {
      s.addText(`${i+1}. ${t.name}`, {
        x:0.4, y:1.1 + i*0.55, w:9.1, h:0.45,
        fontSize:12, color:WHITE, fontFace:"Arial",
      });
    });
  });
}

// ── PAGE 7: Posting Patterns ─────────────────────────────────────────────────
{
  const s = slide();
  header(s, "Posting Patterns", "Title hooks and content formats driving clicks this week");
  const hooks = (report.hooks || []).slice(0, 5);
  hooks.forEach((hook, i) => {
    const y = 1.05 + i * 0.74;
    s.addShape(pptx.ShapeType.rect, { x:0.35, y, w:9.25, h:0.62, fill:{ color: CARD_BG }, line:{ color: ACCENT, width:0.6 } });
    // Hook icon marker
    s.addShape(pptx.ShapeType.rect, { x:0.35, y, w:0.07, h:0.62, fill:{ color: ACCENT } });
    s.addText(hook, {
      x:0.58, y:y+0.1, w:8.9, h:0.44,
      fontSize:12, color:WHITE, fontFace:"Arial",
    });
  });
  // Emerging signals as a small addendum if space allows
  const signals = (report.emerging_signals || []).slice(0, 2);
  if (signals.length && hooks.length < 4) {
    s.addText("Emerging signals to watch:", {
      x:0.35, y:1.05 + hooks.length * 0.74 + 0.1, w:9.25, h:0.3,
      fontSize:10, color:ACCENT, bold:true, fontFace:"Arial",
    });
    signals.forEach((sig, i) => {
      s.addText(`• ${sig}`, {
        x:0.5, y:1.05 + hooks.length * 0.74 + 0.45 + i * 0.38, w:9.0, h:0.32,
        fontSize:11, color:LIGHT, fontFace:"Arial",
      });
    });
  }
}

// ── PAGE 8: Recommendations ──────────────────────────────────────────────────
{
  const s = slide();
  header(s, "Content Recommendations", "For @eitanadar.ai — based on gaps and trending themes this week");
  (report.recommendations || []).slice(0, 4).forEach((rec, i) => {
    const y = 1.05 + i * 0.9;
    s.addShape(pptx.ShapeType.rect, { x:0.35, y, w:9.25, h:0.76, fill:{ color: DEEP_CARD }, line:{ color: ACCENT, width:0.8 } });
    // Arrow marker
    s.addText("→", {
      x:0.42, y:y+0.12, w:0.35, h:0.52,
      fontSize:18, bold:true, color:ACCENT, fontFace:"Arial", align:"center",
    });
    s.addText(rec, {
      x:0.85, y:y+0.1, w:8.6, h:0.58,
      fontSize:12, color:WHITE, fontFace:"Arial",
    });
  });
}

// ── PAGE 9: Closing / Thank You ───────────────────────────────────────────────
{
  const s = slide();
  // Full-bleed primary — mirror the cover
  s.addShape(pptx.ShapeType.rect, { x:0, y:0, w:"100%", h:"100%", fill:{ color: PRIMARY } });
  s.addShape(pptx.ShapeType.rect, { x:0, y:3.5, w:"100%", h:0.07, fill:{ color: ACCENT } });
  s.addShape(pptx.ShapeType.rect, { x:0.5, y:0.75, w:0.08, h:2.4, fill:{ color: ACCENT } });

  s.addText("Thank You", {
    x:0.75, y:0.7, w:8.5, h:1.0,
    fontSize:52, bold:true, color:WHITE, fontFace:"Arial",
  });
  s.addText("Stay curious. Stay ahead.", {
    x:0.75, y:1.65, w:8.5, h:0.55,
    fontSize:22, color:ACCENT, fontFace:"Arial", italic:true,
  });

  // Summary stats line
  const videoCount = (report.top_videos || []).length;
  const themeCount = (report.themes || []).length;
  const chanCount  = (report.top_channels || []).length;
  s.addText(`This report analysed ${videoCount} videos  ·  ${themeCount} themes identified  ·  ${chanCount} channels tracked`, {
    x:0.75, y:2.3, w:8.5, h:0.38,
    fontSize:12, color:LIGHT, fontFace:"Arial",
  });

  // Next run note
  const nextItems = (report.next_week_watch || []).slice(0, 3);
  if (nextItems.length) {
    s.addText("Watch next week:", {
      x:0.75, y:2.82, w:8.5, h:0.3,
      fontSize:11, color:ACCENT, bold:true, fontFace:"Arial",
    });
    s.addText(nextItems.join("  ·  "), {
      x:0.75, y:3.12, w:8.5, h:0.3,
      fontSize:11, color:LIGHT, fontFace:"Arial", italic:true,
    });
  }

  s.addText(`Generated ${report.generated_at}  ·  @eitanadar.ai  ·  Adar Realty Studio AI Intelligence`, {
    x:0.5, y:4.82, w:9.0, h:0.28,
    fontSize:9, color:GRAY, fontFace:"Arial",
  });
}

pptx.writeFile({ fileName: outputPath })
  .then(() => { console.log(`Deck saved: ${outputPath}`); process.exit(0); })
  .catch((err) => { console.error("PPTX write error:", err); process.exit(1); });
