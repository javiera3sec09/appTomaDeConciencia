function selectAvatarFromColeccion(imgUrl, cardEl) {
      document.querySelectorAll('.iq-avatar-card-item').forEach(c => c.classList.remove('selected'));
      cardEl.classList.add('selected');

      const csrftoken = (function() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === 'csrftoken=') {
              cookieValue = decodeURIComponent(cookie.substring(10));
              break;
            }
          }
        }
        return cookieValue || document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
      })();

      fetch('/api/player/update-profile/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
          alias: document.getElementById('topbarAlias').textContent.trim(),
          avatar_url: imgUrl
        })
      })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          const topbarImg = document.getElementById('topbarAvatarImg');
          if (topbarImg) topbarImg.src = data.avatar_url || imgUrl;
        }
      })
      .catch(console.error);
    }
