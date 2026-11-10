// Lista de los 5 personajes nigromantes disponibles
    const avataresDisponibles = [
      '/static/img/avatars/necromancer_1.png',
      '/static/img/avatars/necromancer_2.png',
      '/static/img/avatars/necromancer_3.png',
      '/static/img/avatars/necromancer_4.png',
      '/static/img/avatars/necromancer_5.png',
    ];

    const _initLobby = JSON.parse(document.getElementById('lobby-data')?.textContent || '{}');
    let currentAvatarUrl = _initLobby.avatarUrl || '';
    let avatarIndex = 0;

    // Detectar índice inicial del avatar
    (function initAvatarIndex() {
      for (let i = 0; i < avataresDisponibles.length; i++) {
        if (currentAvatarUrl.includes(`necromancer_${i+1}.png`)) {
          avatarIndex = i;
          break;
        }
      }
    })();

    function cambiarAvatarPrev() {
      avatarIndex = (avatarIndex - 1 + avataresDisponibles.length) % avataresDisponibles.length;
      currentAvatarUrl = avataresDisponibles[avatarIndex];
      const img = document.getElementById('profileModalAvatarImg');
      if (img) img.src = currentAvatarUrl;
    }

    function cambiarAvatarNext() {
      avatarIndex = (avatarIndex + 1) % avataresDisponibles.length;
      currentAvatarUrl = avataresDisponibles[avatarIndex];
      const img = document.getElementById('profileModalAvatarImg');
      if (img) img.src = currentAvatarUrl;
    }

    function seleccionarAvatarRapido(imgUrl) {
      currentAvatarUrl = imgUrl;
      const img = document.getElementById('profileModalAvatarImg');
      if (img) img.src = currentAvatarUrl;
      openModal('modalPerfil');
    }

    // Guardar cambios de Perfil (Alias + Avatar) vía AJAX
    async function guardarPerfilJugador() {
      const aliasInput = document.getElementById('inputModalAlias');
      const statusMsg = document.getElementById('profileStatusMsg');
      const btnGuardar = document.getElementById('btnGuardarPerfil');

      if (!aliasInput) return;
      const nuevoAlias = aliasInput.value.trim();

      if (!nuevoAlias) {
        statusMsg.className = 'iq-profile-status-msg error';
        statusMsg.textContent = 'El alias no puede estar vacío.';
        return;
      }

      btnGuardar.disabled = true;
      btnGuardar.innerHTML = '<i class="bi bi-hourglass-split"></i> Guardando...';
      statusMsg.className = 'iq-profile-status-msg';
      statusMsg.textContent = '';

      // Obtener CSRF Token de cookies de Django
      function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }
      const csrftoken = getCookie('csrftoken');

      try {
        const response = await fetch('/api/player/update-profile/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
          },
          body: JSON.stringify({
            alias: nuevoAlias,
            avatar: currentAvatarUrl,
          })
        });

        const data = await response.json();

        if (response.ok && data.success) {
          statusMsg.className = 'iq-profile-status-msg success';
          statusMsg.textContent = '✓ ¡Perfil actualizado exitosamente!';

          // Actualizar inmediatamente en el TopBar sin recargar la página
          const topbarAlias = document.getElementById('topbarAlias');
          if (topbarAlias) topbarAlias.textContent = data.alias;

          const topbarAvatar = document.getElementById('topbarAvatarImg');
          if (topbarAvatar && data.avatar_url) topbarAvatar.src = data.avatar_url;

          // Cerrar modal automáticamente después de 1 segundo
          setTimeout(() => {
            closeModal('modalPerfil');
            statusMsg.textContent = '';
          }, 1000);
        } else {
          statusMsg.className = 'iq-profile-status-msg error';
          statusMsg.textContent = data.error || 'Ocurrió un error al actualizar el perfil.';
        }
      } catch (err) {
        statusMsg.className = 'iq-profile-status-msg error';
        statusMsg.textContent = 'Error de conexión con el servidor.';
      } finally {
        btnGuardar.disabled = false;
        btnGuardar.innerHTML = '<i class="bi bi-check-lg"></i> Guardar Cambios';
      }
    // -----------------------------------------------------------------
    // CONTROL DE VISTAS (LOBBY VS CLASIFICACIÓN)
    // -----------------------------------------------------------------
    function switchLobbyView(viewName) {
      const btnLobby = document.getElementById('btnNavLobby');
      const btnRanking = document.getElementById('btnNavRanking');
      const viewLobbyCenter = document.getElementById('viewLobbyCenter');
      const viewRankingCenter = document.getElementById('viewRankingCenter');
      const viewLobbyRight = document.getElementById('viewLobbyRight');
      const viewRankingRight = document.getElementById('viewRankingRight');

      if (viewName === 'clasificacion') {
        if (btnRanking) btnRanking.classList.add('active');
        if (btnLobby) btnLobby.classList.remove('active');
        if (viewLobbyCenter) viewLobbyCenter.style.display = 'none';
        if (viewRankingCenter) viewRankingCenter.style.display = 'flex';
        if (viewLobbyRight) viewLobbyRight.style.display = 'none';
        if (viewRankingRight) viewRankingRight.style.display = 'flex';

        // Renderizar tabla con paginación
        renderRankTable();

        try {
          const url = new URL(window.location);
          url.searchParams.set('view', 'clasificacion');
          window.history.replaceState({}, '', url);
        } catch (e) {}
      } else {
        if (btnLobby) btnLobby.classList.add('active');
        if (btnRanking) btnRanking.classList.remove('active');
        if (viewRankingCenter) viewRankingCenter.style.display = 'none';
        if (viewLobbyCenter) viewLobbyCenter.style.display = 'flex';
        if (viewRankingRight) viewRankingRight.style.display = 'none';
        if (viewLobbyRight) viewLobbyRight.style.display = 'flex';

        try {
          const url = new URL(window.location);
          url.searchParams.delete('view');
          window.history.replaceState({}, '', url.pathname + (url.search ? url.search : ''));
        } catch (e) {}
      }
    }

    // -----------------------------------------------------------------
    // PAGINACIÓN Y FILTRADO DE LA TABLA DE CLASIFICACIÓN
    // -----------------------------------------------------------------
    const RANK_ROWS_PER_PAGE = 5;
    let currentRankPage = 1;
    let currentRankTab = 'global';

    function getVisibleRankRows() {
      const allRows = Array.from(document.querySelectorAll('#rankingTableBody .iq-rank-row'));
      if (currentRankTab === 'amigos') {
        const userArea = _initLobby.userArea || '';
        const filtered = allRows.filter(row => {
          const area = row.getAttribute('data-area') || '';
          return (userArea && area === userArea) || row.classList.contains('is-current-user');
        });
        return filtered.length > 0 ? filtered : allRows;
      }
      return allRows;
    }

    function renderRankTable() {
      const visibleRows = getVisibleRankRows();
      const allRows = document.querySelectorAll('#rankingTableBody .iq-rank-row');
      const totalPages = Math.max(1, Math.ceil(visibleRows.length / RANK_ROWS_PER_PAGE));

      if (currentRankPage > totalPages) currentRankPage = totalPages;
      if (currentRankPage < 1) currentRankPage = 1;

      // Ocultar todas las filas
      allRows.forEach(row => row.style.display = 'none');

      // Mostrar únicamente las filas de la página actual
      const startIndex = (currentRankPage - 1) * RANK_ROWS_PER_PAGE;
      const endIndex = startIndex + RANK_ROWS_PER_PAGE;
      visibleRows.slice(startIndex, endIndex).forEach(row => {
        row.style.display = '';
      });

      // Actualizar indicador de paginación y botones
      const pageDisplay = document.getElementById('rankPageDisplay');
      if (pageDisplay) {
        pageDisplay.textContent = `${currentRankPage} / ${totalPages}`;
      }

      const btnPrev = document.getElementById('btnRankPrev');
      const btnNext = document.getElementById('btnRankNext');
      if (btnPrev) btnPrev.disabled = (currentRankPage <= 1);
      if (btnNext) btnNext.disabled = (currentRankPage >= totalPages);
    }

    function prevRankPage() {
      if (currentRankPage > 1) {
        currentRankPage--;
        renderRankTable();
      }
    }

    function nextRankPage() {
      const visibleRows = getVisibleRankRows();
      const totalPages = Math.max(1, Math.ceil(visibleRows.length / RANK_ROWS_PER_PAGE));
      if (currentRankPage < totalPages) {
        currentRankPage++;
        renderRankTable();
      }
    }

    function switchRankingTab(tabName) {
      currentRankTab = tabName;
      currentRankPage = 1;

      // Actualizar clases activas en botones de pestañas
      document.querySelectorAll('.iq-rank-tab-btn').forEach(btn => {
        if (btn.getAttribute('data-tab') === tabName) {
          btn.classList.add('active');
        } else {
          btn.classList.remove('active');
        }
      });

      renderRankTable();
    }

    // Manejo de Apertura y Cierre de Modales
    function openModal(id) {
      if (id === 'modalRanking') {
        switchLobbyView('clasificacion');
        return;
      }
      const modal = document.getElementById(id);
      if (modal) {
        modal.classList.add('show');
        if (id === 'modalPerfil') {
          const statusMsg = document.getElementById('profileStatusMsg');
          if (statusMsg) statusMsg.textContent = '';
          const img = document.getElementById('profileModalAvatarImg');
          if (img && currentAvatarUrl) img.src = currentAvatarUrl;
        }
      }
    }

    function closeModal(id) {
      const modal = document.getElementById(id);
      if (modal) modal.classList.remove('show');
    }

    document.querySelectorAll('.iq-modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
          overlay.classList.remove('show');
        }
      });
    });

    // Permitir guardar con tecla Enter en el input de Alias
    document.getElementById('inputModalAlias')?.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        guardarPerfilJugador();
      }
    });

    // Inicialización al cargar la página
    document.addEventListener('DOMContentLoaded', () => {
      const urlParams = new URLSearchParams(window.location.search);
      if (urlParams.get('view') === 'clasificacion') {
        switchLobbyView('clasificacion');
      } else {
        renderRankTable();
      }
    });
