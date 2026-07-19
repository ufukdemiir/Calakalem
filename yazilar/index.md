# ✍️ Çalakalem Zaman Akışı

Kusursuzluk baskısından uzak, alelacele ve gelişigüzel yazılmış tüm serbest metinler.

> 📂 Tüm yazıları yıllara ve aylara göre filtrelenmiş olarak görmek ve istatistikleri incelemek için **[📚 ÇALAKALEM ARŞİVİ](../arsiv/)** sayfasına göz atabilirsiniz.

<div class="timeline" style="margin-top: 30px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;">
  
  {% assign sorted_files = site.static_files | sort: 'path' | reverse %}
  {% for file in sorted_files %}
    {% if file.path contains "yazilar/" and file.extname == ".md" and file.name != "index.md" %}
      {% assign date_str = file.name | remove: ".md" %}
      
      <article style="margin-bottom: 50px; border-left: 4px solid #2ea44f; padding-left: 25px; position: relative;">
        
        <header style="margin-bottom: 15px;">
          <span style="color: #57606a; font-size: 0.9em; font-weight: 600; display: block; margin-bottom: 5px;">
            ✍️ Yazar: Ufuk Demir
          </span>
          <h2 style="margin: 0; font-size: 1.5em; line-height: 1.3;">
            <a href="{{ site.baseurl }}{{ file.path }}" style="text-decoration: none; color: #0969da; font-weight: 700;">
              📅 {{ date_str }}
            </a>
          </h2>
        </header>

        <div class="post-content" style="color: #24292e; line-height: 1.6; font-size: 1.1em; text-align: justify;">
          {% capture file_content %}{% include_relative {{ file.name }} %}{% endcapture %}
          {{ file_content | markdownify }}
        </div>

        <hr style="height: 1px; background-color: #e1e4e8; border: none; margin-top: 30px; margin-bottom: 0;">
      </article>

    {% endif %}
  {% endfor %}

</div>
