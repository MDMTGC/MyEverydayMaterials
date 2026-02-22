import re

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Update variables
new_vars = """
:root {
  /* Warm, tactile background */
  --bg-color: #faf9f5;
  --surface-color: #ffffff;
  --text-main: #18181b; 
  --text-muted: #52525b;
  --border-light: rgba(0, 0, 0, 0.06);
  --border-strong: rgba(0, 0, 0, 0.12);
  
  /* Vibrant Brand Accents */
  --accent-primary: #ef4444; /* Poppy red */
  --accent-brand: #6366f1; /* Indigo */
  --highlight: #fef08a;
  
  /* Soft Geometry */
  --radius-soft: 20px;
  --radius-pill: 100px;
  
  /* Hover physics */
  --shadow-float: 0 12px 32px rgba(0, 0, 0, 0.08);
  --shadow-card: 0 4px 16px rgba(0, 0, 0, 0.03);
  --spring: cubic-bezier(0.175, 0.885, 0.32, 1.15);

  --serif: 'Playfair Display', serif;
  --sans: 'Inter', sans-serif;

  /* Legacy statuses for Homepage grid */
  --green-50: #f0fdf4;
  --green-600: #16a34a;
  --green-700: #15803d;
  --amber-50: #fffbeb;
  --amber-600: #d97706;
  --amber-700: #b45309;
  --red-50: #fef2f2;
  --red-600: #dc2626;
  --red-700: #b91c1c;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-900: #111827;
}
"""
css = re.sub(r':root\s*\{.*?(?=\nbody\s*\{)', new_vars, css, flags=re.DOTALL)

# 2. Update Body
css = css.replace("background-color: var(--bg);", "background-color: var(--bg-color);\n  color: var(--text-main);")

# 3. Update Hero background
hero_regex = r'\.hero\s*\{.*?(?=\n\.hero|\n/\*)'
new_hero = """.hero {
  text-align: center;
  padding: 4.5rem 1.5rem 4rem;
  margin: -2rem -1.25rem 2.5rem;
  background-color: var(--text-main);
  border-radius: 0 0 var(--radius-soft) var(--radius-soft);
}"""
css = re.sub(hero_regex, new_hero, css, flags=re.DOTALL)

# 4. Remove heavy images completely from mobile hero
css = re.sub(r'background-image:[^;]+;', '', css)

# 5. Inject new UI Components
new_ui_components = """

/* ========================================================================= */
/* DYNAMIC MINIMALISM: "Authoritative + Human" Article Components            */
/* ========================================================================= */

.dek {
    font-size: 1.25rem;
    color: var(--text-muted);
    font-weight: 400;
    line-height: 1.5;
    margin-bottom: 2.5rem;
}

/* Dynamic, Rounded Verdict Card */
.verdict-card {
    background: linear-gradient(145deg, #fffafa 0%, #fff0f0 100%);
    border: 2px solid #fecaca;
    border-radius: var(--radius-soft);
    padding: 2rem;
    margin-bottom: 3rem;
    position: relative;
    box-shadow: 0 12px 24px rgba(239, 68, 68, 0.08); /* Glowing shadow */
}

.verdict-header {
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
}

.verdict-bubble {
    background: var(--accent-primary);
    color: white;
    font-family: var(--sans);
    font-weight: 800;
    font-size: 0.6875rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 0.375rem 0.875rem;
    border-radius: var(--radius-pill);
    margin-right: 0.75rem;
    display: inline-block;
}

.verdict-title {
    font-family: var(--serif);
    font-size: 1.5rem;
    font-weight: 700;
    color: #991b1b;
}

.verdict-text {
    font-size: 1rem;
    color: #7f1d1d;
    font-weight: 500;
    margin: 0;
    line-height: 1.6;
}

/* Rounded Floating Fact Cards */
.fact-card {
    background: var(--surface-color);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-soft);
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow-card);
    transition: transform 0.3s var(--spring), box-shadow 0.3s ease;
}

.fact-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-float);
    border-color: var(--border-strong);
}

.fact-icon {
    font-size: 1.5rem;
    margin-bottom: 0.75rem;
}

.fact-label {
    font-family: var(--serif);
    display: block;
    font-weight: 700;
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
    color: var(--text-main);
}
.fact-desc {
    font-family: var(--sans);
    font-size: 1rem;
    color: var(--text-muted);
    margin: 0;
}


/* Friendly Interactive Alternatives */
.alt-card {
    background-color: var(--surface-color);
    border: 2px solid var(--border-light);
    border-radius: var(--radius-soft);
    padding: 1.75rem;
    margin-bottom: 1.25rem;
    transition: all 0.2s ease;
}

.alt-card:hover {
    border-color: var(--accent-brand);
    box-shadow: 0 12px 32px rgba(99, 102, 241, 0.12);
}

.alt-type {
    font-family: var(--sans);
    font-size: 0.6875rem;
    font-weight: 700;
    color: var(--accent-brand);
    text-transform: uppercase;
    letter-spacing: 1px;
    background: #e0e7ff; /* Soft blue */
    padding: 0.375rem 0.75rem;
    border-radius: var(--radius-pill);
    display: inline-block;
    margin-bottom: 1rem;
}

.alt-name {
    font-family: var(--serif);
    font-size: 1.375rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    line-height: 1.2;
}

.alt-desc {
    font-size: 0.9375rem;
    margin-bottom: 1rem;
    color: var(--text-muted);
}

.alt-pros-cons {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    background: var(--bg-color);
    padding: 1rem 1.25rem;
    border-radius: 1rem;
}

.alt-pro, .alt-con {
    font-size: 0.875rem;
    font-weight: 600;
    display: flex;
    align-items: flex-start;
    gap: 0.625rem;
}

.alt-pro::before { content: '✓'; color: #16a34a; font-weight: 800; font-size: 1rem;}
.alt-con::before { content: '✕'; color: #ef4444; font-weight: 800; font-size: 1rem;}

/* Bouncy Magnetic Button */
.btn {
    display: inline-block;
    width: 100%;
    background-color: var(--text-main);
    color: white !important;
    text-align: center;
    padding: 1rem;
    border-radius: var(--radius-pill);
    font-family: var(--sans);
    font-size: 0.9375rem;
    font-weight: 700;
    text-decoration: none;
    border: none;
    cursor: pointer;
    transition: all 0.2s var(--spring);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.btn:hover, .btn:active {
    transform: scale(0.98);
    background-color: var(--accent-brand);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* ========================================= */
/* EXPLORE HUB - Semantic Cross-Linking      */
/* ========================================= */
.connection-hub {
    margin-top: 4rem;
    background: #f4f4f5; /* Soft modern grey */
    padding: 3rem 2rem;
    border-radius: var(--radius-soft);
    border: 1px solid var(--border-light);
    text-align: center;
}

.connection-hub h3 {
    font-family: var(--serif);
    font-size: 1.75rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    color: var(--text-main);
}

.connection-hub p {
    font-size: 1rem;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
    max-width: 480px;
    margin-inline: auto;
}

.connection-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
    text-align: left;
}

@media(min-width: 500px) {
    .connection-grid {
        grid-template-columns: 1fr 1fr;
    }
}

.connect-link {
    display: flex;
    flex-direction: column;
    text-decoration: none;
    background: var(--surface-color);
    padding: 1.5rem;
    border-radius: 1rem;
    border: 2px solid var(--border-light);
    transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(0,0,0,0.02);
}

.connect-link:hover {
    border-color: var(--accent-brand);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.08); /* Indigo glow */
}

.connect-type {
    font-family: var(--sans);
    font-size: 0.6875rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--accent-brand);
    margin-bottom: 0.5rem;
}

.connect-title {
    font-family: var(--serif);
    font-size: 1.125rem;
    font-weight: 700;
    color: var(--text-main);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.connect-link:hover .connect-title {
    color: var(--accent-brand);
}

"""

css += new_ui_components

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Processed style.css successfully.")
