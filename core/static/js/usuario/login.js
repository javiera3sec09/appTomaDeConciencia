// Toggle Password Visibility
    const togglePasswordBtn = document.getElementById('togglePasswordBtn');
    const inputPassword = document.getElementById('inputPassword');
    const eyeIcon = document.getElementById('eyeIcon');

    togglePasswordBtn.addEventListener('click', function() {
      if (inputPassword.type === 'password') {
        inputPassword.type = 'text';
        eyeIcon.classList.remove('bi-eye-slash-fill');
        eyeIcon.classList.add('bi-eye-fill');
      } else {
        inputPassword.type = 'password';
        eyeIcon.classList.remove('bi-eye-fill');
        eyeIcon.classList.add('bi-eye-slash-fill');
      }
    });

    // Developer Quick Fill
    const devToggleBtn = document.getElementById('devToggleBtn');
    const devPanel = document.getElementById('devPanel');
    const closeDevPanelBtn = document.getElementById('closeDevPanelBtn');

    devToggleBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      devPanel.classList.toggle('show');
    });

    closeDevPanelBtn.addEventListener('click', function() {
      devPanel.classList.remove('show');
    });

    document.addEventListener('click', function(e) {
      if (!devPanel.contains(e.target) && e.target !== devToggleBtn) {
        devPanel.classList.remove('show');
      }
    });

    function quickFill(user, pass) {
      document.getElementById('inputUsername').value = user;
      document.getElementById('inputPassword').value = pass;
      devPanel.classList.remove('show');
      
      // Visual feedback highlight
      const card = document.querySelector('.login-card');
      card.style.boxShadow = '0 0 45px rgba(232, 121, 249, 0.9)';
      setTimeout(() => {
        card.style.boxShadow = '';
      }, 700);
    }

    // Modal Helpers for Forgot Password & Google
    const gothicModal = document.getElementById('gothicModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalDesc = document.getElementById('modalDesc');
    const modalCloseBtn = document.getElementById('modalCloseBtn');
    const forgotPwdLink = document.getElementById('forgotPwdLink');
    const googleLoginBtn = document.getElementById('googleLoginBtn');

    forgotPwdLink.addEventListener('click', function() {
      modalTitle.textContent = 'Restablecimiento Arcano';
      modalDesc.textContent = 'Para restablecer tu contraseña del Consejo o clave de acceso institucional, por favor comunícate con el Administrador de Seguridad o soporte de ISO QUEST.';
      gothicModal.classList.add('show');
    });

    googleLoginBtn.addEventListener('click', function() {
      modalTitle.textContent = 'Autenticación con Google';
      modalDesc.textContent = 'El enlace de inicio federado con Google Workspace Institucional está activo en modo protegido. Puedes utilizar tus credenciales de usuario o alias directamente.';
      gothicModal.classList.add('show');
    });

    modalCloseBtn.addEventListener('click', function() {
      gothicModal.classList.remove('show');
    });

    gothicModal.addEventListener('click', function(e) {
      if (e.target === gothicModal) {
        gothicModal.classList.remove('show');
      }
    });
