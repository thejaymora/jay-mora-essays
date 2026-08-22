# essay-inputs/template.py
# Copy this file to week05.py (or weekNN.py) and fill in all fields.
# Run: python generate_essay.py essay-inputs/weekNN.py --version 1

essay = {

    # ── Identity ─────────────────────────────────────────────────────────────
    # edition:   sequential number (1, 2, 3, ...)
    # week_tag:  file naming prefix — use WEEK00, WEEK01, WEEK02, WEEK03, WEEK04...
    "edition":  5,
    "week_tag": "WEEK04",

    # ── SEO & Metadata ────────────────────────────────────────────────────────
    # ghl_title:           window/tab title and og:title (155 chars max, include | Jay Mora)
    # breadcrumb_title:    same as ghl_title but without " | Jay Mora"
    # slug:                URL path segment, no slashes (e.g. "my-essay-title")
    # pillar:              one of the four content pillars (see CLAUDE.md)
    # publish_date_display: human-readable, e.g. "May 7, 2026"
    # publish_date_iso:    ISO 8601, e.g. "2026-05-07"
    # meta_description:    155 chars max, no apostrophes, factual summary
    # ghl_meta_description: same as meta_description but confirmed no apostrophes
    #                       (omit this key to use meta_description as fallback)
    # og_image_url:        full CDN URL to the 1200x630 OG image for this essay
    # og_image_alt:        plain-text description of the OG image, no punctuation issues
    # article_tags:        list of 6-10 SEO keyword strings
    # read_time:           estimated read time, e.g. "11 min read"
    # word_count:          approximate word count as int
    "ghl_title":            "Essay Title Goes Here | Jay Mora",
    "breadcrumb_title":     "Essay Title Goes Here",
    "slug":                 "essay-url-slug-here",
    "pillar":               "Sales Conversation Psychology",
    "publish_date_display": "May 7, 2026",
    "publish_date_iso":     "2026-05-07",
    "meta_description":     "SEO meta description here. No apostrophes. 155 chars max.",
    # "ghl_meta_description": "Override only if meta_description has apostrophes.",
    "og_image_url":         "https://assets.cdn.filesafe.space/oYYHLxBrKKJKNNDegpIm/media/REPLACE_WITH_REAL_ID.png",
    "og_image_alt":         "Essay title plain text -- Jay Mora, High-Ticket Sales Psychologist for Coaches",
    "article_tags": [
        "keyword one",
        "keyword two",
        "keyword three",
        "keyword four",
        "keyword five",
        "keyword six",
    ],
    "read_time":  "11 min read",
    "word_count": 1900,

    # ── Hero ──────────────────────────────────────────────────────────────────
    # hero_h1:   display headline shown in the page hero. Raw HTML allowed.
    #            Use <span class="jmbp-gold">text</span> for gold highlights.
    #            Use <br> for line breaks. No em dashes.
    # hero_lede: one sentence that sets up the essay. Plain text (HTML entities OK).
    "hero_h1":   'Your Display <span class="jmbp-gold">Headline Here.</span><br>Second Line of the <span class="jmbp-gold">Headline.</span>',
    "hero_lede": "One sentence that sets up the essay and makes the reader want to keep going.",

    # ── Article Body ──────────────────────────────────────────────────────────
    # List of (type, content) tuples. Content is raw HTML -- use HTML entities:
    #   &ldquo; &rdquo;  for "curly quotes"
    #   &lsquo; &rsquo;  for 'single curly quotes'
    #   &hellip;         for ...
    #   &trade;          for (TM)
    #   &reg;            for (R)
    #   &ndash;          for - (en dash, ranges)
    #   &amp;            for &
    #   <strong>         for bold text
    #   <em>             for italic text
    #   <a href="...">   for links (style='color:#F5C842;text-decoration:none;' for inline gold links)
    #
    # Section types:
    #   "comment"    -> <!-- HTML comment, labels a section. Pass section title. -->
    #   "lede"       -> Large opening paragraph. Use for the very first sentence only.
    #   "p"          -> Standard body paragraph.
    #   "h2"         -> Section heading (creates a visual divider above it).
    #   "impact"     -> White emphasis sentence. Use for punchy one-liners.
    #   "beat"       -> Italic prose beat. Use for key dialogue/phrases.
    #   "pullquote"  -> Gold italic block quote. Use for the 1-2 most quotable lines.
    #   "reflection" -> Dialog box. Use for exact language the coach says on a call.
    #   "byline"     -> Author byline. Always the last item. Pass None as content.
    "body_sections": [
        ("comment", "SECTION 1: OPENING HOOK"),
        ("lede", "Opening sentence that hooks the reader immediately."),
        ("p", "First paragraph of the essay."),
        ("p", "Second paragraph."),
        ("impact", "A punchy one-liner impact statement."),

        ("comment", "SECTION 2: THE CORE PROBLEM"),
        ("h2", "Section Two Heading Here"),
        ("p", "Body paragraph."),
        ("pullquote", "&ldquo;A key quotable line from the essay.&rdquo;"),
        ("p", "Continuation paragraph."),

        ("comment", "SECTION 3: THE SYSTEM"),
        ("h2", "Section Three Heading"),
        ("p", "<strong>The prospect says:</strong>"),
        ("beat", "&ldquo;The exact thing the prospect says.&rdquo;"),
        ("p", "<strong>The coach responds</strong> with warmth:"),
        ("reflection", "&ldquo;The exact response the coach delivers. Precise language.&rdquo;"),
        ("p", "What happens next."),

        ("comment", "SECTION 4: THE CLOSE"),
        ("h2", "Final Section Heading"),
        ("p", "Closing paragraphs."),
        ("impact", "Final impact statement."),

        ("byline", None),
    ],

    # ── FAQ ───────────────────────────────────────────────────────────────────
    # 10-18 questions. Each answer 80-150 words. No apostrophes in answers.
    # Questions should be the exact search queries readers type into Google.
    # Answers must be complete and standalone (Google shows them in rich results).
    "faqs": [
        {
            "q": "Question one that a reader would Google?",
            "a": "Complete answer to question one. No apostrophes. Around 100 words. "
                 "Full and useful as a standalone answer.",
        },
        {
            "q": "Question two?",
            "a": "Complete answer to question two.",
        },
        # Add more...
    ],
}
