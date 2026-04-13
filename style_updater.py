import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace CSS variables
new_css_vars = """    /* ─── DESIGN TOKENS ─── */
    :root {
      --bg:        #f8f9fa;
      --surface:   #ffffff;
      --surface2:  #f1f3f5;
      --border:    #e9ecef;
      --accent:    #FF76A5;
      --accent2:   #4EA0E2;
      --accent3:   #FE6F17;
      --text:      #212529;
      --muted:     #868e96;
      --danger:    #fa5252;
      --success:   #40c057;
      --radius:    16px;
      --shadow:    0 8px 32px rgba(0,0,0,0.05);
    }"""
html = re.sub(r'/\* ─── DESIGN TOKENS ─── \*/.*?\}', new_css_vars, html, flags=re.DOTALL)

# Remove glowing dots
html = re.sub(r'/\* ─── BACKGROUND GLOW ─── \*/.*?/\* ─── LAYOUT ─── \*/', r'/* ─── LAYOUT ─── */', html, flags=re.DOTALL)

# Logo
new_logo = """    .logo {
      display: inline-flex;
      align-items: center;
      gap: 12px;
      color: #1a1a1a;
      font-size: 3.2rem;
      font-weight: 900;
      letter-spacing: -2px;
      line-height: 1;
    }
    .logo-icon {
      font-size: 2.8rem;
    }
    header p {
      color: var(--muted);
      margin-top: 15px;
      font-size: 1.1rem;
      font-weight: 500;
      letter-spacing: -0.3px;
    }"""
html = re.sub(r'\.logo \{.*?header p \{.*?\}', new_logo, html, flags=re.DOTALL)

# Badges and buttons
html = re.sub(r'background: linear-gradient\(135deg, var\(--accent\), var\(--accent2\)\);', r'background: var(--accent);', html)
html = re.sub(r'box-shadow: 0 4px 20px rgba\(124,92,252,0\.35\);', r'box-shadow: 0 4px 15px rgba(255,118,165,0.3);', html)

# Buzzer Grid
new_buzzer_css = """    /* ─── BUZZER GRID ─── */
    .buzzer-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
      gap: 50px 20px;
      justify-items: center;
      padding-top: 20px;
      margin-bottom: 50px;
    }

    /* ─── BUZZER CARD ─── */
    .buzzer-card {
      position: relative;
      width: 120px;
      height: 120px;
      border-radius: 50%;
      background: var(--card-color, #4EA0E2);
      border: 4px solid var(--surface);
      box-shadow: 
        0 14px 0 var(--card-shadow, rgba(0,0,0,0.15)), 
        0 20px 20px rgba(0,0,0,0.1),
        inset 0 -5px 15px rgba(0,0,0,0.1);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: transform 0.1s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.1s cubic-bezier(0.4, 0, 0.2, 1);
      overflow: visible;
      user-select: none;
      padding: 0;
    }
    
    .buzzer-card:hover { filter: brightness(1.05); }
    
    .buzzer-card:active, .buzzer-card.playing {
      transform: translateY(10px);
      box-shadow: 
        0 4px 0 var(--card-shadow, rgba(0,0,0,0.15)), 
        0 10px 15px rgba(0,0,0,0.05),
        inset 0 -2px 5px rgba(0,0,0,0.05);
    }

    .buzzer-card.playing { border-color: rgba(255,255,255,0.8); }

    .buzzer-emoji {
      font-size: 3rem;
      display: block;
      position: relative;
      z-index: 1;
      filter: drop-shadow(0 4px 6px rgba(0,0,0,0.15));
      transition: transform 0.2s;
      margin-top: -5px;
    }
    .buzzer-card:hover .buzzer-emoji { transform: scale(1.15) rotate(8deg); }

    .buzzer-name {
      font-size: 0.95rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: -0.5px;
      position: absolute; 
      bottom: -35px;
      left: 50%;
      transform: translateX(-50%);
      width: 150px;
      text-align: center;
      color: var(--text);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .wave-indicator {
      display: flex;
      align-items: flex-end;
      justify-content: center;
      gap: 5px;
      height: 30px;
      position: absolute;
      top: -45px;
      opacity: 0;
      transition: opacity 0.2s;
      z-index: 1;
    }
    .buzzer-card.playing .wave-indicator { opacity: 1; }
    .wave-bar {
      width: 6px;
      background: var(--card-color, #4EA0E2);
      border-radius: 4px;
      animation: wave-anim 0.6s ease-in-out infinite;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .wave-bar:nth-child(2) { animation-delay: 0.1s; background: var(--accent); }
    .wave-bar:nth-child(3) { animation-delay: 0.2s; }
    .wave-bar:nth-child(4) { animation-delay: 0.05s; background: var(--accent3); }
    @keyframes wave-anim { 0%, 100% { height: 8px; } 50% { height: 30px; } }

    /* ─── EDIT BUTTON ON CARD ─── */
    .card-edit {
      position: absolute;
      top: 0; right: -15px; left: auto;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 50%;
      width: 32px; height: 32px;
      display: flex; align-items: center; justify-content: center;
      font-size: 0.85rem;
      color: var(--text);
      cursor: pointer;
      opacity: 0;
      transition: opacity 0.2s, background 0.15s, transform 0.15s;
      z-index: 10;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .buzzer-card:hover .card-edit { opacity: 1; }
    .card-edit:hover { background: var(--surface2); transform: scale(1.1); }
"""
html = re.sub(r'/\* ─── BUZZER GRID ─── \*/.*?/\* ─── EMPTY STATE ─── \*/', new_buzzer_css + '\n    /* ─── EMPTY STATE ─── */', html, flags=re.DOTALL)

# Update COLORS inside JSX
new_colors = """    const COLORS = [
      { name: 'Rose',   val: '#FF76A5', shadow: '#D04073' },
      { name: 'Bleu',   val: '#4EA0E2', shadow: '#2778B6' },
      { name: 'Orange', val: '#FE6F17', shadow: '#C84F05' },
      { name: 'Noir',   val: '#212529', shadow: '#000000' },
      { name: 'Vert',   val: '#40c057', shadow: '#2b8a3e' },
      { name: 'Violet', val: '#7c5cfc', shadow: '#5635D0' },
    ];
    const COLOR_SWATCHES = COLORS.map(c => c.val);"""
html = re.sub(r'const COLORS = \[.*?\];\n    const COLOR_SWATCHES = \[.*?\];', new_colors, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
