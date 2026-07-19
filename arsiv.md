---
layout: null
permalink: /arsiv/
---

<!-- Ana kapsayıcı (Sayfayı merkeze alır ve genişliği korur) -->
<div style="max-width: 900px; margin: 0 auto; padding: 40px 20px;">

  <!-- Kalın Başlık -->
  <h1 style="font-weight: 800; font-size: 2.8rem; letter-spacing: -0.05em; color: #111; margin-top: 0; margin-bottom: 0.5rem;">
    Arşiv
  </h1>

  <p style="color: #555; font-size: 1.15rem; font-family: 'Georgia', serif; font-style: italic; margin-bottom: 3rem; line-height: 1.6;">
    Yazılmış tüm metinlerin zaman dilimlerine göre düzenlenmiş dizini.
  </p>

  <!-- Şık Navigasyon Butonu -->
  <div style="margin-bottom: 4rem; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
    <a href="../yazilar/" style="display: inline-block; color: #111; border-bottom: 1px solid #111; padding-bottom: 4px; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; text-decoration: none; transition: opacity 0.2s ease;" onmouseover="this.style.opacity='0.6'" onmouseout="this.style.opacity='1'">
      ← Akışa Dön
    </a>
  </div>

  <div id="archive-app" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
    
    <!-- Veri Kaynağı (Gizli) -->
    <div id="raw-data" style="display:none;">
      {% assign sorted_files = site.static_files | sort: 'path' | reverse %}
      {% for file in sorted_files %}
        {% if file.path contains "yazilar/" and file.extname == ".md" and file.name != "index.md" %}
          {% assign date_str = file.name | remove: ".md" %}
          {% assign parts = date_str | split: "-" %}
          <span data-url="{{ file.path | replace: '../', '/' }}" data-date="{{ date_str }}" data-year="{{ parts[0] }}" data-month="{{ parts[1] }}"></span>
        {% endif %}
      {% endfor %}
    </div>

    <div style="display: flex; gap: 60px; align-items: flex-start; flex-wrap: wrap;">
      
      <!-- Açılır Kapanır Sol Menü -->
      <div style="flex: 1; min-width: 200px;">
        <h3 style="margin-top:0; font-size:0.85rem; text-transform: uppercase; letter-spacing: 2px; color: #888; border-bottom: 1px solid #eee; padding-bottom:12px; margin-bottom: 20px;">Dizin</h3>
        <ul style="list-style: none; padding: 0; margin: 0;">
          <li style="margin-bottom: 24px;">
            <button id="menu-btn-all-all" onclick="setFilter('all', 'all')" style="background:none; border:none; color:#111; cursor:pointer; font-weight:700; font-size:1.1rem; padding:0; transition: opacity 0.2s;" onmouseover="this.style.opacity='0.6'" onmouseout="this.style.opacity='1'">
              Tüm Zamanlar <span style="color:#aaa; font-weight:400; font-size:0.9rem; margin-left: 4px;">(<span id="total-count">0</span>)</span>
            </button>
          </li>
        </ul>
        <div id="filter-tree"></div>
      </div>

      <!-- Zarif Liste Görünümü & Arama -->
      <div style="flex: 2; min-width: 300px;">
        
        <!-- Canlı Arama Kutusu -->
        <div style="margin-bottom: 24px; position: relative;">
          <input type="text" id="search-input" onkeyup="handleSearch(this.value)" placeholder="Yazılar içinde ara..." style="width: 100%; box-sizing: border-box; padding: 12px 16px; font-size: 1rem; font-family: inherit; color: #111; border: 1px solid #eaeaea; border-radius: 6px; background: #fafafa; outline: none; transition: all 0.2s ease;" onfocus="this.style.borderColor='#111'; this.style.background='#fff';" onblur="this.style.borderColor='#eaeaea'; this.style.background='#fafafa';">
        </div>

        <!-- Dinamik Başlık ve Sayaç -->
        <h3 style="margin-top:0; font-size: 2rem; font-weight: 800; letter-spacing: -0.04em; color: #111; border-bottom: 1px solid #eee; padding-bottom: 16px; margin-bottom: 30px; display: flex; align-items: baseline; gap: 10px;">
          <span id="current-filter-title">Tüm Yazılar</span>
          <span id="current-result-count" style="font-size: 1.1rem; font-weight: 400; color: #888;"></span>
        </h3>
        
        <!-- Liste İçeriği -->
        <ul id="filtered-posts-list" style="list-style-type: none; padding-left: 0; margin: 0;">
          <!-- JS ile dolacak -->
        </ul>
      </div>

    </div>
  </div>
</div> <!-- Ana kapsayıcı sonu -->

<script>
// Global Durum (State) Yönetimi
window.archiveState = {
  year: 'all',
  month: 'all',
  query: ''
};

window.monthNames = { "01": "Ocak", "02": "Şubat", "03": "Mart", "04": "Nisan", "05": "Mayıs", "06": "Haziran", "07": "Temmuz", "08": "Ağustos", "09": "Eylül", "10": "Ekim", "11": "Kasım", "12": "Aralık" };

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

  // Ağaç Yapısını Oluşturma (Ayrıca menülere ID eklendi)
  let treeHTML = "";
  Object.keys(tree).sort().reverse().forEach((year, index) => {
    const isFirst = index === 0;
    treeHTML += `<div style="margin-top: 20px;">
      <button id="menu-btn-${year}-all" class="tree-menu-btn" onclick="toggleYear('${year}')" style="background:none; border:none; color:#555; cursor:pointer; font-weight:700; font-size:1.1rem; padding:0; text-align:left; transition: opacity 0.2s;" onmouseover="this.style.opacity='0.6'" onmouseout="this.style.opacity='1'">
        <span id="icon-${year}" style="display:inline-block; width:18px; font-size:0.9em; color:#888;">${isFirst ? '▾' : '▸'}</span>${year} <span style="color:#aaa; font-weight:400; font-size:0.9rem; margin-left: 4px;">(${tree[year].count})</span>
      </button>
      <ul id="months-${year}" style="list-style:none; padding-left:18px; border-left: 1px solid #eee; margin:12px 0 0 7px; display: ${isFirst ? 'block' : 'none'};">`;
    Object.keys(tree[year].months).sort().reverse().forEach(month => {
      treeHTML += `<li style="margin-bottom:10px;"><button id="menu-btn-${year}-${month}" class="tree-menu-btn" onclick="setFilter('${year}', '${month}')" style="background:none; border:none; color:#777; cursor:pointer; font-size:0.95rem; padding:0; transition: color 0.2s;" onmouseover="this.style.color='#111'" onmouseout="this.style.color='#777'">${window.monthNames[month]} <span style="color:#ccc; font-size:0.85rem; margin-left: 4px;">(${tree[year].months[month]})</span></button></li>`;
    });
    treeHTML += `</ul></div>`;
  });
  
  document.getElementById("filter-tree").innerHTML = treeHTML;
  setFilter('all', 'all'); // Başlangıç render'ı
});

// Arama Tetikleyicisi
window.handleSearch = function(query) {
  window.archiveState.query = query.toLowerCase();
  renderPosts();
};

// Açılır Kapanır Yıl Butonu
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
  setFilter(year, 'all');
};

// Filtre Ayarlayıcı ve Arayüz Güncelleyici
window.setFilter = function(year, month) {
  window.archiveState.year = year;
  window.archiveState.month = month;
  
  // Menü Aktif Durum Stilleri
  document.querySelectorAll('.tree-menu-btn').forEach(btn => btn.style.color = '#777');
  document.getElementById('menu-btn-all-all').style.color = '#111';
  document.getElementById('menu-btn-all-all').style.fontWeight = '700';

  if (year !== 'all') {
    document.getElementById('menu-btn-all-all').style.color = '#555';
    document.getElementById('menu-btn-all-all').style.fontWeight = 'normal';
    
    // Yıl başlığını veya ay butonunu koyulaştır
    const targetBtn = document.getElementById(`menu-btn-${year}-${month}`);
    if(targetBtn) {
      targetBtn.style.color = '#111';
    }
  }

  // Arama kutusunu sıfırla (Kullanıcı menüye tıklarsa arama temizlenir)
  document.getElementById("search-input").value = "";
  window.archiveState.query = "";

  renderPosts();
};

// Nihai Listeyi Ekrana Çizme (Render)
window.renderPosts = function() {
  const { year, month, query } = window.archiveState;
  const listContainer = document.getElementById("filtered-posts-list");
  const titleContainer = document.getElementById("current-filter-title");
  const countContainer = document.getElementById("current-result-count");

  // Başlığı Ayarla
  titleContainer.innerText = (year === 'all') ? "Tüm Yazılar" : (month === 'all') ? `${year}` : `${window.monthNames[month]} ${year}`;

  // Filtreleme Algoritması (Yıl + Ay + Arama Sorgusu)
  const filtered = window.allPosts.filter(p => {
    const yearMatch = (year === 'all' || p.year === year);
    const monthMatch = (month === 'all' || p.month === month);
    const searchMatch = (query === '' || p.date.toLowerCase().includes(query));
    return yearMatch && monthMatch && searchMatch;
  });

  // Sonuç Sayısını Ekle
  countContainer.innerText = `(${filtered.length})`;

  // HTML Üretimi
  if (filtered.length === 0) {
    listContainer.innerHTML = "<li style='color: #888; font-style: italic; padding: 20px 0;'>Bu arama kriterlerine uygun bir metin bulunamadı.</li>";
    return;
  }

  listContainer.innerHTML = filtered.map(post => `
    <li style="margin-bottom: 20px; display: flex; align-items: baseline; gap: 20px;">
      <a href="https://github.com/ufukdemiir" target="_blank" style="text-decoration: none; color: #aaa; font-size: 0.85rem; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; width: 100px; flex-shrink: 0; transition: opacity 0.2s;" onmouseover="this.style.opacity='0.6'" onmouseout="this.style.opacity='1'">UFUK DEMİR</a>
      <a href="${post.url}" style="text-decoration: none; color: #111; font-weight: 600; font-size: 1.15rem; transition: opacity 0.2s;" onmouseover="this.style.opacity='0.5'" onmouseout="this.style.opacity='1'">
        ${post.date}
      </a>
    </li>`).join("");
};
</script>
