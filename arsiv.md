# 📚 Çalakalem Arşivi

<div style="margin: 20px 0 30px 0;">
  <a href="../yazilar/" style="display: inline-flex; align-items: center; background-color: #f6f8fa; color: #2ea44f; border: 1px solid #d0d7de; padding: 10px 20px; border-radius: 6px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-weight: 600; text-decoration: none; box-shadow: 0 1px 0 rgba(27,31,36,0.04);">
    ✍️ Yazıları İçerikleriyle Oku (Zaman Akışı) →
  </a>
</div>

Yazılmış tüm metinlerin zaman dilimlerine göre düzenlenmiş istatistiksel arşivi. Filtrelemek istediğiniz yıl veya ayın üzerine tıklayabilirsiniz.

<div id="archive-app" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; margin-top: 30px;">
  
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

  <div style="display: flex; gap: 40px; align-items: flex-start;">
    
    <div style="flex: 1; min-width: 220px; background: #f6f8fa; padding: 20px; border-radius: 6px; border: 1px solid #d0d7de;">
      <h3 style="margin-top:0; font-size:1.1em; border-bottom:1px solid #d0d7de; padding-bottom:8px;">📅 Dönem Filtresi</h3>
      <ul style="list-style: none; padding: 0; margin: 0;">
        <li style="margin-bottom: 8px;">
          <button onclick="filterPosts('all', 'all')" style="background:none; border:none; color:#0969da; cursor:pointer; font-weight:bold; font-size:1em; padding:0;">
            ✨ Tüm Zamanlar (<span id="total-count">0</span>)
          </button>
        </li>
      </ul>
      <div id="filter-tree"></div>
    </div>

    <div style="flex: 2;">
      <h3 id="current-filter-title" style="margin-top:0; color:#24292e;">Tüm Yazılar</h3>
      <ul id="filtered-posts-list" style="list-style-type: none; padding-left: 0; line-height: 1.8;">
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
    treeHTML += `<div style="margin-top: 15px;">`;
    treeHTML += `<button onclick="filterPosts('${year}', 'all')" style="background:none; border:none; color:#24292e; cursor:pointer; font-weight:bold; font-size:1.05em; padding:0; text-align:left;">📁 ${year} (${tree[year].count})</button>`;
    treeHTML += `<ul style="list-style:none; padding-left:15px; margin:5px 0 0 0;">`;
    
    const sortedMonths = Object.keys(tree[year].months).sort().reverse();
    sortedMonths.forEach(month => {
      const name = monthNames[month] || month;
      treeHTML += `<li style="margin-bottom:4px;"><button onclick="filterPosts('${year}', '${month}')" style="background:none; border:none; color:#0969da; cursor:pointer; font-size:0.95em; padding:0;">📄 ${name} (${tree[year].months[month]})</button></li>`;
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
    listContainer.innerHTML = "<li>Bu dönemde yazılmış yazı bulunamadı.</li>";
    return;
  }

  listContainer.innerHTML = filtered.map(post => `
    <li style="margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px dashed #d0d7de;">
      <span style="color: #57606a; font-size: 0.9em; margin-right: 15px;">📅 ${post.date}</span>
      <a href="${post.url}" style="text-decoration: none; color: #0969da; font-weight: 600;">
        ${post.date} Tarihli Çalakalem Metni
      </a>
    </li>
  `).join("");
}
</script>
