---
permalink: /arsiv/
---

# Çalakalem Arşivi

<p style="color: #555; font-size: 1.15rem; font-family: 'Georgia', serif; font-style: italic; margin-bottom: 3rem; line-height: 1.6;">
  Yazılmış tüm metinlerin zaman dilimlerine göre düzenlenmiş dizini.
</p>

<!-- Şık Navigasyon Butonu -->
<div style="margin-bottom: 4rem; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
  <a href="../yazilar/" style="display: inline-block; color: #111; border-bottom: 1px solid #111; padding-bottom: 4px; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; text-decoration: none; transition: opacity 0.2s ease;" onmouseover="this.style.opacity='0.6'" onmouseout="this.style.opacity='1'">
    ← Zaman Akışına Dön
  </a>
</div>

<div id="archive-app" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
  
  <div id="raw-data" style="display:none;">
    {% assign sorted_files = site.static_files | sort: 'path' | reverse %}
    {% for file in sorted_files %}
      {% if file.path contains "yazilar/" and file.extname == ".md" and file.name != "index.md" %}
        {% assign date_str = file.name | remove: ".md" %}
        {% assign parts = date_str | split: "-" %}
        <span data-url="{{ site.baseurl }}{{ file.path }}" data-date="{{ date_str }}" data-year="{{ parts[0] }}" data-month="{{ parts[1] }}"></span>
      {% endif %}
    {% endfor %}
  </div>

  <div style="display: flex; gap: 60px; align-items: flex-start; flex-wrap: wrap;">
    
    <!-- Açılır Kapanır Sol Menü -->
    <div style="flex: 1; min-width: 200px;">
      <h3 style="margin-top:0; font-size:0.85rem; text-transform: uppercase; letter-spacing: 2px; color: #888; border-bottom: 1px solid #eee; padding-bottom:12px; margin-bottom: 20px;">Dizin</h3>
      <ul style="list-style: none; padding: 0; margin: 0;">
        <li style="margin-bottom: 24px;">
          <button onclick="filterPosts('all', 'all')" style="background:none; border:none; color:#111; cursor:pointer; font-weight:700; font-size:1.1rem; padding:0; transition: opacity 0.2s;" onmouseover="this.style.opacity='0.6'" onmouseout="this.style.opacity='1'">
            Tüm Zamanlar <span style="color:#aaa; font-weight:400; font-size:0.9rem; margin-left: 4px;">(<span id="total-count">0</span>)</span>
          </button>
        </li>
      </ul>
      <div id="filter-tree"></div>
    </div>

    <!-- Zarif Liste Görünümü -->
    <div style="flex: 2; min-width: 300px;">
      <h3 id="current-filter-title" style="margin-top:0; font-size: 2rem; font-weight: 800; letter-spacing: -0.04em; color: #111; border-bottom: 1px solid #eee; padding-bottom: 16px; margin-bottom: 30px;">
        Tüm Yazılar
      </h3>
      <ul id="filtered-posts-list" style="list-style-type: none; padding-left: 0; margin: 0;">
        <!-- JS ile dolacak -->
      </ul>
    </div>

  </div>
</div>

<script>
document.addEventListener("DOMContentLoaded", function() {
  const favicon = document.createElement('link');
  favicon.rel = 'icon';
  favicon.href = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">💠</text></svg>';
  document.head.appendChild(favicon);

  const spans = document.querySelectorAll("#raw-data span");
  const posts = [];
  const tree = {};

  spans.forEach(span => {
    const year = span.getAttribute("data-year");
    const month = span.getAttribute("data-month");
    const date = span.getAttribute("data-date");
    const url = span.getAttribute("data-url");
    
    posts.push({ year, month, date, url });

    if (!tree[year]) tree[year] = { count: 0, months: {} };
    if (!tree[year].months[month]) tree[year].months[month] = 0;
    
    tree[year].count++;
    tree[year].months[month]++;
  });

  document.getElementById("total-count").innerText = posts.length;
  window.allPosts = posts;

  const monthNames = {
    "01": "Ocak", "02": "Şubat", "03": "Mart", "04": "Nisan", "05": "Mayıs", "06": "Haziran",
    "07": "Temmuz", "08": "Ağustos", "09": "Eylül", "10": "Ekim", "11": "Kasım", "12": "Aralık"
  };

  let treeHTML = "";
  const sortedYears = Object.keys(tree).sort().reverse();
  
  sortedYears.forEach((year, index) => {
    const isFirst = index === 0;
    const displayStyle = isFirst ? 'block' : 'none';
    const icon = isFirst ? '▾' : '▸';

    treeHTML += `<div style="margin-top: 20px;">`;
    treeHTML += `<button onclick="toggleYear('${year}')" style="background:none; border:none; color:#111; cursor:pointer; font-weight:700; font-size:1.1rem; padding:0; text-align:left; transition: opacity 0.2s;" onmouseover="this.style.opacity='0.6'" onmouseout="this.style.opacity='1'"><span id="icon-${year}" style="display:inline-block; width:18px; font-size:0.9em; color:#888;">${icon}</span>${year} <span style="color:#aaa; font-weight:400; font-size:0.9rem; margin-left: 4px;">(${tree[year].count})</span></button>`;
    treeHTML += `<ul id="months-${year}" style="list-style:none; padding-left:18px; border-left: 1px solid #eee; margin:12px 0 0 7px; display: ${displayStyle};">`;
    
    const sortedMonths = Object.keys(tree[year].months).sort().reverse();
    sortedMonths.forEach(month => {
      const name = monthNames[month] || month;
      treeHTML += `<li style="margin-bottom:10px;"><button onclick="filterPosts('${year}', '${month}')" style="background:none; border:none; color:#555; cursor:pointer; font-size:0.95rem; padding:0; transition: color 0.2s;" onmouseover="this.style.color='#111'" onmouseout="this.style.color='#555'">${name} <span style="color:#ccc; font-size:0.85rem; margin-left: 4px;">(${tree[year].months[month]})</span></button></li>`;
    });
    
    treeHTML += `</ul></div>`;
  });
  
  document.getElementById("filter-tree").innerHTML = treeHTML;
  filterPosts('all', 'all');
});

// Accordion (Açılır Kapanır) Fonksiyonu
window.toggleYear = function(year) {
  const ul = document.getElementById('months-' + year);
  const icon = document.getElementById('icon-' + year);
  if (ul.style.display === 'none') {
    ul.style.display = 'block';
    icon.innerText = '▾';
  } else {
    ul.style.display = 'none';
    icon.innerText = '▸';
  }
  filterPosts(year, 'all');
};

window.filterPosts = function(year, month) {
  const listContainer = document.getElementById("filtered-posts-list");
  const titleContainer = document.getElementById("current-filter-title");
  
  const monthNames = {
    "01": "Ocak", "02": "Şubat", "03": "Mart", "04": "Nisan", "05": "Mayıs", "06": "Haziran",
    "07": "Temmuz", "08": "Ağustos", "09": "Eylül", "10": "Ekim", "11": "Kasım", "12": "Aralık"
  };

  if (year === 'all') titleContainer.innerText = "Tüm Yazılar";
  else if (month === 'all') titleContainer.innerText = `${year}`;
  else titleContainer.innerText = `${monthNames[month]} ${year}`;

  const filtered = window.allPosts.filter(post => {
    const yearMatch = (year === 'all' || post.year === year);
    const monthMatch = (month === 'all' || post.month === month);
    return yearMatch && monthMatch;
  });

  if (filtered.length === 0) {
    listContainer.innerHTML = "<li style='color: #888; font-style: italic; padding: 20px 0;'>Bu dönemde yazılmış bir metin bulunmuyor.</li>";
    return;
  }

  listContainer.innerHTML = filtered.map(post => `
    <li style="margin-bottom: 20px; display: flex; align-items: baseline; gap: 20px;">
      <span style="color: #aaa; font-size: 0.85rem; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; width: 100px; flex-shrink: 0;">Ufuk Demir</span>
      <a href="${post.url}" style="text-decoration: none; color: #111; font-weight: 600; font-size: 1.15rem; transition: opacity 0.2s;" onmouseover="this.style.opacity='0.5'" onmouseout="this.style.opacity='1'">
        ${post.date}
      </a>
    </li>
  `).join("");
};
</script>
