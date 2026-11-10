const _initTopbar = JSON.parse(document.getElementById('topbar-data')?.textContent || '{}');
  const globalAvailableAvatars = (_initTopbar.availableAvatars && _initTopbar.availableAvatars.length)
    ? _initTopbar.availableAvatars
    : [
        "/static/img/avatars/necromancer_1.png",
        "/static/img/avatars/necromancer_2.png",
        "/static/img/avatars/necromancer_3.png",
        "/static/img/avatars/necromancer_4.png",
        "/static/img/avatars/necromancer_5.png"
      ];

  let currentAvatarIndex = 0;
  let currentSelectedAvatarUrl = _initTopbar.avatarUrl || '';

  // Navegación de avatares con las flechas < y >
  function profileAvatarPrev() {
    if (!globalAvailableAvatars || !globalAvailableAvatars.length) return;
    currentAvatarIndex = (currentAvatarIndex - 1 + globalAvailableAvatars.length) % globalAvailableAvatars.length;
    updateProfileModalAvatarDisplay();
  }

  function profileAvatarNext() {
    if (!globalAvailableAvatars || !globalAvailableAvatars.length) return;
    currentAvatarIndex = (currentAvatarIndex + 1) % globalAvailableAvatars.length;
    updateProfileModalAvatarDisplay();
  }

  function updateProfileModalAvatarDisplay() {
    const avatarUrl = globalAvailableAvatars[currentAvatarIndex];
    if (!avatarUrl) return;
    currentSelectedAvatarUrl = avatarUrl;
    const img = document.getElementById('profileModalAvatarImg');
    if (img) {
      img.style.opacity = '0.35';
      img.style.transform = 'scale(0.92)';
      setTimeout(() => {
        img.src = avatarUrl;
        img.style.opacity = '1';
        img.style.transform = 'scale(1)';
      }, 110);
    }
  }

  // Abrir y cerrar el modal idéntico de perfil
  function openPlayerProfileModal(initialAvatarUrl) {
    const topbarImg = document.getElementById('topbarAvatarImg');
    const currentSrc = initialAvatarUrl || (topbarImg ? topbarImg.getAttribute('src') : _initTopbar.avatarUrl || '');

    // Localizar índice del avatar actual
    const matchIdx = globalAvailableAvatars.findIndex(a => currentSrc && currentSrc.includes(a.split('/').pop()));
    if (matchIdx !== -1) {
      currentAvatarIndex = matchIdx;
    }
    currentSelectedAvatarUrl = globalAvailableAvatars[currentAvatarIndex] || currentSrc;

    const modalImg = document.getElementById('profileModalAvatarImg');
    if (modalImg) {
      modalImg.src = currentSelectedAvatarUrl;
      modalImg.style.opacity = '1';
      modalImg.style.transform = 'scale(1)';
    }

    const inputAlias = document.getElementById('inputProfileModalAlias');
    const topbarAlias = document.getElementById('topbarAlias');
    if (inputAlias) {
      inputAlias.value = topbarAlias ? topbarAlias.textContent.trim() : (_initTopbar.alias || '');
    }

    const msg = document.getElementById('profileExactStatusMsg');
    if (msg) msg.textContent = '';

    const modal = document.getElementById('modalPerfilGlobal');
    if (modal) {
      modal.classList.add('active');
      modal.classList.add('show');
    }
  }

  function closePlayerProfileModal() {
    const modal = document.getElementById('modalPerfilGlobal');
    if (modal) {
      modal.classList.remove('active');
      modal.classList.remove('show');
    }
  }

  // Aliases globales de funciones para total interoperabilidad en todas las vistas
  window.openPlayerProfileModal = openPlayerProfileModal;
  window.closePlayerProfileModal = closePlayerProfileModal;
  window.openProfileModal = openPlayerProfileModal;
  window.closeProfileModal = closePlayerProfileModal;
  window.cambiarAvatarPrev = profileAvatarPrev;
  window.cambiarAvatarNext = profileAvatarNext;
  window.profileAvatarPrev = profileAvatarPrev;
  window.profileAvatarNext = profileAvatarNext;

  function openGlobalModal(modalId) {
    if (modalId === 'modalPerfil' || modalId === 'modalPerfilGlobal') {
      openPlayerProfileModal();
      return;
    }
    const el = document.getElementById(modalId);
    if (el) {
      el.classList.add('active');
      el.classList.add('show');
    }
  }

  function closeGlobalModal(modalId) {
    if (modalId === 'modalPerfil' || modalId === 'modalPerfilGlobal') {
      closePlayerProfileModal();
      return;
    }
    const el = document.getElementById(modalId);
    if (el) {
      el.classList.remove('active');
      el.classList.remove('show');
    }
  }

  // Enrutar llamadas previas de openModal / closeModal si existían
  if (typeof window.openModal !== 'function') {
    window.openModal = function(id) {
      if (id === 'modalPerfil' || id === 'modalPerfilGlobal') {
        openPlayerProfileModal();
      } else {
        openGlobalModal(id);
      }
    };
  } else {
    const originalOpenModal = window.openModal;
    window.openModal = function(id) {
      if (id === 'modalPerfil' || id === 'modalPerfilGlobal') {
        openPlayerProfileModal();
      } else {
        originalOpenModal(id);
      }
    };
  }

  if (typeof window.closeModal !== 'function') {
    window.closeModal = function(id) {
      if (id === 'modalPerfil' || id === 'modalPerfilGlobal') {
        closePlayerProfileModal();
      } else {
        closeGlobalModal(id);
      }
    };
  } else {
    const originalCloseModal = window.closeModal;
    window.closeModal = function(id) {
      if (id === 'modalPerfil' || id === 'modalPerfilGlobal') {
        closePlayerProfileModal();
      } else {
        originalCloseModal(id);
      }
    };
  }

  // Guardar cambios de Perfil (Alias + Avatar) vía AJAX
  function saveGlobalProfileChanges() {
    const aliasInput = document.getElementById('inputProfileModalAlias') || document.getElementById('inputModalAlias');
    const msg = document.getElementById('profileExactStatusMsg') || document.getElementById('profileStatusMsg');
    const btn = document.getElementById('btnSaveExactProfile') || document.getElementById('btnGuardarPerfil');
    const newAlias = aliasInput ? aliasInput.value.trim() : '';

    if (!newAlias) {
      if (msg) {
        msg.style.color = '#f87171';
        msg.textContent = 'El alias no puede estar vacío.';
      }
      return;
    }

    if (btn) btn.disabled = true;
    if (msg) {
      msg.style.color = '#c084fc';
      msg.textContent = 'Guardando cambios...';
    }

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
        alias: newAlias,
        avatar_url: currentSelectedAvatarUrl
      })
    })
    .then(r => r.json())
    .then(data => {
      if (btn) btn.disabled = false;
      if (data.success) {
        const finalAlias = data.alias || newAlias;
        const finalAvatar = data.avatar_url || currentSelectedAvatarUrl;

        // Actualizar elementos superiores del HUD de inmediato
        const topbarAlias = document.getElementById('topbarAlias');
        if (topbarAlias) topbarAlias.textContent = finalAlias;
        const topbarImg = document.getElementById('topbarAvatarImg');
        if (topbarImg) topbarImg.src = finalAvatar;

        // Actualizar posibles elementos en la vista activa (Clasificación, Lobby, etc.)
        const myPosAlias = document.getElementById('myPosAlias');
        if (myPosAlias) myPosAlias.textContent = finalAlias;
        const myPosImg = document.getElementById('myPosAvatarImg');
        if (myPosImg) myPosImg.src = finalAvatar;

        const playerRankAlias = document.getElementById('playerRankAlias');
        if (playerRankAlias) playerRankAlias.textContent = finalAlias;
        const playerRankAvatar = document.getElementById('playerRankAvatar');
        if (playerRankAvatar) playerRankAvatar.src = finalAvatar;

        if (msg) {
          msg.style.color = '#34d399';
          msg.innerHTML = '<i class="bi bi-check-circle-fill"></i> ¡Perfil actualizado con éxito!';
        }
        setTimeout(() => closePlayerProfileModal(), 750);
      } else {
        if (msg) {
          msg.style.color = '#f87171';
          msg.textContent = data.error || 'No se pudo guardar el perfil.';
        }
      }
    })
    .catch(err => {
      if (btn) btn.disabled = false;
      if (msg) {
        msg.style.color = '#f87171';
        msg.textContent = 'Error de conexión con el servidor.';
      }
    });
  }
  window.guardarPerfilJugador = saveGlobalProfileChanges;

  function openGlobalShop(cat) {
    openGlobalModal('modalTiendaGlobal');
  }

  function openGlobalMessages() {
    openGlobalModal('modalMensajesGlobal');
  }

  function openGlobalNotifs() {
    openGlobalModal('modalNotificacionesGlobal');
  }

  // Cerrar al hacer clic en el velo exterior
  window.addEventListener('click', (e) => {
    if (e.target && (e.target.id === 'modalPerfilGlobal' || e.target.id === 'modalPerfil')) {
      closePlayerProfileModal();
    } else if (e.target.classList && e.target.classList.contains('iq-global-modal-overlay')) {
      e.target.classList.remove('active');
      e.target.classList.remove('show');
    }
  });
