---
permalink: /arsiv/
---

# 📚 Çalakalem Arşivi

<p style="color: #6e7781; font-size: 1.1em; margin-bottom: 2.5rem; line-height: 1.6;">
  Yazılmış tüm metinlerin zaman dilimlerine göre düzenlenmiş istatistiksel arşivi.
</p>

<div style="margin-bottom: 4rem;">
  <a href="../yazilar/" style="display: inline-flex; align-items: center; background-color: #ffffff; color: #24292f; border: 1px solid #d0d7de; padding: 10px 20px; border-radius: 8px; font-size: 0.95em; font-weight: 600; text-decoration: none; box-shadow: 0 1px 3px rgba(27,31,36,0.04); transition: all 0.2s ease;" onmouseover="this.style.backgroundColor='#f6f8fa'" onmouseout="this.style.backgroundColor='#ffffff'">
    <span style="margin-right: 8px;">✍️</span> Yazıları İçerikleriyle Oku (Zaman Akışı)
  </a>
</div>

<div id="archive-app" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;">
  
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

  <div style="display: flex; gap: 50px; align-items: flex-start; flex-wrap: wrap;">
    
    <!-- Sol Filtre Menüsü -->
    <div style="flex: 1; min-width: 260px; background: #fafbfc; padding: 24px; border-radius: 10px; border: 1px solid #e1e4e8;">
      <h3 style="margin-top:0; font-size:1.1em; color: #24292f; border-bottom:1px solid #e1e4e8; padding-bottom:12px; margin-bottom: 16px;">Dönem Filtresi</h3>
      <ul style="list-style: none; padding: 0; margin: 0;">
        <li style="margin-bottom: 12px;">
          <button onclick="filterPosts('all', 'all')" style="background:none; border:none; color:#0969da; cursor:pointer; font-weight:600; font-size:1em; padding:0; transition: color 0.2s;">
            ✨ Tüm Zamanlar <span style="color:#6e7781; font-weight:normal;">(<span id="total-count">0</span>)</span>
          </button>
        </li>
      </ul>
      <div id="filter-tree"></div>
    </div>

    <!-- Sağ Yazı Listesi -->
    <div style="flex: 2; min-width: 300px;">
      <h3 id="current-filter-title" style="margin-top:0; font-size: 1.6em; font-weight: 700; color: #1F2328; border-bottom: 2px solid #e1e4e8; padding-bottom: 16px; margin-bottom: 24px;">
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
  
  sortedYears.forEach(year => {
    treeHTML += `<div style="margin-top: 20px;">`;
    treeHTML += `<button onclick="filterPosts('${year}', 'all')" style="background:none; border:none; color:#24292f; cursor:pointer; font-weight:600; font-size:1.05em; padding:0; text-align:left; transition: color 0.2s;" onmouseover="this.style.color='#0969da'" onmouseout="this.style.color='#24292f'">📁 ${year} <span style="color:#6e7781; font-weight:normal; font-size:0.9em;">(${tree[year].count})</span></button>`;
    treeHTML += `<ul style="list-style:none; padding-left:20px; margin:8px 0 0 0;">`;
    
    const sortedMonths = Object.keys(tree[year].months).sort().reverse();
    sortedMonths.forEach(month => {
      const name = monthNames[month] || month;
      treeHTML += `<li style="margin-bottom:8px;"><button onclick="filterPosts('${year}', '${month}')" style="background:none; border:none; color:#57606a; cursor:pointer; font-size:0.95em; padding:0; transition: color 0.2s;" onmouseover="this.style.color='#0969da'" onmouseout="this.style.color='#57606a'">📄 ${name} <span style="color:#8c959f; font-size:0.9em;">(${tree[year].months[month]})</span></button></li>`;
    });
    
    treeHTML += `</ul></div>`;
  });
  
  document.getElementById("filter-tree").innerHTML = treeHTML;
  filterPosts('all', 'all');
});

function filterPosts(year, month) {
  const listContainer = document.getElementById("filtered-posts-list");
  const titleContainer = document.getElementById("current-filter-title");
  
  const monthNames = {
    "01": "Ocak", "02": "Şubat", "03": "Mart", "04": "Nisan", "05": "Mayıs", "06": "Haziran",
    "07": "Temmuz", "08": "Ağustos", "09": "Eylül", "10": "Ekim", "11": "Kasım", "12": "Aralık"
  };

  if (year === 'all') titleContainer.innerText = "Tüm Yazılar";
  else if (month === 'all') titleContainer.innerText = `${year} Yılı Yazıları`;
  else titleContainer.innerText = `${monthNames[month]} ${year} Yazıları`;

  const filtered = window.allPosts.filter(post => {
    const yearMatch = (year === 'all' || post.year === year);
    const monthMatch = (month === 'all' || post.month === month);
    return yearMatch && monthMatch;
  });

  if (filtered.length === 0) {
    listContainer.innerHTML = "<li style='color: #6e7781; padding: 20px 0;'>Bu dönemde yazılmış yazı bulunamadı.</li>";
    return;
  }

  // İstediğiniz gibi takvim tarihi yerine Yazar Ufuk Demir kısmı ile şık liste görünümü
  listContainer.innerHTML = filtered.map(post => `
    <li style="margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid #eaecef; display: flex; align-items: center; gap: 15px;">
      <span style="color: #6e7781; font-size: 0.9em; width: 110px; flex-shrink: 0;">✍️ Ufuk Demir</span>
      <a href="${post.url}" style="text-decoration: none; color: #0969da; font-weight: 600; font-size: 1.05em; transition: color 0.2s;" onmouseover="this.style.color='#0550ae'" onmouseout="this.style.color='#0969da'">
        ${post.date} Tarihli Çalakalem Metni
      </a>
    </li>
  `).join("");
}
</script>
