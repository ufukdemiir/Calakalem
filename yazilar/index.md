# ✍️ Tüm Çalakalem Yazıları

Bu zaman akışında, bugüne kadar yazılmış tüm serbest metinleri en yeniden en eskiye doğru bulabilirsiniz.

<div class="timeline" style="margin-top: 30px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;">
  <ul style="list-style-type: none; padding-left: 0;">
    {% assign sorted_files = site.static_files | sort: 'path' | reverse %}
    {% for file in sorted_files %}
      {% if file.path contains "yazilar/" and file.extname == ".md" and file.name != "index.md" %}
        {% assign date_str = file.name | remove: ".md" %}
        <li style="margin-bottom: 25px; border-left: 4px solid #2ea44f; padding-left: 20px; position: relative;">
          <div style="color: #57606a; font-size: 0.85em; font-weight: 600; margin-bottom: 4px;">
            📅 {{ date_str }}
          </div>
          <h3 style="margin: 0; font-size: 1.15em; line-height: 1.4;">
            <a href="{{ site.baseurl }}{{ file.path }}" style="text-decoration: none; color: #0969da; font-weight: 600;">
              Çalakalem Egzersizi: {{ date_str }}
            </a>
          </h3>
        </li>
      {% endif %}
    {% endfor %}
  </ul>
</div>
