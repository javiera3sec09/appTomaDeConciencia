// Gestión del Modal de Perfil para el Administrador
    const adminAvataresDisponibles = [
      '/static/img/avatars/necromancer_1.png',
      '/static/img/avatars/necromancer_2.png',
      '/static/img/avatars/necromancer_3.png',
      '/static/img/avatars/necromancer_4.png',
      '/static/img/avatars/necromancer_5.png',
    ];

    let currentAdminAvatar = document.getElementById('adminTopbarAvatar')?.getAttribute('src') || '/static/img/avatars/necromancer_3.png';
    let adminAvatarIdx = 2; // Default necromancer_3

    (function initAdminAvatarIndex() {
      for (let i = 0; i < adminAvataresDisponibles.length; i++) {
        if (currentAdminAvatar.includes(`necromancer_${i+1}.png`)) {
          adminAvatarIdx = i;
          break;
        }
      }
    })();

    function openAdminProfileModal() {
      const modal = document.getElementById('modalPerfil');
      if (modal) {
        modal.classList.add('show');
        const img = document.getElementById('adminProfileModalAvatarImg');
        if (img && currentAdminAvatar) img.src = currentAdminAvatar;
        const msg = document.getElementById('adminProfileStatusMsg');
        if (msg) msg.textContent = '';
      }
    }

    function closeAdminProfileModal() {
      const modal = document.getElementById('modalPerfil');
      if (modal) modal.classList.remove('show');
    }

    function adminAvatarPrev() {
      adminAvatarIdx = (adminAvatarIdx - 1 + adminAvataresDisponibles.length) % adminAvataresDisponibles.length;
      currentAdminAvatar = adminAvataresDisponibles[adminAvatarIdx];
      const img = document.getElementById('adminProfileModalAvatarImg');
      if (img) img.src = currentAdminAvatar;
    }

    function adminAvatarNext() {
      adminAvatarIdx = (adminAvatarIdx + 1) % adminAvataresDisponibles.length;
      currentAdminAvatar = adminAvataresDisponibles[adminAvatarIdx];
      const img = document.getElementById('adminProfileModalAvatarImg');
      if (img) img.src = currentAdminAvatar;
    }

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

    async function guardarAdminPerfil() {
      const input = document.getElementById('inputAdminModalAlias');
      const statusMsg = document.getElementById('adminProfileStatusMsg');
      const btnGuardar = document.getElementById('btnAdminGuardarPerfil');
      if (!input) return;
      const nuevoAlias = input.value.trim();

      if (!nuevoAlias) {
        statusMsg.className = 'iq-profile-status-msg error';
        statusMsg.textContent = 'El alias no puede estar vacío.';
        return;
      }

      if (btnGuardar) {
        btnGuardar.disabled = true;
        btnGuardar.innerHTML = '<i class="bi bi-hourglass-split"></i> Guardando...';
      }
      statusMsg.className = 'iq-profile-status-msg';
      statusMsg.textContent = '';

      const csrftoken = getCookie('csrftoken') || (document.querySelector('[name=csrfmiddlewaretoken]')?.value);

      try {
        const resp = await fetch('/api/player/update-profile/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
          },
          body: JSON.stringify({
            alias: nuevoAlias,
            avatar: currentAdminAvatar,
          })
        });

        const res = await resp.json();
        if (res.success) {
          statusMsg.className = 'iq-profile-status-msg success';
          statusMsg.textContent = '✓ ¡Perfil actualizado exitosamente!';

          const topbarAlias = document.getElementById('adminTopbarAlias');
          if (topbarAlias) topbarAlias.textContent = res.alias;

          const topbarAvatar = document.getElementById('adminTopbarAvatar');
          if (topbarAvatar && res.avatar_url) topbarAvatar.src = res.avatar_url;

          setTimeout(() => {
            closeAdminProfileModal();
            statusMsg.textContent = '';
          }, 900);
        } else {
          statusMsg.className = 'iq-profile-status-msg error';
          statusMsg.textContent = res.error || 'Ocurrió un error al actualizar.';
        }
      } catch (err) {
        statusMsg.className = 'iq-profile-status-msg error';
        statusMsg.textContent = 'Error de conexión con el servidor.';
      } finally {
        if (btnGuardar) {
          btnGuardar.disabled = false;
          btnGuardar.innerHTML = '<i class="bi bi-check-lg"></i> Guardar Cambios';
        }
      }
    }

    document.getElementById('modalPerfil')?.addEventListener('click', function(e) {
      if (e.target === this) closeAdminProfileModal();
    });

    document.getElementById('inputAdminModalAlias')?.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        guardarAdminPerfil();
      }
    });
