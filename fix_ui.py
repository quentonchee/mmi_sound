import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# CSS Fixes
new_css = """
    /* ─── UPLOAD FULL COLLAPSE ─── */
    .upload-collapse {
      max-height: 0;
      overflow: hidden;
      opacity: 0;
      transition: max-height 0.4s cubic-bezier(0, 1, 0, 1), opacity 0.3s, margin 0.3s;
      margin-bottom: 0;
    }
    .upload-collapse.open {
      max-height: 800px;
      opacity: 1;
      margin-bottom: 40px;
      transition: max-height 0.6s ease-in-out, opacity 0.4s 0.1s, margin 0.4s;
    }
    
    /* ─── FAB ADD BUTTON ─── */
    .fab-add {
      position: fixed;
      bottom: 30px;
      right: 30px;
      width: 65px;
      height: 65px;
      border-radius: 50%;
      background: var(--accent);
      color: white;
      font-size: 2.5rem;
      border: none;
      box-shadow: 0 8px 25px rgba(255,118,165,0.4);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), background 0.3s;
      z-index: 100;
      line-height: 1;
    }
    .fab-add:hover {
      transform: scale(1.1);
      background: var(--accent3);
      box-shadow: 0 12px 30px rgba(254,111,23,0.4);
    }
    .fab-add.rotate {
      transform: rotate(135deg);
      background: var(--danger);
      box-shadow: 0 8px 25px rgba(250,82,82,0.4);
    }
    
    /* ─── MEDIA QUERY ADDITIONS ─── */
    @media (max-width: 600px) {
      .fab-add { bottom: 20px; right: 20px; width: 60px; height: 60px; font-size: 2rem; }
    }
"""

# Insert CSS before </style>
html = html.replace('</style>', new_css + '\n  </style>')

# Remove unnecessary header text
html = re.sub(r'<p>Développé avec React.*?<\/p>', '', html, flags=re.DOTALL)

# Clean up stats bar
old_stats = r'<div className="stat-chip">💾 Stockage.*?<\/div>.*?<div className="stat-chip">🕐 Son joué.*?<\/div>'
html = re.sub(old_stats, '', html, flags=re.DOTALL)

# Remove (React Cloud) from Logo
html = html.replace('MMI SoundBoard (React Cloud)', 'MMI SoundBoard')

# Add isUploadOpen state
html = re.sub(r'const \[searchFilter, setSearchFilter\] = useState\(\'\'\);', r'const [searchFilter, setSearchFilter] = useState(\'\');\n      const [isUploadOpen, setIsUploadOpen] = useState(false);', html)

# Wrap upload section
html = html.replace('<div \n            className="upload-section"', '<div className={`upload-collapse ${isUploadOpen ? \'open\' : \'\'}`}>\n          <div \n            className="upload-section"')
html = html.replace('</button>\n              </div>\n            </div>\n            <input type="file"', '</button>\n              </div>\n            </div>\n            <input type="file"')
# This above replace is incomplete to wrap the closing div, we need to find the exact end of .upload-section.
html = re.sub(r'(<input type="file" ref=\{fileInputRef\}.*?\/>\n          <\/div>)', r'\1\n          </div>', html, flags=re.DOTALL)

# Add FAB button just before <footer>
html = html.replace('<footer>', '<button className={`fab-add ${isUploadOpen ? \'rotate\' : \'\'}`} onClick={() => setIsUploadOpen(!isUploadOpen)}>➕</button>\n          <footer>')

# Fix search input overlapping padding
html = html.replace('className="input-field" \n                placeholder="Rechercher..."', 'id="searchInput"\n                className="input-field" \n                placeholder="Rechercher..."')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
