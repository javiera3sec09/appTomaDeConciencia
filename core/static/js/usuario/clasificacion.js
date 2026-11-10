// Datos reales de todos los jugadores de la base de datos
    const _initClasif = JSON.parse(document.getElementById('clasificacion-data')?.textContent || '{}');
    const allRankingPlayers = _initClasif.rankingPlayers || [];
    const rankPageSize = 5;
    let currentRankPage = 1;
    const totalRankPages = Math.max(1, Math.ceil((allRankingPlayers.length || 1) / rankPageSize));

    // Variables de estado
    let selectedAvatarUrl = _initClasif.avatarUrl || '';

    function formatNumberRank(num) {
      return Number(num).toLocaleString('es-ES');
    }

    function escapeHtmlRank(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    function renderRankPage(page) {
      const tbody = document.getElementById('rankingTableBody');
      if (!tbody) return;

      const startIndex = (page - 1) * rankPageSize;
      const pagePlayers = allRankingPlayers.slice(startIndex, startIndex + rankPageSize);

      if (pagePlayers.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="4" style="text-align: center; color: #cbd5e1; padding: 20px; font-weight: 600;">
              No hay jugadores clasificados.
            </td>
          </tr>
        `;
        return;
      }

      let html = '';
      pagePlayers.forEach((player) => {
        const isGold = (player.rank === 1);
        let rankBadge = '';
        if (player.rank === 1) {
          rankBadge = '<i class="bi bi-crown-fill iq-rank-crown-icon gold" title="1° Lugar"></i>';
        } else if (player.rank === 2) {
          rankBadge = '<i class="bi bi-crown-fill iq-rank-crown-icon silver" title="2° Lugar"></i>';
        } else if (player.rank === 3) {
          rankBadge = '<i class="bi bi-crown-fill iq-rank-crown-icon bronze" title="3° Lugar"></i>';
        } else {
          rankBadge = `<span class="iq-rank-number-text">${player.rank}</span>`;
        }

        const avatarUrl = escapeHtmlRank(player.avatar_url || '/static/img/avatars/necromancer_1.png');
        const alias = escapeHtmlRank(player.alias || 'Jugador');
        const nivel = player.nivel;
        const xpFormatted = formatNumberRank(player.xp);

        html += `
          <tr class="${isGold ? 'is-gold-row' : ''}" data-user-id="${player.user_id}">
            <td class="iq-cl-td-rank">
              ${rankBadge}
            </td>
            <td class="iq-cl-td-player">
              <div class="iq-player-cell-box">
                <img src="${avatarUrl}" alt="${alias}" class="iq-cell-avatar" onerror="this.src='/static/img/avatars/necromancer_1.png'">
                <span class="iq-cell-name">${alias}</span>
              </div>
            </td>
            <td class="iq-cl-td-level">Nv. ${nivel}</td>
            <td class="iq-cl-td-xp">${xpFormatted} XP</td>
          </tr>
        `;
      });

      tbody.innerHTML = html;
    }

    // Abrir y Cerrar Modal de Perfil
    function openProfileModal() {
      if (typeof openPlayerProfileModal === 'function') {
        openPlayerProfileModal();
      } else {
        const m = document.getElementById('modalPerfil');
        if (m) m.classList.add('show');
      }
    }

    function closeProfileModal() {
      document.getElementById('modalPerfil').classList.remove('show');
    }

    // Selección de Avatar en el modal
    function selectAvatarOption(cardElem, imgUrl) {
      document.querySelectorAll('.iq-avatar-option-card').forEach(el => el.classList.remove('selected'));
      cardElem.classList.add('selected');
      selectedAvatarUrl = imgUrl;
    }

    // Guardar cambios vía AJAX
    function saveProfileChanges() {
      const alias = document.getElementById('inputAlias').value.trim();
      if (!alias) {
        alert('Por favor, ingresa un alias válido.');
        return;
      }

      fetch(_initClasif.updateProfileUrl || '/api/player/update-profile/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': (function() { const m = document.cookie.match(/csrftoken=([^;]+)/); if (m) return m[1]; return document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''; })()
        },
        body: JSON.stringify({
          alias: alias,
          avatar_url: selectedAvatarUrl
        })
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          // Actualizar UI inmediatamente
          document.getElementById('topbarAlias').textContent = alias;
          document.getElementById('topbarAvatarImg').src = selectedAvatarUrl;
          const myPosAlias = document.getElementById('myPosAlias');
          if (myPosAlias) myPosAlias.textContent = alias;
          const myPosImg = document.getElementById('myPosAvatarImg');
          if (myPosImg) myPosImg.src = selectedAvatarUrl;
          closeProfileModal();
        } else {
          alert('Error al guardar: ' + (data.error || 'Intente nuevamente'));
        }
      })
      .catch(err => {
        console.error(err);
        // Fallback local en caso de requerir refresh
        document.getElementById('topbarAlias').textContent = alias;
        document.getElementById('topbarAvatarImg').src = selectedAvatarUrl;
        closeProfileModal();
      });
    }


    // Paginación de la Tabla de Clasificación (< 1 / N >)
    function changeRankPage(delta) {
      const newPage = currentRankPage + delta;
      if (newPage < 1 || newPage > totalRankPages) return;

      currentRankPage = newPage;
      const textElem = document.getElementById('rankPageText');
      if (textElem) textElem.textContent = currentRankPage + ' / ' + totalRankPages;

      const btnPrev = document.getElementById('btnPagePrev');
      const btnNext = document.getElementById('btnPageNext');
      if (btnPrev) btnPrev.disabled = (currentRankPage === 1);
      if (btnNext) btnNext.disabled = (currentRankPage === totalRankPages);

      const tbody = document.getElementById('rankingTableBody');
      if (tbody) {
        tbody.style.opacity = '0.4';
        setTimeout(() => {
          renderRankPage(currentRankPage);
          tbody.style.opacity = '1';
        }, 120);
      } else {
        renderRankPage(currentRankPage);
      }
    }

    // Cerrar modal al presionar Escape o clic fuera
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeProfileModal();
    });

    const modalPerfilElem = document.getElementById('modalPerfil');
    if (modalPerfilElem) {
      modalPerfilElem.addEventListener('click', (e) => {
        if (e.target.id === 'modalPerfil') closeProfileModal();
      });
    }
