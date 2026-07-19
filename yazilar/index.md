# Çalakalem

<p style="color: #555; font-size: 1.15rem; font-family: 'Georgia', serif; font-style: italic; margin-bottom: 3rem; line-height: 1.6;">
  Kusursuzluk baskısından uzak, alelacele ve gelişigüzel yazılmış serbest metinler.
</p>

<!-- Şık Navigasyon Butonu -->
<div style="margin-bottom: 5rem; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
  <a href="../arsiv/" style="display: inline-block; color: #111; border-bottom: 1px solid #111; padding-bottom: 4px; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; text-decoration: none; transition: opacity 0.2s ease;" onmouseover="this.style.opacity='0.6'" onmouseout="this.style.opacity='1'">
    Arşivi Görüntüle →
  </a>
</div>

<div id="posts-wrapper">
  
  {% assign sorted_files = site.static_files | sort: 'path' | reverse %}
  {% for file in sorted_files %}
    {% if file.path contains "yazilar/" and file.extname == ".md" and file.name != "index.md" %}
      {% assign date_str = file.name | remove: ".md" %}
      
      <!-- Zarif Yazı Kartı (Sola Yaslı) -->
      <article class="post-item" style="display: none; margin-bottom: 6rem;">
        
        <header style="margin-bottom: 2rem; text-align: left;">
          <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 0.85rem; color: #888; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px;">
            Ufuk Demir
          </div>
          <h2 style="margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 2.2rem; font-weight: 800; letter-spacing: -0.04em;">
            <a href="{{ site.baseurl }}{{ file.path }}" style="text-decoration: none; color: #111; transition: color 0.2s ease;" onmouseover="this.style.color='#555'" onmouseout="this.style.color='#111'">
              {{ date_str }}
            </a>
          </h2>
        </header>

        <div class="post-content" style="color: #222; line-height: 1.9; font-size: 1.15rem; font-family: 'Georgia', serif; text-align: justify;">
          {% capture file_content %}{% include_relative {{ file.name }} %}{% endcapture %}
          {{ file_content | markdownify }}
        </div>

        <div style="text-align: left; margin-top: 4rem;">
          <span style="display: inline-block; width: 40px; height: 1px; background-color: #ddd;"></span>
        </div>
        
      </article>

    {% endif %}
  {% endfor %}

</div>

<!-- Minimalist Sayfalama Kontrolleri -->
<div id="pagination-controls" style="display: flex; justify-content: flex-start; align-items: center; gap: 12px; margin-top: 2rem; margin-bottom: 5rem; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
</div>

<script>
document.addEventListener("DOMContentLoaded", function() {
  const favicon = document.createElement('link');
  favicon.rel = 'icon';
  favicon.href = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">💠</text></svg>';
  document.head.appendChild(favicon);

  const posts = document.querySelectorAll('.post-item');
  const postsPerPage = 10;
  const totalPages = Math.ceil(posts.length / postsPerPage);
  let currentPage = 1;

  function renderPosts() {
    posts.forEach((post, index) => {
      post.style.display = 'none';
      if (index >= (currentPage - 1) * postsPerPage && index < currentPage * postsPerPage) {
        post.style.display = 'block';
        post.style.animation = 'fadeIn 0.5s ease';
      }
    });
    renderPagination();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function createButton(text, pageNum, disabled = false, active = false) {
    const btn = document.createElement('button');
    btn.innerHTML = text;
    btn.disabled = disabled;
    
    let baseStyle = "background: none; border: none; font-size: 1rem; font-weight: 500; cursor: pointer; transition: all 0.2s ease; padding: 5px 10px; ";
    
    if (active) {
      btn.style = baseStyle + "color: #111; border-bottom: 2px solid #111;";
    } else if (disabled) {
      btn.style = baseStyle + "color: #ccc; cursor: default;";
    } else {
      btn.style = baseStyle + "color: #888;";
      btn.onmouseover = () => { btn.style.color = '#111'; };
      btn.onmouseout = () => { btn.style.color = '#888'; };
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
    if (totalPages <= 1) return;

    container.appendChild(createButton('«', 1, currentPage === 1));
    container.appendChild(createButton('‹', currentPage - 1, currentPage === 1));

    let startPage = Math.max(1, currentPage - 2);
    let endPage = Math.min(totalPages, currentPage + 2);

    if (currentPage <= 2) endPage = Math.min(totalPages, 5);
    if (currentPage >= totalPages - 1) startPage = Math.max(1, totalPages - 4);

    for (let i = startPage; i <= endPage; i++) {
      container.appendChild(createButton(i, i, false, i === currentPage));
    }

    container.appendChild(createButton('›', currentPage + 1, currentPage === totalPages));
    container.appendChild(createButton('»', totalPages, currentPage === totalPages));
  }

  renderPosts();
});
</script>
<style>
  @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
  .post-content p { margin-bottom: 1.5rem; }
</style>
