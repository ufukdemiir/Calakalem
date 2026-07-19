# ✍️ Çalakalem Zaman Akışı

<p style="color: #6e7781; font-size: 1.1em; margin-bottom: 2.5rem; line-height: 1.6;">
  Kusursuzluk baskısından uzak, alelacele ve gelişigüzel yazılmış tüm serbest metinler.
</p>

<!-- Şık Buton -->
<div style="margin-bottom: 4rem;">
  <a href="../arsiv/" style="display: inline-flex; align-items: center; background-color: #ffffff; color: #24292f; border: 1px solid #d0d7de; padding: 10px 20px; border-radius: 8px; font-size: 0.95em; font-weight: 600; text-decoration: none; box-shadow: 0 1px 3px rgba(27,31,36,0.04); transition: all 0.2s ease;" onmouseover="this.style.backgroundColor='#f6f8fa'" onmouseout="this.style.backgroundColor='#ffffff'">
    <span style="margin-right: 8px;">📚</span> Yıllara ve Aylara Göre Filtreli Arşive Git
  </a>
</div>

<div id="posts-wrapper" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;">
  
  {% assign sorted_files = site.static_files | sort: 'path' | reverse %}
  {% for file in sorted_files %}
    {% if file.path contains "yazilar/" and file.extname == ".md" and file.name != "index.md" %}
      {% assign date_str = file.name | remove: ".md" %}
      
      <!-- Yazı Kartı -->
      <article class="post-item" style="display: none; margin-bottom: 4rem; padding-bottom: 3rem; border-bottom: 1px solid #e1e4e8;">
        
        <header style="margin-bottom: 1.5rem;">
          <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px; font-size: 0.95em;">
            <span style="color: #57606a; font-weight: 500;">✍️ Ufuk Demir</span>
            <span style="color: #d0d7de;">•</span>
            <span style="color: #6e7781;">{{ date_str }}</span>
          </div>
          <h2 style="margin: 0; font-size: 1.8em; font-weight: 700; line-height: 1.2; letter-spacing: -0.02em;">
            <a href="{{ site.baseurl }}{{ file.path }}" style="text-decoration: none; color: #1F2328;" onmouseover="this.style.color='#0969da'" onmouseout="this.style.color='#1F2328'">
              {{ date_str }}
            </a>
          </h2>
        </header>

        <div class="post-content" style="color: #24292f; line-height: 1.8; font-size: 1.1em;">
          {% capture file_content %}{% include_relative {{ file.name }} %}{% endcapture %}
          {{ file_content | markdownify }}
        </div>
        
      </article>

    {% endif %}
  {% endfor %}

</div>

<!-- Sayfalama (Pagination) Kontrolleri -->
<div id="pagination-controls" style="display: flex; justify-content: center; align-items: center; gap: 8px; margin-top: 2rem; margin-bottom: 5rem; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
  <!-- JS ile sayfa butonları buraya eklenecek -->
</div>

<script>
document.addEventListener("DOMContentLoaded", function() {
  const posts = document.querySelectorAll('.post-item');
  const postsPerPage = 10; // Her sayfada görünecek yazı sayısı
  const totalPages = Math.ceil(posts.length / postsPerPage);
  let currentPage = 1;

  function renderPosts() {
    posts.forEach((post, index) => {
      post.style.display = 'none';
      if (index >= (currentPage - 1) * postsPerPage && index < currentPage * postsPerPage) {
        post.style.display = 'block';
      }
    });
    renderPagination();
    // Sayfa değiştiğinde yumuşakça en üste kaydırır
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function createButton(text, pageNum, disabled = false, active = false) {
    const btn = document.createElement('button');
    btn.innerHTML = text;
    btn.disabled = disabled;
    
    let baseStyle = "min-width: 36px; height: 36px; padding: 0 10px; border-radius: 6px; font-size: 0.95em; font-weight: 500; cursor: pointer; transition: all 0.2s ease; border: 1px solid ";
    
    if (active) {
      btn.style = baseStyle + "#d0d7de; background-color: #f6f8fa; color: #24292f;";
    } else if (disabled) {
      btn.style = baseStyle + "transparent; background-color: transparent; color: #8c959f; cursor: default;";
      btn.style.opacity = "0.5";
    } else {
      btn.style = baseStyle + "transparent; background-color: transparent; color: #0969da;";
      btn.onmouseover = () => { btn.style.backgroundColor = '#f3f4f6'; };
      btn.onmouseout = () => { btn.style.backgroundColor = 'transparent'; };
    }

    if (!disabled && !active) {
      btn.addEventListener('click', () => {
        currentPage = pageNum;
        renderPosts();
      });
    }
    return btn;
  }

  function renderPagination() {
    const container = document.getElementById('pagination-controls');
    container.innerHTML = '';

    if (totalPages <= 1) return; // Tek sayfaysa gizle

    // << ve <
    container.appendChild(createButton('«', 1, currentPage === 1));
    container.appendChild(createButton('‹', currentPage - 1, currentPage === 1));

    // Numaralar
    let startPage = Math.max(1, currentPage - 2);
    let endPage = Math.min(totalPages, currentPage + 2);

    if (currentPage <= 2) endPage = Math.min(totalPages, 5);
    if (currentPage >= totalPages - 1) startPage = Math.max(1, totalPages - 4);

    for (let i = startPage; i <= endPage; i++) {
      container.appendChild(createButton(i, i, false, i === currentPage));
    }

    // > ve >>
    container.appendChild(createButton('›', currentPage + 1, currentPage === totalPages));
    container.appendChild(createButton('»', totalPages, currentPage === totalPages));
  }

  renderPosts();
});
</script>
